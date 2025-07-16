import tkinter as tk
from tkinter import ttk, messagebox
from ttkbootstrap import Style
import mysql.connector
import subprocess  # To open admin_dashboard.py

# Function to check admin login
def admin_login():
    password = password_entry.get()

    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",           # Change if needed
            password="Root@2507",           # Your MySQL password if any
            database="estudio_db"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE role='admin' LIMIT 1")
        result = cursor.fetchone()

        if result and password == result[0]:
            root.destroy()
            subprocess.Popen(["python", "admin_dashboard.py"])
        else:
            messagebox.showerror("Login Failed", "Incorrect admin password.")

        cursor.close()
        conn.close()

    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", str(e))

# --- UI Setup ---
root = tk.Tk()
root.title("Admin Login - eStudio Management")
root.geometry("400x220")

style = Style(theme="darkly")  # You can try "minty", "morph", "flatly", etc.

frame = ttk.Frame(root, padding=20)
frame.pack(expand=True)

ttk.Label(frame, text="Admin Login", font=("Helvetica", 18)).pack(pady=10)
ttk.Button(root, text="📊 Booking Reports", command=lambda: subprocess.Popen(["python", "booking_report.py"]), bootstyle="primary").pack(pady=10)

password_entry = ttk.Entry(frame, show="*", width=30)
password_entry.pack(pady=10)
password_entry.focus()

login_button = ttk.Button(frame, text="Login", command=admin_login)
login_button.pack(pady=10)

root.mainloop()
