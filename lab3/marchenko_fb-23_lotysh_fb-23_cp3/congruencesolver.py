#Finds the Bézout coefficient for a mod b and the GCD
def ExtendedEuclidean(a,b):
    old_r, r = a, b
    old_s, s = 1, 0
    
    while(r!=0):
        q=old_r//r
        old_r, r=r, old_r-q*r
        old_s, s=s, old_s-q*s

    return (old_s%b, old_r) #x, GCD

#Returns a list of solutions mod m
#Use CongruenceSolve(a,b,m)[0] to get the solution if you know there's only one
#(There's only 1 solution if a and m are coprime)
def CongruenceSolve(a,b,m):
    if(b==0):
        return [0]
    inverse, gcd = ExtendedEuclidean(a,m)
    if(gcd!=1):
        gcd=ExtendedEuclidean(gcd, b)[1]
        if(gcd==1):
            return [] #no solutions
        else:
            x0 = CongruenceSolve(a//gcd, b//gcd, m//gcd)[0]
            return [x0+i*(m//gcd) for i in range(gcd)]

    else:
        gcd_ab=ExtendedEuclidean(a,b)[1]
        a1=a//gcd_ab
        b1=b//gcd_ab
        return [b1*ExtendedEuclidean(a1, m)[0]%m]
    
