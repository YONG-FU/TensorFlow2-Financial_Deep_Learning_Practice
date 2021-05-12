def find_roots(a, b, c):
    x1 = (-b + (b ** 2 - 4 * a * c) ** 0.5) / (2 * a)
    x2 = (-b - (b ** 2 - 4 * a * c) ** 0.5) / (2 * a)
    return tuple([x1, x2])

print(find_roots(2, 10, 8))
# should print (-1, -4) or (-4, -1)
