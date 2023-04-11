def calculate_trapped_scores(num):
    res = 0
    for i in range(num + 1):
        res += 4 * i ** 2
    return res
print(calculate_trapped_scores(8))