for i in range(1, 13):
    b = 168 % i
    if b == 0:
        c = 168/i + i
        if c % 2 == 0:
            n = c/2
            print 'n:', n
            m = n - i
            print 'm:', m
            z = m**2 + n**2 - 368
            if z % 2 == 0:
                x = z/2
                print 'x:', x
            print '--------------'
