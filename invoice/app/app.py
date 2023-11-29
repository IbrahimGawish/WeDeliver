from flask import Flask, jsonify,request
import mysql.connector
from apscheduler.schedulers.background import BackgroundScheduler
import requests
import socket

app = Flask(__name__)
#app.config['ENV'] = 'development'
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
    cursor.execute('SELECT id,  invoice_payment_status, invoice_amount, customer_id '
                   ' FROM invoices_data')
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results

def scheduled_invoice():
    print("Monthly Invoice executed!", flush=True)
    host_ip = socket.gethostbyname('host.docker.internal')
    api_url = f"http://{host_ip}:5006/api/get_current_contracts"
    timeout = 5
    try:
        response = requests.get(api_url, timeout=timeout)
        if response.status_code == 200:
            invoices = response.json()
            if(invoices['invoices_num'] >0):
                connection = mysql.connector.connect(**config)
                cursor = connection.cursor()
                query = " delete from invoices_data;"
                cursor.execute(query)
                for invoice in invoices['invoices']:
                    query = (" insert into invoices_data(invoice_payment_status,invoice_amount,customer_id)"
                              " values "
                              " ('UnPaid',"+str(invoice['number_of_days'] * invoice['price_per_day']) + ","
                              " "+str(invoice['customer_id'])+ ");")
                    cursor.execute(query)
                cursor.close()
                connection.commit()
                connection.close()
                return f"Invoices added successfully."
        else:
            return f"Error calling API. Status code: {response.status_code}"
    except requests.exceptions.Timeout:
        return f"Request to API timed out after {timeout} seconds."
    except requests.exceptions.RequestException as e:
        return f"Error calling API: {e}"

@app.route('/')
def index():
    return jsonify({'Invoices Data': invoices_data()})

@app.route("/api/sayHello")
def hello():
    print("Ok!!!", flush=True)
    return "Hello, Welcome to Invoice Service"

@app.route('/api/pay_invoice', methods=['POST'])
def pay_invoice():
    customer_id = request.args.get("customer_id")
    invoice_id = request.args.get("invoice_id")
    invoice_amount = request.args.get("invoice_amount")
    except_case = request.args.get("except_case",'')
    msg = ''
    if(customer_id and invoice_id and invoice_amount):
        host_ip = socket.gethostbyname('host.docker.internal')
        timeout = 5
        finance_check = ''
        print("-----1-----",flush=True)
        try:
            finance_url = f"http://{host_ip}:5008/api/add_finance"
            finance_data = {
                "customer_id": customer_id,
                "invoice_id": invoice_id,
                "invoice_amount": invoice_amount
            }
            response = requests.post(finance_url, data=finance_data, timeout=timeout)
            if response.json()['msg'] =="": finance_check ="Ok"
            print("-----2-----",flush=True)
        except requests.exceptions.Timeout:
            print("-----3-----",flush=True)
            msg+= f"Request to Finance API timed out after {timeout} seconds."
        except requests.exceptions.RequestException as e:
            print("-----4-----",flush=True)
            msg += f"Error calling Finance API: {e}"
        if(finance_check == "Ok"):
            connection = mysql.connector.connect(**config)
            cursor = connection.cursor()
            query = " select invoice_amount from invoices_data where ID = "+invoice_id+";"
            cursor.execute(query)
            invoice_original_amount = cursor.fetchone()[0]
            cursor.close()
            connection.close()
            customer_balance = int(invoice_amount )- int(invoice_original_amount)
            customer_url = f"http://{host_ip}:5002/api/modify_customer_balance"
            customer_data = {
                "customer_id": customer_id,
                "balance": customer_balance
            }
            response = requests.post(customer_url, data=customer_data, timeout=timeout)
            print("-----5-----", flush=True)
            print(response.json()['msg'], flush=True)
            if(response.json()['msg'] == ""):
                try:
                    print("-----6-----", flush=True)
                    if (int(invoice_original_amount) == int(invoice_amount)):
                        if(except_case):
                            customer_url = f"http://{host_ip}:5004/api/payInvoiceFullyWithException"
                        else:
                            customer_url = f"http://{host_ip}:5004/api/payInvoiceFully"
                        customer_data = {
                            "invoice_id": invoice_id,
                            "except_case": except_case
                        }
                        response = requests.post(customer_url, data=customer_data, timeout=timeout)
                        msg += response.json()['msg']
                        print("-----7-----", flush=True)
                    if (int(invoice_original_amount) > int(invoice_amount)):
                        customer_url = f"http://{host_ip}:5004/api/payInvoicePartially"
                        customer_data = {
                            "invoice_id": invoice_id,
                            "except_case": except_case
                        }
                        print("-----8-----", flush=True)
                        response = requests.post(customer_url, data=customer_data, timeout=timeout)
                        msg += response.json()['msg']
                except Exception as e:
                    print("-----9-----", flush=True)
                    print(e, flush=True)
                    customer_url = f"http://{host_ip}:5002/api/modify_customer_balance"
                    customer_data = {
                        "customer_id": customer_id,
                        "balance": customer_balance * -1
                    }
                    response = requests.post(customer_url, data=customer_data, timeout=timeout)
                    msg += response.json()['msg']
                    finance_url = f"http://{host_ip}:5008/api/delete_finance"
                    finance_data = {
                        "customer_id": customer_id,
                        "invoice_id": invoice_id,
                        "invoice_amount": invoice_amount
                    }
                    response = requests.post(finance_url, data=finance_data, timeout=timeout)
                    msg += response.json()['msg']
                    print("-----10-----", flush=True)
            else:
                print("-----11-----", flush=True)
                finance_url = f"http://{host_ip}:5008/api/delete_finance"
                finance_data = {
                    "customer_id": customer_id,
                    "invoice_id": invoice_id,
                    "invoice_amount": invoice_amount
                }
                response = requests.post(finance_url, data=finance_data, timeout=timeout)
                msg += response.json()['msg']
    else:
        msg += f"Missing Parameters"
    print("Pay4",flush=True)
    print(invoice_amount,flush=True)
    return jsonify({'msg':( msg if msg !='' else "Paid transaction done")})

@app.route('/api/payInvoiceFully', methods=['POST'])
def payInvoiceFully():
    msg =' '
    invoice_id = request.form.get("invoice_id")
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        query = " update invoices_data  set invoice_payment_status ='Fully Paid' where id = "+invoice_id
        cursor.execute(query)
        cursor.close()
        connection.commit()
        connection.close()
    except Exception as e:
        msg += f"Missing Parameters"
    return jsonify({'msg':msg})

@app.route('/api/payInvoiceFullyWithException', methods=['POST'])
def payInvoiceFullyWithException():
    msg =' '
    invoice_id = request.form.get("invoice_id")
    try:
        print(ox)
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        query = " update invoices_data  set invoice_payment_status ='Fully Paid' where id = "+invoice_id
        cursor.execute(query)
        cursor.close()
        connection.commit()
        connection.close()
    except Exception as e:
        msg += f"Error in Paying"
    return jsonify({'msg':msg})

@app.route('/api/payInvoicePartially', methods=['POST'])
def payInvoicePartially():
    msg =' '
    invoice_id = request.form.get("invoice_id")
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        query = " update invoices_data  set invoice_payment_status ='Partially Paid' where id = "+invoice_id
        cursor.execute(query)
        cursor.close()
        connection.commit()
        connection.close()
    except Exception as e:
        msg += f"Missing Parameters"
    return jsonify({'msg':msg})

scheduler = BackgroundScheduler(daemon=True)
# Add the scheduled task to run every 30 days
scheduler.add_job(scheduled_invoice, 'interval', days=30, max_instances=1 )
#scheduler.add_job(scheduled_invoice, 'interval', seconds=15, max_instances=1)
scheduler.start()
'''
@app.teardown_appcontext
def shutdown_scheduler(exception=None):
    scheduler.shutdown()
'''
if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)