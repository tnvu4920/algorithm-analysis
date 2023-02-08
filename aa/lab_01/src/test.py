def reverse(string):
    return ' '.join(string[::-1].split()[::-1])


a = 1234567
b = sum(map(int, list(str(a))))

# чекнуть про типы в пандасе (одинаковыве или нет)
