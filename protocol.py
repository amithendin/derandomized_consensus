import random
import types

from util import random_bit_string, xor_bits, flip_bit, sha256_of_bits


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
    def __init__(self, id, shared):
        self.id = id
        self.shared = shared

    def approximate_agreement(self, inp, s):
        i = inp
        for r in range(0, s):
            self.shared[r][i % 2] = i
            yield
            i_tag = self.shared[r][(i+1) % 2]
            yield
            if i_tag == None:
                i = 2*i
            else:
                i = i + i_tag
        yield i

    def treshold_conciliator(self, inp, f, s):
        for i in self.approximate_agreement(inp, s): yield
        print(f'[{self.id}: {i}]')
        yield f(i)
