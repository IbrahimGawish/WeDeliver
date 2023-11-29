from flask import Flask, jsonify
import mysql.connector


app = Flask(__name__)
config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'vehicles',
        'auth_plugin': 'mysql_native_password'
    }

def vehicles_data():
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT id, vehicle_type, vehicle_status, rent_price, onboard_date '
                   ' FROM vehicles_data')
    results = cursor.fetchall()
    cursor.close()
    #cursor = connection.cursor()
    #cursor.execute("update vehicles_data set onboard_date ='2023-12-28 12:00:00' where vehicle_type='Car'; ")
    #cursor.execute("update vehicles_data set onboard_date ='2023-12-20 12:00:00' where vehicle_type='Motorcycle'; ")
    #connection.commit()
    connection.close()
    return results

@app.route('/')
def index():
    return jsonify({'Vehicles Data': vehicles_data()})

@app.route("/api/sayHello")
def hello():
    return "Hello, Welcome to Vehicle Service"

if __name__ == '__main__':
    app.run(host='0.0.0.0')