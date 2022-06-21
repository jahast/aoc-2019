from itertools import groupby

with open("input.txt", "r") as f:
    lines = [l.strip() for l in f.readlines()]

map = [list(r) for r in lines]
x_max, y_max = len(map), len(map[0])
asteroid_idxs = [(i,j) for i in range(x_max) for j in range(y_max) if map[i][j] == "#"]

def blocked(pos, other, x_max, y_max):
    offset = (other[0] - pos[0], other[1] - pos[1])

    offset_abs = (abs(offset[0]), abs(offset[1]))
    gcf = next((f for f in range(min(offset_abs), 1, -1) if offset[0] % f == 0 and offset[1] % f == 0), None)
    # handle offsets like (3,-3) and (2,0)
    if offset_abs[0] == offset_abs[1] or any(c == 0 for c in offset):
        divisor = max(offset_abs)
        offset = (offset[0] // divisor, offset[1] // divisor)
    # handle offsets like (4,-2), (12,8)
    elif gcf != None:
        offset = (offset[0] // gcf, offset[1] // gcf)

    ret = []
    i = 1
    while True:
        new_pos = (other[0] + offset[0] * i, other[1] + offset[1] * i)
        if new_pos[0] not in range(x_max) or new_pos[1] not in range(y_max):
            return ret
        else:
            ret.append(new_pos)
            i += 1

ans1 = ((-1,-1), -1)
asteroid_idxs_set = set(asteroid_idxs)
for pos in asteroid_idxs:
    all_blocked = []
    for other in asteroid_idxs:
        if pos == other:
            continue
        all_blocked += blocked(pos, other, x_max, y_max)
    all_seen = asteroid_idxs_set.difference(set(all_blocked + [pos]))

    if (n := len(all_seen)) > ans1[1]:
        ans1 = (pos, n)

print(ans1)

laser_pos, _ = ans1
lpx, lpy = laser_pos

quarters = zip(
    [list(range(0, lpx)), list(range(lpx, x_max)), list(range(lpx + 1, x_max)), list(range(0, lpx + 1))],
    [list(range(lpy, y_max)), list(range(lpy + 1, y_max)), list(range(0, lpy + 1)), list(range(0, lpy))]
)

# this is hairy af
# the idea is to sort all vectors from the station asteroid by the vectors tangent so to say.
# we don't need to calculate the actual tangent function since it's strictly increasing.
# to get rid of duplicate vectors (eg (2,2), (4,2)) we store each vector by their "tangent"
# and replace it if we find a new one with smaller manhattan dist
dirs = []
for i, (xs, ys) in enumerate(quarters):
    tmp = {}
    for x in xs:
        for y in ys:
            offset_x, offset_y = x - lpx, y - lpy
            if i == 0:
                comp = offset_y * 1000 // abs(offset_x) if offset_x != 0 else 1
            elif i == 1:
                comp = offset_x * 1000 // offset_y if offset_y != 0 else 1
            elif i == 2:
                comp = abs(offset_y) * 1000 // offset_x if offset_x != 0 else 1
            elif i == 3:
                comp = offset_x * 1000 // offset_y if offset_y != 0 else 1
            
            def manhattan(tpl):
                return sum(abs(c) for c in tpl)

            ofs = (offset_x, offset_y)
            if comp not in tmp:
                tmp[comp] = ofs
            elif manhattan(tmp[comp]) > manhattan(ofs):
                tmp[comp] = ofs
    
    dirs_sorted = sorted(tmp.items(), key=lambda x: x[0])
    dirs.extend([d[1] for d in dirs_sorted])

def plus(coord, offset):
    return (coord[0] + offset[0], coord[1] + offset[1])

i = 0
d_i = 0
while i < 200:
    dir = dirs[d_i % len(dirs)]

    next_to_check = plus(laser_pos, dir)
    while next_to_check[0] in range(0, x_max) and next_to_check[1] in range(0, y_max):
        if map[next_to_check[0]][next_to_check[1]] == "#":
            map[next_to_check[0]][next_to_check[1]] = "0"
            i += 1
            print(f"{i}: {str(next_to_check)}")
            break
        next_to_check = plus(next_to_check, dir)

    d_i += 1

ans2 = next_to_check[1] * 100 + next_to_check[0]
print(ans2)

