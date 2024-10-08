from ia01.utils import moyenne

def taux_erreur(y_true, y_pred):
    return len([yt for yt, yp in zip(y_true, y_pred) if yt != yp]) / len(y_true)

def eqm(y_true, y_pred):
    return moyenne([(yt - yp) ** 2 for yt, yp in zip(y_true, y_pred)])

def reqm(y_true, y_pred):
    return eqm(y_true, y_pred) ** 0.5

def repartition(x, X):
    somme = 0
    n = len(X)
    for element in X:
        if element <= x:
            somme += 1
    return somme / n

def quantile(X, alpha):
    X_sort = X.copy()
    X_sort.sort()
    n = len(X)
    return X_sort[min(int(alpha * n), n - 1)]

def valeurs_lim(X):
    Q1 = quantile(X, 0.25)
    Q3 = quantile(X, 0.75)
    IQR = Q3 - Q1
    v_min, v_max = Q1, Q3
    for x in X:
        if x < v_min and x >= Q1 - 1.5 * IQR:
            v_min = x
        elif x > v_max and x <= Q3 + 1.5 * IQR:
            v_max = x
    return v_min, v_max