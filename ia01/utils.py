def test_utils():
    """Fonction de test"""
    print("Test du module utils du package ia01 !")

def unique(y):
    label = []
    for element in y:
        if element not in label:
            label.append(element)
    return label

def compte(y):
    occurence = {element : 0 for element in unique(y)}
    for element in y:
        occurence[element] += 1
    return occurence

def lecture_csv(fichier, sep=","):
    """Lecture d'un fichier texte sous format CSV.
    La première ligne du fichier donne le nom des champs.

    Paramètres
    ----------
    fichier : string
        Chemin vers le fichier à lire
    sep : char, default = ","
        Caractère pour séparer les champs

    Sorties
    -------
    data : list of dict
        Liste des éléments du fichier CSV.
        Chaque élément est stocké dans un dictionnaire dont les champs
        sont donnés par la première ligne du fichier CSV.
    """
    data = []
    with open(fichier, "r") as f:
        lines = f.read().splitlines()
        keys = lines[0].split(sep)
        for line in lines[1:]:
            values = line.split(sep)
            data.append(dict(zip(keys, values)))
    return data

def moyenne(y):
    return sum(y) / len(y)

def argsort(x, reverse=False):
    """Calcul l'indice de chaque élément dans l'ordre trié.

    Paramètres
    ----------
    x : list
        Liste d'éléments non trié
    reverse : bool
        False (par défaut): tri par ordre croissant
        True : tri par ordre décroissant

    Sorties
    -------
    idx : list
        Liste des indices dans l'ordre
        Si tri croissant, alors x[idx[0]] est le plus petit élément de x
    """
    return sorted(range(len(x)), key=x.__getitem__, reverse=reverse)

def normalisation(X, loc, scale):
    """Méthodes de normalisation de vecteurs

    Paramètres
    ----------
    X : list[list]
        Liste de vecteurs sur lesquels appliquer la normalisation
    loc, scale : list
        Liste de paramètres de normalisation pour chaque dimension
        Pour un vecteur x de la liste X, la normalisation pour chaque dimension est :
        x[j] = (x[j] - loc[j]) / scale[j]

    Sorties
    -------
    Xnorm : list[list]
        Liste des vecteurs normalisés
    """
    X_norm = []

    for x in X:
        x_norm = []
        for j in range(len(x)):
            x_norm.append((x[j] - loc[j]) / scale[j])
        X_norm.append(x_norm)

    return X_norm

def norm_param(X, methode="echelle"):
    """Calcul des paramètres de normalisation

    Paramètres
    ----------
    X : list[list]
        Liste de vecteurs à partir desquels calculer les paramètres de normalisation
    methode : str, default = "echelle"
        Méthode de normalisation utilisée : "echelle" ou "centre"

    Sorties
    -------
    loc, scale : list
        Liste de paramètres de normalisation pour chaque dimension
    """

    assert (
        methode == "echelle" or methode == "centre"
    ), "Le paramètre `methode` doit valoir `echelle` ou `centre`."

    loc = []
    scale = []

    for i in range(len(X[0])):
        L = [x[i] for x in X]
        if methode == "echelle":
            loc.append(min(L))
            scale.append(max(L) - min(L))
        else:
            loc.append(moyenne(L))
            scale.append(ecart_type(L))
    
    return loc, scale

def moyenne(X):
    n = len(X)
    somme = 0
    for x in X:
        somme += x
    return somme / n


def ecart_type(X):
    n = len(X)
    moy = moyenne(X)
    sigma = 0

    for x in X:
        sigma += (x - moy) ** 2

    return (sigma / n) ** (1 / 2)

def variance(X):
    return ecart_type(X) ** 2
