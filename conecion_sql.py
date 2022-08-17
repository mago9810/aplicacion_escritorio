import sqlite3

try:
    # mi_conexion = sqlite3.connect("Universidad.sqlite3")   
    # cursor = mi_conexion.cursor()
    # cursor.execute("SELECT * FROM Academico_curso")
    # rows = cursor.fetchall()
    # for row in rows:
    #     print(row)

    mi_conexion = sqlite3.connect("data_base.sqllite3")   
    cursor = mi_conexion.cursor()
    cursor.execute("SELECT * FROM productos")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
except Exception as ex:
    print(ex)

