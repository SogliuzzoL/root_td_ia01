from ia01.utils import gini, variance, unique
from ia01.majoritaire import vote_majoritaire

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
    X_inf, y_inf, X_sup, y_sup = [], [], [], []

    for i, x in enumerate(X):
        if x[d] > s:
            X_sup.append(X[i])
            y_sup.append(y[i])
        else:
            X_inf.append(X[i])
            y_inf.append(y[i])

    return X_inf, y_inf, X_sup, y_sup

def score_coupe(X, y, d, s, reg=False):
    X_inf, y_inf, X_sup, y_sup = coupe(X, y, d, s)
    score_inf, score_sup = score(y_inf, reg), score(y_sup, reg)
    n_inf, n_sup = len(y_inf), len(y_sup)
    n = n_inf = n_sup
    return (n_inf * score_inf + n_sup * score_sup) / n

def seuil_coupe(X, d):
    """Calcul des seuils auxquels partitionner un ensemble sur la dimension d

    Paramètres
    ----------
    X : list[list]
        Liste de vecteurs à partitionner
    d : int
        Dimension selon laquelle faire la coupe        

    Sorties
    -------
    seuils : list
        Seuils pour faire les coupes
    """
    assert (
        isinstance(d, int) and d >= 0
    ), "Le paramètre `d` doit être un entier positif."

    X_d = unique([x[d] for x in X])
    seuils = [(X_d[i] + X_d[i + 1]) / 2 for i in range(len(X_d) - 1)]

    return seuils

def meilleure_coupe(X, y, reg):
    """Calcul des seuils auxquels partitionner un ensemble sur la dimension d

    Paramètres
    ----------
    X : list[list]
        Liste de vecteurs à partitionner
    y : list
        Liste des prédictions associées à X
    reg : bool
        Indique s'il s'agit d'un problème de régression (True) ou de classification (False)

    Sorties
    -------
    best_dim : int
        Meilleure dimension pour faire la coupe
    best_seuil : float
        Meilleure seuils pour faire la coupe
    X_inf, y_inf, X_sup, y_sup : list
        Partitionnement résultant de la coupe
    """
    best_d, best_s, best_score = 0, 0, float("inf")

    for d in range(len(X[0])):
        seuils = seuil_coupe(X, d)
        for s in seuils:
            current_score = score_coupe(X, y, d, s, reg)
            if current_score < best_score:
                best_d, best_s, best_score = d, s, current_score
    X_inf, y_inf, X_sup, y_sup = coupe(X, y, best_d, best_s)
    return best_d, best_s, X_inf, y_inf, X_sup, y_sup

def arbre_train(X_train, y_train, reg=False, max_prof=float("inf"), profondeur=0):
    """
    Apprentissage d'un arbre de décision

    Paramètres
    ----------
    X_train : list[list]
        Liste des vecteurs de l'ensemble d'apprentissage
    y_train : list
        Liste des prédictions associées aux éléments de X_train
    reg : bool, default = False
        Indique s'il s'agit d'un problème de régression (True) 
        ou de classification (False)
    max_prof : int, default = float("inf")
        Profondeur maximale de l'arbre de décision
    profondeur : int
        Profondeur courante du noeud de l'arbre, paramètre utilisé par récurrence

    Sorties
    -------
    arbre :
        Structure arbre binaire, chaque noeud est un dictionnaire contenant 
        un champ "info" et un champ "coupe".
        Dans le champ "info", il y a l'information de profondeur ("profondeur"), 
        le score associé ("score") et une prédiction si elle est faite 
        au niveau de ce noeud ("prediction").
        Le champ "coupe" est nul ("None") si le noeud est une feuille, sinon il
        contient la dimension ("dimension") et le seuil ("seuil") de la coupe ainsi
        que les deux sous-arbres résultants de la coupe ("arbre_inf" et "arbre_sup").
    """
    arbre = {
        "info": {
            "profondeur": profondeur,
            "score": score(y_train, reg),
            "prediction": vote_majoritaire(y_train, reg),
        },
        "coupe": None,
    }
    if profondeur < max_prof:
        d, s, X_inf, y_inf, X_sup, y_sup = meilleure_coupe(X_train, y_train, reg)
        if X_inf:
            arbre["coupe"] = {
                "dimension": d,
                "seuil": s,
                "arbre_inf": arbre_train(X_inf, y_inf, reg, max_prof, profondeur + 1),
                "arbre_sup": arbre_train(X_sup, y_sup, reg, max_prof, profondeur + 1),
            }
    return arbre


def arbre_pred(X, arbre, max_prof=float("inf")):
    """
    Prédiction à partir d'un arbre de décision

    Paramètres
    ----------
    X : list[list]
        Liste de vecteurs sur lesquels appliquer l'arbre de décision
    arbre : 
        Arbre de décision
    max_prof : int, default = float("inf")
        Profondeur maximale d'exploration de l'arbre de décision

    Sorties
    -------
    y_pred : list
        Liste des prédictions associées aux éléments de X
    """

    def arbre_pred_single(x, arbre, max_prof):
        if arbre["coupe"] is None or arbre["info"]["profondeur"] >= max_prof:
            return arbre["info"]["prediction"]
        else:
            d = arbre["coupe"]["dimension"]
            s = arbre["coupe"]["seuil"]
            if x[d] <= s:
                return arbre_pred_single(x, arbre["coupe"]["arbre_inf"], max_prof)
            else:
                return arbre_pred_single(x, arbre["coupe"]["arbre_sup"], max_prof)

    return [arbre_pred_single(x, arbre, max_prof) for x in X]