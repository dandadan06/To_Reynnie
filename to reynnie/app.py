from flask import Flask, render_template, request, jsonify
import mysql.connector
from twilio.rest import Client

app = Flask(__name__)

# MySQL Configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # Default for XAMPP
    'database': 'love_letter'
}

# Twilio Configuration (replace these with your actual Twilio credentials)
account_sid = 'AC2d6bbd6741d764c34adf4dd4f45435d4'
auth_token = '39c238d50df828f2f0c293e0504224a7'
twilio_number = '+639602618779'  # Your Twilio number
your_number = '+639363639838'  # Your personal number

twilio_client = Client(account_sid, auth_token)

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

def send_sms(answer):
    try:
        message = twilio_client.messages.create(
            body=f"She answered: {answer.upper()} ❤️",
            from_=twilio_number,
            to=your_number
        )
        print("SMS sent:", message.sid)
    except Exception as e:
        print("SMS error:", e)

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
        send_sms(answer)
        return jsonify({'redirect': f'/{answer}'})
    
    return jsonify({'error': 'Invalid response'}), 400

if __name__ == '__main__':
    app.run(debug=True)
