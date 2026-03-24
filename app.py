from flask import Flask, render_template, request, redirect
import psycopg2
import os
from datetime import datetime

app = Flask(__name__)

DATABASE_URL = os.environ.get('DATABASE_URL')

def get_conn():
    return psycopg2.connect(DATABASE_URL)

@app.route('/')
def index():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS moods (
            id   SERIAL PRIMARY KEY,
            mood TEXT,
            note TEXT,
            date TEXT
        )
    ''')
    conn.commit()
    cur.execute('SELECT mood, note, date FROM moods ORDER BY id DESC')
    moods = cur.fetchall()
    conn.close()
    return render_template('index.html', moods=moods)

@app.route('/save', methods=['POST'])
def save():
    mood = request.form['mood']
    note = request.form['note']
    date = datetime.now().strftime('%Y-%m-%d %H:%M')

    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO moods (mood, note, date) VALUES (%s, %s, %s)',
        (mood, note, date)
    )
    conn.commit()
    conn.close()

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
```

---

**requirements.txt**
```
flask
psycopg2-binary