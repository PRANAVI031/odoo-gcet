Description of CoreHR
Authentication Module – CoreHR / Dayflow

This module implements a complete authentication system for the CoreHR platform. It supports secure company onboarding, automatic login ID generation, password protection, and user access handling.
Key Features
Company Admin signup with the following inputs:
Company name, first name, last name, email, phone, password
Automatic Login ID generation
Based on company initials, user initials, year, and yearly running serial
Example: MOSATE20260009
Displayed to the user after signup via popup
Secure Login functionality
Login using Login ID or Email
Password stored using PBKDF2 SHA256 hashing
Frontend validation
Valid email format check
Phone number must be 10 digits

Password requires:
Minimum 7 characters
At least 1 uppercase letter
At least 1 number
At least 1 special character
Confirm password validation and password show/hide toggle
Forgot Password workflow (prototype)
Forgot password page
OTP verification page (demo OTP: 123456)
Reset password page

Tech Stack
Flask, MySQL, Passlib, HTML, CSS, JavaScript

Status
Signup, login, validation, and popup functionality fully working. Forgot password screens and demo OTP implemented and ready for future email integration.


MODULE -  Leave & Time-Off Management
The Leave & Time-Off Management module is designed to make the leave application and approval process simple, transparent, and efficient for both employees and administrators.

--Employee Side--
From the employee’s perspective, this module allows them to easily apply for leave through a dedicated Time-Off section. The employee can:
Select the type of leave (Paid Time Off, Sick Leave, or Unpaid Leave)
Choose a start date and end date, after which the system automatically calculates the total number of leave days
Upload supporting documents (such as a medical certificate) as proof when required
Submit the leave request, which is then stored securely in the database
Once submitted, the employee can immediately view their leave history on the same page, along with the current status of each request (Pending, Approved, or Rejected).
Importantly, an employee can only see their own leave records, ensuring privacy and data integrity.

--Admin Side--
On the admin side, this module provides a centralized dashboard where all employee leave requests are displayed in an organized table. The admin can:
View all leave applications submitted by employees
Check important details such as leave dates, leave type, total days, and uploaded proof documents
Open and verify attachments directly from the system
Approve or reject leave requests using clear action buttons
Any action taken by the admin is reflected instantly on the employee’s Time-Off page, ensuring real-time synchronization between both sides.

Dynamic Employee Dashboard

After login/signup, employees are displayed on the dashboard as employee cards
Each card shows:
Employee name
Role / designation
Attendance status (present/absent – demo)
The dashboard dynamically fetches employee data from the backend database
My Profile Section
Clicking on an employee navigates to the My Profile page
The profile page displays detailed employee information such as:
Basic personal details
Job role and company information
Additional sections like Resume, Private Info, Salary Info, and Security (UI ready)
The profile layout is designed to support future dynamic data integration

