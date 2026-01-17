import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext

DB_PATH = r"DB\TEST-PyGUI.rmtree"
DEBUG = False   # Set to True for console debugging

# ---------------------------------------------------------
# 1. JOIN QUERY AND COLUMN MAPPINGS
# ---------------------------------------------------------

JOIN_SQL = """
WITH
 tab AS (
  SELECT 
    (ROW_NUMBER() OVER (
        ORDER BY Sort1 DESC, Sort2 ASC, DNATable.RecID ASC
    )),
    DNATable.RecID,
    Label2,
    SharedCM,
    Note,
    adt.AuxDNATableID,
    adt.Sort1,
    adt.Sort2,
    adt.UTCModDate

  FROM DNATable
  INNER JOIN AuxDNATable AS adt
    ON adt.AuxDNATableID = DNATable.RecID

  ORDER BY Sort1 DESC, Sort2 ASC, DNATable.RecID ASC
)
SELECT *
FROM tab
WHERE RecID = ?
"""

JOIN_COLUMNS = [
    "SeqNum",
    "RecID",
    "Label2",
    "SharedCM",
    "Note",
    "AuxDNATableID",
    "Sort1",
    "Sort2",
    "UTCModDate",
]

# ---------------------------------------------------------
# 2. FIELD LAYOUT (Entry + Text widgets)
# ---------------------------------------------------------

FIELD_LAYOUT = {
    "RecID":       {"row": 1, "col": 0,  "width": 10, "readonly": True},
    "SeqNum":      {"row": 1, "col": 2,  "width": 10, "readonly": True},

    "Label2":      {"row": 2, "col": 0,  "width": 40},
    "SharedCM":    {"row": 3, "col": 0,  "width": 10},

    "Sort1":       {"row": 4, "col": 0,  "width": 10},
    "Sort2":       {"row": 4, "col": 2,  "width": 10},

    # Multi-line ScrolledText field
    "Note":        {"row": 6, "col": 0, "width": 20, "height": 6, "type": "ScrolledText"},

    "UTCModDate":  {"row": 7, "col": 0,  "width": 25, "readonly": True}
}

VISIBLE_FIELDS = set(FIELD_LAYOUT.keys())

# ---------------------------------------------------------
# 3. WRITABLE MAP + PRIMARY KEYS
# ---------------------------------------------------------

WRITABLE_MAP = {
    "Label2":   ("DNATable", "Label2"),
    "SharedCM": ("DNATable", "SharedCM"),
    "Note":     ("DNATable", "Note"),

    "Sort1":    ("AuxDNATable", "Sort1"),
    "Sort2":    ("AuxDNATable", "Sort2")

}

PRIMARY_KEYS = {
    "DNATable":    "RecID",
    "AuxDNATable": "AuxDNATableID",
}

# ---------------------------------------------------------
# 4. APPLICATION CLASS
# ---------------------------------------------------------

class JoinedRecordApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Joined Record Viewer/Editor")

        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()

        self.entries = {}
        self.current_row = None

        self.build_ui()

    # ---------------------------------------------------------
    # BUILD UI
    # ---------------------------------------------------------

    def build_ui(self):

        root.columnconfigure(0, weight=1)
        root.rowconfigure(1, weight=1)

        top_frame = tk.Frame(self.root, highlightbackground="black", 
                             highlightthickness=1, bg="lightblue")
        top_frame.grid(row=0, column=0, sticky="EW")
        top_frame.rowconfigure(0, weight=1)


        bottom_frame =tk.Frame(self.root,highlightbackground="black", 
                               highlightthickness=1,bg="lightgreen")
        bottom_frame.grid(row=1, column=0, pady=20, sticky="NSEW")
        bottom_frame.columnconfigure(0, weight=1)
        bottom_frame.rowconfigure(1, weight=1)


        tk.Label(top_frame, text="PKNum:", font=("Arial", 10, "bold")).grid(
            row=0, column=0, padx=5, pady=5, sticky="w"
        )

        self.id_entry = tk.Entry(top_frame, width=10)
        self.id_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        tk.Button(top_frame, text="Load", command=self.load_by_id).grid(
            row=0, column=1, padx=100, pady=5, sticky="w"
        )

        for field in JOIN_COLUMNS:

            if field not in FIELD_LAYOUT:
                continue

            layout = FIELD_LAYOUT[field]

            tk.Label(
                top_frame,
                text=field,
                font=("Arial", 10, "bold")
            ).grid(
                row=layout["row"],
                column=layout["col"],
                padx=5,
                pady=5,
                sticky="w"
            )

            widget_type = layout.get("type", "entry")

            if widget_type == "ScrolledText":
                entry = scrolledtext.ScrolledText(
                    bottom_frame,
                    width=layout["width"]
                )
                entry.grid(row=0, column=0, sticky="NSEW")
            else:
                entry = tk.Entry(top_frame, width=layout["width"])
                if layout.get("readonly", False):
                    entry.config(state="readonly")
                entry.grid(
                    row=layout["row"],
                    column=layout["col"] + 1,
                    padx=5,
                    pady=5,
                    sticky="w"
                )

            entry.bind("<KeyRelease>", self.on_field_change)
            self.entries[field] = entry

        tk.Button(top_frame, text="Save Changes", command=self.save_record).grid(
            row=20, column=0, columnspan=4, pady=15
        )

    # ---------------------------------------------------------
    # LOAD RECORD
    # ---------------------------------------------------------

    def load_by_id(self):
        try:
            pk_num = int(self.id_entry.get())
        except ValueError:
            messagebox.showerror("Invalid", "PKNum must be an integer")
            return

        self.cursor.execute(JOIN_SQL, (pk_num,))
        row = self.cursor.fetchone()

        if row is None:
            messagebox.showerror("Not found", f"No record with SeqNum {pk_num}")
            return

        self.current_row = dict(zip(JOIN_COLUMNS, row))

        for col, value in self.current_row.items():

            if col not in self.entries:
                continue

            widget = self.entries[col]
            text_value = "" if value is None else str(value)

            if isinstance(widget, tk.Text):
                widget.config(state="normal")
                widget.delete("1.0", tk.END)
                widget.insert("1.0", text_value)
                if FIELD_LAYOUT[col].get("readonly", False):
                    widget.config(state="disabled")
            else:
                if widget.cget("state") == "readonly":
                    widget.config(state="normal")
                    widget.delete(0, tk.END)
                    widget.insert(0, text_value)
                    widget.config(state="readonly")
                else:
                    widget.delete(0, tk.END)
                    widget.insert(0, text_value)

            widget.config(bg="white")

    # ---------------------------------------------------------
    # FIELD CHANGE HIGHLIGHTING
    # ---------------------------------------------------------

    def on_field_change(self, event):
        widget = event.widget

        field = None
        for f, w in self.entries.items():
            if w is widget:
                field = f
                break

        if field is None:
            return

        if FIELD_LAYOUT[field].get("readonly", False):
            return

        if isinstance(widget, tk.Text):
            new_value = widget.get("1.0", tk.END).strip()
        else:
            new_value = widget.get().strip()

        old_raw = self.current_row[field]
        old_value = "" if old_raw is None else str(old_raw).strip()

        widget.config(bg="#fff2a8" if new_value != old_value else "white")

    # ---------------------------------------------------------
    # SAVE RECORD
    # ---------------------------------------------------------

    def save_record(self):
        if self.current_row is None:
            messagebox.showerror("No record", "Load a record first")
            return

        updates_by_table = {}

        for field, (table, column) in WRITABLE_MAP.items():

            widget = self.entries[field]

            if isinstance(widget, tk.Text):
                new_value = widget.get("1.0", tk.END).strip()
            else:
                new_value = widget.get().strip()

            old_raw = self.current_row[field]
            old_value = "" if old_raw is None else str(old_raw).strip()

            if new_value == old_value:
                continue

            updates_by_table.setdefault(table, {})[column] = new_value

        if not updates_by_table:
            messagebox.showinfo("No changes", "No fields were modified.")
            return

        for table, updates in updates_by_table.items():
            pk_col = PRIMARY_KEYS[table]
            pk_value = self.current_row[pk_col]

            set_clause = ", ".join([f"{col}=?" for col in updates])
            sql = f"UPDATE {table} SET {set_clause} WHERE {pk_col}=?"
            params = list(updates.values()) + [pk_value]

            self.cursor.execute(sql, params)

        self.conn.commit()
        # messagebox.showinfo("Saved", "Changes saved successfully.")

    def __del__(self):
        try:
            self.conn.close()
        except:
            pass


# ---------------------------------------------------------
# RUN APP
# ---------------------------------------------------------

if __name__ == "__main__":
    root = tk.Tk()
    app = JoinedRecordApp(root)
    root.mainloop()