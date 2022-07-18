with open("input.txt", "r") as f:
    lines = f.readlines()

matr = [list(l) for l in lines]
places_raw = {(i,j):el for i, r in enumerate(matr) for j, el in enumerate(r) if el not in ["#", "\n"]}

offsets = [
    (1, 0),
    (0, 1),
    (-1, 0),
    (0, -1)
]

max_i, max_j = len(matr) - 1, len(matr[0]) - 2

portals = {}
found = set()

for (i,j), v in places_raw.items():
    if v == "." or (i,j) in found:
        continue

    is_outer = i in [0, max_i] or j in [0, max_j]

    nexts = [[(i + ii, j + jj), (i + ii * 2, j + jj * 2)] for ii,jj in offsets]

    for n_i, next in enumerate(nexts):
        if not all(n in places_raw for n in next):
            continue

        points_in_line = [places_raw[p] for p in next]

        if points_in_line[0].isupper() and points_in_line[1] == ".":
            found = found.union([(i,j), next[1]])
            if n_i <= 1:
                portals[next[0]] = (v + points_in_line[0]), is_outer
            else:
                portals[next[0]] = (points_in_line[0] + v), is_outer
            break

places = {(i,j):(el, False) for i, r in enumerate(matr) for j, el in enumerate(r) if el == "."}
places.update(portals)

graph = {}

def recurse(visited, mileage):
    i,j = visited[-1]
    neighbour_idxs = [(i+ii, j+jj) for ii,jj in offsets]
    neighbours = [(p, places[p]) for p in neighbour_idxs if p in places and p not in visited]
    res = []
    for p, (n, is_outer) in neighbours:
        if n == ".":
            res.extend(recurse(visited + [p], mileage + 1))
        else:
            res.append((n, mileage, is_outer))
    return res

for p, (v, is_outer) in places.items():
    if v == ".":
        continue

    graph[(v,is_outer)] = recurse([p], 0)

ans1 = 10**10

states = [([("AA", False)], 0)]

while len(states) > 0:
    visited, mileage = states.pop(0)

    last_key, last_is_outer = visited[-1]

    if last_key == "ZZ":
        ans1 = ans1 if ans1 < mileage else mileage
        continue

    if mileage > ans1:
        continue

    this_key = (last_key, not last_is_outer)

    nexts = [n for n in graph[this_key] if (n[0], n[1]) not in visited]

    if len(nexts) == 0:
        continue

    for next_dest, plus_mileage, is_outer in nexts:
        if next_dest == "AA":
            continue
        new_state = (visited + [(next_dest, is_outer)], mileage + plus_mileage)
        states.append(new_state)

    states.sort(key=lambda x: x[1])

print(ans1 - 1)

states = [([("AA", False)], 0, 0)]

ans2 = 10**10

while len(states) > 0:
    visited, mileage, level = states.pop(0)

    if level < -1 or level > 100:
        continue

    last_key, last_is_outer = visited[-1]

    if last_key == "ZZ":
        ans2 = ans2 if ans2 < mileage else mileage
        continue

    if mileage > ans2:
        continue

    this_key = (last_key, not last_is_outer)
    nexts = [n for n in graph[this_key]]

    if len(nexts) == 0:
        continue

    for next_dest, plus_mileage, is_outer in nexts:

        last_couple_visited_keys = [v[0] for v in visited[-1:]]

        if next_dest in last_couple_visited_keys:
            continue

        if level != 0 and is_outer and next_dest == "ZZ":
            continue

        if level == 0 and is_outer and next_dest != "ZZ":
            continue

        if next_dest == "AA":
            continue

        new_level = level - 1 if is_outer else level + 1
        new_visited = visited + [(next_dest, is_outer)]
        new_mileage = mileage + plus_mileage
        new_state = (new_visited, new_mileage, new_level)

        is_inferior = False
        for o_v, o_m, o_l in states:
            if o_l == new_level and o_m < new_mileage and o_v[-1] == (next_dest, is_outer) and set(o_v).issubset(set(new_visited)):
                is_inferior = True
                break

        if not is_inferior:
            states.append(new_state)

    states.sort(key=lambda x: x[1])

print(ans2 - 1)