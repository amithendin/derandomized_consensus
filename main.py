import random
from pprint import pprint

from protocol import *

s = 100 # range of values for Approximate Agreement
n = 10 # number of processes
l = 1024 # range of the threshold / number of hashes in the obfuscation
T = 643 # threshold value
m = 10 # length of a single hash
k = 5 # length of preimage nonce
w = 10 # number of adopt-commit objects, (theoretically, needs to be infinite)

A = [[None]*2]*s # shared registers for Approximate Agreement
present = [[None]*2]*s # shared registers for Oracle Conciliator
D = [[[None]*n]*2]*w # shared registers for adopt-commit objects

# generate random binary input values for processes
process_inputs = [random.randint(0, 1) for i in range(n)]

# compute obfuscation
C, P = preprocess(l,T,m,k)

#compose obfuscsated threshold function f
def f(i):
    return queryThreshold(i, l,m,k,C,P)

# initialize processes
processes = [Process(i, A, present, D) for i in range(n)]
generators = {} # necesary for technical hack for interrupted function execution using python generators
return_values = {} # the decision values of the protocol for each terminated process
stopped = set() # set of id's of terminated proceses

# compute a random schedule for the processes of 10,000 steps
schedule = random.choices(processes, k=10_000)

# execute the schedule
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

# print returned values
pprint(return_values)
s = sum(return_values.values())
print(s,  s == 0 or s == n)