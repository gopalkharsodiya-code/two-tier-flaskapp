import os
from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configure MySQL from environment variables
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD', 'password')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB', 'testdb')

# Initialize MySQL
mysql = MySQL(app)

# Create table if not exists
def init_db():
    with app.app_context():
        cur = mysql.connection.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INT AUTO_INCREMENT PRIMARY KEY,
                message TEXT
            );
        """)
        mysql.connection.commit()
        cur.close()

# Home route
@app.route('/')
def home():
    try:
        cur = mysql.connection.cursor()
        cur.execute('SELECT message FROM messages')
        messages = cur.fetchall()
        cur.close()
    except Exception as e:
        print("DB Error:", e)
        messages = []

    return render_template('index.html', messages=messages)

# Submit message
@app.route('/submit', methods=['POST'])
def submit():
    new_message = request.form.get('new_message')

    if not new_message:
        return jsonify({'error': 'Message cannot be empty'}), 400

    try:
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO messages (message) VALUES (%s)', [new_message])
        mysql.connection.commit()
        cur.close()
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'message': new_message})

# Run app
if __name__ == '__main__':
    init_db()
    print("Login feature added")   # ✅ your line
    app.run(host='0.0.0.0', port=5000, debug=True)
