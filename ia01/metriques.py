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

def precision(y_true, y_pred, label_pos):
    VP = 0
    FP = 0
    for i, y in enumerate(y_pred):
        if y == label_pos and y == y_true[i]:
            VP += 1
        elif y == label_pos and y != y_true[i]:
            FP += 1
    if VP + FP == 0:
        return 0
    return VP / (VP + FP)
def rappel(y_true, y_pred, label_pos):
    VP = 0
    FN = 0
    for i, y in enumerate(y_pred):
        if y == label_pos and y == y_true[i]:
            VP += 1
        elif y != label_pos and y == y_true[i]:
            FN += 1
    if VP + FN == 0:
        return 0
    return VP / (VP + FN)

def f_score(y_true, y_pred, label_pos, beta=1):
    prec = precision(y_true, y_pred, label_pos)
    rap = rappel(y_true, y_pred, label_pos)
    if prec == 0 or rap == 0:
        return 0
    return (1 + beta**2) * (prec * rap) / (beta ** 2 * prec + rap)