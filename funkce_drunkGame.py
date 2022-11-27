import random
import numpy as np


def ocekavanahodnota(hodnoty_dict):
    kroky = list(hodnoty_dict.keys())
    pocet = [x / sum(hodnoty_dict.values()) for x in hodnoty_dict.values()]
    values = np.asarray(kroky)
    weights = np.asarray(pocet)
    return (values * weights).sum() / weights.sum()


def drunkGame(cesta, pocetkroku, tisknout):
    slovo = list("." * (cesta - 1))
    # začni na pozici delka slova (+1 list)
    pozice_opilce = len(slovo)
    kroky = 0
    moznosti = [-1, 1]
    # opakuj dokud nevycerpa kroky nebo když nedorazí domu -> pozice -1
    while kroky != pocetkroku and pozice_opilce != -1:
        # když je pozice delka listu tak krok k domu jinak nahdne
        if pozice_opilce == len(slovo):
            krok = -1
        else:
            krok = moznosti[random.randint(0, 1)]

        kroky += 1
        pozice_opilce += krok

        # když je pozice opilce v rozmezí 0 - 7 tak dej hvězdu
        if tisknout:
            if pozice_opilce in range(0, len(slovo)):
                if pozice_opilce - krok != len(slovo):
                    slovo[pozice_opilce - krok] = "."
                slovo[pozice_opilce] = "*"
            else:
                slovo[pozice_opilce - krok] = "."
            print('domov' + ''.join(slovo) + 'hospoda')

    if pozice_opilce == -1:
        uspech = True
    else:
        uspech = False

    return {"úspěch": uspech, "kroku": kroky}


def analyzaHry(cesta, pocetkroku, pocetopakovani):
    DoselDocile = 0
    krokucelkem = 0
    rolozeni_uspechu_kroky = {}
    for hra in range(1, pocetopakovani):
        vysledek = drunkGame(cesta, pocetkroku, False)
        if vysledek["úspěch"]:
            DoselDocile += 1
            krokucelkem += vysledek["kroku"]
            klic = vysledek.get(vysledek["kroku"])
            if klic:
                rolozeni_uspechu_kroky[vysledek["kroku"]] += 1
            else:
                rolozeni_uspechu_kroky[vysledek["kroku"]] = 1

    minimum = min(rolozeni_uspechu_kroky.keys()) if len(rolozeni_uspechu_kroky) > 1 else 0
    maximum = max(rolozeni_uspechu_kroky.keys()) if len(rolozeni_uspechu_kroky) > 1 else 0
    smerodatna_odchylka = np.std(list(rolozeni_uspechu_kroky.keys()))
    expectedvalue = ocekavanahodnota(rolozeni_uspechu_kroky)
    procentoUspechu = round((DoselDocile / pocetopakovani) * 100)
    prumerKroku = round(krokucelkem / DoselDocile)
    return {"úspěch": procentoUspechu, "prumer_Kroku": prumerKroku, "očekávaná hodnota": expectedvalue,
            "smerodatna odchylka": smerodatna_odchylka, "min": minimum, "max": maximum}