from datetime import datetime
from tkinter import messagebox, ttk
import tkinter as tk
import re
import sys
from pathlib import Path
sys.path.append(
    str(Path.resolve(Path(__file__).resolve().parent / '../RMpy package')))


import RMpy.common as RMc       # noqa #type: ignore
import RMpy.launcher            # noqa #type: ignore


# ===================================================DIV60==
def main():

    # Configuration
    utility_info = {}
    utility_info["utility_name"] = "PlaceTableEditor"
    utility_info["utility_version"] = "UTILITY_VERSION_NUMBER_RM_UTILS_OVERRIDE"
    utility_info["config_file_name"] = "RM-Python-config.ini"
    utility_info["script_path"] = Path(__file__).parent.resolve()
    utility_info["run_features_function"] = run_places_editor
    utility_info["allow_db_changes"] = True
    utility_info["RMNOCASE_required"] = True
    utility_info["RMNOCASE_optional"] = False
    utility_info["RegExp_required"] = False
    utility_info["RegExp_optional"] = False

    RMpy.launcher.launcher(utility_info)


# ===================================================DIV60==
def run_places_editor(config, db_connection, report_file):
    table_name = "PlaceTable"

    RMpy.common.reindex_RMNOCASE(db_connection)

    try:
        table_info = db_connection.execute(
            f"PRAGMA table_info({table_name})").fetchall()
    except Exception as error:
        messagebox.showerror("Database error", str(error))
        return

    if not table_info:
        messagebox.showerror(
            "Database error", f"The database does not contain {table_name}.")
        return

    columns = [row[1] for row in table_info]
    note_column_index = next(
        (index for index, column in enumerate(columns)
         if column.lower() in {"note", "notes"}), None)
    if note_column_index is None:
        messagebox.showerror(
            "Database error", "The PlaceTable does not contain a Note field.")
        return
    name_column_index = next(
        (index for index, column in enumerate(columns)
         if column.lower() == "name"), None)
    if name_column_index is None:
        messagebox.showerror(
            "Database error", "The PlaceTable does not contain a Name field.")
        return
    column_sql = ", ".join(f'"{column.replace(chr(34), chr(34) * 2)}"'
                           for column in columns)
    try:
        rows = db_connection.execute(
            f"SELECT {column_sql} FROM {table_name} "
            f"ORDER BY \"{columns[0].replace(chr(34), chr(34) * 2)}\""
        ).fetchall()
    except Exception as error:
        messagebox.showerror("Database error", str(error))
        return

    root = tk.Tk()
    root.title("RootsMagic Place Table Editor")
    root.geometry("760x900")
    root.minsize(760, 520)

    place_type_value = config.get("OPTIONS", "PLACETYPE", fallback="").strip()
    place_type_filter = None
    if place_type_value:
        try:
            place_type_filter = int(place_type_value)
        except ValueError:
            messagebox.showerror(
                "Invalid PLACETYPE", "PLACETYPE must be 0, 1 or 2.")
            root.destroy()
            return

    filter_value = ""
    exclude_note_filter_value = ""
    exclude_name_filter_value = ""
    try:
        filter_value = config.get("OPTIONS", "PLACE_FILTER", fallback="")
        exclude_note_filter_value = config.get(
            "OPTIONS", "PLACE_FILTER_NOT_NOTE",
            fallback=config.get("OPTIONS", "PLACE_FILTER_NOT", fallback=""))
        exclude_name_filter_value = config.get(
            "OPTIONS", "PLACE_FILTER_NOT_NAME", fallback="")
    except (AttributeError, KeyError):
        pass

    filtered_rows = []
    current_index = 0
    fields = {}
    utc_mod_date_column = next(
        (column for column in columns if column.lower() == "utcmoddate"), None)

    filter_frame = ttk.Frame(root, padding=8)
    filter_frame.pack(fill="x")
    filter_frame.columnconfigure(1, weight=1)
    ttk.Label(filter_frame, text="Match records:").grid(
        row=0, column=0, sticky="w", padx=(0, 6), pady=2)
    filter_entry = ttk.Entry(filter_frame, width=48)
    filter_entry.grid(row=0, column=1, sticky="ew", pady=2)
    filter_entry.insert(0, filter_value)
    ttk.Label(filter_frame, text="But not Note:").grid(
        row=1, column=0, sticky="w", padx=(0, 6), pady=2)
    exclude_note_filter_entry = ttk.Entry(filter_frame, width=48)
    exclude_note_filter_entry.grid(row=1, column=1, sticky="ew", pady=2)
    exclude_note_filter_entry.insert(0, exclude_note_filter_value)
    ttk.Label(filter_frame, text="But not Name:").grid(
        row=2, column=0, sticky="w", padx=(0, 6), pady=2)
    exclude_name_filter_entry = ttk.Entry(filter_frame, width=48)
    exclude_name_filter_entry.grid(row=2, column=1, sticky="ew", pady=2)
    exclude_name_filter_entry.insert(0, exclude_name_filter_value)
    status_label = ttk.Label(filter_frame, text="")
    status_label.grid(row=3, column=1, sticky="w", padx=(6, 0), pady=2)

    body = ttk.Frame(root, padding=(8, 0, 8, 8))
    body.pack(fill="both", expand=True)
    body.columnconfigure(0, weight=1)
    body.rowconfigure(0, weight=1)

    canvas = tk.Canvas(body, highlightthickness=0)
    scrollbar = ttk.Scrollbar(body, orient="vertical", command=canvas.yview)
    fields_frame = ttk.Frame(canvas)
    canvas_window = canvas.create_window(
        (0, 0), window=fields_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.grid(row=0, column=0, sticky="nsew")
    scrollbar.grid(row=0, column=1, sticky="ns")

    def resize_fields(event):
        canvas.itemconfigure(canvas_window, width=event.width)

    fields_frame.bind(
        "<Configure>", lambda event: canvas.configure(
            scrollregion=canvas.bbox("all")))
    canvas.bind("<Configure>", resize_fields)

    note_column = columns[note_column_index]
    display_columns = [column for column in columns if column != note_column]
    display_columns.append(note_column)

    for row_number, column in enumerate(display_columns):
        ttk.Label(fields_frame, text=column).grid(
            row=row_number, column=0, sticky="nw", padx=(0, 8), pady=3)
        if column.lower() in {"note", "notes"}:
            note_frame = ttk.Frame(fields_frame)
            note_frame.grid(row=row_number, column=1, sticky="nsew", pady=3)
            field = tk.Text(note_frame, height=12, width=180, wrap="word")
            field.configure(state="normal")
            note_scrollbar = ttk.Scrollbar(
                note_frame, orient="vertical", command=field.yview)
            field.configure(yscrollcommand=note_scrollbar.set)
            field.grid(row=0, column=0, sticky="nsew")
            note_scrollbar.grid(row=0, column=1, sticky="ns")
            note_frame.columnconfigure(0, weight=1)
            note_frame.rowconfigure(0, weight=1)
        else:
            if column == utc_mod_date_column:
                utc_frame = ttk.Frame(fields_frame)
                utc_frame.grid(row=row_number, column=1, sticky="w", pady=3)
                field = ttk.Entry(utc_frame, width=27)
                field.configure(state="readonly")
                field.pack(side="left")
                ttk.Button(
                    utc_frame, text="Update", width=10,
                    command=lambda: update_utc_mod_date()).pack(
                        side="left", padx=(6, 0))
            else:
                field = ttk.Entry(fields_frame, width=40)
                field.configure(state="normal")
                field.grid(row=row_number, column=1, sticky="ew", pady=3)
        fields[column] = field
    fields_frame.columnconfigure(1, weight=1)

    navigation = ttk.Frame(root, padding=(8, 0, 8, 8))
    navigation.pack(fill="x")
    goto_entry = ttk.Entry(navigation, width=10)
    goto_entry.pack(side="left", padx=(0, 5))

    def set_field(field, value):
        text = "" if value is None else str(value)
        column = next(
            column_name for column_name, field_value in fields.items()
            if field_value is field)
        if column == utc_mod_date_column and value is not None:
            try:
                local_time = datetime.fromtimestamp(
                    (float(value) + 2415018.5 - 2440587.5) * 86400)
                text = local_time.strftime("%Y-%m-%d %H:%M:%S")
            except (TypeError, ValueError, OverflowError):
                text = str(value)
        read_only = field is fields[columns[0]]
        read_only = read_only or column == utc_mod_date_column
        if isinstance(field, tk.Text):
            field.configure(state="normal")
            field.delete("1.0", tk.END)
            field.insert("1.0", text)
        else:
            field.configure(state="normal")
            field.delete(0, tk.END)
            field.insert(0, text)
            field.configure(state="readonly" if read_only else "normal")

    def show_current():
        if not filtered_rows:
            for field in fields.values():
                set_field(field, "")
            status_label.configure(text="0 records")
            return
        row = filtered_rows[current_index]
        for column, value in zip(columns, row):
            set_field(fields[column], value)
        status_label.configure(
            text=f"Record {current_index + 1} of {len(filtered_rows)}")
        goto_entry.delete(0, tk.END)
        goto_entry.insert(0, str(current_index + 1))

    def apply_filter():
        nonlocal filtered_rows, current_index
        expression = filter_entry.get().strip()
        exclude_note_expression = exclude_note_filter_entry.get().strip()
        exclude_name_expression = exclude_name_filter_entry.get().strip()
        try:
            match_pattern = re.compile(
                expression, re.IGNORECASE) if expression else None
            exclude_note_pattern = re.compile(
                exclude_note_expression, re.IGNORECASE
            ) if exclude_note_expression else None
            exclude_name_pattern = re.compile(
                exclude_name_expression, re.IGNORECASE
            ) if exclude_name_expression else None
        except re.error as error:
            messagebox.showerror("Invalid regex", str(error))
            return
        filtered_rows = [
            row for row in rows
            if (place_type_filter is None
                or row[columns.index("PlaceType")] == place_type_filter)
            and (match_pattern is None or match_pattern.search("\x1f".join(
                "" if value is None else str(value) for value in row)))
            and (exclude_note_pattern is None or not exclude_note_pattern.search(
                "" if row[note_column_index] is None
                else str(row[note_column_index])))
            and (exclude_name_pattern is None or not exclude_name_pattern.search(
                "" if row[name_column_index] is None
                else str(row[name_column_index])))
        ]
        current_index = 0
        show_current()

    def move_record(offset):
        nonlocal current_index
        if filtered_rows:
            current_index = max(0, min(
                len(filtered_rows) - 1, current_index + offset))
            show_current()

    def goto_record():
        nonlocal current_index
        try:
            requested = int(goto_entry.get())
        except ValueError:
            messagebox.showerror("Invalid record number",
                                 "Enter a whole number.")
            return
        if not 1 <= requested <= len(filtered_rows):
            messagebox.showerror(
                "Invalid record number",
                f"Enter a number from 1 to {len(filtered_rows)}.")
            return
        current_index = requested - 1
        show_current()

    def save_record():
        nonlocal rows
        if not filtered_rows:
            messagebox.showerror("No record", "There is no record to save.")
            return

        current_row = filtered_rows[current_index]
        key_column = columns[0]
        key_value = current_row[0]
        values = []
        for column in columns[1:]:
            field = fields[column]
            if column == utc_mod_date_column:
                values.append(current_row[columns.index(column)])
            elif isinstance(field, tk.Text):
                values.append(field.get("1.0", tk.END).rstrip("\n"))
            else:
                values.append(field.get())

        changes = [
            (column, old_value, new_value)
            for column, old_value, new_value in zip(
                columns[1:], current_row[1:], values)
            if ("" if old_value is None else str(old_value)) != new_value
        ]
        if not changes:
            messagebox.showinfo("No changes", "The record was not changed.")
            return

        quoted_key = key_column.replace(chr(34), chr(34) * 2)
        set_clause = ", ".join(
            f'"{column.replace(chr(34), chr(34) * 2)}" = ?'
            for column in columns[1:])
        try:
            db_connection.execute(
                f'UPDATE "{table_name}" SET {set_clause} '
                f'WHERE "{quoted_key}" = ?', values + [key_value])
            db_connection.commit()
            report_file.write(
                f"\nPlaceTable record changed: {key_column} = {key_value}\n")
            for column, old_value, new_value in changes:
                report_file.write(
                    f"  {column}: before={old_value!r}\n\nafter={new_value!r}\n")
            report_file.flush()
            messagebox.showinfo("Saved", f"Record {key_value} was saved.")
        except Exception as error:
            db_connection.rollback()
            messagebox.showerror("Database error", str(error))
            return

        rows = db_connection.execute(
            f"SELECT {column_sql} FROM {table_name} "
            f'ORDER BY "{quoted_key}"').fetchall()
        apply_filter()

    def update_utc_mod_date():
        nonlocal rows
        if not filtered_rows:
            messagebox.showerror("No record", "There is no record to update.")
            return

        current_row = filtered_rows[current_index]
        key_column = columns[0]
        key_value = current_row[0]
        old_value = current_row[columns.index(utc_mod_date_column)]
        quoted_key = key_column.replace(chr(34), chr(34) * 2)
        quoted_utc_column = utc_mod_date_column.replace(
            chr(34), chr(34) * 2)
        try:
            new_value = db_connection.execute(
                "SELECT julianday('now') - 2415018.5").fetchone()[0]
            db_connection.execute(
                f'UPDATE "{table_name}" SET "{quoted_utc_column}" = ? '
                f'WHERE "{quoted_key}" = ?', (new_value, key_value))
            db_connection.commit()
            report_file.write(
                f"\nPlaceTable record changed: {key_column} = {key_value}\n"
                f"  {utc_mod_date_column}: before={old_value!r}, "
                f"after={new_value!r}\n")
            report_file.flush()
        except Exception as error:
            db_connection.rollback()
            messagebox.showerror("Database error", str(error))
            return

        rows = db_connection.execute(
            f"SELECT {column_sql} FROM {table_name} "
            f'ORDER BY "{quoted_key}"').fetchall()
        apply_filter()

    ttk.Button(filter_frame, text="Apply",
               command=apply_filter).grid(row=3, column=0, sticky="w", pady=2)
    ttk.Button(navigation, text="Previous", command=lambda: move_record(-1)).pack(
        side="right", padx=2)
    ttk.Button(navigation, text="Next", command=lambda: move_record(1)).pack(
        side="right", padx=2)
    ttk.Button(navigation, text="Go to record", command=goto_record).pack(
        side="left")
    ttk.Button(navigation, text="Save record", command=save_record).pack(
        side="left", padx=(8, 0))
    filter_entry.bind("<Return>", lambda event: apply_filter())
    exclude_note_filter_entry.bind("<Return>", lambda event: apply_filter())
    exclude_name_filter_entry.bind("<Return>", lambda event: apply_filter())
    goto_entry.bind("<Return>", lambda event: goto_record())

    def show_startup_reminder():
        messagebox.showwarning(
            "RootsMagic reminder",
            "Run 'Rebuild indexes' tool immediately after opening in RootsMagic.",
            parent=root)
        root.deiconify()
        root.lift()
        root.focus_force()

    apply_filter()
    root.after_idle(show_startup_reminder)
    root.mainloop()


# ===================================================DIV60==
# Call the "main" function
if __name__ == '__main__':
    main()

# ===================================================DIV60==
