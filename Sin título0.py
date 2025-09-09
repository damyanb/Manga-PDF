#ejercicio 2.1)
def rotation(n,s):
    ns = len(s)
    N = n % ns # numero de rot efectiva
    sc = s
    while N>0:
        for i in range(0,ns-1):
            sc[i] = s[i+1]
            print()
        sc[ns-1] = s[0]
        s = sc
        N -=1
    print(s)
s = [1, 2, 3]
rotation(2,s)