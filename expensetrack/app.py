import csv
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox
from datetime import datetime, timedelta

# File to store expenses
FILE_NAME = 'expenses.csv'

# Function to initialize file
def initialize_file():
    try:
        with open(FILE_NAME, 'x', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Date', 'Category', 'Amount', 'Description'])
    except FileExistsError:
        pass

# Function to add a new expense
def add_expense():
    date = datetime.now().strftime('%Y-%m-%d')
    category = category_var.get()
    amount = amount_var.get()
    description = description_var.get()

    if not category or not amount or not description:
        messagebox.showwarning("Warning", "Please fill all fields.")
        return
    
    try:
        with open(FILE_NAME, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([date, category, float(amount), description])
        messagebox.showinfo("Success", "Expense added successfully!")
        clear_fields()
        view_expenses()
    except ValueError:
        messagebox.showerror("Error", "Invalid amount entered.")

# Function to clear fields
def clear_fields():
    category_var.set('')
    amount_var.set('')
    description_var.set('')

# Function to view all expenses
def view_expenses():
    for row in tree.get_children():
        tree.delete(row)
    try:
        with open(FILE_NAME, 'r') as file:
            reader = csv.reader(file)
            try:
                header = next(reader)  # Skip header if present
                for row in reader:
                    tree.insert('', END, values=row)
            except StopIteration:
                pass  # File exists but is empty
    except FileNotFoundError:
        pass

# Function to generate report
def generate_report(period):
    try:
        total_spent = 0.0
        cutoff_date = None
        today = datetime.now()

        if period == 'day':
            cutoff_date = today
        elif period == 'week':
            cutoff_date = today - timedelta(days=7)
        elif period == 'month':
            cutoff_date = today.replace(day=1)
        elif period == 'year':
            cutoff_date = today.replace(month=1, day=1)

        with open(FILE_NAME, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header

            for row in reader:
                # Ensure row has at least 3 columns (Date, Category, Amount)
                if len(row) < 3:
                    continue  # Skip incomplete rows
                row_date = datetime.strptime(row[0], '%Y-%m-%d')
                if row_date >= cutoff_date:
                    total_spent += float(row[2])

        messagebox.showinfo("Report", f"Total spent in the {period}: Rs {total_spent:.2f}")
    except FileNotFoundError:
        messagebox.showerror("Error", "No expense file found.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


# Initialize file
initialize_file()

# Main GUI application
root = tb.Window(themename="superhero")
root.title("Expense Tracker")
root.geometry("900x500")
root.resizable(False, False)

# Frame for input fields
input_frame = tb.Frame(root, padding=(10, 10))
input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

# Input fields
tb.Label(input_frame, text="Category:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
category_var = tb.StringVar()
category_entry = tb.Entry(input_frame, textvariable=category_var, width=30)
category_entry.grid(row=0, column=1, padx=5, pady=5)


tb.Label(input_frame, text="Amount:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
amount_var = tb.StringVar()
amount_entry = tb.Entry(input_frame, textvariable=amount_var, width=30)
amount_entry.grid(row=1, column=1, padx=5, pady=5)


tb.Label(input_frame, text="Description:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
description_var = tb.StringVar()
description_entry = tb.Entry(input_frame, textvariable=description_var, width=30)
description_entry.grid(row=2, column=1, padx=5, pady=5)

# Buttons
button_frame = tb.Frame(root, padding=(10, 10))
button_frame.grid(row=1, column=0, sticky="ew")

add_button = tb.Button(button_frame, text="Add Expense", command=add_expense, bootstyle="success")
add_button.grid(row=0, column=0, padx=10, pady=10)

clear_button = tb.Button(button_frame, text="Clear Fields", command=clear_fields, bootstyle="warning")
clear_button.grid(row=0, column=1, padx=10, pady=10)

report_button = tb.Menubutton(button_frame, text="Generate Report", bootstyle="info")
report_menu = tb.Menu(report_button, tearoff=0)
report_button['menu'] = report_menu
report_menu.add_command(label="Daily Report", command=lambda: generate_report('day'))
report_menu.add_command(label="Weekly Report", command=lambda: generate_report('week'))
report_menu.add_command(label="Monthly Report", command=lambda: generate_report('month'))
report_menu.add_command(label="Yearly Report", command=lambda: generate_report('year'))
report_button.grid(row=0, column=2, padx=10, pady=10)

# Expense list (Treeview)
tree_frame = tb.Frame(root, padding=(10, 10))
tree_frame.grid(row=2, column=0, sticky="nsew")

columns = ('Date', 'Category', 'Amount', 'Description')
tree = tb.Treeview(tree_frame, columns=columns, show='headings', bootstyle="info")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor=CENTER, width=200)

scrollbar = tb.Scrollbar(tree_frame, orient=VERTICAL, command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side=RIGHT, fill=Y)
tree.pack(fill=BOTH, expand=True)

# Load initial data
view_expenses()

# Run the application
root.mainloop()
