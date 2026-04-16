import sqlite3
import re
import difflib
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

# Regex rules: (pattern, replacement, flags)
REGEX_RULES = [
    (r"You are not a memberRequest membership", "", 0)
]

# ----------------------------------------


class RegexEditorApp:
    def __init__(self, master):
        self.master = master
        master.title("SQLite Regex Editor")

        # DB + data
        self.conn = sqlite3.connect(DB_PATH)
        self.conn.row_factory = sqlite3.Row
        self.rows = self.load_rows()
        self.index = 0
        self.apply_to_all = False

        # Current record text
        self.current_old = ""
        self.current_new = ""

        # GUI
        self.create_widgets()
        self.show_next_record()

    # ---------------- DB ----------------

    def load_rows(self):
        cur = self.conn.cursor()
        cur.execute(SQL_QUERY)
        return cur.fetchall()

    def update_db(self, key_value, new_text):
        cur = self.conn.cursor()
        cur.execute(
            f"UPDATE {TABLE_NAME} SET {TARGET_COL} = ? WHERE {KEY_COL} = ?",
            (new_text, key_value),
        )
        self.conn.commit()

    # ---------------- REGEX ----------------

    def apply_regexes(self, text):
        new_text = text
        for pattern, repl, flags in REGEX_RULES:
            new_text = re.sub(pattern, repl, new_text, flags=flags)
        return new_text

    # ---------------- DIFF: UNIFIED ----------------

    def make_unified_diff(self, old, new):
        old_lines = old.splitlines(keepends=True)
        new_lines = new.splitlines(keepends=True)

        diff = difflib.unified_diff(
            old_lines,
            new_lines,
            fromfile="before",
            tofile="after",
            lineterm=""
        )
        return list(diff)

    def render_unified_diff(self, diff_lines):
        self.before_text.delete("1.0", tk.END)

        for line in diff_lines:
            if line.startswith("+") and not line.startswith("+++"):
                tag = "added"
            elif line.startswith("-") and not line.startswith("---"):
                tag = "removed"
            elif line.startswith("@@") or line.startswith("---") or line.startswith("+++"):
                tag = "header"
            else:
                tag = "context"

            self.before_text.insert(tk.END, line + "\n", tag)

        self.after_text.delete("1.0", tk.END)
        self.after_text.insert("1.0", "(Unified diff mode)")

    # ---------------- DIFF: SIDE-BY-SIDE ----------------

    def make_side_by_side_diff(self, old, new):
        old_lines = old.splitlines()
        new_lines = new.splitlines()

        sm = difflib.SequenceMatcher(None, old_lines, new_lines)
        result = []

        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag == "equal":
                for a, b in zip(old_lines[i1:i2], new_lines[j1:j2]):
                    result.append(("  " + a, "  " + b, "context"))
            elif tag == "replace":
                for a, b in zip(old_lines[i1:i2], new_lines[j1:j2]):
                    result.append(("- " + a, "+ " + b, "changed"))
            elif tag == "delete":
                for a in old_lines[i1:i2]:
                    result.append(("- " + a, "", "removed"))
            elif tag == "insert":
                for b in new_lines[j1:j2]:
                    result.append(("", "+ " + b, "added"))

        return result

    def render_side_by_side(self, diff_rows):
        self.before_text.delete("1.0", tk.END)
        self.after_text.delete("1.0", tk.END)

        for left, right, tag in diff_rows:
            self.before_text.insert(tk.END, left + "\n", tag)
            self.after_text.insert(tk.END, right + "\n", tag)

    # ---------------- GUI ----------------

    def create_widgets(self):
        # Labels
        label_frame = ttk.Frame(self.master)
        label_frame.pack(fill="x", padx=5, pady=5)

        ttk.Label(label_frame, text="Before / Diff").grid(row=0, column=0, sticky="w")
        ttk.Label(label_frame, text="After").grid(row=0, column=1, sticky="w")

        # Text frames
        text_frame = ttk.Frame(self.master)
        text_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # BEFORE text
        self.before_text = tk.Text(text_frame, wrap="none", font=("Consolas", 10))
        self.before_text.grid(row=0, column=0, sticky="nsew")

        before_scroll_y = ttk.Scrollbar(text_frame, orient="vertical", command=self.before_text.yview)
        before_scroll_y.grid(row=0, column=1, sticky="ns")
        before_scroll_x = ttk.Scrollbar(text_frame, orient="horizontal", command=self.before_text.xview)
        before_scroll_x.grid(row=1, column=0, sticky="ew")

        self.before_text.configure(yscrollcommand=before_scroll_y.set, xscrollcommand=before_scroll_x.set)

        # AFTER text
        self.after_text = tk.Text(text_frame, wrap="none", font=("Consolas", 10))
        self.after_text.grid(row=0, column=2, sticky="nsew")

        after_scroll_y = ttk.Scrollbar(text_frame, orient="vertical", command=self.after_text.yview)
        after_scroll_y.grid(row=0, column=3, sticky="ns")
        after_scroll_x = ttk.Scrollbar(text_frame, orient="horizontal", command=self.after_text.xview)
        after_scroll_x.grid(row=1, column=2, sticky="ew")

        self.after_text.configure(yscrollcommand=after_scroll_y.set, xscrollcommand=after_scroll_x.set)

        # Grid weights
        text_frame.columnconfigure(0, weight=1)
        text_frame.columnconfigure(2, weight=1)
        text_frame.rowconfigure(0, weight=1)

        # Color tags for diff
        for widget in (self.before_text, self.after_text):
            widget.tag_configure("added", foreground="#008000")
            widget.tag_configure("removed", foreground="#cc0000")
            widget.tag_configure("changed", foreground="#aa5500")
            widget.tag_configure("header", foreground="#666666")
            widget.tag_configure("context", foreground="#000000")

        # Controls
        control_frame = ttk.Frame(self.master)
        control_frame.pack(fill="x", padx=5, pady=5)

        self.info_label = ttk.Label(control_frame, text="")
        self.info_label.pack(side="left")

        # View mode selector
        self.view_mode = tk.StringVar(value="raw")

        ttk.Radiobutton(control_frame, text="Raw", value="raw",
                        variable=self.view_mode, command=self.refresh_view).pack(side="right", padx=5)

        ttk.Radiobutton(control_frame, text="Unified diff", value="unified",
                        variable=self.view_mode, command=self.refresh_view).pack(side="right", padx=5)

        ttk.Radiobutton(control_frame, text="Side‑by‑side diff", value="sidebyside",
                        variable=self.view_mode, command=self.refresh_view).pack(side="right", padx=5)

        ttk.Button(control_frame, text="Skip", command=self.skip_record).pack(side="right", padx=2)
        ttk.Button(control_frame, text="Apply to all remaining", command=self.apply_all_remaining).pack(side="right", padx=2)
        ttk.Button(control_frame, text="Apply", command=self.apply_record).pack(side="right", padx=2)

    # ---------------- VIEW LOGIC ----------------

    def refresh_view(self):
        if not hasattr(self, "current_old"):
            return

        mode = self.view_mode.get()

        if mode == "raw":
            self.before_text.delete("1.0", tk.END)
            self.before_text.insert("1.0", self.current_old)

            self.after_text.delete("1.0", tk.END)
            self.after_text.insert("1.0", self.current_new)

        elif mode == "unified":
            diff_lines = self.make_unified_diff(self.current_old, self.current_new)
            self.render_unified_diff(diff_lines)

        elif mode == "sidebyside":
            diff_rows = self.make_side_by_side_diff(self.current_old, self.current_new)
            self.render_side_by_side(diff_rows)

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

            self.current_old = old_text
            self.current_new = new_text

            self.info_label.config(
                text=f"Record {self.index + 1} of {len(self.rows)} (CitationID={row[KEY_COL]})"
            )

            self.refresh_view()
            return

        # No more records
        self.before_text.delete("1.0", tk.END)
        self.after_text.delete("1.0", tk.END)
        self.info_label.config(text="No more records to process.")
        messagebox.showinfo("Done", "All applicable records processed.")

    # ---------------- BUTTON ACTIONS ----------------

    def apply_record(self):
        if self.index >= len(self.rows):
            return
        row = self.rows[self.index]
        new_text = self.apply_regexes(row[TARGET_COL] or "")
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
    root.geometry("1600x900")
    app = RegexEditorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

    