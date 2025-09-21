import sqlite3
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Connect to database (creates file if not exists)
conn = sqlite3.connect('students.db', check_same_thread=False)
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        department TEXT NOT NULL,
        email TEXT NOT NULL
    )
''')
conn.commit()

@app.route('/')
def index():
    c.execute("SELECT * FROM students")
    students = c.fetchall()
    return render_template("index.html", students=students)

@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    age = request.form['age']
    department = request.form['department']
    email = request.form['email']
    c.execute("INSERT INTO students (name, age, department, email) VALUES (?, ?, ?, ?)",
              (name, age, department, email))
    conn.commit()
    return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    c.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)