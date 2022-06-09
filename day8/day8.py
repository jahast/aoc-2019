with open("input.txt", "r") as f:
    lines = [l.strip() for l in f.readlines()]

pixels = [c for c in lines[0]]

def chunk(ls, size):
    return [ls[i:(i + size)] for i in range(0,len(ls), size)]

layers = chunk(pixels, 25 * 6)

least_zeroes = min(layers, key= lambda x: x.count("0"))

ans1 = least_zeroes.count("1") * least_zeroes.count("2")
print(ans1)

ans2 = []
for j in range(6):
    ans2 += [["2"] * 25]

for layer in layers:
    chunked = chunk(layer, 25)
    for j in range(6):
        for i in range(25):
            if ans2[j][i] == "2":
                ans2[j][i] = chunked[j][i]

ans2_image = "\n".join(["".join(r) for r in ans2])
print(ans2_image)
