try:
    x = open('settings.dat', 'r')
    print(x.read())
except FileNotFoundError:
    x = open('settings.dat', 'w')
