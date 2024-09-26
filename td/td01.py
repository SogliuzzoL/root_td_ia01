from ia01.utils import unique, compte, lecture_csv
from ia01.majoritaire import vote_majoritaire
from ia01.metriques import taux_erreur, eqm, reqm

data = lecture_csv("C:\\Users\\sogli\\Documents\\IA\\root_td_ia01\\data\\dorade.csv")
espece = []
poids = []

for element in data:
    espece.append(element['espece'])
    poids.append(float(element['poids']))

# Problème de classification
espece_pred = vote_majoritaire(espece)
espece_err = taux_erreur(espece, [espece_pred for _ in range(len(espece))])
print(f"Le taux d'erreur du vote majoritaire des espèces de dorade est de {espece_err * 100}%")

# Problème de régression
poids_pred = vote_majoritaire(poids, True)
poids_err_eqm = eqm(poids, [poids_pred for _ in range(len(poids))])
poids_err_reqm = reqm(poids, [poids_pred for _ in range(len(poids))])
print(f"L'eqm du vote majoritaire des poids de dorade est de {poids_err_eqm}")
print(f"La reqm du vote majoritaire des poids de dorade est de {poids_err_reqm} grammes")

# Régression par classification
poids_class = []
for element in poids:
    if element <= 500:
        poids_class.append(250)
    elif element <= 1000:
        poids_class.append(750)
    elif element <= 1500:
        poids_class.append(1250)
    elif element <= 2000:
        poids_class.append(1750)

poids_class_pred = vote_majoritaire(poids_class)
poids_class_err = taux_erreur(poids_class, [poids_class_pred for _ in range(len(poids_class))])
print(f"Le taux d'erreur du vote majoritaire des poids de dorade est de {poids_class_err * 100}%")
