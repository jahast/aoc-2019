from operator import add, mul
from functools import reduce
from collections import defaultdict

def intcode2(ops_ls, phase, input, state = None):
    pointer = 0
    if state == None:
        ops = defaultdict(int, {k:v for k,v in enumerate(ops_ls)})
        inputs = [phase, input]
    else:
        ops, pointer = state["ops"], state["pointer"]
        inputs = [input]
    while True:
        op = ops[pointer]
        opcode_and_modes = [c for c in str(op)][::-1]
        opcode_and_modes += "0" * (5 - len(opcode_and_modes))
        opcode, modes = opcode_and_modes[0:2], opcode_and_modes[2:]

        first_val = ops[ops[pointer + 1]] if modes[0] == "0" else ops[pointer + 1]
        second_val = ops[ops[pointer + 2]] if modes[1] == "0" else ops[pointer + 2]
        third_val = ops[pointer + 3]

        # kinda ugly but whatever
        if opcode == ["3", "0"]:
            ops[ops[pointer + 1]] = inputs.pop(0)
            pointer += 2
        elif opcode == ["4", "0"]:
            pointer += 2
            return first_val, {'ops': ops, 'pointer': pointer}
        elif opcode == ["9", "9"]:
            return None, {}
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
            ops[third_val] = 1 if first_val < second_val else 0
            pointer += 4
        elif opcode == ["8", "0"]:
            ops[third_val] = 1 if first_val == second_val else 0
            pointer += 4
        elif opcode == ["2", "0"] or opcode == ["1", "0"]:
            vals = [first_val, second_val]
            new_val = reduce(add if opcode == ["1", "0"] else mul, vals, 0 if opcode == ["1", "0"] else 1)
            ops[third_val] = new_val
            pointer += 4
        else:
            raise "not gud"
