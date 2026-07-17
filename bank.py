
# === PART 1 ===

import os
import csv
from tkinter import *
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import matplotlib.pyplot as plt

DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "transactions.csv")
REPORT_FILE = os.path.join(DATA_DIR, "report.txt")

os.makedirs(DATA_DIR, exist_ok=True)


class FinanceApp:

    def __init__(self, root):

        self.root = root
        self.root.title("Personal Finance Manager")
        self.root.geometry("1200x700")
        self.root.configure(bg="#1e1e1e")
        self.root.resizable(False, False)

        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Treeview",
            background="#2b2b2b",
            foreground="white",
            fieldbackground="#2b2b2b",
            rowheight=28
        )

        style.configure(
            "Treeview.Heading",
            background="#3b82f6",
            foreground="white",
            font=("Segoe UI", 11, "bold")
        )

        title = Label(
            root,
            text="💰 Personal Finance Manager",
            bg="#1e1e1e",
            fg="white",
            font=("Segoe UI", 22, "bold")
        )

        title.pack(pady=15)

        form = Frame(root, bg="#1e1e1e")
        form.pack(fill="x", padx=20)

        Label(
            form,
            text="Type",
            bg="#1e1e1e",
            fg="white",
            font=("Segoe UI", 11)
        ).grid(row=0, column=0, padx=10, pady=10)

        self.type_box = ttk.Combobox(
            form,
            values=["income", "expense"],
            width=18,
            state="readonly"
        )

        self.type_box.current(0)
        self.type_box.grid(row=0, column=1)

        Label(
            form,
            text="Amount",
            bg="#1e1e1e",
            fg="white",
            font=("Segoe UI", 11)
        ).grid(row=0, column=2, padx=10)

        self.amount_entry = Entry(form, width=20)
        self.amount_entry.grid(row=0, column=3)

        Label(
            form,
            text="Category",
            bg="#1e1e1e",
            fg="white",
            font=("Segoe UI", 11)
        ).grid(row=1, column=0, pady=10)

        self.category_entry = Entry(form, width=20)
        self.category_entry.grid(row=1, column=1)

        Label(
            form,
            text="Date",
            bg="#1e1e1e",
            fg="white",
            font=("Segoe UI", 11)
        ).grid(row=1, column=2)

        self.date_entry = Entry(form, width=20)
        self.date_entry.insert(
            0,
            datetime.today().strftime("%Y-%m-%d")
        )
        self.date_entry.grid(row=1, column=3)

        button_frame = Frame(root, bg="#1e1e1e")
        button_frame.pack(pady=15)

        Button(
            button_frame,
            text="Add",
            bg="#16a34a",
            fg="white",
            width=12,
            command=self.add_transaction
        ).grid(row=0, column=0, padx=5)

        Button(
            button_frame,
            text="Refresh",
            bg="#2563eb",
            fg="white",
            width=12,
            command=self.load_table
        ).grid(row=0, column=1, padx=5)

        Button(
            button_frame,
            text="Summary",
            bg="#9333ea",
            fg="white",
            width=12,
            command=self.summary
        ).grid(row=0, column=2, padx=5)

        Button(
            button_frame,
            text="Filter",
            bg="#f59e0b",
            fg="black",
            width=12,
            command=self.filter_window
        ).grid(row=0, column=3, padx=5)

        Button(
            button_frame,
            text="Chart",
            bg="#0ea5e9",
            fg="white",
            width=12,
            command=self.chart
        ).grid(row=0, column=4, padx=5)

        Button(
            button_frame,
            text="Report",
            bg="#ef4444",
            fg="white",
            width=12,
            command=self.save_report
        ).grid(row=0, column=5, padx=5)

        Button(
            button_frame,
            text="Delete",
            bg="#dc2626",
            fg="white",
            width=12,
            command=self.delete_transaction
        ).grid(row=0, column=6, padx=5)

        table_frame = Frame(root)
        table_frame.pack(fill="both", expand=True, padx=20)

        columns = (
            "Type",
            "Amount",
            "Category",
            "Date"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=15
        )

        for c in columns:
            self.tree.heading(c, text=c)
            self.tree.column(
                c,
                anchor=CENTER,
                width=250
            )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient=VERTICAL,
            command=self.tree.yview
        )

        self.tree.configure(
            yscrollcommand=scrollbar.set
        )

        self.tree.pack(
            side=LEFT,
            fill=BOTH,
            expand=True
        )

        scrollbar.pack(
            side=RIGHT,
            fill=Y
        )

        bottom = Frame(root, bg="#1e1e1e")
        bottom.pack(fill="x")

        self.income_label = Label(
            bottom,
            text="Income : 0",
            bg="#1e1e1e",
            fg="#22c55e",
            font=("Segoe UI", 12, "bold")
        )

        self.income_label.pack(
            side=LEFT,
            padx=20,
            pady=15
        )

        self.expense_label = Label(
            bottom,
            text="Expense : 0",
            bg="#1e1e1e",
            fg="#ef4444",
            font=("Segoe UI", 12, "bold")
        )

        self.expense_label.pack(
            side=LEFT,
            padx=20
        )

        self.balance_label = Label(
            bottom,
            text="Balance : 0",
            bg="#1e1e1e",
            fg="#38bdf8",
            font=("Segoe UI", 12, "bold")
        )

        self.balance_label.pack(
            side=LEFT,
            padx=20
        )

        self.create_file()

        self.load_table()

    def create_file(self):

        if not os.path.exists(DATA_FILE):

            with open(
                DATA_FILE,
                "w",
                newline="",
                encoding="utf-8"
            ) as f:

                writer = csv.writer(f)

                writer.writerow(
                    [
                        "type",
                        "amount",
                        "category",
                        "date"
                    ]
                )

    def add_transaction(self):

        t = self.type_box.get()

        amount = self.amount_entry.get()

        category = self.category_entry.get()

        date = self.date_entry.get()

        if amount == "" or category == "" or date == "":

            messagebox.showerror(
                "Error",
                "Fill all fields."
            )

            return

        try:

            amount = float(amount)

        except:

            messagebox.showerror(
                "Error",
                "Amount must be numeric."
            )

            return

        with open(
            DATA_FILE,
            "a",
            newline="",
            encoding="utf-8"
        ) as f:

            writer = csv.writer(f)

            writer.writerow(
                [
                    t,
                    amount,
                    category,
                    date
                ]
            )

        self.amount_entry.delete(0, END)

        self.category_entry.delete(0, END)

        self.date_entry.delete(0, END)

        self.date_entry.insert(
            0,
            datetime.today().strftime("%Y-%m-%d")
        )

        self.load_table()

        messagebox.showinfo(
            "Done",
            "Transaction Added."
        )

    def read_data(self):

        data = []

        with open(
            DATA_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            reader = csv.DictReader(f)

            for row in reader:

                row["amount"] = float(row["amount"])

                data.append(row)

        return data

    def load_table(self):

        for item in self.tree.get_children():

            self.tree.delete(item)

        data = self.read_data()

        income = 0

        expense = 0

        for row in data:

            self.tree.insert(
                "",
                END,
                values=(
                    row["type"],
                    f'{row["amount"]:.2f}',
                    row["category"],
                    row["date"]
                )
            )

            if row["type"] == "income":

                income += row["amount"]

            else:

                expense += row["amount"]

        self.income_label.config(
            text=f"Income : {income:.2f}"
        )

        self.expense_label.config(
            text=f"Expense : {expense:.2f}"
        )

        self.balance_label.config(
            text=f"Balance : {income-expense:.2f}"
        )

