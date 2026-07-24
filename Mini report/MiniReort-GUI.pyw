#!/usr/bin/env python3
import sqlite3
import pyperclip
import re
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
import os

# ------------------------------------------------------------
# Hard‑coded RM database path
# ------------------------------------------------------------
DBPath = r"C:\Users\rotter\Genealogy\GeneDB\Otter-Saito.rmtree"

# ------------------------------------------------------------
# Config file for saving auto-close state and delay
# ------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CFG_FILE = os.path.join(BASE_DIR, "minireport.cfg")


def load_config():
    auto_close = 0
    delay_ms = 3000

    if not os.path.exists(CFG_FILE):
        return auto_close, delay_ms

    try:
        with open(CFG_FILE, "r") as f:
            for line in f:
                if line.startswith("auto_close="):
                    auto_close = int(line.split("=")[1].strip())
                elif line.startswith("delay_ms="):
                    delay_ms = int(line.split("=")[1].strip())
    except (OSError, ValueError):
        pass

    return auto_close, delay_ms


def save_config(auto_close_value, delay_ms_value):
    try:
        with open(CFG_FILE, "w") as f:
            f.write(f"auto_close={auto_close_value}\n")
            f.write(f"delay_ms={delay_ms_value}\n")
    except OSError:
        pass

# ------------------------------------------------------------
# Utility functions
# ------------------------------------------------------------


def format_rm_date(raw):
    if not raw:
        return ""

    m = re.search(r"(\d{8})", raw)
    if not m:
        return ""

    ymd = m.group(1)
    year = int(ymd[0:4])
    month = int(ymd[4:6])
    day = int(ymd[6:8])

    if year == 0:
        return ""

    if month == 0:
        return f"{year}"

    if day == 0:
        try:
            dt = datetime(year, month, 1)
            return dt.strftime("%b %Y")
        except ValueError:
            return f"{year}"

    try:
        dt = datetime(year, month, day)
        return dt.strftime("%d %b %Y")
    except ValueError:
        return f"{year}"


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

    return f"{line1}\n{line2}"

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


def run_report():
    pid_text = entry.get().strip()
    if not pid_text.isdigit():
        messagebox.showerror("Error", "PersonID must be numeric.")
        return

    person_id = int(pid_text)

    try:
        conn = sqlite3.connect(DBPath)
        report = generate_report(conn, person_id)
        conn.close()
    except Exception as e:
        messagebox.showerror("Database Error", str(e))
        return

    pyperclip.copy(report)

    output_box.config(state="normal")
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, report)
    output_box.config(state="disabled")

    save_config(auto_close_var.get(), delay_ms)

    if auto_close_var.get() == 1:
        root.after(delay_ms, root.destroy)


root = tk.Tk()
root.title("MiniReport")

auto_close, delay_ms = load_config()
auto_close_var = tk.IntVar(value=auto_close)

tk.Label(root, text="Enter PersonID:").pack(padx=10, pady=5)

entry = tk.Entry(root, width=20)
entry.pack(padx=10, pady=5)
entry.focus_set()  # ✔ cursor starts here
entry.bind("<Return>", lambda event: run_report())

tk.Checkbutton(root, text="Auto-close",
               variable=auto_close_var).pack(padx=10, pady=5)

tk.Button(root, text="Generate Report",
          command=run_report).pack(padx=10, pady=10)

output_box = tk.Text(root, width=50, height=4, state="disabled", bg="#f0f0f0")
output_box.pack(padx=10, pady=10)

root.update_idletasks()
center_window(root)

root.mainloop()
