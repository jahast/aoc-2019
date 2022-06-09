import sys

with open("input.txt", "r") as f:
    lines = [l.strip() for l in f.readlines()]

def to_path(line):
    dirs = line.split(",")
    return [(d[0], int(d[1:])) for d in dirs]

path1 = to_path(lines[0])
path2 = to_path(lines[1])

def to_coords(path):
    start = (0,0)
    coords = []
    for d, l in path:
        for _ in range(l):
            if d == "R":
                start = (start[0] + 1, start[1])
                coords.append(start)
            if d == "L":
                start = (start[0] - 1, start[1])
                coords.append(start)
            if d == "U":
                start = (start[0], start[1] + 1)
                coords.append(start)
            if d == "D":
                start = (start[0], start[1] - 1)
                coords.append(start)
    return coords

coords1 = to_coords(path1)
coords2 = to_coords(path2)

intersects = set(coords1).intersection(set(coords2))

ans1 = min(abs(c[0]) + abs(c[1]) for c in intersects)
print(ans1)

ans2 = sys.maxsize

for intersect in intersects:
    ans2 = min(ans2, coords1.index(intersect) + coords2.index(intersect) + 2)

print(ans2)
