# e-studio-management
📸 A desktop application for managing bookings, artists, and payments in a photography/videography studio using Python and MySQL.
---

## 💻 Tech Stack

- Python (Tkinter for GUI)
- MySQL (backend database)
- ttkbootstrap (UI styling)
- tkcalendar (date input)
- mysql-connector-python (database connectivity)
- FPDF (PDF report generation)
- PyInstaller (for creating .exe)

---

## 🚀 Features

- 🔐 Admin login: confirm/cancel bookings, assign artists, manage payments
- 👨‍🎨 Artist login: view assigned events and contact details
- 📆 Customer/receptionist access: book events, check booking status, slot availability
- 🧾 Export reports to PDF/CSV
- 💾 MySQL backend with 5 main tables

---

## 🗃️ Folder Structure
e-studio-management/
e-studio-management/
├── main_app.py
├── admin_dashboard.py
├── artist_login.py
├── artist_dashboard.py
├── admin_login.py
├── new_booking_form.py
├── booking_ui.py
├── booking_status_enquiry.py
├── update_payments_ui.py
├── customer_slot_checker.py
├── selected_slot.txt                  # (if needed)
├── studio_icon.ico                    # (for PyInstaller or app branding)
├── requirements.txt                   # (generate it)
├── README.md
├── database/
│   └── estudio_db_schema.sql         # include SQL schema
├── screenshots/
│   └── dashboard.png                 # sample UI screenshots
├── receipts/                         # optional folder for PDF samples
│   └── receipt_booking_1.pdf


## ▶️ How to Run

After setting up the folder and database:
```bash
pip install -r requirements.txt
```

## Launch the application:
```bash
python main_app.py
```
python main_app.py
## ✅ Make sure your MySQL server is running and the estudio_db database is created using:

pgsql
Copy code
database/estudio_db_schema.sql

