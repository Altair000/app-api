@app.route('/actualizar-venta', methods=['GET'])
def actualizar_venta_get():
    id_producto = request.args.get('id')
    incremento = request.args.get('cantidad', type=int)  # Convertir el parámetro a entero

    if not id_producto or incremento is None:
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
