from intcode import intcode 

with open("input.txt", "r") as f:
    lines = [l.strip() for l in f.readlines()]

ops = [int(c) for c in lines[0].split(",")]

def run(ops, painted = {}):
    pos = (0,0)
    dirs = [(0,1), (1,0), (0,-1), (-1, 0)]
    dir = 0
    comp = intcode(ops)
    while True:
        cur_color = painted[pos] if pos in painted else 0

        new_paint = comp.input_and_run([cur_color])
        if new_paint == None:
            break

        dir_ins = comp.run()
        if dir_ins == None:
            break
        
        painted[pos] = new_paint
        dir = (dir - 1) % 4 if dir_ins == 0 else (dir + 1) % 4
        new_dir = dirs[dir]
        pos = (pos[0] + new_dir[0], pos[1] + new_dir[1])
    return painted

ans1 = len(run(ops))
print(ans1)

ans2 = run(ops, {(0,0): 1})
xs, ys = [p[0] for p in ans2.keys()], [p[1] for p in ans2.keys()]
min_x, max_x = min(xs), max(xs)
min_y, max_y = min(ys), max(ys)

canvas = [["." for _ in range(0, max_y - min_y + 1)] for _ in range(0, max_x - min_x + 1)]
for k,v in ans2.items():
    normal_x, normal_y = k[0] - min_x, k[1] - min_y
    canvas[normal_x][normal_y] = "#" if v == 1 else "."

image = "\n".join(["".join(r) for r in canvas])

print(image)
