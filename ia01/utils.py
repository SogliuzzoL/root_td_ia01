def test_utils():
    """Fonction de test"""
    print("Test du module utils du package ia01 !")

def unique(y):
    return list(set(y))

def compte(y):
    return [y.count(li) for li in unique(y)]

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
    return [[(xij - l) / s for xij, l, s in zip(xi, loc, scale)] for xi in X]

def norm_param(X, methode="echelle"):
    assert (
        methode == "echelle" or methode == "centre"
    ), "Le paramètre `methode` doit valoir `echelle` ou `centre`."

    d = len(X[0])
    if methode == "echelle":
        loc = [min([xi[j] for xi in X]) for j in range(d)]
        scale = [max([xi[j] for xi in X]) - min([xi[j] for xi in X]) for j in range(d)]
    else:
        loc = [moyenne([xi[j] for xi in X]) for j in range(d)]
        scale = [ecart_type([xi[j] for xi in X]) for j in range(d)]

    return loc, scale

def variance(x):
    x_moy = moyenne(x)
    return moyenne([(xi - x_moy) ** 2 for xi in x])

def ecart_type(x):
    return variance(x) ** 0.5

def gini(y):
    c = compte(y)
    n = sum(c)
    return 1 - sum([(ci/n) ** 2 for ci in c])
