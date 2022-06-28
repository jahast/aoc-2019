from intcode import Intcode
from itertools import combinations

with open("input.txt", "r") as f:
    lines = [l.strip() for l in f.readlines()]

ops = [int(c) for c in lines[0].split(",")]
comp = Intcode(ops)

arr = [[]]

while True:
    res = comp.run()
    if res == 10:
        arr.append([])
    elif res == None:
        break
    else:
        arr[-1].append(chr(res))

arr = [r for r in arr if r != []]

ans1 = 0
for y, r in enumerate(arr):
    for x, el in enumerate(r):
        if y in (0, len(arr) - 1):
            continue
        if x in (0, len(r) - 1):
            continue
        if el == "#":
            is_intersection = all(
                [
                    arr[y + 1][x] in ["#", "<", ">", "^", "v"],
                    arr[y - 1][x] in ["#", "<", ">", "^", "v"],
                    arr[y][x + 1] in ["#", "<", ">", "^", "v"],
                    arr[y][x - 1] in ["#", "<", ">", "^", "v"]
                ]
            )
            if is_intersection:
                ans1 += (y)*(x)

print(ans1)

pos = next((i,j) for i,r  in enumerate(arr) for j, el in enumerate(r) if el in ["<", ">", "^", "v"])

dirs = [
    "<",
    "^",
    ">",
    "v"
]

offsets = [
    (0,-1),
    (-1,0),
    (0,1),
    (1, 0)
]

commands = []
i,j = pos
cur = arr[i][j]

def is_in_range(i,j,arr):
    imin, imax = 0, len(arr)
    jmin, jmax = 0, len(arr[0])
    return i in range(imin, imax) and j in range(jmin, jmax)

# first figure out the whole path
while True:
    cur_dir_idx = dirs.index(cur)
    cur_offset = offsets[cur_dir_idx]

    left_idx = (cur_dir_idx - 1) % 4
    left_offset = offsets[left_idx]
    li, lj = i+left_offset[0], j+left_offset[1]

    right_idx = (cur_dir_idx + 1) % 4
    right_offset = offsets[right_idx]
    ri, rj = i+right_offset[0], j+right_offset[1]

    if is_in_range(li,lj, arr) and arr[li][lj] == "#":
        commands.append("L")
        cur = dirs[left_idx]
        ii, jj = left_offset
    elif is_in_range(ri,rj, arr) and arr[ri][rj] == "#":
        commands.append("R")
        cur = dirs[right_idx]
        ii, jj = right_offset
    else:
        break
    
    n_i,n_j = i+ii, j+jj
    rep = 0
    while is_in_range(n_i, n_j, arr) and arr[n_i][n_j] == "#":
        rep += 1
        i,j = n_i, n_j
        n_i, n_j = i+ii, j+jj
    
    commands.append(rep)

# then generate all possible routines
candidates = []
for start in range(0, len(commands) - 3, 2):
    temp = commands[start:]
    i = 2
    while True:
        candidate = temp[0:i]
        subsections_left = len(temp) - i + 1
        subsections = [temp[j+i:j+i+i] for j in range(0, subsections_left, 2)]
        matches_next = any(s == candidate for s in subsections)
        if not matches_next:
            break
        else:
            if temp[0:i] not in candidates:
                candidates.append(temp[0:i])
            i += 2

# see which ones empty the whole path and choose one with the shortest main function (latter probably not necessary)
best = (10000, [], [])
for comb in combinations(candidates, 3):
    comb = sorted(comb, key=lambda x: len(x), reverse=True)
    temp = commands.copy()
    main = []
    while True:
        replaced = False
        for sidx, sub in enumerate(comb):
            to_try = temp[0:len(sub)]
            if to_try == sub:
                temp = temp[len(sub):]
                main.append(sidx)
                replaced = True
        if len(temp) == 0 or not replaced:
            break
    if len(temp) == 0:
        if len(main) < best[0]:
            best = (len(main), main, comb)

# and finally map to commands and run
def to_ascii(ar):
    return [ord(a) for a in ",".join(str(el) for el in ar)] + [10]

main = [chr(65 + idx) for idx in best[1]]

ascii_commands = to_ascii(main) + to_ascii(best[2][0]) + to_ascii(best[2][1]) + to_ascii(best[2][2]) + [ord("n"), 10]

ops[0] = 2
comp = Intcode(ops)
comp.add_input(ascii_commands)
while True:
    temp = comp.run()
    if temp == None:
        break
    ans2 = temp

print(ans2)
