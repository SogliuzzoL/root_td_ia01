from ia01.utils import lecture_csv
from ia01.metriques import TPR, FPR, ROC, f_score, rappel, precision
from matplotlib import pyplot as plt

# Ex 1.1
datas = lecture_csv("data/compas.csv")
data = [element for element in datas if element["race"] in ["Caucasian", "African-American"]]

# Ex 1.2
X = []
G = []
y_true = []
for element in data:
    X.append(int(element["decile_score"]))
    y_true.append(int(element["two_year_recid"]))
    if element["race"] == "Caucasian":
        G.append(1)
    else:
        G.append(2)

y_pred = [int(x >= 8) for x in X]

# Ex 1.3
p1 = 0
p2 = 0
n1 = 0
n2 = 0
for y, g in zip(y_pred, G):
    if g == 1:
        n1 += 1
    else:
        n2 += 1
    if y == 1:
        if g == 1:
            p1 += 1
        else:
            p2 += 1

print(f"Proba Récidiviste Caucasian : {round(p1 / n1, 2)}\nProba Récidiviste African-American : {round(p2 / n2, 2)}")

# La règle n'est pas équitable au sens de l'égalité des chances

# Ex 1.4
y_pred1, y_pred2 = [], []
y_true1, y_true2 = [], []
s_pred1, s_pred2 = [], []
for yp, yt, g, s in zip(y_pred, y_true, G, X):
    if g == 1:
        y_pred1.append(yp)
        y_true1.append(yt)
        s_pred1.append(s)
    else:
        y_pred2.append(yp)
        y_true2.append(yt)
        s_pred2.append(s)

print(f"\nTPR Caucasian : {round(TPR(y_true1, y_pred1, 1), 2)}, FPR Caucasian : {round(FPR(y_true1, y_pred1, 1), 2)}")
print(f"TPR African-American : {round(TPR(y_true2, y_pred2, 1), 2)}, FPR African-American : {round(FPR(y_true2, y_pred2, 1), 2)}\n")

# Ex 1.6
seuils = [i for i in range(1, 12)]
ROC1 = ROC(y_true1, s_pred1, 1, seuils)
ROC2 = ROC(y_true2, s_pred2, 1, seuils)

plt.plot(seuils, ROC1[0], label="Caucasian - TPR")
plt.plot(seuils, ROC2[0], label="African-American - TPR")
plt.plot(seuils, ROC1[1], label="Caucasian - FPR")
plt.plot(seuils, ROC2[1], label="African-American - FPR")
plt.legend()


# Ex 1.7
for beta in [1, 3, 1/3]:
    alpha = 0.05
    F1_max, t1_max, t2_max, rappel_max, précision_max = 0, 0, 0, 0, 0
    for i, t1 in enumerate(seuils):
        for j, t2 in enumerate(seuils):
            if abs(ROC1[0][i] - ROC2[0][j]) <= alpha and abs(ROC1[1][i] - ROC2[1][j]) <= alpha:
                y_pred = []
                for x, g in zip(X, G):
                    if g == 1:
                        y_pred.append(int(x >= t1))
                    else:
                        y_pred.append(int(x >= t2))
                F1 = f_score(y_true, y_pred, 1, beta)
                if F1 > F1_max:
                    F1_max = F1
                    t1_max = t1
                    t2_max = t2
                    rappel_max = rappel(y_true, y_pred, 1)
                    précision_max = precision(y_true, y_pred, 1)
    print(f"Pour beta = {round(beta, 2)}, Meilleur F1 = {round(F1_max, 2)} pour t1 = {t1_max} et t2 = {t2_max}, rappel = {round(rappel_max, 2)}, précision = {round(précision_max, 2)}")

plt.show()
