import math, random
from congruencesolver import ExtendedEuclidean
from hornerpow import HornerPow

def MillerRabin(p):
    k=16
    p1=p-1
    bits=format(p1, 'b')
    s=0
    d=p1
    while(not(d&1)):
        s+=1
        d=d>>1
    for i in range(k):
        x=random.randrange(2,p-1)
        gcd=ExtendedEuclidean(x,p)[1]
        if(gcd>1):
            return False
        xr=HornerPow(x, d, p)
        if(xr==1 or xr==p1):
            continue
        for r in range(1,s+1):
            xr=HornerPow(xr, 2, p)
            if(xr==p1):
                break;
            elif(xr==1):
                return False
            else:
                continue
        if(xr!=p1):
            return False
    return True
        
        

def generatePrimeNumber(minlen, maxlen):
    while True:
        p=random.randrange(2**minlen,2**(maxlen+1))
        if(not (p&1)):
            continue
        if MillerRabin(p):
            return p
        else:
            continue

def GenerateKeyPair():
    p=generatePrimeNumber(256,512)
    q=generatePrimeNumber(256,512)
    n=p*q
    e=65537 #2**16 + 1
    d=ExtendedEuclidean(e,(p-1)*(q-1))
    return ((d,p,q),(e,n))

def GenerateKeyPairs():
    A=GenerateKeyPair()
    B=GenerateKeyPair()
    if(A[0][1]*A[0][2]>B[0][1]*B[0][2]):
        A, B=B, A
    return (A, B)
