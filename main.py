from protocol import *

s = 100; process_inputs = [0,1,1,1,0,1,0,0]; n = len(process_inputs)  #protocol parameters
l = 200; T = 143; m=12; k=7 #obfuscation parameters
C, P = preprocess(l,T,m,k)

def f(i):
    return queryThreshold(i, l,m,k,C,P)

A = [None]*s
processes = [Process(i, A) for i in range(n)]

