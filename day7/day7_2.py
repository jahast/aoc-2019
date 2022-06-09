from intcode2 import intcode2
from itertools import permutations

with open("input.txt", "r") as f:
    lines = [l.strip() for l in f.readlines()]

ops = [int(i) for i in lines[0].split(",")]

# i don't like copy pasting and hacking the intcode file
# but i keep the code nice here at least
all_phase_seqs = permutations([5,6,7,8,9], 5)
ans2 = 0
best_phase = None
for phase_seq in all_phase_seqs:
    inp = 0
    states = {}
    for i, phase in enumerate(phase_seq):
        inp, state = intcode2(ops, phase, inp)
        states[i] = state
    prev = inp
    i = 0
    while inp != None:
        if i % 5 == 0:
            prev = inp
        amp_state = states[i % 5]
        inp, state = intcode2(ops, phase, inp, amp_state)
        states[i % 5] = state
        i += 1
    if prev > ans2:
        ans2 = prev
        best_phase = phase_seq

print(ans2)
print(best_phase)