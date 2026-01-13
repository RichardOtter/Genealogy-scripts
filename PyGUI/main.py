import sqlite3
import tkinter as tk
from tkinter import messagebox

DB_PATH = r"DB\TEST-PyGUI.rmtree"

# ---------------------------------------------------------
# 1. DEFINE YOUR JOIN QUERY AND COLUMN MAPPINGS HERE
# ---------------------------------------------------------


JOIN_SQL = """
WITH
 constants AS (SELECT
    4  AS C_Matcher,  -- 17 Roman, 4 Rose, 1 RJO, 6 GCS
    5  AS C_DnaService,  -- 2 Anc, 5 MyHer
    1  AS C_Offset ),
 tab AS (
  SELECT 
  (ROW_NUMBER() OVER( ORDER BY Sort1 DESC, Sort2 ASC, RecID ASC))
    -(SELECT C_Offset FROM constants) AS SeqNum,
  "RecID", Label2, "SharedCM", "AuxDNATableID", Sort1, Sort2, adt.UTCModDate
  FROM DNATable
  INNER JOIN AuxDNATable AS adt ON AuxDNATableID = RecID
  WHERE ID1=(SELECT C_Matcher FROM constants)
    AND DNAProvider=(SELECT C_DnaService FROM constants)
  ORDER BY Sort1 DESC, Sort2 ASC, RecID ASC)
SELECT *
FROM tab
WHERE SeqNum = ?
"""

# Columns returned by the JOIN query (in order)
JOIN_COLUMNS = ["SeqNum", "RecID", "Label2", "SharedCM", "AuxDNATableID", "Sort1", "Sort2",  "UTCModDate"]

FIELD_LAYOUT = {
    "RecID":         {"row": 1, "col": 0, "width": 10, "readonly": True},
    "SeqNum":       {"row": 1, "col": 30, "width": 10, "readonly": True},
    "Label2":      {"row": 2, "col": 0, "width": 40},
    "SharedCM":    {"row": 3, "col": 2, "width": 10},
    "Sort1":       {"row": 4, "col": 2, "width": 20},
    "Sort2":      {"row": 4, "col": 25, "width": 20},
#    "AuxDNATableID": hidden
    "UTCModDate":      {"row": 7, "col": 25, "width": 20}

}

# Mapping of GUI fields → (table, column)
# This allows updating multiple tables cleanly.
WRITABLE_MAP = {
    "Label2": ("DNATable", "Label2"),
    "SharedCM": ("DNATable", "SharedCM"),
    "Sort1": ("AuxDNATable", "Sort1"),
    "Sort2": ("AuxDNATable", "Sort2"),
}

# Primary key columns for each table
PRIMARY_KEYS = {
    "DNATable": "RecID",
    "AuxDNATable": "AuxDNATableID",
}

VISIBLE_FIELDS = set(FIELD_LAYOUT.keys())

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
        tk.Label(self.root, text="Record ID:", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5, pady=5)
        self.id_entry = tk.Entry(self.root, width=10)
        self.id_entry.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(self.root, text="Load", command=self.load_by_id).grid(row=0, column=2, padx=5, pady=5)

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

            # Read-only support
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

        tk.Button(self.root, text="Save Changes", command=self.save_record).grid(
            row=20, column=0, columnspan=4, pady=15
        )

    # ---------------------------------------------------------
    # LOAD RECORD
    # ---------------------------------------------------------

    def load_by_id(self):
        try:
            record_id = int(self.id_entry.get())
        except ValueError:
            messagebox.showerror("Invalid", "ID must be an integer")
            return

        self.cursor.execute(JOIN_SQL, (record_id,))
        row = self.cursor.fetchone()

        if row is None:
            messagebox.showerror("Not found", f"No record with ID {record_id}")
            return

        self.current_row = dict(zip(JOIN_COLUMNS, row))

        for col_name, value in self.current_row.items():

            # Skip hidden fields
            if col_name not in self.entries:
                continue

            widget = self.entries[col_name]

            # Handle read-only fields
            if widget.cget("state") == "readonly":
                widget.config(state="normal")
                widget.delete(0, tk.END)
                widget.insert(0, "" if value is None else str(value))
                widget.config(state="readonly")
            else:
                widget.delete(0, tk.END)
                widget.insert(0, "" if value is None else str(value))

            widget.config(bg="white")

    # ---------------------------------------------------------
    # FIELD CHANGE HIGHLIGHTING
    # ---------------------------------------------------------

    def on_field_change(self, event):
        widget = event.widget

        for field_name, entry_widget in self.entries.items():
            if entry_widget is widget:
                break
        else:
            return

        # Skip read-only fields
        if widget.cget("state") == "readonly":
            return

        new_value = widget.get()
        old_value = "" if self.current_row[field_name] is None else str(self.current_row[field_name])

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

        for field, (table, column) in WRITABLE_MAP.items():

            # Skip hidden fields
            if field not in self.entries:
                continue

            widget = self.entries[field]

            # Skip read-only fields
            if widget.cget("state") == "readonly":
                continue

            new_value = widget.get()
            old_value = "" if self.current_row[field] is None else str(self.current_row[field])

            if new_value == old_value:
                continue

            if table not in updates_by_table:
                updates_by_table[table] = {}

            updates_by_table[table][column] = new_value

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

        for table, updates in updates_by_table.items():
            pk_col = PRIMARY_KEYS[table]
            pk_value = self.current_row[pk_col]

            set_clause = ", ".join([f"{col}=?" for col in updates.keys()])
            sql = f"UPDATE {table} SET {set_clause} WHERE {pk_col}=?"
            params = list(updates.values()) + [pk_value]

            self.cursor.execute(sql, params)

        self.conn.commit()
        messagebox.showinfo("Saved", "Changes saved successfully.")

    def __del__(self):
        self.conn.close()


# ---------------------------------------------------------
# RUN APP
# ---------------------------------------------------------

if __name__ == "__main__":
    root = tk.Tk()
    app = JoinedRecordApp(root)
    root.mainloop()
