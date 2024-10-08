from ia01.utils import lecture_csv, est_complet
from ia01.metriques import valeurs_lim, taux_erreur
from ia01.evaluation import partition_train_val, partition_val_croisee
from ia01.arbre import arbre_train, arbre_pred

# Exercice 1
champs_descr = [
    "annee_construction",
    "surface_habitable",
    "nombre_niveaux",
    "surface_baies_orientees_nord",
    "surface_baies_orientees_est_ouest",
    "surface_baies_orientees_sud",
    "surface_planchers_hauts_deperditifs",
    "surface_planchers_bas_deperditifs",
    "surface_parois_verticales_opaques_deperditives",
    "longitude",
    "latitude",
    "tr001_modele_dpe_type_libelle",
    "tr002_type_batiment_libelle",
]

data = lecture_csv("data/dep_48_filtre.csv")
data_valide = [element for element in data if element["classe_consommation_energie"] != "N" and element["annee_construction"] not in ["0", "1"]]

surface = [float(element["surface_habitable"]) for element in data_valide]
surface_min ,surface_max = valeurs_lim(surface)
data_valide = [element for element in data_valide if float(element["surface_habitable"]) >= surface_min and float(element["surface_habitable"]) <= surface_max]

data_valide = [element for element in data_valide if est_complet(element)]

clé_surface = ["surface_baies_orientees_nord", 
               "surface_baies_orientees_est_ouest",
               "surface_baies_orientees_sud",
               "surface_planchers_hauts_deperditifs",
               "surface_planchers_bas_deperditifs",
               "surface_parois_verticales_opaques_deperditives"]

new_data_valide = []
for element in data_valide:
    valide = False
    for clé in clé_surface:
        if float(element[clé]) != 0.0:
            valide = True
            break
    if valide:
        new_data_valide.append(element)

data_valide = new_data_valide

data_valide = [element for element in data_valide if float(element["consommation_energie"]) != 0.0 or float(element["estimation_ges"]) != 0.0]

# Exercice 2
data = lecture_csv("data/dep_48_clean.csv")

y = []
X = []

modele = ["Copropriete", "Location", "Neuf", "Vente"]
batiment = ["Appartement", "Logements collectifs", "Maison"]

for element in data:
    x = [[0 for i in range(len(modele))], [0 for i in range(len(batiment))]]
    x[0][modele.index(element["tr001_modele_dpe_type_libelle"])] = 1
    x[1][batiment.index(element["tr002_type_batiment_libelle"])] = 1
    x = x[0] + x[1]
    X.append(x)

    if element["classe_consommation_energie"] in ["F", "G"]:
        y.append(1)
    else:
        y.append(0)

X_train, y_train, X_test, y_test = partition_train_val(X, y, 0.25)
K = 5
X_K, y_K = partition_val_croisee(X_train, y_train, K)

for prof in range(1, 5):
    erreur_cv = 0
    for i in range(K):
        X_val, y_val = X_K[i], y_K[i]
        X_train, y_train = [], []
        for j in range(K):
            if j != i:
                X_train += X_K[j]
                y_train += y_K[j]
        arbre = arbre_train(X_train, y_train, max_prof=prof)
        y_pred_val = arbre_pred(X_val, arbre, max_prof=prof)
        erreur_cv += taux_erreur(y_val, y_pred_val)
    erreur_cv /= K    
    
    arbre = arbre_train(X, y, max_prof=prof)
    y_pred_test = arbre_pred(X_test, arbre, max_prof=prof)
    erreur_test = taux_erreur(y_test, y_pred_test)
    print(
        f"Taux d'erreur pour prof={prof} ; VC={erreur_cv:.3f} ; test={erreur_test:.3f}"
    )