from ia01.utils import gini, moyenne, variance

def score(y, reg):
    return variance(y) if reg else gini(y)

def coupe(X, y, d, s):
    """Partitionnement d'un ensemble sur le dimension d par rapport à un seuil s

    Paramètres
    ----------
    X : list[list]
        Liste de vecteurs à partitionner
    y : list
        Liste des prédictions associées à X
    d : int
        Dimension selon laquelle faire la coupe
    s : float
        Seuil pour faire la coupe

    Sorties
    -------
    X_inf, y_inf, X_sup, y_sup :
        X_inf, y_inf : partie des éléments tels que x[d] <= s
        X_sup, y_sup : partie des éléments tels que x[d] > s
    """
    assert (
        isinstance(d, int) and d >= 0
    ), "Le paramètre `d` doit être un entier positif."

    pass  # À compléter