import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import os
import subprocess
from ttkbootstrap import Style

# Launchers for respective modules
# def open_admin_dashboard():
#     pwd = simpledialog.askstring("Admin Login", "Enter admin password:", show='*')
#     if pwd == "admin123":  # Replace with secure verification
#         subprocess.Popen(["python", "admin_dashboard.py"])
#     else:
#         messagebox.showerror("Access Denied", "Incorrect password!")

# def open_artist_dashboard():
#     subprocess.Popen(["python", "artist_login.py"])

# def open_new_booking():
#     subprocess.Popen(["python", "new_booking_form.py"])

# def open_booking_status():
#     subprocess.Popen(["python", "booking_status_enquiry.py"])

# def open_free_slot_checker():
#     subprocess.Popen(["python", "customer_slot_checker.py"])

# def open_payment_updates():
#     subprocess.Popen(["python", "update_payments_ui.py"])

# def open_completed_payments():
#     messagebox.showinfo("Coming Soon", "Completed payments module is not yet linked.")
#     # Link to a real script if available


# --- Launchers for respective modules (.exe) ---



def open_admin_dashboard():
    pwd = simpledialog.askstring("Admin Login", "Enter admin password:", show='*')
    if pwd == "admin123":  # Use real DB validation later
        subprocess.Popen([os.path.join(os.getcwd(), "admin_dashboard.exe")])
    else:
        messagebox.showerror("Access Denied", "Incorrect password!")

def open_artist_dashboard():
    subprocess.Popen([os.path.join(os.getcwd(), "artist_login.exe")])


def open_new_booking():
    subprocess.Popen([os.path.join(os.getcwd(), "new_booking_form.exe")])

def open_booking_status():
    subprocess.Popen([os.path.join(os.getcwd(), "booking_status_enquiry.exe")])

def open_free_slot_checker():
    subprocess.Popen([os.path.join(os.getcwd(), "customer_slot_checker.exe")])

def open_payment_updates():
    subprocess.Popen([os.path.join(os.getcwd(), "update_payments_ui.exe")])

# GUI Setup
root = tk.Tk()
root.title("📸 eStudio Reception Panel")
root.geometry("600x500")
style = Style("sandstone")

ttk.Label(root, text="eStudio Management System", font=("Helvetica", 18, "bold")).pack(pady=20)

# Button Layout
main_frame = ttk.Frame(root, padding=20)
main_frame.pack(fill="both", expand=True)

# Admin
ttk.Button(main_frame, text="🛡️ Admin Dashboard", command=open_admin_dashboard, width=30).pack(pady=5)

# Artist
ttk.Button(main_frame, text="🎨 Artist Dashboard", command=open_artist_dashboard, width=30).pack(pady=5)

# Booking Dropdowns
ttk.Label(main_frame, text="📅 Booking", font=("Helvetica", 12, "underline")).pack(pady=(20, 0))
ttk.Button(main_frame, text="➕ New Booking", command=open_new_booking, width=30).pack(pady=5)
ttk.Button(main_frame, text="🔍 Booking Status Enquiry", command=open_booking_status, width=30).pack(pady=5)

# Slot Checker
ttk.Button(main_frame, text="🕐 Free Slot Enquiry", command=open_free_slot_checker, width=30).pack(pady=(20, 5))

# Payments Dropdowns
ttk.Label(main_frame, text="💳 Payments", font=("Helvetica", 12, "underline")).pack(pady=(20, 0))
# ttk.Button(main_frame, text="✅ Completed Payments", command=open_completed_payments, width=30).pack(pady=5)
ttk.Button(main_frame, text="💰 Update Balance Payments", command=open_payment_updates, width=30).pack(pady=5)

# Exit
ttk.Button(root, text="🚪 Exit", command=root.destroy, style="danger.TButton").pack(pady=20)

root.mainloop()
