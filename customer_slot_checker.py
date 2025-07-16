import tkinter as tk
from tkinter import ttk, messagebox
from ttkbootstrap import Style
import mysql.connector
from datetime import datetime, timedelta, time
import subprocess
import os

# --- Restore slot if available ---
slot_date = slot_time = slot_skill = ""
if os.path.exists("selected_slot.txt"):
    try:
        with open("selected_slot.txt", "r") as f:
            content = f.read().strip()
            if content:
                slot_date, slot_time, slot_skill = content.split("|")
    except:
        pass

# --- DB Connection ---
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Root@2507",
        database="estudio_db"
    )

# --- Check Slot Availability ---
def check_slots():
    date_str = date_entry.get()
    skill_required = skill_combo.get()
    slot_listbox.delete(0, tk.END)
    proceed_button.config(state="disabled")

    if not date_str or not skill_required:
        messagebox.showwarning("Missing Input", "Please select both date and skill.")
        return

    try:
        selected_date = datetime.strptime(date_str, "%d-%m-%Y").date()
    except ValueError:
        messagebox.showerror("Date Format Error", "Enter date as DD-MM-YYYY.")
        return

    conn = connect_db()
    cursor = conn.cursor()

    # Get artist IDs by skill
    if skill_required in ["photography", "videography"]:
        cursor.execute("SELECT artist_id FROM artists WHERE active=1 AND (skill=%s OR skill='both')", (skill_required,))
    else:
        cursor.execute("SELECT artist_id FROM artists WHERE active=1 AND skill='both'")
    artist_ids = [row[0] for row in cursor.fetchall()]

    if not artist_ids:
        messagebox.showinfo("No Artists", "No available artists for selected skill.")
        return

    # Get busy slots for each artist on that date
    artist_busy = {aid: [] for aid in artist_ids}
    for aid in artist_ids:
        cursor.execute("""
            SELECT b.event_date, b.start_time, b.duration_hours
            FROM bookings b
            JOIN artist_assignments aa ON b.booking_id = aa.booking_id
            WHERE b.status = 'confirmed' AND b.event_date = %s AND aa.artist_id = %s
        """, (selected_date, aid))

        for date, start_time, duration in cursor.fetchall():
            # Fix for timedelta issue
            if isinstance(start_time, timedelta):
                start_time = (datetime.min + start_time).time()

            start_dt = datetime.combine(date, start_time)
            end_dt = start_dt + timedelta(hours=duration + 2)  # includes 2-hour buffer
            artist_busy[aid].append((start_dt, end_dt))

    available_slots = []
    for hour in range(8, 20):
        slot_start = time(hour, 0)
        slot_str = f"{slot_start.strftime('%H:%M')} - {(hour + 1):02}:00"
        slot_start_dt = datetime.combine(selected_date, slot_start)
        slot_end_dt = slot_start_dt + timedelta(hours=1)

        # Check conflict per artist
        for aid in artist_ids:
            conflict = any(
                slot_start_dt < busy_end and slot_end_dt > busy_start
                for busy_start, busy_end in artist_busy[aid]
            )
            if not conflict:
                available_slots.append(slot_str)
                slot_listbox.insert(tk.END, f"{slot_str} | Available ✅")
                break
        else:
            slot_listbox.insert(tk.END, f"{slot_str} | Booked ❌")

    if available_slots:
        proceed_button.config(state="normal")

    cursor.close()
    conn.close()

# --- Proceed to Booking ---
def proceed_to_booking():
    selected = slot_listbox.curselection()
    if not selected:
        messagebox.showwarning("No Slot Selected", "Please select an available slot.")
        return

    slot_text = slot_listbox.get(selected[0])
    if "Booked" in slot_text:
        messagebox.showwarning("Unavailable", "Please select a slot marked Available.")
        return

    start_time = slot_text.split(" - ")[0].strip()
    date_str = date_entry.get()
    skill = skill_combo.get()

    with open("selected_slot.txt", "w") as f:
        f.write(f"{date_str}|{start_time}|{skill}")

    subprocess.Popen(["python", "booking_ui.py"])
    root.destroy()

# --- GUI Setup ---
root = tk.Tk()
root.title("Check Free Slots - eStudio")
root.geometry("520x580")
style = Style("litera")

frame = ttk.Frame(root, padding=20)
frame.pack(fill="both", expand=True)

# Date entry
ttk.Label(frame, text="Select Event Date (DD-MM-YYYY):", font=("Segoe UI", 10)).pack(pady=5)
date_entry = ttk.Entry(frame, width=30, font=("Segoe UI", 10))
date_entry.insert(0, slot_date)
date_entry.pack()

# Skill dropdown
ttk.Label(frame, text="Required Artist Skill:", font=("Segoe UI", 10)).pack(pady=5)
skill_combo = ttk.Combobox(frame, values=["photography", "videography", "both"], state="readonly", width=27, font=("Segoe UI", 10))
skill_combo.set(slot_skill)
skill_combo.pack()

# Check button
ttk.Button(frame, text="🔍 Check Availability", command=check_slots, bootstyle="info").pack(pady=10)

# Slot list
ttk.Label(frame, text="Available Time Slots:", font=("Segoe UI", 10)).pack(pady=5)
slot_listbox = tk.Listbox(frame, width=50, height=14, font=("Courier New", 10))
slot_listbox.pack()

# Proceed button
proceed_button = ttk.Button(frame, text="➡️ Proceed to Booking", command=proceed_to_booking, bootstyle="success")
proceed_button.pack(pady=15)
proceed_button.config(state="disabled")

root.mainloop()
