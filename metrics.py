import statsd

c = statsd.StatsClient(host='localhost', port=8125, prefix='finance_app')

def record_transaction_added(ttype):
    """Increment counters for transactions."""
    c.incr('transactions.total')
    if ttype == 'Expense':
        c.incr('transactions.expense')
    else:
        c.incr('transactions.income')

def record_export_click():
    """Increment counter for export clicks."""
    c.incr('ui.export_clicks')

def record_app_start():
    """Record that the application has started a new session."""
    c.incr('sessions.started')