from ia01.utils import lecture_csv
from ia01.metriques import taux_erreur, reqm
from ia01.kppv import kppv
from ia01.evaluation import partition_train_val, partition_val_croisee
from ia01.arbre import arbre_train, arbre_pred

data = lecture_csv("data/dorade.csv")
X_train = [[float(d["longueur"]), float(d["poids"])] for d in data]
y_train = [d["espece"] for d in data]

test = lecture_csv("data/dorade_test.csv")
X_test = [[float(d["longueur"]), float(d["poids"])] for d in test]
y_test = [d["espece"] for d in test]

for k in range(1,8,2):
    y_pred_train = kppv(X_train, X_train, y_train, k)
    y_pred_test = kppv(X_test, X_train, y_train, k)
    err_train = taux_erreur(y_train, y_pred_train)
    err_test = taux_erreur(y_test, y_pred_test)
    print(f"Taux d'erreur pour k={k} : train={err_train}, test={err_test}")

data = lecture_csv("data/dorade.csv")
X = [[float(d["longueur"]), float(d["poids"])] for d in data]
y = [d["espece"] for d in data]

for r in [1 / 5, 1 / 4, 1 / 3, 1 / 2]:
    X_train, y_train, X_val, y_val = partition_train_val(X, y, r)
    print(f"Ratio train/val : {r:.2f}")
    for k in [1, 3, 5, 7]:
        y_pred_val = kppv(X_val, X_train, y_train, k)
        y_pred_test = kppv(X_test, X_train, y_train, k)
        print(
            f"Taux d'erreur pour k={k} ; val={taux_erreur(y_val, y_pred_val):.3f} ; test={taux_erreur(y_test, y_pred_test):.3f}"
        )

# KPPV
X = [[float(d["longueur"]), float(d["poids"])] for d in data]
y = [d["espece"] for d in data]

test = lecture_csv("data/dorade_test.csv")
X_test = [[float(d["longueur"]), float(d["poids"])] for d in test]
y_test = [d["espece"] for d in test]

K = 5
X_K, y_K = partition_val_croisee(X, y, K)

for k in [1, 3, 5, 7]:
    erreur_cv = 0
    for i in range(K):
        X_val = X_K[i]
        y_val = y_K[i]
        X_train, y_train = [], []
        for j in range(K):
            if j != i:
                X_train += X_K[j]
                y_train += y_K[j]
        erreur_cv += taux_erreur(y_val, kppv(X_val, X_train, y_train, k))
    erreur_cv /= K    
    
    y_pred_test = kppv(X_test, X, y, k)
    erreur_test = taux_erreur(y_test, y_pred_test)
    print(
        f"Taux d'erreur pour k={k} ; VC={erreur_cv:.3f} ; test={erreur_test:.3f}"
    )

# Arbre de décision
X = [[float(d["longueur"]), float(d["poids"])] for d in data]
y = [d["espece"] for d in data]

test = lecture_csv("data/dorade_test.csv")
X_test = [[float(d["longueur"]), float(d["poids"])] for d in test]
y_test = [d["espece"] for d in test]

K = 5
X_K, y_K = partition_val_croisee(X, y, K)

for prof in [3, 5, 7, float("inf")]:
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

# KPPV reg
X = [[float(d["longueur"])] for d in data]
y = [float(d["poids"]) for d in data]

test = lecture_csv("data/dorade_test.csv")
X_test = [[float(d["longueur"])] for d in test]
y_test = [float(d["poids"]) for d in test]

K = 5
X_K, y_K = partition_val_croisee(X, y, K)

for k in [1, 3, 5, 7]:
    erreur_cv = 0
    for i in range(K):
        X_val, y_val = X_K[i], y_K[i]
        X_train, y_train = [], []
        for j in range(K):
            if j != i:
                X_train += X_K[j]
                y_train += y_K[j]
        erreur_cv += reqm(y_val, kppv(X_val, X_train, y_train, k, reg=True))
    erreur_cv /= K    
    
    y_pred_test = kppv(X_test, X, y, k, reg=True)
    erreur_test = reqm(y_test, y_pred_test)
    print(
        f"REQM pour k={k} ; VC={erreur_cv:.3f} ; test={erreur_test:.3f}"
    )

# Arbre reg
X = [[float(d["longueur"])] for d in data]
y = [float(d["poids"]) for d in data]

test = lecture_csv("data/dorade_test.csv")
X_test = [[float(d["longueur"])] for d in test]
y_test = [float(d["poids"]) for d in test]

K = 5
X_K, y_K = partition_val_croisee(X, y, K)

for prof in [3, 5, 7, float("inf")]:
    erreur_cv = 0
    for i in range(K):
        X_val = X_K[i]
        y_val = y_K[i]
        X_train, y_train = [], []
        for j in range(K):
            if j != i:
                X_train += X_K[j]
                y_train += y_K[j]
        arbre = arbre_train(X_train, y_train, max_prof=prof, reg=True)
        y_pred_val = arbre_pred(X_val, arbre, max_prof=prof)
        erreur_cv += reqm(y_val, y_pred_val)
    erreur_cv /= K
    
    arbre = arbre_train(X, y, max_prof=prof, reg=True)
    y_pred_test = arbre_pred(X_test, arbre, max_prof=prof)
    erreur_test = reqm(y_test, y_pred_test)
    print(
        f"REQM pour prof={prof} ; VC={erreur_cv:.3f} ; test={erreur_test:.3f}"
    )