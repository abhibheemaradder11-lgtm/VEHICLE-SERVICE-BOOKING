-- 1. Create the Database
CREATE DATABASE IF NOT EXISTS elite_autocare;
USE elite_autocare;

-- 2. Create the Users Table (Handles both Customers and Admins via the 'role' column)
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(15) NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('customer', 'admin') DEFAULT 'customer',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Create the Appointments Table (Tracks vehicle service requests)
CREATE TABLE IF NOT EXISTS appointments (
    booking_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    vehicle_model VARCHAR(100) NOT NULL,
    vehicle_number VARCHAR(20) NOT NULL,
    service_type VARCHAR(100) NOT NULL,
    booking_date DATE NOT NULL,
    status ENUM('Pending', 'In Progress', 'Completed', 'Cancelled') DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- 4. Create the Service Billing Table (Manages invoices and receipt generation data)
CREATE TABLE IF NOT EXISTS service_billing (
    bill_id INT AUTO_INCREMENT PRIMARY KEY,
    booking_id INT NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    billing_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    payment_status ENUM('Unpaid', 'Paid') DEFAULT 'Unpaid',
    FOREIGN KEY (booking_id) REFERENCES appointments(booking_id) ON DELETE CASCADE
);

-- ==========================================
-- OPTIONAL: SAMPLE SEED DATA FOR TESTING
-- ==========================================

-- Insert an Admin and a Customer (Passwords should be hashed using bcrypt/werkzeug in Flask later)
INSERT INTO users (full_name, email, phone, password, role) VALUES
('System Admin', 'admin@eliteautocare.com', '9876543210', 'adminpass123', 'admin'),
('John Doe', 'johndoe@gmail.com', '9123456789', 'userpass123', 'customer');

-- Insert a sample booking for John Doe (user_id = 2)
INSERT INTO appointments (user_id, vehicle_model, vehicle_number, service_type, booking_date, status) VALUES
(2, 'Hyundai i20', 'KA-25-EA-1234', 'Full General Service', '2026-05-30', 'Pending');

-- Insert a sample billing record for the booking above (booking_id = 1)
INSERT INTO service_billing (booking_id, total_amount, payment_status) VALUES
(1, 4500.00, 'Unpaid');
