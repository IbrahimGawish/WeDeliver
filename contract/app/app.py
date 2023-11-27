from flask import Flask, jsonify
import mysql.connector


app = Flask(__name__)
config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'contract',
        'auth_plugin': 'mysql_native_password'
    }

def contracts_data():
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT customer_id, vehicle_id, lease_start_date, lease_end_date, price_per_day '
                   ' FROM contracts_data')
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results

@app.route('/')
def index():
    return jsonify({'Contracts Data': contracts_data()})

@app.route("/api/sayHello")
def hello():
    return "Hello, Welcome to Contract Service"

if __name__ == '__main__':
    app.run(host='0.0.0.0')