import random
import types

from util import random_bit_string, xor_bits, flip_bit, sha256_of_bits, H, find_i_tuple

# the preprocess algorithm from the article
def preprocess(l, T, m, k=12):
    if T > l:
        raise Exception("T must be less than l")
    if k > m:
        raise Exception("k must be less than m")

    C = ['0'*m]*l
    P = ['0'*k]*l

    for i in range(0, l):
        P[i] = random_bit_string(k)
        ri = random_bit_string(m-k)
        ai = int(i > T)

        if xor_bits(ri) != ai:
            ri = flip_bit(ri, random.randint(0, m-k-1))

        yi = P[i] + ri
        C[i] = sha256_of_bits(yi)[:m]
    return C, P

# the probeThreshold algorithm from the article
def queryThreshold(i, l,m,k,C,P):
    i = i % l
    # if i > l:
    #     raise Exception("i must be less than l")
    if k > m:
        raise Exception("k must be less than m")

    while True:
        a = random_bit_string(m)
        ha = sha256_of_bits(a)[:m]
        if ha == C[i] and a[:k] == P[i]:
            return xor_bits(a[k:])

# class defining a single process and the protocols it can compute
class Process:
    def __init__(self, id, A, present, D):
        self.id = id # unique identifier of the process, used as an index in shared objects
        #shared objects
        self.A = A #lx2 array
        self.present = present #lx2 array
        self.D = D #rx2xn-array

    # the approximateAgreement protocol from the article
    def approximate_agreement(self, inp, s):
        i = inp
        for r in range(0, s):
            self.A[r][i % 2] = i
            yield
            i_tag = self.A[r][(i+1) % 2]
            yield
            if i_tag == None:
                i = 2*i
            else:
                i = i + i_tag
        yield i

    # the thresholdConciliator protocol from the article
    def treshold_conciliator(self, inp, f, s):
        for i in self.approximate_agreement(inp, s): yield
        yield f(i)

    # the adopt-commit protocol from https://www.cs.tau.ac.il/~afek/EliRndByRndpodc98.pdf page 149
    def adopt_commit(self, r, vi):
        i = self.id
        self.D[r][1][i] = vi # write vi to Ci,1
        yield
        # V:= U_j=1...n read Cj,1
        V = set()
        for j in range(len(self.D[r][1])):
            V.add(self.D[r][1][j])
            yield
        #if V - {\perp} = {v}
        V.remove(None)
        if len(V) == 1:
            v = V.pop()
            self.D[r][2][i] = ('commit', v)
        else:
            self.D[r][2][i] = ('adopt', vi)
        yield
        # V:= U_j=1...n read C2,1
        V.clear()
        for j in range(len(self.D[r][2])):
            V.add(self.D[r][2][j])
            yield
        #if V - {\perp} = 'commit v'
        V.remove(None)
        V = list(V)
        if len(V) == 1 and V[0][0] == 'commit':
            yield v
        else: #else if 'commit v' \in V
            v = find_i_tuple(V, 0, 'commit')
            if v is not None:
                yield ('adopt', v[1])
            else:
                yield ('adopt', vi)

    # oracleConciliator protocol from the article
    def oracle_conciliator(self, r, v, nonce):
        self.present[r][v] = 1
        if self.present[r][1 - v] == 0:
            return v
        else:
            return H(r, nonce)

    # consensus protocol from the article
    def consensus(self, inp, f, s, nonce):
        for v in self.treshold_conciliator(inp, f, s): yield
        for a, v in self.adopt_commit(1, v): yield
        if a == 'commit':
            yield v
        r = 0
        while True:
            v = self.oracle_conciliator(r,v,nonce)
            for a, v in self.adopt_commit(r, v): yield
            if a == 'commit':
                yield v
                return
