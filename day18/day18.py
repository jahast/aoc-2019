with open("input.txt", "r") as f:
    lines = [l.strip() for l in f.readlines()]

tunnel = {(i,j):el for i, row in enumerate(lines) for j, el in enumerate(row) if el != "#"}

offsets = [
    (-1, 0),
    (1, 0),
    (0, 1),
    (0, -1)
]

def recurse(path, gates = []):
    i,j = path[-1]
    neighbour_idxs = [(i+o[0], j+o[1]) for o in offsets]
    neighbours = [(p,tunnel[p])  for p in neighbour_idxs if p in tunnel and p not in path]
    res = []
    for n in neighbours:
        n_pos, el = n
        if el.isupper():
            res.extend(recurse(path + [n_pos], gates + [el]))
        elif el.islower():
            res.append((el, len(path), gates))
        else:
            res.extend(recurse(path + [n_pos], gates))
    return res

graph = {}
for p, el in tunnel.items():
    if el.islower():
        graph[el] = recurse([p])

at_position = next(p for p,el in tunnel.items() if el == "@")
starting_options = recurse([at_position])
n_keys = sum(k.islower() for k in graph.keys())

pq = []
for v, m, _ in starting_options:
    pq.append((m, set([v]), v))

ans1 = 10**10

while len(pq) != 0:
    mileage, visited, last = pq.pop(0)
    if len(visited) == n_keys:
        ans1 = ans1 if mileage > ans1 else mileage
        continue
    if mileage > ans1:
        continue
    nexts = graph[last]
    for node, m, gates in nexts:
        gates_with_no_key = set([g.lower() for g in gates]).difference(visited)
        if len(gates_with_no_key) > 0:
            continue
        new_visited = visited.union(node)
        new_mileage = mileage + m
        new_state = (new_mileage, new_visited, node)
        is_inferior = False
        for o_m, o_v, o_l in pq:
            if new_visited.issubset(o_v) and o_l == node and o_m <= new_mileage:
                is_inferior = True
                break
        if not is_inferior:
            pq.append(new_state)

    pq.sort(key=lambda x: x[0])
     
print(ans1)

# I opted to just copy paste
# It's pretty slow but whatever
a_i, a_j = at_position

lines_arr = [[el for el in r] for r in lines]

lines_arr[a_i][a_j] = "#"

lines_arr[a_i][a_j + 1] = "#"
lines_arr[a_i][a_j - 1] = "#"
lines_arr[a_i + 1][a_j] = "#"
lines_arr[a_i - 1][a_j] = "#"

lines_arr[a_i + 1][a_j + 1] = "@"
lines_arr[a_i - 1][a_j + 1] = "@"
lines_arr[a_i + 1][a_j - 1] = "@"
lines_arr[a_i - 1][a_j - 1] = "@"

lines = ["".join(r) for r in lines_arr]

tunnel = {(i,j):el for i, row in enumerate(lines) for j, el in enumerate(row) if el != "#"}

graph = {}
for t in tunnel.items():
    p, el = t
    if el.islower():
        graph[el] = recurse([p])

startings_pos = [p for p,el in tunnel.items() if el == "@"]
starting_options = [recurse([p]) for p in startings_pos]

for i, sp in enumerate(startings_pos):
    graph["@" + str(i)] = recurse([sp])

ans2 = 10**6

states = [(0, set(["@0", "@1", "@2", "@3"]), ["@0", "@1", "@2", "@3"])]

while len(states) > 0:
    mileage, visited, lasts = states.pop(0)
    if len(visited) - 4 == n_keys:
        ans2 = ans2 if mileage > ans2 else mileage
        continue
    if mileage > ans2:
        continue

    for i, l in enumerate(lasts):
        nexts = graph[l]
        for node, m, gates in nexts:
            gates_with_no_key = set([g.lower() for g in gates]).difference(visited)
            if len(gates_with_no_key) > 0:
                continue
            new_visited = visited.union(node)
            new_mileage = mileage + m
            new_lasts = lasts.copy()
            new_lasts[i] = node
            new_state = (new_mileage, new_visited, new_lasts)
            is_inferior = False
            for o_m, o_v, o_l in states:
                if new_visited.issubset(o_v) and set(o_l).issubset(set(new_lasts)) and o_m <= new_mileage:
                    is_inferior = True
                    break
            if not is_inferior:
                states.append(new_state)
    
    states.sort(key=lambda x: x[0])

print(ans2)