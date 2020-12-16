from movements import app
from movements.forms import MovementForm
from flask import render_template, request, url_for, redirect
import csv
import sqlite3
from datetime import date

DBFILE = app.config["DBFILE"]


def consulta(query, params=()):
    conn = sqlite3.connect(DBFILE)
        #conectem amb la base de dades .dd
    c = conn.cursor() #c es el cursor de la base de dades
    '''
    'SELECT * FROM TABLA' -> [(),(), (),]
    'SELECT * FROM TABLA VACIA ' -> []
    'INSERT ...' -> []
    'UPDATE ...' -> []
    'DELETE ...' -> []
    '''

    c.execute(query, params) #ejecuta la consulta i els parametros
    conn.commit()

    filas = c.fetchall()
    print (filas)

    conn.close()

    if len(filas) == 0:  #si esta vuida no retornara res
        return filas

    columnNames = []
    for columnName in c.description:
        columnNames.append(columnName[0])

    listadediccionarios = []

    for fila in filas:
        d = {}
        for ix, columnName in enumerate(columnNames):
            d[columnName] = fila [ix]
        listadediccionarios.append(d)

    return listadediccionarios


@app.route("/")
def listaIngresos():

    ingresos = consulta("SELECT data, concepte, quantitat, id FROM moviments;")
    #estem consultant la base, en retornes el que hi ha , i sino hi ha res, la tabla vuida

    sumador = 0
    for ingreso in ingresos:
        sumador += float(ingreso['quantitat'])

    return render_template("movementsList.html", datos=ingresos, total=sumador) #es un metode, quan tu li dius el nom de fitxero ..html i el busca

@app.route("/creaalta", methods=["GET", "POST"]) #un punt d'entrada que crida a l'arxiu alta.html
def nouIngres(): 
    form = MovementForm(request.form)
    
    if request.method == "POST":

        if form.validate():
            consulta("INSERT INTO moviments (quantitat, concepte, data) VALUES (?, ?, ?);", 
                    (
                        form.quantitat.data,
                        form.concepte.data,
                        form.data.data
                    )
            ) #es la validació del formulari

            return redirect(url_for("listaIngresos"))
        
        else:
            return render_template("alta.html", form=form)

    return render_template("alta.html", form=form) #este form es com li hem dit en alta


@app.route("/modifica/<id>", methods=['GET', 'POST']) #el id es el parametre que modificarem de la base de dades
def modificaIngres(id):

    if request.method == "GET":

        registro = consulta("SELECT data, concepte, quantitat, id FROM moviments WHERE id = ?", (id,))[0]
        #llista de diccionario el 0, es x volem que isca l'1 xq en esta cas volem la id
        registro["data"] = date.fromisoformat(registro["data"]) #es x la fecha poder modificala
        form = MovementForm(data=registro) #data es del reference me torna un diccionari de datos que es el que tenim

        return render_template("modifica.html", form=form, id=id)

    else:
        form = MovementForm()
        if form.validate():
            consulta("UPDATE moviments SET data = ?, concepte = ?, quantitat = ? WHERE id = ?",
                    (request.form.get("data"),
                    request.form.get("concepte"),
                    float(request.form.get("quantitat")),
                    id
                    )
            )

            return redirect(url_for ("listaIngresos"))
        else:
            return render_template("modifica.html", form=form, id=id)
