-- Show all confirmed bookings and who is assigned
SELECT 
    a.name AS artist_name,
    b.customer_name,
    b.event_date,
    b.start_time,
    b.duration_hours
FROM artist_assignments aa
JOIN artists a ON aa.artist_id = a.artist_id
JOIN bookings b ON aa.booking_id = b.booking_id
WHERE b.status = 'confirmed'
ORDER BY a.name, b.event_date, b.start_time;
