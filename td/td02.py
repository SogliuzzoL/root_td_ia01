from ia01.kppv import kppv
from ia01.utils import lecture_csv, norm_param, normalisation
from ia01.metriques import taux_erreur

dorades = lecture_csv("data/dorade.csv")
X = [(float(dorade["longueur"]), float(dorade["poids"])) for dorade in dorades]
X_parm = norm_param(X, "centre")
X_norm = normalisation(X, X_parm[0], X_parm[1])
Y = [dorade["espece"] for dorade in dorades]

for k in range(1, 201):
    y_pred = kppv(X, X, Y, k)
    err = taux_erreur(Y, y_pred)
    y_pred_norm = kppv(X_norm, X_norm, Y, k)
    err_norm = taux_erreur(Y, y_pred_norm)
    print(f"Le taux d'erreur pour k={k} est de {err} et de {err_norm} avec normalisation")