
M_AES = 0b100011011 # modul AES
M = 0b111001111 # 0b100011101 # modul
G = 0b00000010  # generador


def suma(a, b):
        return a ^ b

def prod(a, b):
    acum = 0
    for i in range(0, len(bin(a)) - 1):
        k = 7 - i
        if (a >> i) % 2 == 1:
            acum = acum ^ (b << i)
    return acum

def prod_mod(a, b, m):
    d = prod(a,b)
    m_grade = len(bin(m))-2
    d_grade = len(bin(d))-2
    while d_grade >= m_grade:
        d = suma(d, (m << (d_grade - m_grade)))
        d_grade = len(bin(d))-2
    return d

def divisio(a, b):
    #print("DIV:", a, "//", b, "...")
    if b == 1:
        return a, 0
    Dividend = a
    divisor = b
    quocient = 0
    residu = 0
    Dividend_grade = len(bin(Dividend))-2
    divisor_grade = len(bin(divisor))-2
    while Dividend_grade >= divisor_grade:
        quocient = quocient + 2 ** (Dividend_grade - divisor_grade)
        Dividend = suma(Dividend, prod(divisor, 2 ** (Dividend_grade - divisor_grade))) #resta
        Dividend_grade = len(bin(Dividend))-2
    residu = Dividend
    #print("DIV:", a, "//", b, "=", quocient, "<=>", bin(a), "//", bin(b), "=", bin(quocient))
    return (quocient, residu)

def es_generador(a, m):
    ultim = 1
    r = [ultim]
    for i in range(1, 256 - 1): # "-1" pel pel 0
        ultim = prod_mod(ultim, a, m)
        r.append(ultim)
    for i in range(1, 256):
        if i not in r:
            return False
    return True

def taules16x16(g, m):
    # EXP table
    e = []
    ultim = 1
    for i in range(0, 16):
        row = []
        for j in range(0, 16):
            row.append(ultim)
            ultim = prod_mod(ultim, g, m)
        e.append(row)
    
    # LOG table
    l = [ [ None for x in range(16) ] for y in range(16) ]
    for i in range(0, 16):
        for j in range(0, 16):
            v = e[i][j]
            l[int(v/16)][v%16] = 16*i + j
            print("v=",v,"L[",int(v/16),"] [",v%16,"] = ", 16*i + j)
    l[0][1]=0
    return (e, l)

def taules(g, m):
    # EXP table
    e = []
    ultim = 1
    for i in range(0, 256):
        e.append(ultim)
        ultim = prod_mod(ultim, g, m)
    
    # LOG table
    l = [None for y in range(256) ]
    for i in range(0, 256):
        l[e[i]] = i
    #correccio del 1: 
    #apareix dos cops, a [0] i a [255], es queda amb el 255. El posem a 0:
    l[1] = 0
    return (e, l)

def gcd_extendido_OLD(a, b):
    if a == 0:
        return b, 0, 1

    (q, r) = divisio(b, a)
    
    gcd, x1, y1 = gcd_extendido(r, a) # r = b%a

    x = y1 ^ prod(q, x1) # q = b//a
    y = x1

    return gcd, x, y

def gcd_extendido(b, a):

    x0 = 0
    x1 = 1
    y0 = 1
    y1 = 0

    while True:
        q, r = divisio(b, a)
        b = a

        if r == 0:
            break
    
        a = r
        if q == 0 or x1 == 0:
            x2 = x0
        elif x0 == 0:
            x2 = prod(x1, q)
        else:
            mulres = prod(x0, mulres)
            x2 = suma(x0, mulres)
        
        if q == 0 or y1 == 0:
            y2 = y0
        elif y0 == 0:
            y2 = prod(y1, q)
        else:
            mulres = prod(y1, q)
            y2 = suma(y0, mulres)
        
        y0 = y1
        x0 = x1
        y1 = y2
        x1 = x2

    return y2, x2, b

def inverso_euclides(a, m):
    return gcd_extendido(a, m)[0]


# Galois-Field Encapsulacions

def GF_product_p(a, b):
    m = M
    return prod_mod(a, b, m)

def GF_es_generador(a):
    m = M
    return es_generador(a, m)

def GF_tables():
    g = G
    m = M
    return taules(g, m)

def GF_product_t(a, b):
    if a == 0 or b == 0:
        return 0
    return e[(l[a] + l[b])%255]

def GF_invers_taula(a): # OLD
    return e[255 - l[a]]

def GF_invers(a): #NEW
    if a == 0:
        return 0
    m = M
    return inverso_euclides(a, m)

def main():

    m = M
    a = 67 # 0b00110011 # 0x33
    b = 6 # 0b10000011
    
    print("== MODUL ============= ", bin(m))
    print("== SUMA ============== ", bin(suma(a, b)))
    print("== PRODUCTE ========== ", bin(prod(a, b)))
    print("== PROD. MODULAR ===== ", bin(prod_mod(a, b, m)))
    print("== ES GENERADOR ====== ", GF_es_generador(G))
    print("== TAULA EXP ========= ")
    print(str(e))
    print("== TAULA LOG ========= ")
    print(str(l))
    print("== PROD. MOD (TAULA) = ", bin(GF_product_t(a, b)))
    print("== INVERS (TAULA) ==== ", bin(GF_invers_taula(a)))
    print("== INVERS EUCLIDES === ", bin(GF_invers(a)))
    
    # TESTING

    for i in range(1, 255):
        
        if GF_product_t(i, GF_invers(i)) != 1 :
            raise InversNoElementNeutre
        
        if GF_product_t(i, a) != GF_product_t(a, i) :
            raise ProducteNoCommutatiu
        
        if GF_product_t(i, a) != GF_product_p(i, a) :
            raise ProducteF
        
        if GF_product_t(i, 0) != 0 :
            raise ElementNoAbsorbent
        
        if GF_invers(i) != GF_invers_taula(i) :
            raise CalculInversEuclidesIncorrecte
    
        

(e,l) = GF_tables() #taules exp. log.
main()