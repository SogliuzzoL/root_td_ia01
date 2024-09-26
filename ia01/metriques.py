import math

def taux_erreur(y_true, y_pred):
    """Taux d'erreur pour un problème de classification

    Paramètres
    ----------
    y_true : list
        Liste contenant les vraies valeurs
    y_pred : list
        Liste contenant les valeurs prédites par un classifieur

    Sorties
    -------
    err : float [0,1]
        Ratio (entre 0 et 1) d'éléments où y_true et y_pred sont différents.
    """
    sum = 0
    n = len(y_pred)
    for i in range(n):
        if y_true[i] != y_pred[i]:
            sum += 1
    return sum / n

def eqm(y_true, y_pred):
    """Erreur quadratique moyenne pour un problème de regression

    Paramètres
    ----------
    y_true : list
        Liste contenant les vraies valeurs
    y_pred : list
        Liste contenant les valeurs prédites

    Sorties
    -------
    e : float
        Erreur quadratique moyenne
    """
    sum = 0
    n = len(y_true)
    for i in range(n):
        sum += (y_true[i] - y_pred[i]) ** 2
    return sum / n

def reqm(y_true, y_pred):
    return math.sqrt(eqm(y_true, y_pred))