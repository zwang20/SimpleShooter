try:
    x = open('settings.dat', 'r')
except FileNotFoundError:
    pass

x = open('settings.dat')
