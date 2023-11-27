from flask import Flask, jsonify
import mysql.connector


app = Flask(__name__)
config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'customer',
        'auth_plugin': 'mysql_native_password'
    }

def customers_data():
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT customer_name, customer_n_leased, customer_balance '
                   ' FROM customers_data')
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results

@app.route('/')
def index():
    return jsonify({'Customers Data': customers_data()})

@app.route("/api/sayHello")
def hello():
    return "Hello, Welcome to Customer Service"

if __name__ == '__main__':
    app.run(host='0.0.0.0')