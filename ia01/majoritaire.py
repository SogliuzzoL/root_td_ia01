from ia01.utils import compte, moyenne

def vote_majoritaire(y, reg=False):
    """Applique le vote majoritaire à la liste y.

    Paramètres
    ----------
    y : list
        Liste des labels pour l'ensemble des données
    reg : bool, default = False
        Indique s'il s'agit d'un problème de régression (True) ou de classification (False)
        Par défaut, on considère qu'il s'agit d'un problème de classification (reg=False)

    Sorties
    -------
    label
        Classification : label le plus représenté dans la liste y
        Regression : moyenne empirique des éléments de y
    """
    if reg:
        # Problème de régression
        return moyenne(y)
    else:
        # Problème de classification
        comptage = compte(y)
        majoritaire = (0, 0)
        for key in comptage.keys():
            if comptage[key] > majoritaire[1]:
                majoritaire = (key, comptage[key])
        return majoritaire[0]
