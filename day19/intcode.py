from operator import add, mul
from functools import reduce
from collections import defaultdict


class Intcode:
    def __init__(self, ops_ls):
        self.ops = defaultdict(int, {k: v for k, v in enumerate(ops_ls)})
        self.pointer = 0
        self.rel_base = 0
        self.inputs = []

    def add_input(self, inputs):
        if type(inputs) == list:
            self.inputs.extend(inputs)
        else:
            self.inputs.append(inputs)

    def input_and_run(self, inputs):
        self.add_input(inputs)
        return self.run()

    def get_vals(self, pointer, mode):
        if mode == "0":
            return self.ops[self.ops[pointer]], self.ops[pointer]
        elif mode == "1":
            return self.ops[pointer], None
        elif mode == "2":
            return self.ops[self.rel_base + self.ops[pointer]], self.rel_base + self.ops[pointer]
        else:
            raise Exception("invalid mode")

    def run(self):
        while True:
            op = self.ops[self.pointer]
            opcode_and_modes = [c for c in str(op)][::-1]
            opcode_and_modes += "0" * (5 - len(opcode_and_modes))
            opcode, modes = opcode_and_modes[0:2], opcode_and_modes[2:]

            first_val, first_val_w = self.get_vals(self.pointer + 1, modes[0])
            second_val, _ = self.get_vals(self.pointer + 2, modes[1])
            _, third_val_w = self.get_vals(self.pointer + 3, modes[2])

            if opcode == ["3", "0"]:
                if len(self.inputs) == 0:
                    return "inp"
                self.ops[first_val_w] = self.inputs.pop(0)
                self.pointer += 2
            elif opcode == ["4", "0"]:
                self.pointer += 2
                return first_val
            elif opcode == ["9", "9"]:
                return None
            elif opcode == ["5", "0"]:
                if first_val != 0:
                    self.pointer = second_val
                else:
                    self.pointer += 3
            elif opcode == ["6", "0"]:
                if first_val == 0:
                    self.pointer = second_val
                else:
                    self.pointer += 3
            elif opcode == ["7", "0"]:
                self.ops[third_val_w] = 1 if first_val < second_val else 0
                self.pointer += 4
            elif opcode == ["8", "0"]:
                self.ops[third_val_w] = 1 if first_val == second_val else 0
                self.pointer += 4
            elif opcode == ["9", "0"]:
                self.rel_base += first_val
                self.pointer += 2
            elif opcode == ["2", "0"] or opcode == ["1", "0"]:
                vals = [first_val, second_val]
                new_val = reduce(add if opcode == [
                                 "1", "0"] else mul, vals, 0 if opcode == ["1", "0"] else 1)
                self.ops[third_val_w] = new_val
                self.pointer += 4
            else:
                raise Exception("invalid op")
