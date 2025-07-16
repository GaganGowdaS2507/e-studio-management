import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import sys
from datetime import datetime, timedelta

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Root@2507",
        database="estudio_db"
    )

def fetch_bookings(artist_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            b.booking_id, b.customer_name, b.mobile, b.event_type, 
            b.event_date, b.start_time, b.duration_hours, b.venue
        FROM 
            artist_assignments AS aa
        JOIN 
            bookings AS b ON aa.booking_id = b.booking_id
        WHERE 
            aa.artist_id = %s AND b.status = 'confirmed'
    """, (artist_id,))
    bookings = cursor.fetchall()
    cursor.close()
    conn.close()
    return bookings

def get_artist_name(artist_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM artists WHERE artist_id = %s", (artist_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else "Unknown"

# Booking actions (can be extended to update DB if needed)
def confirm_acknowledgement(booking_id):
    messagebox.showinfo("Acknowledged", f"You have confirmed acknowledgment for Booking ID {booking_id}.")

def mark_completed(booking_id):
    messagebox.showinfo("Completed", f"You have marked Booking ID {booking_id} as completed.")

# Entry point
if len(sys.argv) < 2:
    messagebox.showerror("Missing", "Artist ID not provided.")
    sys.exit()

artist_id = sys.argv[1]
artist_name = get_artist_name(artist_id)

root = tk.Tk()
root.title(f"🎨 Artist Dashboard - {artist_name} (ID: {artist_id})")
root.geometry("900x550")

ttk.Label(root, text=f"Welcome, {artist_name}!", font=("Segoe UI", 14, "bold")).pack(pady=10)

tree = ttk.Treeview(root, columns=("Booking ID", "Customer", "Mobile", "Event", "Date", "Time", "Duration", "Venue"), show="headings")
for col in tree["columns"]:
    tree.heading(col, text=col)
    tree.column(col, anchor="center")
tree.pack(fill="both", expand=True, padx=10)

bookings = fetch_bookings(artist_id)
for b in bookings:
    tree.insert("", "end", values=b)

btn_frame = ttk.Frame(root)
btn_frame.pack(pady=15)

def on_confirm():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Select", "Please select a booking first.")
        return
    data = tree.item(selected[0])["values"]
    confirm_acknowledgement(data[0])

def on_complete():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Select", "Please select a booking first.")
        return
    data = tree.item(selected[0])["values"]
    mark_completed(data[0])

ttk.Button(btn_frame, text="✅ Confirm Acknowledgement", command=on_confirm).pack(side="left", padx=10)
ttk.Button(btn_frame, text="✅ Mark as Completed", command=on_complete).pack(side="left", padx=10)
ttk.Button(btn_frame, text="🔙 Exit", command=root.destroy).pack(side="left", padx=10)

root.mainloop()
