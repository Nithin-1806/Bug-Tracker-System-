import mysql.connector
from config import DB_CONFIG

db = mysql.connector.connect(**DB_CONFIG)
cursor = db.cursor()

def create_tables():
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(100), email VARCHAR(100) UNIQUE, password VARCHAR(255))")
    cursor.execute("CREATE TABLE IF NOT EXISTS bugs (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(255), description TEXT, status ENUM('Open', 'In Progress', 'Resolved') DEFAULT 'Open', created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, assigned_to INT, FOREIGN KEY (assigned_to) REFERENCES users(id))")
    db.commit()

create_tables()
