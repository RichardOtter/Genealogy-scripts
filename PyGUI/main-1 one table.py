import sqlite3
import tkinter as tk
from tkinter import messagebox

DB_PATH = "DB\\TEST-PyGUI.rmtree"
TABLE_NAME = "DNATable"

class SingleRecordByIDApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Record Viewer/Editor")

        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()

        # Load column names dynamically
        self.cursor.execute(f"PRAGMA table_info({TABLE_NAME})")
        self.columns = [col[1] for col in self.cursor.fetchall()]

        self.entries = {}
        self.current_id = None

        self.build_ui()

    def build_ui(self):
        # Row 0: ID input + Load button
        tk.Label(self.root, text="Record ID:", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5, pady=5)
        self.id_entry = tk.Entry(self.root, width=10)
        self.id_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Button(self.root, text="Load", command=self.load_by_id).grid(row=0, column=2, padx=5, pady=5)

        # Rows for each column
        for i, col_name in enumerate(self.columns, start=1):
            tk.Label(self.root, text=col_name, font=("Arial", 10, "bold")).grid(row=i, column=0, padx=5, pady=5)
            entry = tk.Entry(self.root, width=30)
            entry.grid(row=i, column=1, columnspan=2, padx=5, pady=5)
            self.entries[col_name] = entry

        # Save button
        tk.Button(self.root, text="Save Changes", command=self.save_record).grid(
            row=len(self.columns) + 1, column=0, columnspan=3, pady=10
        )

    def load_by_id(self):
        try:
            record_id = int(self.id_entry.get())
        except ValueError:
            messagebox.showerror("Invalid", "ID must be an integer")
            return

        self.cursor.execute(
            f"SELECT * FROM {TABLE_NAME} WHERE {self.columns[0]}=?",
            (record_id,)
        )
        row = self.cursor.fetchone()

        if row is None:
            messagebox.showerror("Not found", f"No record with ID {record_id}")
            return

        self.current_id = record_id

        # Populate fields
        for col_name, value in zip(self.columns, row):
            self.entries[col_name].delete(0, tk.END)
            self.entries[col_name].insert(0, str(value))

    def save_record(self):
        if self.current_id is None:
            messagebox.showerror("No record", "Load a record first")
            return

        values = [self.entries[col].get() for col in self.columns]
        set_clause = ", ".join([f"{col}=?" for col in self.columns[1:]])

        sql = f"UPDATE {TABLE_NAME} SET {set_clause} WHERE {self.columns[0]}=?"
        params = values[1:] + [self.current_id]

        self.cursor.execute(sql, params)
        self.conn.commit()
        messagebox.showinfo("Saved", "Record updated.")

    def __del__(self):
        self.conn.close()


if __name__ == "__main__":
    root = tk.Tk()
    app = SingleRecordByIDApp(root)
    root.mainloop()