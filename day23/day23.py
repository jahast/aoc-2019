from intcode import Intcode

with open("input.txt", "r") as f:
    line = f.readline()

ops = [int(c) for c in line.split(",")]

comps = {i:Intcode(ops) for i in range(50)}

for i, c in comps.items():
    r = c.run()
    assert r == "inp"
    c.add_input(i)

found = False
while not found:
    for i in range(50):
        comp = comps[i]
        while True:
            res = comp.run()
            if res == "inp":
                comp.add_input(-1)
                break
            else:
                new_inputs = [comp.run(), comp.run()]
                if res == 255:
                    found = True
                    break
                comps[res].add_input(new_inputs)

ans1 = new_inputs[1]
print(ans1)

# I'll just copy paste again
comps = {i:Intcode(ops) for i in range(50)}

for i, c in comps.items():
    r = c.run()
    assert r == "inp"
    c.add_input(i)


inputs = {i:[] for i in range(50)}
last_delivered_y = None
while True:
    is_idle = True
    for i in range(50):
        comp = comps[i]
        if inputs[i] != []:
            is_idle = False
        comp.add_input(inputs[i])
        inputs[i] = []
        while True:
            res = comp.run()
            if res == "inp":
                comp.add_input(-1)
                break
            else:
                new_inputs = [comp.run(), comp.run()]
                if res == 255:
                    inputs[255] = new_inputs
                else:
                    inputs[res] = inputs[res] + new_inputs
    if is_idle and 255 in inputs:
        comps[0].add_input(inputs[255])
        if inputs[255][1] == last_delivered_y:
            break
        last_delivered_y = inputs[255][1]

ans2 = last_delivered_y
print(ans2)