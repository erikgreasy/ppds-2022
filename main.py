"""Copyright 2022 Erik Masny.

Simple coprograms implementation.
"""


def cat(f, next_fnc):
    """Read line by line passed file"""
    next(next_fnc)
    for line in f:
        next_fnc.send(line)
    next_fnc.close()


def grep(substr, next_fnc):
    """Count number of substr occurences in line"""
    next(next_fnc)
    try:
        while True:
            line = (yield)
            next_fnc.send(line.count(substr))
    except GeneratorExit:
        next_fnc.close()


def wc(substr):
    """Count number of total occurences for substr"""
    cnt = 0
    try:
        while True:
            cnt += (yield)
    except GeneratorExit:
        print(substr, cnt)


def dispatch(greps):
    """Dispatcher to implement layer for multi greps"""
    for g in greps:
        next(g)
    try:
        while True:
            line = (yield)
            for g in greps:
                g.send(line)
    except GeneratorExit:
        for g in greps:
            g.close()


def main():
    """Main program code"""
    f = open('LICENSE')
    substr = ['to', 'free', 'complain']
    greps = []

    for s in substr:
        w = wc(s)
        g = grep(s, w)
        greps.append(g)

    d = dispatch(greps)
    cat(f, d)


if __name__ == '__main__':
    main()
