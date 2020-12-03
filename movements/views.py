from movements import app
from flask import render_template
import csv

@app.route("/")
def listaIngresos():
    fIngresos = open("movements/data/basedades.csv", "r")  #estem lleguint l'arxiu
    csvReader = csv.reader(fIngresos, delimiter=',', quotechar='"')
    ingresos = list(csvReader)
    sumador = 0
    for ingreso in ingresos:
        sumador += float(ingreso[2]) #el 2, es per mostrat els numeros la llista, elemento 2 de cada linea
                #float es per que estem cridant a un fitxero de texte
    print (ingresos)
    return render_template("movementsList.html", datos=ingresos, total=sumador) #es un metode, quan tu li dius el nom de fitxero ..html i el busca

@app.route("/creaalta") #un punt d'entrada
def nouIngres(): 
    return "demà més"
