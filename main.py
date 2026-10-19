import mysql.connector
from datetime import datetime


def connect_db(database=None):
    try:
        if database:
            return mysql.connector.connect(host="localhost",user="root",password="24766",database="complaint_system_db")

        return mysql.connector.connect(host="localhost",user="root",password="24766")
    except mysql.connector.Error as error:
        print("\nDatabase connection failed!")
        print(error)
        return None

#CREATE DATABASE AND TABLES

def create_database():
    con = connect_db()
    if con is None:
        return False
    cursor = con.cursor()

    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {"complaint_system_db"}")
    con.close()
    con = connect_db("complaint_system_db")

    if con is None:
        return False
    cursor = con.cursor()

#USERS TABLE
    cursor.execute("""CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        password VARCHAR(100) NOT NULL,
        role VARCHAR(20) NOT NULL)""")

#MEMBER PROFILES TABLE
    cursor.execute("""CREATE TABLE IF NOT EXISTS profiles (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT UNIQUE NOT NULL,
                    full_name VARCHAR(100),
                    email VARCHAR(100),
                    phone VARCHAR(20),
                    address VARCHAR(200),
                    FOREIGN KEY (user_id)
                    REFERENCES users(id)
                    ON DELETE CASCADE)""")

#CATEGORIES TABLE

    cursor.execute("""CREATE TABLE IF NOT EXISTS categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    category_name VARCHAR(100) UNIQUE NOT NULL)""")

#COMPLAINTS TABLE


    cursor.execute("""CREATE TABLE IF NOT EXISTS complaints (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                category_id INT NOT NULL,
                subject VARCHAR(150) NOT NULL,
                description TEXT NOT NULL,
                complaint_date VARCHAR(10) NOT NULL,
                status VARCHAR(30) DEFAULT 'Pending',
                admin_remarks VARCHAR(500),
                FOREIGN KEY (user_id)
                REFERENCES users(id)
                ON DELETE CASCADE,
                FOREIGN KEY (category_id)
                REFERENCES categories(id)
                ON DELETE CASCADE)""")

#DEFAULT ADMIN
    cursor.execute("""SELECT id FROM users WHERE username = 'admin'""")
    admin = cursor.fetchone()
    if admin is None:
        cursor.execute("""INSERT INTO users (username, password, role) VALUES ('admin', 'admin123', 'admin')""")

#DEFAULT CATEGORIES

    default_categories = ["Academic","Infrastructure","Technical","Transport","Hostel","Library","Fees","Other"]
    for category in default_categories:
        cursor.execute("""INSERT IGNORE INTO categories(category_name) VALUES (%s)""", (category,))
    con.commit()
    con.close()
    return True

#INPUT FUNCTIONS

def get_non_empty(message):
    while True:
        value = input(message).strip()
        if value:
            return value
        print("Input cannot be empty.")


def get_number(message):
    while True:
        try:
            value = int(input(message))
            if value >= 0:
                return value
            print("Enter a positive number.")
        except ValueError:
            print("Please enter a valid number.")

#DATE


def get_date():
    while True:
        date_text = input("Complaint date (DD/MM/YYYY): ").strip()
        try:
            date_object = datetime.strptime(date_text,"%d/%m/%Y")
            return date_object.strftime("%d/%m/%Y")
        except ValueError:
            print("Invalid date. ""Please use DD/MM/YYYY.")


#MEMBER REGISTRATION

def register_member():
    print("\n" + "=" * 60)
    print("                 REGISTER MEMBER")
    print("=" * 60)
    username = get_non_empty("Create username: ")
    password = get_non_empty("Create password: ")
    con = connect_db("complaint_system_db")

    if con is None:
        return
    cursor = con.cursor()
    try:
        cursor.execute("""INSERT INTO users (username, password, role) VALUES (%s, %s, 'member')""", (username,password))
        user_id = cursor.lastrowid
        cursor.execute("""INSERT INTO profiles (user_id) VALUES (%s)""", (user_id,))
        con.commit()
        print("\nRegistration successful!")
        print("You can now login as a member.")
    except mysql.connector.Error as error:
        con.rollback()
        if error.errno == 1062:
            print("\nUsername already exists.")
        else:
            print("\nRegistration failed.")
            print(error)
    finally:
        con.close()

#LOGIN

def login(expected_role):
    print("\n" + "=" * 60)
    print("                       LOGIN")
    print("=" * 60)
    username = get_non_empty("Username: ")
    password = get_non_empty("Password: ")
    con = connect_db("complaint_system_db")

    if con is None:
        return None
    cursor = con.cursor()
    cursor.execute("""SELECT id, username, role FROM users WHERE username = %s AND password = %s""", (username,password))
    user = cursor.fetchone()
    con.close()

    if user is None:
        print("\nInvalid username or password.")
        return None
    if user[2] != expected_role:
        print( "\nThis account is not a " f"{expected_role} account.")
        return None
    print("\nLogin successful!")
    return user

#MEMBER PROFILE

def edit_profile(user_id):
    con = connect_db("complaint_system_db")
    if con is None:
        return
    cursor = con.cursor()
    cursor.execute("""SELECT full_name,email,phone,address FROM profiles WHERE user_id = %s""", (user_id,))
    profile = cursor.fetchone()

    if profile is None:
        cursor.execute("""INSERT INTO profiles(user_id) VALUES (%s)""", (user_id,))
        con.commit()
        profile = ("", "", "", "")

    print("\n" + "=" * 60)
    print("                   EDIT PROFILE")
    print("=" * 60)
    print("\nPress ENTER to keep the old value.\n")

    full_name = input(f"Full Name [{profile[0] or 'Not set'}]: ").strip()

    email = input(f"Email [{profile[1] or 'Not set'}]: ").strip()

    phone = input(f"Phone [{profile[2] or 'Not set'}]: ").strip()

    address = input(f"Address [{profile[3] or 'Not set'}]: ").strip()

    if not full_name:
        full_name = profile[0]
    if not email:
        email = profile[1]
    if not phone:
        phone = profile[2]
    if not address:
        address = profile[3]

    cursor.execute("""UPDATE profiles SET full_name = %s,email = %s,phone = %s,address = %s WHERE user_id = %s""", (full_name,email,phone,
                   address,user_id))
    con.commit()
    con.close()
    print("\nProfile updated successfully!")

#VIEW PROFILE

def view_profile(user_id):
    con = connect_db("complaint_system_db")
    if con is None:
        return
    cursor = con.cursor()
    cursor.execute("""SELECT full_name,email,phone,address FROM profiles WHERE user_id = %s""", (user_id,))
    profile = cursor.fetchone()
    con.close()

    print("\n" + "=" * 60)
    print("                    MY PROFILE")
    print("=" * 60)

    if profile is None:
        print("Profile not created.")
        return
    
    print("Full Name :",profile[0] or "Not set")
    print("Email     :",profile[1] or "Not set")
    print("Phone     :",profile[2] or "Not set")
    print("Address   :",profile[3] or "Not set")

#VIEW CATEGORIES

def view_categories():
    con = connect_db("complaint_system_db")
    if con is None:
        return []
    cursor = con.cursor()
    cursor.execute("""SELECT id, category_name FROM categories ORDER BY category_name """)
    records = cursor.fetchall()
    con.close()

    print("\n" + "=" * 50)
    print("                 CATEGORIES")
    print("=" * 50)

    for row in records:
        print(f"{row[0]}. {row[1]}")
    return records

# ADMIN - ADD CATEGORY


def add_category():
    print("\n" + "=" * 60)
    print("                  ADD CATEGORY")
    print("=" * 60)

    category = get_non_empty("Category name: ")
    con = connect_db("complaint_system_db")

    if con is None:
        return
    cursor = con.cursor()
    try:
        cursor.execute("""INSERT INTO categories(category_name) VALUES (%s) """, (category,))
        con.commit()

        print("\nCategory added successfully!")
    except mysql.connector.Error as error:
        con.rollback()

        if error.errno == 1062:
            print("\nCategory already exists.")
        else:
            print("\nError:")
            print(error)
    finally:
        con.close()

#MEMBER - SUBMIT COMPLAINT

def submit_complaint(user_id):
    print("\n" + "=" * 60)
    print("                 SUBMIT COMPLAINT")
    print("=" * 60)
    categories = view_categories()

    if not categories:
        print("\nNo categories available.")
        return

    category_id = get_number("\nEnter category ID: ")

    valid_ids = [row[0] for row in categories]

    if category_id not in valid_ids:
        print("\nInvalid category.")
        return

    subject = get_non_empty("\nComplaint subject: ")
    description = get_non_empty("Complaint description: ")

    complaint_date = get_date()
    con = connect_db("complaint_system_db")

    if con is None:
        return
    cursor = con.cursor()
    try:
        cursor.execute("""INSERT INTO complaints(user_id,category_id,subject,description,complaint_date,status,admin_remarks)
                       VALUES(%s,%s,%s,%s,%s,'Pending','')""", (user_id,category_id,subject,description,complaint_date))
        con.commit()
        complaint_id = cursor.lastrowid

        print("\nComplaint submitted successfully!")
        print("Complaint ID:",complaint_id)

    except mysql.connector.Error as error:
        con.rollback()
        print("\nComplaint submission failed.")
        print(error)
    finally:
        con.close()

# MEMBER - VIEW COMPLAINTS

def my_complaints(user_id):
    con = connect_db("complaint_system_db")

    if con is None:
        return

    cursor = con.cursor()
    cursor.execute("""SELECT complaints.id,categories.category_name,complaints.subject,complaints.complaint_date,complaints.status
                     FROM complaints JOIN categories ON complaints.category_id = categories.id WHERE complaints.user_id = %s
                     ORDER BY complaints.id DESC""", (user_id,))
    records = cursor.fetchall()
    con.close()

    print("\n" + "=" * 75)
    print("                    MY COMPLAINTS")
    print("=" * 75)

    if not records:
        print("You have not submitted any complaints.")
        return

    for row in records:
        print("\nComplaint ID :", row[0])
        print("Category     :", row[1])
        print("Subject      :", row[2])
        print("Date         :", row[3])
        print("Status       :", row[4])

        print("-" * 75)


#MEMBER - COMPLAINT DETAILS


def complaint_details(user_id):

    complaint_id = get_number("Enter complaint ID: ")
    con = connect_db("complaint_system_db")

    if con is None:
        return
    cursor = con.cursor()
    cursor.execute("""SELECT complaints.id,categories.category_name,complaints.subject,complaints.description,complaints.complaint_date,
                     complaints.status,complaints.admin_remarks FROM complaints JOIN categories ON complaints.category_id = categories.id
                     WHERE complaints.id = %s AND complaints.user_id = %s""", (complaint_id,user_id))

    complaint = cursor.fetchone()
    con.close()

    if complaint is None:
        print("\nComplaint not found.")
        return
    print("\n" + "=" * 65)
    print("                 COMPLAINT DETAILS")
    print("=" * 65)

    print("Complaint ID :", complaint[0])
    print("Category     :", complaint[1])
    print("Subject      :", complaint[2])
    print("Description  :", complaint[3])
    print("Date         :", complaint[4])
    print("Status       :", complaint[5])
    print("Admin Remarks:",complaint[6] or "No remarks")

# ADMIN - VIEW ALL COMPLAINTS

def admin_view_complaints():
    con = connect_db("complaint_system_db")
    if con is None:
        return
    cursor = con.cursor()
    cursor.execute("""SELECT complaints.id,users.username,categories.category_name,complaints.subject,complaints.complaint_date,complaints.status 
                     FROM complaints JOIN users ON complaints.user_id = users.id JOIN categories ON complaints.category_id = categories.id
                     ORDER BY complaints.id DESC""")

    records = cursor.fetchall()
    con.close()

    print("\n" + "=" * 85)
    print("                    ALL COMPLAINTS")
    print("=" * 85)

    if not records:
        print("No complaints found.")
        return

    for row in records:
        print("\nComplaint ID :", row[0])
        print("Member       :", row[1])
        print("Category     :", row[2])
        print("Subject      :", row[3])
        print("Date         :", row[4])
        print("Status       :", row[5])
        print("-" * 85)

#ADMIN - UPDATE COMPLAINT

def update_complaint():
    print("\n" + "=" * 60)
    print("              UPDATE COMPLAINT")
    print("=" * 60)

    complaint_id = get_number("Enter complaint ID: ")
    con = connect_db("complaint_system_db")

    if con is None:
        return
    cursor = con.cursor()
    cursor.execute("""SELECT complaints.id,users.username,complaints.subject,complaints.status FROM complaints JOIN users
                    ON complaints.user_id = users.id WHERE complaints.id = %s""", (complaint_id,))
    complaint = cursor.fetchone()

    if complaint is None:
        print("\nComplaint not found.")
        con.close()
        return

    print("\nComplaint ID :", complaint[0])
    print("Member       :", complaint[1])
    print("Subject      :", complaint[2])
    print("Current      :", complaint[3])
    print("\nChoose status:")
    print("1. Pending")
    print("2. In Progress")
    print("3. Resolved")
    print("4. Rejected")

    choice = input("\nEnter choice: ").strip()

    statuses = { "1": "Pending","2": "In Progress","3": "Resolved","4": "Rejected"}

    if choice not in statuses:
        print("\nInvalid choice.")
        con.close()
        return

    status = statuses[choice]
    remarks = input("Admin remarks: ").strip()
    cursor.execute("""UPDATE complaints SET status = %s,admin_remarks = %s WHERE id = %s""", (status,remarks,complaint_id))
    con.commit()
    con.close()

    print("\nComplaint updated successfully!")

# ADMIN - VIEW MEMBER PROFILES

def admin_view_profiles():
    con = connect_db("complaint_system_db")
    if con is None:
        return
    cursor = con.cursor()
    cursor.execute("""SELECT users.username,profiles.full_name,profiles.email,profiles.phone,profiles.address FROM users LEFT JOIN profiles
                    ON users.id = profiles.user_id WHERE users.role = 'member'""")
    records = cursor.fetchall()
    con.close()

    print("\n" + "=" * 80)
    print("                    MEMBER PROFILES")
    print("=" * 80)

    if not records:
        print("No members found.")
        return
    for row in records:
        print("\nUsername  :", row[0])
        print("Full Name :",row[1] or "Not set")
        print("Email     :",row[2] or "Not set")
        print("Phone     :",row[3] or "Not set")
        print("Address   :",row[4] or "Not set")
        print("-" * 80)

#ADMIN MENU

def admin_menu():
    while True:
        print("\n")
        print("*" * 65)
        print("                     ADMIN PANEL")
        print("*" * 65)

        print("\n1. View All Complaints")
        print("2. Update Complaint Status")
        print("3. View Member Profiles")
        print("4. Add Complaint Category")
        print("5. View Categories")
        print("6. Logout")

        choice = input("\nEnter choice: ").strip()
        if choice == "1":
            admin_view_complaints()
        elif choice == "2":
            update_complaint()
        elif choice == "3":
            admin_view_profiles()
        elif choice == "4":
            add_category()
        elif choice == "5":
            view_categories()
        elif choice == "6":
            print("\nLogged out.")
            break
        else:
            print("\nInvalid choice.")
            
# MEMBER MENU

def member_menu(user_id):
    while True:
        print("\n")
        print("*" * 65)
        print("                    MEMBER PANEL")
        print("*" * 65)

        print("\n1. Submit Complaint")
        print("2. My Complaints")
        print("3. Complaint Details")
        print("4. My Profile")
        print("5. Edit Profile")
        print("6. View Categories")
        print("7. Logout")

        choice = input("\nEnter choice: ").strip()

        if choice == "1":
            submit_complaint(user_id)
        elif choice == "2":
            my_complaints(user_id)
        elif choice == "3":
            complaint_details(user_id)
        elif choice == "4":
            view_profile(user_id)
        elif choice == "5":
            edit_profile(user_id)
        elif choice == "6":
            view_categories()
        elif choice == "7":
            print("\nLogged out.")
            break
        else:
            print("\nInvalid choice.")

# MAIN

def main():

    if not create_database():
        print("\nUnable to create/connect "
            "to the database.")
        return
    while True:
        print("\n")
        print("=" * 65)
        print("              COMPLAINT MANAGEMENT SYSTEM")
        print("=" * 65)
        print("\n1. Admin Login")
        print("2. Member Login")
        print("3. Register Member")
        print("4. Exit")
        choice = input("\nEnter choice: ").strip()
#ADMIN LOGIN

        if choice == "1":
            user = login("admin")
            if user:
                admin_menu()

# MEMBER LOGIN
        elif choice == "2":
            user = login("member")
            if user:
                member_menu(user[0])

#REGISTER

        elif choice == "3":
            register_member()


#EXIT


        elif choice == "4":
            print("\nThank you for using "
                  "Complaint Management System!")
            break
        else:
            print("\nInvalid choice.")


# START PROGRAM

if __name__ == "__main__":
    main()