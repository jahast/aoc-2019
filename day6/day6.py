with open("input.txt", "r") as f:
    lines = [l.strip() for l in f.readlines()]

orbs = {s.split(")")[1]:s.split(")")[0] for s in lines}

ans1 = 0
for k,v in orbs.items():
    temp_val = v
    while temp_val != "COM":
        ans1 += 1
        temp_val = orbs[temp_val]
    ans1 += 1
print(ans1)

my_path = ["YOU"]
while (last := my_path[-1]) != "COM":
    my_path.append(orbs[last])

san_path = ["SAN"]
while (last := san_path[-1]) != "COM":
    san_path.append(orbs[last])

intersects = set(my_path).intersection(set(san_path))

ans2 = min(my_path.index(inters) + san_path.index(inters) - 2 for inters in intersects)
print(ans2)