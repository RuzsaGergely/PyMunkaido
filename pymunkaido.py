# PyMunkaido v1.0

from datetime import datetime
import sys

kartya_fajl_nev = ""
kartya_adatok_fejlec = []
kartya_adatok_torzs = []

def parancssor():
    bemenet = input("> ")

    if bemenet == "export":
        print()
        parancssor()
    elif bemenet == "belep":
        parancsBelep()
        parancssor()
    elif bemenet == "kilep":
        parancsKilep()
        parancssor()
    elif bemenet == "segitseg":
        print("Parancsok: belep, kilep, segitseg, export, lista, bezar")
        parancssor()
    elif bemenet == "bezar":
        print("Jó pihenést!")
        exit(0)
    elif bemenet == "lista":
        parancsLista()
        parancssor()
    else:
        print("Ismeretlen parancs!")
        parancssor()

def kartyaBeolvas():
    fajl = open(kartya_fajl_nev, "r", encoding="windows-1252").readlines()
    for x in range(len(fajl)):
        if x == 0 or x == 1:
            kartya_adatok_fejlec.append(fajl[x].strip())
        else:
            darabok = fajl[x].strip().split(';')
            kartya_adatok_torzs.append(darabok)
    print("Kártya beolvasva!")
    print(f'Felhasználó: {kartya_adatok_fejlec[0]}')
    print(f'Projekt: {kartya_adatok_fejlec[1]}')

def parancsLista():
    for i in kartya_adatok_torzs:
        print(i)

def parancsBelep():
    if kartya_adatok_torzs[len(kartya_adatok_torzs)-1][0] == "KI":
        leiras = input("Adjon meg egy leírást: ")
        temp = ["BE", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), leiras]
        kartya_adatok_torzs.append(temp)
        print("Kártya érvényesítve, belépési idő rögzítve!")
        open(kartya_fajl_nev, "a", encoding="windows-1252").write(f'\nBE;{datetime.now().strftime("%Y-%m-%d %H:%M:%S")};{leiras}')
    else:
        print("Először zárd le az előző munkaidődet!")

def parancsKilep():
    if kartya_adatok_torzs[len(kartya_adatok_torzs)-1][0] == "BE":
        temp = ["KI", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "~"]
        kartya_adatok_torzs.append(temp)
        print("Kártya érvényesítve, kilépési idő rögzítve!")
        open(kartya_fajl_nev, "a", encoding="windows-1252").write(f'\nKI;{datetime.now().strftime("%Y-%m-%d %H:%M:%S")};~')
    else:
        print("Először nyiss egy munkaidőt!")

if __name__ == "__main__":
    print("### PyMunkaido - Lyukkártya stílusú munkaidő nyilvántartó rendszer ###")
    print(f'Indítási idő: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    if len(sys.argv) < 2:
        print("Adj meg paraméterként egy kártyafájlt a szkript indításakor!")
        exit(1)
    else:
        kartya_fajl_nev = sys.argv[1]
        kartyaBeolvas()
        
    parancssor()