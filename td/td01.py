from ia01.utils import lecture_csv
from ia01.metriques import taux_erreur, eqm, reqm
from ia01.majoritaire import vote_majoritaire

data = lecture_csv("data/dorade.csv")

# Exercice 1
y_true = [d["espece"] for d in data]
y_pred = [vote_majoritaire(y_true)] * len(y_true)

print(taux_erreur(y_true, y_pred))

# Exercice 2
y_true = [float(d["poids"]) for d in data]
y_pred = [vote_majoritaire(y_true, reg=True)] * len(y_true)

print(eqm(y_true, y_pred))

# Exercice 3
y_true = [float(d["poids"]) for d in data]
y_pred = [vote_majoritaire(y_true, reg=True)] * len(y_true)

print(reqm(y_true, y_pred))