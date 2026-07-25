#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.append(
    str(Path.resolve(Path(__file__).resolve().parent / '../RMpy package')))

import configparser
from tkinter import messagebox
import tkinter as tk
from datetime import datetime
import RMpy.launcher
import RMpy.RMDate


# ------------------------------------------------------------
# GUI state
# ------------------------------------------------------------
G_GUI_STATE = {}

def main():
    utility_info = {}
    utility_info["utility_name"] = "MiniReport"
    utility_info["utility_version"] = "UTILITY_VERSION_NUMBER_RM_UTILS_OVERRIDE"
    utility_info["config_file_name"] = "RM-Python-config.ini"
    utility_info["script_path"] = Path(__file__).parent.resolve()
    utility_info["run_features_function"] = build_gui
    utility_info["allow_db_changes"] = False
    utility_info["RMNOCASE_required"] = False
    utility_info["RMNOCASE_optional"] = False
    utility_info["RegExp_required"] = False
    utility_info["RegExp_optional"] = False
    utility_info["ReportFile_no_display"] = True

    RMpy.launcher.launcher(utility_info)


def build_gui(config, db_connection, report_file):
    G_GUI_STATE.clear()

    root = tk.Tk()
    root.title("MiniReport")
    root.db_connection = db_connection

    auto_close, delay_ms_value = load_config(config)

    G_GUI_STATE["root"] = root
    G_GUI_STATE["delay_ms"] = delay_ms_value
    G_GUI_STATE["auto_close"] = auto_close

    tk.Label(root, text="Enter PersonID:").pack(padx=10, pady=5)

    entry = tk.Entry(root, width=20)
    entry.pack(padx=10, pady=5)
    entry.focus_set()
    entry.bind("<Return>", lambda event: run_report(root.db_connection))
    G_GUI_STATE["entry"] = entry

    tk.Button(root, text="Generate Report",
              command=lambda: run_report(root.db_connection)).pack(padx=10, pady=10)

    output_box = tk.Text(root, width=50, height=4,
                         state="disabled", bg="#f0f0f0")
    output_box.pack(padx=10, pady=10)
    G_GUI_STATE["output_box"] = output_box

    root.update_idletasks()
    center_window(root)

    root.mainloop()


def load_config(config):
    auto_close = 1
    delay_ms = 3000

    try:
        auto_close_value = config['OPTIONS']['AUTO_CLOSE']
        auto_close = 1 if str(auto_close_value).strip().lower() in {'1', 'true', 'yes', 'on'} else 0
    except (KeyError, configparser.Error, ValueError):
        auto_close = 1

    try:
        delay_ms = int(config['OPTIONS']['AUTO_CLOSE_DELAY_MS'])
    except (KeyError, configparser.Error, ValueError):
        delay_ms = 3000

    return auto_close, delay_ms


# ------------------------------------------------------------
# Utility functions
# ------------------------------------------------------------


def get_primary_name(conn, person_id):
    cur = conn.execute("""
        SELECT Given, Surname
        FROM NameTable
        WHERE OwnerID = ?
          AND IsPrimary = 1
        LIMIT 1;
    """, (person_id,))
    row = cur.fetchone()
    if row:
        return row[0] or "", row[1] or ""
    return "", ""


def get_birth_death(conn, person_id):
    cur = conn.execute("""
        SELECT EventType, Date
        FROM EventTable
        WHERE OwnerType = 0
          AND OwnerID = ?
          AND (EventType = 1 OR EventType = 2);
    """, (person_id,))
    birth = ""
    death = ""
    for etype, date in cur.fetchall():
        if etype == 1:
            birth = format_rm_date(date or "")
        elif etype == 2:
            death = format_rm_date(date or "")
    return birth, death


def get_parents(conn, person_id):
    cur = conn.execute("""
        SELECT FamilyID
        FROM ChildTable
        WHERE ChildID = ?
        LIMIT 1;
    """, (person_id,))
    row = cur.fetchone()
    if not row:
        return None, None

    family_id = row[0]

    cur = conn.execute("""
        SELECT FatherID, MotherID
        FROM FamilyTable
        WHERE FamilyID = ?
        LIMIT 1;
    """, (family_id,))
    row = cur.fetchone()
    if row:
        return row[0], row[1]
    return None, None


def get_sex_word(conn, person_id):
    cur = conn.execute(
        "SELECT Sex FROM PersonTable WHERE PersonID = ?", (person_id,))
    row = cur.fetchone()
    if not row:
        return "child"

    sex_id = row[0]
    cur = conn.execute(
        "SELECT SexType FROM LU_SexType WHERE SexID = ?", (sex_id,))
    row = cur.fetchone()
    if not row or not row[0]:
        return "child"

    sex_type = row[0].strip().lower()
    if sex_type.startswith("m"):
        return "son"
    elif sex_type.startswith("f"):
        return "daughter"
    return "child"

# ------------------------------------------------------------
# Report generator
# ------------------------------------------------------------


def generate_report(conn, person_id):
    given, surname = get_primary_name(conn, person_id)
    birth, death = get_birth_death(conn, person_id)
    father_id, mother_id = get_parents(conn, person_id)

    father_name = ""
    mother_name = ""

    if father_id:
        fg, fs = get_primary_name(conn, father_id)
        father_name = f"{fg} {fs}".strip()

    if mother_id:
        mg, ms = get_primary_name(conn, mother_id)
        mother_name = f"{mg} {ms}".strip()

    relation_word = get_sex_word(conn, person_id)

    line1 = f"RMID-{person_id}    {given} {surname}".strip()
    if birth or death:
        line1 += " "
        if birth:
            line1 += f"-b {birth}"
        if birth and death:
            line1 += ", "
        if death:
            line1 += f"-d {death}"

    if father_name or mother_name:
        if father_name and mother_name:
            line2 = f"{relation_word} of {father_name} and {mother_name}"
        elif father_name:
            line2 = f"{relation_word} of {father_name}"
        else:
            line2 = f"{relation_word} of {mother_name}"
    else:
        line2 = ""

    return f"{line1}\n{line2}\n"


def format_rm_date(raw):
    if not raw:
        return ""
    try:
        return RMpy.RMDate.RMDate_str_TO_en_str(raw, RMpy.RMDate.Format.SHORT)
    except Exception:
        return ""

# ------------------------------------------------------------
# GUI
# ------------------------------------------------------------


def center_window(win):
    win.update_idletasks()
    w = win.winfo_width()
    h = win.winfo_height()
    sw = win.winfo_screenwidth()
    sh = win.winfo_screenheight()
    x = (sw - w) // 2
    y = (sh - h) // 2
    win.geometry(f"{w}x{h}+{x}+{y}")


def copy_to_clipboard(text):
    if not G_GUI_STATE.get("root"):
        return
    root = G_GUI_STATE["root"]
    root.clipboard_clear()
    root.clipboard_append(text)
    root.update()


def run_report(conn=None):
    entry = G_GUI_STATE.get("entry")
    output_box = G_GUI_STATE.get("output_box")
    if entry is None or output_box is None:
        return

    pid_text = entry.get().strip()
    if not pid_text.isdigit():
        messagebox.showerror("Error", "PersonID must be numeric.")
        return

    person_id = int(pid_text)

    if conn is None:
        conn = getattr(root, "db_connection", None)
    if conn is None:
        messagebox.showerror(
            "Database Error", "No database connection available.")
        return

    try:
        report = generate_report(conn, person_id)
    except Exception as e:
        messagebox.showerror("Database Error", str(e))
        return

    copy_to_clipboard(report)

    output_box.config(state="normal")
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, report)
    output_box.config(state="disabled")

    if G_GUI_STATE.get("auto_close", 1) == 1:
        root = G_GUI_STATE.get("root")
        if root is not None:
            root.after(G_GUI_STATE.get("delay_ms", 3000), root.destroy)



if __name__ == "__main__":
    main()
