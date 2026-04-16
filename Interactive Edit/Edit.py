import sqlite3
import re
import tkinter as tk
from tkinter import ttk, messagebox

# ---------------- CONFIG ----------------

DB_PATH = r"C:\Users\rotter\dev\Genealogy\repo Genealogy-scripts\Misc SQL\DB\TEST-Misc SQL.rmtree"

SQL_QUERY = """
SELECT
   ct.CitationID,
   ct.ActualText
FROM CitationTable AS ct
INNER JOIN SourceTable AS st ON ct.SourceID = st.SourceID
WHERE st.Name LIKE 'RRdb MYH Mem-Tr%'
ORDER BY ct.CitationID ASC
"""

TARGET_COL = "ActualText"
KEY_COL = "CitationID"
TABLE_NAME = "CitationTable"

# List of regex rules: (pattern, replacement, flags)
REGEX_RULES = [
    (r"You are not a memberRequest membership", "", 0)
]

# ----------------------------------------


class RegexEditorApp:
    def __init__(self, master):
        self.master = master
        master.title("SQLite Regex Editor")

        self.conn = sqlite3.connect(DB_PATH)
        self.conn.row_factory = sqlite3.Row
        self.rows = self.load_rows()
        self.index = 0
        self.apply_to_all = False

        self.create_widgets()
        self.show_next_record()

    def load_rows(self):
        cur = self.conn.cursor()
        cur.execute(SQL_QUERY)
        return cur.fetchall()

    def apply_regexes(self, text):
        new_text = text
        for pattern, repl, flags in REGEX_RULES:
            new_text = re.sub(pattern, repl, new_text, flags=flags)
        return new_text

    def create_widgets(self):
        label_frame = ttk.Frame(self.master)
        label_frame.pack(fill="x", padx=5, pady=5)

        ttk.Label(label_frame, text="Before").grid(row=0, column=0, sticky="w")
        ttk.Label(label_frame, text="After").grid(row=0, column=1, sticky="w")

        text_frame = ttk.Frame(self.master)
        text_frame.pack(fill="both", expand=True, padx=5, pady=5)

        self.before_text = tk.Text(text_frame, wrap="none")
        self.before_text.grid(row=0, column=0, sticky="nsew")
        before_scroll_y = ttk.Scrollbar(text_frame, orient="vertical", command=self.before_text.yview)
        before_scroll_y.grid(row=0, column=1, sticky="ns")
        before_scroll_x = ttk.Scrollbar(text_frame, orient="horizontal", command=self.before_text.xview)
        before_scroll_x.grid(row=1, column=0, sticky="ew")
        self.before_text.configure(yscrollcommand=before_scroll_y.set, xscrollcommand=before_scroll_x.set)

        self.after_text = tk.Text(text_frame, wrap="none")
        self.after_text.grid(row=0, column=2, sticky="nsew")
        after_scroll_y = ttk.Scrollbar(text_frame, orient="vertical", command=self.after_text.yview)
        after_scroll_y.grid(row=0, column=3, sticky="ns")
        after_scroll_x = ttk.Scrollbar(text_frame, orient="horizontal", command=self.after_text.xview)
        after_scroll_x.grid(row=1, column=2, sticky="ew")
        self.after_text.configure(yscrollcommand=after_scroll_y.set, xscrollcommand=after_scroll_x.set)

        text_frame.columnconfigure(0, weight=1)
        text_frame.columnconfigure(2, weight=1)
        text_frame.rowconfigure(0, weight=1)

        control_frame = ttk.Frame(self.master)
        control_frame.pack(fill="x", padx=5, pady=5)

        self.info_label = ttk.Label(control_frame, text="")
        self.info_label.pack(side="left")

        ttk.Button(control_frame, text="Skip", command=self.skip_record).pack(side="right", padx=2)
        ttk.Button(control_frame, text="Apply to all remaining", command=self.apply_all_remaining).pack(side="right", padx=2)
        ttk.Button(control_frame, text="Apply", command=self.apply_record).pack(side="right", padx=2)

    def show_next_record(self):
        while self.index < len(self.rows):
            row = self.rows[self.index]
            old_text = row[TARGET_COL] or ""
            new_text = self.apply_regexes(old_text)

            if old_text == new_text:
                self.index += 1
                continue

            if self.apply_to_all:
                self.update_db(row[KEY_COL], new_text)
                self.index += 1
                continue

            self.before_text.delete("1.0", tk.END)
            self.before_text.insert("1.0", old_text)

            self.after_text.delete("1.0", tk.END)
            self.after_text.insert("1.0", new_text)

            self.info_label.config(
                text=f"Record {self.index + 1} of {len(self.rows)} (CitationID={row[KEY_COL]})"
            )
            return

        self.before_text.delete("1.0", tk.END)
        self.after_text.delete("1.0", tk.END)
        self.info_label.config(text="No more records to process.")
        messagebox.showinfo("Done", "All applicable records processed.")

    def update_db(self, key_value, new_text):
        cur = self.conn.cursor()
        cur.execute(
            f"UPDATE {TABLE_NAME} SET {TARGET_COL} = ? WHERE {KEY_COL} = ?",
            (new_text, key_value),
        )
        self.conn.commit()

    def apply_record(self):
        if self.index >= len(self.rows):
            return
        row = self.rows[self.index]
        old_text = row[TARGET_COL] or ""
        new_text = self.apply_regexes(old_text)
        self.update_db(row[KEY_COL], new_text)
        self.index += 1
        self.show_next_record()

    def skip_record(self):
        if self.index >= len(self.rows):
            return
        self.index += 1
        self.show_next_record()

    def apply_all_remaining(self):
        if messagebox.askyesno(
            "Confirm",
            "Apply these regex edits to all remaining records without prompting?"
        ):
            self.apply_to_all = True
            self.show_next_record()


def main():
    root = tk.Tk()
    root.geometry("1200x700")
    app = RegexEditorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
    