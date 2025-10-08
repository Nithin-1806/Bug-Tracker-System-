from flask import Flask, render_template, request, redirect, session
import mysql.connector
from config import DB_CONFIG

app = Flask(__name__)
app.secret_key = 'your_secret_key'

db = mysql.connector.connect(**DB_CONFIG)
cursor = db.cursor()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    cursor.execute("SELECT * FROM bugs")
    bugs = cursor.fetchall()
    return render_template('dashboard.html', bugs=bugs)

@app.route('/add_bug', methods=['GET', 'POST'])
def add_bug():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        cursor.execute("INSERT INTO bugs (title, description) VALUES (%s, %s)", (title, description))
        db.commit()
        return redirect('/dashboard')
    return render_template('add_bug.html')

@app.route('/view_bug/<int:bug_id>')
def view_bug(bug_id):
    cursor.execute("SELECT * FROM bugs WHERE id = %s", (bug_id,))
    bug = cursor.fetchone()
    return render_template('view_bug.html', bug=bug)

if __name__ == '__main__':
    app.run(debug=True)
