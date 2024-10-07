from ia01.utils import moyenne

def taux_erreur(y_true, y_pred):
    return len([yt for yt, yp in zip(y_true, y_pred) if yt != yp]) / len(y_true)

def eqm(y_true, y_pred):
    return moyenne([(yt - yp) ** 2 for yt, yp in zip(y_true, y_pred)])

def reqm(y_true, y_pred):
    return eqm(y_true, y_pred) ** 0.5