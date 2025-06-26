# D:\DevOps - IBM\FinanceDashboard\database.py
import sqlite3
from datetime import datetime

# The default database name for the main application
DEFAULT_DB_NAME = 'finance_tracker.db'

def connect_db(db_name=DEFAULT_DB_NAME): # Allow overriding the db name
    """Establishes a connection to the SQLite database and returns the connection object."""
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_db(conn=None): # Accept an optional connection
    """Creates the 'transactions' table if it doesn't already exist."""
    close_conn = False
    if conn is None:
        conn = connect_db()
        close_conn = True

    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL CHECK(type IN ('Income', 'Expense')),
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            description TEXT,
            timestamp TEXT NOT NULL
        )
    ''')
    conn.commit()
    
    if close_conn:
        conn.close()

def add_transaction(type, category, amount, description, conn=None): # Accept an optional connection
    """Adds a new transaction record to the database."""
    close_conn = False
    if conn is None:
        conn = connect_db()
        close_conn = True

    cursor = conn.cursor()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('INSERT INTO transactions (type, category, amount, description, timestamp) VALUES (?, ?, ?, ?, ?)',
                   (type, category, amount, description, timestamp))
    conn.commit()
    
    if close_conn:
        conn.close()

# --- Other functions updated similarly ---

def get_all_transactions(conn=None):
    close_conn = False
    if conn is None:
        conn = connect_db()
        close_conn = True
    
    cursor = conn.cursor()
    cursor.execute('SELECT id, type, category, amount, description, timestamp FROM transactions ORDER BY id DESC')
    records = cursor.fetchall()
    
    if close_conn:
        conn.close()
    return records

def delete_transaction(transaction_id, conn=None):
    close_conn = False
    if conn is None:
        conn = connect_db()
        close_conn = True
    
    cursor = conn.cursor()
    cursor.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
    conn.commit()
    
    if close_conn:
        conn.close()

def get_financial_summary(conn=None):
    close_conn = False
    if conn is None:
        conn = connect_db()
        close_conn = True
        
    cursor = conn.cursor()
    query = "SELECT SUM(CASE WHEN type = 'Income' THEN amount ELSE 0 END) as total_income, SUM(CASE WHEN type = 'Expense' THEN amount ELSE 0 END) as total_expense FROM transactions"
    cursor.execute(query)
    result = cursor.fetchone()

    if close_conn:
        conn.close()

    total_income = result['total_income'] or 0.0
    total_expense = result['total_expense'] or 0.0
    balance = total_income - total_expense
    return {'income': total_income, 'expense': total_expense, 'balance': balance}
