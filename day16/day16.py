with open("input.txt", "r") as f:
    lines = f.readlines()

input = lines[0]

numbers = [int(c) for c in input]

def run(numbers):
    phase = 0
    base_pattern = [0,1,0,-1]

    while phase < 100:
        new = []
        for i in range(1, len(numbers) + 1):
            sum = 0
            for j, n in enumerate(numbers):
                pattern_idx = ((j + 1) // i) % 4
                pattern = base_pattern[pattern_idx]
                sum += pattern * n
            new.append(abs(sum) % 10)
        numbers = new
        # print(phase)
        phase += 1
    
    return numbers

res1 = run(numbers)

ans1 = "".join(str(c) for c in res1)[:8]
print(ans1)

# had to look this up :( such disappoint
def smart_run(numbers):
    phase = 0
    while phase < 100:
        new = []
        tmp = sum(numbers)
        new.append(tmp % 10)
        for i in range(0, len(numbers) -1):
            tmp -= numbers[i]
            new.append(tmp % 10)
        numbers = new
        phase += 1
        # print(phase)
    
    return numbers

from_idx = int("".join(str(c) for c in numbers[0:7]))
long_numbers = numbers * 10000
res2 = smart_run(long_numbers[from_idx:])
print("".join(str(n) for n in res2[0:8]))
