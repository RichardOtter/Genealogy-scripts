import sqlite3
import tkinter as tk
from tkinter import messagebox

DB_PATH = r"DB\TEST-PyGUI.rmtree"
DEBUG = True  # set to False when you're happy

# ---------------------------------------------------------
# 1. JOIN QUERY AND COLUMN MAPPINGS
# ---------------------------------------------------------

JOIN_SQL = """
WITH
 constants AS (SELECT
    4  AS C_Matcher,      -- 17 Roman, 4 Rose, 1 RJO, 6 GCS
    5  AS C_DnaService,   -- 2 Anc, 5 MyHer
    1  AS C_Offset ),
 tab AS (
  SELECT 
    (ROW_NUMBER() OVER (
        ORDER BY Sort1 DESC, Sort2 ASC, RecID ASC
    ))
    - (SELECT C_Offset FROM constants) AS SeqNum,
    DNATable.RecID,
    Label2,
    SharedCM,
    adt.AuxDNATableID,
    Sort1,
    Sort2,
    adt.UTCModDate
  FROM DNATable
  INNER JOIN AuxDNATable AS adt
    ON adt.AuxDNATableID = DNATable.RecID
  WHERE ID1 = (SELECT C_Matcher FROM constants)
    AND DNAProvider = (SELECT C_DnaService FROM constants)
  ORDER BY Sort1 DESC, Sort2 ASC, RecID ASC
)
SELECT *
FROM tab
WHERE SeqNum = ?
"""

# Columns returned by the JOIN query (in order)
JOIN_COLUMNS = [
    "SeqNum",
    "RecID",
    "Label2",
    "SharedCM",
    "AuxDNATableID",
    "Sort1",
    "Sort2",
    "UTCModDate",
]

# ---------------------------------------------------------
# 2. FIELD LAYOUT AND MAPPINGS
# ---------------------------------------------------------

FIELD_LAYOUT = {
    "RecID":       {"row": 1, "col": 0,  "width": 10, "readonly": True},
    "SeqNum":      {"row": 1, "col": 3,  "width": 10, "readonly": True},
    "Label2":      {"row": 2, "col": 0,  "width": 40},
    "SharedCM":    {"row": 3, "col": 0,  "width": 10},
    "Sort1":       {"row": 4, "col": 0,  "width": 10},
    "Sort2":       {"row": 4, "col": 3,  "width": 10},
    # "AuxDNATableID": hidden on purpose
    "UTCModDate":  {"row": 7, "col": 0,  "width": 25, "readonly": True},
}

VISIBLE_FIELDS = set(FIELD_LAYOUT.keys())

# Mapping of GUI fields → (table, column)
WRITABLE_MAP = {
    "Label2":   ("DNATable", "Label2"),
    "SharedCM": ("DNATable", "SharedCM"),
    "Sort1":    ("AuxDNATable", "Sort1"),
    "Sort2":    ("AuxDNATable", "Sort2"),
}

# Primary key columns for each table
PRIMARY_KEYS = {
    "DNATable":    "RecID",
    "AuxDNATable": "AuxDNATableID",
}

# ---------------------------------------------------------
# 3. APPLICATION CLASS
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
        tk.Label(
            self.root,
            text="SeqNum:",
            font=("Arial", 10, "bold")
        ).grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.id_entry = tk.Entry(self.root, width=10)
        self.id_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        tk.Button(
            self.root,
            text="Load",
            command=self.load_by_id
        ).grid(row=0, column=2, padx=5, pady=5, sticky="w")

        for field in JOIN_COLUMNS:

            # Skip hidden fields
            if field not in FIELD_LAYOUT:
                continue

            layout = FIELD_LAYOUT[field]

            tk.Label(
                self.root,
                text=field,
                font=("Arial", 10, "bold")
            ).grid(
                row=layout["row"],
                column=layout["col"],
                padx=5,
                pady=5,
                sticky="w"
            )

            entry = tk.Entry(self.root, width=layout["width"])

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

        tk.Button(
            self.root,
            text="Save Changes",
            command=self.save_record
        ).grid(row=20, column=0, columnspan=4, pady=15)

    # ---------------------------------------------------------
    # LOAD RECORD BY SeqNum
    # ---------------------------------------------------------

    def load_by_id(self):
        try:
            record_seq = int(self.id_entry.get())
        except ValueError:
            messagebox.showerror("Invalid", "SeqNum must be an integer")
            return

        if DEBUG:
            print(f"[DEBUG] Loading record with SeqNum={record_seq}")

        self.cursor.execute(JOIN_SQL, (record_seq,))
        row = self.cursor.fetchone()

        if row is None:
            messagebox.showerror("Not found", f"No record with SeqNum {record_seq}")
            return

        self.current_row = dict(zip(JOIN_COLUMNS, row))

        if DEBUG:
            print("[DEBUG] current_row loaded:", self.current_row)

        for col_name, value in self.current_row.items():

            if col_name not in self.entries:
                continue

            widget = self.entries[col_name]
            text_value = "" if value is None else str(value)

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

        field_name = None
        for f, entry_widget in self.entries.items():
            if entry_widget is widget:
                field_name = f
                break

        if field_name is None:
            return

        if widget.cget("state") == "readonly":
            return

        new_value = widget.get().strip()
        old_raw = self.current_row[field_name]
        old_value = "" if old_raw is None else str(old_raw).strip()

        if new_value != old_value:
            widget.config(bg="#fff2a8")
        else:
            widget.config(bg="white")

    # ---------------------------------------------------------
    # SAVE RECORD (ONLY CHANGED FIELDS)
    # ---------------------------------------------------------

    def save_record(self):
        if self.current_row is None:
            messagebox.showerror("No record", "Load a record first")
            return

        updates_by_table = {}

        # Detect changed, writable fields
        for field, (table, column) in WRITABLE_MAP.items():

            if field not in self.entries:
                continue

            widget = self.entries[field]

            if widget.cget("state") == "readonly":
                continue

            new_value = widget.get().strip()
            old_raw = self.current_row[field]
            old_value = "" if old_raw is None else str(old_raw).strip()

            if DEBUG:
                print(f"[DEBUG] Check field {field}: old={repr(old_value)} new={repr(new_value)}")

            if new_value == old_value:
                continue

            if table not in updates_by_table:
                updates_by_table[table] = {}

            updates_by_table[table][column] = new_value

        if DEBUG:
            print("[DEBUG] updates_by_table:", updates_by_table)

        if not updates_by_table:
            messagebox.showinfo("No changes", "No fields were modified.")
            return

        changed_fields = []
        for table, updates in updates_by_table.items():
            for col in updates.keys():
                changed_fields.append(f"{table}.{col}")

        field_list = "\n".join(changed_fields)

        confirm = messagebox.askyesno(
            "Confirm Save",
            f"The following fields were modified:\n\n{field_list}\n\nSave these changes?"
        )

        if not confirm:
            return

        # Execute UPDATEs
        for table, updates in updates_by_table.items():
            pk_col = PRIMARY_KEYS[table]
            pk_value = self.current_row[pk_col]

            set_clause = ", ".join([f"{col}=?" for col in updates.keys()])
            sql = f"UPDATE {table} SET {set_clause} WHERE {pk_col}=?"
            params = list(updates.values()) + [pk_value]

            if DEBUG:
                print(f"[DEBUG] Executing UPDATE for {table}")
                print("        SQL:", sql)
                print("        PARAMS:", params)

            self.cursor.execute(sql, params)

            if DEBUG:
                print(f"[DEBUG] {table} rowcount after UPDATE:", self.cursor.rowcount)

        self.conn.commit()
        messagebox.showinfo("Saved", "Changes saved successfully.")

        # Reload current row from DB to sync current_row with DB values
        # (optional, but keeps highlighting logic consistent)
        seqnum = self.current_row["SeqNum"]
        if DEBUG:
            print(f"[DEBUG] Reloading row after save, SeqNum={seqnum}")
        self.cursor.execute(JOIN_SQL, (seqnum,))
        row = self.cursor.fetchone()
        if row is not None:
            self.current_row = dict(zip(JOIN_COLUMNS, row))
            if DEBUG:
                print("[DEBUG] current_row after save:", self.current_row)

    def __del__(self):
        try:
            self.conn.close()
        except Exception:
            pass


# ---------------------------------------------------------
# RUN APP
# ---------------------------------------------------------

if __name__ == "__main__":
    root = tk.Tk()
    app = JoinedRecordApp(root)
    root.mainloop()
    