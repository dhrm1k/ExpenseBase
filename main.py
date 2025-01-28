import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from database import init_db, add_expense, get_expenses, delete_expense  # Add delete_expense function
from analytics import calculate_total, category_breakdown

# Initialize the database
init_db()

class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ExpenseBase")
        self.root.geometry("600x400")

        # Create GUI sections
        self.create_form_frame()
        self.create_table_frame()
        self.create_stats_frame()

        # Refresh table and stats on startup
        self.refresh_table()
        self.refresh_stats()

    def create_form_frame(self):
        """Creates the form for adding expenses."""
        frame = ttk.LabelFrame(self.root, text="Add Expense")
        frame.pack(fill="x", padx=10, pady=5)

        # Form fields
        ttk.Label(frame, text="Date:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.date_entry = DateEntry(frame, date_pattern="yyyy-mm-dd")  # Date picker widget
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Category:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.category_entry = ttk.Entry(frame)
        self.category_entry.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(frame, text="Amount:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.amount_entry = ttk.Entry(frame)
        self.amount_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Description:").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.description_entry = ttk.Entry(frame)
        self.description_entry.grid(row=1, column=3, padx=5, pady=5)

        # Add Expense button
        add_button = ttk.Button(frame, text="Add Expense", command=self.add_expense)
        add_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Delete Expense button
        delete_button = ttk.Button(frame, text="Delete Selected Expense", command=self.delete_selected_expense)
        delete_button.grid(row=2, column=2, columnspan=2, pady=10)

    def create_table_frame(self):
        """Creates the table to display expenses."""
        frame = ttk.LabelFrame(self.root, text="Expenses")
        frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Treeview for table
        self.tree = ttk.Treeview(frame, columns=("ID", "Date", "Category", "Amount", "Description"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Amount", text="Amount")
        self.tree.heading("Description", text="Description")
        self.tree.column("ID", width=50)  # Make the ID column narrower
        self.tree.pack(fill="both", expand=True)

        # Scrollbar
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

    def create_stats_frame(self):
        """Creates the stats section."""
        frame = ttk.LabelFrame(self.root, text="Statistics")
        frame.pack(fill="x", padx=10, pady=5)

        # Total label
        self.total_label = ttk.Label(frame, text="Total Expenses: 0")
        self.total_label.pack(anchor="w", padx=10, pady=5)

        # Breakdown label
        self.breakdown_label = ttk.Label(frame, text="Category Breakdown:")
        self.breakdown_label.pack(anchor="w", padx=10, pady=5)

    def add_expense(self):
        """Adds a new expense to the database and refreshes the table and stats."""
        date = self.date_entry.get()
        category = self.category_entry.get()
        amount = self.amount_entry.get()
        description = self.description_entry.get()

        # Validate inputs
        if not date or not category or not amount:
            messagebox.showerror("Error", "Please fill in all required fields!")
            return

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Error", "Amount must be a number!")
            return

        # Add to database
        add_expense(date, category, amount, description)
        messagebox.showinfo("Success", "Expense added successfully!")

        # Clear form and refresh
        self.category_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)
        self.refresh_table()
        self.refresh_stats()

    def delete_selected_expense(self):
        """Deletes the selected expense from the database."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No expense selected!")
            return

        # Get the selected expense ID
        expense_id = self.tree.item(selected_item)["values"][0]

        # Confirm deletion
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete expense ID {expense_id}?")
        if not confirm:
            return

        # Delete from database
        delete_expense(expense_id)
        messagebox.showinfo("Success", f"Expense ID {expense_id} deleted successfully!")

        # Refresh table and stats
        self.refresh_table()
        self.refresh_stats()

    def refresh_table(self):
        """Refreshes the expense table with the latest data."""
        # Clear existing rows
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Add rows from database
        expenses = get_expenses()
        for expense in expenses:
            self.tree.insert("", "end", values=expense)

    def refresh_stats(self):
        """Refreshes the stats section with the latest data."""
        expenses = get_expenses()
        total = calculate_total(expenses)
        breakdown = category_breakdown(expenses)

        # Update labels
        self.total_label.config(text=f"Total Expenses: {total}")
        breakdown_text = ", ".join([f"{k}: {v}" for k, v in breakdown.items()])
        self.breakdown_label.config(text=f"Category Breakdown: {breakdown_text}")

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()

