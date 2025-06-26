# healthcheck.py
import database
import time
import sys

print("Health check script starting up...")
sys.stdout.flush() # This forces the print statement to appear immediately in logs

try:
    summary = database.get_financial_summary()
    print("Successfully retrieved financial summary.")
    print(f"Current Balance: {summary['balance']}")
    print("Health check successful. Container is operational.")
    print("Application would run here. Keeping container alive for demonstration...")
    sys.stdout.flush()

    # Loop forever to keep the container running
    while True:
        time.sleep(60)
        
except Exception as e:
    print(f"Health check FAILED: {e}")
    sys.stdout.flush()
    exit(1) # Exit with a non-zero error code
