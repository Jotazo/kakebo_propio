from flask import request
from movements import bbdd

l_tipos = ['fasc', 'fdesc', 'casc', 'cdesc', 'dasc', 'ddesc']

def devuelve_query():
    tipo = ''
    desc = False
    bd = bbdd.BBDD()
    
    if request.full_path[1] == 'f':
        tipo='fecha'
        if request.full_path[2] == 'd':
            desc = True
    elif request.full_path[1] == 'c':
        tipo='concepto'
        if request.full_path[2] == 'd':
            desc = True
    elif request.full_path[1] == 'd':
        tipo='cantidad'
        if request.full_path[2] == 'd':
            desc = True
    else:
        print('ERROR')

    datos = bd.query_order_by(tipo, desc=desc)
    return datos