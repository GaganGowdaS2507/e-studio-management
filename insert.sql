USE estudio_db;

-- Insert admin user (used for admin_login.py)
INSERT INTO users (username, password, role)
VALUES ('admin', 'admin123', 'admin');

-- Insert sample artists
INSERT INTO artists (name, contact, skill)
VALUES 
('Ravi Kumar', '9876543210', 'photography'),
('Anjali Verma', '9123456789', 'videography'),
('Manish Sharma', '9012345678', 'both');

-- Insert a pending booking
INSERT INTO bookings (
    customer_name, mobile, event_type, event_date,
    start_time, duration_hours, venue, artist_type_required,
    status, total_amount, paid_amount, balance_amount
) VALUES (
    'Karan Mehta', '9988776655', 'Wedding Ceremony', '2025-06-25',
    '15:00:00', 3, 'Royal Garden, Bengaluru', 'both',
    'pending', 15000.00, 5000.00, 10000.00
);

-- Insert a confirmed booking (for testing artist assignment)
INSERT INTO bookings (
    customer_name, mobile, event_type, event_date,
    start_time, duration_hours, venue, artist_type_required,
    status, total_amount, paid_amount, balance_amount
) VALUES (
    'Shruti Rao', '8844556677', 'Birthday Party', '2025-06-24',
    '11:00:00', 2, 'Green Lawn, Mysuru', 'photography',
    'confirmed', 8000.00, 8000.00, 0.00
);

-- Optional: Assign artist to confirmed booking (already assigned artist)
INSERT INTO artist_assignments (artist_id, booking_id)
VALUES (1, 2);  -- Ravi Kumar assigned to Shruti Rao's birthday

-- Insert an enquiry (for testing enquiry feature)
INSERT INTO enquiries (mobile, enquiry_type)
VALUES 
('9988776655', 'Booking Status'),
('8844556677', 'Free Slot Check');
