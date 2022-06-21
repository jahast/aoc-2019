import re
from itertools import combinations
import math

with open("input.txt", "r") as f:
    lines = [l.strip() for l in f.readlines()]

cleaned = [re.sub("<|>|x|y|z|=", "", line) for line in lines]

orig_positions = []
for l in cleaned:
    orig_positions.append([int(c) for c in l.split(",")])
positions = orig_positions.copy()
velos = [[0, 0, 0] for _ in range(0, len(positions))]

combs_all = combinations(range(len(positions)), 2)
combs = [c for c in combs_all if c[0] != c[1]]


def plus(p, v):
    return [p[i] + v[i] for i in range(len(p))]


i = 0
while i < 1000:
    for c in combs:
        velo1, velo2 = velos[c[0]], velos[c[1]]
        pos1, pos2 = positions[c[0]], positions[c[1]]

        for j in range(3):
            if pos1[j] < pos2[j]:
                velo1[j], velo2[j] = velo1[j] + 1, velo2[j] - 1
            elif pos1[j] > pos2[j]:
                velo1[j], velo2[j] = velo1[j] - 1, velo2[j] + 1

    for k in range(len(positions)):
        positions[k] = plus(positions[k], velos[k])
    i += 1


def energy(p, v):
    return sum(abs(pp) for pp in p) * sum(abs(vv) for vv in v)


ans1 = sum(energy(positions[k], velos[k]) for k in range(len(positions)))
print(ans1)


def to_str(arr):
    return "".join(str(c) for c in arr)


def run(j):
    positions = orig_positions.copy()
    velos = [[0, 0, 0] for _ in range(0, 4)]
    pos, vel = [p[j] for p in positions], [v[j] for v in velos]
    seen = [to_str(pos + vel)]
    i = 0
    while True:
        for c in combs:
            c1, c2 = c
            velo1, velo2 = vel[c1], vel[c2]
            pos1, pos2 = pos[c1], pos[c2]

            if pos1 < pos2:
                vel[c1], vel[c2] = velo1 + 1, velo2 - 1
            elif pos1 > pos2:
                vel[c1], vel[c2] = velo1 - 1, velo2 + 1

        pos = plus(pos, vel)

        to_check = to_str(pos + vel)

        i += 1
        if to_check in seen:
            print(i)
            return i

        seen.append(to_check)


x = run(0)
y = run(1)
z = run(2)


def lcm(a, b):
    return abs(a * b) // math.gcd(a, b)


ans2 = lcm(x, lcm(y, z))
print(ans2)
