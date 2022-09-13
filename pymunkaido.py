# PyMunkaido v1.0

from datetime import datetime
import sys

kartya_fajl_nev = ""
kartya_adatok_fejlec = []
kartya_adatok_torzs = []

def parancssor():
    bemenet = input("> ")

    if bemenet == "export":
        parancsExport()
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

def parancsExport():
    kimeneti_fajl = open(f'{kartya_fajl_nev}_export.html', "w", encoding="utf-8")
    kimeneti_fajl.write("<html><body><h1>Munkaidő jelentés - export</h1>")
    kimeneti_fajl.write(f'<p><b>Felhasználó neve:</b> {kartya_adatok_fejlec[0]}</p><p><b>Projekt neve:</b> {kartya_adatok_fejlec[1]}</p>')
    kimeneti_fajl.write("<table border=1><tr><th>Be/Ki</th><th>Időpont</th><th>Munkaleírás</th><th colspan=2>Munkaidő</th></tr>")
    tempdate = datetime.now()
    total_sec = 0
    for x in kartya_adatok_torzs:
        if x[0] == "BE":
            kimeneti_fajl.write(f'<tr><td>{x[0]}</td><td>{x[1]}</td><td rowspan=2>{x[2]}</td><td><i>Másodperc</i></td><td><i>Perc</i></td></tr>')
            tempdate = datetime.fromisoformat(x[1])
        else:
            kimeneti_fajl.write(f'<tr><td>{x[0]}</td><td>{x[1]}</td><td>{round(((datetime.fromisoformat(x[1])-tempdate).total_seconds()),2)}</td><td>{round(((datetime.fromisoformat(x[1])-tempdate).total_seconds()/60),2)}</td></tr>')
            kimeneti_fajl.write(f'<tr><td colspan=5></td></tr>')
            total_sec += (datetime.fromisoformat(x[1])-tempdate).total_seconds()
    kimeneti_fajl.write(f'<tr><td colspan=5><b>Teljes munkaidő: </b>{round((total_sec/60)/60,2)} óra // {round((total_sec/60),2)} perc</td></tr></table><p>Generálás időpontja: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p></body></html>')

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