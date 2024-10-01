from ia01.utils import lecture_csv, norm_param, normalisation
from ia01.metriques import taux_erreur
from ia01.kppv import kppv

data = lecture_csv("data/dorade.csv")
n = len(data)

X_train, y_train = [], []
for i in range(n):
    X_train.append([float(data[i]["longueur"]), float(data[i]["poids"])])
    y_train.append(data[i]["espece"])

for k in [3, 5, 7]:
    y_pred = kppv(X_train, X_train, y_train, k)
    print("Taux d'erreur pour k =", k, ":", taux_erreur(y_train, y_pred))

for k in [1, 200]:
    y_pred = kppv(X_train, X_train, y_train, k)
    print("Taux d'erreurs pour k =", k, ":", taux_erreur(y_train, y_pred))

loc1, scale1 = norm_param(X_train, "echelle")
loc2, scale2 = norm_param(X_train, "centre")

X_norm1 = normalisation(X_train, loc1, scale1)
X_norm2 = normalisation(X_train, loc2, scale2)

for k in [3, 5, 7]:
    y_pred = kppv(X_train, X_train, y_train, k)
    y_norm1 = kppv(X_norm1, X_norm1, y_train, k)
    y_norm2 = kppv(X_norm2, X_norm2, y_train, k)
    print(
        "k =",
        k,
        ", sans norme :",
        taux_erreur(y_train, y_pred),
        ", norme 1 :",
        taux_erreur(y_train, y_norm1),
        ", norme 2 :",
        taux_erreur(y_train, y_norm2),
    )
