with open("input.txt", "r") as f:
    lines = [l.strip() for l in f.readlines()]

masses = [int(m) for m in lines]
ans1 = sum([m // 3 - 2 for m in masses])
print(ans1)

ans2 = 0
for m in masses:
    tmp = m
    while tmp > 0:
        tmp = max(tmp // 3 - 2, 0)
        ans2 += tmp

print(ans2)
