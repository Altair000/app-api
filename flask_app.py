from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
CORS(app)

# Configuración de la conexión a la base de datos
DB_CONFIG = {
    'host': 'Altallr.mysql.pythonanywhere-services.com',
    'user': 'Altallr',
    'password': '&802r4rL',
    'database': 'Altallr$registro'
}

@app.route('/productos', methods=['GET'])
def get_productos():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            query = "SELECT id, producto, inicio, precio, venta, restante, importe FROM inventario"
            cursor.execute(query)
            productos = cursor.fetchall()
            cursor.close()
            connection.close()
            return jsonify(productos), 200
    except Error as e:
        return jsonify({'error': f'Error al conectarse a la base de datos: {e}'}), 500

@app.route('/detalles-producto', methods=['GET'])
def detalle_producto():
    nombre_producto = request.args.get('producto')
    if not nombre_producto:
        return "Debe proporcionar el nombre del producto como parámetro.", 400

    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT id, producto, inicio, precio, venta, restante, importe
                FROM inventario
                WHERE producto = %s
            """
            cursor.execute(query, (nombre_producto,))
            producto = cursor.fetchone()
            cursor.close()
            connection.close()

            if producto:
                detalle = "\n".join([f"{key.capitalize()}: {value}" for key, value in producto.items()])
                return detalle, 200
            else:
                return "Producto no encontrado", 404
    except Error as e:
        return jsonify({'error': f'Error al conectarse a la base de datos: {e}'}), 500

@app.route('/nombre-producto', methods=['GET'])
def nombre_producto():
    id_producto = request.args.get('id')

    if not id_producto:
        return "Debe proporcionar el ID del producto como parámetro.", 400

    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            query = "SELECT producto FROM inventario WHERE id = %s"
            cursor.execute(query, (id_producto,))
            producto = cursor.fetchone()
            cursor.close()
            connection.close()

            if producto:
                return producto['producto'], 200
            else:
                return "Producto no encontrado", 404
    except Error as e:
        return jsonify({'error': f"Error al conectarse a la base de datos: {e}"}), 500

@app.route('/actualizar-venta', methods=['POST'])
def actualizar_venta():
    datos = request.json
    id_producto = datos.get('id')
    incremento = datos.get('cantidad')

    if not id_producto or not incremento:
        return "Debes proporcionar el ID del producto y el número a incrementar.", 400

    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            query_select = "SELECT venta, restante FROM inventario WHERE id = %s"
            cursor.execute(query_select, (id_producto,))
            producto = cursor.fetchone()

            if not producto:
                cursor.close()
                connection.close()
                return "Producto no encontrado", 404

            nueva_venta = producto['venta'] + incremento
            nuevo_restante = producto['restante'] - incremento

            if nuevo_restante < 0:
                cursor.close()
                connection.close()
                return "No hay suficientes productos restantes para realizar esta venta.", 400

            query_update = """
                UPDATE inventario
                SET venta = %s, restante = %s
                WHERE id = %s
            """
            cursor.execute(query_update, (nueva_venta, nuevo_restante, id_producto))
            connection.commit()
            cursor.close()
            connection.close()

            return f"Venta actualizada correctamente. Nueva venta: {nueva_venta}, Restante: {nuevo_restante}", 200
    except Error as e:
        return jsonify({'error': f"Error al conectarse a la base de datos: {e}"}), 500

if __name__ == '__main__':
    app.run(port=0)
