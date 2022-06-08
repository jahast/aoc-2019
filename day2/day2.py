with open("input.txt", "r") as f:
    lines = [l.strip() for l in f.readlines()]

ops = [int(i) for i in lines[0].split(",")]

ops[1] = 12
ops[2] = 2

for i in range(0, len(ops) + 1, 4):
    op = ops[i]
    if op == 1:
        ops[ops[i+3]] = ops[ops[i+1]] + ops[ops[i+2]]
    if op == 2:
        ops[ops[i+3]] = ops[ops[i+1]] * ops[ops[i+2]]
    if op == 99:
        break

ans1 = ops[0]
print(ans1)

# I just tried these out
noun = 50; verb = 64
ans2 = 100 * noun + verb
print(ans2)