from flask import Flask, render_template, request, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# MySQL Configuration
import mysql.connector
from mysql.connector import Error

hostname = "i34nt.h.filess.io"
database = "loveletter_hatpoolsad"
port = "3307"
username = "loveletter_hatpoolsad"
password = "c7c224177f6cb2e6551e510bc8df435084fe3662"

try:
    connection = mysql.connector.connect(host=hostname, database=database, user=username, password=password, port=port)
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)

except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")



@app.route('/')
def home():
    return render_template('index.html')

@app.route('/yes')
def yes():
    return render_template('yes.html')

@app.route('/no')
def no():
    return render_template('no.html')

@app.route('/send-sms', methods=['POST'])
def handle_response():
    data = request.get_json()
    answer = data.get('response')
    
    if answer in ['yes', 'no']:
        insert_response(answer)
        return jsonify({'redirect': f'/{answer}'})
    
    return jsonify({'error': 'Invalid response'}), 400

if __name__ == '__main__':
    app.run(debug=True)
