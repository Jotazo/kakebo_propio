import sqlite3

class BBDD():

    __DBFILE = 'movements/data/DBFLASK.db'

    def __init__(self):
        self.conn = self.__crea_con()
        self.c = self.__crea_cursor()

    def __crea_con(self):
        conn = sqlite3.connect(self.__DBFILE)
        return conn

    def __crea_cursor(self):
        c = self.conn.cursor()
        return c

    def query_insert(self, datos):
        self.c.execute('INSERT INTO movimientos (cantidad, concepto, fecha) VALUES (?,?,?)', datos)
        self.conn.commit()
        self.conn.close()

    def query_select(self, id='', params=()):

        self.c.execute(f'SELECT fecha, concepto, cantidad, id FROM movimientos {id}', params)
        filas = self.c.fetchall()
        nombres = self.c.description
        if len(filas) == 0:
            return filas
        d = self.__create_dic(nombres, filas)
        self.conn.close()
        return d

    def query_update(self, datos):
        self.c.execute('UPDATE movimientos SET fecha = ?, concepto= ?, cantidad = ? WHERE id = ?', datos)
        self.conn.commit()
        self.conn.close()

    def query_delete(self, id):
        self.c.execute('DELETE FROM movimientos WHERE id=?', id)
        self.conn.commit()
        self.conn.close()
    
    def query_order_by(self, dato, desc=False):
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