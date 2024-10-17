from ia01.utils import lecture_csv
from ia01.privacy import k_anonymite, groupe2, discret_seuils, discretisation

data = lecture_csv("data/compas-privacy.csv")

for element in data:
    element["age"] = int(element["age"])

print(f"Nombre de personnes : {len(data)}\n")
for element in [["sex"], ["age"], ["group"], ["sex", "group"], ["sex", "age"], ["age", "group"], ["sex", "age", "group"]]:
    G = groupe2(data, element)
    taille_G = [len(g) for g in G]
    count = 0
    for taille in taille_G:
        if taille == 1:
            count += 1
    print(f"{k_anonymite(data, element)} - anonyme par rapport à {element}. {count} personnes sont identifiables.")


for element in data:
    if element["group"] not in ["Causasian", "African-American"]:
        element["group"] = "Other"

element = ["sex", "group"]
G = groupe2(data, element)
taille_G = [len(g) for g in G]
count = 0
for taille in taille_G:
    if taille == 1:
        count += 1
print(f"{k_anonymite(data, element)} - anonyme par rapport à {element}. {count} personnes sont identifiables.")


seuils = discret_seuils([element["age"] for element in data], 7)
for element in data:
    element["age"] = discretisation(element["age"], seuils)

element = ["age"]
G = groupe2(data, element)
taille_G = [len(g) for g in G]
count = 0
for taille in taille_G:
    if taille == 1:
        count += 1
print(f"{k_anonymite(data, element)} - anonyme par rapport à {element}. {count} personnes sont identifiables.")

