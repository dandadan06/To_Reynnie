from flask import Flask, render_template, request, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# MySQL Configuration
hostname = "i34nt.h.filess.io"
database = "loveletter_hatpoolsad"
port = 3307  # port as int
username = "loveletter_hatpoolsad"
password = "c7c224177f6cb2e6551e510bc8df435084fe3662"

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=hostname,
            database=database,
            user=username,
            password=password,
            port=port
        )
        return connection
    except Error as e:
        print("Error connecting to MySQL", e)
        return None

def insert_response(answer):
    connection = get_db_connection()
    if connection is None:
        print("DB connection failed")
        return False
    try:
        cursor = connection.cursor()
        # Adjust the table and column names to your actual schema
        sql = "INSERT INTO responses (answer) VALUES (%s)"
        cursor.execute(sql, (answer,))
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except Error as e:
        print("Failed to insert response:", e)
        return False

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
        success = insert_response(answer)
        if success:
            return jsonify({'redirect': f'/{answer}'})
        else:
            return jsonify({'error': 'Database error'}), 500
    
    return jsonify({'error': 'Invalid response'}), 400

if __name__ == '__main__':
    app.run(debug=True)
