from intcode import Intcode

with open("input.txt", "r") as f:
    lines = [l.strip() for l in f.readlines()]

ops = [int(c) for c in lines[0].split(",")]
comp = Intcode(ops)

res = []

for i in range(50):
    cur = []
    for j in range(50):
        comp = Intcode(ops)
        cur.append(comp.input_and_run([i,j]))
    res.append(cur)

ans1 = 0

for r in res:
    ans1 += sum(r)

print(ans1)

row = 790

while True:
    row += 1
    j = row // 2
    while True:
        comp = Intcode(ops)
        beam = comp.input_and_run([row,j])
        if beam == 1:
            break
        j += 1
    
    comp = Intcode(ops)
    beam = comp.input_and_run([row - 99 ,j + 99])

    if beam == 0:
        continue

    break

best = ((0,0), 10**10)

for up in range(50,100):
    dist = (row-up)**2 + j**2
    if dist < best[1]:
        best = ((row-up, j), dist)

for right in range(0,50):
    dist = (row - 99)**2 + (j + right)**2
    if dist < best[1]:
        best = ((row - 99, j + right), dist)
    
ans2 = best[0][0] * 10000 + best[0][1]

print(ans2)
