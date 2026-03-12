import os
import sqlite3
import ctypes
import ctypes.wintypes as wintypes
from pathlib import Path


def main():
    db_path = Path(r"C:\Users\rotter\Genealogy\GeneDB\Otter-Saito.rmtree")

    sql = """
        SELECT PlaceID, Name
        FROM (
            SELECT PlaceID, Name COLLATE NOCASE
            FROM PlaceTable
            WHERE PlaceType = 0
            ORDER BY PlaceID DESC
            LIMIT 30
        )
        ORDER BY PlaceID ASC;
    """

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    print("The last nn places entered into RM\n")

    for pid, name in cur.execute(sql):
        print(f"{pid:6}  {name}")

    conn.close()

    if launched_from_explorer():
        input("\nPress Enter to exit...")


# -------------------------
# Helper functions below
# -------------------------

# Define ULONG_PTR manually for 32/64-bit compatibility
if ctypes.sizeof(ctypes.c_void_p) == 8:
    ULONG_PTR = ctypes.c_uint64
else:
    ULONG_PTR = ctypes.c_uint32

PROCESS_QUERY_LIMITED_INFORMATION = 0x1000

class PROCESS_BASIC_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("ExitStatus", wintypes.LONG),
        ("PebBaseAddress", wintypes.LPVOID),
        ("AffinityMask", ULONG_PTR),
        ("BasePriority", wintypes.LONG),
        ("UniqueProcessId", ULONG_PTR),
        ("InheritedFromUniqueProcessId", ULONG_PTR),
    ]

ntdll = ctypes.WinDLL("ntdll")
kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)

NtQueryInformationProcess = ntdll.NtQueryInformationProcess
NtQueryInformationProcess.restype = wintypes.LONG


def get_parent_pid(pid):
    pbi = PROCESS_BASIC_INFORMATION()
    h = kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
    if not h:
        return None
    try:
        status = NtQueryInformationProcess(
            h, 0, ctypes.byref(pbi), ctypes.sizeof(pbi), None
        )
        if status != 0:
            return None
        return pbi.InheritedFromUniqueProcessId
    finally:
        kernel32.CloseHandle(h)


def get_process_name(pid):
    h = kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
    if not h:
        return None
    try:
        buf = (ctypes.c_wchar * 260)()
        size = wintypes.DWORD(260)
        if kernel32.QueryFullProcessImageNameW(h, 0, buf, ctypes.byref(size)):
            return Path(buf.value).name.lower()
    finally:
        kernel32.CloseHandle(h)
    return None


def launched_from_explorer():
    """Detect double-click launch by checking grandparent process."""
    pid = os.getpid()
    parent = get_parent_pid(pid)
    if not parent:
        return False

    grandparent = get_parent_pid(parent)
    if not grandparent:
        return False

    gp_name = get_process_name(grandparent)
    return gp_name == "explorer.exe"


if __name__ == "__main__":
    main()