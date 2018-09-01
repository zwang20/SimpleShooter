
try:
    x = open('settings.dat', 'r')
    y = x.read()
    print(y)
    z = y.split('\n')
    print(z)
    e = []
    for t in z:
        if t:
            e.append(t.split(' = '))
    print(e)
    w = dict(e)
    print(w)
except FileNotFoundError:
    x = open('settings.dat', 'w')
