from flask import Flask, jsonify,request
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

@app.route('/api/add_finance', methods=['POST'])
def add_finance():
    msg= ''
    customer_id = request.form.get("customer_id")
    invoice_id = request.form.get("invoice_id")
    invoice_amount = request.form.get("invoice_amount")
    if(customer_id and invoice_id and invoice_amount):
        try:
            connection = mysql.connector.connect(**config)
            cursor = connection.cursor()
            query = (" insert into finance_data(invoice_id,customer_id,amount)"
                     " values "
                     " (" + str(invoice_id) + "," + str(customer_id) +"," + str(invoice_amount) + ");")
            cursor.execute(query)
            cursor.close()
            connection.commit()
            connection.close()
        except Exception as e:
            msg = "Error in saving finance"
    else:
        msg= "Missing parameters"
    return jsonify({'msg':msg})

@app.route('/api/delete_finance', methods=['POST'])
def delete_finance():
    msg = ''
    customer_id = request.form.get("customer_id")
    invoice_id = request.form.get("invoice_id")
    invoice_amount = request.form.get("invoice_amount")
    if (customer_id and invoice_id and invoice_amount):
        try:
            connection = mysql.connector.connect(**config)
            cursor = connection.cursor()
            query = (" delete from finance_data where invoice_id="+str(invoice_id)+" "
                    " and customer_id="+str(customer_id)+" and amount = "+invoice_amount+" ")
            cursor.execute(query)
            cursor.close()
            connection.commit()
            connection.close()
        except Exception as e:
            msg = "Error in deleting finance"
    else:
        msg = "Missing parameters"
    return jsonify({'msg':msg})

@app.route('/')
def index():
    return jsonify({'Finance Data': finance_data()})

@app.route("/api/sayHello")
def hello():
    return "Hello, Welcome to Finance Service"

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)