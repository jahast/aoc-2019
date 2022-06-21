from intcode import Intcode
import os


def print_tiles(tls):
    os.system("clear")
    keys = list(tls.keys())
    xs, ys = list(zip(*keys))
    xmax, xmin = max(xs), min(xs)
    ymax, ymin = max(ys), min(ys)

    matr = [["."] * (xmax - xmin + 1) for _ in range(ymin, ymax + 1)]

    for (x, y), v in tls.items():
        if v == 0:
            to_write = "."
        elif v == 1:
            to_write = "|"
        elif v == 2:
            to_write = "#"
        elif v == 3:
            to_write = "-"
        elif v == 4:
            to_write = "0"
        else:
            raise Exception("no")
        matr[y + ymin][x + xmin] = to_write

    to_print = "\n".join("".join(r) for r in matr)
    print(to_print)


with open("input.txt", "r") as f:
    lines = [l.strip() for l in f.readlines()]

ops = [int(c) for c in lines[0].split(",")]

comp = Intcode(ops)

tiles = {}

while True:
    x = comp.run()

    if x == None:
        break

    y = comp.run()
    tid = comp.run()
    tiles[(x, y)] = tid

ans1 = len([v for v in tiles.values() if v == 2])
print(ans1)

ops = [int(c) for c in lines[0].split(",")]
ops[0] = 2
comp = Intcode(ops)

tiles = {}
score = -1

while True:
    x = comp.run()

    if x == None:
        break
    if x == "inp":
        print_tiles(tiles)
        # I will call this "PONG AI 2000"
        ball = next(x for ((x, _), v) in tiles.items() if v == 4)
        paddle = next(x for ((x, _), v) in tiles.items() if v == 3)
        inp = 0
        if paddle < ball:
            inp = 1
        elif paddle > ball:
            inp = -1
        comp.add_input(inp)
        continue

    y = comp.run()

    tid = comp.run()

    if (x, y) == (-1, 0):
        score = tid
        continue
    tiles[(x, y)] = tid

print_tiles(tiles)

ans2 = score
print(ans2)
