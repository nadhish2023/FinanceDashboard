# tests/test_database.py
import pytest
import sqlite3
import database # Your database module

@pytest.fixture
def test_conn():
    """
    A pytest fixture that creates and yields a connection to a fresh, 
    in-memory database, and initializes the schema.
    """
    # 1. Create a connection to an in-memory database
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row

    # 2. Initialize the table structure using this specific connection
    database.initialize_db(conn=conn)
    
    # 3. Yield the connection to the test function
    yield conn
    
    # 4. Cleanup: close the connection after the test is done
    conn.close()

def test_add_and_get(test_conn):
    """Tests that a transaction can be added and retrieved using the test connection."""
    # Pass the test_conn fixture into the database function
    database.add_transaction("Expense", "Test Category", 100, "A test transaction", conn=test_conn)
    
    records = database.get_all_transactions(conn=test_conn)
    assert len(records) == 1
    assert records[0]['category'] == "Test Category"

def test_summary_calculation(test_conn):
    """Tests that the financial summary is calculated correctly using the test connection."""
    # Pass the test_conn fixture into all database functions
    database.add_transaction("Income", "Salary", 2000, "", conn=test_conn)
    database.add_transaction("Expense", "Rent", 800, "", conn=test_conn)
    database.add_transaction("Expense", "Groceries", 200, "", conn=test_conn)
    
    summary = database.get_financial_summary(conn=test_conn)
    assert summary['income'] == 2000
    assert summary['expense'] == 1000
    assert summary['balance'] == 1000
