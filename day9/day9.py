from operator import add, mul
from functools import reduce
from collections import defaultdict

with open("input.txt", "r") as f:
    lines = [l.strip() for l in f.readlines()]

def intcode(ops_ls,):

    def get_vals(pointer, mode, rel_base):
        if mode == "0":
            return ops[ops[pointer]], ops[pointer]
        elif mode == "1":
            return ops[pointer], None
        elif mode == "2":
            return ops[rel_base + ops[pointer]], rel_base + ops[pointer]
        else:
            raise Exception("invalid mode")

    pointer = 0
    rel_base = 0
    ops = defaultdict(int, {k:v for k,v in enumerate(ops_ls)})
    while True:
        op = ops[pointer]
        opcode_and_modes = [c for c in str(op)][::-1]
        opcode_and_modes += "0" * (5 - len(opcode_and_modes))
        opcode, modes = opcode_and_modes[0:2], opcode_and_modes[2:]

        first_val, first_val_w = get_vals(pointer + 1, modes[0], rel_base)
        second_val, _ = get_vals(pointer + 2, modes[1], rel_base)
        _, third_val_w = get_vals(pointer + 3, modes[2], rel_base)

        # kinda ugly but whatever
        if opcode == ["3", "0"]:
            ops[first_val_w] = int(input("inp: \n"))
            pointer += 2
        elif opcode == ["4", "0"]:
            print(first_val)
            pointer += 2
        elif opcode == ["9", "9"]:
            break
        elif opcode == ["5", "0"]:
            if first_val != 0:
                pointer = second_val
            else:
                pointer += 3
        elif opcode == ["6", "0"]:
            if first_val == 0:
                pointer = second_val
            else:
                pointer += 3
        elif opcode == ["7", "0"]:
            ops[third_val_w] = 1 if first_val < second_val else 0
            pointer += 4
        elif opcode == ["8", "0"]:
            ops[third_val_w] = 1 if first_val == second_val else 0
            pointer += 4
        elif opcode == ["9", "0"]:
            rel_base += first_val
            pointer += 2
        elif opcode == ["2", "0"] or opcode == ["1", "0"]:
            vals = [first_val, second_val]
            new_val = reduce(add if opcode == ["1", "0"] else mul, vals, 0 if opcode == ["1", "0"] else 1)
            ops[third_val_w] = new_val
            pointer += 4
        else:
            raise Exception("invalid op")

ops = [int(i) for i in lines[0].split(",")]

intcode(ops)