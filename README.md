------------------------------Complaint Management System--------------------------------------------
A menu-driven Complaint Management System built with Python and MySQL. The application provides separate member and administrator workflows for submitting complaints, tracking their status, maintaining member profiles, and managing complaint categories.
1. Features:-
Member:
- Register a member account and log in.
- Create and update a personal profile.
- Browse available complaint categories.
- Submit a complaint with a subject, description, and date.
- View previously submitted complaints and their status.
- View individual complaint details and administrator remarks.
Administrator:
- Log in through the administrator menu.
- View all submitted complaints.
- Update complaint status to Pending, In Progress, Resolved, or Rejected.
- Add complaint categories.
- View member profiles.
Database:
The application is designed to use MySQL tables for
- users — login account and role information.
- profiles — member contact/profile information.
- categories — complaint categories.
- complaints — complaint descriptions, dates, statuses, and administrator remarks.

Tech Stack
- Language: Python 3
- Database: MySQL
- Python package: mysql-connector-python


Repository Structure
complaint-management-system/
├─ main.py
├─ requirements.txt
├─ README.md


Prerequisites
- Python 3 installed
- MySQL Server installed and running
- A MySQL account with permission to create a database and tables

Installation

1. Create and activate a virtual environment
   macOS/Linux:
   python3 -m venv .venv
   source .venv/bin/activate
   Windows PowerShell:
   py -m venv .venv
   .venv\Scripts\Activate.ps1
2. Install the dependency
   pip install -r requirements.txt
3. Configure MySQL
   Configure the database host, username, password, and database name using environment variables or your own local configuration. The supplied source currently contains hard-coded connection details, so update the connection function before running or publishing it.
   Example environment variables:
   macOS/Linux:
   export DB_HOST=localhost
   export DB_USER=your_mysql_username
   export DB_PASSWORD=your_mysql_password
   export DB_NAME=complaint_system_db
   Windows PowerShell:
   $env:DB_HOST="localhost"
   $env:DB_USER="your_mysql_username"
   $env:DB_PASSWORD="your_mysql_password"
   $env:DB_NAME="complaint_system_db"
   Setting these variables alone will not change the current source code until its connection function is updated to read them.
4. Run the application
   After the source code and database configuration are corrected:
   python main.py
The supplied code is intended to create the database and tables when the application starts. Verify the schema and initialization logic before first use.

How to Use
1. Start the application.
2. Choose Register Member to create a member account, or select the appropriate login option.
3. Members can submit complaints, check complaint status, view complaint details, and manage their profiles.
4. Administrators can review all complaints, change statuses, add categories, and view member profiles.
5. Select the logout option to return to the main menu, or exit the application.
Complaint Statuses
Status	Meaning
Pending	The complaint is awaiting action.
In Progress	The complaint is being handled.
Resolved	The complaint has been resolved.
Rejected	The complaint has been rejected.


Security and Known Issues
This project is suitable as a learning project, but the supplied source should be reviewed and fixed before it is run or published for real use.
- Credentials: The pasted code contains a hard-coded MySQL password. Remove it from source code, use environment-based configuration, and never commit real credentials.
- Password storage: User and default administrator passwords are stored as plain text in the supplied implementation. Use a suitable password-hashing method before using real accounts.
- Default administrator: The source attempts to create a default admin account with a predictable password. Replace this behavior with secure setup and change any demo credentials.
- Database initialization: The pasted database-creation statement appears to have a Python string-syntax issue.
- Category schema: The categories table declares user_id as required, but the supplied category insertion statements do not provide it. Decide whether categories are global or user-specific, then make the schema and insert statements consistent.
- Configuration: The connection helper accepts a database argument, but the supplied code appears to use a hard-coded database name in the connection call.
- Testing: Test database creation, registration, login, complaint submission, and admin status updates against a fresh local database.

These items are listed as review notes, not as fixes that have already been completed.
Screenshots
![Main menu]![alt text](image.png)
Future Improvements
- Secure password hashing and safer administrator account setup.
- Environment-based database configuration.
- Input validation and more consistent error handling.
- Automated tests.
- Complaint filtering and search.
- A graphical or web interface.
