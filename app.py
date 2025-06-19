from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'my_secret_key'  # For flash messages

DATABASE = 'database.db'

# ---------- Database Utilities ----------

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # to access columns by name
    return conn

def init_db():
    if not os.path.exists(DATABASE):
        conn = get_db_connection()
        conn.execute('''
            CREATE TABLE tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

# ---------- Routes ----------

@app.route('/')
def index():
    conn = get_db_connection()
    tasks = conn.execute('SELECT * FROM tasks').fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    content = request.form['content'].strip()
    if content:
        conn = get_db_connection()
        conn.execute('INSERT INTO tasks (content) VALUES (?)', (content,))
        conn.commit()
        conn.close()
        flash('Task added successfully!', 'success')
    else:
        flash('Please enter a valid task.', 'warning')
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete(task_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    flash('Task deleted!', 'info')
    return redirect(url_for('index'))

# ---------- Main ----------
if __name__ == '__main__':
    init_db()
    app.run(debug=True)

