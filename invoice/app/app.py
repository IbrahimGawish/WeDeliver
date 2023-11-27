from flask import Flask, jsonify
import mysql.connector


app = Flask(__name__)
config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'invoice',
        'auth_plugin': 'mysql_native_password'
    }

def invoices_data():
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT id,  invoice_payment_status, invoice_amount '
                   ' FROM invoices_data')
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results

@app.route('/')
def index():
    return jsonify({'Invoices Data': invoices_data()})

@app.route("/api/sayHello")
def hello():
    return "Hello, Welcome to Invoice Service"

if __name__ == '__main__':
    app.run(host='0.0.0.0')