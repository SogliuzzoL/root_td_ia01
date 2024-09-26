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
