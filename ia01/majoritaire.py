from ia01.utils import unique, compte, moyenne


def vote_majoritaire(y, reg=False):
    if reg:
        return moyenne(y)
    else:
        label = unique(y)
        nombre = compte(y)
        return label[nombre.index(max(nombre))]