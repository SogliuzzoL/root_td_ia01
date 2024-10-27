from ia01.utils import lecture_csv, moyenne
from ia01.arbre import arbre_pred, arbre_train
from ia01.metriques import eqm, taux_erreur
from ia01.evaluation import partition_val_croisee
from ia01.privacy import discret_seuils, discretisation

reg_train = lecture_csv("data_examen/reg_train.csv")
reg_test = lecture_csv("data_examen/reg_train.csv")

X_train = [[float(element[key]) for key in element.keys() if key != "y"] for element in reg_train]
y_train = [float(element["y"]) for element in reg_train]
X_test = [[float(element[key]) for key in element.keys() if key != "y"] for element in reg_test]
y_test = [float(element["y"]) for element in reg_test]

meilleur_prof, meilleur_eqm = 0, float("inf")
K = 5
X_k, y_k = partition_val_croisee(X_train, y_train, K)

for p in range(21):
    current_eqm = 0
    for k in range(K):
        X_i, y_i = [], []
        for i in range(K):
            if i != k:
                X_i.extend(X_k[i])
                y_i.extend(y_k[i])
        arbre = arbre_train(X_i, y_i, reg=True, max_prof=p)
        y_k_pred = arbre_pred(X_k[k], arbre, max_prof=p)
        current_eqm += eqm(y_k[k], y_k_pred)
    current_eqm /= K
    if current_eqm < meilleur_eqm:
        meilleur_eqm = current_eqm
        meilleur_prof = p

arbre = arbre_train(X_train, y_train, reg=True, max_prof=meilleur_prof)
y_pred = arbre_pred(X_test, arbre, max_prof=meilleur_prof)
print(meilleur_prof, round(eqm(y_test, y_pred), 3))

seuils = discret_seuils(y_train, len(y_train) // 3)
print(seuils)
y_train_class = [discretisation(y, seuils) for y in y_train]
y_test_class = [discretisation(y, seuils) for y in y_test]

arbre = arbre_train(X_train, y_train_class, max_prof=5)
y_pred_class = arbre_pred(X_test, arbre, max_prof=5)
print(round(taux_erreur(y_test_class, y_pred_class), 3))

def fonction_cout(y_true: list, y_pred: list):
    cout = []
    for true, pred in zip(y_true, y_pred):
        cout.append(abs(true - pred))
    return moyenne(cout)
print(round(fonction_cout(y_test_class, y_pred_class), 3))

meilleur_prof, meilleur_cout = 0, float("inf")
K = 5
X_k, y_k = partition_val_croisee(X_train, y_test_class, K)

for p in range(21):
    current_cout = 0
    for k in range(K):
        X_i, y_i = [], []
        for i in range(K):
            if i != k:
                X_i.extend(X_k[i])
                y_i.extend(y_k[i])
        arbre = arbre_train(X_i, y_i, reg=True, max_prof=p)
        y_k_pred = arbre_pred(X_k[k], arbre, max_prof=p)
        current_cout += fonction_cout(y_k[k], y_k_pred)
    current_cout /= K
    if current_cout < meilleur_cout:
        meilleur_cout = current_cout
        meilleur_prof = p

arbre = arbre_train(X_train, y_train_class, reg=False, max_prof=meilleur_prof)
y_pred = arbre_pred(X_test, arbre, max_prof=meilleur_prof)
print(meilleur_prof, round(fonction_cout(y_test_class, y_pred), 3))