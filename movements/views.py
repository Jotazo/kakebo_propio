from movements import app
from movements import forms
from movements import bbdd
from movements import misc

from flask import render_template, request, url_for, redirect

import sqlite3

from datetime import date

@app.route('/')
@app.route('/<tipo>')
def listaIngresos(tipo='/?'):
    bd = bbdd.BBDD()

    if tipo in misc.l_tipos:
        ingresos = misc.devuelve_query()
    else:
        ingresos = bd.query_select()
    total = 0
    for ingreso in ingresos:
        total += ingreso['cantidad']

    return render_template("movementsList.html",datos=ingresos, total=round(total, 2), tipo=tipo)

@app.route('/creaalta', methods=['GET', 'POST'])
def nuevoIngreso():
    nuestroForm = forms.TaskForm()
    bd = bbdd.BBDD()

    if request.method == 'POST' and nuestroForm.validate_on_submit():

        datos = (nuestroForm.cantidad.data, nuestroForm.concepto.data, nuestroForm.fecha.data)
        bd.query_insert(datos)

        return redirect(url_for('listaIngresos'))
        
    return render_template("alta.html", form=nuestroForm)

@app.route("/modifica/<id>", methods=['GET', 'POST'])
def modificaIngreso(id):
    
    bd = bbdd.BBDD()

    if request.method == 'GET':

        registro = bd.query_select(id='WHERE id=?', params=(id,))[0]
        registro['fecha'] = date.fromisoformat(registro['fecha'])
        nuestroForm = forms.TaskForm(data=registro)
        print(nuestroForm.data)
        return render_template("modifica.html", form=nuestroForm, id=id)

    else:
        nuestroForm = forms.TaskForm()
        if nuestroForm.validate_on_submit():
    
            datos = (nuestroForm.fecha.data, nuestroForm.concepto.data, nuestroForm.cantidad.data, id)
            bd.query_update(datos)

            return redirect(url_for("listaIngresos"))

        else:
            return render_template('modifica.html', form=nuestroForm, id=id)

@app.route("/delete/<id>", methods=['GET', 'POST'])
def eliminaIngreso(id):
    nuestroForm = forms.TaskForm()
    bd = bbdd.BBDD()

    if request.method == 'POST':
        bd.query_delete((id,))
        return redirect(url_for('listaIngresos'))

    registroBorrar = bd.query_select(id='WHERE id=?', params=(id,))
    return render_template("borrar.html", registro=registroBorrar, form=nuestroForm)