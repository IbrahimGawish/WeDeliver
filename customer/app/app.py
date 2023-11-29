from flask import Flask, jsonify,request
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
    cursor.execute('SELECT id,customer_name, customer_n_leased, customer_balance '
                   ' FROM customers_data')
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results

@app.route('/api/modify_customer_balance', methods=['POST'])
def modify_customer_balance():
    msg = ''
    customer_id = request.form.get("customer_id")
    balance = request.form.get("balance")
    if(customer_id and balance):
        try:
            connection = mysql.connector.connect(**config)
            cursor = connection.cursor(dictionary=True)
            table_name = 'customers_data'
            target_column = 'customer_balance'
            condition = 'id =' + str(customer_id)
            query = f"UPDATE {table_name} SET {target_column} = {target_column} + {str(balance)} WHERE {condition};"
            cursor.execute(query)
            connection.commit()
            cursor.close()
            connection.close()
        except Exception as e:
            print(e,flush=True)
            msg = "Error in modifying balance"
    else:
        msg = "Missing parameters"
    return jsonify({'msg': msg})

@app.route('/')
def index():
    return jsonify({'Customers Data': customers_data()})

@app.route("/api/sayHello")
def hello():
    return "Hello, Welcome to Customer Service"

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)