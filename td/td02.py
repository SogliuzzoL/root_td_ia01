from ia01.kppv import kppv
from ia01.utils import lecture_csv, norm_param, normalisation
from ia01.metriques import taux_erreur, reqm

# Exercice 1
dorades = lecture_csv("data/dorade.csv")
X = [(float(dorade["longueur"]), float(dorade["poids"])) for dorade in dorades]

X_parm = norm_param(X, "centre")
X_norm = normalisation(X, X_parm[0], X_parm[1])

X_parm2 = norm_param(X)
X_norm2 = normalisation(X, X_parm2[0], X_parm2[1])

Y = [dorade["espece"] for dorade in dorades]

for k in range(3, 10, 2):
    y_pred = kppv(X, X, Y, k)
    err = taux_erreur(Y, y_pred)
    y_pred1 = kppv(X_norm, X_norm, Y, k)
    err1 = taux_erreur(Y, y_pred1)
    y_pred2 = kppv(X_norm2, X_norm2, Y, k)
    err2 = taux_erreur(Y, y_pred2)
    print(f"Taux d'erreur pour k={k} : sans normalisation {err}, normalisation centrée {err1}, normalisation echelonée {err2}")

X_train = [[float(dorade["longueur"]), int(dorade["espece"] == "grise"), int(dorade["espece"] == "marbree")] for dorade in dorades]
Y_train = [float(dorade["poids"]) for dorade in dorades]

for k in range(3, 10, 2):
    Y_pred = kppv(X_train, X_train, Y_train, k, reg=True)
    print(f"REQM pour k={k}: {reqm(Y_train, Y_pred)}")

# Exercice 2

