import numpy as np
#A punkt startowy B punkt koncowy istnieja dwie trasy
#dane testowe wspolrzedna wierzcholkow
dane_id = ['A','B','C','D','E','F']
dane_x  = [4,21,54,12,789,876]
dane_y  = [6,21,23,567,123,987]

#dane testowe krawedzie
dane_id_E = [1,2,3,4,5,6,7,8,9,10]
dane_dl = [100,200,300,200,799,765,765,98,72,100]
dane_P = ['A','A','B','C','D','D','B','B','C','E']
dane_K = ['B','C','D','D','E','F','C','E','F','F']

n = 999999999999 #nieskonczonosc
S = []
Q = []
f = [n,n,n,n,n,n]
g = [n,n,n,n,n,n]
p = [-1,-1,-1,-1,-1,-1]
pkt_P = 'A'
pkt_K = 'F'

w_p = pkt_P
w_k =''

S.append(dane_id[dane_id.index(w_p)])
g[dane_id.index(w_p)] = 0
f[dane_id.index(w_p)] = 0



while w_p != pkt_K:
    #indeks punktu ktorego sprawdzamy - glownego

    wp_i = [i for i, x in enumerate(dane_P) if x == w_p]

    for i in wp_i:
        if dane_K[i] in S:
            wp_i.remove(i)
    for i in wp_i:
        id_sasiad = dane_id.index(dane_K[i])
        # dodajemy sasiadow ktorych sa polaczenia z glownego
        Q.append(dane_K[i])
        if i > len(dane_id):
            i = dane_id.index(dane_K[i])
        odl_p = dane_dl[i]
        heu=np.sqrt((dane_x[id_sasiad] - dane_x[dane_id.index(w_p)]) ** 2 + (dane_y[id_sasiad] - dane_y[dane_id.index(w_p)]) ** 2)
        g[id_sasiad] = g[dane_id.index(w_p)]+odl_p
        f[id_sasiad] = g[id_sasiad] + heu
        w_k = dane_id[id_sasiad]
        if f[id_sasiad] > f[dane_id.index(w_p)] + odl_p and w_p !=pkt_P:
            f[id_sasiad] = f[dane_id.index(w_p)] + odl_p
            p[id_sasiad] = dane_id[dane_id.index(w_p)]
        elif w_p == pkt_P:
            f[id_sasiad] = f[dane_id.index(w_p)] + odl_p
            p[id_sasiad] = dane_id[dane_id.index(w_p)]
    szukaj = [item for item in dane_id if item not in S]
    z = []
    for i in szukaj:
        z.append(f[dane_id.index(i)])

    n_w_d = z.index(np.min(z))
    n_w = szukaj[n_w_d]
    n_w_i = dane_id.index(n_w)
    S.append(dane_id[n_w_i])
    w_p = dane_id[n_w_i]




print("p"+"=" *40)
print(p)
tab_do_rysowania = []
print(pkt_P)
print(pkt_K)

tab_do_rysowania.append(pkt_K)
w_K = ''
while w_K !=pkt_P:
    i_K = dane_id.index(pkt_K)
    w_K = p[i_K]
    print(w_K)
    tab_do_rysowania.insert(0,w_K)
    pkt_K = w_K

print("tab"+"="*40)
print(tab_do_rysowania)
print "Zbior S " + "=" *40
print(S)
print "Zbior Q " + "=" *40
print(Q)

