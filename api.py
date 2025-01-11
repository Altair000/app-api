from flask import Flask, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Configuración de la conexión a la base de datos
DB_CONFIG = {
    'host': 'Altalr.mysql.pythonanywhere-services.com',
    'user': 'Altalr',  # Reemplaza con tu nombre de usuario
    'password': '&802r4rL',  # Reemplaza con tu contraseña
    'database': 'Altalr$registro'  # Reemplaza con el nombre de tu base de datos
}

@app.route('/productos', methods=['GET'])
def get_productos():
    try:
        # Conectar a la base de datos
        connection = mysql.connector.connect(**DB_CONFIG)

        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)  # Devuelve resultados como diccionarios
            query = "SELECT producto FROM inventario"
            cursor.execute(query)
            productos = cursor.fetchall()  # Obtener todos los resultados

            # Cerrar el cursor y la conexión
            cursor.close()
            connection.close()

            # Devolver los productos en formato JSON
            return jsonify({'productos': productos}), 200

    except Error as e:
        return jsonify({'error': f'Error al conectarse a la base de datos: {e}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
