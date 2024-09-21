from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL,
            phone TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['POST'])
def signup():
    name = request.form['name']
    age = request.form['age']
    gender = request.form['gender']
    phone = request.form['phone']

    conn = get_db_connection()
    conn.execute('INSERT INTO members (name, age, gender, phone) VALUES (?, ?, ?, ?)',
                 (name, age, gender, phone))
    conn.commit()
    conn.close()

    return render_template('index.html', show_modal=True)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        admin_password = request.form['adminPassword']
        if admin_password == '2006':
            return render_template('admin.html', members=get_members())
        else:
            return redirect(url_for('index'))  # 비밀번호가 틀리면 다시 홈으로

    return redirect(url_for('index'))

def get_members():
    conn = get_db_connection()
    members = conn.execute('SELECT * FROM members').fetchall()
    conn.close()
    return members

if __name__ == '__main__':
    create_table()
    app.run(debug=False, port='80', host='0.0.0.0')
