import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import mysql.connector

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Root@2507",
        database="estudio_db"
    )

def login():
    artist_id = entry_id.get().strip()
    if not artist_id.isdigit():
        messagebox.showerror("Invalid", "Please enter a valid numeric Artist ID.")
        return

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM artists WHERE artist_id = %s", (artist_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    if not result:
        messagebox.showerror("Not Found", "Artist ID not found. Please check again.")
        return

    artist_name = result[0]
    if not messagebox.askyesno("Confirm", f"Login as {artist_name}?"):
        return

    root.destroy()
    subprocess.Popen([os.path.join(os.getcwd(), "artist_dashboard.exe"), artist_id])


# GUI
root = tk.Tk()
root.title("🎨 Artist Login - eStudio")
root.geometry("300x200")

ttk.Label(root, text="Enter Artist ID:", font=("Segoe UI", 12)).pack(pady=20)
entry_id = ttk.Entry(root, width=20)
entry_id.pack(pady=10)
ttk.Button(root, text="Login", command=login).pack(pady=10)

root.mainloop()
