import sys
sys.dont_write_bytecode = True

import os
import math
import time
import json
import random
import re
import threading
import subprocess
import queue
import locale
from collections import deque
import colorsys
import hashlib
import shutil
import logging
from logging.handlers import RotatingFileHandler
from decimal import Decimal, InvalidOperation, localcontext
from pathlib import Path


import ctypes
from ctypes import wintypes
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

ULONG_PTR = ctypes.c_size_t
UINT_PTR = ctypes.c_size_t
LRESULT = ctypes.c_ssize_t
INPUT_TAG = 0x4D4942472026
RAW_INPUT_TAG = INPUT_TAG & 0xFFFFFFFF
INPUT_MOUSE = 0
INPUT_KEYBOARD = 1
MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_RIGHTDOWN = 0x0008
MOUSEEVENTF_RIGHTUP = 0x0010
MOUSEEVENTF_MIDDLEDOWN = 0x0020
MOUSEEVENTF_MIDDLEUP = 0x0040
MOUSEEVENTF_XDOWN = 0x0080
MOUSEEVENTF_XUP = 0x0100
MOUSEEVENTF_WHEEL = 0x0800
MOUSEEVENTF_HWHEEL = 0x01000
MOUSEEVENTF_VIRTUALDESK = 0x4000
MOUSEEVENTF_ABSOLUTE = 0x8000
KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP = 0x0002
KEYEVENTF_UNICODE = 0x0004
KEYEVENTF_SCANCODE = 0x0008
MOUSEEVENTF_MOVE_NOCOALESCE = 0x2000
WH_KEYBOARD_LL = 13
WH_MOUSE_LL = 14
WM_QUIT = 0x0012
WM_INPUT = 0x00FF
WM_TIMER = 0x0113
RIDEV_REMOVE = 0x00000001
RIDEV_INPUTSINK = 0x00000100
RID_INPUT = 0x10000003
RIM_TYPEMOUSE = 0
RIM_TYPEKEYBOARD = 1
RI_KEY_BREAK = 0x0001
RI_KEY_E0 = 0x0002
RI_KEY_E1 = 0x0004
RI_MOUSE_LEFT_BUTTON_DOWN = 0x0001
RI_MOUSE_LEFT_BUTTON_UP = 0x0002
RI_MOUSE_RIGHT_BUTTON_DOWN = 0x0004
RI_MOUSE_RIGHT_BUTTON_UP = 0x0008
RI_MOUSE_MIDDLE_BUTTON_DOWN = 0x0010
RI_MOUSE_MIDDLE_BUTTON_UP = 0x0020
RI_MOUSE_BUTTON_4_DOWN = 0x0040
RI_MOUSE_BUTTON_4_UP = 0x0080
RI_MOUSE_BUTTON_5_DOWN = 0x0100
RI_MOUSE_BUTTON_5_UP = 0x0200
HID_USAGE_PAGE_GENERIC = 0x01
HID_USAGE_GENERIC_MOUSE = 0x02
HID_USAGE_GENERIC_KEYBOARD = 0x06
WM_KEYDOWN = 0x0100
WM_KEYUP = 0x0101
WM_SYSKEYDOWN = 0x0104
WM_SYSKEYUP = 0x0105
WM_MOUSEMOVE = 0x0200
WM_LBUTTONDOWN = 0x0201
WM_LBUTTONUP = 0x0202
WM_RBUTTONDOWN = 0x0204
WM_RBUTTONUP = 0x0205
WM_MBUTTONDOWN = 0x0207
WM_MBUTTONUP = 0x0208
WM_XBUTTONDOWN = 0x020B
WM_XBUTTONUP = 0x020C
WM_GETTEXT = 0x000D
WM_GETTEXTLENGTH = 0x000E
EM_SETSEL = 0x00B1
EM_REPLACESEL = 0x00C2
SMTO_ABORTIFHUNG = 0x0002
GWL_STYLE = -16
ES_PASSWORD = 0x0020
GA_ROOT = 2
FILE_ATTRIBUTE_REPARSE_POINT = 0x00000400
INVALID_FILE_ATTRIBUTES = 0xFFFFFFFF
FILE_READ_ATTRIBUTES = 0x0080
FILE_SHARE_READ = 0x00000001
FILE_SHARE_WRITE = 0x00000002
FILE_SHARE_DELETE = 0x00000004
OPEN_EXISTING = 3
FILE_FLAG_BACKUP_SEMANTICS = 0x02000000

class MOUSEINPUT(ctypes.Structure):
    _fields_ = [("dx", wintypes.LONG), ("dy", wintypes.LONG), ("mouseData", wintypes.DWORD),
                ("dwFlags", wintypes.DWORD), ("time", wintypes.DWORD), ("dwExtraInfo", ULONG_PTR)]

class KEYBDINPUT(ctypes.Structure):
    _fields_ = [("wVk", wintypes.WORD), ("wScan", wintypes.WORD), ("dwFlags", wintypes.DWORD),
                ("time", wintypes.DWORD), ("dwExtraInfo", ULONG_PTR)]

class HARDWAREINPUT(ctypes.Structure):
    _fields_ = [("uMsg", wintypes.DWORD), ("wParamL", wintypes.WORD), ("wParamH", wintypes.WORD)]

class INPUTUNION(ctypes.Union):
    _fields_ = [("mi", MOUSEINPUT), ("ki", KEYBDINPUT), ("hi", HARDWAREINPUT)]

class INPUT(ctypes.Structure):
    _anonymous_ = ("u",)
    _fields_ = [("type", wintypes.DWORD), ("u", INPUTUNION)]

class MSLLHOOKSTRUCT(ctypes.Structure):
    _fields_ = [("pt", wintypes.POINT), ("mouseData", wintypes.DWORD), ("flags", wintypes.DWORD),
                ("time", wintypes.DWORD), ("dwExtraInfo", ULONG_PTR)]

class KBDLLHOOKSTRUCT(ctypes.Structure):
    _fields_ = [("vkCode", wintypes.DWORD), ("scanCode", wintypes.DWORD), ("flags", wintypes.DWORD),
                ("time", wintypes.DWORD), ("dwExtraInfo", ULONG_PTR)]

class RAWINPUTDEVICE(ctypes.Structure):
    _fields_ = [
        ("usUsagePage", wintypes.USHORT), ("usUsage", wintypes.USHORT),
        ("dwFlags", wintypes.DWORD), ("hwndTarget", wintypes.HWND),
    ]

class RAWINPUTHEADER(ctypes.Structure):
    _fields_ = [
        ("dwType", wintypes.DWORD), ("dwSize", wintypes.DWORD),
        ("hDevice", wintypes.HANDLE), ("wParam", wintypes.WPARAM),
    ]

class RAWMOUSEBUTTONS(ctypes.Structure):
    _fields_ = [("usButtonFlags", wintypes.USHORT), ("usButtonData", wintypes.USHORT)]

class RAWMOUSEBUTTONUNION(ctypes.Union):
    _anonymous_ = ("buttons",)
    _fields_ = [("ulButtons", wintypes.ULONG), ("buttons", RAWMOUSEBUTTONS)]

class RAWMOUSE(ctypes.Structure):
    _anonymous_ = ("button_union",)
    _fields_ = [
        ("usFlags", wintypes.USHORT), ("button_union", RAWMOUSEBUTTONUNION),
        ("ulRawButtons", wintypes.ULONG), ("lLastX", wintypes.LONG), ("lLastY", wintypes.LONG),
        ("ulExtraInformation", wintypes.ULONG),
    ]

class RAWKEYBOARD(ctypes.Structure):
    _fields_ = [
        ("MakeCode", wintypes.USHORT), ("Flags", wintypes.USHORT), ("Reserved", wintypes.USHORT),
        ("VKey", wintypes.USHORT), ("Message", wintypes.UINT), ("ExtraInformation", wintypes.ULONG),
    ]

class RAWHID(ctypes.Structure):
    _fields_ = [("dwSizeHid", wintypes.DWORD), ("dwCount", wintypes.DWORD), ("bRawData", ctypes.c_ubyte * 1)]

class RAWINPUTDATA(ctypes.Union):
    _fields_ = [("mouse", RAWMOUSE), ("keyboard", RAWKEYBOARD), ("hid", RAWHID)]

class RAWINPUT(ctypes.Structure):
    _fields_ = [("header", RAWINPUTHEADER), ("data", RAWINPUTDATA)]

WNDPROC = ctypes.WINFUNCTYPE(LRESULT, wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM)

class WNDCLASSW(ctypes.Structure):
    _fields_ = [
        ("style", wintypes.UINT), ("lpfnWndProc", WNDPROC), ("cbClsExtra", ctypes.c_int),
        ("cbWndExtra", ctypes.c_int), ("hInstance", wintypes.HINSTANCE), ("hIcon", wintypes.HANDLE),
        ("hCursor", wintypes.HANDLE), ("hbrBackground", wintypes.HANDLE),
        ("lpszMenuName", wintypes.LPCWSTR), ("lpszClassName", wintypes.LPCWSTR),
    ]

class GUITHREADINFO(ctypes.Structure):
    _fields_ = [
        ("cbSize", wintypes.DWORD), ("flags", wintypes.DWORD),
        ("hwndActive", wintypes.HWND), ("hwndFocus", wintypes.HWND),
        ("hwndCapture", wintypes.HWND), ("hwndMenuOwner", wintypes.HWND),
        ("hwndMoveSize", wintypes.HWND), ("hwndCaret", wintypes.HWND),
        ("rcCaret", wintypes.RECT),
    ]

HOOKPROC = ctypes.WINFUNCTYPE(LRESULT, ctypes.c_int, wintypes.WPARAM, wintypes.LPARAM)
WNDENUMPROC = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
kernel32.GetModuleHandleW.argtypes = (wintypes.LPCWSTR,)
kernel32.GetModuleHandleW.restype = wintypes.HMODULE
kernel32.GetConsoleWindow.argtypes = ()
kernel32.GetConsoleWindow.restype = wintypes.HWND
kernel32.GetCurrentThreadId.argtypes = ()
kernel32.GetCurrentThreadId.restype = wintypes.DWORD
user32.ShowWindow.argtypes = (wintypes.HWND, ctypes.c_int)
user32.ShowWindow.restype = wintypes.BOOL
user32.GetCursorPos.argtypes = (ctypes.POINTER(wintypes.POINT),)
user32.GetCursorPos.restype = wintypes.BOOL
user32.GetSystemMetrics.argtypes = (ctypes.c_int,)
user32.GetSystemMetrics.restype = ctypes.c_int
user32.GetMessageW.argtypes = (ctypes.POINTER(wintypes.MSG), wintypes.HWND, wintypes.UINT, wintypes.UINT)
user32.GetMessageW.restype = wintypes.BOOL
user32.TranslateMessage.argtypes = (ctypes.POINTER(wintypes.MSG),)
user32.TranslateMessage.restype = wintypes.BOOL
user32.DispatchMessageW.argtypes = (ctypes.POINTER(wintypes.MSG),)
user32.DispatchMessageW.restype = LRESULT
user32.SendInput.argtypes = (wintypes.UINT, ctypes.POINTER(INPUT), ctypes.c_int)
user32.SendInput.restype = wintypes.UINT
user32.GetForegroundWindow.restype = wintypes.HWND
user32.WindowFromPoint.argtypes = (wintypes.POINT,)
user32.WindowFromPoint.restype = wintypes.HWND
user32.GetAncestor.argtypes = (wintypes.HWND, wintypes.UINT)
user32.GetAncestor.restype = wintypes.HWND
user32.GetClassNameW.argtypes = (wintypes.HWND, wintypes.LPWSTR, ctypes.c_int)
user32.GetClassNameW.restype = ctypes.c_int
user32.GetWindowTextLengthW.argtypes = (wintypes.HWND,)
user32.GetWindowTextLengthW.restype = ctypes.c_int
user32.GetWindowTextW.argtypes = (wintypes.HWND, wintypes.LPWSTR, ctypes.c_int)
user32.GetWindowTextW.restype = ctypes.c_int
user32.GetWindowLongW.argtypes = (wintypes.HWND, ctypes.c_int)
user32.GetWindowLongW.restype = wintypes.LONG
user32.SendMessageTimeoutW.argtypes = (
    wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM,
    wintypes.UINT, wintypes.UINT, ctypes.POINTER(ULONG_PTR),
)
user32.SendMessageTimeoutW.restype = LRESULT
user32.EnumChildWindows.argtypes = (wintypes.HWND, WNDENUMPROC, wintypes.LPARAM)
user32.EnumChildWindows.restype = wintypes.BOOL
user32.IsWindowVisible.argtypes = (wintypes.HWND,)
user32.IsWindowVisible.restype = wintypes.BOOL
user32.SetWindowsHookExW.argtypes = (ctypes.c_int, HOOKPROC, wintypes.HINSTANCE, wintypes.DWORD)
user32.SetWindowsHookExW.restype = wintypes.HHOOK
user32.CallNextHookEx.argtypes = (wintypes.HHOOK, ctypes.c_int, wintypes.WPARAM, wintypes.LPARAM)
user32.CallNextHookEx.restype = LRESULT
user32.UnhookWindowsHookEx.argtypes = (wintypes.HHOOK,)
user32.UnhookWindowsHookEx.restype = wintypes.BOOL
user32.PostThreadMessageW.argtypes = (wintypes.DWORD, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM)
user32.PostThreadMessageW.restype = wintypes.BOOL
user32.RegisterRawInputDevices.argtypes = (ctypes.POINTER(RAWINPUTDEVICE), wintypes.UINT, wintypes.UINT)
user32.RegisterRawInputDevices.restype = wintypes.BOOL
user32.GetRawInputData.argtypes = (wintypes.HANDLE, wintypes.UINT, ctypes.c_void_p, ctypes.POINTER(wintypes.UINT), wintypes.UINT)
user32.GetRawInputData.restype = wintypes.UINT
user32.RegisterClassW.argtypes = (ctypes.POINTER(WNDCLASSW),)
user32.RegisterClassW.restype = wintypes.ATOM
user32.UnregisterClassW.argtypes = (wintypes.LPCWSTR, wintypes.HINSTANCE)
user32.UnregisterClassW.restype = wintypes.BOOL
user32.CreateWindowExW.argtypes = (
    wintypes.DWORD, wintypes.LPCWSTR, wintypes.LPCWSTR, wintypes.DWORD,
    ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, wintypes.HWND,
    wintypes.HMENU, wintypes.HINSTANCE, ctypes.c_void_p,
)
user32.CreateWindowExW.restype = wintypes.HWND
user32.DestroyWindow.argtypes = (wintypes.HWND,)
user32.DestroyWindow.restype = wintypes.BOOL
user32.DefWindowProcW.argtypes = (wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM)
user32.DefWindowProcW.restype = LRESULT
user32.SetTimer.argtypes = (wintypes.HWND, UINT_PTR, wintypes.UINT, ctypes.c_void_p)
user32.SetTimer.restype = UINT_PTR
user32.KillTimer.argtypes = (wintypes.HWND, UINT_PTR)
user32.KillTimer.restype = wintypes.BOOL
user32.SetWindowPos.argtypes = (wintypes.HWND, wintypes.HWND, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, wintypes.UINT)
user32.SetWindowPos.restype = wintypes.BOOL
user32.GetWindowRect.argtypes = (wintypes.HWND, ctypes.POINTER(wintypes.RECT))
user32.GetWindowRect.restype = wintypes.BOOL
user32.GetWindowThreadProcessId.argtypes = (wintypes.HWND, ctypes.POINTER(wintypes.DWORD))
user32.GetWindowThreadProcessId.restype = wintypes.DWORD
user32.GetGUIThreadInfo.argtypes = (wintypes.DWORD, ctypes.POINTER(GUITHREADINFO))
user32.GetGUIThreadInfo.restype = wintypes.BOOL
try:
    user32.GetDpiForWindow.argtypes = (wintypes.HWND,)
    user32.GetDpiForWindow.restype = wintypes.UINT
except Exception:
    pass

class MEMORYSTATUSEX(ctypes.Structure):
    _fields_ = [
        ("dwLength", wintypes.DWORD), ("dwMemoryLoad", wintypes.DWORD),
        ("ullTotalPhys", ctypes.c_ulonglong), ("ullAvailPhys", ctypes.c_ulonglong),
        ("ullTotalPageFile", ctypes.c_ulonglong), ("ullAvailPageFile", ctypes.c_ulonglong),
        ("ullTotalVirtual", ctypes.c_ulonglong), ("ullAvailVirtual", ctypes.c_ulonglong),
        ("ullAvailExtendedVirtual", ctypes.c_ulonglong),
    ]

kernel32.GlobalMemoryStatusEx.argtypes = (ctypes.POINTER(MEMORYSTATUSEX),)
kernel32.GlobalMemoryStatusEx.restype = wintypes.BOOL

class FILETIME(ctypes.Structure):
    _fields_ = [("dwLowDateTime", wintypes.DWORD), ("dwHighDateTime", wintypes.DWORD)]

kernel32.GetSystemTimes.argtypes = (ctypes.POINTER(FILETIME), ctypes.POINTER(FILETIME), ctypes.POINTER(FILETIME))
kernel32.GetSystemTimes.restype = wintypes.BOOL
kernel32.GetFileAttributesW.argtypes = (wintypes.LPCWSTR,)
kernel32.GetFileAttributesW.restype = wintypes.DWORD
kernel32.CreateFileW.argtypes = (
    wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD, ctypes.c_void_p,
    wintypes.DWORD, wintypes.DWORD, wintypes.HANDLE,
)
kernel32.CreateFileW.restype = wintypes.HANDLE
kernel32.GetFinalPathNameByHandleW.argtypes = (wintypes.HANDLE, wintypes.LPWSTR, wintypes.DWORD, wintypes.DWORD)
kernel32.GetFinalPathNameByHandleW.restype = wintypes.DWORD
kernel32.GetDriveTypeW.argtypes = (wintypes.LPCWSTR,)
kernel32.GetDriveTypeW.restype = wintypes.UINT
kernel32.GetVolumePathNameW.argtypes = (wintypes.LPCWSTR, wintypes.LPWSTR, wintypes.DWORD)
kernel32.GetVolumePathNameW.restype = wintypes.BOOL
kernel32.GetVolumeNameForVolumeMountPointW.argtypes = (wintypes.LPCWSTR, wintypes.LPWSTR, wintypes.DWORD)
kernel32.GetVolumeNameForVolumeMountPointW.restype = wintypes.BOOL
kernel32.QueryDosDeviceW.argtypes = (wintypes.LPCWSTR, wintypes.LPWSTR, wintypes.DWORD)
kernel32.QueryDosDeviceW.restype = wintypes.DWORD
kernel32.CloseHandle.argtypes = (wintypes.HANDLE,)
kernel32.CloseHandle.restype = wintypes.BOOL
try:
    kernel32.GetActiveProcessorCount.argtypes = (wintypes.WORD,)
    kernel32.GetActiveProcessorCount.restype = wintypes.DWORD
except Exception:
    pass
try:
    user32.SetProcessDpiAwarenessContext(ctypes.c_void_p(-4))
except Exception:
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
    except Exception:
        pass

SW_HIDE = 0
HWND_TOPMOST = wintypes.HWND(-1)
SWP_NOACTIVATE = 0x0010
SWP_SHOWWINDOW = 0x0040
SYSTEM_DRIVE = os.environ.get("SystemDrive", "C:").upper().rstrip("\\/")
DRIVE_FIXED = 3
HWND_MESSAGE = wintypes.HWND(-3)


class StorageSafetyError(RuntimeError):
    pass


root = None
chosen_path = None
app_dir = None
deps_dir = None
gpu_deps_dir = None
temp_dir = None
storage_root_final = None
phase_var = None
status_var = None
detail_var = None
progress_var = None
progress_percent_var = None
status = None
detail_label = None
progress = None
number_button = None
free_button = None
hardware_var = None
learning_var = None
hardware_profile = None
active_gpu_pci_bus_id = None
runtime_logger = None
ui_queue = queue.Queue()
_cpu_sample_lock = threading.Lock()
_cpu_times_sample = None

app_alive = threading.Event()
app_alive.set()
shutdown_event = threading.Event()
shutdown_started = False
shutdown_lock = threading.Lock()
bootstrap_thread = None
hardware_thread = None
hook_thread = None
release_thread = None
scan_thread = None

child_processes = set()
child_process_lock = threading.Lock()
child_job_lock = threading.Lock()
child_job = None
JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE = 0x00002000
JOB_OBJECT_EXTENDED_LIMIT_INFORMATION_CLASS = 9


class JOBOBJECT_BASIC_LIMIT_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("PerProcessUserTimeLimit", ctypes.c_longlong),
        ("PerJobUserTimeLimit", ctypes.c_longlong),
        ("LimitFlags", wintypes.DWORD),
        ("MinimumWorkingSetSize", ctypes.c_size_t),
        ("MaximumWorkingSetSize", ctypes.c_size_t),
        ("ActiveProcessLimit", wintypes.DWORD),
        ("Affinity", ULONG_PTR),
        ("PriorityClass", wintypes.DWORD),
        ("SchedulingClass", wintypes.DWORD),
    ]


class IO_COUNTERS(ctypes.Structure):
    _fields_ = [
        ("ReadOperationCount", ctypes.c_ulonglong),
        ("WriteOperationCount", ctypes.c_ulonglong),
        ("OtherOperationCount", ctypes.c_ulonglong),
        ("ReadTransferCount", ctypes.c_ulonglong),
        ("WriteTransferCount", ctypes.c_ulonglong),
        ("OtherTransferCount", ctypes.c_ulonglong),
    ]


class JOBOBJECT_EXTENDED_LIMIT_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("BasicLimitInformation", JOBOBJECT_BASIC_LIMIT_INFORMATION),
        ("IoInfo", IO_COUNTERS),
        ("ProcessMemoryLimit", ctypes.c_size_t),
        ("JobMemoryLimit", ctypes.c_size_t),
        ("PeakProcessMemoryUsed", ctypes.c_size_t),
        ("PeakJobMemoryUsed", ctypes.c_size_t),
    ]


try:
    kernel32.CreateJobObjectW.argtypes = (ctypes.c_void_p, wintypes.LPCWSTR)
    kernel32.CreateJobObjectW.restype = wintypes.HANDLE
    kernel32.SetInformationJobObject.argtypes = (wintypes.HANDLE, ctypes.c_int, ctypes.c_void_p, wintypes.DWORD)
    kernel32.SetInformationJobObject.restype = wintypes.BOOL
    kernel32.AssignProcessToJobObject.argtypes = (wintypes.HANDLE, wintypes.HANDLE)
    kernel32.AssignProcessToJobObject.restype = wintypes.BOOL
    kernel32.CloseHandle.argtypes = (wintypes.HANDLE,)
    kernel32.CloseHandle.restype = wintypes.BOOL
except Exception:
    pass


def _shutdown_requested():
    return shutdown_event.is_set() or not app_alive.is_set()


def _ensure_child_job():
    global child_job
    if shutdown_event.is_set():
        return None
    if child_job is not None:
        return child_job
    with child_job_lock:
        if child_job is not None:
            return child_job
        try:
            job = kernel32.CreateJobObjectW(None, None)
            if not job:
                return None
            info = JOBOBJECT_EXTENDED_LIMIT_INFORMATION()
            info.BasicLimitInformation.LimitFlags = JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
            if not kernel32.SetInformationJobObject(
                job, JOB_OBJECT_EXTENDED_LIMIT_INFORMATION_CLASS, ctypes.byref(info), ctypes.sizeof(info)
            ):
                kernel32.CloseHandle(job)
                return None
            child_job = job
        except Exception:
            child_job = None
        return child_job


def _assign_child_to_job(proc):
    job = _ensure_child_job()
    if job is None:
        return
    try:
        handle = getattr(proc, "_handle", None)
        if handle:
            kernel32.AssignProcessToJobObject(job, wintypes.HANDLE(handle))
    except Exception:
        pass


def _terminate_process(proc):
    if proc is None or proc.poll() is not None:
        return
    try:
        proc.terminate()
    except Exception:
        pass
    try:
        proc.wait(timeout=0.8)
        return
    except Exception:
        pass
    try:
        proc.kill()
    except Exception:
        pass
    try:
        proc.wait(timeout=0.5)
    except Exception:
        pass


def terminate_child_processes():
    global child_job
    with child_job_lock:
        job = child_job
        child_job = None
    if job is not None:
        try:
            kernel32.CloseHandle(job)
        except Exception:
            pass
    with child_process_lock:
        processes = list(child_processes)
    for proc in processes:
        _terminate_process(proc)


def run_child(cmd, timeout=None, cancel_event=None, **kwargs):
    if _shutdown_requested():
        return None
    if cancel_event is not None and cancel_event.is_set():
        return None
    proc = subprocess.Popen(cmd, **kwargs)
    with child_process_lock:
        child_processes.add(proc)
    if shutdown_event.is_set():
        _terminate_process(proc)
        with child_process_lock:
            child_processes.discard(proc)
        return None
    _assign_child_to_job(proc)
    started = time.monotonic()
    try:
        while True:
            if shutdown_event.is_set() or (cancel_event is not None and cancel_event.is_set()):
                _terminate_process(proc)
                return None
            remaining = None
            if timeout is not None:
                remaining = float(timeout) - (time.monotonic() - started)
                if remaining <= 0.0:
                    _terminate_process(proc)
                    return None
            slice_timeout = 0.10 if remaining is None else max(0.01, min(0.10, remaining))
            try:
                stdout, stderr = proc.communicate(timeout=slice_timeout)
                return subprocess.CompletedProcess(cmd, proc.returncode, stdout, stderr)
            except subprocess.TimeoutExpired:
                continue
    finally:
        with child_process_lock:
            child_processes.discard(proc)


def _normalized_final_path_text(path):
    text = str(path)
    if text.startswith("\\\\?\\UNC\\"):
        return "\\\\" + text[8:]
    if text.startswith("\\\\?\\"):
        return text[4:]
    return text


def _win_final_path(path):
    path = Path(path)
    handle = kernel32.CreateFileW(
        str(path), FILE_READ_ATTRIBUTES,
        FILE_SHARE_READ | FILE_SHARE_WRITE | FILE_SHARE_DELETE,
        None, OPEN_EXISTING, FILE_FLAG_BACKUP_SEMANTICS, None,
    )
    invalid = ctypes.c_void_p(-1).value
    if handle in (None, 0, invalid):
        raise ctypes.WinError()
    try:
        size = kernel32.GetFinalPathNameByHandleW(handle, None, 0, 0)
        if not size:
            raise ctypes.WinError()
        buffer = ctypes.create_unicode_buffer(size + 2)
        written = kernel32.GetFinalPathNameByHandleW(handle, buffer, len(buffer), 0)
        if not written or written >= len(buffer):
            raise ctypes.WinError()
        return Path(_normalized_final_path_text(buffer.value))
    finally:
        kernel32.CloseHandle(handle)


def _drive_root(path):
    text = str(path)
    if text.startswith("\\"):
        return None
    drive = Path(text).drive.upper().rstrip("\\/")
    if not re.fullmatch(r"[A-Z]:", drive):
        return None
    return drive + "\\"


def _drive_is_subst(drive_root):
    drive = str(drive_root).upper().rstrip("\\/")
    if not re.fullmatch(r"[A-Z]:", drive):
        return True
    buffer = ctypes.create_unicode_buffer(32768)
    written = int(kernel32.QueryDosDeviceW(drive, buffer, len(buffer)))
    if not written:
        raise ctypes.WinError()
    target = buffer.value.strip()
    return bool(re.match(r"^\\\?\?\\[A-Za-z]:\\", target))


def _volume_guid_for_path(path):
    path_buffer = ctypes.create_unicode_buffer(32768)
    if not kernel32.GetVolumePathNameW(str(path), path_buffer, len(path_buffer)):
        raise ctypes.WinError()
    mount = path_buffer.value
    if not mount:
        raise RuntimeError("无法确定所选路径所在 volume。")
    volume_buffer = ctypes.create_unicode_buffer(32768)
    if not kernel32.GetVolumeNameForVolumeMountPointW(mount, volume_buffer, len(volume_buffer)):
        raise ctypes.WinError()
    return volume_buffer.value.rstrip("\\/").upper()


def _assert_selected_path_chain_no_reparse(path):
    candidate = Path(os.path.abspath(str(path)))
    lexical_root = _drive_root(candidate)
    if lexical_root is None:
        raise StorageSafetyError("请选择本地磁盘上的文件夹。")
    drive_path = Path(lexical_root)
    try:
        relative = candidate.relative_to(drive_path)
    except ValueError as exc:
        raise StorageSafetyError("所选路径不是有效的本地磁盘路径。") from exc
    current = drive_path
    for part in relative.parts:
        current = current / part
        attrs = int(kernel32.GetFileAttributesW(str(current)))
        if attrs == INVALID_FILE_ATTRIBUTES:
            raise RuntimeError(f"所选路径不存在或不可访问：{current}")
        if attrs & FILE_ATTRIBUTE_REPARSE_POINT:
            raise StorageSafetyError(f"所选路径或其父级包含 junction/symlink/reparse point：{current}")
    return candidate


def _validate_selected_storage_root(path):
    candidate = _assert_selected_path_chain_no_reparse(path)
    if str(candidate).startswith("\\"):
        raise StorageSafetyError("不允许选择 UNC 或网络路径。")
    lexical_root = _drive_root(candidate)
    if lexical_root is None:
        raise StorageSafetyError("请选择本地磁盘上的文件夹。")
    if int(kernel32.GetDriveTypeW(lexical_root)) != DRIVE_FIXED:
        raise StorageSafetyError("只允许选择本地固定磁盘上的文件夹。")
    if _drive_is_subst(lexical_root):
        raise StorageSafetyError("不允许选择 SUBST 虚拟盘。")

    final_path = _win_final_path(candidate)
    if str(final_path).startswith("\\"):
        raise StorageSafetyError("所选文件夹最终解析到 UNC 或网络路径。")
    final_root = _drive_root(final_path)
    if final_root is None or int(kernel32.GetDriveTypeW(final_root)) != DRIVE_FIXED:
        raise StorageSafetyError("所选文件夹最终位置不是本地固定磁盘。")
    system_volume = _volume_guid_for_path(SYSTEM_DRIVE + "\\")
    selected_volume = _volume_guid_for_path(final_path)
    if selected_volume == system_volume:
        raise StorageSafetyError("所选文件夹最终解析到系统 volume，请选择真正的非系统盘文件夹。")
    return final_path


def _durable_replace(temp_path, destination, validator=None):
    temp_path = Path(temp_path)
    destination = Path(destination)
    _assert_storage_path(temp_path, allow_missing=False)
    _assert_storage_path(destination.parent, allow_missing=False)
    with open(temp_path, "rb+") as handle:
        handle.flush()
        os.fsync(handle.fileno())
    if validator is not None and not bool(validator(temp_path)):
        raise RuntimeError(f"持久化文件重新加载验证失败：{temp_path.name}")
    os.replace(temp_path, destination)


def _normalize_pci_bus_id(value):
    if isinstance(value, (bytes, bytearray)):
        value = bytes(value).decode("ascii", "ignore")
    text = str(value or "").strip().upper()
    match = re.fullmatch(r"([0-9A-F]+):([0-9A-F]{2}):([0-9A-F]{2})\.([0-7])", text)
    if not match:
        return ""
    domain, bus, device, function = match.groups()
    return f"{int(domain, 16):X}:{bus}:{device}.{function}"


def _cupy_device_index_for_pci(cupy_module, pci_bus_id, alternate_pci_ids=()):
    requested = []
    for value in (pci_bus_id, *tuple(alternate_pci_ids or ())):
        normalized = _normalize_pci_bus_id(value)
        if normalized and normalized not in requested:
            requested.append(normalized)
    if not requested:
        raise RuntimeError("nvidia-smi 未返回可验证的 PCI Bus ID。")
    visible = {}
    for index in range(int(cupy_module.cuda.runtime.getDeviceCount())):
        actual = _normalize_pci_bus_id(cupy_module.cuda.runtime.deviceGetPCIBusId(index))
        if actual and actual not in visible:
            visible[actual] = index
    for expected in requested:
        if expected in visible:
            return visible[expected]
    raise RuntimeError("nvidia-smi 检测到的 GPU 在当前 CUDA 可见设备中不存在。")


def _path_has_reparse_attribute(path):
    attrs = int(kernel32.GetFileAttributesW(str(path)))
    if attrs == INVALID_FILE_ATTRIBUTES:
        return False
    return bool(attrs & FILE_ATTRIBUTE_REPARSE_POINT)


def _path_within(candidate, root_path):
    try:
        return os.path.commonpath((os.path.normcase(str(candidate)), os.path.normcase(str(root_path)))) == os.path.normcase(str(root_path))
    except (ValueError, TypeError):
        return False


def _assert_storage_path(path, allow_missing=False):
    if chosen_path is None or storage_root_final is None:
        raise StorageSafetyError("存储根目录尚未完成安全初始化。")
    candidate = Path(os.path.abspath(str(path)))
    lexical_root = Path(os.path.abspath(str(chosen_path)))
    if not _path_within(candidate, lexical_root):
        raise StorageSafetyError(f"拒绝访问用户所选文件夹之外的路径：{candidate}")
    try:
        relative = candidate.relative_to(lexical_root)
    except ValueError as exc:
        raise StorageSafetyError(f"拒绝访问用户所选文件夹之外的路径：{candidate}") from exc
    current = lexical_root
    nearest_existing = lexical_root
    for part in relative.parts:
        current = current / part
        attrs = int(kernel32.GetFileAttributesW(str(current)))
        if attrs == INVALID_FILE_ATTRIBUTES:
            if not allow_missing:
                raise FileNotFoundError(str(current))
            break
        if _path_has_reparse_attribute(current):
            raise StorageSafetyError(f"拒绝使用 reparse point/junction 存储路径：{current}")
        nearest_existing = current
    final_existing = _win_final_path(nearest_existing)
    if not _path_within(final_existing, storage_root_final):
        raise StorageSafetyError(f"存储路径最终位置越出用户所选文件夹：{nearest_existing}")
    if candidate.exists():
        final_candidate = _win_final_path(candidate)
        if not _path_within(final_candidate, storage_root_final):
            raise StorageSafetyError(f"存储路径最终位置越出用户所选文件夹：{candidate}")
    return candidate


def _safe_mkdir(path):
    target = Path(path)
    _assert_storage_path(target.parent, allow_missing=False)
    attrs = int(kernel32.GetFileAttributesW(str(target)))
    if attrs != INVALID_FILE_ATTRIBUTES:
        _assert_storage_path(target, allow_missing=False)
        if not target.is_dir():
            raise RuntimeError(f"预期目录但发现其他对象：{target}")
        return target
    target.mkdir(parents=False, exist_ok=False)
    _assert_storage_path(target, allow_missing=False)
    return target


def _assert_storage_subtree_no_reparse(path):
    root_path = _assert_storage_path(path, allow_missing=False)
    if not root_path.is_dir():
        return
    for walk_root, dirs, files in os.walk(root_path, topdown=True, followlinks=False):
        walk_root = Path(walk_root)
        for name in list(dirs) + list(files):
            child = walk_root / name
            if _path_has_reparse_attribute(child):
                raise StorageSafetyError(f"拒绝遍历包含 reparse point/junction 的存储树：{child}")


def _safe_rmtree(path, ignore_errors=False):
    target = Path(path)
    if int(kernel32.GetFileAttributesW(str(target))) == INVALID_FILE_ATTRIBUTES:
        return
    # Storage-boundary/reparse validation is never suppressible.  Only a
    # non-security deletion failure may be ignored by cleanup callers.
    _assert_storage_subtree_no_reparse(target)
    try:
        shutil.rmtree(target)
    except Exception:
        if not ignore_errors:
            raise


def _clamp(value, low, high):
    return max(low, min(high, value))


def _filetime_value(value):
    return (int(value.dwHighDateTime) << 32) | int(value.dwLowDateTime)


def _sample_cpu_utilization():
    global _cpu_times_sample
    idle = FILETIME(); kernel = FILETIME(); user = FILETIME()
    if not kernel32.GetSystemTimes(ctypes.byref(idle), ctypes.byref(kernel), ctypes.byref(user)):
        return 0.0
    sample = (_filetime_value(idle), _filetime_value(kernel), _filetime_value(user))
    with _cpu_sample_lock:
        previous = _cpu_times_sample
        _cpu_times_sample = sample
    if previous is None:
        return 0.0
    idle_delta = max(0, sample[0] - previous[0])
    total_delta = max(1, (sample[1] - previous[1]) + (sample[2] - previous[2]))
    busy = max(0, total_delta - idle_delta)
    return _clamp(busy * 100.0 / total_delta, 0.0, 100.0)


def _detect_hardware_profile(preferred_gpu_pci_bus_id=None):
    preferred_gpu_pci_bus_id = _normalize_pci_bus_id(preferred_gpu_pci_bus_id)
    cpu_count = max(1, int(os.cpu_count() or 1))
    try:
        cpu_count = max(cpu_count, int(kernel32.GetActiveProcessorCount(0xFFFF)))
    except Exception:
        pass
    cpu_util = _sample_cpu_utilization()
    memory = MEMORYSTATUSEX()
    memory.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
    if kernel32.GlobalMemoryStatusEx(ctypes.byref(memory)):
        ram_total = max(1, int(memory.ullTotalPhys))
        ram_free = max(0, int(memory.ullAvailPhys))
    else:
        ram_total = 8 << 30
        ram_free = ram_total // 2
    usage = shutil.disk_usage(chosen_path)
    screen_pixels = max(1, int(user32.GetSystemMetrics(78))) * max(1, int(user32.GetSystemMetrics(79)))

    gpu_total_mib = 0.0
    gpu_free_mib = 0.0
    gpu_util = 0.0
    gpu_name = None
    gpu_index = 0
    gpu_uuid = None
    gpu_pci_bus_id = None
    gpu_candidates = []
    candidates = []
    discovered = shutil.which("nvidia-smi")
    if discovered:
        candidates.append(discovered)
    program_files = os.environ.get("ProgramFiles")
    if program_files:
        candidates.append(str(Path(program_files) / "NVIDIA Corporation" / "NVSMI" / "nvidia-smi.exe"))
    for executable in candidates:
        try:
            if not Path(executable).exists():
                continue
            result = run_child(
                [executable, "--query-gpu=index,pci.bus_id,uuid,name,memory.total,memory.free,utilization.gpu", "--format=csv,noheader,nounits"],
                cwd=str(app_dir), env=os.environ.copy(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                timeout=max(2.0, math.log2(cpu_count + 1.0)),
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
            )
            if result is None or result.returncode != 0:
                continue
            rows = [row.strip() for row in result.stdout.splitlines() if row.strip()]
            parsed = []
            for row in rows:
                parts = [part.strip() for part in row.split(",")]
                if len(parts) < 7:
                    continue
                pci_id = _normalize_pci_bus_id(parts[1])
                if not pci_id:
                    continue
                parsed.append((int(parts[0]), pci_id, parts[2], parts[3], float(parts[4]), float(parts[5]), float(parts[6])))
            if parsed:
                parsed.sort(key=lambda item: item[4], reverse=True)
                gpu_candidates = [
                    {
                        "smi_index": item[0], "pci_bus_id": item[1], "uuid": item[2], "name": item[3],
                        "total_mib": item[4], "free_mib": item[5], "util": item[6],
                    }
                    for item in parsed
                ]
                selected = parsed[0]
                if preferred_gpu_pci_bus_id:
                    selected = next(
                        (item for item in parsed if _normalize_pci_bus_id(item[1]) == preferred_gpu_pci_bus_id),
                        None,
                    )
                    if selected is None:
                        # 还可能存在另一个 nvidia-smi 路径，继续尝试；只有全部候选都
                        # 无法找到当前 CuPy 设备时才让监控失败并保留上一份 profile。
                        continue
                gpu_index, gpu_pci_bus_id, gpu_uuid, gpu_name, gpu_total_mib, gpu_free_mib, gpu_util = selected
                break
        except Exception:
            continue

    if preferred_gpu_pci_bus_id and _normalize_pci_bus_id(gpu_pci_bus_id) != preferred_gpu_pci_bus_id:
        raise RuntimeError(f"当前 CUDA GPU 已从 NVIDIA 监控结果中消失：{preferred_gpu_pci_bus_id}")

    ram_gib = ram_total / float(1 << 30)
    cpu_factor = math.log2(cpu_count + 1.0)
    ram_factor = math.log2(ram_gib + 2.0)
    ram_headroom = _clamp(ram_free / float(max(1, ram_total)), 0.05, 1.0)
    disk_headroom = _clamp(usage.free / float(max(1, usage.total)), 0.01, 1.0)
    cpu_headroom = 1.0 - _clamp(cpu_util / 100.0, 0.0, 0.95)
    gpu_headroom = (gpu_free_mib / gpu_total_mib) if gpu_total_mib > 0 else 0.5
    gpu_headroom = _clamp(gpu_headroom, 0.05, 1.0)
    gpu_idle = 1.0 - _clamp(gpu_util / 100.0, 0.0, 0.95)
    base_capacity = math.sqrt(cpu_factor * ram_factor)
    pressure_factor = _clamp(0.52 + 0.48 * math.sqrt(cpu_headroom * ram_headroom), 0.52, 1.0)
    display_factor = _clamp(0.86 + 0.14 * math.sqrt(gpu_headroom * gpu_idle), 0.86, 1.0)
    capacity = base_capacity * pressure_factor
    cv_fraction = _clamp((0.24 + 0.12 * capacity) * (0.65 + 0.35 * cpu_headroom), 1.0 / cpu_count, 0.92)
    cv_threads = int(round(_clamp(cpu_count * cv_fraction, 1.0, float(cpu_count))))
    coarse_ratio = _clamp(0.20 + 0.085 * capacity * display_factor + 0.12 * ram_headroom, 0.26, 0.80)
    coarse_pixel_budget = max(640 * 360, int(screen_pixels * coarse_ratio))
    tile_pixel_budget = max(900 * 600, int(coarse_pixel_budget * _clamp(0.50 + 0.09 * cpu_factor * pressure_factor, 0.60, 1.20)))
    scan_frames = int(_clamp(round(1.0 + capacity * 0.60 * display_factor), 2, 4))
    scale_spread = _clamp(0.11 + 0.03 * capacity * pressure_factor, 0.13, 0.25)
    scan_scales = (1.0, 1.0 - scale_spread, 1.0 + scale_spread)
    scan_deadline = _clamp(5.0 + math.sqrt(screen_pixels / max(1.0, coarse_pixel_budget)) * (4.0 + 2.5 / max(0.52, pressure_factor)), 7.0, 22.0)
    training_epochs = int(_clamp(round(17 + capacity * 4.5), 20, 44))
    training_batch = int(_clamp(round(28 * max(2.0, cpu_factor) * _clamp((ram_gib * ram_headroom) / 6.0, 0.65, 3.0)), 48, 384))
    save_interval = _clamp(28.0 + (1.0 - disk_headroom) * 38.0 + (1.0 - ram_headroom) * 12.0, 28.0, 78.0)
    recent_window = int(_clamp(round(22 + capacity * (7.0 + 5.0 * ram_headroom)), 28, 112))
    return {
        "cpu_count": cpu_count, "cpu_util": cpu_util, "cpu_headroom": cpu_headroom,
        "ram_total": ram_total, "ram_free": ram_free, "ram_headroom": ram_headroom,
        "disk_total": usage.total, "disk_free": usage.free, "disk_headroom": disk_headroom,
        "gpu_name": gpu_name, "gpu_index": gpu_index, "gpu_uuid": gpu_uuid, "gpu_pci_bus_id": gpu_pci_bus_id,
        "gpu_candidates": gpu_candidates,
        "gpu_total_mib": gpu_total_mib, "gpu_free_mib": gpu_free_mib,
        "gpu_util": gpu_util, "gpu_headroom": gpu_headroom,
        "screen_pixels": screen_pixels, "capacity": capacity, "cv_threads": cv_threads,
        "coarse_pixel_budget": coarse_pixel_budget, "tile_pixel_budget": tile_pixel_budget,
        "scan_frames": scan_frames, "scan_scales": scan_scales, "scan_deadline": scan_deadline,
        "training_epochs": training_epochs, "training_batch": training_batch,
        "save_interval": save_interval, "recent_window": recent_window,
    }


def _format_gain(value):
    try:
        number = float(value)
        if abs(number - round(number)) < 1e-9:
            return f"+{int(round(number))}"
        return f"+{number:.2f}".rstrip("0").rstrip(".")
    except Exception:
        return "+0"


def _refresh_info_vars():
    if hardware_var is not None:
        profile = hardware_profile or {}
        gpu_name = str(profile.get("gpu_name") or "未检测到 NVIDIA GPU")
        gpu_util = float(profile.get("gpu_util", 0.0) or 0.0)
        hook_state = "正常" if controller is not None and controller.input_hooks_ready.is_set() else "准备中"
        monitor_state = "监控暂不可用" if profile.get("monitor_unavailable") else f"利用率 {gpu_util:.0f}%"
        compute_state = str(profile.get("gpu_compute_backend") or ("CUDA AI" if cp is not None else "AI GPU 未就绪"))
        hardware_var.set(f"GPU  {gpu_name}  ·  {compute_state}  ·  {monitor_state}  ·  输入监听 {hook_state}")
    if learning_var is not None:
        state = getattr(controller, "state", None) if controller is not None else None
        if not isinstance(state, dict):
            state = {}
        trials = max(0, int(state.get("trials", 0) or 0))
        successes = max(0, int(state.get("successes", 0) or 0))
        unknowns = max(0, int(state.get("unknowns", 0) or 0))
        best_gain = _format_gain(state.get("best_gain", 0.0))
        learning_var.set(f"学习 {trials} 次  ·  成功 {successes} 次  ·  待确认 {unknowns} 次  ·  最佳提升 {best_gain}")


def _apply_progress(payload):
    if not isinstance(payload, dict):
        return
    if phase_var is not None and "phase" in payload:
        phase_var.set(str(payload.get("phase") or ""))
    if status_var is not None and "text" in payload:
        status_var.set(str(payload.get("text") or ""))
    if detail_var is not None and "detail" in payload:
        detail_var.set(str(payload.get("detail") or ""))
    if progress is None or progress_var is None:
        return
    try:
        progress.stop()
    except Exception:
        pass
    progress.configure(mode="determinate", maximum=100)
    try:
        value = float(payload.get("value", progress_var.get()))
    except (TypeError, ValueError, tk.TclError):
        try:
            value = float(progress_var.get())
        except Exception:
            value = 0.0
    value = max(0.0, min(100.0, value))
    progress_var.set(value)
    if progress_percent_var is not None:
        progress_percent_var.set(f"{int(value + 0.5)}%")


def set_progress(value, text, detail="", phase="正在准备"):
    post_ui("progress", {
        "value": float(value),
        "text": str(text),
        "detail": str(detail),
        "phase": str(phase),
    })


def _hardware_monitor_loop():
    global hardware_profile
    while app_alive.is_set() and not shutdown_event.is_set():
        if shutdown_event.wait(45.0):
            return
        if not app_alive.is_set():
            return
        try:
            previous = hardware_profile or {}
            pinned_pci = _normalize_pci_bus_id(active_gpu_pci_bus_id or previous.get("active_gpu_pci_bus_id"))
            profile = _detect_hardware_profile(pinned_pci)
            if _shutdown_requested():
                return
            if pinned_pci:
                profile["active_gpu_pci_bus_id"] = pinned_pci
            profile["gpu_compute_backend"] = previous.get("gpu_compute_backend")
            hardware_profile = profile
            post_ui("metrics")
        except Exception as exc:
            if _shutdown_requested():
                return
            profile = dict(hardware_profile or {})
            profile["monitor_unavailable"] = True
            hardware_profile = profile
            _log_runtime("warning", f"hardware monitor unavailable: {exc}")
            post_ui("metrics")
            continue


def _init_runtime_logging():
    global runtime_logger
    if app_dir is None:
        return
    logger = logging.getLogger("MakeItBigger")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    for handler in list(logger.handlers):
        try:
            handler.close()
        except Exception:
            pass
        logger.removeHandler(handler)
    try:
        handler = RotatingFileHandler(
            app_dir / "runtime.log", maxBytes=2 * 1024 * 1024, backupCount=1, encoding="utf-8"
        )
        handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
        logger.addHandler(handler)
        runtime_logger = logger
        logger.info("MakeItBigger started; runtime data directory initialized")
    except Exception:
        runtime_logger = None


def _log_runtime(level, message):
    logger = runtime_logger
    if logger is None:
        return
    try:
        getattr(logger, str(level), logger.info)(str(message))
    except Exception:
        pass


def _log_exception(context, exc):
    logger = runtime_logger
    if logger is None:
        return
    try:
        logger.error(
            "%s: %s: %s",
            str(context),
            exc.__class__.__name__,
            exc,
            exc_info=(type(exc), exc, exc.__traceback__),
        )
    except Exception:
        pass


def _quarantine_corrupt_file(path, reason):
    """Keep damaged learning artifacts inside the selected folder for diagnosis/recovery."""
    candidate = Path(path)
    try:
        if not candidate.exists():
            return None
        _assert_storage_path(candidate, allow_missing=False)
        stamp = time.strftime("%Y%m%d-%H%M%S", time.localtime())
        suffix = f"{time.time_ns() % 1_000_000_000:09d}"
        destination = candidate.with_name(f"{candidate.name}.corrupt.{stamp}.{suffix}")
        _assert_storage_path(destination, allow_missing=True)
        os.replace(candidate, destination)
        _log_runtime("warning", f"quarantined corrupt file {candidate.name} -> {destination.name}; reason: {reason}")
        _cleanup_corrupt_quarantine()
        return destination
    except StorageSafetyError:
        raise
    except Exception as exc:
        _log_runtime("error", f"failed to quarantine corrupt file {candidate.name}: {exc}; original reason: {reason}")
        return None


def _corrupt_quarantine_category(path):
    name = Path(path).name.lower()
    if name.startswith("digit_model"):
        return "ocr_model"
    if name.startswith("digit_self_samples"):
        return "ocr_samples"
    if name.startswith("learning"):
        return "learning_state"
    return "other"


def _cleanup_corrupt_quarantine():
    if app_dir is None or int(kernel32.GetFileAttributesW(str(app_dir))) == INVALID_FILE_ATTRIBUTES:
        return
    try:
        _assert_storage_subtree_no_reparse(app_dir)
        groups = {}
        entries = []
        for candidate in app_dir.glob("*.corrupt.*"):
            if not candidate.is_file() or _path_has_reparse_attribute(candidate):
                continue
            _assert_storage_path(candidate, allow_missing=False)
            stat = candidate.stat()
            entry = (float(stat.st_mtime), max(0, int(stat.st_size)), candidate)
            groups.setdefault(_corrupt_quarantine_category(candidate), []).append(entry)
            entries.append(entry)

        keep = set()
        per_category_cap = 4
        for group_entries in groups.values():
            for entry in sorted(group_entries, reverse=True)[:per_category_cap]:
                keep.add(entry[2])
        for _mtime, _size, candidate in sorted(entries):
            if candidate not in keep:
                try:
                    candidate.unlink()
                except Exception:
                    pass

        remaining = []
        total = 0
        for candidate in keep:
            try:
                stat = candidate.stat()
                size = max(0, int(stat.st_size))
                remaining.append((float(stat.st_mtime), size, candidate))
                total += size
            except Exception:
                continue
        total_cap = 64 * 1024 * 1024
        if total > total_cap:
            for _mtime, size, candidate in sorted(remaining):
                try:
                    candidate.unlink()
                    total -= size
                except Exception:
                    continue
                if total <= total_cap:
                    break
    except StorageSafetyError:
        raise
    except Exception as exc:
        _log_runtime("warning", f"corrupt quarantine cleanup skipped: {exc}")


def post_ui(kind, payload=None):
    if shutdown_event.is_set():
        return
    ui_queue.put((str(kind), payload))


def drain_ui_queue():
    if root is None or shutdown_event.is_set():
        return
    try:
        while True:
            try:
                kind, payload = ui_queue.get_nowait()
            except queue.Empty:
                break
            if kind == "status":
                if status_var is not None:
                    status_var.set(str(payload))
            elif kind == "progress":
                _apply_progress(payload)
            elif kind == "metrics":
                _refresh_info_vars()
            elif kind == "dependency_failed":
                dependency_failed(str(payload))
            elif kind == "enable_controls":
                enable_main_controls()
            elif kind == "show_overlays":
                show_number_overlays(payload)
            elif kind == "show_stopping":
                show_main_stopping()
            elif kind == "show_user_control":
                show_main_user_control()
            elif kind == "show_agent_stopped":
                show_main_agent_stopped(str(payload))
            elif kind == "runtime_error":
                _clear_overlays_and_show_error(str(payload))
    finally:
        if root is not None and not shutdown_event.is_set():
            try:
                root.after(40, drain_ui_queue)
            except tk.TclError:
                pass


def build_main_ui(initial_phase="正在准备", initial_status="正在初始化本地 AI…", initial_detail="所有运行数据均保存在所选文件夹"):
    global root, phase_var, status_var, detail_var, progress_var, progress_percent_var, status, detail_label, progress
    global number_button, free_button, hardware_var, learning_var
    if root is None:
        root = tk.Tk()
    root.withdraw()
    for child in list(root.winfo_children()):
        try:
            child.destroy()
        except Exception:
            pass

    root.title("Make It Bigger")
    root.geometry("720x520")
    root.minsize(580, 420)
    root.resizable(True, True)
    root.protocol("WM_DELETE_WINDOW", shutdown)
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

    style = ttk.Style(root)
    if "vista" in style.theme_names():
        try:
            style.theme_use("vista")
        except tk.TclError:
            pass
    style.configure("Title.TLabel", font=("Segoe UI", 22, "bold"))
    style.configure("Subtitle.TLabel", font=("Segoe UI", 10))
    style.configure("Phase.TLabel", font=("Segoe UI", 12, "bold"))
    style.configure("Status.TLabel", font=("Segoe UI", 11))
    style.configure("Detail.TLabel", font=("Segoe UI", 9))
    style.configure("Primary.TButton", font=("Segoe UI", 12, "bold"), padding=(18, 14))
    style.configure("Secondary.TButton", font=("Segoe UI", 11), padding=(16, 10))
    style.configure("Footer.TLabel", font=("Segoe UI", 9))

    phase_var = tk.StringVar(value=initial_phase)
    status_var = tk.StringVar(value=initial_status)
    detail_var = tk.StringVar(value=initial_detail)
    progress_var = tk.DoubleVar(value=0.0)
    progress_percent_var = tk.StringVar(value="0%")
    hardware_var = tk.StringVar(value="硬件监控 GPU  NVIDIA  ·  输入监听 准备中")
    learning_var = tk.StringVar(value="学习 0 次  ·  成功 0 次  ·  待确认 0 次  ·  最佳提升 +0")

    main = ttk.Frame(root, padding=(28, 24, 28, 22))
    main.grid(row=0, column=0, sticky="nsew")
    main.columnconfigure(0, weight=1)
    main.rowconfigure(2, weight=1)

    ttk.Label(main, text="Make It Bigger", style="Title.TLabel").grid(row=0, column=0, sticky="w")
    ttk.Label(main, text="让本地 AI 根据你的选择执行操作", style="Subtitle.TLabel").grid(row=1, column=0, sticky="w", pady=(2, 18))

    card = ttk.LabelFrame(main, text="状态", padding=(18, 14))
    card.grid(row=2, column=0, sticky="nsew")
    card.columnconfigure(0, weight=1)
    card.rowconfigure(2, weight=1)

    ttk.Label(card, textvariable=phase_var, style="Phase.TLabel").grid(row=0, column=0, sticky="w")
    status = ttk.Label(card, textvariable=status_var, style="Status.TLabel", anchor="w", justify="left")
    status.grid(row=1, column=0, sticky="ew", pady=(7, 4))
    detail_label = ttk.Label(card, textvariable=detail_var, style="Detail.TLabel", anchor="nw", justify="left")
    detail_label.grid(row=2, column=0, sticky="nsew", pady=(0, 12))
    progress_row = ttk.Frame(card)
    progress_row.grid(row=3, column=0, sticky="ew")
    progress_row.columnconfigure(0, weight=1)
    progress = ttk.Progressbar(progress_row, variable=progress_var, maximum=100, mode="determinate")
    progress.grid(row=0, column=0, sticky="ew")
    ttk.Label(
        progress_row, textvariable=progress_percent_var, width=5, anchor="e", style="Detail.TLabel"
    ).grid(row=0, column=1, padx=(10, 0))

    actions = ttk.Frame(main)
    actions.grid(row=3, column=0, sticky="ew", pady=(18, 0))
    actions.columnconfigure(0, weight=1)
    number_button = ttk.Button(actions, text="让你选择的数变大", style="Primary.TButton", state="disabled")
    number_button.grid(row=0, column=0, sticky="ew")
    ttk.Label(actions, text="选择数字：识别屏幕上的数字，由你指定 AI 的目标。", style="Detail.TLabel").grid(row=1, column=0, sticky="w", pady=(5, 12))
    free_button = ttk.Button(actions, text="自由", style="Secondary.TButton", state="disabled")
    free_button.grid(row=2, column=0, sticky="ew")
    ttk.Label(actions, text="自由模式：让 AI 自主运行，直到检测到你的鼠标或键盘输入。", style="Detail.TLabel").grid(row=3, column=0, sticky="w", pady=(5, 0))

    footer = ttk.Frame(main)
    footer.grid(row=4, column=0, sticky="ew", pady=(18, 0))
    footer.columnconfigure(0, weight=1)
    ttk.Separator(footer).grid(row=0, column=0, sticky="ew", pady=(0, 9))
    ttk.Label(footer, textvariable=hardware_var, style="Footer.TLabel").grid(row=1, column=0, sticky="w")
    ttk.Label(footer, textvariable=learning_var, style="Footer.TLabel").grid(row=2, column=0, sticky="w", pady=(3, 0))

    def on_window_resize(event):
        if event.widget is root:
            wrap = max(320, int(event.width) - 120)
            try:
                status.configure(wraplength=wrap)
                detail_label.configure(wraplength=wrap)
            except tk.TclError:
                pass

    root.bind("<Configure>", on_window_resize)
    _refresh_info_vars()
    root.deiconify()
    root.lift()
    try:
        root.after(40, drain_ui_queue)
    except tk.TclError:
        pass


def _cleanup_selected_storage():
    """Recover interrupted dependency swaps and bound stale temp storage."""
    stage_dir = app_dir / "deps.new"
    old_dir = app_dir / "deps.old"
    wheel_dir = app_dir / "wheels.new"
    gpu_stage_dir = app_dir / "gpu-deps.new"
    gpu_old_dir = app_dir / "gpu-deps.old"
    gpu_wheel_dir = app_dir / "gpu-wheels.new"
    pip_bootstrap_dir = app_dir / "pip-bootstrap"

    # Recover the only dangerous swap window first: deps was renamed to
    # deps.old but the verified deps.new tree was not promoted yet.
    if not deps_dir.exists() and old_dir.exists():
        _assert_storage_path(old_dir)
        try:
            os.replace(old_dir, deps_dir)
        except Exception as exc:
            _log_runtime("warning", f"visual dependency rollback restore failed: {exc}")
    elif deps_dir.exists() and old_dir.exists():
        _safe_rmtree(old_dir, ignore_errors=True)

    if not gpu_deps_dir.exists() and gpu_old_dir.exists():
        _assert_storage_path(gpu_old_dir)
        try:
            os.replace(gpu_old_dir, gpu_deps_dir)
        except Exception as exc:
            _log_runtime("warning", f"GPU dependency rollback restore failed: {exc}")
    elif gpu_deps_dir.exists() and gpu_old_dir.exists():
        _safe_rmtree(gpu_old_dir, ignore_errors=True)
    for residue in (stage_dir, wheel_dir, gpu_stage_dir, gpu_wheel_dir, pip_bootstrap_dir):
        _safe_rmtree(residue, ignore_errors=True)

    _safe_mkdir(temp_dir)
    _assert_storage_subtree_no_reparse(temp_dir)
    now = time.time()
    stale_age = 24.0 * 3600.0
    entries = []
    total = 0
    try:
        for path in temp_dir.rglob("*"):
            try:
                if path.is_symlink():
                    path.unlink(missing_ok=True)
                    continue
                if not path.is_file():
                    continue
                stat = path.stat()
                if now - stat.st_mtime >= stale_age:
                    try:
                        path.unlink()
                        continue
                    except Exception:
                        pass
                total += max(0, int(stat.st_size))
                entries.append((float(stat.st_mtime), max(0, int(stat.st_size)), path))
            except Exception:
                continue
        # A hard cap prevents crash leftovers from growing forever.  Delete
        # oldest files first; current-process files do not exist at startup.
        cap = 256 * 1024 * 1024
        if total > cap:
            for _mtime, size, path in sorted(entries):
                try:
                    path.unlink()
                    total -= size
                except Exception:
                    continue
                if total <= cap:
                    break
        for directory in sorted((q for q in temp_dir.rglob("*") if q.is_dir()), key=lambda q: len(q.parts), reverse=True):
            try:
                directory.rmdir()
            except Exception:
                pass
    except StorageSafetyError:
        raise
    except Exception as exc:
        _log_runtime("warning", f"temp cleanup skipped: {exc}")


def initialize_ui_and_storage():
    global root, chosen_path, app_dir, deps_dir, gpu_deps_dir, temp_dir, hardware_profile, storage_root_final
    root = tk.Tk()
    root.withdraw()
    root.update_idletasks()

    console = kernel32.GetConsoleWindow()
    if console:
        user32.ShowWindow(console, SW_HIDE)

    while True:
        chosen = filedialog.askdirectory(title="选择非系统盘文件夹")
        if not chosen:
            root.destroy()
            root = None
            return False
        chosen_path = Path(os.path.abspath(chosen))
        try:
            storage_root_final = _validate_selected_storage_root(chosen_path)
            if not chosen_path.is_dir():
                raise RuntimeError("用户选择的路径不是可用文件夹。")
            break
        except Exception as exc:
            messagebox.showerror("请选择真正的非系统盘固定磁盘", str(exc))

    app_dir = chosen_path / ".makeitbigger"
    deps_dir = app_dir / "deps"
    gpu_deps_dir = app_dir / "gpu-deps"
    temp_dir = app_dir / "temp"
    _safe_mkdir(app_dir)
    _safe_mkdir(temp_dir)
    for protected_dir in (app_dir, temp_dir):
        _assert_storage_path(protected_dir)
    for protected_dir in (deps_dir, gpu_deps_dir):
        if int(kernel32.GetFileAttributesW(str(protected_dir))) != INVALID_FILE_ATTRIBUTES:
            _assert_storage_path(protected_dir)
    _assert_storage_subtree_no_reparse(app_dir)
    _init_runtime_logging()
    _cleanup_selected_storage()
    _cleanup_corrupt_quarantine()

    for key in ("TMP", "TEMP", "TMPDIR", "PIP_CACHE_DIR", "XDG_CACHE_HOME", "CUDA_CACHE_PATH", "CUPY_CACHE_DIR", "OPENCV_OPENCL_CACHE_DIR"):
        os.environ[key] = str(temp_dir)
    os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
    os.environ["PYTHONNOUSERSITE"] = "1"
    os.environ["PIP_DISABLE_PIP_VERSION_CHECK"] = "1"
    os.environ["PIP_NO_INPUT"] = "1"
    os.environ["PIP_PROGRESS_BAR"] = "off"
    os.environ["PIP_CONFIG_FILE"] = os.devnull
    os.environ["OPENCV_LOG_LEVEL"] = "SILENT"

    build_main_ui(
        initial_phase="正在准备运行环境",
        initial_status="开始初始化本地 AI",
        initial_detail="所有运行数据、依赖与学习结果仅保存在你选择的文件夹内。",
    )
    _apply_progress({"value": 0, "phase": "正在准备运行环境", "text": "开始初始化本地 AI", "detail": "正在初始化所选文件夹。"})
    _apply_progress({"value": 5, "phase": "正在准备运行环境", "text": "已初始化存储目录", "detail": "正在检查本机硬件配置…"})
    try:
        root.update()
    except tk.TclError:
        return False
    if _shutdown_requested():
        return False

    _apply_progress({"value": 10, "phase": "正在准备运行环境", "text": "正在检查硬件", "detail": "正在读取 CPU、内存、磁盘与 NVIDIA GPU 信息。"})
    try:
        root.update_idletasks()
    except tk.TclError:
        return False
    hardware_profile = _detect_hardware_profile()
    if float(hardware_profile.get("gpu_total_mib", 0.0) or 0.0) <= 0.0:
        raise RuntimeError("未检测到可用的 NVIDIA GPU。")
    if _shutdown_requested():
        return False
    thread_hint = str(max(1, int(hardware_profile["cv_threads"])))
    for key in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
        os.environ[key] = thread_hint
    if deps_dir.exists() and str(deps_dir) not in sys.path:
        sys.path.insert(0, str(deps_dir))
    _refresh_info_vars()
    _apply_progress({"value": 15, "phase": "正在准备运行环境", "text": "硬件检查完成", "detail": "正在检查本地运行依赖。"})
    _apply_progress({"value": 20, "phase": "正在准备运行环境", "text": "正在检查本地依赖", "detail": "检查本地视觉依赖是否完整可用。"})
    return True


def show_startup_error(exc):
    detail = str(exc).strip() or "未知错误"
    text = f"启动出错：{exc.__class__.__name__}: {detail}。AI已停止。"
    previous_progress = 0.0
    try:
        if progress_var is not None:
            previous_progress = float(progress_var.get())
    except Exception:
        previous_progress = 0.0
    if shutdown_event.is_set():
        return False
    try:
        build_main_ui(initial_phase="已停止", initial_status=text, initial_detail="AI 没有继续控制鼠标或键盘。")
        _apply_progress({"value": previous_progress, "phase": "已停止", "text": text, "detail": "AI 没有继续控制鼠标或键盘。关闭窗口即可退出。"})
        number_button.config(state="disabled")
        free_button.config(state="disabled")
        root.deiconify()
        root.lift()
        return True
    except Exception:
        try:
            user32.MessageBoxW(None, text, "Make It Bigger", 0x10)
        except Exception:
            pass
        return False

np = None
cp = None
cv2 = None
Image = None
ImageGrab = None
ImageDraw = None
ImageFont = None

def bootstrap_dependencies():
    try:
        if _shutdown_requested():
            return
        _bootstrap_dependencies_impl()
    except Exception as exc:
        if _shutdown_requested():
            return
        _log_exception("bootstrap dependencies failed", exc)
        detail = str(exc).strip() or "未知错误"
        post_ui("dependency_failed", f"本地运行环境准备失败：{exc.__class__.__name__}: {detail}")


def _bootstrap_dependencies_impl():
    global np, cp, cv2, Image, ImageGrab, ImageDraw, ImageFont, deps_dir, gpu_deps_dir, recognizer, controller
    global hardware_thread, hook_thread, release_thread, active_gpu_pci_bus_id
    ready_marker = ".ready-v5"
    stage_dir = app_dir / "deps.new"
    old_dir = app_dir / "deps.old"
    wheel_dir = app_dir / "wheels.new"

    DEPENDENCY_SETS = {(3, 10): {'visual': ({'name': 'visual-primary',
                           'packages': ('numpy==2.2.6', 'Pillow==11.3.0', 'opencv-python-headless==4.12.0.88'),
                           'wheels': {'numpy-2.2.6-cp310-cp310-win_amd64.whl': 'f0fd6321b839904e15c46e0d257fdd101dd7f530fe03fd6359c1ea63738703f3',
                                      'pillow-11.3.0-cp310-cp310-win_amd64.whl': '19d2ff547c75b8e3ff46f4d9ef969a06c30ab2d4263a9e287733aa8b2429ce8f',
                                      'opencv_python_headless-4.12.0.88-cp37-abi3-win_amd64.whl': '86b413bdd6c6bf497832e346cd5371995de148e579b9774f8eba686dee3f5528'}},
                          {'name': 'visual-fallback',
                           'packages': ('numpy==2.2.5', 'Pillow==12.0.0', 'opencv-python-headless==4.11.0.86'),
                           'wheels': {'numpy-2.2.5-cp310-cp310-win_amd64.whl': 'e4f0b035d9d0ed519c813ee23e0a733db81ec37d2e9503afbb6e54ccfdee0fa7',
                                      'pillow-12.0.0-cp310-cp310-win_amd64.whl': '455247ac8a4cfb7b9bc45b7e432d10421aea9fc2e74d285ba4072688a74c2e9d',
                                      'opencv_python_headless-4.11.0.86-cp37-abi3-win_amd64.whl': '6c304df9caa7a6a5710b91709dd4786bf20a74d57672b3c31f7033cc638174ca'}}),
               'gpu': ({'name': 'gpu-primary',
                        'packages': ('cupy-cuda12x==14.2.0', 'fastrlock==0.8.3'),
                        'wheels': {'cupy_cuda12x-14.2.0-cp310-cp310-win_amd64.whl': '2d0c77202f5ac5920a420888b28200a11d03d24352b7585d3cb1a84f67fbc96c',
                                   'fastrlock-0.8.3-cp310-cp310-win_amd64.whl': '001fd86bcac78c79658bac496e8a17472d64d558cd2227fdc768aa77f877fe40'}},
                       {'name': 'gpu-fallback',
                        'packages': ('cupy-cuda12x==14.1.0', 'fastrlock==0.8.3'),
                        'wheels': {'cupy_cuda12x-14.1.0-cp310-cp310-win_amd64.whl': '323111bb35aa0b75552b69755dea48184136660e0bcd1b4a0e21a0d93c14bf6a',
                                   'fastrlock-0.8.3-cp310-cp310-win_amd64.whl': '001fd86bcac78c79658bac496e8a17472d64d558cd2227fdc768aa77f877fe40'}})},
     (3, 11): {'visual': ({'name': 'visual-primary',
                           'packages': ('numpy==2.2.6', 'Pillow==11.3.0', 'opencv-python-headless==4.12.0.88'),
                           'wheels': {'numpy-2.2.6-cp311-cp311-win_amd64.whl': 'e8213002e427c69c45a52bbd94163084025f533a55a59d6f9c5b820774ef3303',
                                      'pillow-11.3.0-cp311-cp311-win_amd64.whl': '1a992e86b0dd7aeb1f053cd506508c0999d710a8f07b4c791c63843fc6a807ac',
                                      'opencv_python_headless-4.12.0.88-cp37-abi3-win_amd64.whl': '86b413bdd6c6bf497832e346cd5371995de148e579b9774f8eba686dee3f5528'}},
                          {'name': 'visual-fallback',
                           'packages': ('numpy==2.2.5', 'Pillow==12.0.0', 'opencv-python-headless==4.11.0.86'),
                           'wheels': {'numpy-2.2.5-cp311-cp311-win_amd64.whl': 'b13f04968b46ad705f7c8a80122a42ae8f620536ea38cf4bdd374302926424dd',
                                      'pillow-12.0.0-cp311-cp311-win_amd64.whl': 'b583dc9070312190192631373c6c8ed277254aa6e6084b74bdd0a6d3b221608e',
                                      'opencv_python_headless-4.11.0.86-cp37-abi3-win_amd64.whl': '6c304df9caa7a6a5710b91709dd4786bf20a74d57672b3c31f7033cc638174ca'}}),
               'gpu': ({'name': 'gpu-primary',
                        'packages': ('cupy-cuda12x==14.2.0', 'fastrlock==0.8.3'),
                        'wheels': {'cupy_cuda12x-14.2.0-cp311-cp311-win_amd64.whl': 'eceffbf02a5833c8ba1c94615da07c374284db76a60f8c8b217b0d9d2667162a',
                                   'fastrlock-0.8.3-cp311-cp311-win_amd64.whl': '5e5f1665d8e70f4c5b4a67f2db202f354abc80a321ce5a26ac1493f055e3ae2c'}},
                       {'name': 'gpu-fallback',
                        'packages': ('cupy-cuda12x==14.1.0', 'fastrlock==0.8.3'),
                        'wheels': {'cupy_cuda12x-14.1.0-cp311-cp311-win_amd64.whl': 'cf2c10e00ea116ebca9eb9943482a5e6e4879f44d9850cec3e06786f3f63826c',
                                   'fastrlock-0.8.3-cp311-cp311-win_amd64.whl': '5e5f1665d8e70f4c5b4a67f2db202f354abc80a321ce5a26ac1493f055e3ae2c'}})},
     (3, 12): {'visual': ({'name': 'visual-primary',
                           'packages': ('numpy==2.2.6', 'Pillow==11.3.0', 'opencv-python-headless==4.12.0.88'),
                           'wheels': {'numpy-2.2.6-cp312-cp312-win_amd64.whl': 'c1f9540be57940698ed329904db803cf7a402f3fc200bfe599334c9bd84a40b2',
                                      'pillow-11.3.0-cp312-cp312-win_amd64.whl': 'a6444696fce635783440b7f7a9fc24b3ad10a9ea3f0ab66c5905be1c19ccf17d',
                                      'opencv_python_headless-4.12.0.88-cp37-abi3-win_amd64.whl': '86b413bdd6c6bf497832e346cd5371995de148e579b9774f8eba686dee3f5528'}},
                          {'name': 'visual-fallback',
                           'packages': ('numpy==2.2.5', 'Pillow==12.0.0', 'opencv-python-headless==4.11.0.86'),
                           'wheels': {'numpy-2.2.5-cp312-cp312-win_amd64.whl': 'ced69262a8278547e63409b2653b372bf4baff0870c57efa76c5703fd6543282',
                                      'pillow-12.0.0-cp312-cp312-win_amd64.whl': '9fe611163f6303d1619bbcb653540a4d60f9e55e622d60a3108be0d5b441017a',
                                      'opencv_python_headless-4.11.0.86-cp37-abi3-win_amd64.whl': '6c304df9caa7a6a5710b91709dd4786bf20a74d57672b3c31f7033cc638174ca'}}),
               'gpu': ({'name': 'gpu-primary',
                        'packages': ('cupy-cuda12x==14.2.0', 'fastrlock==0.8.3'),
                        'wheels': {'cupy_cuda12x-14.2.0-cp312-cp312-win_amd64.whl': 'c9571d3b5f2e65758137e210f7fb3c3b34767f0af6b6ca04035a244b6141ee12',
                                   'fastrlock-0.8.3-cp312-cp312-win_amd64.whl': 'da06d43e1625e2ffddd303edcd6d2cd068e1c486f5fd0102b3f079c44eb13e2c'}},
                       {'name': 'gpu-fallback',
                        'packages': ('cupy-cuda12x==14.1.0', 'fastrlock==0.8.3'),
                        'wheels': {'cupy_cuda12x-14.1.0-cp312-cp312-win_amd64.whl': '31c388f6b20acc265658363466cf58c5419e0ca47ff54d44d78e6ef6f997d3ac',
                                   'fastrlock-0.8.3-cp312-cp312-win_amd64.whl': 'da06d43e1625e2ffddd303edcd6d2cd068e1c486f5fd0102b3f079c44eb13e2c'}})},
     (3, 13): {'visual': ({'name': 'visual-primary',
                           'packages': ('numpy==2.2.6', 'Pillow==11.3.0', 'opencv-python-headless==4.12.0.88'),
                           'wheels': {'numpy-2.2.6-cp313-cp313-win_amd64.whl': 'b0544343a702fa80c95ad5d3d608ea3599dd54d4632df855e4c8d24eb6ecfa1c',
                                      'pillow-11.3.0-cp313-cp313-win_amd64.whl': '0bce5c4fd0921f99d2e858dc4d4d64193407e1b99478bc5cacecba2311abde51',
                                      'opencv_python_headless-4.12.0.88-cp37-abi3-win_amd64.whl': '86b413bdd6c6bf497832e346cd5371995de148e579b9774f8eba686dee3f5528'}},
                          {'name': 'visual-fallback',
                           'packages': ('numpy==2.2.5', 'Pillow==12.0.0', 'opencv-python-headless==4.11.0.86'),
                           'wheels': {'numpy-2.2.5-cp313-cp313-win_amd64.whl': 'd8882a829fd779f0f43998e931c466802a77ca1ee0fe25a3abe50278616b1471',
                                      'pillow-12.0.0-cp313-cp313-win_amd64.whl': '4cf7fed4b4580601c4345ceb5d4cbf5a980d030fd5ad07c4d2ec589f95f09905',
                                      'opencv_python_headless-4.11.0.86-cp37-abi3-win_amd64.whl': '6c304df9caa7a6a5710b91709dd4786bf20a74d57672b3c31f7033cc638174ca'}}),
               'gpu': ({'name': 'gpu-primary',
                        'packages': ('cupy-cuda12x==14.2.0', 'fastrlock==0.8.3'),
                        'wheels': {'cupy_cuda12x-14.2.0-cp313-cp313-win_amd64.whl': 'dcea9f2b1887ac631a9275a61577e09d1eea26bf5f95491501c3b7528cebc592',
                                   'fastrlock-0.8.3-cp313-cp313-win_amd64.whl': '8d1d6a28291b4ace2a66bd7b49a9ed9c762467617febdd9ab356b867ed901af8'}},
                       {'name': 'gpu-fallback',
                        'packages': ('cupy-cuda12x==14.1.0', 'fastrlock==0.8.3'),
                        'wheels': {'cupy_cuda12x-14.1.0-cp313-cp313-win_amd64.whl': '3dba5342eff14b534104c5caeec0ed80699244cbc03d7cc93c4573f6c94cdae9',
                                   'fastrlock-0.8.3-cp313-cp313-win_amd64.whl': '8d1d6a28291b4ace2a66bd7b49a9ed9c762467617febdd9ab356b867ed901af8'}})}}
    python_dependency_set = DEPENDENCY_SETS.get(tuple(sys.version_info[:2]))
    if sys.implementation.name != "cpython" or python_dependency_set is None or ctypes.sizeof(ctypes.c_void_p) != 8:
        supported_text = ", ".join(f"{major}.{minor}" for major, minor in sorted(DEPENDENCY_SETS))
        raise RuntimeError(f"仅支持 Windows 11 x64 上的 64 位 CPython {supported_text}。")
    gil_probe = getattr(sys, "_is_gil_enabled", None)
    if callable(gil_probe) and not bool(gil_probe()):
        raise RuntimeError("当前依赖仅支持标准 GIL 构建的 64 位 CPython。")
    dependency_manifests = tuple(python_dependency_set["visual"])
    gpu_manifests = tuple(python_dependency_set["gpu"])

    last_dependency_progress = 20.0
    pip_env = os.environ.copy()
    for key in list(pip_env):
        if key.upper().startswith("PIP_"):
            pip_env.pop(key, None)
    pip_env["PIP_CONFIG_FILE"] = os.devnull
    pip_python = sys.executable
    pip_bootstrap_dir = app_dir / "pip-bootstrap"

    def ensure_local_pip():
        nonlocal pip_python
        probe = run_child(
            [sys.executable, "-m", "pip", "--version"], cwd=str(app_dir), env=pip_env,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=20.0,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
        if probe is not None and probe.returncode == 0:
            pip_python = sys.executable
            return
        _safe_rmtree(pip_bootstrap_dir, ignore_errors=True)
        dependency_progress(22, "正在自动恢复 pip", "当前 Python 没有可用 pip；正在所选文件夹内创建临时 pip 环境。")
        result = run_child(
            [sys.executable, "-m", "venv", "--clear", str(pip_bootstrap_dir)],
            cwd=str(app_dir), env=pip_env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            timeout=120.0, creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
        candidate = pip_bootstrap_dir / "Scripts" / "python.exe"
        if result is not None and result.returncode == 0 and candidate.exists():
            probe = run_child(
                [str(candidate), "-m", "pip", "--version"], cwd=str(app_dir), env=pip_env,
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=30.0,
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
            )
            if probe is not None and probe.returncode == 0:
                pip_python = str(candidate)
                return

        # Some otherwise valid Python distributions omit both pip and a usable
        # venv command but still ship ensurepip's bundled pip wheel.  Copy that
        # trusted wheel into the selected folder and run it via PYTHONPATH, so
        # recovery remains automatic without installing anything system-wide.
        try:
            import ensurepip
            bundled = Path(ensurepip.__file__).resolve().parent / "_bundled"
            wheels = sorted(bundled.glob("pip-*.whl"))
            if not wheels:
                raise FileNotFoundError("ensurepip bundled pip wheel not found")
            _safe_mkdir(pip_bootstrap_dir)
            local_wheel = pip_bootstrap_dir / "pip-bootstrap.whl"
            shutil.copy2(wheels[-1], local_wheel)
            inherited = str(pip_env.get("PYTHONPATH") or "").strip()
            pip_env["PYTHONPATH"] = str(local_wheel) + (os.pathsep + inherited if inherited else "")
            probe = run_child(
                [sys.executable, "-m", "pip", "--version"], cwd=str(app_dir), env=pip_env,
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=30.0,
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
            )
            if probe is None or probe.returncode != 0:
                raise RuntimeError("bundled pip wheel could not be executed")
            pip_python = sys.executable
            return
        except Exception as exc:
            raise RuntimeError("Python 未提供可在所选文件夹内自动恢复的 pip 组件。") from exc

    def dependency_progress(value, text, detail):
        nonlocal last_dependency_progress
        last_dependency_progress = max(last_dependency_progress, float(value))
        set_progress(last_dependency_progress, text, detail, phase="正在准备运行环境")

    integrity_manifest_name = ".integrity-v2.json"

    def _sha256_file(path):
        digest_state = hashlib.sha256()
        with Path(path).open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest_state.update(chunk)
        return digest_state.hexdigest().lower()

    def _integrity_candidates(directory):
        directory = Path(directory)
        _assert_storage_subtree_no_reparse(directory)
        found = {}
        for walk_root, dirs, files in os.walk(directory, topdown=True, followlinks=False):
            walk_root = Path(walk_root)
            for name in files:
                candidate = walk_root / name
                if candidate.name == integrity_manifest_name:
                    continue
                if _path_has_reparse_attribute(candidate) or not candidate.is_file():
                    raise StorageSafetyError(f"依赖目录包含不可验证的 reparse point 或非普通文件：{candidate}")
                relative = candidate.relative_to(directory).as_posix()
                found[relative] = candidate
        return found

    def _write_dependency_integrity_manifest(directory):
        directory = Path(directory)
        files = _integrity_candidates(directory)
        if not files:
            raise RuntimeError("已安装依赖目录为空，无法建立完整性清单。")
        payload_files = {}
        for name, path in sorted(files.items()):
            stat = path.stat()
            payload_files[name] = {"size": int(stat.st_size), "sha256": _sha256_file(path)}
        payload = {"version": 2, "files": payload_files}
        target = directory / integrity_manifest_name
        with target.open("w", encoding="utf-8", newline="") as handle:
            json.dump(payload, handle, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
            handle.flush()
            os.fsync(handle.fileno())

    def _dependency_tree_integrity_valid(directory):
        directory = Path(directory)
        manifest_path = directory / integrity_manifest_name
        try:
            _assert_storage_subtree_no_reparse(directory)
            data = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest_files = data.get("files")
            if int(data.get("version", -1)) != 2 or not isinstance(manifest_files, dict) or not manifest_files:
                return False
            current_files = _integrity_candidates(directory)
            if set(current_files) != set(manifest_files):
                return False
            for relative, metadata in manifest_files.items():
                if (not isinstance(relative, str) or not relative or "\x00" in relative or "\\" in relative
                        or relative.startswith("/") or any(part in ("", ".", "..") for part in relative.split("/"))):
                    return False
                if not isinstance(metadata, dict):
                    return False
                expected_size = int(metadata.get("size", -1))
                expected_hash = str(metadata.get("sha256", "")).lower()
                if expected_size < 0 or not re.fullmatch(r"[0-9a-f]{64}", expected_hash):
                    return False
                candidate = current_files.get(relative)
                if candidate is None:
                    return False
                stat = candidate.stat()
                if int(stat.st_size) != expected_size or _sha256_file(candidate) != expected_hash:
                    return False
            return True
        except StorageSafetyError:
            raise
        except Exception as exc:
            _log_exception(f"dependency integrity validation failed for {directory.name}", exc)
            return False

    def _prepare_hashed_dependency_set(manifest, stage, wheels, smoke_test_fn, kind):
        packages = tuple(manifest["packages"])
        expected_wheels = dict(manifest["wheels"])
        if not packages or not expected_wheels:
            raise RuntimeError(f"已审核依赖方案为空：{manifest.get('name', kind)}")
        _safe_rmtree(stage, ignore_errors=True)
        _safe_rmtree(wheels, ignore_errors=True)
        _safe_mkdir(stage)
        _safe_mkdir(wheels)

        for index, package in enumerate(packages):
            if _shutdown_requested():
                return False
            if kind == "visual":
                before = 25.0 + 15.0 * index / len(packages)
                after = 25.0 + 15.0 * (index + 1) / len(packages)
                dependency_progress(before, "正在下载本地运行依赖", f"正在准备 {package}")
            else:
                after = 64.0
                dependency_progress(64.0, "正在准备 NVIDIA GPU 计算后端", f"正在准备 {package}")
            result = run_child(
                [
                    pip_python, "-m", "pip", "--isolated", "download", "--no-input", "--no-cache-dir",
                    "--disable-pip-version-check", "--index-url", "https://pypi.org/simple", "--timeout", "20",
                    "--retries", "2", "--no-deps", "--only-binary=:all:", "--dest", str(wheels), package,
                ],
                timeout=480.0, cwd=str(app_dir), env=pip_env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
            )
            if result is None:
                if _shutdown_requested():
                    return False
                raise RuntimeError(f"{package} 下载超时或被终止。")
            if result.returncode != 0:
                raise RuntimeError(f"{package} 下载失败，pip 返回代码 {result.returncode}。")
            if kind == "visual":
                dependency_progress(after, "正在下载本地运行依赖", f"{index + 1}/{len(packages)} 个依赖已下载")

        if kind == "visual":
            dependency_progress(43, "正在校验下载文件", "正在校验本地依赖安装包的文件名与完整性。")
        downloaded = {path.name: path for path in Path(wheels).glob("*.whl")}
        if set(downloaded) != set(expected_wheels):
            actual = ", ".join(sorted(downloaded)) or "无"
            raise RuntimeError(f"下载到的依赖文件与已审核方案不一致：{actual}")
        for name, expected_hash in expected_wheels.items():
            if _shutdown_requested():
                return False
            if _sha256_file(downloaded[name]) != str(expected_hash).lower():
                raise RuntimeError(f"依赖完整性校验失败：{name}")

        if kind == "visual":
            dependency_progress(45, "依赖完整性校验通过", "正在安装依赖到你选择的文件夹。")
            dependency_progress(50, "正在安装本地依赖", "正在安装 NumPy、Pillow 与 OpenCV。")
        result = run_child(
            [
                pip_python, "-m", "pip", "--isolated", "install", "--no-input", "--no-cache-dir",
                "--disable-pip-version-check", "--no-index", "--no-deps", "--target", str(stage),
                *[str(downloaded[name]) for name in sorted(expected_wheels)],
            ],
            timeout=480.0, cwd=str(app_dir), env=pip_env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
        _safe_rmtree(wheels, ignore_errors=True)
        if result is None:
            if _shutdown_requested():
                return False
            raise RuntimeError("本地依赖安装超时或被终止。")
        if result.returncode != 0:
            raise RuntimeError(f"本地依赖安装失败，pip 返回代码 {result.returncode}。")
        if kind == "visual":
            dependency_progress(58, "本地依赖安装完成", "正在执行本地依赖自检。")
        if not smoke_test_fn(stage):
            if _shutdown_requested():
                return False
            raise RuntimeError(f"已审核依赖方案安装自检失败：{manifest.get('name', kind)}")
        if kind == "visual":
            marker_name, marker_value = ".ready-v5", "5"
        elif kind == "gpu":
            marker_name, marker_value = ".ready-v3", "3"
        else:
            raise RuntimeError(f"未知依赖类型：{kind}")
        (stage / marker_name).write_text(marker_value, encoding="ascii")
        _write_dependency_integrity_manifest(stage)
        if not _dependency_tree_integrity_valid(stage):
            raise RuntimeError(f"已审核依赖方案安装摘要验证失败：{manifest.get('name', kind)}")
        if kind == "visual":
            dependency_progress(60, "本地依赖自检通过", "正在切换到已验证的本地依赖。")
        return True

    def smoke_test(directory):
        if _shutdown_requested():
            return False
        _assert_storage_subtree_no_reparse(directory)
        env = os.environ.copy()
        env["PYTHONPATH"] = str(directory)
        env["MAKEITBIGGER_DEPS"] = str(directory)
        code = (
            "import os,pathlib,numpy as n,cv2,PIL; from PIL import Image; "
            "base=pathlib.Path(os.environ['MAKEITBIGGER_DEPS']).resolve(); "
            "mods=(n,cv2,PIL); assert all(base in pathlib.Path(m.__file__).resolve().parents for m in mods); "
            "a=n.zeros((8,8),dtype=n.uint8); assert cv2.countNonZero(a)==0; "
            "assert Image.new('L',(2,2)).size==(2,2)"
        )
        result = run_child(
            [sys.executable, "-c", code], cwd=str(app_dir), env=env,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            timeout=_clamp(20.0 + hardware_profile["capacity"] * 4.0, 24.0, 45.0),
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
        if _shutdown_requested():
            return False
        return result is not None and result.returncode == 0

    def prepare_dependencies_once(manifest):
        return _prepare_hashed_dependency_set(manifest, stage_dir, wheel_dir, smoke_test, "visual")

    if _shutdown_requested():
        return
    dependency_progress(20, "正在检查本地依赖", "检查本地视觉依赖是否完整可用。")
    ready = deps_dir / ready_marker
    dependencies_ready = ready.exists() and _dependency_tree_integrity_valid(deps_dir) and smoke_test(deps_dir)
    if _shutdown_requested():
        return

    if not dependencies_ready:
        ensure_local_pip()
        last_error = None
        prepared = False
        for recovery_attempt in range(4):
            if _shutdown_requested():
                _safe_rmtree(stage_dir, ignore_errors=True)
                _safe_rmtree(wheel_dir, ignore_errors=True)
                return
            if recovery_attempt:
                dependency_progress(
                    last_dependency_progress,
                    "正在自动修复启动环境",
                    "上一轮已审核依赖方案均未成功，程序正在自动清理临时文件并重试。",
                )
            for manifest_index, manifest in enumerate(dependency_manifests):
                if _shutdown_requested():
                    _safe_rmtree(stage_dir, ignore_errors=True)
                    _safe_rmtree(wheel_dir, ignore_errors=True)
                    return
                dependency_progress(
                    last_dependency_progress,
                    "正在尝试已审核依赖方案",
                    f"方案 {manifest_index + 1}/{len(dependency_manifests)}：{manifest['name']}，仅接受固定版本与固定 SHA-256。",
                )
                try:
                    prepared = prepare_dependencies_once(manifest)
                    if prepared:
                        last_error = None
                        break
                except StorageSafetyError:
                    raise
                except Exception as exc:
                    last_error = exc
                    _log_exception(
                        f"dependency manifest {manifest['name']} attempt {recovery_attempt + 1}", exc
                    )
                    _safe_rmtree(stage_dir, ignore_errors=True)
                    _safe_rmtree(wheel_dir, ignore_errors=True)
            if prepared:
                break
            if recovery_attempt < 3:
                delay = min(8.0, 1.0 * (2 ** recovery_attempt))
                dependency_progress(
                    last_dependency_progress,
                    "正在自动恢复启动环境",
                    f"已审核依赖方案均未成功；程序将在短暂退避后自动重试（{recovery_attempt + 2}/4）。",
                )
                if shutdown_event.wait(delay):
                    return
        if not prepared and last_error is not None:
            raise last_error
        _safe_rmtree(wheel_dir, ignore_errors=True)
        if not prepared:
            _safe_rmtree(stage_dir, ignore_errors=True)
            if last_error is not None:
                raise last_error
            if _shutdown_requested():
                return
            raise RuntimeError("本地运行依赖自动准备失败。")
        if _shutdown_requested():
            _safe_rmtree(stage_dir, ignore_errors=True)
            return
        _safe_rmtree(old_dir, ignore_errors=True)
        try:
            if deps_dir.exists():
                os.replace(deps_dir, old_dir)
            os.replace(stage_dir, deps_dir)
            _assert_storage_subtree_no_reparse(deps_dir)
            _safe_rmtree(old_dir, ignore_errors=True)
        except Exception:
            if not deps_dir.exists() and old_dir.exists():
                os.replace(old_dir, deps_dir)
            _safe_rmtree(stage_dir, ignore_errors=True)
            raise
    else:
        dependency_progress(60, "本地依赖已就绪", "已验证本地视觉依赖，正在加载组件。")

    _safe_rmtree(pip_bootstrap_dir, ignore_errors=True)
    if _shutdown_requested():
        return
    set_progress(61, "正在加载 NumPy", "正在导入本地数值计算组件。", phase="正在准备运行环境")
    if str(deps_dir) not in sys.path:
        sys.path.insert(0, str(deps_dir))
    import importlib
    importlib.invalidate_caches()
    if _shutdown_requested():
        return
    import numpy as _np
    set_progress(62.5, "正在加载 OpenCV", "正在导入本地视觉处理组件。", phase="正在准备运行环境")
    import cv2 as _cv2
    set_progress(64, "正在加载 Pillow", "正在导入本地图像与字体组件。", phase="正在准备运行环境")
    from PIL import Image as _Image, ImageGrab as _ImageGrab, ImageDraw as _ImageDraw, ImageFont as _ImageFont
    if _shutdown_requested():
        return

    def gpu_pci_order():
        values = [hardware_profile.get("gpu_pci_bus_id")]
        values.extend(item.get("pci_bus_id") for item in hardware_profile.get("gpu_candidates", ()) if isinstance(item, dict))
        ordered = []
        for value in values:
            normalized = _normalize_pci_bus_id(value)
            if normalized and normalized not in ordered:
                ordered.append(normalized)
        return ordered

    def gpu_smoke_test(directory):
        _assert_storage_subtree_no_reparse(directory)
        env = os.environ.copy()
        env["PYTHONPATH"] = os.pathsep.join((str(directory), str(deps_dir)))
        env["MAKEITBIGGER_GPU_DEPS"] = str(Path(directory).resolve())
        env["MAKEITBIGGER_GPU_PCI_ORDER"] = ";".join(gpu_pci_order())
        code = r"""
import os, pathlib, re, cupy as c

def norm(value):
    if isinstance(value, (bytes, bytearray)):
        value = bytes(value).decode("ascii", "ignore")
    text = str(value or "").strip().upper()
    match = re.fullmatch(r"([0-9A-F]+):([0-9A-F]{2}):([0-9A-F]{2})\.([0-7])", text)
    if not match:
        return ""
    domain, bus, device, function = match.groups()
    return f"{int(domain, 16):X}:{bus}:{device}.{function}"

root = pathlib.Path(os.environ["MAKEITBIGGER_GPU_DEPS"]).resolve()
mod = pathlib.Path(c.__file__).resolve()
assert root == mod or root in mod.parents
count = int(c.cuda.runtime.getDeviceCount())
assert count > 0
visible = {}
for index in range(count):
    pci = norm(c.cuda.runtime.deviceGetPCIBusId(index))
    if pci and pci not in visible:
        visible[pci] = index
requested = [norm(value) for value in os.environ.get("MAKEITBIGGER_GPU_PCI_ORDER", "").split(";")]
requested = [value for value in requested if value]
idx = next((visible[value] for value in requested if value in visible), None)
assert idx is not None
c.cuda.Device(idx).use()
a = c.arange(64, dtype=c.float32).reshape(8, 8)
b = a @ a
assert float(c.asnumpy(b[0, 0])) >= 0
c.cuda.runtime.deviceSynchronize()
"""
        result = run_child(
            [sys.executable, "-c", code], cwd=str(app_dir), env=env,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=60.0,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
        return result is not None and result.returncode == 0

    gpu_ready_marker = gpu_deps_dir / ".ready-v3"
    gpu_backend_error = None
    gpu_validation_error = None
    try:
        gpu_ready = gpu_ready_marker.exists() and _dependency_tree_integrity_valid(gpu_deps_dir) and gpu_smoke_test(gpu_deps_dir)
    except StorageSafetyError:
        raise
    except Exception as exc:
        gpu_ready = False
        gpu_validation_error = exc
        _log_exception("existing GPU backend validation", exc)

    if not gpu_ready:
        if gpu_validation_error is not None:
            _log_runtime("warning", f"existing GPU backend validation failed; rebuilding automatically: {gpu_validation_error}")
        gpu_stage = app_dir / "gpu-deps.new"
        gpu_old = app_dir / "gpu-deps.old"
        gpu_wheels = app_dir / "gpu-wheels.new"
        try:
            ensure_local_pip()

            def prepare_gpu_manifest(manifest):
                return _prepare_hashed_dependency_set(manifest, gpu_stage, gpu_wheels, gpu_smoke_test, "gpu")

            dependency_progress(63.5, "正在准备 NVIDIA GPU 计算后端", "正在自动尝试固定版本、固定 SHA-256 的本地 CUDA 依赖方案。")
            gpu_last_error = None
            gpu_prepared = False
            for manifest_index, manifest in enumerate(gpu_manifests):
                if _shutdown_requested():
                    _safe_rmtree(gpu_stage, ignore_errors=True)
                    _safe_rmtree(gpu_wheels, ignore_errors=True)
                    return
                dependency_progress(63.5, "正在尝试已审核 GPU 依赖方案", f"方案 {manifest_index + 1}/{len(gpu_manifests)}：{manifest['name']}，只安装通过固定 SHA-256 校验的 wheel。")
                try:
                    gpu_prepared = prepare_gpu_manifest(manifest)
                    if gpu_prepared:
                        gpu_last_error = None
                        break
                except StorageSafetyError:
                    raise
                except Exception as exc:
                    gpu_last_error = exc
                    _log_exception(f"GPU dependency manifest {manifest['name']}", exc)
                    _safe_rmtree(gpu_stage, ignore_errors=True)
                    _safe_rmtree(gpu_wheels, ignore_errors=True)
            if not gpu_prepared:
                raise gpu_last_error or RuntimeError("NVIDIA GPU 计算后端自动准备失败。")

            _safe_rmtree(gpu_old, ignore_errors=True)
            try:
                if gpu_deps_dir.exists():
                    os.replace(gpu_deps_dir, gpu_old)
                os.replace(gpu_stage, gpu_deps_dir)
                _assert_storage_subtree_no_reparse(gpu_deps_dir)
                _safe_rmtree(gpu_old, ignore_errors=True)
            except Exception:
                if not gpu_deps_dir.exists() and gpu_old.exists():
                    os.replace(gpu_old, gpu_deps_dir)
                raise
        except StorageSafetyError:
            raise
        except Exception as exc:
            gpu_backend_error = exc
            _log_exception("GPU backend preparation", exc)
            _safe_rmtree(gpu_stage, ignore_errors=True)
            _safe_rmtree(gpu_wheels, ignore_errors=True)
            _log_runtime("warning", f"GPU backend unavailable; continuing with NumPy CPU fallback: {exc}")

    _cp = None
    if gpu_backend_error is None:
        try:
            if str(gpu_deps_dir) not in sys.path:
                sys.path.insert(0, str(gpu_deps_dir))
            import cupy as _cp
            if int(_cp.cuda.runtime.getDeviceCount()) <= 0:
                raise RuntimeError("CUDA 后端没有检测到可用 NVIDIA GPU。")
            alternate_pci_ids = [
                item.get("pci_bus_id") for item in hardware_profile.get("gpu_candidates", ()) if isinstance(item, dict)
            ]
            gpu_index = _cupy_device_index_for_pci(_cp, hardware_profile.get("gpu_pci_bus_id"), alternate_pci_ids)
            _cp.cuda.Device(gpu_index).use()
            actual_gpu_pci = _normalize_pci_bus_id(_cp.cuda.runtime.deviceGetPCIBusId(gpu_index))
            if not actual_gpu_pci:
                raise RuntimeError("CuPy 未返回可验证的 CUDA GPU PCI Bus ID。")
            active_gpu_pci_bus_id = actual_gpu_pci
            hardware_profile["active_gpu_pci_bus_id"] = actual_gpu_pci
            for candidate in hardware_profile.get("gpu_candidates", ()):
                if isinstance(candidate, dict) and _normalize_pci_bus_id(candidate.get("pci_bus_id")) == actual_gpu_pci:
                    hardware_profile["gpu_index"] = int(candidate.get("smi_index", 0))
                    hardware_profile["gpu_pci_bus_id"] = actual_gpu_pci
                    hardware_profile["gpu_uuid"] = candidate.get("uuid")
                    hardware_profile["gpu_name"] = candidate.get("name")
                    hardware_profile["gpu_total_mib"] = float(candidate.get("total_mib", 0.0))
                    hardware_profile["gpu_free_mib"] = float(candidate.get("free_mib", 0.0))
                    hardware_profile["gpu_util"] = float(candidate.get("util", 0.0))
                    hardware_profile["gpu_headroom"] = _clamp(
                        hardware_profile["gpu_free_mib"] / max(1.0, hardware_profile["gpu_total_mib"]), 0.05, 1.0
                    )
                    break
            hardware_profile["gpu_cuda_index"] = gpu_index
            test = _cp.arange(16, dtype=_cp.float32).reshape(4, 4)
            _ = test @ test
            _cp.cuda.runtime.deviceSynchronize()
        except Exception as exc:
            gpu_backend_error = exc
            active_gpu_pci_bus_id = None
            hardware_profile.pop("active_gpu_pci_bus_id", None)
            _log_exception("GPU runtime initialization", exc)
            _cp = None

    _safe_rmtree(pip_bootstrap_dir, ignore_errors=True)
    np, cp, cv2 = _np, _cp, _cv2
    Image, ImageGrab, ImageDraw, ImageFont = _Image, _ImageGrab, _ImageDraw, _ImageFont
    cv2.setNumThreads(max(1, int(hardware_profile["cv_threads"])))
    if cp is None:
        hardware_profile["gpu_compute_backend"] = "NumPy / CPU fallback"
        set_progress(65, "本地视觉组件已加载", "NVIDIA GPU 后端当前不可用；程序已自动切换到 NumPy CPU 后端，并会在下次启动重新尝试 GPU。", phase="正在准备本地 AI")
    else:
        hardware_profile["gpu_compute_backend"] = "CuPy / CUDA"
        set_progress(65, "GPU 计算后端与本地视觉组件已加载", "自建数字模型的矩阵计算将使用 NVIDIA GPU。", phase="正在准备本地 AI")

    if _shutdown_requested():
        return
    recognizer = LocalDigitRecognizer()
    if _shutdown_requested():
        return
    set_progress(97, "本机数字视觉模型已就绪", "正在初始化本地学习与输入控制组件。", phase="正在完成启动")
    controller = LearningController()
    if _shutdown_requested():
        return

    hardware_thread = threading.Thread(target=_hardware_monitor_loop, name="MakeItBiggerHardware", daemon=True)
    hardware_thread.start()
    set_progress(99, "正在安装鼠标和键盘输入监听", "监听就绪前 AI 不会控制任何输入。", phase="正在完成启动")
    if _shutdown_requested():
        return
    release_thread = threading.Thread(target=controller.run_release_worker, name="MakeItBiggerInputRelease", daemon=True)
    release_thread.start()
    hook_thread = threading.Thread(target=controller.run_input_monitor, name="MakeItBiggerInputHook", daemon=True)
    hook_thread.start()


def dependency_failed(text):
    _clear_overlays_and_show_error(text)


def _as_decimal(value):
    if isinstance(value, Decimal):
        result = value
    elif isinstance(value, int):
        result = Decimal(value)
    elif isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError("number is not finite")
        result = Decimal(str(value))
    else:
        result = Decimal(str(value).strip())
    if not result.is_finite():
        raise ValueError("number is not finite")
    return result


def _same_number(a, b):
    try:
        return _as_decimal(a) == _as_decimal(b)
    except (InvalidOperation, TypeError, ValueError):
        return False


def _decimal_quantum(value):
    number = _as_decimal(value)
    exponent = number.as_tuple().exponent
    return Decimal(1).scaleb(exponent)


def _observation_value_and_quantum(observation):
    if isinstance(observation, dict):
        value = _as_decimal(observation.get("value"))
        raw_quantum = observation.get("display_quantum")
        try:
            quantum = abs(_as_decimal(raw_quantum)) if raw_quantum is not None else abs(_decimal_quantum(value))
        except (InvalidOperation, TypeError, ValueError):
            quantum = abs(_decimal_quantum(value))
        return value, max(quantum, Decimal("1e-10000"))
    value = _as_decimal(observation)
    return value, max(abs(_decimal_quantum(value)), Decimal("1e-10000"))


def _same_ocr_number(a, b):
    try:
        av, aq = _observation_value_and_quantum(a)
        bv, bq = _observation_value_and_quantum(b)
        tolerance = min(aq, bq) * Decimal("0.25")
        return abs(av - bv) <= tolerance
    except (InvalidOperation, TypeError, ValueError):
        return False


def _number_key(value):
    return _as_decimal(value).normalize()


def _format_number(value):
    number = _as_decimal(value)
    if number.is_zero():
        return "0"
    normalized = number.normalize()
    adjusted = normalized.adjusted()
    if normalized == normalized.to_integral_value() and -6 <= adjusted <= 18:
        return format(normalized, "f")
    if -6 <= adjusted <= 18:
        return format(normalized, "f")
    return format(normalized, "E").replace("E", "e")


def _format_number_like_observation(value, observation):
    number = _as_decimal(value)
    raw = str((observation or {}).get("raw_text") or (observation or {}).get("text") or "").strip()
    if not raw:
        return _format_number(number)
    try:
        _old_value, quantum = _observation_value_and_quantum(observation)
        decimals = max(0, -int(quantum.normalize().as_tuple().exponent))
    except Exception:
        decimals = max(0, -int(number.as_tuple().exponent))
    parenthesized = raw.startswith("(") and raw.endswith(")")
    core = raw[1:-1].strip() if parenthesized else raw
    explicit_plus = core.startswith("+")
    unsigned_core = core.lstrip("+-").strip()
    scientific = re.fullmatch(r"(.+?)([eE])([+-]?)(\d+)", unsigned_core)
    if scientific:
        mantissa, marker, exp_sign, exp_digits = scientific.groups()
        punct = [i for i, ch in enumerate(mantissa) if ch in ".,"]
        frac_digits = 0
        decimal_sep = "."
        if punct:
            pos = punct[-1]
            frac_digits = sum(ch.isdigit() for ch in mantissa[pos + 1:])
            decimal_sep = mantissa[pos]
        else:
            frac_digits = decimals
        rendered = format(abs(number), f".{frac_digits}E")
        out_mantissa, out_exp = rendered.split("E", 1)
        if decimal_sep != ".":
            out_mantissa = out_mantissa.replace(".", decimal_sep)
        exp_value = int(out_exp)
        exp_width = max(1, len(exp_digits))
        out_exp_text = f"{abs(exp_value):0{exp_width}d}"
        out = f"{out_mantissa}{marker}{'+' if exp_value >= 0 else '-'}{out_exp_text}"
    else:
        punctuation = [i for i, ch in enumerate(unsigned_core) if ch in ".,"]
        decimal_sep = None
        if decimals > 0 and punctuation:
            decimal_sep = unsigned_core[punctuation[-1]]
        grouping_sep = None
        for sep in (",", "."):
            if sep in unsigned_core and sep != decimal_sep:
                grouping_sep = sep
                break
        raw_integer = unsigned_core
        if decimal_sep is not None:
            raw_integer = raw_integer.rsplit(decimal_sep, 1)[0]
        raw_integer_digits = "".join(ch for ch in raw_integer if ch.isdigit())
        int_width = max(1, len(raw_integer_digits))
        fixed = format(abs(number), f".{decimals}f")
        integer, dot, fraction = fixed.partition(".")
        integer = integer.zfill(int_width)
        if grouping_sep:
            groups = []
            while integer:
                groups.append(integer[-3:])
                integer = integer[:-3]
            integer = grouping_sep.join(reversed(groups))
        if decimals > 0:
            out = integer + (decimal_sep or ".") + fraction
        else:
            out = integer
    if number < 0:
        return f"({out})" if parenthesized else "-" + out
    if explicit_plus:
        return "+" + out
    return out


def _decimal_to_learning_float(value):
    number = abs(_as_decimal(value))
    if number.is_zero():
        return 0.0
    if number.adjusted() > 300:
        return 1e300
    try:
        converted = float(number)
    except (OverflowError, ValueError):
        return 1e300
    return min(1e300, max(0.0, converted))


class LocalDigitRecognizer:
    LABELS = tuple("0123456789+-.,eE()")
    MODEL_VERSION = "self-trained-digit-mlp-v5"
    INPUT_SHAPE = (28, 20)
    HIDDEN = 96
    GPU_INFERENCE_MIN_BATCH = 64
    OCR_CANARY_PER_LABEL = 24

    def __init__(self):
        self.model_path = app_dir / "digit_model.npz"
        self.model_backup_path = app_dir / "digit_model.bak.npz"
        self.self_sample_path = app_dir / "digit_self_samples.npz"
        self.self_sample_backup_path = app_dir / "digit_self_samples.bak.npz"
        self.guard_valid_x = None
        self.guard_valid_y = None
        self._gpu_weights = None
        self.gpu_disabled = cp is None
        self.self_sample_lock = threading.Lock()
        self.self_features = []
        self.self_labels = []
        self.self_sample_weights = []
        self.self_sample_sources = []
        self.canary_features = []
        self.canary_labels = []
        self.self_sample_seen = [0 for _ in self.LABELS]
        self.bad_font_paths = set()
        self.new_self_samples = 0
        self.last_self_tune = time.monotonic()
        self.label_to_index = {label: i for i, label in enumerate(self.LABELS)}
        try:
            locale.setlocale(locale.LC_NUMERIC, "")
            conv = locale.localeconv()
        except Exception:
            conv = {}
        self.locale_decimal = str(conv.get("decimal_point") or ".")
        self.locale_thousands = str(conv.get("thousands_sep") or "")
        loaded = self._load_model()
        self._load_self_samples()
        if loaded:
            set_progress(94, "已加载本机数字视觉模型", "本机模型已通过结构检查。", phase="正在准备本地 AI")
        else:
            set_progress(65, "正在生成本机数字视觉模型", "正在生成本机训练样本。", phase="正在准备本地 AI")
            if _shutdown_requested():
                return
            self._train_model()
            if _shutdown_requested():
                return
            if self.self_features:
                set_progress(94.5, "正在融合已有本机学习样本", "正在把历史确认样本融入新模型。", phase="正在准备本地 AI")
                self._fine_tune_self_samples(force=True)
            set_progress(95, "正在保存本机数字视觉模型", "正在写入并原子替换本机模型文件。", phase="正在准备本地 AI")
            self._save_model()
            if _shutdown_requested():
                return
            set_progress(96, "正在验证本机数字视觉模型", "正在重新读取刚保存的模型并检查结构。", phase="正在准备本地 AI")
            if not self._load_model():
                raise RuntimeError("本机数字视觉模型保存后验证失败。")
            set_progress(97, "本机数字视觉模型验证通过", "模型已保存并可正常重新加载。", phase="正在准备本地 AI")

    def _font_paths(self):
        windir = Path(os.environ.get("WINDIR", r"C:\Windows")) / "Fonts"
        preferred = [
            "segoeui.ttf", "seguisb.ttf", "arial.ttf", "arialbd.ttf", "calibri.ttf", "calibrib.ttf",
            "consola.ttf", "consolab.ttf", "tahoma.ttf", "verdana.ttf", "times.ttf", "trebuc.ttf",
            "cour.ttf", "courbd.ttf", "georgia.ttf", "impact.ttf"
        ]
        found = []
        for name in preferred:
            path = windir / name
            if path.exists():
                found.append(path)
        for pattern in ("*.ttf", "*.otf", "*.ttc"):
            for path in sorted(windir.glob(pattern)):
                if path not in found:
                    found.append(path)
        usable = []
        for path in found:
            try:
                ImageFont.truetype(str(path), 32)
                usable.append(path)
            except Exception:
                continue
        if not usable:
            raise RuntimeError("找不到可用的 Windows 字体。")
        return usable

    def _normalize_mask(self, mask):
        mask = np.asarray(mask, dtype=np.uint8)
        ys, xs = np.where(mask > 0)
        if len(xs) == 0:
            return np.zeros(self.INPUT_SHAPE, dtype=np.float32).reshape(-1)
        crop = mask[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
        h, w = crop.shape
        target_h, target_w = self.INPUT_SHAPE
        scale = min((target_w - 4.0) / max(w, 1), (target_h - 4.0) / max(h, 1))
        nw, nh = max(1, int(round(w * scale))), max(1, int(round(h * scale)))
        interpolation = cv2.INTER_AREA if scale < 1.0 else cv2.INTER_LINEAR
        resized = cv2.resize(crop, (nw, nh), interpolation=interpolation)
        out = np.zeros((target_h, target_w), dtype=np.uint8)
        x0 = (target_w - nw) // 2
        y0 = (target_h - nh) // 2
        out[y0:y0 + nh, x0:x0 + nw] = resized
        return out.astype(np.float32).reshape(-1) / 255.0

    def _augment_mask(self, mask, rng):
        arr = np.asarray(mask, dtype=np.uint8)
        h, w = arr.shape
        angle = rng.uniform(-10.0, 10.0)
        scale_x = rng.uniform(0.76, 1.24)
        scale_y = rng.uniform(0.78, 1.22)
        matrix = cv2.getRotationMatrix2D((w / 2.0, h / 2.0), angle, 1.0)
        matrix[0, 0] *= scale_x
        matrix[0, 1] *= scale_x
        matrix[1, 0] *= scale_y
        matrix[1, 1] *= scale_y
        matrix[0, 2] += rng.uniform(-5.0, 5.0)
        matrix[1, 2] += rng.uniform(-5.0, 5.0)
        arr = cv2.warpAffine(arr, matrix, (w, h), flags=cv2.INTER_LINEAR, borderValue=0)
        if rng.random() < 0.65:
            shift = rng.uniform(-0.10, 0.10) * w
            src = np.float32([[0, 0], [w - 1, 0], [0, h - 1], [w - 1, h - 1]])
            dst = np.float32([[shift, 0], [w - 1 - shift, 0], [-shift, h - 1], [w - 1 + shift, h - 1]])
            perspective = cv2.getPerspectiveTransform(src, dst)
            arr = cv2.warpPerspective(arr, perspective, (w, h), flags=cv2.INTER_LINEAR, borderValue=0)
        if rng.random() < 0.48:
            k = rng.choice((2, 3))
            kernel = np.ones((k, k), dtype=np.uint8)
            if rng.random() < 0.5:
                arr = cv2.dilate(arr, kernel, iterations=1)
            else:
                arr = cv2.erode(arr, kernel, iterations=1)
        if rng.random() < 0.55:
            sigma = rng.uniform(0.15, 1.05)
            arr = cv2.GaussianBlur(arr, (0, 0), sigmaX=sigma, sigmaY=sigma)
        if rng.random() < 0.52:
            noise_rng = np.random.default_rng(rng.getrandbits(64))
            noise = noise_rng.normal(0.0, 13.0, size=arr.shape).astype(np.float32)
            arr = np.clip(arr.astype(np.float32) + noise, 0, 255).astype(np.uint8)
        threshold = rng.randint(45, 175)
        _, arr = cv2.threshold(arr, threshold, 255, cv2.THRESH_BINARY)
        return arr

    def _font_sample(self, label, font_path, rng):
        canvas = Image.new("L", (88, 88), 0)
        draw = ImageDraw.Draw(canvas)
        size = rng.randint(22, 66)
        font = ImageFont.truetype(str(font_path), size)
        stroke = rng.randint(0, 2)
        bbox = draw.textbbox((0, 0), label, font=font, stroke_width=stroke)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        x = 44 - tw // 2 - bbox[0] + rng.randint(-5, 5)
        y = 44 - th // 2 - bbox[1] + rng.randint(-5, 5)
        draw.text((x, y), label, fill=255, font=font, stroke_width=stroke, stroke_fill=255)
        return self._augment_mask(np.asarray(canvas), rng)

    def _safe_font_sample(self, label, font_paths, rng):
        candidates = [path for path in font_paths if str(path).lower() not in self.bad_font_paths]
        if not candidates:
            return None
        attempts = min(8, len(candidates))
        for font_path in rng.sample(candidates, attempts):
            try:
                return self._font_sample(label, font_path, rng)
            except (OSError, ValueError, RuntimeError, TypeError) as exc:
                self.bad_font_paths.add(str(font_path).lower())
                _log_runtime(
                    "warning",
                    f"font skipped: {font_path.name}: {exc.__class__.__name__}: {exc}",
                )
        return None

    def _seven_segment_sample(self, label, rng):
        canvas = np.zeros((88, 88), dtype=np.uint8)
        thickness = rng.randint(3, 8)
        left = rng.randint(17, 24)
        right = rng.randint(62, 70)
        top = rng.randint(12, 18)
        middle = rng.randint(40, 46)
        bottom = rng.randint(70, 77)
        segments = {
            "a": ((left + 4, top), (right - 4, top)),
            "b": ((right, top + 4), (right, middle - 4)),
            "c": ((right, middle + 4), (right, bottom - 4)),
            "d": ((left + 4, bottom), (right - 4, bottom)),
            "e": ((left, middle + 4), (left, bottom - 4)),
            "f": ((left, top + 4), (left, middle - 4)),
            "g": ((left + 4, middle), (right - 4, middle)),
        }
        digits = {
            "0": "ab cdef".replace(" ", ""), "1": "bc", "2": "abdeg", "3": "abcdg", "4": "bcfg",
            "5": "acdfg", "6": "acdefg", "7": "abc", "8": "abcdefg", "9": "abcdfg"
        }
        if label in digits:
            for name in digits[label]:
                p0, p1 = segments[name]
                cv2.line(canvas, p0, p1, 255, thickness=thickness, lineType=cv2.LINE_AA)
        elif label == "-":
            p0, p1 = segments["g"]
            cv2.line(canvas, p0, p1, 255, thickness=thickness, lineType=cv2.LINE_AA)
        elif label == "+":
            p0, p1 = segments["g"]
            cv2.line(canvas, p0, p1, 255, thickness=thickness, lineType=cv2.LINE_AA)
            cv2.line(canvas, ((left + right) // 2, top + 12), ((left + right) // 2, bottom - 12), 255, thickness=thickness, lineType=cv2.LINE_AA)
        elif label in ".,":
            cx = rng.randint(42, 51)
            cy = rng.randint(68, 77)
            cv2.circle(canvas, (cx, cy), max(2, thickness // 2), 255, -1, lineType=cv2.LINE_AA)
            if label == ",":
                cv2.line(canvas, (cx, cy + 1), (cx - rng.randint(2, 5), min(86, cy + rng.randint(7, 12))), 255, max(1, thickness // 2), lineType=cv2.LINE_AA)
        return self._augment_mask(canvas, rng)

    def _ood_augment_mask(self, mask, rng):
        arr = np.asarray(mask, dtype=np.uint8)
        h, w = arr.shape
        down = rng.uniform(0.42, 0.78)
        small = cv2.resize(arr, (max(8, int(w * down)), max(8, int(h * down))), interpolation=cv2.INTER_AREA)
        arr = cv2.resize(small, (w, h), interpolation=cv2.INTER_LINEAR)
        arr = cv2.GaussianBlur(arr, (0, 0), sigmaX=rng.uniform(0.8, 2.2))
        if rng.random() < 0.55:
            kernel = np.ones((rng.choice((2, 3)), rng.choice((2, 3))), dtype=np.uint8)
            arr = cv2.erode(arr, kernel, iterations=1) if rng.random() < 0.5 else cv2.dilate(arr, kernel, iterations=1)
        threshold = rng.randint(85, 205)
        _, arr = cv2.threshold(arr, threshold, 255, cv2.THRESH_BINARY)
        return arr

    def _make_training_set(self):
        train_rng = random.Random(731921)
        valid_rng = random.Random(918273)
        fonts = self._font_paths()
        holdout_fonts = fonts[::5] or fonts[-1:]
        holdout_set = {str(path).lower() for path in holdout_fonts}
        train_fonts = [path for path in fonts if str(path).lower() not in holdout_set] or fonts
        train_features, train_labels = [], []
        valid_features, valid_labels = [], []
        capacity = max(1.0, float(hardware_profile.get("capacity", 1.0)))
        base_font_rounds = int(_clamp(round(24 + capacity * 5.0), 28, 54))
        base_synth_rounds = int(_clamp(round(16 + capacity * 4.0), 20, 42))
        total_labels = len(self.LABELS)
        for label_index, label in enumerate(self.LABELS):
            if _shutdown_requested():
                empty_x = np.empty((0, self.INPUT_SHAPE[0] * self.INPUT_SHAPE[1]), dtype=np.float32)
                empty_y = np.empty((0,), dtype=np.int32)
                return empty_x, empty_y, empty_x.copy(), empty_y.copy()
            font_rounds = int(round(base_font_rounds * (1.15 if label in ".," else 1.0)))
            for _ in range(font_rounds):
                mask = self._safe_font_sample(label, train_fonts, train_rng)
                if mask is None:
                    mask = self._safe_font_sample(label, fonts, train_rng)
                if mask is None:
                    continue
                feat = self._normalize_mask(mask)
                if feat.sum() >= 2.0:
                    train_features.append(feat); train_labels.append(self.label_to_index[label])
            valid_rounds = max(7, int(round(font_rounds * 0.24)))
            for _ in range(valid_rounds):
                mask = self._safe_font_sample(label, holdout_fonts, valid_rng)
                if mask is None:
                    mask = self._safe_font_sample(label, fonts, valid_rng)
                if mask is None:
                    continue
                mask = self._ood_augment_mask(mask, valid_rng)
                feat = self._normalize_mask(mask)
                if feat.sum() >= 2.0:
                    valid_features.append(feat); valid_labels.append(self.label_to_index[label])
            synth_rounds = int(round(base_synth_rounds * (1.20 if label.isdigit() else 0.75))) if label in "0123456789+-.," else 0
            for _ in range(synth_rounds):
                mask = self._seven_segment_sample(label, train_rng)
                feat = self._normalize_mask(mask)
                if feat.sum() >= 2.0:
                    train_features.append(feat); train_labels.append(self.label_to_index[label])
            for _ in range(max(3, synth_rounds // 5)):
                if not synth_rounds:
                    break
                mask = self._ood_augment_mask(self._seven_segment_sample(label, valid_rng), valid_rng)
                feat = self._normalize_mask(mask)
                if feat.sum() >= 2.0:
                    valid_features.append(feat); valid_labels.append(self.label_to_index[label])
            done = label_index + 1
            set_progress(
                65.0 + 13.0 * done / total_labels,
                "正在生成本机数字训练样本",
                f"正在准备字符样本 {done}/{total_labels}",
                phase="正在准备本地 AI",
            )
        train_x = np.asarray(train_features, dtype=np.float32)
        train_y = np.asarray(train_labels, dtype=np.int32)
        valid_x = np.asarray(valid_features, dtype=np.float32)
        valid_y = np.asarray(valid_labels, dtype=np.int32)
        train_order = np.random.default_rng(731921).permutation(len(train_x))
        valid_order = np.random.default_rng(918273).permutation(len(valid_x))
        return train_x[train_order], train_y[train_order], valid_x[valid_order], valid_y[valid_order]

    def _disable_gpu_backend(self, context, exc):
        if not self.gpu_disabled:
            _log_exception(f"GPU backend disabled during {context}", exc)
            _log_runtime("warning", f"GPU backend failed during {context}; continuing with NumPy CPU fallback: {exc}")
        self.gpu_disabled = True
        self._gpu_weights = None
        hardware_profile["gpu_compute_backend"] = "NumPy / CPU fallback"

    def _invalidate_gpu_weights(self):
        self._gpu_weights = None

    def _gpu_weight_arrays(self):
        if cp is None or self.gpu_disabled:
            return None
        if self._gpu_weights is None:
            self._gpu_weights = (
                cp.asarray(self.w1), cp.asarray(self.b1), cp.asarray(self.w2), cp.asarray(self.b2)
            )
        return self._gpu_weights

    def _forward(self, x):
        if cp is not None and not self.gpu_disabled and len(x) >= self.GPU_INFERENCE_MIN_BATCH:
            try:
                weights = self._gpu_weight_arrays()
                if weights is not None:
                    w1g, b1g, w2g, b2g = weights
                    xg = cp.asarray(x, dtype=cp.float32)
                    hidden_g = cp.maximum(cp.float32(0.0), xg @ w1g + b1g)
                    logits_g = hidden_g @ w2g + b2g
                    logits_g -= logits_g.max(axis=1, keepdims=True)
                    exp_g = cp.exp(logits_g)
                    probs_g = exp_g / cp.maximum(exp_g.sum(axis=1, keepdims=True), cp.float32(1e-8))
                    return None, cp.asnumpy(probs_g)
            except Exception as exc:
                self._disable_gpu_backend("OCR inference", exc)
        hidden = np.maximum(0.0, x @ self.w1 + self.b1)
        logits = hidden @ self.w2 + self.b2
        logits -= logits.max(axis=1, keepdims=True)
        exp = np.exp(logits)
        probs = exp / np.maximum(exp.sum(axis=1, keepdims=True), 1e-8)
        return hidden, probs

    def _gpu_gradients_from_arrays(self, xg, yg, w1g, b1g, w2g, b2g, l2, sample_weights=None):
        hidden = cp.maximum(cp.float32(0.0), xg @ w1g + b1g)
        logits = hidden @ w2g + b2g
        logits -= logits.max(axis=1, keepdims=True)
        exp = cp.exp(logits)
        probs = exp / cp.maximum(exp.sum(axis=1, keepdims=True), cp.float32(1e-8))
        grad = probs.copy()
        grad[cp.arange(len(yg)), yg] -= cp.float32(1.0)
        if sample_weights is None:
            grad /= cp.float32(max(1, len(yg)))
        else:
            wg = cp.asarray(sample_weights, dtype=cp.float32).reshape((-1, 1))
            grad *= wg
            grad /= cp.maximum(wg.sum(), cp.float32(1e-6))
        gw2 = hidden.T @ grad + w2g * cp.float32(l2)
        gb2 = grad.sum(axis=0)
        gh = grad @ w2g.T
        gh[hidden <= 0.0] = 0.0
        gw1 = xg.T @ gh + w1g * cp.float32(l2)
        gb1 = gh.sum(axis=0)
        return gw1, gb1, gw2, gb2

    def _mlp_gradients(self, xb, yb, l2, sample_weights=None):
        hidden = np.maximum(0.0, xb @ self.w1 + self.b1)
        logits = hidden @ self.w2 + self.b2
        logits -= logits.max(axis=1, keepdims=True)
        exp = np.exp(logits)
        probs = exp / np.maximum(exp.sum(axis=1, keepdims=True), 1e-8)
        grad = probs.copy()
        grad[np.arange(len(yb)), yb] -= 1.0
        if sample_weights is None:
            grad /= max(1, len(yb))
        else:
            weights = np.asarray(sample_weights, dtype=np.float32).reshape((-1, 1))
            grad *= weights
            grad /= max(1e-6, float(weights.sum()))
        gw2 = hidden.T @ grad + self.w2 * l2
        gb2 = grad.sum(axis=0)
        gh = grad @ self.w2.T
        gh[hidden <= 0.0] = 0.0
        gw1 = xb.T @ gh + self.w1 * l2
        gb1 = gh.sum(axis=0)
        return gw1, gb1, gw2, gb2

    def _train_batches_gpu(self, train_x, train_y, valid_x, valid_y, rng, batch, epochs):
        train_xg = cp.asarray(train_x, dtype=cp.float32)
        train_yg = cp.asarray(train_y, dtype=cp.int32)
        valid_xg = cp.asarray(valid_x, dtype=cp.float32) if len(valid_x) else None
        valid_yg = cp.asarray(valid_y, dtype=cp.int32) if len(valid_y) else None
        params = [cp.asarray(self.w1), cp.asarray(self.b1), cp.asarray(self.w2), cp.asarray(self.b2)]
        moments = [cp.zeros_like(param) for param in params]
        variances = [cp.zeros_like(param) for param in params]
        best_weights = [param.copy() for param in params]
        best_score = -1.0
        step = 0
        for epoch_index in range(epochs):
            if _shutdown_requested():
                return None
            orderg = cp.asarray(rng.permutation(len(train_x)), dtype=cp.int32)
            for offset in range(0, len(train_x), batch):
                if _shutdown_requested():
                    return None
                idxg = orderg[offset:offset + batch]
                gradients = self._gpu_gradients_from_arrays(train_xg[idxg], train_yg[idxg], *params, 0.0001)
                step += 1
                for i, gradient in enumerate(gradients):
                    moments[i] *= cp.float32(0.9)
                    moments[i] += gradient * cp.float32(0.1)
                    variances[i] *= cp.float32(0.999)
                    variances[i] += gradient * gradient * cp.float32(0.001)
                    m_hat = moments[i] / cp.float32(1.0 - 0.9 ** step)
                    v_hat = variances[i] / cp.float32(1.0 - 0.999 ** step)
                    params[i] -= cp.float32(0.003) * m_hat / (cp.sqrt(v_hat) + cp.float32(1e-8))
            if valid_xg is not None:
                hidden = cp.maximum(cp.float32(0.0), valid_xg @ params[0] + params[1])
                logits = hidden @ params[2] + params[3]
                score = float(cp.asnumpy(cp.mean(cp.argmax(logits, axis=1) == valid_yg)))
                if score > best_score:
                    best_score = score
                    best_weights = [param.copy() for param in params]
            completed_epochs = epoch_index + 1
            set_progress(78.0 + 15.5 * completed_epochs / epochs, "正在训练本机数字视觉模型", f"训练轮次 {completed_epochs}/{epochs}", phase="正在准备本地 AI")
        return tuple(cp.asnumpy(param).astype(np.float32, copy=False) for param in best_weights)

    def _train_batches_cpu(self, train_x, train_y, valid_x, valid_y, rng, batch, epochs):
        params = [self.w1, self.b1, self.w2, self.b2]
        moments = [np.zeros_like(param) for param in params]
        variances = [np.zeros_like(param) for param in params]
        best_weights = [param.copy() for param in params]
        best_score = -1.0
        step = 0
        for epoch_index in range(epochs):
            if _shutdown_requested():
                return None
            order = rng.permutation(len(train_x))
            for offset in range(0, len(order), batch):
                if _shutdown_requested():
                    return None
                idx = order[offset:offset + batch]
                gradients = self._mlp_gradients(train_x[idx], train_y[idx], 0.0001)
                step += 1
                for i, gradient in enumerate(gradients):
                    moments[i] *= 0.9
                    moments[i] += gradient * 0.1
                    variances[i] *= 0.999
                    variances[i] += gradient * gradient * 0.001
                    m_hat = moments[i] / (1.0 - 0.9 ** step)
                    v_hat = variances[i] / (1.0 - 0.999 ** step)
                    params[i] -= 0.003 * m_hat / (np.sqrt(v_hat) + 1e-8)
            if len(valid_x):
                hidden = np.maximum(0.0, valid_x @ self.w1 + self.b1)
                logits = hidden @ self.w2 + self.b2
                score = float(np.mean(np.argmax(logits, axis=1) == valid_y))
                if score > best_score:
                    best_score = score
                    best_weights = [param.copy() for param in params]
            completed_epochs = epoch_index + 1
            set_progress(78.0 + 15.5 * completed_epochs / epochs, "正在训练本机数字视觉模型", f"训练轮次 {completed_epochs}/{epochs}", phase="正在准备本地 AI")
        return tuple(param.copy() for param in best_weights)

    def _train_model(self):
        train_x, train_y, valid_x, valid_y = self._make_training_set()
        if _shutdown_requested():
            return
        minimum = max(len(self.LABELS) * 12, self.HIDDEN * 2)
        if len(train_x) < minimum or len(valid_x) < len(self.LABELS) * 3:
            raise RuntimeError("本机训练或独立验证样本不足。")
        rng = np.random.default_rng(731921)
        input_dim = train_x.shape[1]
        output_dim = len(self.LABELS)
        self.w1 = (rng.standard_normal((input_dim, self.HIDDEN)).astype(np.float32) * math.sqrt(2.0 / input_dim))
        self.b1 = np.zeros((self.HIDDEN,), dtype=np.float32)
        self.w2 = (rng.standard_normal((self.HIDDEN, output_dim)).astype(np.float32) * math.sqrt(2.0 / self.HIDDEN))
        self.b2 = np.zeros((output_dim,), dtype=np.float32)
        batch = max(1, min(len(train_x), int(hardware_profile["training_batch"])))
        epochs = max(1, int(hardware_profile["training_epochs"]))
        set_progress(78, "正在训练本机数字视觉模型", f"训练轮次 0/{epochs}", phase="正在准备本地 AI")

        weights = None
        if cp is not None and not self.gpu_disabled:
            try:
                weights = self._train_batches_gpu(train_x, train_y, valid_x, valid_y, rng, batch, epochs)
            except Exception as exc:
                self._disable_gpu_backend("OCR training", exc)
        if weights is None and not _shutdown_requested():
            # Reinitialize before CPU retry so a failed GPU attempt can never leak partial state.
            rng = np.random.default_rng(731921)
            self.w1 = (rng.standard_normal((input_dim, self.HIDDEN)).astype(np.float32) * math.sqrt(2.0 / input_dim))
            self.b1 = np.zeros((self.HIDDEN,), dtype=np.float32)
            self.w2 = (rng.standard_normal((self.HIDDEN, output_dim)).astype(np.float32) * math.sqrt(2.0 / self.HIDDEN))
            self.b2 = np.zeros((output_dim,), dtype=np.float32)
            weights = self._train_batches_cpu(train_x, train_y, valid_x, valid_y, rng, batch, epochs)
        if weights is None:
            return
        self.w1[:], self.b1[:], self.w2[:], self.b2[:] = weights
        self._invalidate_gpu_weights()

        self.centroids = np.zeros((output_dim, input_dim), dtype=np.float32)
        self.radii = np.zeros((output_dim,), dtype=np.float32)
        for idx in range(output_dim):
            if _shutdown_requested():
                return
            members = train_x[train_y == idx]
            center = members.mean(axis=0)
            self.centroids[idx] = center
            distances = np.mean((members - center) ** 2, axis=1)
            self.radii[idx] = max(0.012, float(np.quantile(distances, 0.985)) * 2.2)
            set_progress(93.5 + 0.5 * (idx + 1) / output_dim, "正在完成本机数字视觉模型", f"正在整理类别统计 {idx + 1}/{output_dim}", phase="正在准备本地 AI")

    def _load_self_samples(self):
        _assert_storage_path(app_dir)
        self.self_features = []
        self.self_labels = []
        self.self_sample_weights = []
        self.self_sample_sources = []
        self.canary_features = []
        self.canary_labels = []
        self.self_sample_seen = [0 for _ in self.LABELS]
        primary_failure = None
        for candidate in (self.self_sample_path, self.self_sample_backup_path):
            _assert_storage_path(candidate, allow_missing=True)
            if not candidate.exists():
                continue
            try:
                _assert_storage_path(candidate, allow_missing=False)
                with np.load(candidate, allow_pickle=False) as data:
                    features = np.asarray(data["features"], dtype=np.float32)
                    labels = np.asarray(data["labels"], dtype=np.int32)
                    if "sources" in data.files:
                        sources = np.asarray(data["sources"]).astype(str)
                    else:
                        sources = np.full((len(features),), "legacy_unverified", dtype="<U24")
                    if "weights" in data.files:
                        weights = np.asarray(data["weights"], dtype=np.float32)
                    else:
                        weights = np.full((len(features),), 0.35, dtype=np.float32)
                    seen = np.asarray(data["seen"], dtype=np.int64) if "seen" in data.files else None
                    canary_semantic_only = bool(
                        "canary_semantic_only" in data.files
                        and np.asarray(data["canary_semantic_only"], dtype=np.uint8).shape == (1,)
                        and int(np.asarray(data["canary_semantic_only"], dtype=np.uint8)[0]) == 1
                    )
                    canary_features = np.asarray(data["canary_features"], dtype=np.float32) if "canary_features" in data.files and canary_semantic_only else np.empty((0, self.INPUT_SHAPE[0] * self.INPUT_SHAPE[1]), dtype=np.float32)
                    canary_labels = np.asarray(data["canary_labels"], dtype=np.int32) if "canary_labels" in data.files and canary_semantic_only else np.empty((0,), dtype=np.int32)
                expected_dim = self.INPUT_SHAPE[0] * self.INPUT_SHAPE[1]
                if (features.ndim != 2 or features.shape[1] != expected_dim or labels.shape != (len(features),)
                        or weights.shape != (len(features),) or sources.shape != (len(features),)):
                    raise ValueError("invalid self-sample shape")
                allowed_sources = {"semantic_truth", "multiview_consensus", "legacy_unverified"}
                if (not np.all(np.isfinite(features)) or not np.all(np.isfinite(weights)) or np.any(weights <= 0.0) or np.any(weights > 1.0)
                        or np.any(labels < 0) or np.any(labels >= len(self.LABELS))
                        or any(str(value) not in allowed_sources for value in sources.tolist())):
                    raise ValueError("invalid self-sample values")
                if canary_features.ndim != 2 or canary_features.shape[1] != expected_dim or canary_labels.shape != (len(canary_features),):
                    raise ValueError("invalid OCR canary shape")
                if not np.all(np.isfinite(canary_features)) or np.any(canary_labels < 0) or np.any(canary_labels >= len(self.LABELS)):
                    raise ValueError("invalid OCR canary values")
                selected = []
                for label_index in range(len(self.LABELS)):
                    indices = np.flatnonzero(labels == label_index).tolist()
                    original_count = len(indices)
                    cap = 260 if self.LABELS[label_index].isdigit() else 187
                    if len(indices) > cap:
                        rng = random.Random(0xD1617 + label_index)
                        indices = sorted(rng.sample(indices, cap))
                    selected.extend(indices)
                    observed = int(seen[label_index]) if seen is not None and seen.shape == (len(self.LABELS),) else original_count
                    self.self_sample_seen[label_index] = max(observed, original_count)
                selected.sort()
                self.self_features = [features[i].copy() for i in selected]
                self.self_labels = [int(labels[i]) for i in selected]
                self.self_sample_weights = [float(weights[i]) for i in selected]
                self.self_sample_sources = [str(sources[i]) for i in selected]
                for label_index in range(len(self.LABELS)):
                    indices = np.flatnonzero(canary_labels == label_index).tolist()[:self.OCR_CANARY_PER_LABEL]
                    self.canary_features.extend(canary_features[i].copy() for i in indices)
                    self.canary_labels.extend(int(canary_labels[i]) for i in indices)
                if candidate == self.self_sample_backup_path:
                    tmp = app_dir / "digit_self_samples.recover.tmp.npz"
                    shutil.copy2(candidate, tmp)
                    _durable_replace(tmp, self.self_sample_path, self._self_sample_file_valid)
                    _log_runtime("warning", f"primary OCR self-samples invalid; recovered from backup; reason: {primary_failure}")
                return
            except Exception as exc:
                _log_exception(f"OCR self-sample load failed for {candidate.name}", exc)
                _quarantine_corrupt_file(candidate, exc)
                if candidate == self.self_sample_path:
                    primary_failure = exc
        if primary_failure is not None:
            _log_runtime("warning", "OCR self-samples could not be recovered from backup; starting with empty verified-sample memory")

    def _self_sample_file_valid(self, path):
        try:
            with np.load(path, allow_pickle=False) as data:
                features = np.asarray(data["features"], dtype=np.float32)
                labels = np.asarray(data["labels"], dtype=np.int32)
                weights = np.asarray(data["weights"], dtype=np.float32) if "weights" in data.files else np.full((len(features),), 0.35, dtype=np.float32)
                sources = np.asarray(data["sources"]).astype(str) if "sources" in data.files else np.full((len(features),), "legacy_unverified", dtype="<U24")
                seen = np.asarray(data["seen"], dtype=np.int64)
                canary_semantic_only = bool(
                    "canary_semantic_only" in data.files
                    and np.asarray(data["canary_semantic_only"], dtype=np.uint8).shape == (1,)
                    and int(np.asarray(data["canary_semantic_only"], dtype=np.uint8)[0]) == 1
                )
                canary_features = np.asarray(data["canary_features"], dtype=np.float32) if "canary_features" in data.files and canary_semantic_only else np.empty((0, self.INPUT_SHAPE[0] * self.INPUT_SHAPE[1]), dtype=np.float32)
                canary_labels = np.asarray(data["canary_labels"], dtype=np.int32) if "canary_labels" in data.files and canary_semantic_only else np.empty((0,), dtype=np.int32)
            expected_dim = self.INPUT_SHAPE[0] * self.INPUT_SHAPE[1]
            if features.ndim != 2 or features.shape[1] != expected_dim:
                return False
            if (labels.shape != (len(features),) or weights.shape != (len(features),)
                    or sources.shape != (len(features),) or seen.shape != (len(self.LABELS),)):
                return False
            if canary_features.ndim != 2 or canary_features.shape[1] != expected_dim or canary_labels.shape != (len(canary_features),):
                return False
            allowed_sources = {"semantic_truth", "multiview_consensus", "legacy_unverified"}
            if (np.any(labels < 0) or np.any(labels >= len(self.LABELS)) or np.any(canary_labels < 0) or np.any(canary_labels >= len(self.LABELS))
                    or np.any(weights <= 0.0) or np.any(weights > 1.0)
                    or any(str(value) not in allowed_sources for value in sources.tolist())):
                return False
            return bool(np.all(np.isfinite(features)) and np.all(np.isfinite(weights)) and np.all(np.isfinite(canary_features)))
        except Exception:
            return False

    def _save_self_samples(self):
        _assert_storage_path(app_dir)
        with self.self_sample_lock:
            if not self.self_features and not self.canary_features:
                return
            tmp = app_dir / "digit_self_samples.tmp.npz"
            expected_dim = self.INPUT_SHAPE[0] * self.INPUT_SHAPE[1]
            np.savez_compressed(
                tmp,
                features=np.asarray(self.self_features, dtype=np.float32).reshape((-1, expected_dim)),
                labels=np.asarray(self.self_labels, dtype=np.int32),
                weights=np.asarray(self.self_sample_weights, dtype=np.float32),
                sources=np.asarray(self.self_sample_sources, dtype="<U24"),
                seen=np.asarray(self.self_sample_seen, dtype=np.int64),
                canary_features=np.asarray(self.canary_features, dtype=np.float32).reshape((-1, expected_dim)),
                canary_labels=np.asarray(self.canary_labels, dtype=np.int32),
                canary_semantic_only=np.asarray([1], dtype=np.uint8),
            )
            if self.self_sample_path.exists():
                backup_tmp = app_dir / "digit_self_samples.bak.tmp.npz"
                shutil.copy2(self.self_sample_path, backup_tmp)
                _durable_replace(backup_tmp, self.self_sample_backup_path, self._self_sample_file_valid)
            _durable_replace(tmp, self.self_sample_path, self._self_sample_file_valid)
            if not self.self_sample_backup_path.exists():
                backup_tmp = app_dir / "digit_self_samples.bak.tmp.npz"
                shutil.copy2(self.self_sample_path, backup_tmp)
                _durable_replace(backup_tmp, self.self_sample_backup_path, self._self_sample_file_valid)

    def _reservoir_add_self_sample(self, feature, label_index, weight=1.0, source="multiview_consensus"):
        label_index = int(label_index)
        weight = float(_clamp(float(weight), 0.05, 1.0))
        source = str(source) if str(source) in {"semantic_truth", "multiview_consensus", "legacy_unverified"} else "legacy_unverified"
        cap = 260 if self.LABELS[label_index].isdigit() else 187
        self.self_sample_seen[label_index] += 1
        indices = [i for i, value in enumerate(self.self_labels) if int(value) == label_index]
        if len(indices) < cap:
            self.self_features.append(feature)
            self.self_labels.append(label_index)
            self.self_sample_weights.append(weight)
            self.self_sample_sources.append(source)
            return
        slot = random.randrange(self.self_sample_seen[label_index])
        if slot < cap:
            replace_at = indices[slot]
            self.self_features[replace_at] = feature
            self.self_labels[replace_at] = label_index
            self.self_sample_weights[replace_at] = weight
            self.self_sample_sources[replace_at] = source

    def _make_guard_validation_set(self):
        if self.guard_valid_x is not None and self.guard_valid_y is not None:
            return self.guard_valid_x, self.guard_valid_y
        rng = random.Random(0x51A7D19)
        fonts = self._font_paths()
        holdout_fonts = fonts[::5] or fonts[-1:]
        features, labels = [], []
        for label in self.LABELS:
            for _ in range(7):
                mask = self._safe_font_sample(label, holdout_fonts, rng)
                if mask is None:
                    mask = self._safe_font_sample(label, fonts, rng)
                if mask is None:
                    continue
                feat = self._normalize_mask(self._ood_augment_mask(mask, rng))
                if feat.sum() >= 2.0:
                    features.append(feat)
                    labels.append(self.label_to_index[label])
            if label in "0123456789+-.,":
                for _ in range(3):
                    feat = self._normalize_mask(self._ood_augment_mask(self._seven_segment_sample(label, rng), rng))
                    if feat.sum() >= 2.0:
                        features.append(feat)
                        labels.append(self.label_to_index[label])
        self.guard_valid_x = np.asarray(features, dtype=np.float32)
        self.guard_valid_y = np.asarray(labels, dtype=np.int32)
        return self.guard_valid_x, self.guard_valid_y

    def _guard_accuracy(self, x, y):
        if x is None or y is None or len(x) == 0:
            return 1.0
        correct = 0
        total = 0
        for start in range(0, len(x), 256):
            xb = np.asarray(x[start:start + 256], dtype=np.float32)
            yb = np.asarray(y[start:start + 256], dtype=np.int32)
            _, probs = self._forward(xb)
            order = np.argsort(probs, axis=1)[:, ::-1]
            best = order[:, 0]
            second = order[:, 1]
            rows = np.arange(len(xb))
            best_prob = probs[rows, best]
            margin = best_prob - probs[rows, second]
            centers = self.centroids[best]
            distance = np.mean((xb - centers) ** 2, axis=1)
            radii = self.radii[best]
            min_prob = np.asarray([0.32 if self.LABELS[int(i)] in "+-.,()" else 0.35 for i in best], dtype=np.float32)
            accepted = (best_prob >= min_prob) & (margin >= 0.06) & (distance <= radii)
            correct += int(np.sum(accepted & (best == yb)))
            total += len(xb)
        return correct / float(max(1, total))

    def _real_validation_split(self, features, labels, weights):
        weights = np.asarray(weights, dtype=np.float32)
        if len(features) < 8:
            empty_x = np.empty((0, self.INPUT_SHAPE[0] * self.INPUT_SHAPE[1]), dtype=np.float32)
            empty_y = np.empty((0,), dtype=np.int32)
            return features, labels, weights, empty_x, empty_y
        validation_mask = []
        for feature, label in zip(features, labels):
            digest = hashlib.blake2b(np.ascontiguousarray(feature).tobytes() + int(label).to_bytes(2, "little"), digest_size=1).digest()[0]
            validation_mask.append((digest % 5) == 0)
        validation_mask = np.asarray(validation_mask, dtype=bool)
        if not np.any(validation_mask):
            validation_mask[0] = True
        if np.all(validation_mask):
            validation_mask[-1] = False
        return features[~validation_mask], labels[~validation_mask], weights[~validation_mask], features[validation_mask], labels[validation_mask]

    def _fine_tune_self_samples(self, force=False, cancel_event=None):
        def cancelled():
            return _shutdown_requested() or (cancel_event is not None and cancel_event.is_set())

        if not self.self_features or cancelled():
            return
        now = time.monotonic()
        if not force and (self.new_self_samples < 48 or now - self.last_self_tune < 120.0):
            return
        with self.self_sample_lock:
            real_x = np.asarray(self.self_features, dtype=np.float32)
            real_y = np.asarray(self.self_labels, dtype=np.int32)
            real_w = np.asarray(self.self_sample_weights, dtype=np.float32)
            canary_x = np.asarray(self.canary_features, dtype=np.float32)
            canary_y = np.asarray(self.canary_labels, dtype=np.int32)
            if len(real_x) > 2048:
                sample_rng = np.random.default_rng(int(now * 1000) & 0xFFFFFFFF)
                selected = sample_rng.choice(len(real_x), size=2048, replace=False)
                real_x = real_x[selected]
                real_y = real_y[selected]
                real_w = real_w[selected]
        train_x, train_y, train_w, real_valid_x, real_valid_y = self._real_validation_split(real_x, real_y, real_w)
        if len(train_x) == 0 or cancelled():
            return
        synthetic_valid_x, synthetic_valid_y = self._make_guard_validation_set()
        if cancelled():
            return

        snapshot = tuple(array.copy() for array in (self.w1, self.b1, self.w2, self.b2, self.centroids, self.radii))
        synth_before = self._guard_accuracy(synthetic_valid_x, synthetic_valid_y)
        real_before = self._guard_accuracy(real_valid_x, real_valid_y) if len(real_valid_x) else 1.0
        canary_before = self._guard_accuracy(canary_x, canary_y) if len(canary_x) else 1.0
        total_valid = len(synthetic_valid_x) + len(real_valid_x)
        overall_before = (synth_before * len(synthetic_valid_x) + real_before * len(real_valid_x)) / float(max(1, total_valid))

        replay_x = np.repeat(self.centroids, 4, axis=0)
        replay_y = np.repeat(np.arange(len(self.LABELS), dtype=np.int32), 4)
        replay_w = np.ones((len(replay_x),), dtype=np.float32)
        x = np.concatenate((train_x[-1024:], replay_x), axis=0)
        y = np.concatenate((train_y[-1024:], replay_y), axis=0)
        weights = np.concatenate((train_w[-1024:], replay_w), axis=0)
        tune_seed = int(now * 1000) & 0xFFFFFFFF
        gpu_tuned = False
        if cp is not None and not self.gpu_disabled and not cancelled():
            try:
                rng = np.random.default_rng(tune_seed)
                xg = cp.asarray(x, dtype=cp.float32)
                yg = cp.asarray(y, dtype=cp.int32)
                wg = cp.asarray(weights, dtype=cp.float32)
                params = [cp.asarray(self.w1), cp.asarray(self.b1), cp.asarray(self.w2), cp.asarray(self.b2)]
                gpu_cancelled = False
                for _ in range(3):
                    orderg = cp.asarray(rng.permutation(len(x)), dtype=cp.int32)
                    for offset in range(0, len(x), 96):
                        if cancelled():
                            gpu_cancelled = True
                            break
                        idxg = orderg[offset:offset + 96]
                        gradients = self._gpu_gradients_from_arrays(xg[idxg], yg[idxg], *params, 0.00005, sample_weights=wg[idxg])
                        for param, gradient in zip(params, gradients):
                            param -= cp.float32(0.0008) * gradient
                    if gpu_cancelled:
                        break
                if gpu_cancelled:
                    return
                updated = [cp.asnumpy(param).astype(np.float32, copy=False) for param in params]
                self.w1, self.b1, self.w2, self.b2 = updated
                gpu_tuned = True
            except Exception as exc:
                self._disable_gpu_backend("OCR fine-tuning", exc)
        if not gpu_tuned:
            rng = np.random.default_rng(tune_seed)
            cpu_cancelled = False
            for _ in range(3):
                order = rng.permutation(len(x))
                for offset in range(0, len(order), 96):
                    if cancelled():
                        cpu_cancelled = True
                        break
                    idx = order[offset:offset + 96]
                    gradients = self._mlp_gradients(x[idx], y[idx], 0.00005, sample_weights=weights[idx])
                    self.w1 -= 0.0008 * gradients[0]
                    self.b1 -= 0.0008 * gradients[1]
                    self.w2 -= 0.0008 * gradients[2]
                    self.b2 -= 0.0008 * gradients[3]
                if cpu_cancelled:
                    break
            if cpu_cancelled:
                self.w1[:], self.b1[:], self.w2[:], self.b2[:], self.centroids[:], self.radii[:] = snapshot
                self._invalidate_gpu_weights()
                return
        self._invalidate_gpu_weights()

        for idx in range(len(self.LABELS)):
            if cancelled():
                self.w1[:], self.b1[:], self.w2[:], self.b2[:], self.centroids[:], self.radii[:] = snapshot
                self._invalidate_gpu_weights()
                return
            member_mask = train_y == idx
            members = train_x[member_mask]
            member_weights = train_w[member_mask]
            if len(members) < 2:
                continue
            weight_sum = max(1e-6, float(member_weights.sum()))
            mean = np.sum(members * member_weights[:, None], axis=0) / weight_sum
            self.centroids[idx] = self.centroids[idx] * 0.85 + mean * 0.15
            distances = np.mean((members - self.centroids[idx]) ** 2, axis=1)
            self.radii[idx] = max(float(self.radii[idx]), float(np.quantile(distances, 0.985)) * 1.6, 0.012)

        if cancelled():
            self.w1[:], self.b1[:], self.w2[:], self.b2[:], self.centroids[:], self.radii[:] = snapshot
            self._invalidate_gpu_weights()
            return
        synth_after = self._guard_accuracy(synthetic_valid_x, synthetic_valid_y)
        real_after = self._guard_accuracy(real_valid_x, real_valid_y) if len(real_valid_x) else 1.0
        canary_after = self._guard_accuracy(canary_x, canary_y) if len(canary_x) else 1.0
        overall_after = (synth_after * len(synthetic_valid_x) + real_after * len(real_valid_x)) / float(max(1, total_valid))
        canary_ok = (not len(canary_x)) or canary_after + 0.01 + 1e-12 >= canary_before
        accept = (overall_after + 1e-12 >= overall_before and (not len(real_valid_x) or real_after + 1e-12 >= real_before) and canary_ok)
        if not accept:
            self.w1[:], self.b1[:], self.w2[:], self.b2[:], self.centroids[:], self.radii[:] = snapshot
            self._invalidate_gpu_weights()
            _log_runtime("warning", f"OCR self-tune rolled back: overall {overall_before:.4f}->{overall_after:.4f}, real {real_before:.4f}->{real_after:.4f}, canary {canary_before:.4f}->{canary_after:.4f}")
        else:
            self._save_model(backup_current=True)
            _log_runtime("info", f"OCR self-tune accepted: overall {overall_before:.4f}->{overall_after:.4f}, real {real_before:.4f}->{real_after:.4f}, canary {canary_before:.4f}->{canary_after:.4f}")
        self.new_self_samples = 0
        self.last_self_tune = now

    def verified_variant_consensus(self, image, origin, observation, expected_text):
        if observation is None:
            return False
        expected = str(expected_text)
        try:
            x0, y0, x1, y1 = observation["box"]
        except Exception:
            return False
        h = max(4, int(y1 - y0))
        pad = max(3, int(round(h * 0.45)))
        ix0 = max(0, int(x0 - origin[0] - pad)); iy0 = max(0, int(y0 - origin[1] - pad))
        ix1 = min(image.width, int(x1 - origin[0] + pad)); iy1 = min(image.height, int(y1 - origin[1] + pad))
        if ix1 - ix0 < 4 or iy1 - iy0 < 4:
            return False
        crop = image.crop((ix0, iy0, ix1, iy1))
        crop_origin = (origin[0] + ix0, origin[1] + iy0)
        for family in ("adaptive", "otsu"):
            found = self.detect(crop, crop_origin, fast=True, mask_family=family)
            if not any(
                str(item.get("text", "")) == expected
                and float(item.get("conf", 0.0)) >= 0.78
                and self._iou(item.get("box", (0, 0, 0, 0)), observation.get("box", (0, 0, 0, 0))) >= 0.38
                for item in found
            ):
                return False
        return True

    def observe_verified_number(self, image, origin, observation, expected_text, source="multiview_consensus", cancel_event=None):
        if (cancel_event is not None and cancel_event.is_set()) or observation is None or float(observation.get("conf", 0.0)) < 0.86:
            return
        chars = observation.get("chars")
        text = str(observation.get("text", ""))
        expected = str(expected_text)
        if not isinstance(chars, list) or len(chars) != len(text) or text != expected or len(chars) != len(expected):
            return
        gray = np.asarray(image.convert("L"), dtype=np.uint8)
        additions = []
        for item, label in zip(chars, expected):
            if cancel_event is not None and cancel_event.is_set():
                return
            if label not in self.label_to_index or str(item.get("char", "")) != label or float(item.get("conf", 0.0)) < 0.82:
                return
            x0, y0, x1, y1 = item["box"]
            ix0 = max(0, int(x0 - origin[0])); iy0 = max(0, int(y0 - origin[1]))
            ix1 = min(gray.shape[1], int(x1 - origin[0])); iy1 = min(gray.shape[0], int(y1 - origin[1]))
            if ix1 - ix0 < 2 or iy1 - iy0 < 2:
                return
            crop = gray[iy0:iy1, ix0:ix1]
            _, light = cv2.threshold(crop, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
            candidates = []
            for mask in (light, 255 - light):
                result = self._classify_mask(mask)
                if result is not None and result[0] == label and float(result[1]) >= 0.80:
                    candidates.append((float(result[1]), self._normalize_mask(mask)))
            if not candidates:
                return
            additions.append(max(candidates, key=lambda pair: pair[0])[1])
        if cancel_event is not None and cancel_event.is_set():
            return
        strong_truth = str(source) == "semantic_truth"
        training_weight = 1.0 if strong_truth else 0.35
        with self.self_sample_lock:
            for feature, label in zip(additions, expected):
                label_index = self.label_to_index[label]
                self._reservoir_add_self_sample(feature, label_index, weight=training_weight, source=source)
                if strong_truth and sum(1 for existing in self.canary_labels if int(existing) == label_index) < self.OCR_CANARY_PER_LABEL:
                    self.canary_features.append(feature.copy())
                    self.canary_labels.append(label_index)
            self.new_self_samples += len(additions)
        self._save_self_samples()
        self._fine_tune_self_samples(cancel_event=cancel_event)

    def _model_file_valid(self, path):
        try:
            with np.load(path, allow_pickle=False) as data:
                version = str(data["version"][0])
                labels = tuple(str(v) for v in data["labels"].tolist())
                w1 = np.asarray(data["w1"], dtype=np.float32)
                b1 = np.asarray(data["b1"], dtype=np.float32)
                w2 = np.asarray(data["w2"], dtype=np.float32)
                b2 = np.asarray(data["b2"], dtype=np.float32)
                centroids = np.asarray(data["centroids"], dtype=np.float32)
                radii = np.asarray(data["radii"], dtype=np.float32)
            if version != self.MODEL_VERSION or labels != self.LABELS:
                return False
            if w1.shape != (self.INPUT_SHAPE[0] * self.INPUT_SHAPE[1], self.HIDDEN):
                return False
            if w2.shape != (self.HIDDEN, len(self.LABELS)) or centroids.shape != (len(self.LABELS), w1.shape[0]):
                return False
            if b1.shape != (self.HIDDEN,) or b2.shape != (len(self.LABELS),) or radii.shape != (len(self.LABELS),):
                return False
            return all(np.all(np.isfinite(array)) for array in (w1, b1, w2, b2, centroids, radii))
        except Exception:
            return False

    def _save_model(self, backup_current=False):
        _assert_storage_path(app_dir)
        tmp = app_dir / "digit_model.tmp.npz"
        np.savez_compressed(
            tmp, version=np.asarray([self.MODEL_VERSION]), labels=np.asarray(self.LABELS),
            w1=self.w1, b1=self.b1, w2=self.w2, b2=self.b2,
            centroids=self.centroids, radii=self.radii
        )
        if backup_current and self.model_path.exists():
            backup_tmp = app_dir / "digit_model.bak.tmp.npz"
            shutil.copy2(self.model_path, backup_tmp)
            _durable_replace(backup_tmp, self.model_backup_path, self._model_file_valid)
        _durable_replace(tmp, self.model_path, self._model_file_valid)
        if not self.model_backup_path.exists():
            backup_tmp = app_dir / "digit_model.bak.tmp.npz"
            shutil.copy2(self.model_path, backup_tmp)
            _durable_replace(backup_tmp, self.model_backup_path, self._model_file_valid)

    def _load_model_file(self, path):
        with np.load(path, allow_pickle=False) as data:
            version = str(data["version"][0])
            labels = tuple(str(v) for v in data["labels"].tolist())
            if version != self.MODEL_VERSION or labels != self.LABELS:
                return False
            w1 = np.asarray(data["w1"], dtype=np.float32)
            b1 = np.asarray(data["b1"], dtype=np.float32)
            w2 = np.asarray(data["w2"], dtype=np.float32)
            b2 = np.asarray(data["b2"], dtype=np.float32)
            centroids = np.asarray(data["centroids"], dtype=np.float32)
            radii = np.asarray(data["radii"], dtype=np.float32)
        if w1.shape != (self.INPUT_SHAPE[0] * self.INPUT_SHAPE[1], self.HIDDEN):
            return False
        if w2.shape != (self.HIDDEN, len(self.LABELS)) or centroids.shape != (len(self.LABELS), w1.shape[0]):
            return False
        if b1.shape != (self.HIDDEN,) or b2.shape != (len(self.LABELS),) or radii.shape != (len(self.LABELS),):
            return False
        if not all(np.all(np.isfinite(array)) for array in (w1, b1, w2, b2, centroids, radii)):
            return False
        self.w1, self.b1, self.w2, self.b2 = w1, b1, w2, b2
        self.centroids, self.radii = centroids, radii
        self._invalidate_gpu_weights()
        return True

    def _load_model(self):
        _assert_storage_path(app_dir)
        primary_failure = None
        for index, path in enumerate((self.model_path, self.model_backup_path)):
            _assert_storage_path(path, allow_missing=True)
            if not path.exists():
                continue
            try:
                _assert_storage_path(path, allow_missing=False)
                if not self._load_model_file(path):
                    raise ValueError("OCR model semantic validation failed")
                if index == 1:
                    tmp = app_dir / "digit_model.recover.tmp.npz"
                    shutil.copy2(path, tmp)
                    _durable_replace(tmp, self.model_path, self._model_file_valid)
                    _log_runtime("warning", f"primary OCR model was invalid; recovered digit_model.npz from backup; reason: {primary_failure}")
                return True
            except Exception as exc:
                _log_exception(f"OCR model load failed for {path.name}", exc)
                _quarantine_corrupt_file(path, exc)
                if index == 0:
                    primary_failure = exc
        return False

    def _classify_masks(self, crops):
        results = [None] * len(crops)
        features = []
        slots = []
        for slot, crop in enumerate(crops):
            feat = self._normalize_mask(crop)
            if feat.sum() < 2.0:
                continue
            features.append(feat)
            slots.append(slot)
        if not features:
            return results
        feature_batch = np.asarray(features, dtype=np.float32)
        _, probs = self._forward(feature_batch)
        for row_index, slot in enumerate(slots):
            row = probs[row_index]
            order = np.argsort(row)[::-1]
            best_idx = int(order[0])
            second_idx = int(order[1])
            best_prob = float(row[best_idx])
            margin = best_prob - float(row[second_idx])
            feat = feature_batch[row_index]
            distance = float(np.mean((feat - self.centroids[best_idx]) ** 2))
            label = self.LABELS[best_idx]
            min_prob = 0.32 if label in "+-.,()" else 0.35
            if best_prob < min_prob or margin < 0.06 or distance > float(self.radii[best_idx]):
                continue
            distance_score = max(0.0, 1.0 - distance / max(float(self.radii[best_idx]), 1e-6))
            results[slot] = (label, max(0.0, min(1.0, best_prob * 0.72 + distance_score * 0.28)))
        return results

    def _classify_mask(self, crop):
        return self._classify_masks([crop])[0]

    def _parse_number_candidates(self, text):
        raw_text = str(text).strip()
        parenthesized_negative = False
        wrapped = re.fullmatch(r"\(\s*(.*?)\s*\)", raw_text)
        if wrapped:
            parenthesized_negative = True
            raw_text = wrapped.group(1).strip()
        # Spaces, NBSP and narrow NBSP are common visual grouping separators.
        # They do not need their own OCR class: when they occur between digits,
        # normalize them away before separator disambiguation.
        raw_text = re.sub(r"(?<=\d)[ \u00A0\u202F]+(?=\d)", "", raw_text)
        match = re.fullmatch(r"([+-]?)([0-9]+(?:[.,][0-9]*)*|[.,][0-9]+)(?:([eE])([+-]?\d+))?", raw_text)
        if not match:
            return []
        sign_text, mantissa, exponent_mark, exponent_text = match.groups()
        if parenthesized_negative and sign_text:
            return []
        if not mantissa or not any(ch.isdigit() for ch in mantissa):
            return []
        exponent = int(exponent_text) if exponent_mark else 0
        if abs(exponent) > 10000:
            return []

        def add_value(values, normalized):
            try:
                with localcontext() as ctx:
                    ctx.prec = max(64, len(normalized) + abs(exponent) + 8)
                    value = Decimal(normalized)
                    if sign_text == "-" or parenthesized_negative:
                        value = -value
                    if exponent:
                        value = value.scaleb(exponent)
            except (InvalidOperation, ValueError, OverflowError):
                return
            if value.is_finite() and not any(_same_number(value, existing) for existing in values):
                values.append(value)

        values = []
        dots = mantissa.count(".")
        commas = mantissa.count(",")
        if dots and commas:
            decimal_sep = "." if mantissa.rfind(".") > mantissa.rfind(",") else ","
            grouping_sep = "," if decimal_sep == "." else "."
            compact = mantissa.replace(grouping_sep, "")
            if compact.count(decimal_sep) == 1:
                add_value(values, compact.replace(decimal_sep, "."))
        elif dots or commas:
            sep = "." if dots else ","
            parts = mantissa.split(sep)
            grouping_valid = len(parts) >= 2 and parts[0].isdigit() and all(part.isdigit() and len(part) == 3 for part in parts[1:])
            decimal_valid = len(parts) == 2 and all(part.isdigit() or part == "" for part in parts)
            prefer_grouping = sep == self.locale_thousands and sep != self.locale_decimal
            prefer_decimal = sep == self.locale_decimal
            interpretations = []
            if grouping_valid and prefer_grouping:
                interpretations.append("group")
            if decimal_valid and prefer_decimal:
                interpretations.append("decimal")
            if grouping_valid and "group" not in interpretations:
                interpretations.append("group")
            if decimal_valid and "decimal" not in interpretations:
                interpretations.append("decimal")
            for interpretation in interpretations:
                if interpretation == "group":
                    add_value(values, mantissa.replace(sep, ""))
                else:
                    normalized = mantissa.replace(sep, ".")
                    if normalized.startswith("."):
                        normalized = "0" + normalized
                    if normalized.endswith("."):
                        normalized += "0"
                    add_value(values, normalized)
        else:
            add_value(values, mantissa)
        return values

    def _parse_number_text(self, text, reference=None):
        candidates = self._parse_number_candidates(text)
        if not candidates:
            return None
        if reference is not None:
            try:
                ref = _as_decimal(reference)
                scale = max(Decimal(1), abs(ref))
                return min(candidates, key=lambda value: abs(value - ref) / scale)
            except (InvalidOperation, TypeError, ValueError):
                pass
        return candidates[0]


    def _best_numeric_span(self, selected):
        best = None
        for i in range(len(selected)):
            for j in range(i + 1, len(selected) + 1):
                span = selected[i:j]
                text = "".join(char["char"] for char in span)
                candidates = self._parse_number_candidates(text)
                if not candidates:
                    continue
                digit_count = sum(char["char"].isdigit() for char in span)
                if digit_count == 0:
                    continue
                mean_conf = sum(float(char["conf"]) for char in span) / len(span)
                exponent_bonus = 0.4 if "e" in text.lower() else 0.0
                score = digit_count * 2.0 + len(span) * 0.35 + mean_conf + exponent_bonus
                if best is None or score > best[0]:
                    best = (score, span, candidates[0], text, candidates)
        return best

    def _candidate_masks(self, gray, fast=False, family=None):
        h_img, w_img = gray.shape
        block = 31 if min(h_img, w_img) >= 31 else max(3, min(h_img, w_img) | 1)
        adaptive_inv = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, block, 9)
        _, otsu_inv = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
        adaptive = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, block, 9)
        _, otsu = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        if family == "adaptive":
            return (adaptive_inv, adaptive)
        if family == "otsu":
            return (otsu_inv, otsu)
        if fast:
            return (adaptive_inv, otsu_inv)
        kernel_edge = max(3, int(round(math.sqrt(max(9, min(h_img, w_img))) / 4.0)) | 1)
        close_kernel = np.ones((kernel_edge, kernel_edge), dtype=np.uint8)
        return (
            adaptive_inv, adaptive, otsu_inv, otsu,
            cv2.morphologyEx(adaptive_inv, cv2.MORPH_CLOSE, close_kernel, iterations=1),
            cv2.morphologyEx(adaptive, cv2.MORPH_CLOSE, close_kernel, iterations=1),
        )

    def _char_overlap_fraction(self, a, b):
        x0 = max(a[0], b[0])
        y0 = max(a[1], b[1])
        x1 = min(a[2], b[2])
        y1 = min(a[3], b[3])
        inter = max(0, x1 - x0) * max(0, y1 - y0)
        area_a = max(1, (a[2] - a[0]) * (a[3] - a[1]))
        area_b = max(1, (b[2] - b[0]) * (b[3] - b[1]))
        return inter / float(min(area_a, area_b))

    def _add_char(self, chars, item):
        new_box = item["box"]
        new_area = max(1, (new_box[2] - new_box[0]) * (new_box[3] - new_box[1]))
        for old in chars:
            old_box = old["box"]
            overlap = self._char_overlap_fraction(new_box, old_box)
            if overlap < 0.82:
                continue
            old_area = max(1, (old_box[2] - old_box[0]) * (old_box[3] - old_box[1]))
            if new_area > old_area * 1.22 and float(item["conf"]) >= float(old["conf"]) - 0.12:
                old.update(item)
            elif old_area <= new_area * 1.22 and float(item["conf"]) > float(old["conf"]):
                old.update(item)
            return
        chars.append(item)

    def _repair_punctuation(self, chars):
        for item in chars:
            box = item["box"]
            h = max(1, box[3] - box[1])
            w = max(1, box[2] - box[0])
            if w / float(h) > 1.65 or item.get("char") in "+-":
                continue
            neighbors = []
            cx = (box[0] + box[2]) / 2.0
            for other in chars:
                if other is item:
                    continue
                ob = other["box"]
                oh = max(1, ob[3] - ob[1])
                ocx = (ob[0] + ob[2]) / 2.0
                if oh >= h * 1.8 and abs(ocx - cx) <= oh * 5.5 and abs(ob[3] - box[3]) <= oh * 0.38:
                    neighbors.append(oh)
            if not neighbors:
                continue
            reference = sorted(neighbors)[len(neighbors) // 2]
            if h <= reference * 0.42 and w <= reference * 0.42:
                item["char"] = "," if h > w * 1.45 else "."
                item["conf"] = max(float(item.get("conf", 0.0)), 0.86)

    def _mser_chars(self, gray, stop_event=None, deadline=None):
        h_img, w_img = gray.shape
        detector = cv2.MSER_create()
        detector.setMinArea(3)
        detector.setMaxArea(max(64, int(h_img * w_img * 0.025)))
        _, boxes = detector.detectRegions(gray)
        seen = set()
        chars = []
        records = []
        crops = []
        for index, raw in enumerate(boxes):
            if index % max(8, int(math.sqrt(len(boxes) + 1))) == 0 and _scan_cancelled(stop_event, deadline):
                break
            x, y, w, h = (int(raw[0]), int(raw[1]), int(raw[2]), int(raw[3]))
            key = (x, y, w, h)
            if key in seen:
                continue
            seen.add(key)
            if h < 2 or h > min(640, h_img * 0.70) or w < 1 or w > min(520, w_img * 0.45):
                continue
            aspect = w / float(max(h, 1))
            if aspect < 0.035 or aspect > 8.0:
                continue
            pad = max(1, int(round(max(h, w) * 0.05)))
            x0, y0 = max(0, x - pad), max(0, y - pad)
            x1, y1 = min(w_img, x + w + pad), min(h_img, y + h + pad)
            crop = gray[y0:y1, x0:x1]
            _, light = cv2.threshold(crop, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
            dark = 255 - light
            records.append((x, y, w, h))
            crops.extend((light, dark))
        classified = self._classify_masks(crops)
        for record_index, (x, y, w, h) in enumerate(records):
            choices = [candidate for candidate in classified[record_index * 2:record_index * 2 + 2] if candidate is not None]
            if not choices:
                continue
            label, conf = max(choices, key=lambda candidate: candidate[1])
            if label in ".," and h > max(20, int(w * 3.0)):
                continue
            self._add_char(chars, {"char": label, "conf": conf, "box": (x, y, x + w, y + h)})
        return chars

    def detect(self, pil_image, origin, stop_event=None, deadline=None, fast=False, mask_family=None):
        if _scan_cancelled(stop_event, deadline):
            return []
        rgb = np.asarray(pil_image.convert("RGB"))
        gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
        h_img, w_img = gray.shape
        chars = []
        masks = self._candidate_masks(gray, fast=fast, family=mask_family)
        for mask_index, mask in enumerate(masks):
            if _scan_cancelled(stop_event, deadline):
                break
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            check_stride = max(8, int(math.sqrt(len(contours) + 1)))
            records = []
            crops = []
            for contour_index, contour in enumerate(contours):
                if contour_index % check_stride == 0 and _scan_cancelled(stop_event, deadline):
                    break
                x, y, w, h = cv2.boundingRect(contour)
                if h < 2 or h > min(640, h_img * 0.70) or w < 1 or w > min(520, w_img * 0.45):
                    continue
                aspect = w / float(max(h, 1))
                if aspect < 0.035 or aspect > 8.0:
                    continue
                area = cv2.contourArea(contour)
                fill_ratio = area / float(max(1, w * h))
                if area < 3 or fill_ratio < 0.018 or (fill_ratio > 0.94 and w * h > 600):
                    continue
                pad = max(1, int(round(max(h, w) * 0.07)))
                x0, y0 = max(0, x - pad), max(0, y - pad)
                x1, y1 = min(w_img, x + w + pad), min(h_img, y + h + pad)
                records.append((x, y, w, h))
                crops.append(mask[y0:y1, x0:x1])
            classified = self._classify_masks(crops)
            for (x, y, w, h), result in zip(records, classified):
                if result is None:
                    continue
                label, conf = result
                if label in ".," and h > max(20, int(w * 3.0)):
                    continue
                self._add_char(chars, {"char": label, "conf": conf, "box": (x, y, x + w, y + h)})
        if not fast and not _scan_cancelled(stop_event, deadline):
            for item in self._mser_chars(gray, stop_event=stop_event, deadline=deadline):
                self._add_char(chars, item)
        self._repair_punctuation(chars)
        chars.sort(key=lambda char: (char["box"][1], char["box"][0]))
        groups = []
        used = set()
        for i, char in enumerate(chars):
            if _scan_cancelled(stop_event, deadline):
                break
            if i in used:
                continue
            line = [i]
            box = char["box"]
            cy = (box[1] + box[3]) / 2.0
            hh = max(1, box[3] - box[1])
            for j in range(i + 1, len(chars)):
                if j in used:
                    continue
                other = chars[j]["box"]
                hj = max(1, other[3] - other[1])
                cyj = (other[1] + other[3]) / 2.0
                center_close = abs(cyj - cy) <= 0.55 * max(hh, hj)
                baseline_close = abs(other[3] - box[3]) <= 0.42 * max(hh, hj)
                punctuation = char["char"] in "+-.,()" or chars[j]["char"] in "+-.,()"
                ratio_ok = 0.38 <= hj / max(hh, 1) <= 2.7
                if (center_close and (ratio_ok or punctuation)) or (punctuation and baseline_close):
                    line.append(j)
            line.sort(key=lambda idx: chars[idx]["box"][0])
            seq = [line[0]]
            for line_pos, idx in enumerate(line[1:], start=1):
                prev_idx = seq[-1]
                prev = chars[prev_idx]["box"]
                curr = chars[idx]["box"]
                gap = curr[0] - prev[2]
                typical_h = max(1, prev[3] - prev[1], curr[3] - curr[1])
                join = gap <= typical_h * 0.85
                if not join and gap <= typical_h * 1.35 and chars[prev_idx]["char"].isdigit() and chars[idx]["char"].isdigit():
                    # Infer a visual thousands separator only when the next
                    # group contains a compact three-digit block.
                    tail = line[line_pos:line_pos + 3]
                    if len(tail) == 3 and all(chars[t]["char"].isdigit() for t in tail):
                        compact = True
                        for a, b in zip(tail, tail[1:]):
                            ab = chars[a]["box"]; bb = chars[b]["box"]
                            local_h = max(1, ab[3] - ab[1], bb[3] - bb[1])
                            if bb[0] - ab[2] > local_h * 0.85:
                                compact = False
                                break
                        join = compact
                if join:
                    seq.append(idx)
            selected = [chars[idx] for idx in seq]
            best = self._best_numeric_span(selected)
            if best is not None:
                _, span, value, text, candidates = best
                gx0 = min(item["box"][0] for item in span)
                gy0 = min(item["box"][1] for item in span)
                gx1 = max(item["box"][2] for item in span)
                gy1 = max(item["box"][3] for item in span)
                confidence = sum(float(item["conf"]) for item in span) / len(span)
                groups.append({
                    "value": value, "value_candidates": candidates, "text": text, "raw_text": text,
                    "display_quantum": str(abs(_decimal_quantum(value))),
                    "box": (gx0 + origin[0], gy0 + origin[1], gx1 + origin[0], gy1 + origin[1]),
                    "chars": [dict(item, box=(item["box"][0] + origin[0], item["box"][1] + origin[1],
                                                   item["box"][2] + origin[0], item["box"][3] + origin[1])) for item in span],
                    "conf": confidence,
                })
                for idx in seq:
                    used.add(idx)
        return self._dedupe_groups(groups)

    def _dedupe_groups(self, groups):
        groups.sort(key=lambda group: (group["conf"], len(group["text"])), reverse=True)
        kept = []
        for group in groups:
            duplicate = False
            for old in kept:
                if self._iou(group["box"], old["box"]) > 0.60:
                    duplicate = True
                    break
            if not duplicate:
                kept.append(group)
        return kept

    def _iou(self, a, b):
        x0 = max(a[0], b[0])
        y0 = max(a[1], b[1])
        x1 = min(a[2], b[2])
        y1 = min(a[3], b[3])
        inter = max(0, x1 - x0) * max(0, y1 - y0)
        area_a = max(1, (a[2] - a[0]) * (a[3] - a[1]))
        area_b = max(1, (b[2] - b[0]) * (b[3] - b[1]))
        return inter / float(area_a + area_b - inter)


def _stable_window_title(title):
    text = str(title or "").strip()
    if not text:
        return ""
    parts = re.split(r"\s+[—–-]\s+", text)
    if len(parts) > 1:
        tail = parts[-1].strip()
        if 1 <= len(tail) <= 48:
            text = tail
    text = re.sub(r"[A-Za-z]:\\[^|<>]*", "<path>", text)
    text = re.sub(r"\b[0-9a-fA-F]{8,}\b", "#", text)
    text = re.sub(r"\d+", "#", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:48]


class LearningController:
    STATE_VERSION = 11
    ACTION_SUCCESS = "success"
    ACTION_NOT_APPLICABLE = "not_applicable"
    ACTION_FAILED = "failed"
    CONTROL_READY = "READY"
    CONTROL_SCANNING = "SCANNING"
    CONTROL_SELECTING = "SELECTING"
    CONTROL_ARMING = "ARMING"
    CONTROL_CONTROLLING = "CONTROLLING"
    CONTROL_STOPPING = "STOPPING"
    MAX_STORED_POLICY_BYTES = 98304
    MAX_OPS = 128
    MAX_KEY_BATCH = 8
    MAX_WAIT_SECONDS = 2.0
    MAX_MOVE_SECONDS = 2.0
    MAX_TEXT_UNITS = 128
    MAX_TEXT_INTERVAL = 0.25
    MAX_WHEEL_DELTA = 1200
    VALID_OPS = ("mouse_abs", "mouse_rel", "mouse_button", "wheel", "key_event", "unicode_text", "replace_number", "wait")
    IDLE_VALID_OPS = ("mouse_abs", "mouse_rel", "mouse_button", "wheel", "key_event", "wait")
    IDLE_INITIAL_VKS = (0x25, 0x26, 0x27, 0x28)
    IDLE_SAFE_VKS = IDLE_INITIAL_VKS

    def __init__(self):
        self.state_path = app_dir / "learning.json"
        self.state_backup_path = app_dir / "learning.bak"
        self.state_recovered_from_backup = False
        self.state_recovery_reason = None
        self._limit_cache = None
        self._limit_cache_until = 0.0
        self.state_io_lock = threading.Lock()
        self.state_dirty = False
        self.last_state_save = time.monotonic()
        self.state_save_interval = float(hardware_profile["save_interval"])
        self._loading_legacy_gain = False
        self.state = self._load_state()
        self._compact_state()
        self.running = False
        self.mode = None
        self.control_state = self.CONTROL_READY
        self.stop_event = threading.Event()
        self.user_interrupt_event = threading.Event()
        self.hook_callback_error_event = threading.Event()
        self.hook_quit_posted = threading.Event()
        self.release_requested = threading.Event()
        self.release_ui_requested = threading.Event()
        self.overlay_mode = False
        self.arming = False
        self.ignore_selection_lbutton_up = False
        self.selection_release_seen_at = 0.0
        self.selection_release_source = None
        self.user_interrupt_pending = False
        self.target = None
        self.original_target = None
        self.current_value = None
        self.target_identity = None
        self.overlays = []
        self.overlay_targets = []
        self.overlay_canvas = None
        self.overlay_items = []
        self.hook_thread_id = 0
        self.input_hooks_ready = threading.Event()
        self.mouse_hook = None
        self.keyboard_hook = None
        self.mouse_proc = None
        self.keyboard_proc = None
        self.raw_input_hwnd = None
        self.raw_input_class_name = None
        self.raw_input_wndproc = None
        self.raw_input_registered = False
        self.raw_input_timer_id = 0
        self.hook_mouse_probe_sent_at = 0.0
        self.hook_mouse_probe_ack_at = 0.0
        self.held_keys = set()
        self.held_mouse = set()
        self.physical_keys_down = set()
        self.physical_buttons_down = set()
        self.system_stop_reason = None
        self.lock = threading.Lock()
        self.physical_state_lock = threading.Lock()
        self.input_gate_lock = threading.RLock()
        self.input_enabled = False
        self.agent_thread = None
        recent_window = max(8, int(hardware_profile["recent_window"]))
        self.idle_recent_states = deque(maxlen=recent_window)
        self.idle_recent_actions = deque(maxlen=recent_window)
        self.idle_recent_windows = deque(maxlen=recent_window)
        self.idle_no_novelty_streak = 0
        self.uia_semantic_cache = {}
        self.uia_fallback_last = {}
        self.last_replace_attempt = None

    def _transition_control(self, expected, new_state, *, enable_input=False, running=None, arming=None, ignore_selection_lbutton_up=None):
        if isinstance(expected, str):
            expected_states = {expected}
        else:
            expected_states = {str(state) for state in expected}
        allowed = {
            self.CONTROL_READY: {self.CONTROL_READY, self.CONTROL_SCANNING, self.CONTROL_CONTROLLING, self.CONTROL_STOPPING},
            self.CONTROL_SCANNING: {self.CONTROL_SCANNING, self.CONTROL_SELECTING, self.CONTROL_READY, self.CONTROL_STOPPING},
            self.CONTROL_SELECTING: {self.CONTROL_SELECTING, self.CONTROL_ARMING, self.CONTROL_READY, self.CONTROL_STOPPING},
            self.CONTROL_ARMING: {self.CONTROL_ARMING, self.CONTROL_CONTROLLING, self.CONTROL_READY, self.CONTROL_STOPPING},
            self.CONTROL_CONTROLLING: {self.CONTROL_CONTROLLING, self.CONTROL_STOPPING},
            self.CONTROL_STOPPING: {self.CONTROL_STOPPING, self.CONTROL_READY},
        }
        with self.input_gate_lock:
            old_state = self.control_state
            if old_state not in expected_states:
                self.input_enabled = False
                if old_state != self.CONTROL_READY:
                    self.stop_event.set()
                _log_runtime("warning", f"rejected control transition {old_state} -> {new_state}; expected {sorted(expected_states)}")
                return False
            if new_state not in allowed.get(old_state, set()):
                self.input_enabled = False
                self.stop_event.set()
                self.control_state = self.CONTROL_STOPPING
                _log_runtime("error", f"illegal control transition {old_state} -> {new_state}; forced STOPPING")
                return False
            self.input_enabled = False
            if running is not None:
                self.running = bool(running)
            if arming is not None:
                self.arming = bool(arming)
            if ignore_selection_lbutton_up is not None:
                previous_ignore = bool(self.ignore_selection_lbutton_up)
                self.ignore_selection_lbutton_up = bool(ignore_selection_lbutton_up)
                if self.ignore_selection_lbutton_up or previous_ignore:
                    self.selection_release_seen_at = 0.0
                    self.selection_release_source = None
            self.control_state = new_state
            if enable_input:
                if new_state != self.CONTROL_CONTROLLING or self.stop_event.is_set() or self.user_interrupt_event.is_set():
                    self.stop_event.set()
                    self.control_state = self.CONTROL_STOPPING
                    _log_runtime("warning", f"refused input enable while entering {new_state}; forced STOPPING")
                    return False
                self.input_enabled = True
        if old_state != new_state:
            _log_runtime("info", f"control transition {old_state} -> {new_state}; input_enabled={int(bool(enable_input))}")
        return True

    def _fresh_state(self):
        return {
            "version": self.STATE_VERSION, "trials": 0, "successes": 0, "unknowns": 0, "best_gain": 0.0,
            "contexts": {}, "success_memory": [], "elite_policies": {},
            "idle_trials": 0, "idle_contexts": {}, "idle_memory": []
        }

    def _storage_limits(self):
        now = time.monotonic()
        if self._limit_cache is not None and now < self._limit_cache_until:
            return self._limit_cache
        try:
            usage = shutil.disk_usage(app_dir)
            total = max(1, int(usage.total))
            free = max(0, int(usage.free))
        except Exception:
            total = max(1, int(hardware_profile["disk_total"]))
            free = max(0, int(hardware_profile["disk_free"]))
        ram_total = max(1, int(hardware_profile["ram_total"]))
        free_ratio = free / float(total)
        reserve = max(int(total * 0.01), int(ram_total * 0.02))
        spendable = max(0, free - reserve)
        soft_budget = min(int(total * 0.00025), int(spendable * 0.0035), int(ram_total * 0.002))
        floor_budget = max(2 << 20, int(min(ram_total, total) * 0.00003))
        ceiling_budget = max(floor_budget, min(64 << 20, int(ram_total * 0.004), max(floor_budget, int(free * 0.01))))
        byte_budget = int(_clamp(max(floor_budget, soft_budget), floor_budget, ceiling_budget))
        scale = math.sqrt(byte_budget / float(max(1, 8 << 20)))
        capacity = max(1.0, float(hardware_profile["capacity"]))
        programs = int(_clamp(round(150 * scale * (0.8 + capacity * 0.08)), 96, 1024))
        contexts = int(_clamp(round(math.sqrt(programs) * 6.0), 36, 192))
        elites = int(_clamp(round(contexts * 0.9), 32, contexts))
        memory = int(_clamp(round(programs * 2.0), 192, 2048))
        history = int(_clamp(round(math.log2(programs + 1.0) * 2.2), 10, 40))
        self.state_save_interval = _clamp(30.0 + (1.0 - free_ratio) * 30.0, 30.0, 60.0)
        limits = {"programs": programs, "contexts": contexts, "elites": elites, "memory": memory, "history": history, "bytes": byte_budget}
        self._limit_cache = limits
        self._limit_cache_until = now + _clamp(self.state_save_interval / 2.0, 15.0, 30.0)
        return limits

    def _collapse_replace_scaffolding(self, program):
        def vk(op, code, down):
            return (op.get("op") == "key_event" and op.get("mode") == "vk"
                    and int(op.get("code", 0)) == code and bool(op.get("down", True)) is down)

        out = list(program)
        index = 0
        while index < len(out):
            if out[index].get("op") != "replace_number":
                index += 1
                continue
            start = index
            if index >= 4 and (vk(out[index - 4], 0x11, True) and vk(out[index - 3], 0x41, True)
                               and vk(out[index - 2], 0x41, False) and vk(out[index - 1], 0x11, False)):
                start = index - 4
                if start >= 2 and (out[start - 2].get("op") == "mouse_button"
                                   and out[start - 2].get("button") == "left" and bool(out[start - 2].get("down"))
                                   and out[start - 1].get("op") == "mouse_button"
                                   and out[start - 1].get("button") == "left" and not bool(out[start - 1].get("down"))):
                    start -= 2
                    if start >= 1 and out[start - 1].get("op") == "mouse_abs":
                        start -= 1
            end = index + 1
            if end + 1 < len(out) and vk(out[end], 0x0D, True) and vk(out[end + 1], 0x0D, False):
                end += 2
            if start != index or end != index + 1:
                replacement = out[index]
                out[start:end] = [replacement]
                index = start + 1
            else:
                index += 1
        return out

    def _normalize_program(self, program, space="target"):
        if not isinstance(program, list) or space not in ("target", "screen"):
            return []
        if len(program) > self.MAX_OPS:
            return []
        out = []
        held_mouse = set()
        held_keys = set()
        for source in program:
            if not isinstance(source, dict):
                return []
            kind = source.get("op")
            if kind not in self.VALID_OPS:
                return []
            if held_keys and kind != "key_event":
                return []
            op = {"op": kind}
            try:
                if kind == "mouse_abs":
                    if space == "target":
                        rx, ry = float(source["rx"]), float(source["ry"])
                        if not (math.isfinite(rx) and math.isfinite(ry)):
                            return []
                        op.update(rx=rx, ry=ry)
                    else:
                        sx, sy = float(source["sx"]), float(source["sy"])
                        if not (math.isfinite(sx) and math.isfinite(sy)):
                            return []
                        op.update(sx=_clamp(sx, 0.0, 1.0), sy=_clamp(sy, 0.0, 1.0))
                    duration = max(0.0, float(source.get("duration", 0.0)))
                    if not math.isfinite(duration):
                        return []
                    op["duration"] = min(duration, self.MAX_MOVE_SECONDS)
                elif kind == "mouse_rel":
                    if space == "target":
                        rdx, rdy = float(source["rdx"]), float(source["rdy"])
                        if not (math.isfinite(rdx) and math.isfinite(rdy)):
                            return []
                        op.update(rdx=rdx, rdy=rdy)
                    else:
                        sdx, sdy = float(source["sdx"]), float(source["sdy"])
                        if not (math.isfinite(sdx) and math.isfinite(sdy)):
                            return []
                        op.update(sdx=sdx, sdy=sdy)
                    duration = max(0.0, float(source.get("duration", 0.0)))
                    if not math.isfinite(duration):
                        return []
                    op["duration"] = min(duration, self.MAX_MOVE_SECONDS)
                    op["no_coalesce"] = bool(source.get("no_coalesce", False))
                elif kind == "mouse_button":
                    button = str(source.get("button", "left"))
                    if button not in ("left", "right", "middle", "x1", "x2"):
                        return []
                    down = bool(source.get("down", True))
                    if down:
                        if button in held_mouse:
                            return []
                        held_mouse.add(button)
                    else:
                        if button not in held_mouse:
                            return []
                        held_mouse.remove(button)
                    op.update(button=button, down=down)
                elif kind == "wheel":
                    delta = int(source.get("delta", 0))
                    if delta == 0:
                        return []
                    op.update(delta=int(_clamp(delta, -self.MAX_WHEEL_DELTA, self.MAX_WHEEL_DELTA)), horizontal=bool(source.get("horizontal", False)))
                elif kind == "key_event":
                    mode = str(source.get("mode", "vk"))
                    if mode not in ("vk", "scan"):
                        return []
                    code = int(source.get("code", 0)) & 0xFFFF
                    if code == 0:
                        return []
                    extended = bool(source.get("extended", False))
                    down = bool(source.get("down", True))
                    identity = (mode, code, extended)
                    if down:
                        if identity in held_keys:
                            return []
                        held_keys.add(identity)
                    else:
                        if identity not in held_keys:
                            return []
                        held_keys.remove(identity)
                    op.update(mode=mode, code=code, down=down, extended=extended)
                elif kind == "unicode_text":
                    text = str(source.get("text", ""))
                    if not text or len(text.encode("utf-16-le")) // 2 > self.MAX_TEXT_UNITS:
                        return []
                    interval = max(0.0, float(source.get("interval", 0.0)))
                    if not math.isfinite(interval):
                        return []
                    op.update(text=text, interval=min(interval, self.MAX_TEXT_INTERVAL))
                elif kind == "replace_number":
                    delta = abs(_as_decimal(source.get("delta", "1")))
                    if delta <= 0:
                        return []
                    op["delta"] = str(delta.normalize())
                elif kind == "wait":
                    seconds = max(0.0, float(source.get("seconds", 0.0)))
                    if not math.isfinite(seconds):
                        return []
                    op["seconds"] = min(seconds, self.MAX_WAIT_SECONDS)
            except (KeyError, TypeError, ValueError, OverflowError, InvalidOperation):
                return []
            out.append(op)
        if held_mouse or held_keys:
            return []
        out = self._collapse_replace_scaffolding(out)
        if len(out) > self.MAX_OPS:
            return []
        try:
            if len(json.dumps(out, ensure_ascii=False, separators=(",", ":")).encode("utf-8")) > self.MAX_STORED_POLICY_BYTES:
                return []
        except Exception:
            return []
        return out

    def _normalize_idle_program(self, program):
        normalized = self._normalize_program(program, space="screen")
        out = []
        for op in normalized:
            kind = op.get("op")
            if kind not in self.IDLE_VALID_OPS:
                return []
            if kind == "key_event":
                if op.get("mode") != "vk" or int(op.get("code", 0)) not in self.IDLE_SAFE_VKS:
                    return []
                op["extended"] = False
            out.append(op)
        return out

    def _state_int_field(self, source, key, default=0, minimum=0, maximum=None):
        value = source.get(key, default)
        if isinstance(value, bool) or not isinstance(value, int):
            raise ValueError(f"{key} must be an integer")
        value = int(value)
        if minimum is not None and value < int(minimum):
            raise ValueError(f"{key} is below its minimum")
        if maximum is not None and value > int(maximum):
            raise ValueError(f"{key} exceeds its maximum")
        return value

    def _state_float_field(self, source, key, default=0.0, minimum=None, maximum=None):
        value = source.get(key, default)
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f"{key} must be numeric")
        value = float(value)
        if not math.isfinite(value):
            raise ValueError(f"{key} must be finite")
        if minimum is not None and value < float(minimum):
            raise ValueError(f"{key} is below its minimum")
        if maximum is not None and value > float(maximum):
            raise ValueError(f"{key} exceeds its maximum")
        return value

    def _state_text_field(self, source, key, default="", require_nonempty=False):
        value = source.get(key, default)
        if not isinstance(value, str):
            raise ValueError(f"{key} must be a string")
        if require_nonempty and not value:
            raise ValueError(f"{key} must not be empty")
        return value

    def _load_idle_record(self, source):
        if not isinstance(source, dict):
            return None
        program = self._normalize_idle_program(source.get("program"))
        fingerprint = self._state_text_field(source, "fingerprint", require_nonempty=True)
        if not program:
            return None
        return {
            "fingerprint": fingerprint, "program": program, "n": self._state_int_field(source, "n"),
            "q": self._state_float_field(source, "q"), "reward_sum": self._state_float_field(source, "reward_sum"),
            "best_reward": self._state_float_field(source, "best_reward", -1e9),
            "last_seen": self._state_int_field(source, "last_seen"),
        }

    def _validate_state_finite(self, value, path="state"):
        if isinstance(value, float):
            if not math.isfinite(value):
                raise ValueError(f"{path} contains non-finite number")
            return
        if isinstance(value, dict):
            for key, item in value.items():
                self._validate_state_finite(item, f"{path}.{key}")
        elif isinstance(value, list):
            for index, item in enumerate(value):
                self._validate_state_finite(item, f"{path}[{index}]")

    def _load_policy_canary(self, source):
        if source is None:
            return None
        if not isinstance(source, dict):
            raise ValueError("context canary must be an object")
        result = {
            "success_floor": self._state_float_field(source, "success_floor", 0.0, 0.0, 1.0),
            "gain_floor": self._state_float_field(source, "gain_floor", 0.0, 0.0),
            "reward_floor": self._state_float_field(source, "reward_floor", -1e9),
            "established_trial": self._state_int_field(source, "established_trial"),
        }
        self._validate_state_finite(result, "context.canary")
        return result

    def _parse_state(self, data, source_name):
        if not isinstance(data, dict):
            raise ValueError(f"{source_name} root is not an object")
        fresh = self._fresh_state()
        stored_version = self._state_int_field(data, "version", -1, minimum=-1)
        if stored_version not in (5, 6, 7, 8, 10, self.STATE_VERSION):
            raise ValueError(f"unsupported learning state version: {stored_version}")
        self._loading_legacy_gain = stored_version < 8
        try:
            fresh["trials"] = self._state_int_field(data, "trials")
            fresh["successes"] = self._state_int_field(data, "successes")
            fresh["unknowns"] = self._state_int_field(data, "unknowns")
            fresh["best_gain"] = self._state_float_field(data, "best_gain", 0.0, 0.0)

            contexts = data.get("contexts", {})
            if not isinstance(contexts, dict):
                raise ValueError("contexts must be an object")
            for key, source_ctx in contexts.items():
                if not isinstance(source_ctx, dict):
                    raise ValueError(f"context {key!r} is not an object")
                ctx = {
                    "programs": [], "best_policy": None, "challenger": None, "canary": None,
                    "champion_history": [], "trials": self._state_int_field(source_ctx, "trials"),
                    "last_used": self._state_int_field(source_ctx, "last_used"),
                    "unknowns": self._state_int_field(source_ctx, "unknowns"),
                    "stagnation": self._state_int_field(source_ctx, "stagnation") if stored_version >= 8 else 0,
                    "replace_not_applicable": self._state_int_field(source_ctx, "replace_not_applicable"),
                    "pending_confirmations": {},
                }
                source_programs = source_ctx.get("programs", [])
                if not isinstance(source_programs, list):
                    raise ValueError(f"context {key!r}.programs must be a list")
                for record_index, source_rec in enumerate(source_programs):
                    rec = self._load_record(source_rec)
                    if rec is None:
                        raise ValueError(f"context {key!r}.programs[{record_index}] is invalid")
                    ctx["programs"].append(rec)
                raw_best = source_ctx.get("best_policy")
                best = self._load_policy(raw_best)
                if raw_best is not None and best is None:
                    raise ValueError(f"context {key!r}.best_policy is invalid")
                ctx["best_policy"] = best
                raw_challenger = source_ctx.get("challenger")
                challenger = self._load_challenger(raw_challenger)
                if raw_challenger is not None and challenger is None:
                    raise ValueError(f"context {key!r}.challenger is invalid")
                ctx["challenger"] = challenger
                ctx["canary"] = self._load_policy_canary(source_ctx.get("canary"))
                history = source_ctx.get("champion_history", [])
                if not isinstance(history, list):
                    raise ValueError(f"context {key!r}.champion_history must be a list")
                for history_index, item in enumerate(history):
                    loaded = self._load_policy(item)
                    if loaded is None:
                        raise ValueError(f"context {key!r}.champion_history[{history_index}] is invalid")
                    ctx["champion_history"].append(loaded)
                pending = source_ctx.get("pending_confirmations", {})
                if not isinstance(pending, dict):
                    raise ValueError(f"context {key!r}.pending_confirmations must be an object")
                for pending_key, count in pending.items():
                    if not isinstance(pending_key, str):
                        raise ValueError(f"context {key!r}.pending_confirmations key is not a string")
                    if isinstance(count, bool) or not isinstance(count, int) or not (0 <= count <= 8):
                        raise ValueError(f"context {key!r}.pending_confirmations[{pending_key!r}] is invalid")
                    ctx["pending_confirmations"][pending_key] = int(count)
                fresh["contexts"][str(key)] = ctx

            elites = data.get("elite_policies", {})
            if not isinstance(elites, dict):
                raise ValueError("elite_policies must be an object")
            for key, source_policy in elites.items():
                loaded = self._load_policy(source_policy)
                if loaded is None:
                    raise ValueError(f"elite policy {key!r} is invalid")
                fresh["elite_policies"][str(key)] = loaded
            for key, ctx in fresh["contexts"].items():
                best = ctx.get("best_policy")
                if isinstance(best, dict) and key not in fresh["elite_policies"]:
                    fresh["elite_policies"][key] = json.loads(json.dumps(best))

            memory = data.get("success_memory", [])
            if not isinstance(memory, list):
                raise ValueError("success_memory must be a list")
            for item_index, source_item in enumerate(memory):
                if not isinstance(source_item, dict):
                    raise ValueError(f"success_memory[{item_index}] is not an object")
                program = self._normalize_program(source_item.get("program"), space="target")
                fingerprint = self._state_text_field(source_item, "fingerprint", require_nonempty=True)
                if not program:
                    raise ValueError(f"success_memory[{item_index}] has invalid program")
                fresh["success_memory"].append({
                    "window": self._state_text_field(source_item, "window"), "fingerprint": fingerprint, "program": program,
                    "n": self._state_int_field(source_item, "n", 1, minimum=1),
                    "reward_sum": self._state_float_field(source_item, "reward_sum"),
                    "gain_sum": 0.0 if self._loading_legacy_gain else self._state_float_field(source_item, "gain_sum", 0.0, 0.0),
                    "best_reward": self._state_float_field(source_item, "best_reward"),
                    "best_gain": 0.0 if self._loading_legacy_gain else self._state_float_field(source_item, "best_gain", 0.0, 0.0),
                    "last_seen": self._state_int_field(source_item, "last_seen"),
                })

            fresh["idle_trials"] = self._state_int_field(data, "idle_trials")
            idle_contexts = data.get("idle_contexts", {})
            if not isinstance(idle_contexts, dict):
                raise ValueError("idle_contexts must be an object")
            for key, source_ctx in idle_contexts.items():
                if not isinstance(source_ctx, dict):
                    raise ValueError(f"idle context {key!r} is not an object")
                ctx = {"programs": [], "trials": self._state_int_field(source_ctx, "trials"), "last_used": self._state_int_field(source_ctx, "last_used")}
                programs = source_ctx.get("programs", [])
                if not isinstance(programs, list):
                    raise ValueError(f"idle context {key!r}.programs must be a list")
                for record_index, source_rec in enumerate(programs):
                    rec = self._load_idle_record(source_rec)
                    if rec is None:
                        raise ValueError(f"idle context {key!r}.programs[{record_index}] is invalid")
                    ctx["programs"].append(rec)
                fresh["idle_contexts"][str(key)] = ctx

            idle_memory = data.get("idle_memory", [])
            if not isinstance(idle_memory, list):
                raise ValueError("idle_memory must be a list")
            for item_index, source_item in enumerate(idle_memory):
                if not isinstance(source_item, dict):
                    raise ValueError(f"idle_memory[{item_index}] is not an object")
                program = self._normalize_idle_program(source_item.get("program"))
                fingerprint = self._state_text_field(source_item, "fingerprint", require_nonempty=True)
                if not program:
                    raise ValueError(f"idle_memory[{item_index}] has invalid program")
                fresh["idle_memory"].append({
                    "context": self._state_text_field(source_item, "context"), "fingerprint": fingerprint, "program": program,
                    "n": self._state_int_field(source_item, "n", 1, minimum=1),
                    "reward_sum": self._state_float_field(source_item, "reward_sum"),
                    "best_reward": self._state_float_field(source_item, "best_reward"),
                    "last_seen": self._state_int_field(source_item, "last_seen"),
                })
            self._validate_state_finite(fresh)
            return fresh
        finally:
            self._loading_legacy_gain = False

    def _load_state(self):
        failures = []
        found_any = False

        def reject_constant(value):
            raise ValueError(f"non-finite JSON constant: {value}")

        for candidate_path in (self.state_path, self.state_backup_path):
            _assert_storage_path(candidate_path, allow_missing=True)
            if not candidate_path.exists():
                continue
            found_any = True
            try:
                _assert_storage_path(candidate_path, allow_missing=False)
                raw = candidate_path.read_text(encoding="utf-8")
                data = json.loads(raw, parse_constant=reject_constant)
                parsed = self._parse_state(data, candidate_path.name)
                if candidate_path == self.state_backup_path:
                    self.state_recovered_from_backup = True
                    reason = failures[-1][1] if failures else "primary learning state unavailable"
                    self.state_recovery_reason = str(reason)
                    self.state_dirty = True
                    _log_runtime("warning", f"learning state restored from learning.bak after primary failure: {reason}")
                return parsed
            except Exception as exc:
                self._loading_legacy_gain = False
                failures.append((candidate_path.name, exc))
                _log_exception(f"learning state full parse/validation failed for {candidate_path.name}", exc)
                _quarantine_corrupt_file(candidate_path, exc)
        if failures:
            reason_text = "; ".join(f"{name}: {exc}" for name, exc in failures)
            self.state_recovery_reason = reason_text
            _log_runtime("error", f"no valid learning state remained after primary/backup validation; using fresh state: {reason_text}")
        elif found_any:
            _log_runtime("warning", "learning state files existed but could not be read; using fresh state")
        return self._fresh_state()

    def _load_record(self, source):
        if not isinstance(source, dict):
            return None
        program = self._normalize_program(source.get("program"), space="target")
        fingerprint = self._state_text_field(source, "fingerprint", require_nonempty=True)
        if not program:
            return None
        n = self._state_int_field(source, "n")
        wins = self._state_int_field(source, "wins")
        if wins > n:
            return None
        legacy = bool(self._loading_legacy_gain)
        return {
            "fingerprint": fingerprint, "program": program, "n": n, "wins": wins,
            "q": self._state_float_field(source, "q"),
            "best_gain": 0.0 if legacy else self._state_float_field(source, "best_gain", 0.0, 0.0),
            "best_reward": self._state_float_field(source, "best_reward"),
            "total_reward": self._state_float_field(source, "total_reward"),
            "total_gain": 0.0 if legacy else self._state_float_field(source, "total_gain", 0.0, 0.0),
            "last_seen": self._state_int_field(source, "last_seen"),
            "blocked_until": self._state_int_field(source, "blocked_until"),
        }

    def _load_eval(self, source):
        if source is None:
            source = {}
        if not isinstance(source, dict):
            raise ValueError("policy evaluation must be an object")
        n = self._state_int_field(source, "n")
        wins = self._state_int_field(source, "wins")
        if wins > n:
            raise ValueError("policy evaluation wins exceed trials")
        return {
            "n": n, "wins": wins,
            "reward_sum": self._state_float_field(source, "reward_sum"),
            "gain_sum": 0.0 if self._loading_legacy_gain else self._state_float_field(source, "gain_sum", 0.0, 0.0),
        }

    def _load_policy(self, source):
        if not isinstance(source, dict):
            return None
        program = self._normalize_program(source.get("program"), space="target")
        fingerprint = self._state_text_field(source, "fingerprint", require_nonempty=True)
        evidence_source = source.get("evidence")
        if not program or (evidence_source is not None and not isinstance(evidence_source, dict)):
            return None
        return {
            "fingerprint": fingerprint, "program": program,
            "accepted_trial": self._state_int_field(source, "accepted_trial"),
            "success_floor": self._state_float_field(source, "success_floor", 0.0, 0.0, 1.0),
            "gain_floor": 0.0 if self._loading_legacy_gain else self._state_float_field(source, "gain_floor", 0.0, 0.0),
            "reward_floor": self._state_float_field(source, "reward_floor", -1e9),
            "evidence": self._load_eval(evidence_source),
        }

    def _load_challenger(self, source):
        if not isinstance(source, dict):
            return None
        program = self._normalize_program(source.get("program"), space="target")
        fingerprint = self._state_text_field(source, "fingerprint", require_nonempty=True)
        candidate_eval = source.get("candidate_eval")
        incumbent_eval = source.get("incumbent_eval")
        if (not program or
                (candidate_eval is not None and not isinstance(candidate_eval, dict)) or
                (incumbent_eval is not None and not isinstance(incumbent_eval, dict))):
            return None
        return {
            "fingerprint": fingerprint, "program": program, "started_trial": self._state_int_field(source, "started_trial"),
            "candidate_eval": self._load_eval(candidate_eval),
            "incumbent_eval": self._load_eval(incumbent_eval),
        }

    def _mark_state_dirty(self, urgent=False):
        self.state_dirty = True
        if urgent:
            self._save_state(force=True)


    def _maybe_save_state(self):
        if self.state_dirty and time.monotonic() - self.last_state_save >= self.state_save_interval:
            self._save_state(force=False)


    def _learning_state_file_valid(self, path):
        try:
            def reject_constant(value):
                raise ValueError(f"non-finite JSON constant: {value}")

            raw = Path(path).read_text(encoding="utf-8")
            data = json.loads(raw, parse_constant=reject_constant)
            parsed = self._parse_state(data, Path(path).name)
            return isinstance(parsed, dict) and int(parsed.get("version", -1)) == self.STATE_VERSION
        except Exception:
            self._loading_legacy_gain = False
            return False

    def _save_state(self, force=True):
        _assert_storage_path(app_dir)
        if not force and not self.state_dirty:
            return
        with self.state_io_lock:
            if not force and not self.state_dirty:
                return
            self.state["version"] = self.STATE_VERSION
            self._sync_elite_policies()
            self._compact_state()
            limits = self._storage_limits()
            payload = self._fit_state_payload(limits["bytes"])
            encoded_size = len(payload.encode("utf-8"))
            if encoded_size > limits["bytes"]:
                raise RuntimeError(f"学习状态超过硬上限：{encoded_size}>{limits['bytes']}")
            tmp = app_dir / "learning.tmp"
            backup_tmp = app_dir / "learning.bak.tmp"
            with open(tmp, "w", encoding="utf-8", newline="") as handle:
                handle.write(payload)
            if self.state_path.exists() and not self.state_recovered_from_backup:
                try:
                    old_payload = self.state_path.read_bytes()
                    with open(backup_tmp, "wb") as handle:
                        handle.write(old_payload)
                    _durable_replace(backup_tmp, self.state_backup_path, self._learning_state_file_valid)
                finally:
                    try:
                        backup_tmp.unlink(missing_ok=True)
                    except Exception as exc:
                        _log_runtime("warning", f"learning backup temp cleanup failed: {exc}")
            _durable_replace(tmp, self.state_path, self._learning_state_file_valid)
            if self.state_recovered_from_backup:
                with open(backup_tmp, "w", encoding="utf-8", newline="") as handle:
                    handle.write(payload)
                _durable_replace(backup_tmp, self.state_backup_path, self._learning_state_file_valid)
                recovery_reason = self.state_recovery_reason
                self.state_recovered_from_backup = False
                self.state_recovery_reason = None
                _log_runtime("info", f"learning state recovery finalized and backup refreshed: {recovery_reason}")
            self.state_dirty = False
            self.last_state_save = time.monotonic()

    def _fit_state_payload(self, max_bytes):
        max_bytes = int(max_bytes)
        if max_bytes <= 0:
            raise RuntimeError("学习状态字节上限无效")

        def encode():
            return json.dumps(self.state, ensure_ascii=False, separators=(",", ":"))

        def size(payload):
            return len(payload.encode("utf-8"))

        payload = encode()
        if size(payload) <= max_bytes:
            return payload
        self._compact_state(aggressive=True)
        payload = encode()

        memory = self.state.get("success_memory", [])
        if isinstance(memory, list):
            memory.sort(key=self._memory_quality, reverse=True)
            while memory and size(payload) > max_bytes:
                memory.pop()
                payload = encode()

        idle_memory = self.state.get("idle_memory", [])
        if isinstance(idle_memory, list):
            idle_memory.sort(key=self._idle_memory_quality, reverse=True)
            while idle_memory and size(payload) > max_bytes:
                idle_memory.pop()
                payload = encode()

        idle_contexts = self.state.get("idle_contexts", {})
        while isinstance(idle_contexts, dict) and idle_contexts and size(payload) > max_bytes:
            victim = min(idle_contexts.items(), key=lambda pair: (self._idle_context_quality(pair[1]), int(pair[1].get("last_used", 0))))[0]
            del idle_contexts[victim]
            payload = encode()

        contexts = self.state.get("contexts", {})
        if isinstance(contexts, dict):
            for cap in (64, 32, 16, 8, 4, 2, 1):
                if size(payload) <= max_bytes:
                    break
                for ctx in contexts.values():
                    self._compact_context(ctx, cap, 1)
                payload = encode()
            while contexts and size(payload) > max_bytes:
                victim = min(contexts.items(), key=lambda pair: self._context_rank(pair[1]))[0]
                del contexts[victim]
                payload = encode()

        elites = self.state.get("elite_policies", {})
        while isinstance(elites, dict) and elites and size(payload) > max_bytes:
            victim = min(elites.items(), key=lambda pair: self._elite_rank(pair[0], pair[1]))[0]
            del elites[victim]
            payload = encode()

        if size(payload) > max_bytes:
            for field in ("success_memory", "idle_memory"):
                value = self.state.get(field)
                if isinstance(value, list):
                    value.clear()
            for field in ("contexts", "idle_contexts", "elite_policies"):
                value = self.state.get(field)
                if isinstance(value, dict):
                    value.clear()
            payload = encode()

        if size(payload) > max_bytes:
            preserved = {
                "version": self.STATE_VERSION,
                "trials": max(0, int(self.state.get("trials", 0))),
                "successes": max(0, int(self.state.get("successes", 0))),
                "unknowns": max(0, int(self.state.get("unknowns", 0))),
                "best_gain": float(self.state.get("best_gain", 0.0)),
                "contexts": {}, "success_memory": [], "elite_policies": {},
                "idle_trials": max(0, int(self.state.get("idle_trials", 0))),
                "idle_contexts": {}, "idle_memory": []
            }
            self.state.clear()
            self.state.update(preserved)
            payload = encode()

        if size(payload) > max_bytes:
            raise RuntimeError("学习状态最小载荷仍超过硬字节上限")
        return payload

    def _policy_fingerprint(self, program, target):
        canonical = []
        for op in program:
            kind = op.get("op")
            if kind == "mouse_abs":
                canonical.append((kind, round(float(op.get("rx", 0.0)) * 4.0) / 4.0,
                                  round(float(op.get("ry", 0.0)) * 4.0) / 4.0,
                                  self._time_bucket(op.get("duration", 0.0))))
            elif kind == "mouse_rel":
                canonical.append((kind, round(float(op.get("rdx", 0.0)) * 4.0) / 4.0,
                                  round(float(op.get("rdy", 0.0)) * 4.0) / 4.0,
                                  self._time_bucket(op.get("duration", 0.0)), bool(op.get("no_coalesce", False))))
            elif kind == "mouse_button":
                canonical.append((kind, str(op.get("button", "left")), bool(op.get("down", True))))
            elif kind == "wheel":
                canonical.append((kind, int(round(float(op.get("delta", 0)) / 120.0)), bool(op.get("horizontal", False))))
            elif kind == "key_event":
                canonical.append((kind, str(op.get("mode", "vk")), int(op.get("code", 0)) & 0xFFFF,
                                  bool(op.get("down", True)), bool(op.get("extended", False))))
            elif kind == "unicode_text":
                text = str(op.get("text", ""))
                number = recognizer._parse_number_text(text) if recognizer is not None else None
                if number is not None:
                    number = float(number)
                    text_key = ("numeric", self._magnitude_bucket(number), 1 if number >= 0 else -1)
                else:
                    text_key = ("text", hashlib.blake2b(text.encode("utf-8", "replace"), digest_size=6).hexdigest())
                canonical.append((kind, text_key, self._time_bucket(op.get("interval", 0.0))))
            elif kind == "replace_number":
                delta = max(1e-12, abs(float(op.get("delta", 1.0))))
                canonical.append((kind, self._magnitude_bucket(delta)))
            elif kind == "wait":
                canonical.append((kind, self._time_bucket(op.get("seconds", 0.0))))
        raw = json.dumps(canonical, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        return hashlib.blake2b(raw, digest_size=12).hexdigest()

    def _time_bucket(self, value):
        seconds = max(0.0, float(value))
        return int(round(math.log1p(seconds) * 12.0))

    def _magnitude_bucket(self, value):
        magnitude = abs(float(value))
        if magnitude < 1e-12:
            return 0
        return int(round(math.log10(magnitude) * 8.0))

    def _record_quality(self, rec):
        n = max(1, int(rec.get("n", 0)))
        rate = int(rec.get("wins", 0)) / n
        gain = float(rec.get("total_gain", 0.0)) / n
        reward = float(rec.get("total_reward", 0.0)) / n
        confidence = 1.0 - math.exp(-n / 8.0)
        weak_penalty = 1.0 if n >= 8 and rate < 0.05 and gain <= 0.0 and reward < -0.1 else 0.0
        return rate * 4.0 + math.log1p(max(0.0, gain)) * 0.55 + reward * 0.65 + float(rec.get("q", 0.0)) * 0.35 + confidence * 0.20 - weak_penalty

    def _memory_quality(self, item):
        n = max(1, int(item.get("n", 1)))
        return (float(item.get("gain_sum", 0.0)) / n, float(item.get("reward_sum", 0.0)) / n, math.log1p(n), int(item.get("last_seen", 0)))

    def _compact_context(self, ctx, program_cap, history_cap):
        protected = set()
        best = ctx.get("best_policy")
        challenger = ctx.get("challenger")
        if isinstance(best, dict):
            protected.add(best.get("fingerprint"))
        if isinstance(challenger, dict):
            protected.add(challenger.get("fingerprint"))
        records = list(ctx.get("programs", []))
        records.sort(
            key=lambda rec: (
                rec.get("fingerprint") in protected,
                int(rec.get("wins", 0)) > 0,
                self._record_quality(rec),
                int(rec.get("last_seen", 0)),
            ),
            reverse=True,
        )
        ctx["programs"] = records[:max(1, int(program_cap))]
        history = list(ctx.get("champion_history", []))
        ctx["champion_history"] = history[-max(1, int(history_cap)):]

    def _context_quality(self, ctx):
        best = ctx.get("best_policy")
        best_score = 0.0
        if isinstance(best, dict):
            best_score = float(best.get("success_floor", 0.0)) * 5.0 + math.log1p(float(best.get("gain_floor", 0.0)))
        return best_score + math.log1p(max(0, int(ctx.get("trials", 0)))) * 0.08

    def _context_rank(self, ctx):
        return (self._context_quality(ctx), int(ctx.get("last_used", 0)))

    def _idle_record_quality(self, rec):
        n = max(1, int(rec.get("n", 0)))
        avg_reward = float(rec.get("reward_sum", 0.0)) / n
        confidence = 1.0 - math.exp(-n / 6.0)
        return avg_reward * 0.70 + float(rec.get("q", 0.0)) * 0.30 + confidence * 0.05

    def _idle_memory_quality(self, item):
        n = max(1, int(item.get("n", 1)))
        return float(item.get("reward_sum", 0.0)) / n + math.log1p(n) * 0.02 + int(item.get("last_seen", 0)) * 1e-9

    def _compact_idle_context(self, ctx, program_cap):
        records = list(ctx.get("programs", []))
        records.sort(key=lambda rec: (self._idle_record_quality(rec), int(rec.get("last_seen", 0))), reverse=True)
        ctx["programs"] = records[:max(1, int(program_cap))]

    def _idle_context_quality(self, ctx):
        records = ctx.get("programs", [])
        best = max((self._idle_record_quality(rec) for rec in records), default=0.0)
        return best + math.log1p(max(0, int(ctx.get("trials", 0)))) * 0.05 + int(ctx.get("last_used", 0)) * 1e-9

    def _compact_state(self, aggressive=False):
        if not hasattr(self, "state"):
            return
        limits = self._storage_limits()
        program_cap = max(128, limits["programs"] // (2 if aggressive else 1))
        history_cap = max(6, limits["history"] // (2 if aggressive else 1))
        for ctx in self.state.get("contexts", {}).values():
            if isinstance(ctx, dict):
                self._compact_context(ctx, program_cap, history_cap)
        contexts = self.state.get("contexts", {})
        context_cap = max(24, limits["contexts"] // (2 if aggressive else 1))
        if isinstance(contexts, dict) and len(contexts) > context_cap:
            ranked = sorted(contexts.items(), key=lambda pair: self._context_rank(pair[1]), reverse=True)
            self.state["contexts"] = dict(ranked[:context_cap])
        elite_cap = max(24, limits["elites"] // (2 if aggressive else 1))
        self._trim_elite_policies(elite_cap)
        memory = self.state.get("success_memory", [])
        if isinstance(memory, list):
            memory.sort(key=self._memory_quality, reverse=True)
            memory_cap = max(128, limits["memory"] // (2 if aggressive else 1))
            del memory[memory_cap:]
        idle_program_cap = max(48, limits["programs"] // (4 if aggressive else 2))
        for ctx in self.state.get("idle_contexts", {}).values():
            if isinstance(ctx, dict):
                self._compact_idle_context(ctx, idle_program_cap)
        idle_contexts = self.state.get("idle_contexts", {})
        idle_context_cap = max(16, limits["contexts"] // (3 if aggressive else 2))
        if isinstance(idle_contexts, dict) and len(idle_contexts) > idle_context_cap:
            ranked = sorted(idle_contexts.items(), key=lambda pair: self._idle_context_quality(pair[1]), reverse=True)
            self.state["idle_contexts"] = dict(ranked[:idle_context_cap])
        idle_memory = self.state.get("idle_memory", [])
        if isinstance(idle_memory, list):
            idle_memory.sort(key=self._idle_memory_quality, reverse=True)
            idle_memory_cap = max(64, limits["memory"] // (4 if aggressive else 2))
            del idle_memory[idle_memory_cap:]

    def _eval_update(self, stats, reward, gain):
        stats["n"] = int(stats.get("n", 0)) + 1
        if reward > 0:
            stats["wins"] = int(stats.get("wins", 0)) + 1
        stats["reward_sum"] = float(stats.get("reward_sum", 0.0)) + float(reward)
        stats["gain_sum"] = float(stats.get("gain_sum", 0.0)) + float(gain)

    def _wilson_lower(self, wins, n, z=1.2815515655446004):
        n = max(0, int(n))
        if n == 0:
            return 0.0
        p = max(0.0, min(1.0, float(wins) / n))
        denom = 1.0 + z * z / n
        center = p + z * z / (2.0 * n)
        margin = z * math.sqrt((p * (1.0 - p) + z * z / (4.0 * n)) / n)
        return max(0.0, (center - margin) / denom)

    def _policy_from_evidence(self, program, fingerprint, evidence):
        n = max(1, int(evidence.get("n", 0)))
        wins = max(0, int(evidence.get("wins", 0)))
        avg_gain = float(evidence.get("gain_sum", 0.0)) / n
        avg_reward = float(evidence.get("reward_sum", 0.0)) / n
        return {
            "fingerprint": fingerprint, "program": json.loads(json.dumps(program)),
            "accepted_trial": int(self.state.get("trials", 0)),
            "success_floor": self._wilson_lower(wins, n),
            "gain_floor": max(0.0, avg_gain * 0.92), "reward_floor": avg_reward - 0.08,
            "evidence": dict(evidence)
        }

    def _elite_quality(self, policy):
        if not isinstance(policy, dict):
            return (-1.0, -1.0, -1e9, -1)
        return (
            float(policy.get("success_floor", 0.0)),
            float(policy.get("gain_floor", 0.0)),
            float(policy.get("reward_floor", -1e9)),
            int(policy.get("accepted_trial", 0)),
        )

    def _policy_is_not_worse(self, candidate, incumbent):
        if not isinstance(candidate, dict):
            return False
        if not isinstance(incumbent, dict):
            return True
        return (
            float(candidate.get("success_floor", 0.0)) + 1e-12 >= float(incumbent.get("success_floor", 0.0))
            and float(candidate.get("gain_floor", 0.0)) + 1e-12 >= float(incumbent.get("gain_floor", 0.0))
            and float(candidate.get("reward_floor", -1e9)) + 1e-12 >= float(incumbent.get("reward_floor", -1e9))
        )

    def _policy_is_strict_upgrade(self, candidate, incumbent):
        if not self._policy_is_not_worse(candidate, incumbent):
            return False
        if not isinstance(incumbent, dict):
            return True
        return (
            float(candidate.get("success_floor", 0.0)) > float(incumbent.get("success_floor", 0.0)) + 1e-9
            or float(candidate.get("gain_floor", 0.0)) > float(incumbent.get("gain_floor", 0.0)) + 1e-9
            or float(candidate.get("reward_floor", -1e9)) > float(incumbent.get("reward_floor", -1e9)) + 1e-9
        )

    def _elite_rank(self, key, policy):
        ctx = self.state.get("contexts", {}).get(str(key))
        if isinstance(ctx, dict):
            recent = int(ctx.get("last_used", 0))
        else:
            recent = int(policy.get("accepted_trial", 0)) if isinstance(policy, dict) else 0
        return (self._elite_quality(policy), recent)

    def _trim_elite_policies(self, cap=None):
        elites = self.state.setdefault("elite_policies", {})
        if not isinstance(elites, dict):
            self.state["elite_policies"] = {}
            return
        if cap is None:
            cap = self._storage_limits()["elites"]
        cap = max(1, int(cap))
        if len(elites) <= cap:
            return
        ranked = sorted(elites.items(), key=lambda pair: self._elite_rank(pair[0], pair[1]), reverse=True)
        self.state["elite_policies"] = dict(ranked[:cap])

    def _store_elite_policy(self, key, policy):
        if not isinstance(policy, dict):
            return
        elites = self.state.setdefault("elite_policies", {})
        current = elites.get(str(key))
        if current is None or self._policy_is_strict_upgrade(policy, current):
            elites[str(key)] = json.loads(json.dumps(policy))
        self._trim_elite_policies()

    def _sync_elite_policies(self):
        elites = self.state.setdefault("elite_policies", {})
        for key, ctx in self.state.get("contexts", {}).items():
            if not isinstance(ctx, dict):
                continue
            best = ctx.get("best_policy")
            elite = elites.get(str(key))
            if self._policy_is_strict_upgrade(elite, best):
                ctx["best_policy"] = json.loads(json.dumps(elite))
                ctx["challenger"] = None
            elif self._policy_is_strict_upgrade(best, elite):
                elites[str(key)] = json.loads(json.dumps(best))
        self._trim_elite_policies()

    def clear_user_interrupt(self):
        self.user_interrupt_event.clear()
        with self.input_gate_lock:
            self.ignore_selection_lbutton_up = False
            self.selection_release_seen_at = 0.0
            self.selection_release_source = None
        with self.lock:
            self.user_interrupt_pending = False

    def _clear_target_tracking(self):
        self.target = None
        self.original_target = None
        self.current_value = None
        self.target_identity = None
        self.last_replace_attempt = None

    def handle_runtime_error(self, exc, context="运行过程"):
        detail = str(exc).strip() or exc.__class__.__name__
        _log_runtime("error", f"{context}: {detail}")
        reason = f"{context}出错：{detail}。AI已停止。可重新选择模式。"
        self._transition_control(
            (self.CONTROL_READY, self.CONTROL_SCANNING, self.CONTROL_SELECTING, self.CONTROL_ARMING, self.CONTROL_CONTROLLING, self.CONTROL_STOPPING),
            self.CONTROL_STOPPING, enable_input=False,
        )
        self.stop_event.set()
        self.release_requested.set()
        with self.lock:
            self.user_interrupt_pending = False
            self.system_stop_reason = reason
            self.overlay_mode = False
        self._clear_target_tracking()
        self._release_all_inputs()
        if app_alive.is_set():
            post_ui("runtime_error", reason)
        return reason

    def select_target(self, target):
        chosen = dict(target)
        self.target = chosen
        self.original_target = dict(chosen)
        self.current_value = chosen["value"]
        stable_window = str(chosen.get("stable_window_signature") or chosen.get("window_signature") or "")
        initial_root_hwnd = int(chosen.get("root_hwnd", 0) or 0)
        self.target_identity = {
            "initial_box": list(chosen["box"]),
            "window": stable_window or None,
            "root_hwnd": initial_root_hwnd,
            "context": None,
            "dynamic": bool(chosen.get("dynamic", False)),
            "natural_rate": "0",
            "natural_noise_rate": "0",
            "natural_last_calibration": 0.0,
        }

    def _cursor_pos(self):
        pt = wintypes.POINT()
        user32.GetCursorPos(ctypes.byref(pt))
        return (pt.x, pt.y)

    def _window_signature(self, target):
        x0, y0, x1, y1 = target["box"]
        pt = wintypes.POINT(int((x0 + x1) / 2), int((y0 + y1) / 2))
        hwnd = user32.WindowFromPoint(pt)
        if hwnd:
            root_hwnd = user32.GetAncestor(hwnd, GA_ROOT)
            if root_hwnd:
                hwnd = root_hwnd
        if not hwnd:
            hwnd = user32.GetForegroundWindow()
        length = user32.GetWindowTextLengthW(hwnd)
        title_buf = ctypes.create_unicode_buffer(length + 1)
        user32.GetWindowTextW(hwnd, title_buf, len(title_buf))
        class_buf = ctypes.create_unicode_buffer(128)
        user32.GetClassNameW(hwnd, class_buf, len(class_buf))
        title = _stable_window_title(title_buf.value)
        cls = class_buf.value.strip()[:48]
        return f"{cls}|{title}"

    def _target_window_info(self, target):
        vx0, vy0, vx1, vy1 = self._screen_bounds()
        x0, y0, x1, y1 = target["box"]
        pt = wintypes.POINT(int((x0 + x1) / 2), int((y0 + y1) / 2))
        hwnd = user32.WindowFromPoint(pt)
        if hwnd:
            root_hwnd = user32.GetAncestor(hwnd, GA_ROOT)
            if root_hwnd:
                hwnd = root_hwnd
        rect = wintypes.RECT()
        if not hwnd or not user32.GetWindowRect(hwnd, ctypes.byref(rect)):
            rect.left, rect.top, rect.right, rect.bottom = vx0, vy0, vx1 + 1, vy1 + 1
            hwnd = None
        dpi = 96
        if hwnd:
            try:
                dpi = max(48, int(user32.GetDpiForWindow(hwnd) or 96))
            except Exception:
                dpi = 96
        return hwnd, rect, dpi

    def _visual_context_token(self):
        stored = (self.target_identity or {}).get("context")
        if stored is None:
            return "v0"
        try:
            arr = np.asarray(stored, dtype=np.float32).reshape(24, 30)
            small = cv2.resize(arr, (8, 6), interpolation=cv2.INTER_AREA)
            median = float(np.median(small))
            bits = 0
            for value in small.reshape(-1):
                bits = (bits << 1) | int(float(value) >= median)
            return f"v{bits:012x}"
        except Exception:
            return "v0"

    def _context_key(self, target):
        x0, y0, x1, y1 = target["box"]
        cx = (x0 + x1) / 2.0
        cy = (y0 + y1) / 2.0
        _, rect, dpi = self._target_window_info(target)
        ww = max(1.0, float(rect.right - rect.left))
        wh = max(1.0, float(rect.bottom - rect.top))
        locx = int(_clamp(((cx - rect.left) / ww) * 12.0, 0.0, 11.999))
        locy = int(_clamp(((cy - rect.top) / wh) * 12.0, 0.0, 11.999))
        logical_h = max(1.0, (y1 - y0) * 96.0 / max(48.0, float(dpi)))
        logical_wh = max(1.0, wh * 96.0 / max(48.0, float(dpi)))
        size_bucket = int(_clamp(round((logical_h / logical_wh) * 120.0), 0, 99))
        signature = self._window_signature(target)
        digits = len(str(self.original_target.get("raw_text", self.original_target.get("text", self.original_target["value"]))))
        return f"{signature}|w{locx},{locy}|d{digits}|s{size_bucket}|{self._visual_context_token()}"

    def _context_descriptor(self, image, origin, box):
        x0, y0, x1, y1 = box
        bw = max(6, x1 - x0)
        bh = max(6, y1 - y0)
        margin_x = max(28, int(bw * 3.4))
        margin_y = max(24, int(bh * 2.8))
        ix0 = max(0, int(x0 - margin_x - origin[0]))
        iy0 = max(0, int(y0 - margin_y - origin[1]))
        ix1 = min(image.width, int(x1 + margin_x - origin[0]))
        iy1 = min(image.height, int(y1 + margin_y - origin[1]))
        if ix1 - ix0 < 12 or iy1 - iy0 < 12:
            return None
        gray = np.asarray(image.crop((ix0, iy0, ix1, iy1)).convert("L"), dtype=np.uint8).copy()
        tx0 = max(0, int(x0 - origin[0] - ix0 - bw * 0.25))
        ty0 = max(0, int(y0 - origin[1] - iy0 - bh * 0.25))
        tx1 = min(gray.shape[1], int(x1 - origin[0] - ix0 + bw * 0.25))
        ty1 = min(gray.shape[0], int(y1 - origin[1] - iy0 + bh * 0.25))
        fill = int(np.median(gray))
        gray[ty0:ty1, tx0:tx1] = fill
        small = cv2.resize(gray, (30, 24), interpolation=cv2.INTER_AREA).astype(np.float32) / 255.0
        mean = float(small.mean())
        std = float(small.std())
        if std > 0.03:
            small = (small - mean) / std
            small = np.clip((small + 3.0) / 6.0, 0.0, 1.0)
        return small.reshape(-1).tolist()

    def _ensure_identity_context(self, image, origin):
        if self.target_identity is None or self.target is None:
            return
        if not self.target_identity.get("window"):
            self.target_identity["window"] = self._window_signature(self.target)
        if self.target_identity.get("context") is None:
            desc = self._context_descriptor(image, origin, self.target["box"])
            if desc is not None:
                self.target_identity["context"] = desc

    def _match_target(self, numbers, image, origin, wide=False):
        if not numbers or self.target is None or self.original_target is None:
            return None
        old_box = self.target["box"]
        ox = (old_box[0] + old_box[2]) / 2.0
        oy = (old_box[1] + old_box[3]) / 2.0
        oh = max(1.0, old_box[3] - old_box[1])
        ident = self.target_identity or {}
        initial_box = ident.get("initial_box", old_box)
        ix = (initial_box[0] + initial_box[2]) / 2.0
        iy = (initial_box[1] + initial_box[3]) / 2.0
        stored_context = ident.get("context")
        stored_window = ident.get("window", "")
        max_target_move = 18.0 if wide else 5.5
        max_context_mse = 0.14 if wide else 0.12
        ranked = []
        for source in numbers:
            n = dict(source)
            candidates = source.get("value_candidates")
            if self.current_value is not None and isinstance(candidates, list) and candidates:
                n["value"] = recognizer._parse_number_text(source.get("text", ""), reference=self.current_value)
                if n["value"] is None:
                    n["value"] = source["value"]
            b = n["box"]
            cx = (b[0] + b[2]) / 2.0
            cy = (b[1] + b[3]) / 2.0
            nh = max(1.0, b[3] - b[1])
            dist = math.hypot(cx - ox, cy - oy) / oh
            if dist > max_target_move:
                continue
            if stored_window and self._window_signature(n) != stored_window:
                continue
            context_mse = None
            if stored_context is not None:
                desc = self._context_descriptor(image, origin, b)
                if desc is None:
                    continue
                a = np.asarray(stored_context, dtype=np.float32)
                d = np.asarray(desc, dtype=np.float32)
                context_mse = float(np.mean((a - d) ** 2))
                if context_mse > max_context_mse:
                    continue
            overlap = recognizer._iou(b, old_box)
            size_penalty = abs(math.log(nh / oh))
            if wide:
                score = min(dist, 10.0) * 0.22 + size_penalty * 0.9 - overlap * 1.7
                score += math.hypot(cx - ix, cy - iy) / max(oh, 12.0) * 0.018
                if self.current_value is not None and _same_ocr_number(n, self.target):
                    score -= 0.35
            else:
                score = dist * 0.72 + size_penalty * 1.15 - overlap * 2.6
            if stored_context is None and not _same_ocr_number(n, self.original_target):
                score += 1.35
            if context_mse is not None:
                score += context_mse * (7.0 if wide else 8.5)
            ranked.append((score, n))
        ranked.sort(key=lambda pair: pair[0])
        if not ranked:
            return None
        threshold = 5.2 if wide else 3.5
        return ranked[0][1] if ranked[0][0] <= threshold else None

    def observe_selected_semantic_truth(self):
        if (recognizer is None or self.target is None or self.control_state != self.CONTROL_ARMING
                or self.stop_event.is_set() or self.user_interrupt_event.is_set()):
            return False
        image, origin = capture_screen()
        observation = self._detect_target_region(image, origin, window_scope=False)
        if observation is None:
            observation = self._detect_target_region(image, origin, window_scope=True)
        if observation is None or float(observation.get("conf", 0.0)) < 0.86:
            return False
        ocr_text = str(observation.get("text", ""))
        if not ocr_text or not recognizer._parse_number_candidates(ocr_text):
            return False
        self.target = dict(observation)
        self.current_value = observation.get("value")
        semantic_text = self._native_value_near_target()
        if not semantic_text:
            semantic_text = self._uia_value_near_target(cooldown_kind="pre_value", cooldown=3.0)
        if not semantic_text:
            return False
        semantic_values = recognizer._parse_number_candidates(semantic_text)
        if not semantic_values or not any(_same_number(value, observation.get("value")) for value in semantic_values):
            return False
        recognizer.observe_verified_number(
            image, origin, observation, ocr_text, source="semantic_truth", cancel_event=self.stop_event,
        )
        return True

    def _screen_bounds(self):
        vx, vy = virtual_origin()
        return vx, vy, vx + max(1, user32.GetSystemMetrics(78)) - 1, vy + max(1, user32.GetSystemMetrics(79)) - 1

    def _exploration_level(self, ctx):
        trials = max(1, int(ctx.get("trials", 0)))
        stagnation = max(0, int(ctx.get("stagnation", 0)))
        required = max(3, int(round(math.log2(trials + 3.0))))
        return min(3, stagnation // required)


    def _window_bounds_for_target(self, target):
        vx0, vy0, vx1, vy1 = self._screen_bounds()
        _, rect, _ = self._target_window_info(target)
        return max(vx0, rect.left), max(vy0, rect.top), min(vx1, rect.right - 1), min(vy1, rect.bottom - 1)


    def _point_to_target_relative(self, x, y, target):
        x0, y0, x1, y1 = target["box"]
        cx = (x0 + x1) / 2.0
        cy = (y0 + y1) / 2.0
        h = max(1.0, y1 - y0)
        return (float(x) - cx) / h, (float(y) - cy) / h


    def _random_point(self, target, level):
        vx0, vy0, vx1, vy1 = self._screen_bounds()
        x0, y0, x1, y1 = target["box"]
        cx = (x0 + x1) / 2.0
        cy = (y0 + y1) / 2.0
        h = max(1.0, y1 - y0)
        level = int(_clamp(level, 0, 3))
        if level == 0:
            x = random.uniform(x0, max(x0 + 1, x1))
            y = random.uniform(y0, max(y0 + 1, y1))
        elif level == 1:
            radius = random.uniform(1.0, 3.0) * h
            angle = random.uniform(0.0, math.tau)
            x = cx + math.cos(angle) * radius + random.gauss(0.0, h * 0.35)
            y = cy + math.sin(angle) * radius + random.gauss(0.0, h * 0.35)
        elif level == 2:
            wx0, wy0, wx1, wy1 = self._window_bounds_for_target(target)
            x = random.uniform(wx0, max(wx0 + 1, wx1))
            y = random.uniform(wy0, max(wy0 + 1, wy1))
        else:
            wx0, wy0, wx1, wy1 = self._window_bounds_for_target(target)
            edge_bias = random.random() < 0.35
            if edge_bias:
                x = random.choice((random.uniform(wx0, wx0 + (wx1 - wx0) * 0.22), random.uniform(wx1 - (wx1 - wx0) * 0.22, wx1)))
                y = random.uniform(wy0, wy1)
            else:
                x = random.uniform(wx0, max(wx0 + 1, wx1))
                y = random.uniform(wy0, max(wy0 + 1, wy1))
        x = _clamp(x, vx0, vx1)
        y = _clamp(y, vy0, vy1)
        return self._point_to_target_relative(x, y, target)


    def _uia_semantic_program(self, target):
        if self.current_value is None:
            return None
        key = self._context_key(target)
        now = time.monotonic()
        cached = self.uia_semantic_cache.get(key)
        if isinstance(cached, tuple) and now - float(cached[0]) < 45.0:
            payload = cached[1]
        else:
            x0, y0, x1, y1 = target["box"]
            cx = int(round((x0 + x1) / 2.0))
            cy = int(round((y0 + y1) / 2.0))
            powershell = Path(os.environ.get("SystemRoot", r"C:\Windows")) / "System32" / "WindowsPowerShell" / "v1.0" / "powershell.exe"
            if not powershell.exists():
                self.uia_semantic_cache[key] = (now, None)
                return None
            script = f'''$ErrorActionPreference='Stop';
Add-Type -AssemblyName UIAutomationClient; Add-Type -AssemblyName UIAutomationTypes; Add-Type -AssemblyName WindowsBase;
$p=New-Object System.Windows.Point({cx},{cy}); $e=[System.Windows.Automation.AutomationElement]::FromPoint($p);
if($null -eq $e){{exit 0}};
$walker=[System.Windows.Automation.TreeWalker]::ControlViewWalker; $out=$null;
for($i=0;$i -lt 4 -and $null -ne $e;$i++){{
  $hasValue=$false; $readOnly=$true; $hasRange=$false; $hasInvoke=$false;
  try{{$vp=$e.GetCurrentPattern([System.Windows.Automation.ValuePattern]::Pattern);$hasValue=$true;$readOnly=$vp.Current.IsReadOnly}}catch{{}};
  try{{$rp=$e.GetCurrentPattern([System.Windows.Automation.RangeValuePattern]::Pattern);$hasRange=$true}}catch{{}};
  try{{$ip=$e.GetCurrentPattern([System.Windows.Automation.InvokePattern]::Pattern);$hasInvoke=$true}}catch{{}};
  if(($hasValue -and -not $readOnly) -or $hasRange -or $hasInvoke){{
    $r=$e.Current.BoundingRectangle;
    $out=[pscustomobject]@{{type=$e.Current.ControlType.ProgrammaticName;name=$e.Current.Name;value=$hasValue;readonly=$readOnly;range=$hasRange;invoke=$hasInvoke;left=$r.Left;top=$r.Top;right=$r.Right;bottom=$r.Bottom}};break
  }};
  $e=$walker.GetParent($e)
}};
if($null -ne $out){{$out|ConvertTo-Json -Compress}}'''
            result = run_child(
                [str(powershell), "-NoLogo", "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass", "-Command", script],
                cwd=str(app_dir), env=os.environ.copy(), stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                text=True, timeout=2.5, cancel_event=self.stop_event,
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
            )
            payload = None
            if result is not None and result.returncode == 0 and str(result.stdout).strip():
                try:
                    payload = json.loads(str(result.stdout).strip().splitlines()[-1])
                except Exception:
                    payload = None
            self.uia_semantic_cache[key] = (now, payload)
            if len(self.uia_semantic_cache) > 96:
                oldest = sorted(self.uia_semantic_cache.items(), key=lambda pair: float(pair[1][0]))[:32]
                for old_key, _ in oldest:
                    self.uia_semantic_cache.pop(old_key, None)

        if not isinstance(payload, dict):
            return None
        if bool(payload.get("value")) and not bool(payload.get("readonly", True)):
            current = abs(_as_decimal(self.current_value or 0))
            exponent = current.adjusted() if current else 0
            try:
                _value, display_quantum = _observation_value_and_quantum(target)
            except Exception:
                display_quantum = Decimal(1)
            delta = max(display_quantum, Decimal(1).scaleb(exponent - 1))
            return [{"op": "replace_number", "delta": str(delta.normalize())}]

        try:
            left = float(payload.get("left")); top = float(payload.get("top"))
            right = float(payload.get("right")); bottom = float(payload.get("bottom"))
            cx = (left + right) / 2.0; cy = (top + bottom) / 2.0
        except (TypeError, ValueError):
            return None
        rx, ry = self._point_to_target_relative(cx, cy, target)
        focus = [
            {"op": "mouse_abs", "rx": rx, "ry": ry, "duration": 0.06},
            {"op": "mouse_button", "button": "left", "down": True},
            {"op": "mouse_button", "button": "left", "down": False},
        ]
        if bool(payload.get("range")):
            focus.extend([
                {"op": "key_event", "mode": "vk", "code": 0x27, "down": True, "extended": False},
                {"op": "key_event", "mode": "vk", "code": 0x27, "down": False, "extended": False},
            ])
            return focus
        if bool(payload.get("invoke")):
            name = str(payload.get("name") or "").strip().lower()
            if name in {"+", "＋", "increase", "increment", "add", "增加", "增大", "加"}:
                return focus
        return None


    def _native_control_candidates(self, target):
        root_hwnd, _root_rect, _dpi = self._target_window_info(target)
        if not root_hwnd:
            return []
        x0, y0, x1, y1 = target["box"]
        tcx = (x0 + x1) / 2.0
        tcy = (y0 + y1) / 2.0
        th = max(1.0, y1 - y0)
        candidates = []

        @WNDENUMPROC
        def enum_proc(hwnd, _lparam):
            try:
                if not user32.IsWindowVisible(hwnd):
                    return True
                rect = wintypes.RECT()
                if not user32.GetWindowRect(hwnd, ctypes.byref(rect)):
                    return True
                if rect.right <= rect.left or rect.bottom <= rect.top:
                    return True
                cx = (rect.left + rect.right) / 2.0
                cy = (rect.top + rect.bottom) / 2.0
                distance = math.hypot(cx - tcx, cy - tcy) / th
                if distance > 8.0:
                    return True
                class_buf = ctypes.create_unicode_buffer(128)
                user32.GetClassNameW(hwnd, class_buf, len(class_buf))
                cls = class_buf.value.strip()
                length = min(256, max(0, int(user32.GetWindowTextLengthW(hwnd))))
                text_buf = ctypes.create_unicode_buffer(length + 1)
                if length:
                    user32.GetWindowTextW(hwnd, text_buf, len(text_buf))
                candidates.append({
                    "hwnd": hwnd,
                    "class": cls,
                    "text": text_buf.value.strip(),
                    "rect": (rect.left, rect.top, rect.right, rect.bottom),
                    "distance": distance,
                })
            except Exception:
                pass
            return True

        try:
            user32.EnumChildWindows(root_hwnd, enum_proc, 0)
        except Exception:
            return []
        return candidates

    def _send_message_timeout(self, hwnd, message, w_param=0, l_param=0, timeout_ms=300):
        result = ULONG_PTR(0)
        ok = user32.SendMessageTimeoutW(
            hwnd, int(message), wintypes.WPARAM(int(w_param)), wintypes.LPARAM(int(l_param)),
            SMTO_ABORTIFHUNG, max(50, int(timeout_ms)), ctypes.byref(result),
        )
        return bool(ok), int(result.value)

    def _native_edit_at_target(self):
        if self.target is None:
            return None
        x0, y0, x1, y1 = self.target["box"]
        pt = wintypes.POINT(int(round((x0 + x1) / 2.0)), int(round((y0 + y1) / 2.0)))
        hwnd = user32.WindowFromPoint(pt)
        if not hwnd:
            return None
        root_hwnd, _rect, _dpi = self._target_window_info(self.target)
        selected_root = int((self.target_identity or {}).get("root_hwnd", 0) or 0)
        actual_root = user32.GetAncestor(hwnd, GA_ROOT) or hwnd
        if not root_hwnd or not selected_root or int(root_hwnd) != selected_root or int(actual_root) != selected_root:
            return None
        class_buf = ctypes.create_unicode_buffer(128)
        user32.GetClassNameW(hwnd, class_buf, len(class_buf))
        cls = class_buf.value.strip().lower()
        if not (cls.startswith("edit") or cls.startswith("richedit")):
            return None
        style = int(user32.GetWindowLongW(hwnd, GWL_STYLE)) & 0xFFFFFFFF
        if style & ES_PASSWORD:
            return None
        rect = wintypes.RECT()
        if not user32.GetWindowRect(hwnd, ctypes.byref(rect)):
            return None
        ix = max(0.0, min(float(rect.right), float(x1)) - max(float(rect.left), float(x0)))
        iy = max(0.0, min(float(rect.bottom), float(y1)) - max(float(rect.top), float(y0)))
        overlap = (ix * iy) / max(1.0, float(x1 - x0) * float(y1 - y0))
        return hwnd if overlap >= 0.70 else None

    def _native_get_control_text(self, hwnd):
        ok, length = self._send_message_timeout(hwnd, WM_GETTEXTLENGTH)
        if not ok:
            return None
        length = max(0, min(4096, int(length)))
        buffer = ctypes.create_unicode_buffer(length + 2)
        ok, _ = self._send_message_timeout(hwnd, WM_GETTEXT, len(buffer), ctypes.addressof(buffer))
        return buffer.value if ok else None

    def _native_value_near_target(self):
        hwnd = self._native_edit_at_target()
        if not hwnd:
            return None
        text = self._native_get_control_text(hwnd)
        return str(text).strip() if text is not None else None

    def _unique_numeric_span_matching(self, control_text, expected_value):
        if recognizer is None:
            return None
        pattern = re.compile(
            r"(?<![0-9A-Za-z_])(?:\(\s*)?[+-]?(?:"
            r"(?:\d+(?:[ \u00A0\u202F]+\d+)*(?:[.,]\d*(?:[ \u00A0\u202F]+\d+)*)*)"
            r"|(?:[.,]\d+(?:[ \u00A0\u202F]+\d+)*))"
            r"(?:[eE][+-]?\d+)?(?:\s*\))?(?![0-9A-Za-z_])"
        )
        matches = []
        for match in pattern.finditer(str(control_text)):
            token = match.group(0)
            try:
                values = recognizer._parse_number_candidates(token)
            except Exception:
                continue
            if any(_same_number(value, expected_value) for value in values):
                matches.append((match.start(), match.end()))
        return matches[0] if len(matches) == 1 else None

    def _native_set_value_near_target(self, text):
        if self.current_value is None:
            return False
        hwnd = self._native_edit_at_target()
        if not hwnd:
            return False
        current_text = self._native_get_control_text(hwnd)
        if current_text is None:
            return False
        span = self._unique_numeric_span_matching(current_text, self.current_value)
        if span is None:
            return False
        start, end = span
        start_units = len(current_text[:start].encode("utf-16-le")) // 2
        end_units = len(current_text[:end].encode("utf-16-le")) // 2
        replacement = str(text)
        expected_full_text = current_text[:start] + replacement + current_text[end:]
        ok, _ = self._send_message_timeout(hwnd, EM_SETSEL, start_units, end_units, timeout_ms=450)
        if not ok:
            return False
        buffer = ctypes.create_unicode_buffer(replacement)
        ok, _ = self._send_message_timeout(hwnd, EM_REPLACESEL, 1, ctypes.addressof(buffer), timeout_ms=450)
        if not ok:
            return False
        updated = self._native_get_control_text(hwnd)
        return updated == expected_full_text

    def _native_semantic_program(self, target):
        if self.current_value is None:
            return None
        x0, y0, x1, y1 = target["box"]
        center_pt = wintypes.POINT(int((x0 + x1) / 2), int((y0 + y1) / 2))
        direct_hwnd = user32.WindowFromPoint(center_pt)
        direct_class = ""
        if direct_hwnd:
            class_buf = ctypes.create_unicode_buffer(128)
            user32.GetClassNameW(direct_hwnd, class_buf, len(class_buf))
            direct_class = class_buf.value.strip().lower()
        if direct_class.startswith("edit") or direct_class.startswith("richedit"):
            current = abs(_as_decimal(self.current_value or 0))
            exponent = current.adjusted() if current else 0
            delta = max(Decimal(1), Decimal(1).scaleb(exponent - 1))
            return [{"op": "replace_number", "delta": str(delta.normalize())}]

        candidates = self._native_control_candidates(target)
        if not candidates:
            return None
        plus_tokens = {"+", "＋", "▲", "↑", "add", "increase", "increment", "增加", "增大", "加"}
        ranked = []
        for item in candidates:
            cls = item["class"].lower()
            text = item["text"].strip().lower()
            rect = item["rect"]
            cx = (rect[0] + rect[2]) / 2.0
            cy = (rect[1] + rect[3]) / 2.0
            if cls == "button" and text in plus_tokens:
                ranked.append((0, item["distance"], "click", cx, cy))
            elif "updown" in cls:
                # Native spinner increment region is the upper half.
                ranked.append((1, item["distance"], "click", cx, rect[1] + (rect[3] - rect[1]) * 0.25))
            elif "trackbar" in cls:
                ranked.append((2, item["distance"], "right", cx, cy))
        if not ranked:
            return None
        _priority, _distance, action, cx, cy = min(ranked)
        rx, ry = self._point_to_target_relative(cx, cy, target)
        click = [
            {"op": "mouse_abs", "rx": rx, "ry": ry, "duration": 0.06},
            {"op": "mouse_button", "button": "left", "down": True},
            {"op": "mouse_button", "button": "left", "down": False},
        ]
        if action == "right":
            click.extend([
                {"op": "key_event", "mode": "vk", "code": 0x27, "down": True, "extended": False},
                {"op": "key_event", "mode": "vk", "code": 0x27, "down": False, "extended": False},
            ])
        return click


    def _random_duration(self, mean):
        return random.expovariate(1.0 / max(1e-6, float(mean)))

    def _random_count(self, stop_probability=0.68):
        count = 1
        while random.random() > stop_probability:
            count += 1
        return count

    def _random_text(self):
        digits = "0123456789"
        count = max(1, self._random_count(0.72))
        body = "".join(random.choice(digits) for _ in range(count))
        if random.random() < 0.24:
            separator = recognizer.locale_decimal if recognizer is not None and recognizer.locale_decimal in (".", ",") else "."
            tail = "".join(random.choice(digits) for _ in range(max(1, min(4, self._random_count(0.68)))))
            body += separator + tail
        if random.random() < 0.14:
            exponent = random.randint(-max(1, count), max(2, count * 2))
            body += random.choice(("e", "E")) + ("+" if exponent >= 0 and random.random() < 0.5 else "") + str(exponent)
        return body


    def _grow_key_tap(self):
        priority = (0x26, 0x28, 0x6B, 0x6D, 0xBB, 0xBD)
        code = random.choice(priority)
        return [
            {"op": "key_event", "mode": "vk", "code": code, "down": True, "extended": False},
            {"op": "key_event", "mode": "vk", "code": code, "down": False, "extended": False},
        ]


    def _random_operation(self, target, level):
        kinds = ("move", "click", "mouse_rel", "wheel", "key", "replace_number", "wait")
        locality = 1.0 + max(0, 2 - int(level)) * 0.25
        ctx = self._ctx(self._context_key(target))
        replace_blocked = int(ctx.get("replace_not_applicable", 0)) > 0
        # Once direct editing has been proven inapplicable for this context,
        # spend exploration budget on nearby controls/keys instead of repeating
        # a click that may navigate away.
        weights = (12 * locality, 22 * locality, 5, 17, 20, (0.5 if replace_blocked else 20), 8)
        kind = random.choices(kinds, weights=weights, k=1)[0]
        if kind in ("move", "click"):
            rx, ry = self._random_point(target, level)
            move = {"op": "mouse_abs", "rx": rx, "ry": ry, "duration": self._random_duration(0.18 if kind == "move" else 0.12)}
            if kind == "move":
                return [move]
            return [
                move,
                {"op": "mouse_button", "button": "left", "down": True},
                {"op": "wait", "seconds": self._random_duration(0.04)},
                {"op": "mouse_button", "button": "left", "down": False},
            ]
        if kind == "mouse_rel":
            spread = 0.55 + 0.85 * int(level)
            return [{"op": "mouse_rel", "rdx": random.gauss(0.0, spread), "rdy": random.gauss(0.0, spread),
                     "duration": self._random_duration(0.14), "no_coalesce": False}]
        if kind == "wheel":
            steps = random.choice((-3, -2, -1, 1, 2, 3))
            return [{"op": "wheel", "delta": steps * 120, "horizontal": random.random() < 0.08}]
        if kind == "key":
            return self._grow_key_tap()
        if kind == "replace_number":
            current = abs(_as_decimal(self.current_value or 0))
            exponent = current.adjusted() if current else 0
            deltas = (Decimal(1).scaleb(exponent - 2), Decimal(1).scaleb(exponent - 1), Decimal(1),
                      Decimal(1).scaleb(exponent), Decimal(1).scaleb(exponent + 1))
            delta = abs(random.choice(deltas))
            return [{"op": "replace_number", "delta": str(delta.normalize())}]
        return [{"op": "wait", "seconds": self._random_duration(0.20)}]

    def _random_program(self, target, level=0):
        ctx = self._ctx(self._context_key(target))
        replace_blocked = int(ctx.get("replace_not_applicable", 0)) > 0
        if not replace_blocked and random.random() < 0.34:
            current = abs(_as_decimal(self.current_value or 0))
            exponent = current.adjusted() if current else 0
            delta = abs(random.choice((Decimal(1), Decimal(1).scaleb(exponent - 1),
                                       Decimal(1).scaleb(exponent), Decimal(1).scaleb(exponent + 1))))
            return [{"op": "replace_number", "delta": str(delta.normalize())}]
        chunks = max(1, self._random_count(0.64))
        program = []
        for _ in range(chunks):
            program.extend(self._random_operation(target, level))
        normalized = self._normalize_program(program, space="target")
        return normalized if normalized else self._grow_key_tap()

    def _mutate_program(self, program, target, level=0):
        mutated = self._normalize_program(json.loads(json.dumps(program)), space="target")
        if not mutated or random.random() < 0.16:
            return self._random_program(target, level)
        mode = random.choice(("tweak", "tweak", "insert", "replace_all"))
        if mode == "replace_all":
            return self._random_program(target, level)
        if mode == "insert":
            chunk = self._random_operation(target, level)
            index = random.randrange(len(mutated) + 1)
            candidate = mutated[:index] + chunk + mutated[index:]
            normalized = self._normalize_program(candidate, space="target")
            return normalized if normalized else mutated
        index = random.randrange(len(mutated))
        op = mutated[index]
        kind = op.get("op")
        factor = math.exp(random.gauss(0.0, 0.35))
        if kind == "mouse_abs":
            spread = 0.25 + 0.45 * int(level)
            op["rx"] = float(op.get("rx", 0.0)) + random.gauss(0.0, spread)
            op["ry"] = float(op.get("ry", 0.0)) + random.gauss(0.0, spread)
            op["duration"] = max(0.0, float(op.get("duration", 0.0)) * factor)
        elif kind == "mouse_rel":
            spread = 0.25 + 0.45 * int(level)
            op["rdx"] = float(op.get("rdx", 0.0)) + random.gauss(0.0, spread)
            op["rdy"] = float(op.get("rdy", 0.0)) + random.gauss(0.0, spread)
            op["duration"] = max(0.0, float(op.get("duration", 0.0)) * factor)
        elif kind == "mouse_button":
            old_button = str(op.get("button", "left"))
            new_button = random.choice(("left", "right", "middle"))
            for item in mutated:
                if item.get("op") == "mouse_button" and str(item.get("button", "left")) == old_button:
                    item["button"] = new_button
        elif kind == "wheel":
            steps = int(round(float(op.get("delta", 120)) / 120.0)) + random.choice((-2, -1, 1, 2))
            op["delta"] = (steps or random.choice((-1, 1))) * 120
        elif kind == "key_event":
            old_identity = (str(op.get("mode", "vk")), int(op.get("code", 0)), bool(op.get("extended", False)))
            replacement = self._grow_key_tap()[0]
            for item in mutated:
                if item.get("op") == "key_event" and (str(item.get("mode", "vk")), int(item.get("code", 0)), bool(item.get("extended", False))) == old_identity:
                    item["mode"] = replacement["mode"]
                    item["code"] = replacement["code"]
                    item["extended"] = replacement["extended"]
        elif kind == "unicode_text":
            op["text"] = self._random_text()
            op["interval"] = max(0.0, float(op.get("interval", 0.0)) * factor)
        elif kind == "replace_number":
            op["delta"] = max(1e-6, abs(float(op.get("delta", 1.0))) * factor)
        elif kind == "wait":
            op["seconds"] = max(0.0, float(op.get("seconds", 0.0)) * factor)
        normalized = self._normalize_program(mutated, space="target")
        return normalized if normalized else self._random_program(target, level)

    def _ctx(self, key):
        contexts = self.state["contexts"]
        if key not in contexts:
            limits = self._storage_limits()
            if len(contexts) >= limits["contexts"]:
                victim = min(contexts.items(), key=lambda pair: self._context_rank(pair[1]))[0]
                del contexts[victim]
            elite = self.state.get("elite_policies", {}).get(str(key))
            contexts[key] = {
                "programs": [], "best_policy": json.loads(json.dumps(elite)) if isinstance(elite, dict) else None,
                "challenger": None, "canary": None, "champion_history": [], "trials": 0, "stagnation": 0,
                "last_used": int(self.state.get("trials", 0)),
            }
        ctx = contexts[key]
        ctx.setdefault("stagnation", 0)
        ctx.setdefault("canary", None)
        if ctx.get("canary") is None and isinstance(ctx.get("best_policy"), dict):
            ctx["canary"] = self._policy_canary_from_policy(ctx["best_policy"])
            self.state_dirty = True
        ctx["last_used"] = int(self.state.get("trials", 0))
        return ctx

    def _find_record(self, ctx, fingerprint):
        for rec in ctx.get("programs", []):
            if rec.get("fingerprint") == fingerprint:
                return rec
        return None

    def _policy_canary_from_policy(self, policy):
        if not isinstance(policy, dict):
            return None
        return {
            "success_floor": max(0.0, min(1.0, float(policy.get("success_floor", 0.0)))),
            "gain_floor": max(0.0, float(policy.get("gain_floor", 0.0))),
            "reward_floor": float(policy.get("reward_floor", -1e9)),
            "established_trial": int(self.state.get("trials", 0)),
        }

    def _policy_passes_canary(self, candidate, canary):
        if not isinstance(canary, dict):
            return True
        if not isinstance(candidate, dict):
            return False
        return (
            float(candidate.get("success_floor", 0.0)) + 0.01 >= float(canary.get("success_floor", 0.0))
            and float(candidate.get("gain_floor", 0.0)) + max(1e-9, abs(float(canary.get("gain_floor", 0.0))) * 0.03) >= float(canary.get("gain_floor", 0.0))
            and float(candidate.get("reward_floor", -1e9)) + 0.05 >= float(canary.get("reward_floor", -1e9))
        )

    def _strengthen_policy_canary(self, ctx, policy):
        proposed = self._policy_canary_from_policy(policy)
        if proposed is None:
            return
        current = ctx.get("canary")
        if not isinstance(current, dict):
            ctx["canary"] = proposed
            return
        current["success_floor"] = max(float(current.get("success_floor", 0.0)), proposed["success_floor"])
        current["gain_floor"] = max(float(current.get("gain_floor", 0.0)), proposed["gain_floor"])
        current["reward_floor"] = max(float(current.get("reward_floor", -1e9)), proposed["reward_floor"])

    def _maybe_seed_best_policy(self, key, ctx, rec):
        if ctx.get("best_policy") is not None:
            return
        n = int(rec.get("n", 0))
        wins = int(rec.get("wins", 0))
        if n < 8 or wins < 3:
            return
        evidence = {"n": n, "wins": wins, "reward_sum": float(rec.get("total_reward", 0.0)), "gain_sum": float(rec.get("total_gain", 0.0))}
        ctx["best_policy"] = self._policy_from_evidence(rec["program"], rec["fingerprint"], evidence)
        self._strengthen_policy_canary(ctx, ctx["best_policy"])
        self._store_elite_policy(key, ctx["best_policy"])
        self._mark_state_dirty(urgent=True)

    def _maybe_nominate_challenger(self, ctx, rec):
        best = ctx.get("best_policy")
        if best is None or ctx.get("challenger") is not None:
            return
        if rec.get("fingerprint") == best.get("fingerprint"):
            return
        if int(rec.get("blocked_until", 0)) > int(ctx.get("trials", 0)):
            return
        n = int(rec.get("n", 0))
        wins = int(rec.get("wins", 0))
        if n < 8 or wins < 3:
            return
        evidence = {"n": n, "wins": wins, "reward_sum": float(rec.get("total_reward", 0.0)), "gain_sum": float(rec.get("total_gain", 0.0))}
        candidate = self._policy_from_evidence(rec["program"], rec["fingerprint"], evidence)
        if not self._policy_is_strict_upgrade(candidate, best):
            return
        ctx["challenger"] = {
            "fingerprint": rec["fingerprint"], "program": json.loads(json.dumps(rec["program"])),
            "started_trial": int(ctx.get("trials", 0)),
            "candidate_eval": {"n": 0, "wins": 0, "reward_sum": 0.0, "gain_sum": 0.0},
            "incumbent_eval": {"n": 0, "wins": 0, "reward_sum": 0.0, "gain_sum": 0.0}
        }

    def _resolve_challenger(self, key, ctx):
        challenger = ctx.get("challenger")
        best = ctx.get("best_policy")
        if challenger is None or best is None:
            return
        cand = challenger["candidate_eval"]
        inc = challenger["incumbent_eval"]
        cand_n = max(0, int(cand.get("n", 0)))
        inc_n = max(0, int(inc.get("n", 0)))
        if cand_n < 16 or inc_n < 16:
            return
        cand_success = self._wilson_lower(cand["wins"], cand_n)
        inc_success = self._wilson_lower(inc["wins"], inc_n)
        cand_gain = float(cand["gain_sum"]) / cand_n
        inc_gain = float(inc["gain_sum"]) / inc_n
        cand_reward = float(cand["reward_sum"]) / cand_n
        inc_reward = float(inc["reward_sum"]) / inc_n
        candidate_policy = self._policy_from_evidence(challenger["program"], challenger["fingerprint"], cand)
        preserves_champion = self._policy_is_not_worse(candidate_policy, best)
        not_worse_in_validation = (
            cand_success + 1e-12 >= inc_success
            and cand_gain + 1e-12 >= inc_gain
            and cand_reward + 1e-12 >= inc_reward
        )
        clearly_better_in_validation = (
            cand_success > inc_success + 0.02
            or cand_gain > inc_gain * 1.05 + 1e-9
            or cand_reward > inc_reward + 0.05
        )
        passes_canary = self._policy_passes_canary(candidate_policy, ctx.get("canary"))
        if preserves_champion and passes_canary and self._policy_is_strict_upgrade(candidate_policy, best) and not_worse_in_validation and clearly_better_in_validation:
            ctx["champion_history"].append(json.loads(json.dumps(best)))
            ctx["best_policy"] = candidate_policy
            self._strengthen_policy_canary(ctx, candidate_policy)
            self._store_elite_policy(key, candidate_policy)
            ctx["challenger"] = None
            self._compact_context(ctx, self._storage_limits()["programs"], self._storage_limits()["history"])
            self._mark_state_dirty(urgent=True)
            return
        clearly_worse = (
            cand_success + 0.03 < inc_success
            or cand_gain + max(1e-9, abs(inc_gain) * 0.06) < inc_gain
            or cand_reward + 0.07 < inc_reward
            or not self._policy_is_not_worse(candidate_policy, best)
            or not self._policy_passes_canary(candidate_policy, ctx.get("canary"))
        )
        if clearly_worse or (cand_n >= 48 and inc_n >= 48):
            rec = self._find_record(ctx, challenger["fingerprint"])
            if rec is not None:
                rec["blocked_until"] = int(ctx.get("trials", 0)) + 192
            ctx["challenger"] = None

    def _semanticize_numeric_program(self, program):
        if self.current_value is None or recognizer is None:
            return json.loads(json.dumps(program))
        current = _as_decimal(self.current_value)
        prepared = []
        for source in program:
            op = dict(source)
            if op.get("op") == "unicode_text":
                parsed = recognizer._parse_number_text(str(op.get("text", "")))
                if parsed is not None:
                    difference = parsed - current
                    delta = difference if difference > 0 else abs(difference)
                    if delta == 0:
                        delta = max(Decimal(1), abs(current) * Decimal("0.01"))
                    op = {"op": "replace_number", "delta": str(delta.normalize())}
            prepared.append(op)
        return prepared

    def _pick_program(self, key, target):
        ctx = self._ctx(key)
        challenger = ctx.get("challenger")
        best = ctx.get("best_policy")
        if challenger is None and (best is None or float(best.get("success_floor", 0.0)) < 0.45):
            semantic = self._native_semantic_program(target)
            if semantic is None:
                semantic = self._uia_semantic_program(target)
            if semantic is not None and random.random() < 0.78:
                return self._semanticize_numeric_program(semantic), "semantic"
        if challenger is not None and best is not None:
            cand_n = int(challenger["candidate_eval"].get("n", 0))
            inc_n = int(challenger["incumbent_eval"].get("n", 0))
            if cand_n * 2 <= inc_n:
                prepared = self._semanticize_numeric_program(challenger["program"])
                return prepared, "challenger"
            prepared = self._semanticize_numeric_program(best["program"])
            return prepared, "incumbent_validation"
        programs = ctx["programs"]
        context_trials = int(ctx.get("trials", 0))
        confidence = 0.0
        if isinstance(best, dict):
            evidence = best.get("evidence", {})
            sample_confidence = 1.0 - math.exp(-max(0, int(evidence.get("n", 0))) / 10.0)
            performance_confidence = max(0.0, min(1.0, float(best.get("success_floor", 0.0)) + 0.25))
            confidence = sample_confidence * performance_confidence
        epsilon = 1.0
        if best is not None:
            epsilon = 0.16 * math.exp(-context_trials / 90.0) * (1.0 - 0.65 * confidence)
            epsilon += 0.018 * (1.0 - confidence) * math.exp(-context_trials / 700.0)
            if random.random() >= epsilon:
                return self._semanticize_numeric_program(best["program"]), "best"
        ranked = sorted(programs, key=lambda rec: (self._record_quality(rec), int(rec.get("n", 0))), reverse=True)
        base = None
        if best is not None and random.random() < 0.62:
            base = best["program"]
        elif ranked and random.random() < 0.74:
            pool_size = max(1, int(math.sqrt(len(ranked))))
            base = random.choice(ranked[:pool_size])["program"]
        elif self.state.get("success_memory") and random.random() < 0.62:
            window = self._window_signature(target)
            matches = [item for item in self.state["success_memory"] if item.get("window") == window]
            if matches:
                weighted = sorted(matches, key=self._memory_quality, reverse=True)
                base = random.choice(weighted[:max(1, int(math.sqrt(len(weighted))))])["program"]
        level = self._exploration_level(ctx)
        program = self._mutate_program(base, target, level) if base is not None else self._random_program(target, level)
        return self._semanticize_numeric_program(program), "explore"

    def _learn_program(self, key, program, reward, step_gain, role="explore", promotion_guard=False):
        self.state["trials"] = int(self.state.get("trials", 0)) + 1
        if step_gain > 0.0:
            self.state["successes"] = int(self.state.get("successes", 0)) + 1
        ctx = self._ctx(key)
        ctx["trials"] = int(ctx.get("trials", 0)) + 1
        ctx["last_used"] = int(self.state["trials"])
        if step_gain > 0.0:
            ctx["stagnation"] = 0
        else:
            ctx["stagnation"] = int(ctx.get("stagnation", 0)) + 1
        normalized = self._normalize_program(program, space="target")
        self._mark_state_dirty()
        if not normalized:
            self._maybe_save_state()
            return
        fingerprint = self._policy_fingerprint(normalized, self.target)
        pending = ctx.setdefault("pending_confirmations", {})
        pending_key = str(fingerprint)
        if step_gain > 0.0 and (promotion_guard or pending_key in pending):
            count = int(pending.get(pending_key, 0)) + 1
            if count < 2:
                pending[pending_key] = count
                if len(pending) > 24:
                    for stale_key in list(pending)[:-24]:
                        pending.pop(stale_key, None)
                self.state_dirty = True
                self._maybe_save_state()
                return
            pending.pop(pending_key, None)

        rec = self._find_record(ctx, fingerprint)
        if rec is None:
            rec = {
                "fingerprint": fingerprint, "program": json.loads(json.dumps(normalized)), "n": 0, "q": 0.0,
                "wins": 0, "best_gain": 0.0, "best_reward": -1e9, "total_reward": 0.0, "total_gain": 0.0,
                "last_seen": int(self.state["trials"]), "blocked_until": 0,
            }
            ctx["programs"].append(rec)
        rec["n"] = int(rec.get("n", 0)) + 1
        rec["total_reward"] = float(rec.get("total_reward", 0.0)) + float(reward)
        rec["total_gain"] = float(rec.get("total_gain", 0.0)) + float(step_gain)
        rec["last_seen"] = int(self.state["trials"])
        alpha = 1.0 / math.sqrt(rec["n"])
        rec["q"] = float(rec.get("q", 0.0)) + alpha * (float(reward) - float(rec.get("q", 0.0)))
        if step_gain > 0.0:
            rec["wins"] = int(rec.get("wins", 0)) + 1
            rec["best_gain"] = max(float(rec.get("best_gain", 0.0)), float(step_gain))
        if float(reward) > float(rec.get("best_reward", -1e9)):
            rec["best_reward"] = float(reward)
            rec["program"] = json.loads(json.dumps(normalized))
        if step_gain > 0.0:
            window = self._window_signature(self.target)
            memory = self.state.setdefault("success_memory", [])
            remembered = None
            for item in memory:
                if item.get("window") == window and item.get("fingerprint") == fingerprint:
                    remembered = item
                    break
            if remembered is None:
                remembered = {
                    "window": window, "fingerprint": fingerprint, "program": json.loads(json.dumps(normalized)),
                    "n": 0, "reward_sum": 0.0, "gain_sum": 0.0, "best_reward": -1e9, "best_gain": 0.0,
                    "last_seen": int(self.state["trials"]),
                }
                memory.append(remembered)
            remembered["n"] = int(remembered.get("n", 0)) + 1
            remembered["reward_sum"] = float(remembered.get("reward_sum", 0.0)) + float(reward)
            remembered["gain_sum"] = float(remembered.get("gain_sum", 0.0)) + float(step_gain)
            remembered["last_seen"] = int(self.state["trials"])
            if float(reward) > float(remembered.get("best_reward", -1e9)):
                remembered["best_reward"] = float(reward)
                remembered["best_gain"] = max(float(remembered.get("best_gain", 0.0)), float(step_gain))
                remembered["program"] = json.loads(json.dumps(normalized))

        challenger = ctx.get("challenger")
        best = ctx.get("best_policy")
        if challenger is not None and best is not None:
            if role == "challenger":
                self._eval_update(challenger["candidate_eval"], reward, step_gain)
            elif role == "incumbent_validation":
                self._eval_update(challenger["incumbent_eval"], reward, step_gain)
            self._resolve_challenger(key, ctx)
        self._maybe_seed_best_policy(key, ctx, rec)
        if role == "explore" and ctx.get("challenger") is None:
            self._maybe_nominate_challenger(ctx, rec)
        limits = self._storage_limits()
        if len(ctx["programs"]) > limits["programs"]:
            self._compact_context(ctx, limits["programs"], limits["history"])
        if len(self.state.get("success_memory", [])) > limits["memory"]:
            self._compact_state()
        self.state_dirty = True
        self._maybe_save_state()

    def _foreground_window_signature(self):
        hwnd = user32.GetForegroundWindow()
        if not hwnd:
            return "no-window"
        length = user32.GetWindowTextLengthW(hwnd)
        title_buf = ctypes.create_unicode_buffer(length + 1)
        user32.GetWindowTextW(hwnd, title_buf, len(title_buf))
        class_buf = ctypes.create_unicode_buffer(128)
        user32.GetClassNameW(hwnd, class_buf, len(class_buf))
        return f"{class_buf.value.strip()[:48]}|{_stable_window_title(title_buf.value)}"

    def _idle_context_key(self):
        vx0, vy0, vx1, vy1 = self._screen_bounds()
        width_bucket = max(1, (vx1 - vx0 + 1) // 320)
        height_bucket = max(1, (vy1 - vy0 + 1) // 180)
        return f"{self._foreground_window_signature()}|{width_bucket}x{height_bucket}"

    def _idle_program_fingerprint(self, program):
        canonical = []
        for op in program:
            kind = op.get("op")
            if kind == "mouse_abs":
                canonical.append((kind, round(float(op.get("sx", 0.0)), 3), round(float(op.get("sy", 0.0)), 3), self._time_bucket(op.get("duration", 0.0))))
            elif kind == "mouse_rel":
                canonical.append((kind, round(float(op.get("sdx", 0.0)), 3), round(float(op.get("sdy", 0.0)), 3),
                                  self._time_bucket(op.get("duration", 0.0)), bool(op.get("no_coalesce", False))))
            elif kind == "mouse_button":
                canonical.append((kind, str(op.get("button", "left")), bool(op.get("down", True))))
            elif kind == "wheel":
                canonical.append((kind, int(round(float(op.get("delta", 0)) / 120.0)), bool(op.get("horizontal", False))))
            elif kind == "key_event":
                canonical.append((kind, int(op.get("code", 0)), bool(op.get("down", True))))
            elif kind == "wait":
                canonical.append((kind, self._time_bucket(op.get("seconds", 0.0))))
        raw = json.dumps(canonical, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        return hashlib.blake2b(raw, digest_size=12).hexdigest()

    def _idle_random_point(self):
        vx0, vy0, vx1, vy1 = self._screen_bounds()
        width = max(1.0, float(vx1 - vx0 + 1))
        height = max(1.0, float(vy1 - vy0 + 1))
        for _ in range(20):
            if random.random() < 0.62:
                cx, cy = self._cursor_pos()
                x = random.gauss(cx, width * 0.14)
                y = random.gauss(cy, height * 0.14)
            else:
                x = random.uniform(vx0, vx1)
                y = random.uniform(vy0, vy1)
            x = _clamp(x, vx0, vx1)
            y = _clamp(y, vy0, vy1)
            if self._idle_point_is_safe(x, y):
                return _clamp((x - vx0) / width, 0.0, 1.0), _clamp((y - vy0) / height, 0.0, 1.0)
        hwnd = user32.GetForegroundWindow()
        rect = wintypes.RECT()
        if hwnd and user32.GetWindowRect(hwnd, ctypes.byref(rect)):
            x = (rect.left + rect.right) / 2.0
            y = (rect.top + rect.bottom) / 2.0
            if self._idle_point_is_safe(x, y):
                return _clamp((x - vx0) / width, 0.0, 1.0), _clamp((y - vy0) / height, 0.0, 1.0)
        cx, cy = self._cursor_pos()
        return _clamp((cx - vx0) / width, 0.0, 1.0), _clamp((cy - vy0) / height, 0.0, 1.0)

    def _window_class_and_text(self, hwnd):
        if not hwnd:
            return "", ""
        class_buf = ctypes.create_unicode_buffer(128)
        user32.GetClassNameW(hwnd, class_buf, len(class_buf))
        length = min(512, max(0, int(user32.GetWindowTextLengthW(hwnd))))
        text_buf = ctypes.create_unicode_buffer(length + 1)
        if length:
            user32.GetWindowTextW(hwnd, text_buf, len(text_buf))
        return class_buf.value.strip().lower(), text_buf.value.strip().lower()

    def _idle_sensitive_foreground(self):
        hwnd = user32.GetForegroundWindow()
        if not hwnd:
            return True
        cls, title = self._window_class_and_text(hwnd)
        sensitive_class_tokens = ("msidialog", "installshield", "credential", "security")
        sensitive_title_tokens = (
            "confirm", "confirmation", "warning", "security", "administrator", "permission", "credential",
            "install", "installer", "uninstall", "setup", "format", "purchase", "payment", "checkout",
            "确认", "警告", "安全", "管理员", "权限", "凭据", "安装", "卸载", "格式化", "购买", "付款", "结账",
        )
        if cls == "#32770" or any(token in cls for token in sensitive_class_tokens) or any(token in title for token in sensitive_title_tokens):
            return True
        thread_id = int(user32.GetWindowThreadProcessId(hwnd, None))
        if thread_id:
            info = GUITHREADINFO(); info.cbSize = ctypes.sizeof(GUITHREADINFO)
            if user32.GetGUIThreadInfo(thread_id, ctypes.byref(info)) and info.hwndFocus:
                focus_cls, _ = self._window_class_and_text(info.hwndFocus)
                if focus_cls.startswith("edit") or focus_cls.startswith("richedit"):
                    style = int(user32.GetWindowLongW(info.hwndFocus, GWL_STYLE)) & 0xFFFFFFFF
                    if style & ES_PASSWORD:
                        return True
        return False

    def _idle_point_is_safe(self, x, y):
        pt = wintypes.POINT(int(round(x)), int(round(y)))
        hwnd = user32.WindowFromPoint(pt)
        if not hwnd:
            return False
        root_hwnd = user32.GetAncestor(hwnd, GA_ROOT) or hwnd
        unsafe = {"shell_traywnd", "shell_secondarytraywnd", "traynotifywnd", "progman", "workerw"}
        for candidate in (hwnd, root_hwnd):
            cls, _text = self._window_class_and_text(candidate)
            if cls in unsafe:
                return False
        return True

    def _idle_click_is_safe(self, x, y):
        if not self._idle_point_is_safe(x, y) or self._idle_sensitive_foreground():
            return False
        pt = wintypes.POINT(int(round(x)), int(round(y)))
        hwnd = user32.WindowFromPoint(pt)
        root_hwnd = user32.GetAncestor(hwnd, GA_ROOT) or hwnd
        rect = wintypes.RECT()
        if user32.GetWindowRect(root_hwnd, ctypes.byref(rect)):
            try:
                dpi = max(48, int(user32.GetDpiForWindow(root_hwnd) or 96))
            except Exception:
                dpi = 96
            top_band = max(34, int(round(46 * max(1.0, dpi / 96.0))))
            if rect.top <= y <= rect.top + top_band:
                return False
        cls, text = self._window_class_and_text(hwnd)
        dangerous = (
            "delete", "remove", "erase", "destroy", "format", "uninstall", "purchase", "buy", "pay", "checkout",
            "submit", "send", "close", "exit", "quit", "terminate", "reset", "factory", "install", "execute",
            "删除", "移除", "清除", "销毁", "格式化", "卸载", "购买", "付款", "结账", "提交", "发送", "关闭", "退出",
            "重置", "恢复出厂", "安装", "执行",
        )
        if any(token in text for token in dangerous):
            return False
        if cls.startswith("edit") or cls.startswith("richedit"):
            style = int(user32.GetWindowLongW(hwnd, GWL_STYLE)) & 0xFFFFFFFF
            if style & ES_PASSWORD:
                return False
        # Learning may change exploration probability, but it never bypasses this permanent click-safety boundary.
        # Clicks are allowed only when Win32 semantics remain visible and low-side-effect.
        # Push buttons are allowed only when their label describes a low-side-effect navigation/help action.
        if hwnd == root_hwnd:
            return False
        if cls.startswith("button"):
            benign_button_tokens = (
                "help", "details", "more", "back", "previous", "cancel", "learn more", "info",
                "帮助", "详情", "更多", "返回", "上一步", "取消", "了解更多", "信息",
            )
            return bool(text) and any(token in text for token in benign_button_tokens)
        semantic_classes = ("syslink", "combobox", "listbox", "syslistview32", "systreeview32", "scrollbar", "msctls_trackbar")
        return any(cls.startswith(prefix) for prefix in semantic_classes)

    def _idle_key_is_safe(self, code):
        code = int(code)
        if self._idle_sensitive_foreground():
            return False
        # The permanent keyboard safety boundary is limited to the four arrow keys.
        return code in self.IDLE_INITIAL_VKS

    def _sanitize_idle_program(self, program):
        normalized = self._normalize_idle_program(program)
        if not normalized:
            return [{"op": "wait", "seconds": 0.08}]
        vx0, vy0, vx1, vy1 = self._screen_bounds()
        width = max(1.0, float(vx1 - vx0 + 1)); height = max(1.0, float(vy1 - vy0 + 1))
        pending = self._cursor_pos()
        safe = []
        skipped_buttons = set()
        for op in normalized:
            kind = op.get("op")
            if kind == "mouse_abs":
                pending = (vx0 + float(op.get("sx", 0.5)) * width, vy0 + float(op.get("sy", 0.5)) * height)
                safe.append(op)
            elif kind == "mouse_rel":
                pending = (pending[0] + float(op.get("sdx", 0.0)) * width, pending[1] + float(op.get("sdy", 0.0)) * height)
                safe.append(op)
            elif kind == "mouse_button":
                button = str(op.get("button", "left"))
                down = bool(op.get("down", True))
                if down:
                    if button == "left" and self._idle_click_is_safe(*pending):
                        safe.append(op)
                    else:
                        skipped_buttons.add(button)
                elif button not in skipped_buttons:
                    safe.append(op)
                else:
                    skipped_buttons.discard(button)
            elif kind == "wheel":
                if self._idle_point_is_safe(*pending):
                    safe.append(op)
            elif kind == "key_event":
                if self._idle_key_is_safe(op.get("code", 0)):
                    safe.append(op)
            elif kind == "wait":
                safe.append(op)
        normalized = self._normalize_idle_program(safe)
        if not normalized:
            return [{"op": "wait", "seconds": 0.08}]
        return normalized

    def _idle_key_tap(self):
        code = random.choice(self.IDLE_INITIAL_VKS)
        return [
            {"op": "key_event", "mode": "vk", "code": code, "down": True, "extended": False},
            {"op": "key_event", "mode": "vk", "code": code, "down": False, "extended": False},
        ]

    def _random_idle_program(self):
        sx, sy = self._idle_random_point()
        gesture = random.choices(("move", "click", "scroll", "key", "move_rel", "compound"), weights=(24, 8, 25, 18, 16, 9), k=1)[0]
        if gesture == "move":
            return [{"op": "mouse_abs", "sx": sx, "sy": sy, "duration": self._random_duration(0.24)}]
        if gesture == "click":
            return [{"op": "mouse_abs", "sx": sx, "sy": sy, "duration": self._random_duration(0.18)}, {"op": "mouse_button", "button": "left", "down": True}, {"op": "wait", "seconds": self._random_duration(0.045)}, {"op": "mouse_button", "button": "left", "down": False}]
        if gesture == "scroll":
            delta = random.choice((-720, -360, -240, -120, 120, 240, 360, 720))
            return [{"op": "mouse_abs", "sx": sx, "sy": sy, "duration": self._random_duration(0.16)}, {"op": "wheel", "delta": delta, "horizontal": random.random() < 0.12}]
        if gesture == "key":
            return self._idle_key_tap()
        if gesture == "move_rel":
            return [{"op": "mouse_rel", "sdx": random.gauss(0.0, 0.08), "sdy": random.gauss(0.0, 0.08), "duration": self._random_duration(0.18), "no_coalesce": False}]
        return [{"op": "mouse_abs", "sx": sx, "sy": sy, "duration": self._random_duration(0.18)}, {"op": "wheel", "delta": random.choice((-240, -120, 120, 240)), "horizontal": False}, {"op": "wait", "seconds": self._random_duration(0.10)}]

    def _mutate_idle_program(self, program):
        mutated = self._normalize_idle_program(json.loads(json.dumps(program)))
        if not mutated:
            return self._random_idle_program()
        op = mutated[random.randrange(len(mutated))]
        kind = op.get("op")
        factor = math.exp(random.gauss(0.0, 0.35))
        if kind == "mouse_abs":
            op["sx"] = _clamp(float(op.get("sx", 0.5)) + random.gauss(0.0, 0.06), 0.0, 1.0)
            op["sy"] = _clamp(float(op.get("sy", 0.5)) + random.gauss(0.0, 0.06), 0.0, 1.0)
            op["duration"] = max(0.0, float(op.get("duration", 0.0)) * factor)
        elif kind == "mouse_rel":
            op["sdx"] = float(op.get("sdx", 0.0)) + random.gauss(0.0, 0.05)
            op["sdy"] = float(op.get("sdy", 0.0)) + random.gauss(0.0, 0.05)
            op["duration"] = max(0.0, float(op.get("duration", 0.0)) * factor)
        elif kind == "wheel":
            steps = int(round(float(op.get("delta", 120)) / 120.0)) + random.choice((-2, -1, 1, 2))
            op["delta"] = (steps or random.choice((-1, 1))) * 120
        elif kind == "key_event":
            old_code = int(op.get("code", 0)); code = random.choice(self.IDLE_INITIAL_VKS)
            for item in mutated:
                if item.get("op") == "key_event" and int(item.get("code", 0)) == old_code:
                    item["code"] = code
        elif kind == "wait":
            op["seconds"] = max(0.0, min(0.8, float(op.get("seconds", 0.0)) * factor))
        if random.random() < 0.18:
            return self._random_idle_program()
        normalized = self._normalize_idle_program(mutated)
        return normalized if normalized else self._random_idle_program()

    def _idle_ctx(self, key):
        contexts = self.state.setdefault("idle_contexts", {})
        if key not in contexts:
            limits = self._storage_limits()
            cap = max(16, limits["contexts"] // 2)
            if len(contexts) >= cap:
                victim = min(contexts.items(), key=lambda pair: self._idle_context_quality(pair[1]))[0]
                del contexts[victim]
            contexts[key] = {"programs": [], "trials": 0, "last_used": int(self.state.get("idle_trials", 0))}
        return contexts[key]

    def _pick_idle_program(self, key):
        ctx = self._idle_ctx(key)
        programs = ctx.get("programs", [])
        trials = int(ctx.get("trials", 0))
        epsilon = 0.72 * math.exp(-trials / 55.0) + 0.12
        ranked = sorted(programs, key=lambda rec: (self._idle_record_quality(rec), int(rec.get("n", 0))), reverse=True)
        if ranked and random.random() >= epsilon:
            selected = random.choice(ranked[:max(1, min(4, int(math.sqrt(len(ranked))) + 1))])
            chosen = json.loads(json.dumps(selected["program"]))
            return self._sanitize_idle_program(chosen)
        base = None
        if ranked and random.random() < 0.64:
            selected = random.choice(ranked[:max(1, min(6, int(math.sqrt(len(ranked))) + 1))])
            base = selected["program"]
        elif self.state.get("idle_memory") and random.random() < 0.45:
            matches = [item for item in self.state["idle_memory"] if item.get("context") == key]
            pool = matches if matches else self.state["idle_memory"]
            if pool:
                pool = sorted(pool, key=self._idle_memory_quality, reverse=True)
                selected = random.choice(pool[:max(1, min(6, int(math.sqrt(len(pool))) + 1))])
                base = selected["program"]
        chosen = self._mutate_idle_program(base) if base is not None else self._random_idle_program()
        return self._sanitize_idle_program(chosen)

    def _idle_state_signature(self, image):
        pixels = max(1, int(hardware_profile["screen_pixels"]))
        ratio = math.sqrt(max(1.0, pixels) / float(1920 * 1080))
        width = int(_clamp(round(48 * ratio ** 0.25), 40, 72))
        height = max(24, int(round(width * 9.0 / 16.0)))
        arr = np.asarray(image.convert("L").resize((width, height), Image.Resampling.BILINEAR), dtype=np.float32) / 255.0
        quantized = np.clip(np.round(arr * 15.0), 0, 15).astype(np.uint8)
        digest = hashlib.blake2b(quantized.tobytes(), digest_size=10).hexdigest()
        return digest, arr


    def _idle_intrinsic_reward(self, before, after, program, before_window, after_window, before_cursor, settled=None, settled_window=None):
        before_hash, before_arr = self._idle_state_signature(before)
        after_hash, after_arr = self._idle_state_signature(after)
        visual_delta = float(np.mean(np.abs(after_arr - before_arr)))
        if self.idle_recent_states:
            novelty = min(float(np.mean(np.abs(after_arr - old_arr))) for _, old_arr in self.idle_recent_states)
            recent_match = min(float(np.mean(np.abs(after_arr - old_arr))) for _, old_arr in list(self.idle_recent_states)[-min(4, len(self.idle_recent_states)):])
        else:
            novelty = visual_delta
            recent_match = visual_delta
        state_repetitions = sum(1 for old_hash, _ in self.idle_recent_states if old_hash == after_hash)
        if novelty < 0.022 or state_repetitions:
            self.idle_no_novelty_streak += 1
        else:
            self.idle_no_novelty_streak = 0

        action = self._idle_program_fingerprint(self._normalize_idle_program(program))
        repetitions = sum(1 for old_action in self.idle_recent_actions if old_action == action)
        action_diversity = 1.0 / (1.0 + repetitions)
        no_change_penalty = max(0.0, 0.02 - visual_delta) * 6.0
        return_penalty = max(0.0, 0.025 - recent_match) * 4.5 if after_hash != before_hash else 0.08
        moderate_change = 1.0 - math.exp(-min(visual_delta, 0.18) * 8.0)
        excessive_change_penalty = max(0.0, visual_delta - 0.18) * 1.8
        stale_exploration_penalty = min(0.28, state_repetitions * 0.05 + self.idle_no_novelty_streak * 0.018)
        persistence_bonus = 0.0
        transient_penalty = 0.0
        if settled is not None:
            _settled_hash, settled_arr = self._idle_state_signature(settled)
            settle_drift = float(np.mean(np.abs(settled_arr - after_arr)))
            persistent_change = max(0.0, visual_delta - settle_drift)
            persistence_bonus = min(0.18, persistent_change * 1.8)
            transient_penalty = min(0.20, max(0.0, settle_drift - visual_delta * 0.45) * 2.0)

        window_switch = before_window != after_window
        recent_switches = 0
        if self.idle_recent_windows:
            sequence = list(self.idle_recent_windows) + [after_window]
            recent_switches = sum(1 for a, b in zip(sequence, sequence[1:]) if a != b)
        window_penalty = (0.15 if window_switch else 0.0) + min(0.22, recent_switches * 0.035)
        if before_window != "no-window" and after_window == "no-window":
            window_penalty += 0.20
        shell_classes = {"progman", "workerw", "shell_traywnd", "shell_secondarytraywnd"}
        if after_window.split("|", 1)[0].lower() in shell_classes:
            window_penalty += 0.35
        if settled_window is not None and settled_window != after_window:
            window_penalty += 0.10

        vx0, vy0, vx1, vy1 = self._screen_bounds()
        diagonal = max(1.0, math.hypot(vx1 - vx0 + 1, vy1 - vy0 + 1))
        cursor_x, cursor_y = before_cursor
        large_click_penalty = 0.0
        pending_point = None
        scroll_penalty = 0.0
        for op in program:
            if op.get("op") == "mouse_abs":
                pending_point = (vx0 + float(op.get("sx", 0.5)) * (vx1 - vx0 + 1), vy0 + float(op.get("sy", 0.5)) * (vy1 - vy0 + 1))
            elif op.get("op") == "mouse_button" and bool(op.get("down", True)) and pending_point is not None:
                travel = math.hypot(pending_point[0] - cursor_x, pending_point[1] - cursor_y) / diagonal
                if travel > 0.34:
                    large_click_penalty += min(0.16, 0.07 + (travel - 0.34) * 0.20)
                cursor_x, cursor_y = pending_point
            elif op.get("op") == "wheel":
                steps = abs(float(op.get("delta", 0))) / 120.0
                if steps > 2.0:
                    scroll_penalty += min(0.18, (steps - 2.0) * 0.045)
        if repetitions and scroll_penalty:
            scroll_penalty *= min(2.0, 1.0 + repetitions * 0.25)

        reward = (novelty * 1.25 + action_diversity * 0.20 + moderate_change * 0.16 + persistence_bonus
                  - no_change_penalty - return_penalty - repetitions * 0.04
                  - window_penalty - large_click_penalty
                  - scroll_penalty - excessive_change_penalty - stale_exploration_penalty - transient_penalty)
        self.idle_recent_states.append((after_hash, after_arr))
        self.idle_recent_actions.append(action)
        self.idle_recent_windows.append(after_window)
        return _clamp(reward, -0.65, 1.0)

    def _learn_idle_program(self, key, program, reward):
        self.state["idle_trials"] = int(self.state.get("idle_trials", 0)) + 1
        ctx = self._idle_ctx(key)
        ctx["trials"] = int(ctx.get("trials", 0)) + 1
        ctx["last_used"] = int(self.state["idle_trials"])
        normalized = self._normalize_idle_program(program)
        self._mark_state_dirty()
        if not normalized:
            self._maybe_save_state()
            return
        fingerprint = self._idle_program_fingerprint(normalized)
        rec = None
        for item in ctx["programs"]:
            if item.get("fingerprint") == fingerprint:
                rec = item
                break
        if rec is None:
            rec = {"fingerprint": fingerprint, "program": json.loads(json.dumps(normalized)), "n": 0,
                   "q": 0.0, "reward_sum": 0.0, "best_reward": -1e9, "last_seen": int(self.state["idle_trials"])}
            ctx["programs"].append(rec)
        rec["n"] = int(rec.get("n", 0)) + 1
        rec["reward_sum"] = float(rec.get("reward_sum", 0.0)) + float(reward)
        rec["last_seen"] = int(self.state["idle_trials"])
        alpha = 1.0 / math.sqrt(rec["n"])
        rec["q"] = float(rec.get("q", 0.0)) + alpha * (float(reward) - float(rec.get("q", 0.0)))
        if float(reward) > float(rec.get("best_reward", -1e9)):
            rec["best_reward"] = float(reward)
            rec["program"] = json.loads(json.dumps(normalized))
        if reward > 0.03:
            memory = self.state.setdefault("idle_memory", [])
            remembered = None
            for item in memory:
                if item.get("context") == key and item.get("fingerprint") == fingerprint:
                    remembered = item
                    break
            if remembered is None:
                remembered = {"context": key, "fingerprint": fingerprint, "program": json.loads(json.dumps(normalized)),
                              "n": 0, "reward_sum": 0.0, "best_reward": -1e9, "last_seen": int(self.state["idle_trials"])}
                memory.append(remembered)
            remembered["n"] = int(remembered.get("n", 0)) + 1
            remembered["reward_sum"] = float(remembered.get("reward_sum", 0.0)) + float(reward)
            remembered["last_seen"] = int(self.state["idle_trials"])
            if float(reward) > float(remembered.get("best_reward", -1e9)):
                remembered["best_reward"] = float(reward)
                remembered["program"] = json.loads(json.dumps(normalized))
        limits = self._storage_limits()
        if len(ctx["programs"]) > max(48, limits["programs"] // 2):
            self._compact_idle_context(ctx, max(48, limits["programs"] // 2))
        if len(self.state.get("idle_memory", [])) > max(64, limits["memory"] // 2):
            self._compact_state()
        self._maybe_save_state()

    def _signed_long(self, value):
        value = int(value)
        if value < -2147483648:
            return -2147483648
        if value > 2147483647:
            return 2147483647
        return value

    def _send_input_failed(self):
        self._transition_control(
            (self.CONTROL_ARMING, self.CONTROL_CONTROLLING, self.CONTROL_STOPPING),
            self.CONTROL_STOPPING, enable_input=False,
        )
        self.stop_event.set()
        self.release_requested.set()
        self.system_stop_reason = "Windows 拒绝了 AI 的鼠标或键盘输入，AI已停止。可重新选择模式。"

    def _raw_mouse_packet(self, dx, dy, data, flags, release=False):
        with self.input_gate_lock:
            if not release and (not self.input_enabled or self.stop_event.is_set()):
                return False
            packet = INPUT()
            packet.type = INPUT_MOUSE
            packet.mi = MOUSEINPUT(self._signed_long(dx), self._signed_long(dy), int(data) & 0xFFFFFFFF, int(flags) & 0xFFFFFFFF, 0, INPUT_TAG)
            if int(user32.SendInput(1, ctypes.byref(packet), ctypes.sizeof(INPUT))) != 1:
                self._send_input_failed()
                return False
            self._track_raw_mouse(int(data), int(flags))
            return True

    def _track_raw_mouse(self, data, flags):
        mapping = (
            ("left", MOUSEEVENTF_LEFTDOWN, MOUSEEVENTF_LEFTUP),
            ("right", MOUSEEVENTF_RIGHTDOWN, MOUSEEVENTF_RIGHTUP),
            ("middle", MOUSEEVENTF_MIDDLEDOWN, MOUSEEVENTF_MIDDLEUP),
        )
        for name, down_flag, up_flag in mapping:
            if flags & down_flag:
                self.held_mouse.add(name)
            if flags & up_flag:
                self.held_mouse.discard(name)
        if flags & MOUSEEVENTF_XDOWN:
            if data & 1:
                self.held_mouse.add("x1")
            if data & 2:
                self.held_mouse.add("x2")
        if flags & MOUSEEVENTF_XUP:
            if data & 1:
                self.held_mouse.discard("x1")
            if data & 2:
                self.held_mouse.discard("x2")

    def _raw_mouse_move_abs(self, x, y):
        vx, vy = virtual_origin()
        vw = max(2, user32.GetSystemMetrics(78))
        vh = max(2, user32.GetSystemMetrics(79))
        nx = max(0, min(65535, int(round((int(x) - vx) * 65535.0 / (vw - 1)))))
        ny = max(0, min(65535, int(round((int(y) - vy) * 65535.0 / (vh - 1)))))
        return self._raw_mouse_packet(nx, ny, 0, MOUSEEVENTF_MOVE | MOUSEEVENTF_ABSOLUTE | MOUSEEVENTF_VIRTUALDESK)

    def _raw_mouse_move_rel(self, dx, dy, no_coalesce=False):
        flags = MOUSEEVENTF_MOVE | (MOUSEEVENTF_MOVE_NOCOALESCE if no_coalesce else 0)
        return self._raw_mouse_packet(dx, dy, 0, flags)

    def _button_packet(self, button, down, release=False):
        mapping = {
            "left": (MOUSEEVENTF_LEFTDOWN, MOUSEEVENTF_LEFTUP, 0),
            "right": (MOUSEEVENTF_RIGHTDOWN, MOUSEEVENTF_RIGHTUP, 0),
            "middle": (MOUSEEVENTF_MIDDLEDOWN, MOUSEEVENTF_MIDDLEUP, 0),
            "x1": (MOUSEEVENTF_XDOWN, MOUSEEVENTF_XUP, 1),
            "x2": (MOUSEEVENTF_XDOWN, MOUSEEVENTF_XUP, 2),
        }
        down_flag, up_flag, data = mapping.get(button, mapping["left"])
        return self._raw_mouse_packet(0, 0, data, down_flag if down else up_flag, release=release)

    def _mouse_button(self, button, down, force=False):
        if self.stop_event.is_set() and down and not force:
            return False
        return self._button_packet(button, down, release=force)

    def _raw_keyboard_packet(self, vk, scan, flags, release=False):
        return self._raw_keyboard_sequence(((vk, scan, flags),), release=release)

    def _raw_keyboard_sequence(self, events, release=False):
        events = tuple(events)
        if not events:
            return True
        offset = 0
        while offset < len(events):
            if not release and self.stop_event.is_set():
                return False
            batch = events[offset:offset + self.MAX_KEY_BATCH]
            with self.input_gate_lock:
                if not release and (not self.input_enabled or self.stop_event.is_set()):
                    return False
                packets = (INPUT * len(batch))()
                normalized_events = []
                for index, (vk, scan, flags) in enumerate(batch):
                    vk = int(vk) & 0xFFFF
                    scan = int(scan) & 0xFFFF
                    flags = int(flags) & 0xFFFFFFFF
                    packets[index].type = INPUT_KEYBOARD
                    packets[index].ki = KEYBDINPUT(vk, scan, flags, 0, INPUT_TAG)
                    normalized_events.append((vk, scan, flags))
                sent = int(user32.SendInput(len(batch), packets, ctypes.sizeof(INPUT)))
                for vk, scan, flags in normalized_events[:max(0, min(sent, len(normalized_events)))]:
                    self._track_raw_keyboard(vk, scan, flags)
                if sent != len(batch):
                    self._send_input_failed()
                    return False
            offset += len(batch)
            if offset < len(events) and not release and self.stop_event.is_set():
                return False
        return True

    def _track_raw_keyboard(self, vk, scan, flags):
        extended = bool(flags & KEYEVENTF_EXTENDEDKEY)
        if flags & KEYEVENTF_UNICODE:
            identity = ("unicode", int(scan) & 0xFFFF, extended)
        elif flags & KEYEVENTF_SCANCODE:
            identity = ("scan", int(scan) & 0xFFFF, extended)
        else:
            identity = ("vk", int(vk) & 0xFFFF, extended)
        if flags & KEYEVENTF_KEYUP:
            self.held_keys.discard(identity)
        else:
            self.held_keys.add(identity)

    def _key_event(self, mode, code, down, extended=False, force=False):
        if self.stop_event.is_set() and down and not force:
            return False
        flags = (KEYEVENTF_EXTENDEDKEY if extended else 0) | (0 if down else KEYEVENTF_KEYUP)
        if mode == "scan":
            flags |= KEYEVENTF_SCANCODE
            return self._raw_keyboard_packet(0, code, flags, release=force)
        return self._raw_keyboard_packet(code, 0, flags, release=force)

    def _unicode_unit(self, unit, down, force=False):
        if self.stop_event.is_set() and down and not force:
            return False
        flags = KEYEVENTF_UNICODE | (0 if down else KEYEVENTF_KEYUP)
        return self._raw_keyboard_packet(0, unit, flags, release=force)

    def _mouse_move_abs(self, x, y, duration=0.0):
        if self.stop_event.is_set():
            return False
        vx0, vy0, vx1, vy1 = self._screen_bounds()
        x = max(vx0, min(vx1, int(x)))
        y = max(vy0, min(vy1, int(y)))
        sx, sy = self._cursor_pos()
        dx, dy = x - sx, y - sy
        duration = min(max(0.0, float(duration)), self.MAX_MOVE_SECONDS)
        if duration == 0.0:
            return self._raw_mouse_move_abs(x, y)
        dist = math.hypot(dx, dy)
        steps = max(1, int(math.ceil(duration * 90.0)), int(math.ceil(dist / 18.0)))
        pause = duration / steps
        nx, ny = (-dy / max(dist, 1.0), dx / max(dist, 1.0))
        curve = random.gauss(0.0, 0.045) * min(dist, 220.0)
        for i in range(1, steps + 1):
            if self.stop_event.is_set():
                return False
            t = i / steps
            ease = 3 * t * t - 2 * t * t * t
            bend = math.sin(math.pi * t) * curve
            if not self._raw_mouse_move_abs(int(round(sx + dx * ease + nx * bend)), int(round(sy + dy * ease + ny * bend))):
                return False
            if pause > 0 and self.stop_event.wait(pause):
                return False
        return True

    def _mouse_move_rel(self, dx, dy, duration=0.0, no_coalesce=False):
        if self.stop_event.is_set():
            return False
        dx, dy = self._signed_long(dx), self._signed_long(dy)
        duration = min(max(0.0, float(duration)), self.MAX_MOVE_SECONDS)
        if duration == 0.0:
            return self._raw_mouse_move_rel(dx, dy, no_coalesce)
        steps = max(1, int(math.ceil(duration * 90.0)), int(math.ceil(max(abs(dx), abs(dy)) / 18.0)))
        pause = duration / steps
        sent_x = sent_y = 0
        for i in range(1, steps + 1):
            if self.stop_event.is_set():
                return False
            target_x = int(round(dx * i / steps))
            target_y = int(round(dy * i / steps))
            if not self._raw_mouse_move_rel(target_x - sent_x, target_y - sent_y, no_coalesce):
                return False
            sent_x, sent_y = target_x, target_y
            if pause > 0 and self.stop_event.wait(pause):
                return False
        return True

    def _wheel(self, delta, horizontal=False):
        if self.stop_event.is_set():
            return False
        delta = int(_clamp(int(delta), -self.MAX_WHEEL_DELTA, self.MAX_WHEEL_DELTA))
        if delta == 0:
            return False
        return self._raw_mouse_packet(0, 0, delta, MOUSEEVENTF_HWHEEL if horizontal else MOUSEEVENTF_WHEEL)

    def _type_text(self, text, interval=0.0):
        units = str(text).encode("utf-16-le")
        if not units or len(units) // 2 > self.MAX_TEXT_UNITS:
            return False
        interval = min(max(0.0, float(interval)), self.MAX_TEXT_INTERVAL)
        for i in range(0, len(units), 2):
            if self.stop_event.is_set():
                return False
            unit = units[i] | (units[i + 1] << 8)
            if not self._raw_keyboard_sequence(((0, unit, KEYEVENTF_UNICODE), (0, unit, KEYEVENTF_UNICODE | KEYEVENTF_KEYUP))):
                return False
            if interval > 0 and self.stop_event.wait(interval):
                return False
        return True

    def _release_all_inputs(self):
        release_error = None
        with self.physical_state_lock:
            physical_buttons = set(self.physical_buttons_down)
            physical_keys = set(self.physical_keys_down)
        for button in list(self.held_mouse):
            try:
                if button in physical_buttons:
                    _log_runtime("info", f"input ownership transferred to user for mouse button: {button}")
                else:
                    self._mouse_button(button, False, force=True)
            except Exception as exc:
                release_error = release_error or exc
            finally:
                self.held_mouse.discard(button)
        for mode, code, extended in list(self.held_keys):
            try:
                identity = (mode, code, extended)
                if mode != "unicode" and identity in physical_keys:
                    _log_runtime("info", f"input ownership transferred to user for key: {mode}:{code}:{int(extended)}")
                elif mode == "unicode":
                    self._unicode_unit(code, False, force=True)
                else:
                    self._key_event(mode, code, False, extended=extended, force=True)
            except Exception as exc:
                release_error = release_error or exc
            finally:
                self.held_keys.discard((mode, code, extended))
        if release_error is not None:
            _log_exception("input release", release_error)
            self._transition_control(
                (self.CONTROL_ARMING, self.CONTROL_CONTROLLING, self.CONTROL_STOPPING),
                self.CONTROL_STOPPING, enable_input=False,
            )
            self.stop_event.set()
            if self.system_stop_reason is None:
                self.system_stop_reason = f"释放鼠标或键盘状态时出错：{release_error}。AI已停止。"

    def _uia_fallback_launch_allowed(self, kind, cooldown):
        root_hwnd = int((self.target_identity or {}).get("root_hwnd", 0) or 0)
        if not root_hwnd:
            return False
        key = (str(kind), root_hwnd)
        now = time.monotonic()
        if now - float(self.uia_fallback_last.get(key, -1e9)) < max(0.0, float(cooldown)):
            return False
        self.uia_fallback_last[key] = now
        if len(self.uia_fallback_last) > 48:
            cutoff = now - 120.0
            self.uia_fallback_last = {item_key: stamp for item_key, stamp in self.uia_fallback_last.items() if float(stamp) >= cutoff}
        return True

    def _uia_value_near_target(self, cooldown_kind="value", cooldown=12.0):
        if self.target is None or self.stop_event.is_set():
            return None
        x0, y0, x1, y1 = self.target["box"]
        cx = int(round((x0 + x1) / 2.0)); cy = int(round((y0 + y1) / 2.0))
        root_hwnd, _rect, _dpi = self._target_window_info(self.target)
        selected_root = int((self.target_identity or {}).get("root_hwnd", 0) or 0)
        if not root_hwnd or not selected_root or int(root_hwnd) != selected_root:
            return None
        powershell = Path(os.environ.get("SystemRoot", r"C:\\Windows")) / "System32" / "WindowsPowerShell" / "v1.0" / "powershell.exe"
        if not powershell.exists() or not self._uia_fallback_launch_allowed(cooldown_kind, cooldown):
            return None
        root_value = int(selected_root)
        ocr_width = max(1.0, float(x1 - x0)); ocr_height = max(1.0, float(y1 - y0)); ocr_area = ocr_width * ocr_height
        script = f"""$ErrorActionPreference='Stop';
Add-Type -AssemblyName UIAutomationClient; Add-Type -AssemblyName UIAutomationTypes; Add-Type -AssemblyName WindowsBase;
$p=New-Object System.Windows.Point({cx},{cy}); $e=[System.Windows.Automation.AutomationElement]::FromPoint($p);
if($null -eq $e){{exit 2}}; $walker=[System.Windows.Automation.TreeWalker]::ControlViewWalker;
for($i=0;$i -lt 4 -and $null -ne $e;$i++){{
  try{{
    $vp=$e.GetCurrentPattern([System.Windows.Automation.ValuePattern]::Pattern); $r=$e.Current.BoundingRectangle;
    $ix=[Math]::Max(0.0,[Math]::Min($r.Right,{float(x1)})-[Math]::Max($r.Left,{float(x0)}));
    $iy=[Math]::Max(0.0,[Math]::Min($r.Bottom,{float(y1)})-[Math]::Max($r.Top,{float(y0)}));
    $overlap=($ix*$iy)/{ocr_area}; $rootOK=$false; $a=$e;
    for($j=0;$j -lt 32 -and $null -ne $a;$j++){{if([int64]$a.Current.NativeWindowHandle -eq {root_value}){{$rootOK=$true;break}};$a=$walker.GetParent($a)}};
    if($overlap -ge 0.70 -and $rootOK){{[pscustomobject]@{{value=$vp.Current.Value}}|ConvertTo-Json -Compress;exit 0}}
  }}catch{{}}; $e=$walker.GetParent($e)
}}; exit 2"""
        result = run_child(
            [str(powershell), "-NoLogo", "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass", "-Command", script],
            cwd=str(app_dir), env=os.environ.copy(), stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
            text=True, timeout=2.5, cancel_event=self.stop_event,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
        if result is None or result.returncode != 0 or not str(result.stdout).strip():
            return None
        try:
            payload = json.loads(str(result.stdout).strip().splitlines()[-1])
            return str(payload.get("value", "")).strip() if isinstance(payload, dict) else None
        except Exception:
            return None

    def _uia_set_value_near_target(self, text):
        # ValuePattern cannot perform a partial writable text-range replacement.
        # This fallback therefore uses SetValue only when the complete ValuePattern
        # value itself parses as the selected number; mixed-content fields are rejected.
        if self.target is None or self.current_value is None or self.stop_event.is_set():
            return False
        x0, y0, x1, y1 = self.target["box"]
        cx = int(round((x0 + x1) / 2.0))
        cy = int(round((y0 + y1) / 2.0))
        root_hwnd, _rect, _dpi = self._target_window_info(self.target)
        selected_root = int((self.target_identity or {}).get("root_hwnd", 0) or 0)
        if not root_hwnd or not selected_root or int(root_hwnd) != selected_root:
            return False
        root_hwnd = selected_root
        current_decimal = _as_decimal(self.current_value)
        if not current_decimal.is_finite() or abs(current_decimal).adjusted() > 300:
            return False
        try:
            _value, quantum = _observation_value_and_quantum(self.target)
        except Exception:
            quantum = abs(_decimal_quantum(current_decimal))
        expected_current = _format_number(current_decimal)
        tolerance = max(abs(quantum) * Decimal("0.25"), abs(current_decimal) * Decimal("1e-12"), Decimal("1e-12"))
        powershell = Path(os.environ.get("SystemRoot", r"C:\\Windows")) / "System32" / "WindowsPowerShell" / "v1.0" / "powershell.exe"
        if not powershell.exists() or not self._uia_fallback_launch_allowed("set", 5.0):
            return False
        safe_text = str(text).replace("'", "''")
        safe_current = expected_current.replace("'", "''")
        safe_tolerance = _format_number(tolerance).replace("'", "''")
        root_value = int(root_hwnd)
        ocr_width = max(1.0, float(x1 - x0))
        ocr_height = max(1.0, float(y1 - y0))
        ocr_area = ocr_width * ocr_height
        script = f'''$ErrorActionPreference='Stop';
Add-Type -AssemblyName UIAutomationClient; Add-Type -AssemblyName UIAutomationTypes; Add-Type -AssemblyName WindowsBase;
$styles=[Globalization.NumberStyles]::Float -bor [Globalization.NumberStyles]::AllowThousands -bor [Globalization.NumberStyles]::AllowParentheses;
$expected=[double]::Parse('{safe_current}',[Globalization.CultureInfo]::InvariantCulture);
$tol=[double]::Parse('{safe_tolerance}',[Globalization.CultureInfo]::InvariantCulture);
$p=New-Object System.Windows.Point({cx},{cy}); $e=[System.Windows.Automation.AutomationElement]::FromPoint($p);
if($null -eq $e){{exit 2}}; $walker=[System.Windows.Automation.TreeWalker]::ControlViewWalker;
for($i=0;$i -lt 4 -and $null -ne $e;$i++){{
  try{{
    $vp=$e.GetCurrentPattern([System.Windows.Automation.ValuePattern]::Pattern);
    if(-not $vp.Current.IsReadOnly){{
      $r=$e.Current.BoundingRectangle;
      $ix=[Math]::Max(0.0,[Math]::Min($r.Right,{float(x1)})-[Math]::Max($r.Left,{float(x0)}));
      $iy=[Math]::Max(0.0,[Math]::Min($r.Bottom,{float(y1)})-[Math]::Max($r.Top,{float(y0)}));
      $overlap=($ix*$iy)/{ocr_area};
      $heightRatio=$r.Height/{ocr_height};
      $areaRatio=($r.Width*$r.Height)/{ocr_area};
      $rootOK=$false; $a=$e;
      for($j=0;$j -lt 32 -and $null -ne $a;$j++){{
        if([int64]$a.Current.NativeWindowHandle -eq {root_value}){{$rootOK=$true;break}};
        $a=$walker.GetParent($a)
      }};
      $current=0.0; $parsed=[double]::TryParse($vp.Current.Value,$styles,[Globalization.CultureInfo]::CurrentCulture,[ref]$current);
      if(-not $parsed){{$parsed=[double]::TryParse($vp.Current.Value,$styles,[Globalization.CultureInfo]::InvariantCulture,[ref]$current)}};
      if($overlap -ge 0.70 -and $heightRatio -le 4.5 -and $areaRatio -le 120.0 -and $rootOK -and $parsed -and [Math]::Abs($current-$expected) -le $tol){{
        $vp.SetValue('{safe_text}');exit 0
      }}
    }}
  }}catch{{}};
  $e=$walker.GetParent($e)
}}; exit 2'''
        result = run_child(
            [str(powershell), "-NoLogo", "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass", "-Command", script],
            cwd=str(app_dir), env=os.environ.copy(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            timeout=2.5, cancel_event=self.stop_event,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
        return result is not None and result.returncode == 0

    def _replace_number(self, delta):
        if self.current_value is None or self.target is None:
            raise RuntimeError("当前数字或目标位置不可用，无法执行参数化替换")
        delta_value = abs(_as_decimal(delta))
        if delta_value <= 0:
            raise ValueError("replace_number 的 delta 必须是有限正数")
        try:
            _display_value, display_quantum = _observation_value_and_quantum(self.target)
            delta_value = max(delta_value, display_quantum)
        except Exception:
            pass
        next_value = _as_decimal(self.current_value) + delta_value
        if not next_value.is_finite():
            raise OverflowError("参数化替换结果不是有限数字")
        expected_text = _format_number_like_observation(next_value, self.target)
        if len(expected_text.encode("utf-16-le")) // 2 > self.MAX_TEXT_UNITS:
            self.last_replace_attempt = None
            return self.ACTION_NOT_APPLICABLE
        # Native Edit/RichEdit replaces only the unique numeric span. UIA uses
        # whole-value SetValue only when the entire semantic value is proven to be
        # the selected number. If neither proof is available, do not edit visually.
        if self._native_set_value_near_target(expected_text) or self._uia_set_value_near_target(expected_text):
            key = self._context_key(self.target)
            ctx = self._ctx(key)
            ctx["replace_not_applicable"] = 0
            self.last_replace_attempt = {"expected": next_value, "text": expected_text}
            return self.ACTION_SUCCESS
        self.last_replace_attempt = None
        return self.ACTION_NOT_APPLICABLE

    def _target_absolute_point(self, op):
        if self.target is None:
            raise RuntimeError("目标坐标不可用")
        x0, y0, x1, y1 = self.target["box"]
        h = max(1.0, y1 - y0)
        cx = (x0 + x1) / 2.0
        cy = (y0 + y1) / 2.0
        return int(round(cx + float(op["rx"]) * h)), int(round(cy + float(op["ry"]) * h))


    def _screen_absolute_point(self, op):
        vx0, vy0, vx1, vy1 = self._screen_bounds()
        width = max(1.0, float(vx1 - vx0))
        height = max(1.0, float(vy1 - vy0))
        return int(round(vx0 + float(op["sx"]) * width)), int(round(vy0 + float(op["sy"]) * height))


    def _perform_program(self, program):
        space = "target" if self.mode == "grow" else "screen"
        normalized = self._normalize_program(program, space=space)
        if not normalized:
            return self.ACTION_FAILED
        completed = True
        skipped_idle_buttons = set()
        try:
            index = 0
            while index < len(normalized):
                if self.stop_event.is_set():
                    completed = False
                    break
                op = normalized[index]
                kind = op.get("op")
                ok = True
                if kind == "key_event":
                    block = []
                    idle_key_block_safe = True
                    while index < len(normalized) and normalized[index].get("op") == "key_event":
                        item = normalized[index]
                        if space == "screen" and bool(item.get("down", True)) and not self._idle_key_is_safe(item.get("code", 0)):
                            idle_key_block_safe = False
                        flags = (KEYEVENTF_EXTENDEDKEY if bool(item.get("extended", False)) else 0)
                        if not bool(item.get("down", True)):
                            flags |= KEYEVENTF_KEYUP
                        if str(item.get("mode", "vk")) == "scan":
                            flags |= KEYEVENTF_SCANCODE
                            block.append((0, int(item.get("code", 0)), flags))
                        else:
                            block.append((int(item.get("code", 0)), 0, flags))
                        index += 1
                    ok = True if (space == "screen" and not idle_key_block_safe) else self._raw_keyboard_sequence(block)
                    if ok is False:
                        completed = False
                        break
                    continue
                if kind == "mouse_abs":
                    x, y = self._target_absolute_point(op) if space == "target" else self._screen_absolute_point(op)
                    ok = self._mouse_move_abs(x, y, op.get("duration", 0.0))
                elif kind == "mouse_rel":
                    if space == "target":
                        if self.target is None:
                            ok = False
                        else:
                            h = max(1.0, self.target["box"][3] - self.target["box"][1])
                            dx = int(round(float(op["rdx"]) * h))
                            dy = int(round(float(op["rdy"]) * h))
                            ok = self._mouse_move_rel(dx, dy, op.get("duration", 0.0), bool(op.get("no_coalesce", False)))
                    else:
                        vx0, vy0, vx1, vy1 = self._screen_bounds()
                        dx = int(round(float(op["sdx"]) * max(1, vx1 - vx0 + 1)))
                        dy = int(round(float(op["sdy"]) * max(1, vy1 - vy0 + 1)))
                        ok = self._mouse_move_rel(dx, dy, op.get("duration", 0.0), bool(op.get("no_coalesce", False)))
                elif kind == "mouse_button":
                    button = op.get("button", "left")
                    down = bool(op.get("down", True))
                    if space == "screen" and down and not self._idle_click_is_safe(*self._cursor_pos()):
                        skipped_idle_buttons.add(button)
                        ok = True
                    elif space == "screen" and not down and button in skipped_idle_buttons:
                        skipped_idle_buttons.discard(button)
                        ok = True
                    else:
                        ok = self._mouse_button(button, down)
                elif kind == "wheel":
                    if space == "screen" and not self._idle_point_is_safe(*self._cursor_pos()):
                        ok = True
                    else:
                        ok = self._wheel(op.get("delta", 120), bool(op.get("horizontal", False)))
                elif kind == "unicode_text":
                    ok = self._type_text(op.get("text", ""), op.get("interval", 0.0))
                elif kind == "replace_number":
                    replace_result = self._replace_number(op.get("delta", 1.0))
                    if replace_result == self.ACTION_NOT_APPLICABLE:
                        return self.ACTION_NOT_APPLICABLE
                    ok = replace_result == self.ACTION_SUCCESS
                elif kind == "wait" and self.stop_event.wait(max(0.0, float(op.get("seconds", 0.0)))):
                    ok = False
                if ok is False:
                    completed = False
                    break
                index += 1
            return self.ACTION_SUCCESS if completed and not self.stop_event.is_set() else self.ACTION_FAILED
        finally:
            self._release_all_inputs()

    def _detect_target_region(self, image, origin, window_scope=False):
        if self.target is None:
            return None
        if window_scope:
            gx0, gy0, gx1, gy1 = self._window_bounds_for_target(self.target)
        else:
            x0, y0, x1, y1 = self.target["box"]
            h = max(6, y1 - y0)
            margin_x = max(int(h * 8.0), x1 - x0)
            margin_y = int(h * 5.0)
            gx0, gy0, gx1, gy1 = x0 - margin_x, y0 - margin_y, x1 + margin_x, y1 + margin_y
        ix0 = max(0, int(gx0 - origin[0])); iy0 = max(0, int(gy0 - origin[1]))
        ix1 = min(image.width, int(gx1 - origin[0] + 1)); iy1 = min(image.height, int(gy1 - origin[1] + 1))
        if ix1 - ix0 < 6 or iy1 - iy0 < 6:
            return None
        crop = image.crop((ix0, iy0, ix1, iy1))
        crop_origin = (origin[0] + ix0, origin[1] + iy0)
        numbers = detect_multiscale_image(crop, crop_origin, scales=(1.0,), stop_event=self.stop_event)
        return self._match_target(numbers, crop, crop_origin, wide=window_scope)

    def _reacquire_target(self, bounded_rounds=None):
        rounds = 0
        while app_alive.is_set() and not shutdown_event.is_set() and not self.stop_event.is_set() and self.target is not None:
            image, origin = capture_screen()
            numbers = detect_multiscale_image(image, origin, scales=(1.0, 0.84, 1.18), stop_event=self.stop_event)
            observed = self._match_target(numbers, image, origin, wide=True)
            if observed is not None:
                self.target = dict(observed)
                self.current_value = observed["value"]
                self._ensure_identity_context(image, origin)
                return observed
            rounds += 1
            if bounded_rounds is not None and rounds >= bounded_rounds:
                return None
            if self.stop_event.wait(min(0.45, 0.12 + rounds * 0.03)):
                return None
        return None

    def start(self, mode="grow"):
        if _shutdown_requested() or mode not in ("grow", "free") or not self.input_hooks_ready.is_set():
            return False
        expected_state = self.CONTROL_ARMING if mode == "grow" else self.CONTROL_READY
        with self.input_gate_lock:
            if self.control_state != expected_state or self.running:
                return False
            if mode == "grow":
                if not self.arming or self.target is None or self.original_target is None:
                    return False
                if self.user_interrupt_event.is_set() or self.stop_event.is_set():
                    return False
            else:
                self.user_interrupt_event.clear()
                self.stop_event.clear()
            self.release_requested.clear()
            self.release_ui_requested.clear()
            self.system_stop_reason = None
            self.user_interrupt_pending = False
            self.mode = mode
        if not self._transition_control(
            expected_state, self.CONTROL_CONTROLLING, enable_input=True, running=True, arming=False,
            ignore_selection_lbutton_up=self.ignore_selection_lbutton_up,
        ):
            return False
        root.withdraw()
        loop = self._agent_loop if mode == "grow" else self._idle_agent_loop
        thread = threading.Thread(target=loop, name=f"MakeItBiggerAgent-{mode}", daemon=True)
        with self.lock:
            self.agent_thread = thread
        thread.start()
        return True

    def _estimate_natural_motion(self, force=False):
        ident = self.target_identity or {}
        if not bool(ident.get("dynamic", False)) or self.target is None:
            return True
        now = time.monotonic()
        if not force and now - float(ident.get("natural_last_calibration", 0.0) or 0.0) < 18.0:
            return True
        points = [(now, _as_decimal(self.current_value))]
        for _ in range(3):
            if self.stop_event.wait(0.16):
                return False
            image, origin = capture_screen()
            observed = self._detect_target_region(image, origin, window_scope=False)
            if observed is None:
                observed = self._detect_target_region(image, origin, window_scope=True)
            if observed is None:
                return False
            self.target = dict(observed)
            self.current_value = observed["value"]
            points.append((time.monotonic(), _as_decimal(observed["value"])))
        slopes = []
        for (t0, v0), (t1, v1) in zip(points, points[1:]):
            dt = max(1e-6, t1 - t0)
            slopes.append((v1 - v0) / Decimal(str(dt)))
        if not slopes:
            return True
        ordered = sorted(slopes)
        rate = ordered[len(ordered) // 2]
        deviations = sorted(abs(value - rate) for value in slopes)
        noise_rate = deviations[len(deviations) // 2] if deviations else Decimal(0)
        ident["natural_rate"] = str(rate)
        ident["natural_noise_rate"] = str(noise_rate)
        ident["natural_last_calibration"] = time.monotonic()
        self.target_identity = ident
        return True

    def _reward_for(self, before_value, observed_value, elapsed=0.0):
        baseline = _as_decimal(self.original_target["value"])
        before = _as_decimal(before_value)
        observed = _as_decimal(observed_value)
        ident = self.target_identity or {}
        dynamic = bool(ident.get("dynamic", False))
        if dynamic:
            try:
                rate = _as_decimal(ident.get("natural_rate", "0"))
                noise_rate = abs(_as_decimal(ident.get("natural_noise_rate", "0")))
            except Exception:
                rate = Decimal(0)
                noise_rate = Decimal(0)
            elapsed_decimal = Decimal(str(max(0.0, float(elapsed))))
            expected_natural_gain = rate * elapsed_decimal
            observed_gain = observed - before
            adjusted_gain = observed_gain - expected_natural_gain
            try:
                _value, quantum = _observation_value_and_quantum(self.target or self.original_target)
            except Exception:
                quantum = abs(_decimal_quantum(observed))
            tolerance = max(abs(quantum) * Decimal("0.5"), noise_rate * elapsed_decimal * Decimal("1.75"))
            effective_gain = adjusted_gain - tolerance
            if effective_gain > 0:
                step_gain = _decimal_to_learning_float(effective_gain)
                self.state["best_gain"] = max(float(self.state.get("best_gain", 0.0)), step_gain)
                reward = 0.55 + min(1.45, math.log1p(step_gain) * 0.38)
                return reward, step_gain
            if adjusted_gain >= -tolerance:
                return -0.06, 0.0
            loss = _decimal_to_learning_float(abs(adjusted_gain) - tolerance)
            return -min(1.10, 0.34 + math.log1p(loss) * 0.12), 0.0
        absolute_gain_decimal = max(Decimal(0), observed - baseline)
        step_gain_decimal = max(Decimal(0), observed - before)
        absolute_gain = _decimal_to_learning_float(absolute_gain_decimal)
        step_gain = _decimal_to_learning_float(step_gain_decimal)
        self.state["best_gain"] = max(float(self.state.get("best_gain", 0.0)), absolute_gain)
        if step_gain_decimal > 0:
            if before <= baseline < observed:
                reward = 1.0 + min(1.8, math.log1p(step_gain) * 0.45)
            else:
                reward = 0.45 + min(1.2, math.log1p(step_gain) * 0.35)
            return reward, step_gain
        if observed == before:
            return (-0.04 if observed > baseline else -0.18), 0.0
        if observed > baseline:
            return -0.55, 0.0
        deficit = _decimal_to_learning_float(baseline - observed)
        return -min(1.25, 0.72 + math.log1p(deficit) * 0.12), 0.0

    def _record_unknown_observation(self, key):
        self.state["unknowns"] = int(self.state.get("unknowns", 0)) + 1
        ctx = self._ctx(key)
        ctx["unknowns"] = int(ctx.get("unknowns", 0)) + 1
        self.state_dirty = True
        self._maybe_save_state()

    def _confirm_changed_observation(self, first, before_value=None):
        dynamic_target = bool((self.target_identity or {}).get("dynamic", False))

        def mean_char_conf(observation):
            chars = observation.get("chars") if isinstance(observation, dict) else None
            if not isinstance(chars, list) or not chars:
                return float(observation.get("conf", 0.0)) if isinstance(observation, dict) else 0.0
            return sum(float(item.get("conf", 0.0)) for item in chars) / float(len(chars))

        def agree(a, b):
            if a is None or b is None:
                return False
            if float(a.get("conf", 0.0)) < 0.72 or float(b.get("conf", 0.0)) < 0.72:
                return False
            if mean_char_conf(a) < 0.68 or mean_char_conf(b) < 0.68:
                return False
            a_window = self._window_signature(a)
            b_window = self._window_signature(b)
            expected_window = (self.target_identity or {}).get("window")
            if expected_window and (a_window != expected_window or b_window != expected_window):
                return False
            if a_window != b_window:
                return False
            if recognizer._iou(a["box"], b["box"]) < 0.42:
                return False
            if dynamic_target:
                return True
            return _same_ocr_number(a, b)

        if first is None or float(first.get("conf", 0.0)) < 0.72:
            return None
        if self.stop_event.wait(0.12):
            return None
        image, origin = capture_screen()
        second = self._detect_target_region(image, origin, window_scope=False)
        if second is None:
            second = self._detect_target_region(image, origin, window_scope=True)
        if not agree(first, second):
            return None

        stored_context = (self.target_identity or {}).get("context")
        if stored_context is not None:
            desc = self._context_descriptor(image, origin, second["box"])
            if desc is None:
                return None
            a = np.asarray(stored_context, dtype=np.float32)
            d = np.asarray(desc, dtype=np.float32)
            if float(np.mean((a - d) ** 2)) > 0.11:
                return None

        high_risk = False
        if before_value is not None:
            try:
                before_decimal = _as_decimal(before_value)
                after_decimal = _as_decimal(second.get("value"))
                positive_gain = after_decimal - before_decimal
                if positive_gain > 0:
                    denominator = max(Decimal(1), abs(before_decimal))
                    relative_gain = positive_gain / denominator
                    high_risk = int(self.state.get("successes", 0)) == 0 or relative_gain >= Decimal("5")
            except (InvalidOperation, TypeError, ValueError, OverflowError):
                high_risk = True

        confirmation_image = image
        confirmation_origin = origin
        confirmed = second
        if high_risk:
            if self.stop_event.wait(0.14):
                return None
            third_image, third_origin = capture_screen()
            third = self._detect_target_region(third_image, third_origin, window_scope=False)
            if third is None:
                third = self._detect_target_region(third_image, third_origin, window_scope=True)
            if not agree(second, third) or not agree(first, third):
                return None
            if stored_context is not None:
                desc = self._context_descriptor(third_image, third_origin, third["box"])
                if desc is None:
                    return None
                a = np.asarray(stored_context, dtype=np.float32)
                d = np.asarray(desc, dtype=np.float32)
                if float(np.mean((a - d) ** 2)) > 0.11:
                    return None
            confirmed = third
            confirmation_image = third_image
            confirmation_origin = third_origin
            confirmed = dict(confirmed)
            confirmed["pending_policy_confirmation"] = True

        attempt = self.last_replace_attempt
        if attempt is not None:
            expected = attempt.get("expected")
            if expected is not None and _same_number(first.get("value"), expected) and _same_number(confirmed.get("value"), expected):
                expected_text = str(attempt.get("text", ""))
                if float(first.get("conf", 0.0)) >= 0.86 and float(confirmed.get("conf", 0.0)) >= 0.86:
                    semantic_text = self._native_value_near_target()
                    if not semantic_text:
                        semantic_text = self._uia_value_near_target()
                    uia_truth = False
                    if semantic_text:
                        try:
                            uia_truth = any(_same_number(candidate, expected) for candidate in recognizer._parse_number_candidates(semantic_text))
                        except Exception:
                            uia_truth = False
                    if uia_truth:
                        recognizer.observe_verified_number(
                            confirmation_image, confirmation_origin, confirmed, expected_text,
                            source="semantic_truth", cancel_event=self.stop_event,
                        )
                    else:
                        third_obs = confirmed if confirmed is not second else None
                        third_image = confirmation_image if third_obs is not None else None
                        third_origin = confirmation_origin if third_obs is not None else None
                        if third_obs is None and not self.stop_event.wait(0.10):
                            third_image, third_origin = capture_screen()
                            third_obs = self._detect_target_region(third_image, third_origin, window_scope=False)
                            if third_obs is None:
                                third_obs = self._detect_target_region(third_image, third_origin, window_scope=True)
                        if (third_obs is not None and agree(second, third_obs) and agree(first, third_obs)
                                and _same_number(third_obs.get("value"), expected)
                                and float(third_obs.get("conf", 0.0)) >= 0.86
                                and recognizer.verified_variant_consensus(third_image, third_origin, third_obs, expected_text)):
                            recognizer.observe_verified_number(
                                third_image, third_origin, third_obs, expected_text,
                                source="multiview_consensus", cancel_event=self.stop_event,
                            )
        return confirmed

    def _agent_loop(self):
        runtime_error = False
        exit_reason = "AI已停止。可重新选择模式。"
        try:
            self.stop_event.wait(0.22)
            while app_alive.is_set() and not shutdown_event.is_set() and not self.stop_event.is_set() and self.target is not None:
                image, origin = capture_screen()
                refreshed = self._detect_target_region(image, origin, window_scope=False)
                if refreshed is None:
                    refreshed = self._detect_target_region(image, origin, window_scope=True)
                if refreshed is None:
                    refreshed = self._reacquire_target(bounded_rounds=12)
                    if refreshed is None:
                        if self.stop_event.is_set():
                            break
                        self._clear_target_tracking()
                        exit_reason = "目标数字已无法重新识别，AI已停止。可重新选择模式。"
                        break
                    image, origin = capture_screen()
                self.target = dict(refreshed)
                self._ensure_identity_context(image, origin)
                self.current_value = refreshed["value"]
                if bool(refreshed.get("dynamic", False)) and self.target_identity is not None:
                    self.target_identity["dynamic"] = True
                if bool((self.target_identity or {}).get("dynamic", False)):
                    self._estimate_natural_motion(force=float((self.target_identity or {}).get("natural_last_calibration", 0.0) or 0.0) <= 0.0)
                    if self.stop_event.is_set():
                        break
                target = dict(self.target)
                before_value = self.current_value
                key = self._context_key(target)
                program, role = self._pick_program(key, target)
                action_started = time.monotonic()
                action_result = self._perform_program(program)
                if action_result == self.ACTION_NOT_APPLICABLE:
                    ctx = self._ctx(key)
                    ctx["replace_not_applicable"] = int(ctx.get("replace_not_applicable", 0)) + 1
                    self.last_replace_attempt = None
                    self.state_dirty = True
                    self._maybe_save_state()
                    if self.stop_event.wait(0.08):
                        break
                    continue
                if action_result != self.ACTION_SUCCESS:
                    if self.system_stop_reason:
                        exit_reason = self.system_stop_reason
                    break
                if self.stop_event.is_set() or self.stop_event.wait(random.uniform(0.28, 0.72)):
                    if self.system_stop_reason:
                        exit_reason = self.system_stop_reason
                    break
                image, origin = capture_screen()
                observed = self._detect_target_region(image, origin, window_scope=False)
                if observed is None:
                    observed = self._detect_target_region(image, origin, window_scope=True)
                if observed is None:
                    observed = self._reacquire_target(bounded_rounds=3)
                if observed is None:
                    if self.stop_event.is_set():
                        break
                    self._learn_program(key, program, -0.34, 0.0, role)
                    observed = self._reacquire_target(bounded_rounds=12)
                    if observed is None:
                        if self.stop_event.is_set():
                            break
                        self._clear_target_tracking()
                        exit_reason = "目标数字已无法重新识别，AI已停止。可重新选择模式。"
                        break
                    self.target = dict(observed)
                    self.current_value = observed["value"]
                    continue
                self.target = dict(observed)
                observed_value = observed["value"]
                changed = not _same_ocr_number(target, observed)
                if changed:
                    confirmed = self._confirm_changed_observation(observed, before_value=before_value)
                    if confirmed is None:
                        self.target = dict(target)
                        self.current_value = before_value
                        self._record_unknown_observation(key)
                        _log_runtime("warning", "changed OCR observation was not confirmed; learning result marked unknown")
                        continue
                    observed = confirmed
                    self.target = dict(confirmed)
                    observed_value = confirmed["value"]
                self.last_replace_attempt = None
                reward, step_gain = self._reward_for(before_value, observed_value, elapsed=time.monotonic() - action_started)
                self.current_value = observed_value
                self._learn_program(
                    key, program, reward, step_gain, role,
                    promotion_guard=bool(observed.get("pending_policy_confirmation", False)),
                )
        except Exception as exc:
            runtime_error = True
            exit_reason = self.handle_runtime_error(exc, "AI控制/识别/学习过程")
        finally:
            self._transition_control(
                (self.CONTROL_CONTROLLING, self.CONTROL_STOPPING), self.CONTROL_STOPPING,
                enable_input=False, running=False, arming=False, ignore_selection_lbutton_up=False,
            )
            self._release_all_inputs()
            hook_failed = self.hook_callback_error_event.is_set()
            if hook_failed:
                self.system_stop_reason = "用户输入监听回调出错。AI已停止。可重新选择模式。"
                _log_runtime("error", "low-level input hook callback failed")
            with self.lock:
                user_interrupted = self.user_interrupt_event.is_set() and not hook_failed
                self.user_interrupt_pending = bool(user_interrupted)
                self.mode = None
            if self.system_stop_reason and not self.user_interrupt_pending:
                exit_reason = self.system_stop_reason
            if not runtime_error:
                try:
                    self._save_state(force=True)
                except Exception as exc:
                    runtime_error = True
                    user_interrupted = False
                    exit_reason = self.handle_runtime_error(exc, "学习状态保存")
            if not runtime_error:
                self._transition_control(self.CONTROL_STOPPING, self.CONTROL_READY, enable_input=False, running=False, arming=False)
            if app_alive.is_set() and not runtime_error:
                if user_interrupted and self.user_interrupt_pending:
                    post_ui("show_user_control")
                else:
                    post_ui("show_agent_stopped", exit_reason)
            with self.lock:
                if self.agent_thread is threading.current_thread():
                    self.agent_thread = None

    def _idle_agent_loop(self):
        runtime_error = False
        exit_reason = "自由模式 AI 已停止。可重新选择模式。"
        try:
            self.stop_event.wait(0.22)
            while app_alive.is_set() and not shutdown_event.is_set() and not self.stop_event.is_set():
                before, _ = capture_screen()
                before_window = self._foreground_window_signature()
                before_cursor = self._cursor_pos()
                key = self._idle_context_key()
                program = self._pick_idle_program(key)
                action_result = self._perform_program(program)
                if action_result != self.ACTION_SUCCESS:
                    if self.system_stop_reason:
                        exit_reason = self.system_stop_reason
                    break
                if self.stop_event.is_set() or self.stop_event.wait(random.uniform(0.30, 0.70)):
                    if self.system_stop_reason:
                        exit_reason = self.system_stop_reason
                    break
                after, _ = capture_screen()
                if self.stop_event.is_set():
                    break
                after_window = self._foreground_window_signature()
                if self.stop_event.wait(0.14):
                    if self.system_stop_reason:
                        exit_reason = self.system_stop_reason
                    break
                settled, _ = capture_screen()
                settled_window = self._foreground_window_signature()
                reward = self._idle_intrinsic_reward(
                    before, after, program, before_window, after_window, before_cursor,
                    settled=settled, settled_window=settled_window,
                )
                self._learn_idle_program(key, program, reward)
        except Exception as exc:
            runtime_error = True
            exit_reason = self.handle_runtime_error(exc, "自由模式AI控制/视觉/学习过程")
        finally:
            self._transition_control(
                (self.CONTROL_CONTROLLING, self.CONTROL_STOPPING), self.CONTROL_STOPPING,
                enable_input=False, running=False, arming=False, ignore_selection_lbutton_up=False,
            )
            self._release_all_inputs()
            hook_failed = self.hook_callback_error_event.is_set()
            if hook_failed:
                self.system_stop_reason = "用户输入监听回调出错。AI已停止。可重新选择模式。"
                _log_runtime("error", "low-level input hook callback failed")
            with self.lock:
                user_interrupted = self.user_interrupt_event.is_set() and not hook_failed
                self.user_interrupt_pending = bool(user_interrupted)
                self.mode = None
            if self.system_stop_reason and not self.user_interrupt_pending:
                exit_reason = self.system_stop_reason
            if not runtime_error:
                try:
                    self._save_state(force=True)
                except Exception as exc:
                    runtime_error = True
                    user_interrupted = False
                    exit_reason = self.handle_runtime_error(exc, "自由模式学习状态保存")
            if not runtime_error:
                self._transition_control(self.CONTROL_STOPPING, self.CONTROL_READY, enable_input=False, running=False, arming=False)
            if app_alive.is_set() and not runtime_error:
                if user_interrupted and self.user_interrupt_pending:
                    post_ui("show_user_control")
                else:
                    post_ui("show_agent_stopped", exit_reason)
            with self.lock:
                if self.agent_thread is threading.current_thread():
                    self.agent_thread = None

    def _record_physical_keyboard(self, info, w_param):
        extended = bool(int(info.flags) & 0x01)
        vk_identity = ("vk", int(info.vkCode) & 0xFFFF, extended)
        scan_identity = ("scan", int(info.scanCode) & 0xFFFF, extended)
        message = int(w_param)
        if message in (WM_KEYDOWN, WM_SYSKEYDOWN) and not (int(info.flags) & 0x80):
            down = True
        elif message in (WM_KEYUP, WM_SYSKEYUP) or (int(info.flags) & 0x80):
            down = False
        else:
            return
        with self.physical_state_lock:
            for identity in (vk_identity, scan_identity):
                if down:
                    self.physical_keys_down.add(identity)
                else:
                    self.physical_keys_down.discard(identity)

    def _record_raw_keyboard(self, info):
        flags = int(info.Flags)
        extended = bool(flags & (RI_KEY_E0 | RI_KEY_E1))
        vk_code = int(info.VKey) & 0xFFFF
        scan_code = int(info.MakeCode) & 0xFFFF
        if vk_code == 0x00FF:
            return
        down = not bool(flags & RI_KEY_BREAK)
        identities = []
        if vk_code:
            identities.append(("vk", vk_code, extended))
        if scan_code:
            identities.append(("scan", scan_code, extended))
        with self.physical_state_lock:
            for identity in identities:
                if down:
                    self.physical_keys_down.add(identity)
                else:
                    self.physical_keys_down.discard(identity)

    def _record_physical_mouse(self, info, w_param):
        message = int(w_param)
        button = None
        down = False
        if message in (WM_LBUTTONDOWN, WM_LBUTTONUP):
            button, down = "left", message == WM_LBUTTONDOWN
        elif message in (WM_RBUTTONDOWN, WM_RBUTTONUP):
            button, down = "right", message == WM_RBUTTONDOWN
        elif message in (WM_MBUTTONDOWN, WM_MBUTTONUP):
            button, down = "middle", message == WM_MBUTTONDOWN
        elif message in (WM_XBUTTONDOWN, WM_XBUTTONUP):
            high = (int(info.mouseData) >> 16) & 0xFFFF
            button = "x1" if high == 1 else "x2" if high == 2 else None
            down = message == WM_XBUTTONDOWN
        if button is not None:
            with self.physical_state_lock:
                if down:
                    self.physical_buttons_down.add(button)
                else:
                    self.physical_buttons_down.discard(button)

    def _record_raw_mouse(self, info):
        flags = int(info.usButtonFlags)
        changes = (
            ("left", RI_MOUSE_LEFT_BUTTON_DOWN, RI_MOUSE_LEFT_BUTTON_UP),
            ("right", RI_MOUSE_RIGHT_BUTTON_DOWN, RI_MOUSE_RIGHT_BUTTON_UP),
            ("middle", RI_MOUSE_MIDDLE_BUTTON_DOWN, RI_MOUSE_MIDDLE_BUTTON_UP),
            ("x1", RI_MOUSE_BUTTON_4_DOWN, RI_MOUSE_BUTTON_4_UP),
            ("x2", RI_MOUSE_BUTTON_5_DOWN, RI_MOUSE_BUTTON_5_UP),
        )
        with self.physical_state_lock:
            for button, down_flag, up_flag in changes:
                if flags & down_flag:
                    self.physical_buttons_down.add(button)
                if flags & up_flag:
                    self.physical_buttons_down.discard(button)

    def _consume_selection_lbutton_up(self, source):
        now = time.monotonic()
        if self.ignore_selection_lbutton_up and (self.arming or self.running):
            self.ignore_selection_lbutton_up = False
            self.selection_release_seen_at = now
            self.selection_release_source = str(source)
            return True
        seen_at = float(self.selection_release_seen_at or 0.0)
        if (seen_at > 0.0 and now - seen_at <= 0.08
                and self.selection_release_source is not None
                and str(source) != self.selection_release_source):
            # Raw Input 与低级 Hook 会各报告一次同一物理松键；只吞掉另一通道的
            # 紧邻副本。任何后续按下/移动仍立即按用户抢回控制权处理。
            self.selection_release_seen_at = 0.0
            self.selection_release_source = None
            return True
        return False

    def _register_raw_mouse_input(self, info):
        if not (self.running or self.arming):
            return
        flags = int(info.usButtonFlags)
        selection_flags = RI_MOUSE_LEFT_BUTTON_DOWN | RI_MOUSE_LEFT_BUTTON_UP
        non_selection_flags = flags & ~selection_flags
        if flags & RI_MOUSE_LEFT_BUTTON_UP and not non_selection_flags:
            if self._consume_selection_lbutton_up("raw_mouse"):
                return
        if self.arming and self.ignore_selection_lbutton_up:
            with self.physical_state_lock:
                selection_button_down = "left" in self.physical_buttons_down
            if not non_selection_flags and (
                (flags & RI_MOUSE_LEFT_BUTTON_DOWN)
                or ((int(info.lLastX) != 0 or int(info.lLastY) != 0) and selection_button_down)
            ):
                return
        self._register_user_input("raw_mouse")

    def _register_user_input(self, source=None, w_param=None):
        if source == "mouse":
            message = int(w_param or 0)
            if message == WM_LBUTTONUP and self._consume_selection_lbutton_up("mouse"):
                return
            if self.ignore_selection_lbutton_up and self.arming:
                with self.physical_state_lock:
                    selection_button_down = "left" in self.physical_buttons_down
                if message == WM_MOUSEMOVE and selection_button_down:
                    return
        if not (self.running or self.arming):
            return
        first_interrupt = not self.user_interrupt_event.is_set()
        self.ignore_selection_lbutton_up = False
        self.selection_release_seen_at = 0.0
        self.selection_release_source = None
        self.input_enabled = False
        self.user_interrupt_event.set()
        self.stop_event.set()
        if first_interrupt and self.running:
            self.release_ui_requested.set()
        self.release_requested.set()

    def _fail_closed_input_monitor(self, reason):
        detail = str(reason).strip() or "用户输入监听失效"
        # Hook/WndProc 回调绝不能等待 input_gate_lock：另一个线程可能正持有该锁
        # 执行 SendInput，而 SendInput 又同步等待低级 Hook 回调，拿锁会形成死锁。
        self.input_enabled = False
        self.input_hooks_ready.clear()
        self.hook_callback_error_event.set()
        self.stop_event.set()
        if self.running:
            self.release_ui_requested.set()
        self.release_requested.set()
        if self.system_stop_reason is None:
            self.system_stop_reason = f"{detail}。AI已停止。可重新选择模式。"

    def _input_hook_watchdog_tick(self):
        if not self.running or not self.input_enabled or self.stop_event.is_set():
            self.hook_mouse_probe_sent_at = 0.0
            return
        now = time.monotonic()
        sent_at = float(self.hook_mouse_probe_sent_at or 0.0)
        ack_at = float(self.hook_mouse_probe_ack_at or 0.0)
        if sent_at > 0.0:
            if ack_at >= sent_at:
                self.hook_mouse_probe_sent_at = 0.0
            elif now - sent_at >= 0.40:
                self._fail_closed_input_monitor("低级鼠标 Hook 健康探测无响应")
                return
            else:
                return
        if now - ack_at < 0.45:
            return
        packet = INPUT()
        packet.type = INPUT_MOUSE
        packet.mi = MOUSEINPUT(0, 0, 0, MOUSEEVENTF_MOVE, 0, INPUT_TAG)
        self.hook_mouse_probe_sent_at = time.monotonic()
        if int(user32.SendInput(1, ctypes.byref(packet), ctypes.sizeof(INPUT))) != 1:
            self._fail_closed_input_monitor("低级鼠标 Hook 健康探测无法发送")

    def _install_raw_input_monitor(self, module):
        class_name = f"MakeItBiggerRawInput_{os.getpid()}_{int(self.hook_thread_id)}_{id(self):x}"

        @WNDPROC
        def raw_input_wndproc(hwnd, message, w_param, l_param):
            message = int(message)
            if message == WM_TIMER:
                try:
                    self._input_hook_watchdog_tick()
                except Exception as exc:
                    self._fail_closed_input_monitor(f"输入监听健康探测出错：{exc}")
                return 0
            if message == WM_INPUT:
                try:
                    size = wintypes.UINT(0)
                    header_size = ctypes.sizeof(RAWINPUTHEADER)
                    first = int(user32.GetRawInputData(
                        wintypes.HANDLE(l_param), RID_INPUT, None, ctypes.byref(size), header_size
                    ))
                    if first == 0xFFFFFFFF:
                        raise ctypes.WinError()
                    if int(size.value) < header_size or int(size.value) > (1 << 20):
                        raise RuntimeError(f"Raw Input 数据大小异常：{int(size.value)}")
                    word_count = max(1, (int(size.value) + 3) // 4)
                    buffer = (ctypes.c_uint32 * word_count)()
                    received = int(user32.GetRawInputData(
                        wintypes.HANDLE(l_param), RID_INPUT, ctypes.byref(buffer), ctypes.byref(size), header_size
                    ))
                    if received == 0xFFFFFFFF:
                        raise ctypes.WinError()
                    if received != int(size.value):
                        raise RuntimeError(f"Raw Input 数据读取不完整：{received}/{int(size.value)}")
                    raw = ctypes.cast(ctypes.byref(buffer), ctypes.POINTER(RAWINPUT)).contents
                    device_handle = int(raw.header.hDevice or 0)
                    if int(raw.header.dwType) == RIM_TYPEMOUSE:
                        info = raw.data.mouse
                        injected_by_self = int(info.ulExtraInformation) == RAW_INPUT_TAG
                        # hDevice==0 既可能来自 SendInput，也可能来自 Precision Touchpad。
                        # 这类歧义输入交给低级 Hook；watchdog 会在 Hook 静默失效时 fail closed。
                        if not injected_by_self and device_handle:
                            self._record_raw_mouse(info)
                            self._register_raw_mouse_input(info)
                    elif int(raw.header.dwType) == RIM_TYPEKEYBOARD:
                        info = raw.data.keyboard
                        injected_by_self = int(info.ExtraInformation) == RAW_INPUT_TAG
                        if not injected_by_self and device_handle:
                            self._record_raw_keyboard(info)
                            if self.running or self.arming:
                                self._register_user_input("raw_keyboard", w_param)
                except Exception as exc:
                    self._fail_closed_input_monitor(f"Raw Input 物理输入监听出错：{exc}")
                return user32.DefWindowProcW(hwnd, message, w_param, l_param)
            return user32.DefWindowProcW(hwnd, message, w_param, l_param)

        window_class = WNDCLASSW()
        window_class.lpfnWndProc = raw_input_wndproc
        window_class.hInstance = module
        window_class.lpszClassName = class_name
        atom = int(user32.RegisterClassW(ctypes.byref(window_class)))
        if not atom:
            raise ctypes.WinError()
        hwnd = user32.CreateWindowExW(
            0, class_name, class_name, 0, 0, 0, 0, 0, HWND_MESSAGE, None, module, None
        )
        if not hwnd:
            user32.UnregisterClassW(class_name, module)
            raise ctypes.WinError()
        devices = (RAWINPUTDEVICE * 2)()
        devices[0] = RAWINPUTDEVICE(HID_USAGE_PAGE_GENERIC, HID_USAGE_GENERIC_MOUSE, RIDEV_INPUTSINK, hwnd)
        devices[1] = RAWINPUTDEVICE(HID_USAGE_PAGE_GENERIC, HID_USAGE_GENERIC_KEYBOARD, RIDEV_INPUTSINK, hwnd)
        if not user32.RegisterRawInputDevices(devices, len(devices), ctypes.sizeof(RAWINPUTDEVICE)):
            user32.DestroyWindow(hwnd)
            user32.UnregisterClassW(class_name, module)
            raise ctypes.WinError()
        self.raw_input_wndproc = raw_input_wndproc
        self.raw_input_class_name = class_name
        self.raw_input_hwnd = hwnd
        self.raw_input_registered = True
        self.raw_input_timer_id = int(user32.SetTimer(hwnd, 1, 500, None))
        if not self.raw_input_timer_id:
            self._remove_raw_input_monitor(module)
            raise ctypes.WinError()

    def _remove_raw_input_monitor(self, module):
        if self.raw_input_timer_id and self.raw_input_hwnd:
            if not user32.KillTimer(self.raw_input_hwnd, self.raw_input_timer_id):
                _log_runtime("warning", "输入监听健康探测定时器注销失败。")
        self.raw_input_timer_id = 0
        self.hook_mouse_probe_sent_at = 0.0
        if self.raw_input_registered:
            devices = (RAWINPUTDEVICE * 2)()
            devices[0] = RAWINPUTDEVICE(HID_USAGE_PAGE_GENERIC, HID_USAGE_GENERIC_MOUSE, RIDEV_REMOVE, None)
            devices[1] = RAWINPUTDEVICE(HID_USAGE_PAGE_GENERIC, HID_USAGE_GENERIC_KEYBOARD, RIDEV_REMOVE, None)
            if not user32.RegisterRawInputDevices(devices, len(devices), ctypes.sizeof(RAWINPUTDEVICE)):
                _log_runtime("warning", "Raw Input 注销失败；进程退出时 Windows 会回收注册。")
        self.raw_input_registered = False
        if self.raw_input_hwnd:
            if not user32.DestroyWindow(self.raw_input_hwnd):
                _log_runtime("warning", "Raw Input 消息窗口销毁失败。")
        self.raw_input_hwnd = None
        if self.raw_input_class_name:
            if not user32.UnregisterClassW(self.raw_input_class_name, module):
                _log_runtime("warning", "Raw Input 窗口类注销失败。")
        self.raw_input_class_name = None
        self.raw_input_wndproc = None

    def run_release_worker(self):
        while app_alive.is_set() and not shutdown_event.is_set():
            if not self.release_requested.wait(0.25):
                continue
            self.release_requested.clear()
            if self.user_interrupt_event.is_set():
                self._transition_control(
                    (self.CONTROL_ARMING, self.CONTROL_CONTROLLING, self.CONTROL_STOPPING),
                    self.CONTROL_STOPPING, enable_input=False,
                )
            self._release_all_inputs()
            if self.release_ui_requested.is_set():
                self.release_ui_requested.clear()
                post_ui("show_stopping")
            if self.hook_callback_error_event.is_set() and not self.hook_quit_posted.is_set() and self.hook_thread_id:
                if user32.PostThreadMessageW(self.hook_thread_id, WM_QUIT, 0, 0):
                    self.hook_quit_posted.set()

    def run_input_monitor(self):
        failures = 0
        while app_alive.is_set() and not shutdown_event.is_set():
            try:
                self.monitor_input()
                if _shutdown_requested():
                    return
                raise RuntimeError("用户输入监听线程意外停止")
            except Exception as exc:
                if _shutdown_requested():
                    return
                failures += 1
                self.handle_runtime_error(exc, "用户输入监听")
                self.input_hooks_ready.clear()
                delay = min(8.0, 0.5 * (2 ** min(failures - 1, 4)))
                post_ui(
                    "runtime_error",
                    f"用户输入监听出错：{str(exc).strip() or exc.__class__.__name__}。AI已停止控制；程序正在自动恢复输入监听。",
                )
                if shutdown_event.wait(delay):
                    return
                self.hook_callback_error_event.clear()
                self.hook_quit_posted.clear()
                if not self.running and not self.arming and self.control_state == self.CONTROL_STOPPING:
                    self._transition_control(self.CONTROL_STOPPING, self.CONTROL_READY, enable_input=False, running=False, arming=False)

    def monitor_input(self):
        self.hook_thread_id = kernel32.GetCurrentThreadId()

        @HOOKPROC
        def mouse_proc(n_code, w_param, l_param):
            try:
                if n_code >= 0:
                    info = ctypes.cast(l_param, ctypes.POINTER(MSLLHOOKSTRUCT)).contents
                    if int(info.dwExtraInfo) == INPUT_TAG:
                        self.hook_mouse_probe_ack_at = time.monotonic()
                    else:
                        self._record_physical_mouse(info, w_param)
                        self._register_user_input("mouse", w_param)
            except Exception as exc:
                self._fail_closed_input_monitor(f"低级鼠标 Hook 回调出错：{exc}")
            return user32.CallNextHookEx(self.mouse_hook, n_code, w_param, l_param)

        @HOOKPROC
        def keyboard_proc(n_code, w_param, l_param):
            try:
                if n_code >= 0:
                    info = ctypes.cast(l_param, ctypes.POINTER(KBDLLHOOKSTRUCT)).contents
                    if int(info.dwExtraInfo) != INPUT_TAG:
                        self._record_physical_keyboard(info, w_param)
                        self._register_user_input("keyboard", w_param)
            except Exception as exc:
                self._fail_closed_input_monitor(f"低级键盘 Hook 回调出错：{exc}")
            return user32.CallNextHookEx(self.keyboard_hook, n_code, w_param, l_param)

        self.mouse_proc = mouse_proc
        self.keyboard_proc = keyboard_proc
        module = kernel32.GetModuleHandleW(None)
        self._install_raw_input_monitor(module)
        self.mouse_hook = user32.SetWindowsHookExW(WH_MOUSE_LL, self.mouse_proc, module, 0)
        self.keyboard_hook = user32.SetWindowsHookExW(WH_KEYBOARD_LL, self.keyboard_proc, module, 0)
        if not self.mouse_hook or not self.keyboard_hook:
            if self.mouse_hook:
                user32.UnhookWindowsHookEx(self.mouse_hook)
            if self.keyboard_hook:
                user32.UnhookWindowsHookEx(self.keyboard_hook)
            self.mouse_hook = None
            self.keyboard_hook = None
            self.input_hooks_ready.clear()
            self._remove_raw_input_monitor(module)
            raise RuntimeError("无法安装用户输入监听钩子")

        self.input_hooks_ready.set()
        post_ui("enable_controls")
        msg = wintypes.MSG()
        try:
            while app_alive.is_set() and not shutdown_event.is_set():
                result = user32.GetMessageW(ctypes.byref(msg), None, 0, 0)
                if result == -1:
                    raise ctypes.WinError()
                if result == 0:
                    break
                user32.TranslateMessage(ctypes.byref(msg))
                user32.DispatchMessageW(ctypes.byref(msg))
        finally:
            self.input_hooks_ready.clear()
            if self.mouse_hook and not user32.UnhookWindowsHookEx(self.mouse_hook):
                _log_runtime("warning", "低级鼠标 Hook 注销失败。")
            if self.keyboard_hook and not user32.UnhookWindowsHookEx(self.keyboard_hook):
                _log_runtime("warning", "低级键盘 Hook 注销失败。")
            self.mouse_hook = None
            self.keyboard_hook = None
            self._remove_raw_input_monitor(module)
        if app_alive.is_set() and not shutdown_event.is_set():
            if self.hook_callback_error_event.is_set():
                raise RuntimeError("用户输入监听回调出错")
            raise RuntimeError("用户输入监听消息循环已停止")


recognizer = None
controller = None


def virtual_origin():
    return (user32.GetSystemMetrics(76), user32.GetSystemMetrics(77))


def capture_screen():
    origin = virtual_origin()
    return ImageGrab.grab(all_screens=True), origin


def _observation_frame_ids(item):
    ids = set()
    for value in item.get("frame_ids", ()) if isinstance(item.get("frame_ids"), (list, tuple, set)) else ():
        try:
            ids.add(int(value))
        except (TypeError, ValueError):
            pass
    if item.get("frame_id") is not None:
        try:
            ids.add(int(item["frame_id"]))
        except (TypeError, ValueError):
            pass
    return ids


def _observation_window_signatures(item):
    values = set()
    raw = item.get("window_signatures")
    if isinstance(raw, (list, tuple, set)):
        values.update(str(value) for value in raw if str(value))
    single = str(item.get("window_signature") or "")
    if single:
        values.add(single)
    return values


def _merge_number_observations(observations):
    # Spatial identity and numeric value are deliberately kept separate.  A
    # timer/FPS/counter may change value every frame while remaining the same
    # selectable screen object.
    clusters = []
    for item in observations:
        item_signatures = _observation_window_signatures(item)
        best_cluster = None
        best_iou = 0.0
        for cluster in clusters:
            cluster_signatures = cluster.get("window_signatures", set())
            if item_signatures and cluster_signatures and item_signatures.isdisjoint(cluster_signatures):
                continue
            overlap = recognizer._iou(item["box"], cluster["box"])
            if overlap > best_iou:
                best_iou = overlap
                best_cluster = cluster
        if best_cluster is None or best_iou < 0.46:
            clusters.append({
                "box": item["box"],
                "items": [item],
                "window_signatures": set(item_signatures),
            })
        else:
            best_cluster["items"].append(item)
            best_cluster["window_signatures"].update(item_signatures)
            representative = max(best_cluster["items"], key=lambda g: float(g.get("conf", 0.0)))
            best_cluster["box"] = representative["box"]

    merged = []
    for cluster in clusters:
        votes = {}
        values = {}
        per_value_frame_best = {}
        position_frame_ids = set()
        window_signatures = set()
        per_frame_best = {}
        all_scale_ids = set()

        for item in cluster["items"]:
            key = _number_key(item["value"])
            values[key] = item["value"]
            confidence = max(0.05, float(item.get("conf", 0.0)))
            frame_ids = _observation_frame_ids(item)
            position_frame_ids.update(frame_ids)
            window_signatures.update(_observation_window_signatures(item))
            raw_scale_ids = item.get("scale_ids")
            if isinstance(raw_scale_ids, (list, tuple, set)):
                all_scale_ids.update(str(scale_id) for scale_id in raw_scale_ids)
            elif item.get("scale_id") is not None:
                all_scale_ids.add(str(item.get("scale_id")))

            if frame_ids:
                for frame_id in frame_ids:
                    evidence_key = (key, frame_id)
                    per_value_frame_best[evidence_key] = max(per_value_frame_best.get(evidence_key, 0.0), confidence)
                    previous = per_frame_best.get(frame_id)
                    if previous is None or confidence > float(previous.get("conf", 0.0)):
                        per_frame_best[frame_id] = item
            else:
                votes[key] = votes.get(key, 0.0) + confidence

        for (key, _frame_id), confidence in per_value_frame_best.items():
            votes[key] = votes.get(key, 0.0) + confidence
        if not votes:
            continue

        consensus_key = max(votes.items(), key=lambda kv: kv[1])[0]
        consensus_value = values[consensus_key]
        matching = [item for item in cluster["items"] if _number_key(item["value"]) == consensus_key]
        consensus_best = max(matching, key=lambda g: float(g.get("conf", 0.0)))

        frame_value_keys = {_number_key(item["value"]) for item in per_frame_best.values()}
        dynamic = len(per_frame_best) >= 2 and len(frame_value_keys) >= 2
        if dynamic:
            latest_frame = max(per_frame_best)
            best = per_frame_best[latest_frame]
            value = best["value"]
        else:
            best = consensus_best
            value = consensus_value

        value_frame_ids = set()
        for item in matching:
            value_frame_ids.update(_observation_frame_ids(item))

        result = dict(best)
        result["value"] = value
        result["consensus_value"] = consensus_value
        result["frame_ids"] = sorted(position_frame_ids)
        # distinct_frames now means independent positional observations, not
        # repeated sightings of one exact numeric value.
        result["distinct_frames"] = len(position_frame_ids)
        result["value_frame_ids"] = sorted(value_frame_ids)
        result["value_distinct_frames"] = len(value_frame_ids)
        result["dynamic"] = bool(dynamic)
        result["window_signatures"] = sorted(window_signatures)
        if len(window_signatures) == 1:
            result["stable_window_signature"] = next(iter(window_signatures))
        else:
            result.pop("stable_window_signature", None)
        result["scale_ids"] = sorted(all_scale_ids)
        independent_bonus = min(0.18, 0.07 * max(0, len(position_frame_ids) - 1))
        result["conf"] = min(1.0, float(best.get("conf", 0.0)) + independent_bonus)
        merged.append(result)

    merged.sort(
        key=lambda g: (
            int(g.get("distinct_frames", 0)),
            float(g.get("conf", 0.0)),
            len(str(g.get("text", g.get("value", "")))),
        ),
        reverse=True,
    )
    return merged

def _scan_cancelled(stop_event=None, deadline=None):
    if shutdown_event.is_set() or not app_alive.is_set():
        return True
    if stop_event is not None and stop_event.is_set():
        return True
    return deadline is not None and time.monotonic() >= float(deadline)


def detect_multiscale_image(image, origin, scales=(1.0, 0.86, 1.16), stop_event=None, deadline=None, fast=False, frame_id=None):
    observations = []
    for scale_index, scale in enumerate(scales):
        if _scan_cancelled(stop_event, deadline):
            break
        scale = float(scale)
        if abs(scale - 1.0) < 0.001:
            scaled = image
        else:
            scaled = image.resize((max(1, int(round(image.width * scale))), max(1, int(round(image.height * scale)))), Image.Resampling.BILINEAR)
        found = recognizer.detect(scaled, (0, 0), stop_event=stop_event, deadline=deadline, fast=fast)
        inv = 1.0 / scale
        for item in found:
            x0, y0, x1, y1 = item["box"]
            mapped = dict(item)
            mapped["scale_id"] = scale_index
            mapped["scale_ids"] = [str(scale_index)]
            if frame_id is not None:
                mapped["frame_id"] = int(frame_id)
                mapped["frame_ids"] = [int(frame_id)]
            mapped["box"] = (
                int(round(x0 * inv + origin[0])), int(round(y0 * inv + origin[1])),
                int(round(x1 * inv + origin[0])), int(round(y1 * inv + origin[1])),
            )
            if isinstance(item.get("chars"), list):
                mapped["chars"] = []
                for char in item["chars"]:
                    cx0, cy0, cx1, cy1 = char["box"]
                    mapped_char = dict(char)
                    mapped_char["box"] = (
                        int(round(cx0 * inv + origin[0])), int(round(cy0 * inv + origin[1])),
                        int(round(cx1 * inv + origin[0])), int(round(cy1 * inv + origin[1])),
                    )
                    mapped["chars"].append(mapped_char)
            observations.append(mapped)
    return _merge_number_observations(observations)


def detect_multiframe_screen(frame_count=None, scales=None, stop_event=None, deadline=None):
    if frame_count is None:
        frame_count = int(hardware_profile["scan_frames"])
    if scales is None:
        scales = tuple(hardware_profile["scan_scales"])
    observations = []
    for frame in range(max(1, int(frame_count))):
        if _scan_cancelled(stop_event, deadline):
            break
        image, origin = capture_screen()
        pixels = max(1, image.width * image.height)
        coarse_scale = min(1.0, math.sqrt(float(hardware_profile["coarse_pixel_budget"]) / pixels))
        coarse_scale = _clamp(coarse_scale, 0.35, 1.0)
        coarse = detect_multiscale_image(image, origin, scales=(coarse_scale,), stop_event=stop_event, deadline=deadline, fast=True, frame_id=frame)

        if not _scan_cancelled(stop_event, deadline) and (not coarse or (frame == 0 and coarse_scale < 0.72)):
            tile_pixels = max(1, int(hardware_profile["tile_pixel_budget"]))
            aspect = image.width / float(max(1, image.height))
            tile_w = max(320, int(round(math.sqrt(tile_pixels * max(1.0, aspect)))))
            tile_h = max(240, int(round(tile_pixels / float(tile_w))))
            overlap_x = max(8, int(tile_w * 0.06))
            overlap_y = max(8, int(tile_h * 0.06))
            step_x = max(1, tile_w - overlap_x)
            step_y = max(1, tile_h - overlap_y)
            y = 0
            while y < image.height and not _scan_cancelled(stop_event, deadline):
                x = 0
                while x < image.width and not _scan_cancelled(stop_event, deadline):
                    right = min(image.width, x + tile_w)
                    bottom = min(image.height, y + tile_h)
                    crop = image.crop((x, y, right, bottom))
                    coarse.extend(detect_multiscale_image(crop, (origin[0] + x, origin[1] + y), scales=(1.0,), stop_event=stop_event, deadline=deadline, fast=True, frame_id=frame))
                    if right >= image.width:
                        break
                    x += step_x
                if bottom >= image.height:
                    break
                y += step_y

        coarse = _merge_number_observations(coarse)
        frame_observations = list(coarse)
        regions = []
        for item in coarse:
            x0, y0, x1, y1 = item["box"]
            h = max(1, y1 - y0)
            w = max(1, x1 - x0)
            mx = max(w, int(h * 4.0))
            my = max(h, int(h * 2.0))
            regions.append([x0 - mx, y0 - my, x1 + mx, y1 + my])
        merged_regions = []
        for region in regions:
            joined = False
            for existing in merged_regions:
                if not (region[2] < existing[0] or region[0] > existing[2] or region[3] < existing[1] or region[1] > existing[3]):
                    existing[0] = min(existing[0], region[0]); existing[1] = min(existing[1], region[1])
                    existing[2] = max(existing[2], region[2]); existing[3] = max(existing[3], region[3])
                    joined = True
                    break
            if not joined:
                merged_regions.append(region)
        for gx0, gy0, gx1, gy1 in merged_regions:
            if _scan_cancelled(stop_event, deadline):
                break
            ix0 = max(0, int(gx0 - origin[0])); iy0 = max(0, int(gy0 - origin[1]))
            ix1 = min(image.width, int(gx1 - origin[0])); iy1 = min(image.height, int(gy1 - origin[1]))
            if ix1 - ix0 < 4 or iy1 - iy0 < 4:
                continue
            crop = image.crop((ix0, iy0, ix1, iy1))
            frame_observations.extend(detect_multiscale_image(crop, (origin[0] + ix0, origin[1] + iy0), scales=scales, stop_event=stop_event, deadline=deadline, fast=False, frame_id=frame))
        frame_observations = _merge_number_observations(frame_observations)
        for item in frame_observations:
            item["frame_id"] = frame
            item["frame_ids"] = [frame]
            if controller is not None:
                signature = controller._window_signature(item)
                if signature:
                    item["window_signature"] = signature
                    item["window_signatures"] = [signature]
                root_hwnd, _window_rect, _window_dpi = controller._target_window_info(item)
                if root_hwnd:
                    item["root_hwnd"] = int(root_hwnd)
        observations.extend(frame_observations)
        if frame + 1 < int(frame_count) and stop_event is not None:
            if stop_event.wait(_clamp(0.04 + 0.01 * frame, 0.04, 0.08)):
                break
    merged = _merge_number_observations(observations)
    return [
        item for item in merged
        if int(item.get("distinct_frames", 0)) >= 2
        and len(item.get("window_signatures", ())) == 1
    ]


def _controls_can_start():
    return (
        controller is not None
        and controller.input_hooks_ready.is_set()
        and not controller.hook_callback_error_event.is_set()
        and not controller.running
        and not controller.arming
        and not controller.overlay_mode
        and controller.control_state == controller.CONTROL_READY
        and not _shutdown_requested()
    )


def enable_main_controls():
    can_start = _controls_can_start()
    number_button.config(state="normal" if can_start else "disabled", command=scan_numbers)
    free_button.config(state="normal" if can_start else "disabled", command=start_free)
    if can_start:
        _apply_progress({
            "value": 100,
            "phase": "已就绪",
            "text": "请选择运行模式",
            "detail": "数字识别正常 · 鼠标键盘监听正常",
        })
    _refresh_info_vars()


def _launch_scan_worker():
    global scan_thread
    if _shutdown_requested() or controller is None or not controller.overlay_mode:
        return
    scan_thread = threading.Thread(target=_scan_worker, name="MakeItBiggerScan", daemon=True)
    scan_thread.start()


def scan_numbers():
    if not _controls_can_start():
        return
    controller.clear_user_interrupt()
    controller.stop_event.clear()
    if not controller._transition_control(controller.CONTROL_READY, controller.CONTROL_SCANNING, enable_input=False):
        return
    controller.overlay_mode = True
    _apply_progress({
        "value": 0,
        "phase": "正在扫描",
        "text": "正在识别屏幕上的数字",
        "detail": "主界面已隐藏；识别结束后会显示可选择的数字区域。",
    })
    root.withdraw()
    delay = max(120, int(round(1000.0 / max(2.0, hardware_profile["capacity"]))))
    root.after(delay, _launch_scan_worker)


def start_free():
    if not _controls_can_start():
        return
    controller._clear_target_tracking()
    if not controller.start("free"):
        dependency_failed("用户输入监听不可用，AI不会开始控制。")


def _scan_worker():
    if _shutdown_requested() or controller is None:
        return
    deadline = time.monotonic() + float(hardware_profile["scan_deadline"])
    try:
        numbers = detect_multiframe_screen(stop_event=controller.stop_event, deadline=deadline)
        if _shutdown_requested() or controller is None or not controller.overlay_mode:
            return
        if numbers:
            post_ui("show_overlays", numbers)
            return
        controller.overlay_mode = False
        controller._transition_control(controller.CONTROL_SCANNING, controller.CONTROL_READY, enable_input=False)
        post_ui("runtime_error", "未识别到屏幕上的数字。")
    except Exception as exc:
        if controller is not None and not _shutdown_requested():
            controller.handle_runtime_error(exc, "扫描/截图/数字识别")


def show_number_overlays(numbers):
    if (_shutdown_requested() or controller is None
            or controller.control_state != controller.CONTROL_SCANNING):
        return
    if not controller._transition_control(controller.CONTROL_SCANNING, controller.CONTROL_SELECTING, enable_input=False):
        return
    for old in list(controller.overlays):
        try:
            old.destroy()
        except Exception:
            pass
    controller.overlays = []
    controller.overlay_targets = list(numbers)
    controller.overlay_items = []
    controller.overlay_canvas = None
    if not controller.overlay_targets:
        controller.overlay_mode = False
        controller._transition_control(controller.CONTROL_SELECTING, controller.CONTROL_READY, enable_input=False)
        _show_main_with_status("未识别到经过多帧确认的屏幕数字。")
        return

    vx, vy = virtual_origin()
    vw = max(2, int(user32.GetSystemMetrics(78)))
    vh = max(2, int(user32.GetSystemMetrics(79)))
    transparent_key = "#010203"
    win = tk.Toplevel(root)
    win.withdraw()
    win.overrideredirect(True)
    win.attributes("-topmost", True)
    win.attributes("-alpha", 0.36)
    win.configure(bg=transparent_key)
    try:
        win.wm_attributes("-transparentcolor", transparent_key)
    except tk.TclError:
        win.destroy()
        raise RuntimeError("当前 Windows/Tk 环境不支持透明数字覆盖层。")
    canvas = tk.Canvas(win, width=vw, height=vh, bg=transparent_key, highlightthickness=0, borderwidth=0)
    canvas.pack(fill="both", expand=True)

    draw_order = sorted(range(len(numbers)), key=lambda i: float(numbers[i].get("conf", 0.0)))
    for idx in draw_order:
        item = numbers[idx]
        x0, y0, x1, y1 = item["box"]
        pad = max(2, int((y1 - y0) * 0.10))
        x0, y0, x1, y1 = x0 - pad, y0 - pad, x1 + pad, y1 + pad
        local_box = (x0 - vx, y0 - vy, x1 - vx, y1 - vy)
        r, g, b = colorsys.hsv_to_rgb((idx * 0.61803398875) % 1.0, 0.70, 1.0)
        color = f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"
        rect_id = canvas.create_rectangle(*local_box, fill=color, outline=color, width=1)
        controller.overlay_items.append({
            "index": idx,
            "item_id": rect_id,
            "box": local_box,
            "area": max(1, (local_box[2] - local_box[0]) * (local_box[3] - local_box[1])),
        })

    def on_overlay_click(event):
        x, y = float(event.x), float(event.y)
        hits = [
            entry for entry in controller.overlay_items
            if entry["box"][0] <= x <= entry["box"][2] and entry["box"][1] <= y <= entry["box"][3]
        ]
        if not hits:
            return
        selected = min(hits, key=lambda entry: (entry["area"], -float(numbers[entry["index"]].get("conf", 0.0))))
        choose_number(selected["index"])

    canvas.bind("<Button-1>", on_overlay_click)
    win.deiconify()
    win.update_idletasks()
    hwnd = user32.GetAncestor(wintypes.HWND(win.winfo_id()), GA_ROOT)
    if not hwnd:
        hwnd = wintypes.HWND(win.winfo_id())
    if not user32.SetWindowPos(hwnd, HWND_TOPMOST, int(vx), int(vy), int(vw), int(vh), SWP_NOACTIVATE | SWP_SHOWWINDOW):
        win.destroy()
        raise ctypes.WinError()
    controller.overlays = [win]
    controller.overlay_canvas = canvas


def choose_number(index):
    if _shutdown_requested() or controller is None:
        return
    if (controller.control_state != controller.CONTROL_SELECTING
            or controller.arming or controller.running):
        return
    if index < 0 or index >= len(controller.overlay_targets) or not controller.overlays:
        return
    selected_win = controller.overlays[0]
    selected_target = controller.overlay_targets[index]
    selected_entry = next((entry for entry in controller.overlay_items if entry["index"] == index), None)
    if selected_entry is None or controller.overlay_canvas is None:
        return
    # The first selection is final for this overlay.  Unbind before arming so a
    # second click can only be interpreted by the low-level hook as user control.
    controller.overlay_canvas.unbind("<Button-1>")
    controller.select_target(selected_target)
    for entry in list(controller.overlay_items):
        if entry is not selected_entry:
            controller.overlay_canvas.delete(entry["item_id"])
    controller.overlay_items = [selected_entry]
    controller.overlay_targets = [controller.target]
    if not controller._transition_control(
        controller.CONTROL_SELECTING, controller.CONTROL_ARMING, enable_input=False,
        running=False, arming=True, ignore_selection_lbutton_up=True,
    ):
        return
    fade_selected(selected_win, 0)


def fade_selected(win, frame):
    if _shutdown_requested():
        try:
            if win.winfo_exists():
                win.destroy()
        except Exception:
            pass
        return
    if controller is None:
        return
    if controller.arming and (controller.stop_event.is_set() or controller.user_interrupt_event.is_set()):
        try:
            if win.winfo_exists():
                win.destroy()
        except Exception:
            pass
        controller.overlays = []
        controller.overlay_targets = []
        controller.overlay_items = []
        controller.overlay_canvas = None
        controller.overlay_mode = False
        controller._transition_control(
            (controller.CONTROL_ARMING, controller.CONTROL_STOPPING), controller.CONTROL_READY, enable_input=False,
            running=False, arming=False, ignore_selection_lbutton_up=False,
        )
        controller._clear_target_tracking()
        _show_main_with_status("启动已取消。可重新选择模式。")
        return
    if not win.winfo_exists():
        return
    total = 30
    if frame >= total:
        win.destroy()
        controller.overlays = []
        controller.overlay_targets = []
        controller.overlay_items = []
        controller.overlay_canvas = None
        controller.overlay_mode = False
        try:
            controller.observe_selected_semantic_truth()
        except Exception as exc:
            controller.handle_runtime_error(exc, "选中数字的语义标签验证")
            return
        if not controller.start("grow"):
            was_cancelled = controller.user_interrupt_event.is_set() or controller.stop_event.is_set()
            controller._transition_control(
                (controller.CONTROL_ARMING, controller.CONTROL_STOPPING), controller.CONTROL_READY, enable_input=False,
                running=False, arming=False, ignore_selection_lbutton_up=False,
            )
            if was_cancelled:
                controller._clear_target_tracking()
                _show_main_with_status("启动已取消。可重新选择模式。")
            else:
                dependency_failed("用户输入监听不可用，AI不会开始控制。")
        return
    alpha = 0.36 * (1.0 - frame / total)
    win.attributes("-alpha", max(0.01, alpha))
    root.after(100, lambda: fade_selected(win, frame + 1))

def _clear_overlays_and_show_error(text):
    if controller is not None:
        was_running = bool(controller.running)
        controller.stop_event.set()
        controller._transition_control(
            (controller.CONTROL_READY, controller.CONTROL_SCANNING, controller.CONTROL_SELECTING, controller.CONTROL_ARMING, controller.CONTROL_CONTROLLING, controller.CONTROL_STOPPING),
            controller.CONTROL_STOPPING, enable_input=False, arming=False, ignore_selection_lbutton_up=False,
        )
        if not was_running:
            controller._transition_control(
                controller.CONTROL_STOPPING, controller.CONTROL_READY,
                enable_input=False, running=False, arming=False,
            )
        controller.overlay_mode = False
        controller.system_stop_reason = str(text)
        try:
            controller._release_all_inputs()
        except Exception as exc:
            _log_exception("error-path input release", exc)
            controller.stop_event.set()
            controller.input_enabled = False
            controller.system_stop_reason = f"{text}；释放鼠标或键盘状态时出错：{exc}。AI已停止。"
        if controller.system_stop_reason:
            text = controller.system_stop_reason
        controller._clear_target_tracking()
        for win in list(controller.overlays):
            try:
                if win.winfo_exists():
                    win.destroy()
            except tk.TclError:
                continue
        controller.overlays = []
        controller.overlay_targets = []
        controller.overlay_items = []
        controller.overlay_canvas = None
    _show_main_with_status(text)


def _show_main_with_status(text):
    if _shutdown_requested() or root is None:
        return
    text = str(text)
    is_error = any(token in text for token in ("出错", "失败", "不可用", "未识别", "拒绝"))
    current_progress = 0.0
    try:
        if progress_var is not None:
            current_progress = float(progress_var.get())
    except Exception:
        current_progress = 0.0
    _apply_progress({
        "value": current_progress if is_error else 100,
        "phase": "已停止" if is_error else "已就绪",
        "text": text,
        "detail": (
            "运行环境未准备完成，AI 当前不控制鼠标或键盘。"
            if is_error
            else "AI 当前不控制鼠标或键盘。可重新选择模式。"
        ),
    })
    can_start = _controls_can_start()
    number_button.config(state="normal" if can_start else "disabled", command=scan_numbers)
    free_button.config(state="normal" if can_start else "disabled", command=start_free)
    _refresh_info_vars()
    root.deiconify()
    root.lift()


def show_main_stopping():
    if _shutdown_requested() or root is None:
        return
    current_progress = 0.0
    try:
        if progress_var is not None:
            current_progress = float(progress_var.get())
    except Exception:
        current_progress = 0.0
    _apply_progress({
        "value": current_progress,
        "phase": "正在停止",
        "text": "已检测到用户输入，AI已停止控制，正在完成状态保存",
        "detail": "主界面已恢复；状态保存完成后即可重新选择模式。",
    })
    number_button.config(state="disabled")
    free_button.config(state="disabled")
    _refresh_info_vars()
    root.deiconify()
    root.lift()


def show_main_user_control():
    _show_main_with_status("已检测到你的鼠标或键盘输入，AI已停止。")


def show_main_agent_stopped(reason):
    _show_main_with_status(reason)


def _tk_callback_exception(exc_type, exc_value, exc_tb):
    exc = exc_value if isinstance(exc_value, BaseException) else RuntimeError(str(exc_value))
    if controller is not None:
        controller.handle_runtime_error(exc, "界面/扫描回调")
    else:
        dependency_failed(f"运行出错：{exc}")


def shutdown():
    global shutdown_started
    with shutdown_lock:
        if shutdown_started:
            return
        shutdown_started = True

    shutdown_event.set()
    app_alive.clear()

    if root is not None:
        try:
            root.withdraw()
        except tk.TclError:
            pass

    agent_thread = None
    if controller is not None:
        try:
            controller.stop_event.set()
        except Exception as exc:
            _log_exception("shutdown stop signal", exc)
        try:
            controller._transition_control(
                (controller.CONTROL_READY, controller.CONTROL_SCANNING, controller.CONTROL_SELECTING, controller.CONTROL_ARMING, controller.CONTROL_CONTROLLING, controller.CONTROL_STOPPING),
                controller.CONTROL_STOPPING, enable_input=False, running=False, arming=False, ignore_selection_lbutton_up=False,
            )
        except Exception as exc:
            _log_exception("shutdown control transition", exc)
        try:
            controller._release_all_inputs()
        except Exception as exc:
            _log_exception("shutdown input release", exc)
        try:
            controller.overlay_mode = False
            for win in list(controller.overlays):
                try:
                    win.destroy()
                except Exception:
                    pass
            controller.overlays = []
            controller.overlay_targets = []
            controller.overlay_items = []
            controller.overlay_canvas = None
            controller.ignore_selection_lbutton_up = False
        except Exception:
            pass
        try:
            if controller.hook_thread_id:
                user32.PostThreadMessageW(controller.hook_thread_id, WM_QUIT, 0, 0)
        except Exception as exc:
            _log_exception("shutdown input monitor stop", exc)
        try:
            with controller.lock:
                agent_thread = controller.agent_thread
        except Exception:
            agent_thread = getattr(controller, "agent_thread", None)

    terminate_child_processes()

    deadline = time.monotonic() + 1.5
    threads = [bootstrap_thread, hardware_thread, hook_thread, release_thread, scan_thread, agent_thread]
    seen = set()
    for thread in threads:
        if thread is None or thread is threading.current_thread() or id(thread) in seen:
            continue
        seen.add(id(thread))
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            break
        try:
            thread.join(timeout=min(0.5, remaining))
        except Exception:
            pass

    if controller is not None:
        try:
            controller._save_state()
        except Exception as exc:
            _log_exception("shutdown learning state save", exc)

    if root is not None:
        try:
            root.destroy()
        except Exception:
            pass


def run_application():
    global bootstrap_thread
    try:
        if not initialize_ui_and_storage():
            return
        if _shutdown_requested():
            return
        root.report_callback_exception = _tk_callback_exception
        bootstrap_thread = threading.Thread(target=bootstrap_dependencies, name="MakeItBiggerBootstrap", daemon=True)
        bootstrap_thread.start()
        root.mainloop()
    except Exception as exc:
        _log_exception("application startup failed", exc)
        app_alive.clear()
        terminate_child_processes()
        if controller is not None:
            try:
                controller.stop_event.set()
            except Exception as stop_exc:
                _log_exception("startup failure stop signal", stop_exc)
            try:
                controller._transition_control(
                    (controller.CONTROL_READY, controller.CONTROL_SCANNING, controller.CONTROL_SELECTING, controller.CONTROL_ARMING, controller.CONTROL_CONTROLLING, controller.CONTROL_STOPPING),
                    controller.CONTROL_STOPPING, enable_input=False, running=False, arming=False, ignore_selection_lbutton_up=False,
                )
            except Exception as transition_exc:
                _log_exception("startup failure control transition", transition_exc)
            try:
                controller._release_all_inputs()
            except Exception as release_exc:
                _log_exception("startup failure input release", release_exc)
            try:
                if controller.hook_thread_id:
                    user32.PostThreadMessageW(controller.hook_thread_id, WM_QUIT, 0, 0)
            except Exception as hook_exc:
                _log_exception("startup failure hook stop", hook_exc)
        if show_startup_error(exc):
            root.report_callback_exception = _tk_callback_exception
            try:
                root.mainloop()
            except Exception:
                pass


run_application()
