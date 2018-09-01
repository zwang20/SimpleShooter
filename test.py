
try:
    x = open('settings.dat', 'r')
    y = x.read()
    print(y)
    z = y.split('\n')
    print(z)
    w = dict(z)
    print(w)
except FileNotFoundError:
    x = open('settings.dat', 'w')
