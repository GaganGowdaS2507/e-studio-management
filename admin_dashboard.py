import tkinter as tk
from tkinter import ttk, messagebox
from ttkbootstrap import Style
import mysql.connector
from datetime import datetime, timedelta, time
import os
import subprocess 
import sys

# Connect to MySQL database
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Root@2507",  # Use your password here
        database="estudio_db"
    )

# Load all pending bookings
def load_pending_bookings():
    for row in booking_tree.get_children():
        booking_tree.delete(row)
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT booking_id, customer_name, event_type, event_date, start_time, duration_hours, artist_type_required FROM bookings WHERE status = 'pending'")
    for row in cursor.fetchall():
        booking_tree.insert('', 'end', values=row)
    cursor.close()
    conn.close()

# Confirm or cancel a booking
def update_booking_status(new_status):
    selected = booking_tree.focus()
    if not selected:
        messagebox.showwarning("No Selection", "Please select a booking.")
        return
    booking_id = booking_tree.item(selected)['values'][0]
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE bookings SET status=%s WHERE booking_id=%s", (new_status, booking_id))
    conn.commit()
    cursor.close()
    conn.close()
    load_pending_bookings()
    load_artist_assign_dropdowns()
    messagebox.showinfo("Success", f"Booking marked as {new_status}.")

# Add artist
def add_artist():
    name = entry_name.get()
    contact = entry_contact.get()
    skill = combo_skill.get()
    if not name or not skill:
        messagebox.showwarning("Missing Data", "Please enter artist name and skill.")
        return
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO artists (name, contact, skill) VALUES (%s, %s, %s)", (name, contact, skill))
    conn.commit()
    conn.close()
    load_artist_list()
    entry_name.delete(0, tk.END)
    entry_contact.delete(0, tk.END)
    combo_skill.set("")
    messagebox.showinfo("Success", "Artist added.")

# Remove selected artist
def remove_artist():
    selected = artist_tree.selection()
    if not selected:
        messagebox.showwarning("Select Artist", "Please select an artist to remove.")
        return

    artist_id = artist_tree.item(selected[0])['values'][0]

    conn = connect_db()
    cursor = conn.cursor()

    # Check if artist is assigned
    cursor.execute("SELECT COUNT(*) FROM artist_assignments WHERE artist_id = %s", (artist_id,))
    assigned_count = cursor.fetchone()[0]

    if assigned_count > 0:
        messagebox.showerror("Cannot Remove", "This artist is currently assigned to bookings.\nUnassign them first.")
        cursor.close()
        conn.close()
        return

    confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to remove this artist?")
    if not confirm:
        cursor.close()
        conn.close()
        return

    try:
        cursor.execute("DELETE FROM artists WHERE artist_id=%s", (artist_id,))
        conn.commit()
        messagebox.showinfo("Deleted", "Artist removed successfully.")
        load_artists()
    except Exception as e:
        messagebox.showerror("Error", str(e))

    cursor.close()
    conn.close()


# Load artist list into tree
def load_artist_list():
    for row in artist_tree.get_children():
        artist_tree.delete(row)
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT artist_id, name, skill FROM artists")
    for row in cursor.fetchall():
        artist_tree.insert('', 'end', values=row)
    cursor.close()
    conn.close()

# Assign artist to booking
def assign_artist_to_booking():
    selected_booking = assign_booking_combo.get()
    selected_artist = assign_artist_combo.get()

    if not selected_booking or not selected_artist:
        messagebox.showwarning("Missing Selection", "Please select both booking and artist.")
        return

    booking_id = int(selected_booking.split(" - ")[0])
    artist_id = int(selected_artist.split(" - ")[0])

    try:
        conn = connect_db()
        cursor = conn.cursor()

        # Get booking details
        cursor.execute("SELECT event_date, start_time, duration_hours, artist_type_required FROM bookings WHERE booking_id=%s", (booking_id,))
        result = cursor.fetchone()
        if not result:
            messagebox.showerror("Error", "Booking not found.")
            return
        b_date, b_start, b_duration, b_required = result

        if isinstance(b_start, timedelta):
            b_start = (datetime.min + b_start).time()

        # Get artist skill
        cursor.execute("SELECT skill FROM artists WHERE artist_id=%s", (artist_id,))
        result = cursor.fetchone()
        if not result:
            messagebox.showerror("Error", "Artist not found.")
            return
        artist_skill = result[0]

        # Skill check with prioritization
        if artist_skill != b_required:
            if artist_skill != 'both' or b_required == 'both':
                messagebox.showerror("Skill Mismatch", f"Artist skill '{artist_skill}' doesn't match required type '{b_required}'.")
                return

        # Check for schedule overlap
        start_dt = datetime.combine(b_date, b_start)
        end_dt = start_dt + timedelta(hours=b_duration)
        cursor.execute("""
            SELECT b.event_date, b.start_time, b.duration_hours
            FROM artist_assignments aa
            JOIN bookings b ON aa.booking_id = b.booking_id
            WHERE aa.artist_id = %s AND b.status = 'confirmed'
        """, (artist_id,))
        for b in cursor.fetchall():
            exist_start_time = b[1]
            if isinstance(exist_start_time, timedelta):
                exist_start_time = (datetime.min + exist_start_time).time()
            exist_start = datetime.combine(b[0], exist_start_time)
            exist_end = exist_start + timedelta(hours=b[2])
            if start_dt < exist_end and end_dt > exist_start:
                messagebox.showerror("Conflict", "Artist is already booked at this time.")
                return

        # Assign artist
        cursor.execute("INSERT INTO artist_assignments (artist_id, booking_id) VALUES (%s, %s)", (artist_id, booking_id))
        conn.commit()
        messagebox.showinfo("Success", f"Artist successfully assigned to booking ID {booking_id}.")
        load_artist_assign_dropdowns()

    except mysql.connector.Error as db_err:
        messagebox.showerror("Database Error", str(db_err))
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def load_artist_assign_dropdowns():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT booking_id, customer_name FROM bookings WHERE status='confirmed'")
    bookings = cursor.fetchall()
    assign_booking_combo['values'] = [f"{b[0]} - {b[1]}" for b in bookings]

    cursor.execute("SELECT artist_id, name FROM artists")
    artists = cursor.fetchall()
    assign_artist_combo['values'] = [f"{a[0]} - {a[1]}" for a in artists]

    conn.close()


def open_artist_dashboard():
    subprocess.Popen([os.path.join(os.getcwd(), "artist_login.exe")])

# def open_artist_dashboard():
#     exe_path = os.path.join(os.getcwd(), "artist_login.exe")
#     py_path = os.path.join(os.getcwd(), "artist_login.py")
    
#     if getattr(sys, 'frozen', False):  # Running from compiled .exe
#         subprocess.Popen([exe_path])
#     else:
#         subprocess.Popen(["python", py_path])


# -------------------- GUI Setup --------------------

root = tk.Tk()
root.title("Admin Dashboard - eStudio")
root.geometry("950x650")

style = Style("superhero")
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill='both', padx=10, pady=10)

ttk.Button(root, text="🎨 Artist Dashboard", command=lambda: subprocess.Popen([os.path.join(os.getcwd(), "artist_login.exe")]), bootstyle="info").pack(pady=10)

# --- TAB 1: Pending Bookings ---
pending_frame = ttk.Frame(notebook, padding=10)
notebook.add(pending_frame, text="Pending Bookings")

booking_tree = ttk.Treeview(pending_frame, columns=("ID", "Customer", "Event", "Date", "Start", "Duration", "Required"), show='headings')
for col in booking_tree["columns"]:
    booking_tree.heading(col, text=col)
booking_tree.pack(expand=True, fill='both')

btn_frame = ttk.Frame(pending_frame)
btn_frame.pack(pady=10)
ttk.Button(btn_frame, text="Confirm", command=lambda: update_booking_status('confirmed')).pack(side='left', padx=10)
ttk.Button(btn_frame, text="Cancel", command=lambda: update_booking_status('cancelled')).pack(side='left', padx=10)

# --- TAB 2: Artist Management ---
artist_frame = ttk.Frame(notebook, padding=10)
notebook.add(artist_frame, text="Manage Artists")

ttk.Label(artist_frame, text="Name").grid(row=0, column=0, sticky='e', padx=5, pady=5)
entry_name = ttk.Entry(artist_frame, width=30)
entry_name.grid(row=0, column=1, padx=5)

ttk.Label(artist_frame, text="Contact").grid(row=1, column=0, sticky='e', padx=5, pady=5)
entry_contact = ttk.Entry(artist_frame, width=30)
entry_contact.grid(row=1, column=1, padx=5)

ttk.Label(artist_frame, text="Skill").grid(row=2, column=0, sticky='e', padx=5, pady=5)
combo_skill = ttk.Combobox(artist_frame, values=["photography", "videography", "both"], width=28, state="readonly")
combo_skill.grid(row=2, column=1, padx=5)

ttk.Button(artist_frame, text="Add Artist", command=add_artist).grid(row=3, column=0, columnspan=2, pady=10)

artist_tree = ttk.Treeview(artist_frame, columns=("ID", "Name", "Skill"), show='headings')
for col in artist_tree["columns"]:
    artist_tree.heading(col, text=col)
artist_tree.grid(row=4, column=0, columnspan=2, pady=10, sticky='nsew')

ttk.Button(artist_frame, text="Remove Selected", command=remove_artist).grid(row=5, column=0, columnspan=2, pady=10)

# --- TAB 3: Assign Artist ---
assign_frame = ttk.Frame(notebook, padding=10)
notebook.add(assign_frame, text="Assign Artist")

ttk.Label(assign_frame, text="Select Confirmed Booking").pack(pady=5)
assign_booking_combo = ttk.Combobox(assign_frame, state="readonly", width=50)
assign_booking_combo.pack(pady=5)

ttk.Label(assign_frame, text="Select Artist").pack(pady=5)
assign_artist_combo = ttk.Combobox(assign_frame, state="readonly", width=50)
assign_artist_combo.pack(pady=5)

ttk.Button(assign_frame, text="Assign Artist", command=assign_artist_to_booking).pack(pady=15)
# --- TAB 4: Artist Dashboard Access ---
dashboard_frame = ttk.Frame(notebook, padding=20)
notebook.add(dashboard_frame, text="Artist Panel")

ttk.Label(dashboard_frame, text="Open Artist Dashboard Interface").pack(pady=10)
ttk.Button(dashboard_frame, text="🎨 Open Artist Login", command=lambda: subprocess.Popen([os.path.join(os.getcwd(), "artist_login.exe")]), bootstyle="info").pack()



# Load everything
load_pending_bookings()
load_artist_list()
load_artist_assign_dropdowns()

root.mainloop()

