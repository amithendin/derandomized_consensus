import random
import types

from util import random_bit_string, xor_bits, flip_bit, sha256_of_bits, H


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

class Process:
    def __init__(self, id, A, present):
        self.id = id
        self.A = A
        self.present = present

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

    def treshold_conciliator(self, inp, f, s):
        for i in self.approximate_agreement(inp, s): yield
        yield f(i)

    def adopt_commit(self, r, v):
        pass

    def oracle_conciliator(self, r, v, nonce):
        self.present[r][v] = 1
        if self.present[r][1 - v] == 0:
            return v
        else:
            return H(r, nonce)

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
