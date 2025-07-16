import tkinter as tk
from tkinter import ttk, messagebox
from ttkbootstrap import Style
import mysql.connector
from decimal import Decimal
from datetime import date, time, timedelta

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Root@2507",
        database="estudio_db"
    )

def format_time(value):
    if isinstance(value, time):
        return value.strftime("%H:%M")
    elif isinstance(value, timedelta):
        # Convert timedelta to total seconds, then to hours:minutes
        total_seconds = int(value.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        return f"{hours:02d}:{minutes:02d}"
    elif isinstance(value, str):
        return value
    else:
        return "Unknown Time"


def search_booking():
    booking_id = entry_id.get().strip()
    if not booking_id.isdigit():
        messagebox.showwarning("Invalid", "Please enter a valid Booking ID (number only).")
        return

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bookings WHERE booking_id=%s", (booking_id,))
    booking = cursor.fetchone()
    cursor.close()
    conn.close()

    result_box.delete("1.0", tk.END)

    if not booking:
        result_box.insert(tk.END, "❌ No booking found with this Booking ID.")
        return

    (
        booking_id, name, mobile, event_type, event_date,
        start_time, duration, venue, artist_type,
        status, total, paid, balance, _  # _ for request_time
    ) = booking

    # Safely convert values for formatting
    total = float(total) if isinstance(total, Decimal) else total
    paid = float(paid) if isinstance(paid, Decimal) else paid
    balance = float(balance) if isinstance(balance, Decimal) else balance

    result_box.insert(tk.END, f"""
                      
    
------------------------------
📄 Booking ID: {booking_id}
👤 Customer: {name}
📞 Mobile: {mobile}
🎉 Event: {event_type}
🎨 Artist Needed: {artist_type}
📅 Date: {event_date.strftime('%d-%m-%Y')}
⏰ Time: {format_time(start_time)}
⏳ Duration: {duration} hrs
📍 Venue: {venue.strip()}
📦 Status: {str(status).upper()}
👥 Artists: [Assigned by Admin]
💰 Payment: ₹{paid:.2f} paid of ₹{total:.2f} (Balance ₹{balance:.2f})
------------------------------
""")

# GUI Setup
root = tk.Tk()
root.title("🔎 Booking Status Enquiry - eStudio")
root.geometry("650x600")
style = Style("flatly")

frame = ttk.Frame(root, padding=20)
frame.pack(fill="both", expand=True)

ttk.Label(frame, text="Enter Booking ID:", font=("Segoe UI", 10)).pack(pady=5)
entry_id = ttk.Entry(frame, width=40)
entry_id.pack(pady=5)

ttk.Button(frame, text="Check Status", command=search_booking, bootstyle="info").pack(pady=10)

ttk.Label(frame, text="Booking Details:").pack(pady=5)
result_box = tk.Text(frame, width=75, height=20)
result_box.pack()

ttk.Button(frame, text="🔙 Back", command=root.destroy, bootstyle="secondary").pack(pady=10)

root.mainloop()
