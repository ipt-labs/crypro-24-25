def HornerPow(base, exp, mod):
    lng=exp.bit_length()
    y=1
    for i in reversed(range(lng)):
        y=(y*y)%mod
        if(not not(exp & (1 << i))):
            y=(y*base)%mod
    return y
