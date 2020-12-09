from movements import app
from flask import render_template, request, url_for, redirect
import csv

@app.route("/")
def listaIngresos():
    fIngresos = open("movements/data/basedades.csv", "r")  #estem lleguint l'arxiu
    csvReader = csv.reader(fIngresos, delimiter=',', quotechar='"')
    ingresos = list(csvReader)
    sumador = 0
    for ingreso in ingresos:
        sumador += float(ingreso[2]) #el 2, es per mostrat els numeros la llista, element 2 de cada linea
                    #Estem estem cridant a un fitxero de texte
    return render_template("movementsList.html", datos=ingresos, total=sumador) #es un metode, quan tu li dius el nom de fitxero ..html i el busca

@app.route("/creaalta", methods=["GET", "POST"]) #un punt d'entrada que crida a l'arxiu alta.html
def nouIngres(): 
    if request.method == "POST":
        fIngresos = open("movements/data/basedades.csv", "a", newline="")  #per ficar cada nou registre
        csvWriter = csv.writer(fIngresos, delimiter=',', quotechar='"')
        csvWriter.writerow([request.form.get("data"), request.form.get("concepte"), request.form.get("import")])  #.form. formulari
        #per registrsar els camps nous del formulari de alta.html -creaalta
        return redirect(url_for("listaIngresos")) #es la ruta que crida a la funció

    return render_template("alta.html")

