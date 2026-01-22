Cyber Café Management System (CCMS)
Overview
The Cyber Café Management System (CCMS) is a web-based academic project designed to automate and digitalize daily cyber café operations such as customer management, session tracking, billing, and reporting. The system emphasizes strong DBMS design principles and HCI usability concepts to ensure accuracy, efficiency, and ease of use.
This project was developed as part of the DBMS and HCI coursework.

Tech Stack
* Frontend: HTML, CSS, JavaScript

* Database: MySQL

* Tools: Visual Studio Code

* Browser: Chrome / Edge

Key Features
DBMS Features
* ER modeling with normalization up to Third Normal Form (3NF)
* Structured relational database for customers, sessions, billing, and services
* Ensures data integrity and reduced redundancy
* Automated billing based on session duration
HCI Features
* Role-based interfaces for Admin, Staff, and Customer
* Clear navigation and consistent feedback
* Minimal input effort for routine tasks
* User-friendly and intuitive interface design

Functional Modules
* User Authentication (Admin / Staff / Customer)
* Customer Registration and Management
* Computer Allocation and Session Tracking
* Automated Billing and Payment Records
* Membership Management
* Complaints and Feedback Handling
* Maintenance and Inventory Records
* Usage and Revenue Report Generation

System Requirements
Hardware Requirements
* Processor: Intel i5 or higher
* RAM: 8 GB
* Storage: 100 GB
* Internet Connectivity
Software Requirements
* Windows Operating System
* MySQL Server
* Visual Studio Code
* Chrome / Edge Browser

Installation & Execution Instructions
Step 1: Clone the Repository
git clone https://github.com/your-username/cyber-cafe-management-system.git
cd cyber-cafe-management-system

Step 2: Database Setup
1. Install MySQL Server.
2. Open MySQL Command Line or MySQL Workbench.
3. Create a new database:
CREATE DATABASE ccms;
4. Import the database file:
USE ccms;
SOURCE database/ccms.sql;
Ensure that the MySQL service is running before proceeding.

Step 3: Configure Database Connection
1. Open the database configuration file (e.g., db.js or config.js).
2. Update database credentials:
host: "localhost",
user: "root",
password: "your_password",
database: "ccms"

Step 4: Run the Application
* Open the project folder in Visual Studio Code.
* Open index.html using:
o Live Server extension, or
o Directly open the file in a web browser
Right-click ? Open with Live Server

Step 5: Access the System
* Admin Login: Manage customers, rates, billing, and reports
* Customer Login: Start sessions and access services

Default Credentials (Demo)
RoleUsernamePasswordAdminadminadmin123Customerdemodemo123Note: Change credentials after first login.

Project Structure
ccms/
??? database/
?   ??? ccms.sql
??? css/
??? js/
??? images/
??? index.html
??? admin.html
??? customer.html
??? README.md

Future Enhancements
* Online computer reservation system
* Email/SMS notifications
* Mobile-responsive UI
* Advanced analytics dashboard

Academic Information
* Project Type: Academic Mini Project
* Course: DBMS & HCI
* Department: Computer Engineering
* Institute: Pimpri Chinchwad College of Engineering & Research, Pune
* Project Guide: Mrs. Sonali Lunawat

Authors
* Nimish Khairnar
* Vaishnav Pawar
* Aditya Sutar
