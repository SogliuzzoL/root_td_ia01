from ia01.utils import argsort
from ia01.majoritaire import vote_majoritaire

def kppv(X, X_train, y_train, k, p=2, reg=False):
    """Méthode des k plus proches voisins

    Paramètres
    ----------
    X : list[list]
        Liste de vecteurs sur lesquels appliquer la méthode des k-ppv
    X_train : list[list]
        Liste des vecteurs de l'ensemble d'apprentissage
    y_train : list
        Liste des prédictions associées aux éléments de X_train
    k : int
        Nombre de voisins
    p : float, default = 2
        Paramètre de la distance de Minkowski
        p > 0, pour la distance de Tchebychev p = float('inf')
    reg : bool, default = False
        Indique s'il s'agit d'un problème de régression (True) ou de classification (False)

    Sorties
    -------
    y_pred : list
        Liste des prédictions associées aux éléments de X
    """

    assert isinstance(k, int) and k > 0, "k doit être un entier strictement positif"

    y_pred = []

    for x in X:
        d = distance(x, X_train, p)
        ordre = argsort(d)
        ppv = [y_train[ordre[i]] for i in range(k)]
        y_pred.append(vote_majoritaire(ppv, reg))
    return y_pred
        


def distance2(x1, x2, p=2):
    """Calcule la distance de Minkowski de paramètre p entre les vecteurs x1 et x2

    Paramètres
    ----------
    x1, x2 : list
        Vecteurs de dimension d
    p : float, default = 2
        Paramètre de la distance de Minkowski
        p > 0, pour la distance de Tchebychev p = float('inf')

    Sorties
    -------
    dist : float
        Distance entre x1 et x2
    """
    assert len(x1) == len(x2), "Les vecteurs x1 et x2 doivent être de même dimension."
    assert p > 0, "Le paramètre p doit être strictement supérieur à 0."
    
    n = len(x1)

    if p < float("inf"):
        somme = 0
        for i in range(n):
            somme += abs(x1[i] - x2[i]) ** p
        return somme ** (1 / p)
    else:
        X = [abs(x1[i] - x2[i]) for i in range(n)]
        return max(X)

def distance(x, X_train, p=2):
    """Calcule la distance de Minkowski de paramètre p entre le vecteur x
       et tous les éléments de X_train.

    Paramètres
    ----------
    X_train : list[list]
        Liste de vecteurs de dimension d
    x : list
        Vecteur de dimension d
    p : float, default = 2
        Paramètre de la distance de Minkowski
        p > 0, pour la distance de Tchebychev p = float('inf')

    Sorties
    -------
    dist : list
        Distances entre x et tous les éléments de X_train
    """
    return [distance2(x, X, p) for X in X_train]