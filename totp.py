import tkinter as tk
from tkinter import ttk
import time
import hmac
import hashlib
import base64
import struct
import urllib.request
from email.utils import parsedate_to_datetime

# --- Core Logic ---
def get_time_offset():
    try:
        req = urllib.request.Request("https://google.com", method="HEAD")
        with urllib.request.urlopen(req, timeout=3) as response:
            date_str = response.headers['Date']
            true_time_dt = parsedate_to_datetime(date_str)
            true_network_time = int(true_time_dt.timestamp())
            local_time = int(time.time())
            return true_network_time - local_time
    except:
        return 0

def generate_totp(secret_key, time_offset):
    secret_key = secret_key.replace(" ", "").upper()
    if not secret_key:
        return "------"
    
    secret_key += "=" * ((8 - len(secret_key) % 8) % 8) 
    
    try:
        key_bytes = base64.b32decode(secret_key)
    except Exception:
        return "INVALID"

    current_corrected_time = int(time.time()) + time_offset
    time_counter = current_corrected_time // 30
    time_bytes = struct.pack(">Q", time_counter)

    hmac_hash = hmac.new(key_bytes, time_bytes, hashlib.sha1).digest()
    offset = hmac_hash[-1] & 0x0F
    truncated_bytes = hmac_hash[offset : offset + 4]
    code_int = struct.unpack(">I", truncated_bytes)[0] & 0x7FFFFFFF

    totp_code = code_int % 1000000
    code_str = str(totp_code).zfill(6)
    return f"{code_str[:3]} {code_str[3:]}"

# --- Graphical User Interface ---
class AuthenticatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Authenticator")
        self.root.geometry("320x280")
        self.root.resizable(False, False)
        
        self.time_offset = get_time_offset()

        # --- UI Styling ---
        style = ttk.Style()
        style.configure("TLabel", font=("Segoe UI", 11))
        style.configure("Title.TLabel", font=("Segoe UI", 14, "bold"))
        style.configure("Code.TLabel", font=("Consolas", 32, "bold"), foreground="#005A9E")
        style.configure("Timer.TLabel", font=("Segoe UI", 10), foreground="#555555")

        # --- Widgets ---
        ttk.Label(root, text="Input your Secret Key:", style="Title.TLabel").pack(pady=(20, 5))
        
        self.secret_entry = ttk.Entry(root, width=30, justify="center", font=("Segoe UI", 10))
        self.secret_entry.pack(pady=5)
        
        # This line automatically puts the cursor in the box so you can start typing immediately!
        self.secret_entry.focus_set()

        # OTP Display (Clickable)
        self.code_label = ttk.Label(root, text="--- ---", style="Code.TLabel", cursor="hand2")
        self.code_label.pack(pady=(15, 0))
        self.code_label.bind("<Button-1>", lambda e: self.copy_to_clipboard())

        # Timer Display
        self.timer_label = ttk.Label(root, text="Valid for: 30s", style="Timer.TLabel")
        self.timer_label.pack(pady=(0, 15))

        # Copy Button
        self.copy_btn = ttk.Button(root, text="Copy to Clipboard", command=self.copy_to_clipboard)
        self.copy_btn.pack(pady=5)

        # Status Bar
        status_text = "Synced with Google Time" if self.time_offset != 0 else "Using Local Computer Time"
        self.status_label = ttk.Label(root, text=status_text, font=("Segoe UI", 8), foreground="#888888")
        self.status_label.pack(side="bottom", pady=10)

        self.update_ui()

    def copy_to_clipboard(self):
        code = self.code_label.cget("text").replace(" ", "")
        if code.isdigit():
            self.root.clipboard_clear()
            self.root.clipboard_append(code)
            self.copy_btn.config(text="Copied!")
            self.root.after(2000, lambda: self.copy_btn.config(text="Copy to Clipboard"))

    def update_ui(self):
        secret = self.secret_entry.get()
        code = generate_totp(secret, self.time_offset)
        self.code_label.config(text=code)
        
        current_corrected_time = int(time.time()) + self.time_offset
        seconds_remaining = 30 - (current_corrected_time % 30)
        
        if seconds_remaining <= 5:
            self.timer_label.config(text=f"Valid for: {seconds_remaining}s", foreground="#D13438")
        else:
            self.timer_label.config(text=f"Valid for: {seconds_remaining}s", foreground="#555555")

        self.root.after(1000, self.update_ui)

if __name__ == "__main__":
    root = tk.Tk()
    app = AuthenticatorApp(root)
    root.mainloop()