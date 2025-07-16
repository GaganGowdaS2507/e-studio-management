import tkinter as tk
from tkinter import ttk, messagebox
from ttkbootstrap import Style
import mysql.connector
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import os
import subprocess

# ---------------- Configuration ----------------
LOGO_PATH = r"C:\Users\sgaga\Downloads\studio_icon.ico"  # Change if needed

# ---------------- Database Connection ----------------
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Root@2507",
        database="estudio_db"
    )

# ---------------- Load Bookings ----------------
def load_confirmed_bookings():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT booking_id, customer_name FROM bookings WHERE status='confirmed'")
    results = cursor.fetchall()
    booking_combo['values'] = [f"{row[0]} - {row[1]}" for row in results]
    cursor.close()
    conn.close()

# ---------------- Fetch Booking Details ----------------
def fetch_payment_details(event=None):
    selected = booking_combo.get()
    if not selected:
        return

    booking_id = selected.split(" - ")[0]
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT customer_name, event_date, start_time, total_amount, paid_amount, balance_amount
        FROM bookings WHERE booking_id = %s
    """, (booking_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    if result:
        name, event_date, start_time, total, paid, balance = result

        if isinstance(start_time, timedelta):
            start_time = (datetime.min + start_time).time()

        current_booking.update({
            "id": int(booking_id),
            "name": name,
            "date": event_date.strftime("%d-%m-%Y"),
            "time": start_time.strftime("%H:%M"),
            "total": float(total),
            "paid": float(paid),
            "balance": float(balance)
        })

        lbl_customer_val.config(text=name)
        lbl_date_val.config(text=current_booking["date"])
        lbl_time_val.config(text=current_booking["time"])
        lbl_total_val.config(text=f"₹ {total:.2f}")
        lbl_paid_val.config(text=f"₹ {paid:.2f}")
        lbl_balance_val.config(text=f"₹ {balance:.2f}")
        entry_new_payment.delete(0, tk.END)

# ---------------- Update Payment ----------------
def update_payment():
    if not booking_combo.get():
        messagebox.showwarning("Select Booking", "Please select a booking.")
        return

    try:
        new_payment = float(entry_new_payment.get().strip())
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid number.")
        return

    current_paid = current_booking["paid"]
    current_balance = current_booking["balance"]

    if new_payment <= 0 or new_payment > current_balance:
        messagebox.showwarning("Invalid Amount", f"Enter amount between ₹0 and ₹{current_balance:.2f}")
        return

    if not messagebox.askyesno("Confirm Payment", f"Confirm to add ₹{new_payment:.2f}?"):
        return

    updated_paid = current_paid + new_payment
    updated_balance = current_balance - new_payment

    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE bookings
            SET paid_amount = %s, balance_amount = %s
            WHERE booking_id = %s
        """, (updated_paid, updated_balance, current_booking["id"]))
        conn.commit()
        cursor.close()
        conn.close()

        # Show preview before saving
        preview_text = (
            f"Generate Receipt for:\n\n"
            f"Booking ID: {current_booking['id']}\n"
            f"Customer: {current_booking['name']}\n"
            f"New Payment: ₹{new_payment:.2f}\n\n"
            f"Proceed to save receipt?"
        )
        if messagebox.askyesno("Receipt Preview", preview_text):
            generate_pdf_receipt(new_payment)

        messagebox.showinfo("Success", "Payment updated successfully.")
        fetch_payment_details()

    except Exception as e:
        messagebox.showerror("Database Error", str(e))

# ---------------- Generate PDF Receipt ----------------
def generate_pdf_receipt(amount_paid):
    booking_id = current_booking["id"]
    year = datetime.now().year
    receipt_number = f"SBH{year}{str(booking_id).zfill(5)}"
    customer_folder = current_booking['name'].replace(" ", "_")
    receipt_dir = os.path.join(os.getcwd(), "receipts", customer_folder)
    os.makedirs(receipt_dir, exist_ok=True)

    filename = f"receipt_{receipt_number}.pdf"
    filepath = os.path.join(receipt_dir, filename)

    c = canvas.Canvas(filepath, pagesize=A4)
    width, height = A4

    # Try to draw logo
    try:
        logo = ImageReader(LOGO_PATH)
        c.drawImage(logo, 40, height - 110, width=100, preserveAspectRatio=True, mask='auto')
    except:
        pass

    c.setFont("Helvetica-Bold", 16)
    c.drawString(160, height - 60, "eStudio - Payment Receipt")
    c.setFont("Helvetica", 10)
    c.drawString(160, height - 75, f"Receipt No: {receipt_number}")
    c.line(40, height - 120, width - 40, height - 120)

    # Content
    c.setFont("Helvetica", 12)
    lines = [
        f"Booking ID: {booking_id}",
        f"Customer Name: {current_booking['name']}",
        f"Event Date: {current_booking['date']}",
        f"Event Time: {current_booking['time']}",
        f"Total Amount: ₹ {current_booking['total']:.2f}",
        f"Previously Paid: ₹ {current_booking['paid']:.2f}",
        f"New Payment Made: ₹ {amount_paid:.2f}",
        f"Updated Balance: ₹ {current_booking['balance'] - amount_paid:.2f}",
        f"Date of Payment: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}"
    ]

    y = height - 160
    for line in lines:
        c.drawString(50, y, line)
        y -= 20

    c.setFont("Helvetica-Oblique", 11)
    c.drawString(50, y - 30, "'MOVEMENTS CAN'T BE RECREATED, SO WE CAPTURE THEM FOR YOU'")
    c.drawString(50, y - 50, "Thank you for your payment!")

    c.save()
    messagebox.showinfo("Receipt Saved", f"Saved at: {filepath}")
    try:
        subprocess.Popen(['start', '', filepath], shell=True)
    except:
        pass

# ---------------- Return to Main Menu ----------------
def return_to_main():
    root.destroy()
    subprocess.Popen(["python", "main_app.py"])

# ---------------- GUI ----------------
root = tk.Tk()
root.title("💳 Update Payments - eStudio")
root.geometry("620x580")
style = Style("flatly")

current_booking = {}
frame = ttk.Frame(root, padding=20)
frame.pack(fill='both', expand=True)

ttk.Label(frame, text="📝 Payment Update Portal", font=("Segoe UI", 16, "bold")).grid(
    row=0, column=0, columnspan=2, pady=(0, 10)
)

# Dropdown
ttk.Label(frame, text="Select Confirmed Booking:", font=("Segoe UI", 10)).grid(row=1, column=0, sticky='w', pady=5)
booking_combo = ttk.Combobox(frame, state="readonly", width=40, font=("Segoe UI", 10))
booking_combo.grid(row=1, column=1, pady=5, sticky='w')
booking_combo.bind("<<ComboboxSelected>>", fetch_payment_details)

# Info section
info_frame = ttk.LabelFrame(frame, text=" Booking & Payment Details ", padding=15, bootstyle="primary")
info_frame.grid(row=2, column=0, columnspan=2, pady=15, sticky='ew')

def label_row(row, text, label, color=None):
    ttk.Label(info_frame, text=text, font=("Segoe UI", 10)).grid(row=row, column=0, sticky='w', pady=4)
    if color:
        label.config(foreground=color, font=("Segoe UI", 10, "bold"))
    label.grid(row=row, column=1, sticky='w', pady=4)

lbl_customer_val = ttk.Label(info_frame, text="")
lbl_date_val = ttk.Label(info_frame, text="")
lbl_time_val = ttk.Label(info_frame, text="")
lbl_total_val = ttk.Label(info_frame, text="")
lbl_paid_val = ttk.Label(info_frame, text="")
lbl_balance_val = ttk.Label(info_frame, text="")

label_row(0, "Customer Name:", lbl_customer_val)
label_row(1, "Event Date:", lbl_date_val)
label_row(2, "Event Time:", lbl_time_val)
label_row(3, "Total Amount:", lbl_total_val, "#117A65")
label_row(4, "Paid Amount:", lbl_paid_val, "#1A5276")
label_row(5, "Balance Amount:", lbl_balance_val, "#922B21")

# New payment
ttk.Label(frame, text="Enter New Payment:", font=("Segoe UI", 10)).grid(row=3, column=0, sticky='w', pady=(5, 0))
entry_new_payment = ttk.Entry(frame, width=30, font=("Segoe UI", 10))
entry_new_payment.grid(row=3, column=1, pady=(5, 10), sticky='w')

# Buttons
ttk.Button(frame, text="💰 Update Payment", command=update_payment, bootstyle="success").grid(row=4, column=0, columnspan=2, pady=10)
ttk.Button(frame, text="🔙 Back to Main Menu", command=return_to_main, bootstyle="secondary").grid(row=5, column=0, columnspan=2, pady=5)

# Load data
load_confirmed_bookings()
root.mainloop()
