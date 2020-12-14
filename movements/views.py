from movements import app
from flask import render_template, request, url_for, redirect
import sqlite3
from movements import forms as form
from movements import bbdd

@app.route('/')
def listaIngresos():
    bd = bbdd.BBDD()

    ingresos = bd.query_select()
    total = 0
    for ingreso in ingresos:
        total += float(ingreso['cantidad'])

    return render_template("movementsList.html",datos=ingresos, total=round(total, 2))

@app.route('/creaalta', methods=['GET', 'POST'])
def nuevoIngreso():
    nuestroForm = form.TaskForm()
    bd = bbdd.BBDD()

    if request.method == 'POST' and nuestroForm.validate_on_submit():

        datos = (nuestroForm.cantidad.data, nuestroForm.concepto.data, nuestroForm.fx.data)
        bd.query_insert(datos)

        return redirect(url_for('listaIngresos'))
        
    return render_template("alta.html", form=nuestroForm)

@app.route("/modifica/<id>", methods=['GET', 'POST'])
def modificaIngreso(id):
    nuestroForm = form.TaskForm()
    bd = bbdd.BBDD()

    if request.method =='POST' and nuestroForm.validate_on_submit():
    
        datos = (nuestroForm.fx.data, nuestroForm.concepto.data, nuestroForm.cantidad.data, int(nuestroForm.idhidden.data))
        bd.query_update(datos)

        return redirect(url_for("listaIngresos"))

    registro = bd.query_select(id='WHERE id=?', params=(id,))
    return render_template("modifica.html", form=nuestroForm, registro=registro)

@app.route("/delete/<id>", methods=['GET', 'POST'])
def eliminaIngreso(id):
    nuestroForm = form.TaskForm()
    bd = bbdd.BBDD()

    if request.method == 'POST':
        bd.query_delete(id)
        return redirect(url_for('listaIngresos'))

    registroBorrar = bd.query_select(id='WHERE id=?', params=(id,))
    return render_template("borrar.html", registro=registroBorrar, form=nuestroForm)
