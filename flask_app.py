from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
CORS(app)

# Configuración de la conexión a la base de datos
DB_CONFIG = {
    'host': 'Altallr.mysql.pythonanywhere-services.com',
    'user': 'Altallr',  # Reemplaza con tu nombre de usuario
    'password': '&802r4rL',  # Reemplaza con tu contraseña
    'database': 'Altallr$registro'  # Reemplaza con el nombre de tu base de datos
}

@app.route('/productos', methods=['GET'])
def get_productos():
    try:
        # Conectar a la base de datos
        connection = mysql.connector.connect(**DB_CONFIG)

        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)  # Devuelve resultados como diccionarios
            query = "SELECT id, producto, inicio, precio, venta, restante, importe FROM inventario"
            cursor.execute(query)
            productos = cursor.fetchall()  # Obtener todos los resultados

            # Cerrar el cursor y la conexión
            cursor.close()
            connection.close()

            # Devolver los productos en formato JSON
            return jsonify(productos), 200

    except Error as e:
        return jsonify({'error': f'Error al conectarse a la base de datos: {e}'}), 500

@app.route('/detalles-producto', methods=['GET'])
def detalle_producto():
    nombre_producto = request.args.get('producto')

    producto = next((item for item in productos if item['producto'].lower() == nombre_producto.lower()), None)

    if producto:
        detalle = "\n".join([f"{key.capitalize()}: {value}" for key, value in producto.items()])
        return detalle, 200
    else:
        return "Producto no encontrado", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=0)
