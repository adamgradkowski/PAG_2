import numpy as np
#testowy plik do implementacji algorytmu Dijskra

#pkt A to star pkt B to koniec
A_x = 3
A_y = 3
B_x = 20
B_y = 21

#testowe dane
dane_id = ['A','a','b','c','d','e','f','g','h','i','j','k','l','m','B']
dane_x = [3,3,9,9,16,16,20,9,15,12,19,20,9,15,20]
dane_y = [3,10,10,3,3,12,12,16,16,21,18,18,21,18,21]

lista = [dane_id,dane_x,dane_y]

dane_id_E = [1,2,3,4,4,5,6,7,8,9,10,11,12,13,14,15,16,17]
dane_P = ['A','A','a','c','c','b','g','g','l','i','h','m','d','e','f','k','j']
dane_K = ['c','a','b','b','d','g','l','h','i','B','m','j','e','f','k','j','B']
lista2 = [dane_id_E,dane_P,dane_K]
array_E = np.array(zip(*lista2))

n = 999999999999 #nieskonczonosc
S = [] # lista wierzcholkow przetworzonych
Q = []# lista wszystkich wiezcholkow
d = [n,n,n,n,n,n,n,n,n,n,n,n,n,n,n] # tymczasowa waga sciezki dla danego wierzcholka
p = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1] # poprzedni wierzcholek w sciezce
Q.extend(dane_id)

pkt_P = 'A'
pkt_K = 'B'
start = dane_id.index(pkt_P)
koniec = dane_id.index(pkt_K)
d[start] = 0


w_p = pkt_P

S.append(dane_id[dane_id.index(w_p)])
Q.remove(dane_id[dane_id.index(w_p)])
d_kopia = []
d_kopia.extend(d)
d_kopia[dane_id.index(w_p)] = n


#tu rozpoczne petle
while len(Q) != 0 :
    wp_i = [i for i, x in enumerate(dane_P) if x == w_p]
    for i in wp_i:
        id_sasiad = dane_id.index(dane_K[i])
        odl = np.sqrt((dane_x[id_sasiad] - dane_x[dane_id.index(w_p)]) ** 2 + (dane_y[id_sasiad] - dane_y[dane_id.index(w_p)]) ** 2)
        if d[id_sasiad] > d[dane_id.index(w_p)] + odl:
            d[id_sasiad] = d[dane_id.index(w_p)] + odl
            d_kopia[id_sasiad] = d[dane_id.index(w_p)] + odl
            p[id_sasiad] = dane_id[dane_id.index(w_p)]

    n_w_d = d_kopia.index(np.min(d_kopia))
    w_p = dane_id[n_w_d]
    S.append(dane_id[n_w_d])
    Q.remove(dane_id[n_w_d])
    d_kopia[n_w_d] = n

print(p)
print(pkt_K)
tab_do_rysowania = []
while pkt_K != pkt_P:
    d_id  = dane_id.index(pkt_K)
    q = p[d_id]
    tab_do_rysowania.append(q)
    print(q)
    d_id = dane_id.index(q)
    pkt_K = q



