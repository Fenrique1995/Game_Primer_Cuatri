import sqlite3
import json

try:

    def crear_tabla():
        mi_conexion = sqlite3.connect('src/mi_basede_datos.sql')
        cursor = mi_conexion.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS mi_tabla (
            id INTEGER PRIMARY KEY,
            nombre TEXT,
            score INTEGER
        )
        ''')

        mi_conexion.commit()
        mi_conexion.close()

    def leer_base_de_datos():
        mi_conexion = sqlite3.connect('src/mi_basede_datos.sql')
        cursor = mi_conexion.cursor()

        cursor.execute('SELECT nombre, score FROM mi_tabla')
        filas = cursor.fetchall()

        mi_conexion.close()

        return {nombre: score for nombre, score in filas}

    def actualizar_base_de_datos(nuevos_datos):
        mi_conexion = sqlite3.connect('src/mi_basede_datos.sql')
        cursor = mi_conexion.cursor()

        for nombre, score in nuevos_datos.items():
            cursor.execute('''
                INSERT OR IGNORE INTO mi_tabla (nombre, score)
                VALUES (?, ?)
            ''', (nombre, score))

        mi_conexion.commit()
        mi_conexion.close()

    # Lectura y comparación de datos
    with open('player_data.json', 'r') as file:
        nuevos_datos_json = json.load(file)

    crear_tabla()
    datos_actuales = leer_base_de_datos()

    if datos_actuales != nuevos_datos_json:
        # Actualizar la base de datos
        actualizar_base_de_datos(nuevos_datos_json)
        print("Se actualizaron los datos en la base de datos.")
    else:
        print("No hay cambios en los datos.")

except Exception as e:
    # Código que se ejecuta si se produce una excepción
    print(f"Se produjo una excepción: {e}")
