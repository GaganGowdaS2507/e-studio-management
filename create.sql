
USE estudio_db;


CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    role ENUM('admin', 'artist') NOT NULL
);

CREATE TABLE artists (
    artist_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    contact VARCHAR(20),
    skill ENUM('photography', 'videography', 'both') NOT NULL,
    active BOOLEAN DEFAULT TRUE
);


CREATE TABLE bookings (
    booking_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(100),
    mobile VARCHAR(15),
    event_type VARCHAR(100),
    event_date DATE,
    start_time TIME,
    duration_hours INT,
    venue TEXT,
    artist_type_required ENUM('photography', 'videography', 'both'),
    status ENUM('pending', 'confirmed', 'cancelled') DEFAULT 'pending',
    total_amount DECIMAL(10,2),
    paid_amount DECIMAL(10,2),
    balance_amount DECIMAL(10,2),
    request_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE artist_assignments (
    assignment_id INT AUTO_INCREMENT PRIMARY KEY,
    artist_id INT NOT NULL,
    booking_id INT NOT NULL,
    FOREIGN KEY (artist_id) REFERENCES artists(artist_id),
    FOREIGN KEY (booking_id) REFERENCES bookings(booking_id)
);

CREATE TABLE enquiries (
    enquiry_id INT AUTO_INCREMENT PRIMARY KEY,
    mobile VARCHAR(15),
    enquiry_type VARCHAR(50),
    enquiry_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE bookings
MODIFY COLUMN status VARCHAR(20) DEFAULT 'pending';

ALTER TABLE artist_assignments
ADD COLUMN acknowledged BOOLEAN DEFAULT FALSE,
ADD COLUMN event_completed BOOLEAN DEFAULT FALSE;

show tables
