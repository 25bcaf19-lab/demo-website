from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('database.db')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS moods (
            id   INTEGER PRIMARY KEY AUTOINCREMENT,
            mood TEXT,
            note TEXT,
            date TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    moods = conn.execute(
        'SELECT mood, note, date FROM moods ORDER BY id DESC'
    ).fetchall()
    conn.close()
    return render_template('index.html', moods=moods)

@app.route('/save', methods=['POST'])
def save():
    mood = request.form['mood']
    note = request.form['note']
    date = datetime.now().strftime('%Y-%m-%d %H:%M')

    conn = sqlite3.connect('database.db')
    conn.execute(
        'INSERT INTO moods (mood, note, date) VALUES (?, ?, ?)',
        (mood, note, date)
    )
    conn.commit()
    conn.close()

    return redirect('/confirmation')  # ← fixed

@app.route('/confirmation')  # ← new route
def confirmation():
    return render_template('confirmation.html')

if __name__ == '__main__':
    app.run(debug=True)