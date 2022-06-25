from math import ceil
from collections import defaultdict

with open("input.txt", "r") as f:
    lines = [l.strip() for l in f.readlines()]

reactions = {}

for line in lines:
    left, right = line.split("=>")

    result_quantity_raw, result_chem_raw = right.strip().split(" ")
    result_q, result_c = int(result_quantity_raw), result_chem_raw.strip()

    inputs = []
    for input in left.split(","):
        inp_quantity_raw, inp_chem_raw = input.strip().split(" ")
        inp_q, inp_c = int(inp_quantity_raw), inp_chem_raw.strip()
        inputs.append((inp_c, inp_q))
    
    reactions[result_c] = (result_q, inputs)

# my solution seems pretty complicated and slow
# there's probably a better way than this
def recurse_requirements(cur_el, how_many, surplus, reactions):
    result_q, inps = reactions[cur_el]

    in_surplus = surplus[cur_el]
    new_chem_req = how_many - in_surplus
    used_surplus = 0
    if new_chem_req == 0:
        surplus[cur_el] = 0
        used_surplus = in_surplus
        return surplus
    if new_chem_req < 0:
        surplus[cur_el] -= how_many
        used_surplus = how_many
        return surplus
    else:
        new_need_mult = ceil(new_chem_req / result_q)
        new_surplus = new_need_mult * result_q - new_chem_req    
        surplus[cur_el] = new_surplus
        used_surplus = in_surplus
    
    if inps[0][0] == "ORE":
        new_ore = new_need_mult * inps[0][1]
        surplus["ORE"] += new_ore
        return surplus

    for r in inps:
        total_need = how_many - used_surplus
        new_how_many = ceil(total_need / result_q) * r[1]
        surplus = recurse_requirements(r[0], new_how_many, surplus, reactions)
    
    return surplus


surplus = recurse_requirements("FUEL", 1, defaultdict(int), reactions)

ans1 = surplus["ORE"]
print(ans1)

ans2 = 0
surplus = defaultdict(int)

# and after some googling I could found the solution million times quicker
# by adjusting the "1" argument to the recurse_requirements function
while surplus["ORE"] < 1000000000000:
    surplus = recurse_requirements("FUEL", 1, surplus, reactions)
    ans2 += 1
    if ans2 % 100000 == 0:
        print(f"iters: {ans2}, ore: {surplus['ORE']}")

print(ans2 - 1)
