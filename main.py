
from flask_cors import CORS

import psycopg2
import os
from flask import Flask, request, jsonify


os.environ['DATABASE_URL'] = "postgresql://postgres:TEyDcvdPSGfuMWcfMocSETeTblbPmcnm@junction.proxy.rlwy.net:48402/railway"

app = Flask(__name__)

CORS(app)

DATABASE_URL = os.getenv('DATABASE_URL')

def connect_db():
    return psycopg2.connect(DATABASE_URL)

@app.route('/get_data', methods=['GET'])
def get_data():
    try:
        with connect_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM led_log")
                rows = cursor.fetchall()
                data = [{'id': row[0], 'timestamp': row[1], 'led_status': row[2]} for row in rows]
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/add_data', methods=['POST'])
def add_data():
    try:
        led_status = request.json.get('led_status')
        with connect_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO led_log (timestamp, led_status) VALUES (NOW(), %s)", (led_status,))
            conn.commit()
        return jsonify({'message': 'La informacion se guardo correctamente en la base de datos'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')