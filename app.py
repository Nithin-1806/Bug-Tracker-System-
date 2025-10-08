from flask import Flask, render_template, request, redirect, session, url_for
import mysql.connector
from config import DB_CONFIG
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database connection
db = mysql.connector.connect(**DB_CONFIG)
cursor = db.cursor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, password))
        db.commit()
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user and check_password_hash(user[3], password):
            session['user_id'] = user[0]
            session['user_name'] = user[1]
            return redirect(url_for('dashboard'))
        else:
            return "Invalid email or password!"
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    cursor.execute("SELECT * FROM bugs")
    bugs = cursor.fetchall()
    return render_template('dashboard.html', bugs=bugs)

@app.route('/add_bug', methods=['GET', 'POST'])
def add_bug():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        cursor.execute("INSERT INTO bugs (title, description, assigned_to, status) VALUES (%s, %s, %s, %s)", 
                       (title, description, session['user_id'], 'Open'))
        db.commit()
        return redirect(url_for('dashboard'))
    
    return render_template('add_bug.html')

@app.route('/view_bug/<int:bug_id>')
def view_bug(bug_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    cursor.execute("SELECT * FROM bugs WHERE id = %s", (bug_id,))
    bug = cursor.fetchone()
    
    if not bug:
        return "Bug not found!"
    
    return render_template('view_bug.html', bug=bug)

# **NEW**: Update Bug Status
@app.route('/update_bug_status/<int:bug_id>', methods=['POST'])
def update_bug_status(bug_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    new_status = request.form['status']

    cursor.execute("UPDATE bugs SET status = %s WHERE id = %s", (new_status, bug_id))
    db.commit()
    
    return redirect(url_for('view_bug', bug_id=bug_id))

# **NEW**: Edit Bug
@app.route('/edit_bug/<int:bug_id>', methods=['GET', 'POST'])
def edit_bug(bug_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    cursor.execute("SELECT * FROM bugs WHERE id = %s", (bug_id,))
    bug = cursor.fetchone()

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        cursor.execute("UPDATE bugs SET title = %s, description = %s WHERE id = %s", (title, description, bug_id))
        db.commit()
        return redirect(url_for('dashboard'))

    return render_template('edit_bug.html', bug=bug)

# **NEW**: Delete Bug
@app.route('/delete_bug/<int:bug_id>', methods=['POST'])
def delete_bug(bug_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    cursor.execute("DELETE FROM bugs WHERE id = %s", (bug_id,))
    db.commit()
    
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
