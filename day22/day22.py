import re

with open("input.txt", "r") as f:
    lines = f.readlines()
N_CARDS = 10007

cards = list(range(0,N_CARDS))

instructions = []
cleaned = [l.strip() for l in lines]
for line in cleaned:
    if line == "deal into new stack":
        instructions.append(("S"))
    elif line.startswith("deal with increment"):
        search = re.search("\d+", line)
        instructions.append(("I", int(search.group())))
    else:
        search = re.search("-?\d+", line)
        instructions.append(("C", int(search.group())))

for ins in instructions:
    next_deck = cards.copy()

    if ins[0] == "I":
        inc = ins[1]
        init = [-1 for _ in range(0,N_CARDS)]
        for i in range(0, N_CARDS):
            init[(i * inc) % N_CARDS] = cards[i]
        cards = init

    elif ins[0] == "S":
        cards = cards[::-1]
    else:
        inc = ins[1]
        cards = cards[inc:] + cards[:inc]

ans1 = cards.index(2019)
print(ans1)

idx = 2020
N_CARDS = 119315717514047
N_TIMES = 101741582076661

# I tried going backwards to see if there's a repeat somewhere and there wasn't (probably the reverse instructions were wrong anyway)
# Had to resort to reddit to figure this out https://www.reddit.com/r/adventofcode/comments/ee0rqi/comment/fbnkaju/

def f(idx, instrs):
    for ins in instrs[::-1]:
        if ins[0] == "S":
            idx = N_CARDS - idx - 1 % N_CARDS
        elif ins[0] == "C":
            idx = idx + ins[1] % N_CARDS
        else:
            idx = pow(ins[1], -1, N_CARDS) * idx % N_CARDS
    return idx

X = f(idx, instructions)
Y = f(X, instructions)

# X = ai + b % N_CARDS
# Y = aX + b % N_CARDS
# subtract lower from upper
# => a = (X - Y) / (idx - X) mod N_CARDS ≈ (X - Y) * modinv(idx - X, N_CARDS) mod N_CARDS
# from the first equation
# => b = X - ai mod N_CARDS

a = (X - Y) * pow(idx - X, -1, N_CARDS) % N_CARDS
b = (X - a * idx) % N_CARDS

# f(i) = ax + b
# f(f(i)) = a(ax + b) + b = a^2*X + ab +b
# f(f(f(i))) = a(a^2 + ab +b) + b = a^3*X + ba^2 + ab + b
# => f_n(i) = a^n*X + b*(a^(N_TIMES) - 1) * modinv(a - 1, N_CARDS) mod N_CARDS

ans2 = pow(a, N_TIMES, N_CARDS) * idx + \
    (b * (pow(a, N_TIMES, N_CARDS) - 1) * pow(a-1, -1, N_CARDS))

ans2 = ans2 % N_CARDS

print(ans2)
