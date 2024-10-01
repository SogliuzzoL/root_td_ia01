def partition_train_val(X, y, r=1/5):
    """Partitionne un ensemble X, y en un ensemble train et val.

    Paramètres
    ----------
    X : list[list]
        Liste de vecteurs à partitionner
    y : list
        Liste des prédictions associées à X
    r : float [0, 1], default = 1/5
        Ratio de (X, y) à mettre dans l'ensemble de validation
        On choisit r tel que r = 1/K avec K un entier
        L'ensemble de validation X_val, y_val contient tous les éléments de X, y
        dont l'indice modulo K est égal à zéro, les autres éléments sont dans 
        l'ensemble X_train, y_train.
        X_val, y_val contiennent les éléments 0, K, 2K, 3K, etc.

    Sorties
    -------
    X_train, y_train :
        Ensemble d'apprentissage
    X_val, y_val :
        Ensemble de validation
    """

    K = round(1/r)
    X_val, y_val, X_train, y_train = [], [], [], []
    for i in range(len(X)):
        if i % K:
            X_train.append(X[i])
            y_train.append(y[i])
        else:
            X_val.append(X[i])
            y_val.append(y[i])
    
    return X_train, y_train, X_val, y_val

def partition_val_croisee(X, y, K=5):
    """Partitionne un ensemble X, y en K sous-ensemble.

    Paramètres
    ----------
    X : list[list]
        Liste de vecteurs à partitionner
    y : list
        Liste des prédictions associées à X
    K : int, default = 5
        Nombre de partitions

    Sorties
    -------
    X_K, y_K :
        Liste comprenant les K sous-ensembles de X et y
        X_K[k], y_val[k] contiennent tous les éléments de X, y
        dont l'indice modulo K est égal à k.
    """
    X_K, y_K = [[] for k in range(K)], [[] for k in range(K)]
    for i in range(len(X)):
        X_K[i % K].append(X[i])
        y_K[i % K].append(y[i])
    return X_K, y_K