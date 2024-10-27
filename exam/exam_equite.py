from ia01.utils import lecture_csv, moyenne
from ia01.metriques import FPR, TPR, f_score

dorades = lecture_csv("data_examen/dorade_examen.csv")

bob = [float(dorade["bob"]) for dorade in dorades]
bob_marbree = [float(dorade["bob"]) for dorade in dorades if dorade["espece"] == "marbree"]
bob_grise = [float(dorade["bob"]) for dorade in dorades if dorade["espece"] != "marbree"]

IMC_marbree = [float(dorade["poids"]) / 1000 / pow(float(dorade["longueur"]) / 100, 2) for dorade in dorades if dorade["espece"] == "marbree"]
IMC_grise = [float(dorade["poids"]) / 1000 / pow(float(dorade["longueur"]) / 100, 2) for dorade in dorades if dorade["espece"] != "marbree"]
IMC = [float(dorade["poids"]) / 1000 / pow(float(dorade["longueur"]) / 100, 2) for dorade in dorades]
print(round(moyenne(IMC_marbree), 3))
print(round(moyenne(IMC_grise), 3))

C_marbree = [abs(imc - 4.8) for imc in IMC_marbree]
C_grise = [abs(imc - 4.8) for imc in IMC_grise]
C = [abs(imc - 4.8) for imc in IMC]

t = 0.5
y_marbree = [int(C <= t) for C in C_marbree]
y_grise = [int(C <= t) for C in C_grise]
y = [int(C <= t) for C in C]

p_marbree = len([1 for y in y_marbree if y == 1]) / len(y_marbree)
p_grise = len([1 for y in y_grise if y == 1]) / len(y_grise)

print(round(abs(p_marbree - p_grise) * 100, 3))

print(round(abs(TPR(bob_marbree, y_marbree, 1) - TPR(bob_grise, y_grise, 1)) * 100, 3))
print(round(abs(FPR(bob_marbree, y_marbree, 1) - FPR(bob_grise, y_grise, 1)) * 100 , 3))

meilleurf, meilleur1, meilleur2 = 0, 0, 0
for seuil1 in [i * 2 / 1000 for i in range(1000)]:
    for seuil2 in [i * 2 / 1000 for i in range(1000)]:
        y_marbree = [int(C <= seuil1) for C in C_marbree]
        y_grise = [int(C <= seuil2) for C in C_grise]
        if abs(TPR(bob_marbree, y_marbree, 1) - TPR(bob_grise, y_grise, 1)) <= 1 / 100 and FPR(bob_marbree, y_marbree, 1) - FPR(bob_grise, y_grise, 1) <= 1 / 100:
            meilleurf = f_score(bob_marbree + bob_grise, y_marbree + y_grise, 1)
            meilleur1 = seuil1
            meilleur2 = seuil2

print(meilleur1, meilleur2, round(meilleurf, 3))