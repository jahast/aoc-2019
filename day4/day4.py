pmax = 576723
pmin = 109165

ans1 = 0
n_len = len(str(pmax))
for i in range(pmax, pmin, -1):
    as_array = [int(n) for n in str(i)]
    has_same_adj = any(as_array[j] == as_array[j+1] for j in range(n_len - 1))
    if not has_same_adj:
        continue
    
    has_decrease = any(as_array[j] > as_array[j+1] for j in range(n_len - 1))
    if has_decrease:
        continue

    ans1 += 1

print(ans1)

ans2 = 0
for i in range(pmax, pmin, -1):
    as_array = [int(n) for n in str(i)]

    potential_doubles = [as_array[j] for j in range(n_len - 1) if as_array[j] == as_array[j+1]]
    has_single_double = any(p for p in potential_doubles if as_array.count(p) == 2)
    if not has_single_double:
        continue
    
    has_decrease = any(as_array[j] > as_array[j+1] for j in range(n_len - 1))
    if has_decrease:
        continue

    ans2 += 1

print(ans2)