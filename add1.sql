-- Set the database
USE estudio_db;

🔐 1. View all users (admin and artist login data)
SELECT * FROM users;

-- 👨‍🎨 2. View all artists
SELECT * FROM artists;

-- 📋 2.1 View only photographers
SELECT * FROM artists WHERE skill = 'photography';

-- 📋 2.2 View only videographers
SELECT * FROM artists WHERE skill = 'videography';

-- 📋 2.3 View artists who do both
SELECT * FROM artists WHERE skill = 'both';

-- 📆 3. View all bookings
SELECT * FROM bookings;

-- 📆 3.1 View only pending bookings
SELECT * FROM bookings WHERE status = 'pending';

-- 📆 3.2 View only confirmed bookings
SELECT * FROM bookings WHERE status = 'confirmed';

-- 📆 3.3 View only cancelled bookings
SELECT * FROM bookings WHERE status = 'cancelled';

-- 💰 3.4 View bookings with balance payments pending
SELECT * FROM bookings WHERE balance_amount > 0;

-- 📍 4. View all artist assignments
SELECT * FROM artist_assignments;

-- 📍 4.1 View full assignment details with artist and booking info
SELECT 
    aa.assignment_id,
    a.name AS artist_name,
    a.skill,
    b.customer_name,
    b.event_type,
    b.event_date,
    b.start_time,
    b.duration_hours,
    b.venue
FROM artist_assignments aa
JOIN artists a ON aa.artist_id = a.artist_id
JOIN bookings b ON aa.booking_id = b.booking_id;

-- 🧾 5. View all enquiries (e.g., status check, free slot checks)
SELECT * FROM enquiries;

-- 🧾 5.1 View enquiries of type 'Booking Status'
SELECT * FROM enquiries WHERE enquiry_type = 'Booking Status';

-- -- 🧾 5.2 View enquiries of type 'Free Slot Check'
SELECT * FROM enquiries WHERE enquiry_type = 'Free Slot Check';
SELECT 
    b.booking_id, b.customer_name, b.mobile, b.event_type, b.event_date, 
    b.start_time, b.duration_hours, b.venue,
    aa.assignment_id
FROM 
    artist_assignments AS aa
JOIN 
    bookings AS b ON aa.booking_id = b.booking_id
JOIN 
    artists AS ar ON aa.artist_id = ar.artist_id
WHERE 
    aa.artist_id = 1;

