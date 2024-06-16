from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Initialize the database
def initialize_database():
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT NOT NULL,
        activity TEXT NOT NULL,
        time TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

initialize_database()

@app.route('/')
def index():
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    user = request.form['user']
    activity = request.form['activity']
    time = request.form['time']
    
    if user and activity and time:
        conn = sqlite3.connect('todo.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO tasks (user, activity, time) VALUES (?, ?, ?)', (user, activity, time))
        conn.commit()
        conn.close()
    
    return redirect(url_for('index'))

@app.route('/clear', methods=['POST'])
def clear_tasks():
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tasks')
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
