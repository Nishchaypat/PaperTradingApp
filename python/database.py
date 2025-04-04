import sqlite3

DB_FILE = "trading_app.db"

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    # Create users table if not exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            email TEXT PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            password TEXT
        )
    """)
    # Create trades table if not exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS trades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT,
            action TEXT,
            symbol TEXT,
            quantity INTEGER,
            price REAL,
            total REAL,
            date TEXT,
            FOREIGN KEY (user_email) REFERENCES users(email)
        )
    """)
    conn.commit()
    conn.close()

def add_user(first_name, last_name, email, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO users (email, first_name, last_name, password)
            VALUES (?, ?, ?, ?)
        """, (email, first_name, last_name, password))
        conn.commit()
        print(f"User {email} added successfully")
        return True
    except sqlite3.IntegrityError as e:
        print(f"Failed to add user {email}: {e}")
        return False
    finally:
        conn.close()

def add_trade(user_email, action, symbol, quantity, price, total, date):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO trades (user_email, action, symbol, quantity, price, total, date)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (user_email, action, symbol, quantity, price, total, date))
    conn.commit()
    conn.close()

def verify_user(email, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
    user = cursor.fetchone()
    conn.close()
    return user is not None
