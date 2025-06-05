from flask import Flask, render_template, request, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# MySQL Configuration
hostname = "i34nt.h.filess.io"
database = "loveletter_hatpoolsad"
port = "3307"
username = "loveletter_hatpoolsad"
password = "c7c224177f6cb2e6551e510bc8df435084fe3662"

db_config = {
    "host": hostname,
    "database": database,
    "user": username,
    "password": password,
    "port": port
}

try:
    connection = mysql.connector.connect(**db_config)
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

def insert_response(answer):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO responses (answer) VALUES (%s)", (answer,))
        conn.commit()
        cursor.close()
        conn.close()
        print(f"Saved response: {answer}")
    except Exception as e:
        print("Database error:", e)

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
