# new_booking_form.py
import tkinter as tk
from tkinter import ttk, messagebox
from ttkbootstrap import Style
import mysql.connector
from datetime import datetime
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader


# Check if launched via selected_slot.txt
launched_from_slot_checker = os.path.exists("selected_slot.txt")
prefill_date, prefill_time, prefill_skill = "", "", ""
if launched_from_slot_checker:
    try:
        with open("selected_slot.txt", "r") as f:
            prefill_date, prefill_time, prefill_skill = f.read().strip().split("|")
    except:
        launched_from_slot_checker = False

def connect_db():
    return mysql.connector.connect(
        host="localhost", user="root", password="Root@2507", database="estudio_db"
    )

def calculate_balance(*args):
    try:
        total = float(entry_total.get())
        paid = float(entry_paid.get())
        balance_var.set(f"{total - paid:.2f}")
    except:
        balance_var.set("")

def generate_pdf_receipt_new(booking_id, name, date, time, total, paid, balance):
    year = datetime.now().year
    receipt_number = f"SBH{year}{str(booking_id).zfill(5)}"
    customer_folder = name.replace(" ", "_")
    receipt_dir = os.path.join(os.getcwd(), "receipts", customer_folder)
    os.makedirs(receipt_dir, exist_ok=True)

    filename = f"receipt_{receipt_number}.pdf"
    filepath = os.path.join(receipt_dir, filename)

    c = canvas.Canvas(filepath, pagesize=A4)
    width, height = A4

    # Optional: logo drawing
    try:
        logo = ImageReader("logo.png")  # update path if needed
        c.drawImage(logo, 40, height - 110, width=100, preserveAspectRatio=True, mask='auto')
    except:
        pass

    c.setFont("Helvetica-Bold", 16)
    c.drawString(160, height - 60, "eStudio - Booking Receipt")
    c.setFont("Helvetica", 10)
    c.drawString(160, height - 75, f"Receipt No: {receipt_number}")
    c.line(40, height - 120, width - 40, height - 120)

    lines = [
        f"Booking ID: {booking_id}",
        f"Customer Name: {name}",
        f"Event Date: {date}",
        f"Event Time: {time}",
        f"Total Amount: ₹ {float(total):.2f}",
        f"Paid: ₹ {float(paid):.2f}",
        f"Balance: ₹ {float(balance):.2f}",
        f"Booking Time: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}"
    ]

    y = height - 160
    c.setFont("Helvetica", 12)
    for line in lines:
        c.drawString(50, y, line)
        y -= 20

    c.setFont("Helvetica-Oblique", 11)
    c.drawString(50, y - 30, "'MOVEMENTS CAN'T BE RECREATED, SO WE CAPTURE THEM FOR YOU'")
    c.drawString(50, y - 50, "Thank you for booking with us!")

    c.save()

    try:
        subprocess.Popen(['start', '', filepath], shell=True)
    except:
        pass


def submit_booking():
    name = entry_name.get().strip()
    mobile = entry_mobile.get().strip()
    event_type = entry_event_type.get().strip()
    artist_needed = artist_type.get()
    date = entry_date.get().strip()
    time = entry_time.get().strip()
    duration = entry_duration.get().strip()
    venue = text_venue.get("1.0", tk.END).strip()
    total = entry_total.get().strip()
    paid = entry_paid.get().strip()
    balance = balance_var.get()

    if not (name and mobile and event_type and artist_needed and date and time and duration and venue and total and paid):
        messagebox.showwarning("Missing Info", "Please fill all the required fields.")
        return

    summary = f"""
Name: {name}
Mobile: {mobile}
Event Type: {event_type}
Artist Needed: {artist_needed}
Date: {date}
Time: {time}
Duration: {duration} hrs
Venue: {venue}
Total: ₹{total} | Paid: ₹{paid} | Balance: ₹{balance}
    """
    if not messagebox.askyesno("Confirm Booking", summary.strip()):
        return

    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO bookings (
                customer_name, mobile, event_type, artist_type_required,
                event_date, start_time, duration_hours, venue,
                total_amount, paid_amount, balance_amount
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            name, mobile, event_type, artist_needed,
            datetime.strptime(date, "%d-%m-%Y").date(),
            datetime.strptime(time, "%H:%M").time(),
            int(duration), venue,
            float(total), float(paid), float(balance)
        ))
        conn.commit()
        booking_id = cursor.lastrowid
        cursor.close()
        conn.close()

        if os.path.exists("selected_slot.txt"):
            os.remove("selected_slot.txt")

        generate_pdf_receipt_new(
            booking_id=booking_id,
            name=name,
            date=date,
            time=time,
            total=total,
            paid=paid,
            balance=balance
        )

        messagebox.showinfo("Success", "Booking submitted and receipt generated!")
        root.destroy()

    except Exception as e:
        messagebox.showerror("Error", str(e))

# GUI
root = tk.Tk()
root.title("📝 New Booking Form - eStudio")
root.geometry("650x750")
Style("flatly")

frame = ttk.Frame(root, padding=20)
frame.pack(fill="both", expand=True)

def add_label_entry(row, label, widget):
    ttk.Label(frame, text=label).grid(row=row, column=0, sticky="w", pady=5)
    widget.grid(row=row, column=1, pady=5)

entry_name = ttk.Entry(frame, width=40)
add_label_entry(0, "Customer Name", entry_name)

entry_mobile = ttk.Entry(frame, width=40)
add_label_entry(1, "Mobile Number", entry_mobile)

entry_event_type = ttk.Entry(frame, width=40)
add_label_entry(2, "Event Type", entry_event_type)

artist_type = ttk.Combobox(frame, values=["photography", "videography", "both"], width=38)
artist_type.set(prefill_skill or "photography")
add_label_entry(3, "Artist Needed", artist_type)
if launched_from_slot_checker:
    artist_type.config(state="readonly")

entry_date = ttk.Entry(frame, width=40)
entry_date.insert(0, prefill_date)
add_label_entry(4, "Event Date (DD-MM-YYYY)", entry_date)
if launched_from_slot_checker:
    entry_date.config(state="readonly")

entry_time = ttk.Entry(frame, width=40)
entry_time.insert(0, prefill_time)
add_label_entry(5, "Start Time (HH:MM)", entry_time)
if launched_from_slot_checker:
    entry_time.config(state="readonly")

entry_duration = ttk.Entry(frame, width=40)
add_label_entry(6, "Duration (Hours)", entry_duration)

ttk.Label(frame, text="Venue").grid(row=7, column=0, sticky="nw", pady=5)
text_venue = tk.Text(frame, width=30, height=4)
text_venue.grid(row=7, column=1, pady=5)

entry_total = ttk.Entry(frame, width=40)
add_label_entry(8, "Total Amount", entry_total)

entry_paid = ttk.Entry(frame, width=40)
add_label_entry(9, "Paid Amount", entry_paid)

balance_var = tk.StringVar()
entry_balance = ttk.Entry(frame, textvariable=balance_var, width=40, state="readonly")
add_label_entry(10, "Balance", entry_balance)

entry_total.bind("<KeyRelease>", calculate_balance)
entry_paid.bind("<KeyRelease>", calculate_balance)

btn_frame = ttk.Frame(frame)
btn_frame.grid(row=11, column=0, columnspan=2, pady=20)
ttk.Button(btn_frame, text="🔙 Back", command=root.destroy, bootstyle="secondary").pack(side="left", padx=10)
ttk.Button(btn_frame, text="✅ Submit Booking", command=submit_booking, bootstyle="success").pack(side="left", padx=10)

root.mainloop()
