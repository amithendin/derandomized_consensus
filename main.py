import random
from pprint import pprint

from protocol import *

s = 100; n = 10  #protocol parameters
l = 1024; T=643; m=10; k=5 #obfuscation parameters
C, P = preprocess(l,T,m,k)

def f(i):
    return queryThreshold(i, l,m,k,C,P)

process_inputs = [random.randint(2, s) for i in range(n)]

A = [[None]*2]*s
processes = [Process(i, A) for i in range(n)]
generators = {}
return_values = {}
stopped = set()
schedule = random.choices(processes, k=10000)

for i in range(len(schedule)):
    if len(stopped) == n:
        print('stopped after ',i,' iterations')
        break
    process = schedule[i]
    if process.id not in generators:
        generators[process.id] = process.treshold_conciliator( process_inputs[process.id], f, s )
    elif process.id not in stopped:
        try: return_values[process.id] = next(generators[process.id])
        except StopIteration: stopped.add(process.id)

pprint(return_values)
s = sum(return_values.values())
print(s,  s == 0 or s == n)