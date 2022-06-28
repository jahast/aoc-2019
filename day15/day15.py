from intcode import Intcode
import os

with open("input.txt", "r") as f:
    lines = [l.strip() for l in f.readlines()]

def print_tiles(tls):
    os.system("clear")
    print("--------------------")
    keys = list(tls.keys())
    xs, ys = list(zip(*keys))
    xmax, xmin = max(xs), min(xs)
    ymax, ymin = max(ys), min(ys)

    matr = [["@"] * (xmax - xmin + 1) for _ in range(ymin, ymax + 1)]

    for (x, y), v in tls.items():
        matr[y - ymin][x - xmin] = v

    to_print = "\n".join("".join(r) for r in matr)
    print(to_print)

ops = [int(c) for c in lines[0].split(",")]

comp = Intcode(ops)

coords = {(0,0): "S"}
path = [(0,0)]

cur_pos = (0,0)

dirs = {
    1: (0,1),
    4: (1,0),
    2: (0,-1),
    3: (-1,0)
}

offset_to_dir = {v:k for k,v in dirs.items()}

offsets = [d for d in dirs.values()]

def plus(cur, offset):
    return (cur[0] + offset[0], cur[1] + offset[1])

def minus(cur, target):
    return (target[0] - cur[0], target[1] - cur[1])

# the idea is to just move somewhere until we are either stuck
# with walls around or there is nowhere to explore.
# Once we get stuck, we backtrack until we find a previous 
# location where we can explore again
is_backtracking = False
surroundings = [plus(cur_pos, offset) for offset in offsets]
unseen = [s for s in surroundings if s not in coords]
while True:
    if is_backtracking:
        has_unseen_space = len(unseen) > 0
        if has_unseen_space:
            is_backtracking = False
            continue

        next = path.pop()

        # kinda lucky this works actually
        if next == (0,0) and len(path) == 0:
            break

        next_offset = minus(cur_pos, next)
        dir = offset_to_dir[next_offset]
    else:
        next = unseen[0]
        next_offset = minus(cur_pos, next)
        dir = offset_to_dir[next_offset]

    res = comp.input_and_run(dir)
    next_pos = plus(cur_pos, dirs[dir])
    if res == 0:
        coords[next_pos] = "#"
    elif res == 1:
        coords[next_pos] = "."
        if not is_backtracking:
            path.append(cur_pos)
        cur_pos = next_pos
    elif res == 2:
        coords[next_pos] = "O"
        if not is_backtracking:
            path.append(cur_pos)
        cur_pos = next_pos

    surroundings = [plus(cur_pos, offset) for offset in offsets]
    unseen = [s for s in surroundings if s not in coords]
    walls_around = sum([s in coords and coords[s] == "#" for s in surroundings])
    is_backtracking = walls_around == 3 or len(unseen) == 0

print_tiles(coords)


def recurse(coords, path):

    cur = path[-1]

    if coords[cur] == "O":
        return len(path)

    surroundings = [plus(cur, offset) for offset in offsets]
    candidates = [c for c in surroundings if coords[c] != "#" and c not in path]
    best = 10**10
    for c in candidates:
        res = recurse(coords, path + [c])
        best = best if best < res else res
    
    return best

ans1 = recurse(coords, [(0,0)])
print(ans1 - 1)


def longest_path(coords, path):
    cur = path[-1]

    surroundings = [plus(cur, offset) for offset in offsets]
    candidates = [c for c in surroundings if coords[c] != "#" and c not in path]
    if len(candidates) == 0:
        return len(path)
    longest = -1
    for c in candidates:
        res = longest_path(coords, path + [c])
        longest = longest if longest > res else res
        
    
    return longest

o_coord = [k for k,v in coords.items() if v == "O"][0]

ans2 = longest_path(coords, [o_coord])
print(ans2 - 1)