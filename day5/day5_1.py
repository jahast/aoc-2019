from operator import add, mul
from functools import reduce

with open("input.txt", "r") as f:
    lines = [l.strip() for l in f.readlines()]

ops = [int(i) for i in lines[0].split(",")]

pointer = 0

while True:
    op = ops[pointer]
    opcode_and_modes = [c for c in str(op)][::-1]
    opcode_and_modes += "0" * (5 - len(opcode_and_modes))
    opcode, modes = opcode_and_modes[0:2], opcode_and_modes[2:]

    if opcode == ["3", "0"]:
        inp = input("gif")
        ops[ops[pointer + 1]] = int(inp)
        pointer += 2
    elif opcode == ["4", "0"]:
        to_print = ops[ops[pointer + 1]] if modes[0] == "0" else ops[pointer + 1]
        print(to_print)
        pointer += 2
    elif opcode == ["9", "9"]:
        break
    else:
        vals = []
        for i in range(2):
            next_op = ops[pointer + i + 1]
            vals.append(next_op if modes[i] == "1" else ops[next_op])
        
        new_val = reduce(add if opcode == ["1", "0"] else mul, vals, 0 if opcode == ["1", "0"] else 1)

        ops[ops[pointer + 3]] = new_val

        pointer += 4
