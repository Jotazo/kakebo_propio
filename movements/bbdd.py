import sqlite3
from movements import app

class BBDD():

    __DBFILE = app.config['DB_FILE']

    def __init__(self):
        self.conn = self.__crea_con()
        self.c = self.__crea_cursor()
        self.__crea_tabla()

    def __crea_tabla(self):
        """
        Creación de la tabla
        """
        self.c.execute('''
        CREATE TABLE IF NOT EXISTS movimientos(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha text NOT NULL,
        concepto text NOT NULL,
        cantidad REAL NOT NULL);
        ''')

    def __crea_con(self):
        conn = sqlite3.connect(self.__DBFILE)
        return conn

    def __crea_cursor(self):
        c = self.conn.cursor()
        return c

    def query_insert(self, datos):
        """
        Llamada de inserción de datos
        """
        self.c.execute('INSERT INTO movimientos (cantidad, concepto, fecha) VALUES (?,?,?)', datos)
        self.conn.commit()
        self.conn.close()

    def query_select(self, id='', params=()):
        """
        Llamada de recuperación de datos
        """
        self.c.execute(f'SELECT fecha, concepto, cantidad, id FROM movimientos {id}', params)
        filas = self.c.fetchall()
        nombres = self.c.description
        if len(filas) == 0:
            return filas
        d = self.__create_dic(nombres, filas)
        self.conn.close()
        return d

    def query_update(self, datos):
        """
        Llamada de actualización de datos
        """
        self.c.execute('UPDATE movimientos SET fecha = ?, concepto= ?, cantidad = ? WHERE id = ?', datos)
        self.conn.commit()
        self.conn.close()

    def query_delete(self, id):
        """
        Llamada de borrado de datos
        """
        self.c.execute('DELETE FROM movimientos WHERE id=?', id)
        self.conn.commit()
        self.conn.close()
    
    def query_order_by(self, dato, desc=False):
        """
        Llamada de ordenado de datos
        """
        if desc:
            self.c.execute(f'SELECT * FROM movimientos ORDER BY {dato} DESC')
        else:
            self.c.execute(f'SELECT * FROM movimientos ORDER BY {dato}') 
        filas = self.c.fetchall()
        nombres = self.c.description
        if len(filas) == 0:
            return filas
        d = self.__create_dic(nombres, filas)
        self.conn.close()
        return d

    def __create_dic(self, nombres, filas):
        """
        Función que nos devuelve una lista de diccionarios con los datos de la BBDD
        """ 
        columnNames = []
        for columnName in nombres:
            columnNames.append(columnName[0])
        listaDeDiccionarios = []

        for fila in filas:
            d = {}
            for ix, columnName in enumerate(columnNames):
                d[columnName] = fila[ix]
            listaDeDiccionarios.append(d)

        return listaDeDiccionarios 