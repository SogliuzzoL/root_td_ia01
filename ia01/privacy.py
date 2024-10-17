def est_identique(d1, d2, attributs):
    """Calcule si d1 et d2 sont identiques selon une liste d'attributs

    Paramètres
    ----------
    d1 : dict
        Individu 1 décrit un par dictionnaire
    d2 : dict
        Individu 2 décrit un par dictionnaire
    attributs : list
        Liste des attributs selon lesquels d1 et d2 sont comparés

    Sorties
    -------
    boolean
        True si d1[a] == d2[a] pour tout a dans attributs
    """
    for attribut in attributs:
        if d1[attribut] != d2[attribut]: return False
    return True

def groupe(data, attributs):
    """Regroupe les individus partageant les mêmes attributs

    Paramètres
    ----------
    data : list[dict]
        Liste d'individus décrits par un dictionnaire
    attributs : list
        Liste des attributs selon lesquels les individus sont comparés

    Sorties
    -------
    G : list
        Liste contenant pour chaque individu un indice representant son groupe
        Tous les individus du même groupe sont égaux selon les attributs considérés
        Les groupes sont indexés de 1 jusqu'à max(G) et il y a exactement max(G) groupes différents
    """
    Groupe = []
    G = []
    for element in data:
        if Groupe == []:
            Groupe.append([element])
            G.append(len(Groupe))
        else:
            ajoute = False
            for i, g in enumerate(Groupe):
                if est_identique(element, g[0], attributs):
                    ajoute = True
                    g.append(element)
                    G.append(i + 1)
                    break
            if not ajoute:
                Groupe.append([element])
                G.append(len(Groupe))
    return G

def groupe2(data, attributs):
    Groupe = []
    G = []
    for element in data:
        if Groupe == []:
            Groupe.append([element])
            G.append(len(Groupe))
        else:
            ajoute = False
            for i, g in enumerate(Groupe):
                if est_identique(element, g[0], attributs):
                    ajoute = True
                    g.append(element)
                    G.append(i + 1)
                    break
            if not ajoute:
                Groupe.append([element])
                G.append(len(Groupe))
    return Groupe

def k_anonymite(data, attributs):
    """k-anonymité d'un jeu de données selon une liste d'attributs

    Paramètres
    ----------
    data : list[dict]
        Liste d'individus décrits par un dictionnaire
    attributs : list
        Liste des attributs selon lesquels les individus sont comparés

    Sorties
    -------
    k : int
        k-anonymité de data selon la liste d'attributs
    """
    G = groupe(data, attributs)
    count = [0 for _ in range(max(G))]
    for g in G:
        count[g - 1] += 1
    return min(count)

def discret_seuils(X, k):
    """Calcule les seuils de discrétisation de X pour avoir au moins k éléments par interval

    Paramètres
    ----------
    X : list
        Liste de valeurs à discrétiser
    k : int
        Nombre minimal d'élément entre deux seuils consécutifs

    Sorties
    -------
    seuils : list
        Le nombre d'élements de X tels que seuils[i] <= x < seuils[i+1] est supérieur ou égal à k
        Le dernier élément de seuils est float("inf")
    """
    count = {}
    for x in X:
        if x in count.keys():
            count[x] += 1
        else:
            count[x] = 1
    cles = list(count.keys())
    cles.sort()
    seuils = []
    n = 0
    for cle in cles:
        n += count[cle]
        if n >= k:
            n = 0
            seuils.append(cle)
    seuils.append(float("inf"))
    return seuils

def discretisation(x, seuils : list):
    """Discrétise une valeur selon des seuils

    Paramètres
    ----------
    x : float
        Une valeur à discrétiser    
    seuils : list
        Seuils de discrétisation

    Sorties
    -------
    i : int
        Indice tel que seuils[i] <= x < seuils[i+1] 
    """
    seuils_copy = seuils.copy()
    seuils_copy.sort(reverse=True)
    for seuil in seuils_copy:
        if x >= seuil:
            return seuil
    return seuils_copy[-1]

def l_diversite(data, attributs, sensible):
    """l-diversité d'un jeu de données selon une liste d'attributs

    Paramètres
    ----------
    data : list[dict]
        Liste d'individus décrits par un dictionnaire
    attributs : list
        Liste des attributs selon lesquels les individus sont comparés
    sensible :
        Attribut sensible sur lequel calculer la diversité

    Sorties
    -------
    l : int
        l-diversité de data selon la liste d'attributs
    """