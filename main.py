import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import database
import metrics
import csv

try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except ImportError:
    pass

class FinanceApp(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setup_styles()
        self.create_widgets()
        self.refresh_records()

    def setup_styles(self):
        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        self.colors = {"dark_blue": "#2c3e50", "light_gray": "#ecf0f1", "accent_blue": "#3498db", "white": "#ffffff", "green": "#2ecc71", "red": "#e74c3c"}
        self.style.configure("TFrame", background=self.colors['light_gray'])
        self.style.configure("Sidebar.TFrame", background=self.colors['dark_blue'])
        self.style.configure("TLabel", font=("Segoe UI", 11), background=self.colors['light_gray'], foreground=self.colors['dark_blue'])
        self.style.configure("Sidebar.TLabel", font=("Segoe UI", 11), background=self.colors['dark_blue'], foreground=self.colors['white'])
        self.style.configure("Sidebar.TLabelframe", background=self.colors['dark_blue'])
        self.style.configure("Sidebar.TLabelframe.Label", font=("Segoe UI", 13, "bold"), foreground=self.colors['white'], background=self.colors['dark_blue'])
        self.style.configure("Treeview", font=("Segoe UI", 10), rowheight=28)
        self.style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"), background=self.colors['accent_blue'], foreground=self.colors['white'])
        self.style.map("Treeview.Heading", background=[('active', self.colors['accent_blue'])])
        self.style.configure("ActionButton.TButton", font=("Segoe UI", 10, "bold"), padding=5)
        self.style.map("ActionButton.TButton", foreground=[('!active', self.colors['white']), ('active', self.colors['white'])], background=[('!active', self.colors['accent_blue']), ('active', '#2980b9')])
        self.style.configure("Success.TButton", font=("Segoe UI", 11, "bold"), padding=8, background=self.colors['green'], foreground=self.colors['white'])
        self.style.map("Success.TButton", background=[('active', '#27ae60')])
        self.style.configure("Danger.TButton", font=("Segoe UI", 10, "bold"), padding=5, background=self.colors['red'], foreground=self.colors['white'])
        self.style.map("Danger.TButton", background=[('active', '#c0392b')])

    def create_widgets(self):
        sidebar_frame = ttk.Frame(self, width=350, style="Sidebar.TFrame")
        sidebar_frame.pack(side="left", fill="y", padx=(0, 5), pady=0)
        sidebar_frame.pack_propagate(False)
        main_frame = ttk.Frame(self, style="TFrame")
        main_frame.pack(side="right", fill="both", expand=True, padx=5, pady=0)
        self._create_sidebar_widgets(sidebar_frame)
        self._create_main_content_widgets(main_frame)

    def _create_sidebar_widgets(self, parent):
        summary_frame = ttk.LabelFrame(parent, text="Dashboard Summary", style="Sidebar.TLabelframe")
        summary_frame.pack(pady=20, padx=20, fill="x")
        self.total_income_var, self.total_expense_var, self.balance_var = tk.StringVar(), tk.StringVar(), tk.StringVar()
        ttk.Label(summary_frame, textvariable=self.total_income_var, style="Sidebar.TLabel", font=("Segoe UI", 12, "bold"), foreground=self.colors['green']).pack(anchor="w", pady=5)
        ttk.Label(summary_frame, textvariable=self.total_expense_var, style="Sidebar.TLabel", font=("Segoe UI", 12, "bold"), foreground=self.colors['red']).pack(anchor="w", pady=5)
        ttk.Label(summary_frame, textvariable=self.balance_var, style="Sidebar.TLabel", font=("Segoe UI", 14, "bold"), foreground=self.colors['white']).pack(anchor="w", pady=10)
        input_frame = ttk.LabelFrame(parent, text="Add New Transaction", style="Sidebar.TLabelframe")
        input_frame.pack(pady=10, padx=20, fill="x")
        input_frame.columnconfigure(1, weight=1); input_frame.columnconfigure(2, weight=1)
        ttk.Label(input_frame, text="Type:", style="Sidebar.TLabel").grid(row=0, column=0, padx=5, pady=8, sticky="w")
        self.type_var = tk.StringVar(value="Expense")
        rb_style = ttk.Style(); rb_style.configure("Sidebar.TRadiobutton", background=self.colors['dark_blue'], foreground=self.colors['white'], font=("Segoe UI", 10))
        ttk.Radiobutton(input_frame, text="Expense", variable=self.type_var, value="Expense", style="Sidebar.TRadiobutton").grid(row=0, column=1, sticky="w")
        ttk.Radiobutton(input_frame, text="Income", variable=self.type_var, value="Income", style="Sidebar.TRadiobutton").grid(row=0, column=2, sticky="w")
        ttk.Label(input_frame, text="Category:", style="Sidebar.TLabel").grid(row=1, column=0, padx=5, pady=8, sticky="w")
        self.category_var = tk.StringVar()
        self.category_entry = ttk.Combobox(input_frame, textvariable=self.category_var, font=("Segoe UI", 11)); self.category_entry['values'] = ('Groceries', 'Rent', 'Salary', 'Entertainment', 'Transport', 'Bills', 'Other'); self.category_entry.grid(row=1, column=1, columnspan=2, padx=5, pady=8, sticky="ew")
        ttk.Label(input_frame, text="Amount:", style="Sidebar.TLabel").grid(row=2, column=0, padx=5, pady=8, sticky="w"); self.amount_entry = ttk.Entry(input_frame); self.amount_entry.grid(row=2, column=1, columnspan=2, padx=5, pady=8, sticky="ew")
        ttk.Label(input_frame, text="Description:", style="Sidebar.TLabel").grid(row=3, column=0, padx=5, pady=8, sticky="w"); self.desc_entry = ttk.Entry(input_frame); self.desc_entry.grid(row=3, column=1, columnspan=2, padx=5, pady=8, sticky="ew")
        add_button = ttk.Button(input_frame, text="✚ Add Transaction", command=self.add_record, style="Success.TButton"); add_button.grid(row=4, column=0, columnspan=3, pady=15, padx=5, sticky="ew")

    def _create_main_content_widgets(self, parent):
        actions_frame = ttk.Frame(parent, style="TFrame", padding=(0, 10)); actions_frame.pack(fill="x")
        ttk.Button(actions_frame, text="🔄 Refresh", command=self.refresh_records, style="ActionButton.TButton").pack(side="left", padx=5)
        ttk.Button(actions_frame, text="⬇️ Export to CSV", command=self.export_to_csv, style="ActionButton.TButton").pack(side="left", padx=5)
        ttk.Button(actions_frame, text="🗑️ Delete Selected", command=self.delete_record, style="Danger.TButton").pack(side="right", padx=5)
        records_frame = ttk.Frame(parent, style="TFrame"); records_frame.pack(fill="both", expand=True, pady=(5, 10))
        columns = ('id', 'type', 'category', 'amount', 'description', 'timestamp')
        self.tree = ttk.Treeview(records_frame, columns=columns, show='headings')
        self.tree.heading('id', text='ID'); self.tree.column('id', width=40, anchor='center')
        self.tree.heading('type', text='Type'); self.tree.column('type', width=80, anchor='center')
        self.tree.heading('category', text='Category'); self.tree.column('category', width=120)
        self.tree.heading('amount', text='Amount ($)'); self.tree.column('amount', width=100, anchor='e')
        self.tree.heading('description', text='Description'); self.tree.column('description', width=200)
        self.tree.heading('timestamp', text='Date'); self.tree.column('timestamp', width=150, anchor='center')
        scrollbar = ttk.Scrollbar(records_frame, orient="vertical", command=self.tree.yview); self.tree.configure(yscrollcommand=scrollbar.set); scrollbar.pack(side="right", fill="y"); self.tree.pack(fill="both", expand=True)
        self.tree.tag_configure('income_row', foreground=self.colors['green']); self.tree.tag_configure('expense_row', foreground=self.colors['red'])

    def add_record(self):
        ttype, category, amount_str, description = self.type_var.get(), self.category_var.get(), self.amount_entry.get(), self.desc_entry.get()
        if not all([ttype, category, amount_str]): return messagebox.showerror("Error", "Type, Category, and Amount are required.")
        try:
            amount = float(amount_str)
            if amount <= 0: return messagebox.showerror("Error", "Amount must be a positive number.")
        except ValueError: return messagebox.showerror("Error", "Amount must be a valid number.")
        database.add_transaction(ttype, category, amount, description); metrics.record_transaction_added(ttype)
        self.clear_form(); self.refresh_records(); messagebox.showinfo("Success", "Transaction added successfully.")

    def clear_form(self):
        self.category_var.set(''); self.amount_entry.delete(0, tk.END); self.desc_entry.delete(0, tk.END); self.type_var.set('Expense')

    def refresh_records(self):
        for item in self.tree.get_children(): self.tree.delete(item)
        summary = database.get_financial_summary()
        self.total_income_var.set(f"Income: ${summary['income']:,.2f}"); self.total_expense_var.set(f"Expense: ${summary['expense']:,.2f}"); self.balance_var.set(f"Balance: ${summary['balance']:,.2f}")
        for i, record in enumerate(database.get_all_transactions()):
            type_tag = 'income_row' if record['type'] == 'Income' else 'expense_row'
            self.tree.insert('', tk.END, values=(record['id'], record['type'], record['category'], f"{record['amount']:,.2f}", record['description'], record['timestamp'].split('.')[0]), tags=(type_tag,))

    def delete_record(self):
        if not (selected_item := self.tree.selection()): return messagebox.showerror("Error", "Please select a record to delete.")
        record_id, _, category, *_ = self.tree.item(selected_item[0])['values']
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete this transaction?\n\nID: {record_id} ({category})"):
            database.delete_transaction(record_id); self.refresh_records(); messagebox.showinfo("Success", "Record deleted.")

    def export_to_csv(self):
        records = database.get_all_transactions()
        if not records: return messagebox.showinfo("Info", "No data to export.")
        if filename := simpledialog.askstring("Export to CSV", "Enter filename:", parent=self.parent, initialvalue="transactions.csv"):
            if not filename.endswith('.csv'): filename += '.csv'
            try:
                with open(filename, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f); writer.writerow(['ID', 'Type', 'Category', 'Amount', 'Description', 'Timestamp']); writer.writerows(records)
                messagebox.showinfo("Success", f"Data successfully exported to {filename}"); metrics.record_export_click()
            except IOError as e: messagebox.showerror("Error", f"Could not export data: {e}")

if __name__ == "__main__":
    database.initialize_db()
    root = tk.Tk()
    root.title("Personal Finance Dashboard")
    root.geometry("1100x700")
    root.configure(bg="#ecf0f1")
    app = FinanceApp(root)
    app.pack(fill="both", expand=True)
    metrics.record_app_start()
    root.mainloop()