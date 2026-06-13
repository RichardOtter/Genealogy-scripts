import os
import ctypes
import ctypes.wintypes as wintypes
from pathlib import Path


# -------------------------
# Helper functions to determine launching method
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
