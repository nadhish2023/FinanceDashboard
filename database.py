import sqlite3
from datetime import datetime

DB_NAME = 'finance_tracker.db'

def connect_db():
    """Establishes a connection to the SQLite database and returns the connection object."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_db():
    """Creates the 'transactions' table if it doesn't already exist."""
    conn = connect_db()
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
    conn.close()

def add_transaction(type, category, amount, description):
    """Adds a new transaction record to the database."""
    conn = connect_db()
    cursor = conn.cursor()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('INSERT INTO transactions (type, category, amount, description, timestamp) VALUES (?, ?, ?, ?, ?)',
                   (type, category, amount, description, timestamp))
    conn.commit()
    conn.close()

def get_all_transactions():
    """Retrieves all transaction records, ordered by most recent."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT id, type, category, amount, description, timestamp FROM transactions ORDER BY id DESC')
    records = cursor.fetchall()
    conn.close()
    return records

def delete_transaction(transaction_id):
    """Deletes a specific transaction by its ID."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
    conn.commit()
    conn.close()

def get_financial_summary():
    """Calculates total income, total expense, and balance with a single, efficient query."""
    conn = connect_db()
    cursor = conn.cursor()
    query = """
    SELECT
        SUM(CASE WHEN type = 'Income' THEN amount ELSE 0 END) as total_income,
        SUM(CASE WHEN type = 'Expense' THEN amount ELSE 0 END) as total_expense
    FROM transactions
    """
    cursor.execute(query)
    result = cursor.fetchone()
    conn.close()

    total_income = result['total_income'] or 0.0
    total_expense = result['total_expense'] or 0.0
    balance = total_income - total_expense

    return {'income': total_income, 'expense': total_expense, 'balance': balance}

# Ensure the database and table exist when the application starts
initialize_db()