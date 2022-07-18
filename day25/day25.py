from intcode import Intcode

with open("input.txt", "r") as f:
    line = f.readline()

ops = [int(c) for c in line.split(",")]

comp = Intcode(ops)

def to_ascii(ar):
    return [ord(a) for a in ar] + [10]

def to_str(ar):
    return "".join([chr(a) for a in ar])

# i just played it
steps = ['west', 'take mug', 'west', 'east', 'north', 'take easter egg', 'south', 'west', 'east', 'east', 'south', 'east', 'north', 'take candy cane', 'south', 'west', 'south', 'north', 'north', 'east', 'take coin', 'north', 'north', 'take hypercube', 'south', 'east', 'take manifold', 'west', 'south', 'south', 'west', 'take astrolabe', 'south', 'north', 'north', 'east', 'north', 'east', 'inv', 'south', 'west', 'south', 'east', 'east', 'take pointer', 'west', 'west', 'south', 'north', 'north', 'east', 'west', 'south', 'north', 'east', 'north', 'drop pointer', 'drop manifold', 'drop easter egg', 'drop candy cane', 'east']

while True:
    res = []
    r = comp.run()
    while r != "inp" and r != None:
        res.append(r)
        r = comp.run()
    
    print("".join(to_str(res)))

    if len(steps) > 0:
        inp = steps.pop(0)
    else:
        inp = input("Enter: \n")

    comp.add_input(to_ascii(inp))

    # print(record)

# - pointer
# - manifold
# - easter egg
# - candy cane


# - mug
# - hypercube
# - astrolabe
# - coin