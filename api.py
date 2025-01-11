# app.py
from flask import Flask, jsonify
import psycopg2
from db import get_db_connection

app = Flask(__name__)

@app.route('/productos', methods=['GET'])
def get_productos():
    # Establece la conexión con la base de datos
    conn = get_db_connection()
    
    try:
        # Crea un cursor y ejecuta la consulta
        cur = conn.cursor()
        cur.execute("SELECT productos FROM inventario;")
        
        # Obtén los resultados de la consulta
        productos = cur.fetchall()
        
        # Devuelve los productos como una respuesta JSON
        return jsonify([producto[0] for producto in productos])  # [producto[0]] es para obtener solo el valor de la columna 'productos'
    
    except Exception as e:
        return str(e), 500
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
