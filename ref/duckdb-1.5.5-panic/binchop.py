with open("bulk.jsonl", "r") as f:
    lines = [line for line in f]

lo = 0
hi = len(lines)

while lo < hi:
    mid = (lo + hi) // 2
    print(f"lo: {lo}, hi: {hi}, lines: {mid}")
    with open("sample.jsonl", "w") as f:
        f.writelines(lines[0:mid])

    fail = input("Failed?")
    if fail.lower().startswith("y"):
        hi = mid
    else:
        lo = mid + 1
