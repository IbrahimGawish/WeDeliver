from flask import Flask, jsonify
import mysql.connector


app = Flask(__name__)
config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'finance',
        'auth_plugin': 'mysql_native_password'
    }

def finance_data():
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT invoice_id, customer_id, amount '
                   ' FROM finance_data')
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results

@app.route('/')
def index():
    return jsonify({'Finance Data': finance_data()})

@app.route("/api/sayHello")
def hello():
    return "Hello, Welcome to Finance Service"

if __name__ == '__main__':
    app.run(host='0.0.0.0')