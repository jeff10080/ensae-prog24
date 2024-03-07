import random
import matplotlib.pyplot as plt
import numpy as np

p_list = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1]
k_list = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1]

def bernoulli(p) :
    if random.random() <= p :
        return 1
    else :
        return 0
   
def X_et_p(n, p, k) : #construit tous les X_i et leurs probas p_i
    P_list = [p]
    X_list = [["Départ"]]
    for i in range(1, n+1) :
        X_precedent = bernoulli(P_list[i-1])
        if X_precedent == 1 :
            P_list.append(p)
        if X_precedent == 0 :
            P_list.append(k * P_list[i-1])
        X_list.append(X_precedent)
    return (X_list, P_list)
           
def nb_victoires(n, p, k) :
    X = X_et_p(n, p, k)[0]
    compt = 0
    for i in range(1, n+1) :
        compt+=X[i]
    return compt

def esperance_vict(n, p, k) :
    S = 0
    for _ in range(10000) :
        S += nb_victoires(n, p, k)
    return S/10000

def graphe_proba_loserq(n, p, k) :
    plt.plot(X_et_p(n, p, k)[1])
    plt.xlabel("Numéro du lancer n")
    plt.ylabel("P(gagner la n-ième game) pour p = {} et k = {}".format(p, k))
    plt.show()

def tracer_E_en_fonct_de_k(n, p) :
    E_k = [esperance_vict(n, p, j) for j in k_list]
    plt.plot(k_list, E_k)
    plt.axis((0.1, 1, 0, p * n))
    plt.xlabel("k")
    plt.ylabel("E(nb_victoires) pour p = {}".format(p))
    plt.show()

def tracer_E_en_fonct_de_p(n, k) :
    E_p = [esperance_vict(n, q, k) for q in p_list]
    plt.plot(p_list, E_p)
    plt.axis((0, 1, 0, n))
    plt.xlabel("p")
    plt.ylabel("E(nb_victoires) pour k = {}".format(k))
    plt.show()

def tracer_E_en_fonct_de_k_et_p(n) :
    E_k_p = [esperance_vict(n, p, k) for p in p_list for k in k_list]
    E = np.array(E_k_p).reshape(len(p_list), len(k_list))
    K, P = np.meshgrid(k_list, p_list)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_surface(K, P, E, cmap='viridis')
    ax.set_xlabel('k')
    ax.set_ylabel('p')
    ax.set_zlabel('E(k, p)')
    fig.colorbar(surf)
    plt.show()

def k_sachant_E_et_p(n, E, p) :
    if E <= p*n : #l'espérance est majorée par celle de n Bernoulli, car p_n <= p
        E_k = [esperance_vict(n, p, j) for j in k_list]
        k =  np.interp(E, E_k, k_list)
        return k
    else :
        print("Espérance inatteignable")
   
def p_sachant_E_et_k(n, E, k) :
    E_p = [esperance_vict(n, q, k) for q in p_list]
    p =  np.interp(E, E_p, p_list)
    return p

#graphe_proba_loserq(100, 0.5, 0.7)
#tracer_E_en_fonct_de_k(100, 0.9)
tracer_E_en_fonct_de_p(100, 0.2)
#print(esperance_vict(1000, 0.5, 0.5))
#print(k_sachant_E_et_p(1000, 333, 0.6))