# Flask_Project_ebill_application

Introduction
The E-Bill Application is a web-based platform developed using Flask, SQLite, and Flask-Mail. This application provides functionalities for administrators to manage bills, customers to register and pay bills, and both parties to handle complaints effectively.
________________________________________
Getting Started
Prerequisites
1.	Install Python (version 3.7 or above).
2.	Install the required libraries using pip:
bash
Copy code
pip install flask flask-mail sqlite3
3.	Ensure you have the database file CaseStudy.db in the application directory. This file should include tables for:
o	Customers
o	Bills
o	Complaints
o	Receipts
4.	Place all HTML templates in a templates folder within the application directory.
________________________________________
Running the Application
1.	Navigate to the directory where the application code is stored.
2.	Run the application using the command:
bash
Copy code
python main.py
3.	Open your browser and go to http://127.0.0.1:5000.
________________________________________

Admin Login
1.	Access the Admin Login page.
o	URL: http://127.0.0.1:5000
2.	Use the following credentials:
o	Username: Admin_123
o	Password: Admin_TCS@python1
3.	After logging in, you can:
o	Add bills for customers.
o	View all customers and complaints.
o	Manage bill statuses.
o	Resolve complaints.
________________________________________
Workflow
Step 1: Adding Bills
1.	Login as Admin using the credentials provided above.
2.	Go to the Add Bill page by selecting the relevant menu option.
3.	Enter the details:
o	Customer ID: Unique identifier for the customer.
o	Bill Number: Auto-generated or manually set.
o	Month: The billing period.
o	Amount: The payable and due amounts.
o	Status: Set as "Unpaid" or "Pending."
4.	Save the bill.
________________________________________
Step 2: Registering a New Customer
1.	Go to the Registration page:
o	URL: http://127.0.0.1:5000/registration
2.	Use the Customer ID and Bill Number provided by the Admin.
3.	Fill out the registration form with valid personal details and submit.
Step 3: Logging in as a Customer
1.	Once registered, login as a customer using the credentials you provided during registration.
2.	You will be able to:
o	View your bills.
o	Pay bills using the Payment Gateway.
o	Raise complaints regarding billing or service issues.
________________________________________
Step 4: Paying Bills
1.	Navigate to the Pay Bill page.
2.	Select the unpaid bills and proceed to payment.
3.	Upon successful payment:
o	A receipt will be generated with a unique transaction number.
o	The status of the bill will be updated to "Paid."
________________________________________
Step 5: Complaints
1.	Raise a Complaint:
o	Go to the Complaint section.
o	Fill out the form with details like type, category, and problem description.
o	Submit the complaint to receive a unique Complaint ID.
2.	Check Complaint Status:
o	Use the Complaint ID to track the status (e.g., "Pending," "In Progress," "Resolved").
3.	Admins can manage complaints and update their statuses as resolved.
________________________________________
Step 6: Viewing Tables
To see specific database tables (admin only):
1.	Bills Table: Access http://127.0.0.1:5000/bview.
2.	Complaints Table: Access http://127.0.0.1:5000/cview.
3.	Customers Table: Access http://127.0.0.1:5000/view.
4.	Receipts Table: Access http://127.0.0.1:5000/rview.
________________________________________
Additional Information
Tools & Technologies Used
1.	Flask: Web framework for Python.
2.	SQLite: Lightweight database management.
3.	Flask-Mail: For sending confirmation and notification emails.
Note
•	The application assumes the database (CaseStudy.db) is pre-configured with tables and schemas required for its functionality.
•	Ensure the Flask-Mail configuration is properly set up to send emails
