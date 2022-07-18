from intcode import Intcode

with open("input.txt", "r") as f:
    line = f.readline()

ops = [int(c) for c in line.split(",")]
comp = Intcode(ops)

def to_ascii(ar):
    return [ord(a) for a in ar] + [10]

# jump if C is empty but there's a tile to land on in D
# othwerwise jump when there's an empty space in A
commands = [
    "NOT C J",
    "AND D J",
    "NOT A T",
    "OR T J",
    "WALK"
]

ascii_commands = []
for c in commands:
    ascii_commands.extend(to_ascii(c))

res = []
while True:
    r = comp.run()
    if r == "inp":
        break
    res.append(r)

print("".join([chr(c) for c in res]))
comp.add_input(ascii_commands)

new_res = []
while True:
    r = comp.run()
    if r == None:
        break
    new_res.append(r)

text_res = [chr(c) for c in new_res[:-1]]

ans1 = new_res[-1]
print(ans1)

comp = Intcode(ops)

# jump if there is empty space in B OR C and can execute a double jump
# othwerwise jump only when there's an empty space in A
commands = [
    "NOT B J",
    "NOT C T",
    "OR T J",
    "AND D J",
    "AND H J",
    "NOT A T",
    "OR T J",
    "RUN"
]

ascii_commands = []
for c in commands:
    ascii_commands.extend(to_ascii(c))

res = []
while True:
    r = comp.run()
    if r == "inp":
        break
    res.append(r)

print("".join([chr(c) for c in res]))
comp.add_input(ascii_commands)

new_res = []
while True:
    r = comp.run()
    if r == None:
        break
    new_res.append(r)

text_res = [chr(c) for c in new_res[:-1]]

print("".join(text_res))

ans2 = new_res[-1]
print(ans2)