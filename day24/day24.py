from collections import defaultdict

with open("input.txt", "r") as f:
    lines = [l.strip() for l in f.readlines()]

tiles = {(i,j):el for i, r in enumerate(lines) for j,el in enumerate(r)}
i_len, j_len = len(lines), len(lines[0])

offsets = [
    (0,1),
    (1,0),
    (0,-1),
    (-1,0)
]

def plus(a, b):
    return (a[0] + b[0], a[1] + b[1])

def compress(tls):
    res = []
    for i in range(i_len):
        for j in range(j_len):
            res.append(tls[(i,j)])
    return "".join(res)

seen = set([compress(tiles)])
while True:
    new_tiles = {(i,j):"" for i in range(i_len) for j in range(j_len)}
    for i in range(i_len):
        for j in range(j_len):
            this_p = (i,j)
            neighbour_idxs = [plus(this_p, o) for o in offsets]
            n_bugs = sum([tiles[p] == "#" for p in neighbour_idxs if p in tiles])
            has_bug = tiles[this_p] == "#"

            if has_bug:
                new_tiles[this_p] = "#" if n_bugs == 1 else "."
            else:
                new_tiles[this_p] = "#" if n_bugs in [1,2] else "."
    
    tiles = new_tiles
    compressed = compress(tiles)
    if compressed in seen:
        break
    seen = seen.union([compressed])

ans1 = 0
for i in range(i_len):
    for j in range(j_len):
        if tiles[(i,j)] == "#":
            ans1 += 2**(i*5 + j)
print(ans1)

tiles = {(i,j):el for i, r in enumerate(lines) for j,el in enumerate(r)}

outer_to_inner = {
    (1,2): [(0,i) for i in range(5)],
    (2,1): [(i,0) for i in range(5)],
    (2,3): [(i,4) for i in range(5)],
    (3,2): [(4,i) for i in range(5)]
}

def e():
    return {(i,j):"." for i, r in enumerate(lines) for j,_ in enumerate(r)}

tiles_on_levels = defaultdict(e)
tiles_on_levels[0] = tiles

max_level, min_level = 0,0
for step in range(200):
    while True:
        next_level = tiles_on_levels[max_level]
        if all(v == "." for v in next_level.values()):
            break
        max_level += 1
    
    while True:
        next_level = tiles_on_levels[min_level]
        if all(v == "." for v in next_level.values()):
            break
        min_level -= 1

    new_tiles_on_levels = defaultdict(e)
    for level in range(min_level, max_level + 1):
        this_level = tiles_on_levels[level]
        outer = tiles_on_levels[level + 1]
        inner = tiles_on_levels[level - 1]
        for p,v in this_level.items():
            if p == (2,2):
                continue
            neighbour_idxs = [plus(p, o) for o in offsets]
            if (2,2) in neighbour_idxs:
                neighbour_idxs.remove((2,2))
            inner_idxs = outer_to_inner[p] if p in outer_to_inner else [] 
            n_inner = sum(inner[pp] == "#" for pp in inner_idxs)
            n_outer = 0
            for i,j in neighbour_idxs:
                if i == -1:
                    n_outer = n_outer + 1 if outer[(1,2)] == "#" else n_outer
                if i == 5:
                    n_outer = n_outer + 1 if outer[(3,2)] == "#" else n_outer
                if j == -1:
                    n_outer = n_outer + 1 if outer[(2,1)] == "#" else n_outer
                if j == 5:
                    n_outer = n_outer + 1 if outer[(2,3)] == "#" else n_outer
            n_this_level = sum([this_level[pp] == "#" for pp in neighbour_idxs if pp in this_level])
            total_bugs = n_inner + n_outer + n_this_level

            has_bug = v == "#"
            if has_bug:
                new_tiles_on_levels[level][p] = "#" if total_bugs == 1 else "."
            else:
                new_tiles_on_levels[level][p] = "#" if total_bugs in [1,2] else "."
    tiles_on_levels = new_tiles_on_levels

ans2 = 0
for level in range(min_level, max_level + 1):
    ans2 += sum(v == "#" for v in tiles_on_levels[level].values())

print(ans2)