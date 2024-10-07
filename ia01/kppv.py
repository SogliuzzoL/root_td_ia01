from ia01.utils import argsort
from ia01.majoritaire import vote_majoritaire

def kppv(X, X_train, y_train, k, p=2, reg=False):
    assert isinstance(k, int) and k > 0, "k doit être un entier strictement positif"

    y_pred = []
    for xi in X:
        dist = distance(xi, X_train, p)
        idx = argsort(dist)
        y_pred.append(vote_majoritaire([y_train[idx[j]] for j in range(k)], reg))
    return y_pred

def distance2(x1, x2, p=2):
    assert len(x1) == len(x2), "Les vecteurs x1 et x2 doivent être de même dimension."
    assert p > 0, "Le paramètre p doit être strictement supérieur à 0."

    if p < float("inf"):
        return sum([abs(x1i - x2i) ** p for x1i, x2i in zip(x1, x2)]) ** (1/p)
    else:
        return max([abs(x1i - x2i) for x1i, x2i in zip(x1, x2)])

def distance(x, X_train, p=2):
    return [distance2(x, xi, p) for xi in X_train]
