from ia01.utils import lecture_csv, est_complet
from ia01.metriques import valeurs_lim, taux_erreur
from ia01.kppv import kppv

class_test = lecture_csv("data_examen/class_test.csv")
X_test = [[float(x["x1"]), float(x["x2"])] for x in class_test]
y_test = [int(y["y"]) for y in class_test]

class_train = lecture_csv("data_examen/class_train.csv")
print(len(class_train))
class_train_complet = class_train.copy()

class_train = [element for element in class_train if est_complet(element)]
print(len(class_train))

x2 = [float(element["x2"]) for element in class_train]
x2_min, x2_max = valeurs_lim(x2)
print(x2_min, x2_max)

new_class_train = []
for element in class_train:
    if float(element["x2"]) <= x2_max and float(element["x2"]) >= x2_min:
        new_class_train.append(element)
print(len(class_train) - len(new_class_train))
class_train = new_class_train

X_train = [[float(element["x1"]), float(element["x2"])]for element in class_train]
y_train = [int(element["y"]) for element in class_train]

y_pred = kppv(X_test, X_train, y_train, k=7, p=1)
print(round(taux_erreur(y_test, y_pred), 3))

# Q16
class_train_manquant = [element for element in class_train_complet if not est_complet(element)]

class_train_abberant = []
for element in [element for element in class_train_complet if est_complet(element)]:
    if not(float(element["x2"]) <= x2_max and float(element["x2"]) >= x2_min):
        class_train_abberant.append(element)

X_train = [[float(element["x1"]), int(element["y"])]for element in class_train]
y_train = [float(element["x2"]) for element in class_train]

X_pred_manquant = [[float(element["x1"]), int(element["y"])]for element in class_train_manquant]
y_pred_manquant = kppv(X_pred_manquant, X_train, y_train, k=7, reg=True)

X_pred_abberant = [[float(element["x1"]), int(element["y"])]for element in class_train_abberant]
y_pred_abberant = kppv(X_pred_abberant, X_train, y_train, k=7, reg=True)

X = y_train + y_pred_abberant + y_pred_manquant
X = [[x1[0], x2] for x1, x2 in zip(X_train + X_pred_abberant + X_pred_manquant, X)]
y = [element[1] for element in X_train + X_pred_abberant + X_pred_manquant]
y_pred = kppv(X_test, X, y, k=7, p=1)
print(round(taux_erreur(y_test, y_pred), 3))