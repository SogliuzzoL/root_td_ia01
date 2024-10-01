from ia01.utils import lecture_csv
from ia01.kppv import kppv
from ia01.metriques import taux_erreur
from ia01.evaluation import partition_train_val, partition_val_croisee

data = lecture_csv("data/dorade.csv")
data_test = lecture_csv("data/dorade_test.csv")

X = [[float(dorade["longueur"]), float(dorade["poids"])] for dorade in data]
y = [dorade["espece"] for dorade in data]

X_test = [[float(dorade["longueur"]), float(dorade["poids"])] for dorade in data_test]
y_test = [dorade["espece"] for dorade in data_test]

X_train, y_train, X_val, y_val = partition_train_val(X, y)

for k in [1, 3, 5, 7]:
    y_pred = kppv(X, X, y, k)
    print(f"Sur X, k={k} : {taux_erreur(y, y_pred)}")
    y_pred = kppv(X_test, X, y, k)
    print(f"Sur X_test, k={k} : {taux_erreur(y_test, y_pred)}")
print("")

for k in [1, 3, 5, 7]:
    y_pred = kppv(X_val, X_train, y_train, k)
    print(f"Sur X_val, k={k} : {taux_erreur(y_val, y_pred)}")
    y_pred = kppv(X_test, X_train, y_train, k)
    print(f"Sur X_test, k={k} : {taux_erreur(y_test, y_pred)}")
print("")

K = 5
X_K, y_K = partition_val_croisee(X, y)

for j in [1, 3, 5, 7]:
    somme = 0
    for k in range(K):
        X_train_k, y_train_k, X_val_k, y_val_k = [], [], [], []
        for i in range(K):
            if i == k:
                X_val_k, y_val_k = X_K[i], y_K[i]
            else:
                X_train_k.extend(X_K[i])
                y_train_k.extend(y_K[i])
        y_pred = kppv(X_val_k, X_train_k, y_train_k, j)
        somme += taux_erreur(y_val_k, y_pred)
    print(f"Erreur moyenne pour k = {j}: {somme / K}")