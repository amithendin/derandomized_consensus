import random
from protocol import *

seed = 42
random.seed(seed)
# protocol parameters
s = 10                       # range of values for Approximate Agreement
n = 10                       # number of processes
l = 2**s+1                   # range of the threshold / number of hashes in the obfuscation
T = random.randint(2,l-1) # threshold value must be < l
m = 10                       # length of a single hash
k = 5                        # length of preimage nonce
w = 500                      # number of adopt-commit objects, (theoretically, needs to be infinite)
schedule_length = 10_000     # maximum length of the schedule
# process inputs
process_inputs = [random.randint(0, 1) for i in range(n)]

# shared memory objects
A = [[None for _ in range(2)] for __ in range(s)]                      # shared registers for Approximate Agreement
present = [[0 for _ in range(2)] for __ in range(w)]                   # shared registers for Oracle Conciliator
D = [[[None for _ in range(n)] for __ in range(2)] for ___ in range(w)]# shared registers for adopt-commit objects


# compute obfuscation
C, P = preprocess(l,T,m,k)

#compose obfuscsated threshold function f
def f(i):
    return queryThreshold(i, l,m,k,C,P)

# generate nonces for the consensus random oracle
nonce = [random.randint(0, n) for _ in range(n)]

# initialize processes
processes = [Process(i, A, present, D) for i in range(n)]
generators = {} # necessary for technical hack for interrupted function execution using python generators
return_values = {} # the decision values of the protocol for each terminated process
stopped = set() # set of id's of terminated proceses

# compute a random schedule for the processes of <schedule_length> steps
schedule = random.choices(processes, k=schedule_length)

# execute the schedule
for i in range(len(schedule)):
    if len(stopped) == n: #stop early if everyone decided
        print(f'stopped after {i} schedule steps')
        break
    process = schedule[i]
    if process.id not in generators: # create a generator for processes that are taking the first step in the schedule
        generators[process.id] = process.consensus( process_inputs[process.id], f, s, nonce[process.id] )
    elif process.id not in stopped:
        # continue to the next step in the protocol for processes that have already begun, record terminted processes so that we skip over them in the schedule
        try: return_values[process.id] = next(generators[process.id])
        except StopIteration: stopped.add(process.id)

# print returned values
print(f'rnd seed:  {seed}')
print(f'inputs:    {process_inputs}')
print(f'decisions: {[return_values[i] for i in range(n)]}')
s = sum([ (v if v is not None else 0) for v in return_values.values() ])
print(f'agreement: {s == 0 or s == n}')