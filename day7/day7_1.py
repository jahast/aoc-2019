from intcode import intcode
from itertools import permutations

with open("test.txt", "r") as f:
    lines = [l.strip() for l in f.readlines()]

ops = [int(i) for i in lines[0].split(",")]

all_phase_seqs = permutations([0,1,2,3,4], 5)

ans1 = 0
best_phase = None
for phase_seq in all_phase_seqs:
    inp = 0
    for phase in phase_seq:
        inp = intcode(ops, phase, inp)
    if inp > ans1:
        ans1 = inp
        best_phase = phase_seq

print(ans1)
print(best_phase)
