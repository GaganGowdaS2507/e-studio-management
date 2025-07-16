# booking_ui.py

import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style
import subprocess
import os

def open_new_booking():
    subprocess.Popen(["python", "new_booking_form.py"])

def open_booking_status():
    subprocess.Popen(["python", "booking_status_enquiry.py"])

def go_back_home():
    root.destroy()

# --- GUI Setup ---
root = tk.Tk()
root.title("📅 Booking Panel - eStudio")
root.geometry("450x300")
style = Style("flatly")

frame = ttk.Frame(root, padding=30)
frame.pack(expand=True)

ttk.Label(frame, text="eStudio Booking Options", font=("Segoe UI", 16, "bold")).pack(pady=(0, 20))

btn_booking = ttk.Button(
    frame,
    text="📝 3.1 - New Booking",
    width=30,
    command=open_new_booking,
    bootstyle="success"
)
btn_booking.pack(pady=10)

btn_status = ttk.Button(
    frame,
    text="🔎 3.2 - Check Booking Status",
    width=30,
    command=open_booking_status,
    bootstyle="info"
)
btn_status.pack(pady=10)

ttk.Button(
    frame,
    text="🔙 Back to Home",
    command=go_back_home,
    bootstyle="secondary"
).pack(pady=(20, 0))

root.mainloop()
