CREATE DATABASE IF NOT EXISTS leave_management;
USE leave_management;

CREATE TABLE time_off_requests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employee_name VARCHAR(100) NOT NULL,
    time_off_type ENUM('Paid Time Off','Sick Leave','Unpaid Leave') NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    allocation_days INT NOT NULL,
    status ENUM('Pending','Approved','Rejected') DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
