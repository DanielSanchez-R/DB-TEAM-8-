""".

Gym Management System (CRUD)
Author: Daniel Sanchez, Adan Delgado
Date:4/27/2025
Description: manages members, classes, and equipment for a gym
It connects to a SQLite database and allows CRUD operations through
a menu-driven interface using an object-oriented design.
"""
import datetime
from datetime import datetime
import sqlite3
from datetime import date


class DatabaseConnection:
    """
    Manages the connection to the SQLite database.
    """
    def __init__(self):
        """
        Initializes a DatabaseConnection instance with no active connection.
        """
        self.conn = None

    def connect(self, db_name):
        """
        Connects to the specified SQLite database and enables foreign key constraints.

        Args:
            db_name (str): The name of the database file.
        """
        try:
            self.conn = sqlite3.connect(db_name)
            self.conn.execute("PRAGMA foreign_keys = ON;")
            print(f"[INFO] Successfully connected to {db_name}")
        except sqlite3.Error as e:
            print(f"[ERROR] Connection failed: {e}")
            self.conn = None

    def close(self):
        """
        Closes the current database connection.
        """
        if self.conn:
            self.conn.close()
            print("[INFO] Database connection closed.")

class MemberManager:
    """
    Handles operations related to gym members such as add, update, delete, and search.
    """
    def __init__(self, conn):
        """
        Initializes MemberManager with an active database connection.

        Args:
            conn: An active SQLite database connection.
        """
        self.conn = conn

    def display_all_members(self):
        """
        Displays all members and their membership plans.
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT m.memberId, m.name, m.email, m.age, IFNULL(mp.planType, 'No Plan')
                FROM Member m
                LEFT JOIN Payment p ON m.memberId = p.memberId
                LEFT JOIN MembershipPlan mp ON p.planId = mp.planId;
            """)
            rows = cursor.fetchall()
            print("Member ID | Member Name | Email | Age | Membership Plan")
            print("----------------------------------------------------------")
            for row in rows:
                print(" | ".join(str(col) for col in row))
        except sqlite3.Error as e:
            print(f"[ERROR] Unable to fetch members: {e}")

    def add_member(self):
        """
       Adds a new member to the database along with their payment information.
       """
        try:
            name = input("Enter member name: ")
            email = input("Enter email: ")
            age = int(input("Enter age: "))
            
            # Validate age
            if age < 15:
                print("[ERROR] Age must be at least 15.")
                return
            
            membership_start_date = input("Enter membership start date (YYYY-MM-DD): ")
            membership_end_date = input("Enter membership end date (YYYY-MM-DD): ")
            
            # Validate dates
            try:
                start = datetime.strptime(membership_start_date, "%Y-%m-%d")
                end = datetime.strptime(membership_end_date, "%Y-%m-%d")
                if end < start:
                    print("[ERROR] Membership end date cannot be before start date.")
                    return
            except ValueError:
                print("[ERROR] Dates must be in YYYY-MM-DD format.")
                return
            
            # Choose plan type
            print("Choose a Membership Plan:")
            print("1. Monthly")
            print("2. Annual")
            plan_choice = input("Enter 1 or 2: ")
            
            if plan_choice == "1":
                plan_id = 1  # Assuming planId=1 is Monthly
                amount_paid = 50.0  # Example: $50 for monthly
            elif plan_choice == "2":
                plan_id = 2  # Assuming planId=2 is Annual
                amount_paid = 500.0  # Example: $500 for annual
            else:
                print("[ERROR] Invalid plan choice. Member not added.")
                return
            
            payment_date = date.today().isoformat()  # Today's date in YYYY-MM-DD
            
            cursor = self.conn.cursor()
    
            # Insert into Member
            cursor.execute("""
                INSERT INTO Member (name, email, age, membershipStartDate, membershipEndDate)
                VALUES (?, ?, ?, ?, ?)
            """, (name, email, age, membership_start_date, membership_end_date))
            self.conn.commit()  # Commit after adding Member
    
            member_id = cursor.lastrowid  # Get the ID of the newly inserted member
    
            # Insert into Payment
            cursor.execute("""
                INSERT INTO Payment (memberId, planId, amountPaid, paymentDate)
                VALUES (?, ?, ?, ?)
            """, (member_id, plan_id, amount_paid, payment_date))
            self.conn.commit()  # Commit after adding Payment
            
            cursor.close()
    
            print("[INFO] Member and Payment added successfully.")
    
        except sqlite3.OperationalError as oe:
            print(f"[ERROR] OperationalError: {oe}")
        except sqlite3.Error as e:
            print(f"[ERROR] Failed to add member: {e}")

    def update_member(self):
        """
       Updates an existing member's email and age information.
       """
        cursor = self.conn.cursor()
    
        # FIRST: Show list of members
        cursor.execute("""
            SELECT m.memberId, m.name, m.email, m.age, IFNULL(mp.planType, 'No Plan')
            FROM Member m
            LEFT JOIN Payment p ON m.memberId = p.memberId
            LEFT JOIN MembershipPlan mp ON p.planId = mp.planId;
        """)
        members = cursor.fetchall()
    
        if not members:
            print("No members found to update.")
            return
    
        print("\nAvailable Members:")
        print("Member ID | Member Name | Email | Age | Membership Plan")
        print("----------------------------------------------------------")
        for member in members:
            print(f"{member[0]} | {member[1]} | {member[2]} | {member[3]} | {member[4]}")
    
        # THEN: Ask for Member ID
        member_id = int(input("\nEnter the ID of the member to update: "))
        new_email = input("Enter new email: ")
        new_age = int(input("Enter new age: "))
    
        # Validate age
        if new_age < 15:
            print("[ERROR] Age must be at least 15.")
            return
    
        # --- NEW: prompt for additional member fields ---
        new_phone = input("Enter new phone number: ")  # <--- Added
        new_address = input("Enter new address: ")     # <--- Added
        # Prompt for membership dates
        new_start = input("Enter new membership start date (YYYY-MM-DD): ")  # <--- Added
        new_end   = input("Enter new membership end date (YYYY-MM-DD): ")    # <--- Added

        # --- NEW: date validation ---
        try:
            fmt = "%Y-%m-%d"
            from datetime import datetime
            start_dt = datetime.strptime(new_start, fmt)
            end_dt = datetime.strptime(new_end, fmt)
            if end_dt < start_dt:
                print("[ERROR] End date cannot be before start date.")
                return
        except ValueError:
            print("[ERROR] Dates must be in YYYY-MM-DD format.")
            return

        # --- UPDATED SQL: include all fields ---
        cursor.execute(
            """
            UPDATE Member
            SET email = ?, age = ?, phone = ?, address = ?, membershipStartDate = ?, membershipEndDate = ?
            WHERE memberId = ?
            """,
            (new_email, new_age, new_phone, new_address, new_start, new_end, member_id)
        )
        self.conn.commit()
        print(f"[INFO] Member {member_id} updated successfully.")

    def delete_member(self):
        """
       Deletes a member from the database.
       """
        try:
            cursor = self.conn.cursor()
    
            # FIRST: Show list of members
            cursor.execute("""
                SELECT m.memberId, m.name, m.email, m.age, IFNULL(mp.planType, 'No Plan')
                FROM Member m
                LEFT JOIN Payment p ON m.memberId = p.memberId
                LEFT JOIN MembershipPlan mp ON p.planId = mp.planId;
            """)
            members = cursor.fetchall()
    
            if not members:
                print("No members found to delete.")
                return
    
            print("\nAvailable Members:")
            print("Member ID | Member Name | Email | Age | Membership Plan")
            print("----------------------------------------------------------")
            for member in members:
                print(f"{member[0]} | {member[1]} | {member[2]} | {member[3]} | {member[4]}")
    
            # THEN: Ask for Member ID
            member_id = int(input("\nEnter the ID of the member to delete: "))
    
            # Validate ID exists
            cursor.execute("SELECT name FROM Member WHERE memberId = ?", (member_id,))
            result = cursor.fetchone()
            if not result:
                print("[ERROR] Member ID not found.")
                return
    
            confirm = input(f"Are you sure you want to delete member '{result[0]}'? (Y/N): ").strip().lower()
            if confirm != 'y':
                print("Deletion cancelled.")
                return
    
            # Delete from Member (foreign key constraints should handle related records)
            cursor.execute("DELETE FROM Member WHERE memberId = ?", (member_id,))
            self.conn.commit()
            print("[INFO] Member deleted successfully.")
    
        except sqlite3.Error as e:
            print(f"[ERROR] Failed to delete member: {e}")


    def find_members_by_class(self):
        """
        Finds and displays members enrolled in a specific class.
        """
        try:
            cursor = self.conn.cursor()
    
            # First, show available classes
            cursor.execute("SELECT classId, className FROM Class;")
            classes = cursor.fetchall()
    
            if not classes:
                print("No classes found.")
                return
    
            print("\nAvailable Classes:")
            print("Class ID | Class Name")
            print("----------------------")
            for cl in classes:
                print(f"{cl[0]} | {cl[1]}")
    
            class_id = int(input("\nEnter Class ID to find members: "))
    
            # Now, find members for that class
            cursor.execute("""
                SELECT DISTINCT m.name
                FROM Member m
                JOIN Attends a ON m.memberId = a.memberId
                WHERE a.classId = ?
            """, (class_id,))
            rows = cursor.fetchall()
    
            if rows:
                print("\nMembers attending class:")
                for row in rows:
                    print(row[0])
            else:
                print("\nNo members found for this class.")
    
        except sqlite3.Error as e:
            print(f"[ERROR] Failed to find members: {e}")

class ClassManager:
    """
    Manages CRUD operations and reporting related to gym classes.
    """
    def __init__(self, conn):
        """
       Initializes ClassManager with a database connection.

       Args:
           conn: The active database connection.
       """
        self.conn = conn

    def list_classes_and_attendance(self):
        """
        Lists all classes along with their attendance counts.
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT c.classId, c.className, COUNT(a.memberId) AS attendance
                FROM Class c
                LEFT JOIN Attends a ON c.classId = a.classId
                GROUP BY c.classId;
            """)
            rows = cursor.fetchall()
    
            print("Class ID | Class Name | Attendance")
            print("-----------------------------------")
            for row in rows:
                print(f"{row[0]} | {row[1]} | {row[2]}")
    
        except sqlite3.Error as e:
            print(f"[ERROR] Unable to list classes: {e}")

    def add_class(self):
        """
        Adds a new class to the gym.
        """
        try:
            class_name = input("Enter class name: ")
            
            print("\nAvailable Class Types: Yoga, Zumba, HIIT, Weights")
            class_type = input("Enter class type (exactly as shown): ")
            
            duration = int(input("Enter class duration (minutes): "))
            capacity = int(input("Enter class capacity: "))
            
            instructor_id = 1  # Hardcoded for now
            gym_id = 1  # Hardcoded because there's only one gym
            
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO Class (className, classType, duration, classCapacity, instructorId, gymID)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (class_name, class_type, duration, capacity, instructor_id, gym_id))
            self.conn.commit()
            print("[INFO] Class added successfully.")
    
        except sqlite3.Error as e:
            print(f"[ERROR] Failed to add class: {e}")

    def update_class(self):
        """
        Updates the name and type of an existing class.
        """
        cursor = self.conn.cursor()
    
        # FIRST: Show list of classes
        cursor.execute("""
            SELECT classId, className, classType
            FROM Class;
        """)
        classes = cursor.fetchall()

        if not classes:
            print("No classes found to update.")
            return

        print("\nAvailable Classes:")
        print("Class ID | Class Name | Class Type")
        print("-----------------------------------")
        for cl in classes:
            print(f"{cl[0]} | {cl[1]} | {cl[2]}")

        # Ask for Class ID
        class_id = int(input("\nEnter class ID to update: "))

        # --- existing prompts ---
        new_name = input("Enter new class name: ")           # <--- Added
        new_type = input("Enter new class type: ")           # <--- Added
        new_duration = input("Enter new duration (minutes): ")# <--- Added
        new_capacity = input("Enter new capacity: ")          # <--- Added
        new_instructor = int(input("Enter new instructor ID: "))  # <--- Added

        # --- UPDATED SQL: include all fields ---
        cursor.execute(
            """
            UPDATE Class
            SET className = ?, classType = ?, duration = ?, classCapacity = ?, instructorId = ?
            WHERE classId = ?
            """,
            (new_name, new_type, new_duration, new_capacity, new_instructor, class_id)
        )
        self.conn.commit()
        print(f"[INFO] Class {class_id} updated successfully.")
        
    def delete_class(self):
        """
        Deletes a class if there are no attendees registered.
        """
        try:
            cursor = self.conn.cursor()
    
            # FIRST: Show list of classes
            cursor.execute("""
                SELECT classId, className, classType
                FROM Class;
            """)
            classes = cursor.fetchall()
    
            if not classes:
                print("No classes found to delete.")
                return
    
            print("\nAvailable Classes:")
            print("Class ID | Class Name | Class Type")
            print("-----------------------------------")
            for cl in classes:
                print(f"{cl[0]} | {cl[1]} | {cl[2]}")
    
            # THEN: Ask for Class ID
            class_id = int(input("\nEnter class ID to delete: "))
    
            # Validate ID exists
            cursor.execute("SELECT className FROM Class WHERE classId = ?", (class_id,))
            result = cursor.fetchone()
            if not result:
                print("[ERROR] Class ID not found.")
                return
    
            confirm = input(f"Are you sure you want to delete class '{result[0]}'? (Y/N): ").strip().lower()
            if confirm != 'y':
                print("Deletion cancelled.")
                return
    
            # Check if class has attendees
            cursor.execute("SELECT COUNT(*) FROM Attends WHERE classId = ?", (class_id,))
            attendees = cursor.fetchone()[0]
            if attendees > 0:
                print(f"[WARNING] Class '{result[0]}' has {attendees} registered member(s).")
                move_choice = input("Would you like to reassign them to another class? (Y/N): ").strip().lower()
                if move_choice != 'y':
                    print("Deletion cancelled.")
                    return

                # Show other classes for reassignment
                cursor.execute("""
                    SELECT classId, className
                    FROM Class
                    WHERE classId != ?;
                """, (class_id,))
                other_classes = cursor.fetchall()
                print("\nAvailable Classes to Move To:")
                print("Class ID | Class Name")
                print("---------------------")
                for oc in other_classes:
                    print(f"{oc[0]} | {oc[1]}")

                new_class_id = int(input("Enter new class ID to reassign members to: "))
                valid_ids = [c[0] for c in other_classes]
                if new_class_id not in valid_ids:
                    print("[ERROR] Invalid class ID chosen. Deletion cancelled.")
                    return

                # Reassign members
                cursor.execute(
                    "UPDATE Attends SET classId = ? WHERE classId = ?",
                    (new_class_id, class_id)
                )
                self.conn.commit()
                print(f"[INFO] Moved {attendees} member(s) to class ID {new_class_id}.")

            # Confirm deletion
            confirm = input(f"Are you sure you want to delete class '{result[0]}'? (Y/N): ").strip().lower()
            if confirm != 'y':
                print("Deletion cancelled.")
                return

            # Delete Class
            cursor.execute("DELETE FROM Class WHERE classId = ?", (class_id,))
            self.conn.commit()
            print("[INFO] Class deleted successfully.")

        except sqlite3.Error as e:
            print(f"[ERROR] Failed to delete class: {e}")


class EquipmentManager:
    """
    Manages CRUD operations related to gym equipment.
    """
    def __init__(self, conn):
        """
        Initializes EquipmentManager with a database connection.

        Args:
            conn: The active database connection.
        """
        self.conn = conn

    def show_all_equipment(self):
        """
        Displays a list of all equipment in the gym.
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT equipmentId, name, type, quantity FROM Equipment;")
            rows = cursor.fetchall()
    
            print("Equipment ID | Name | Type | Quantity")
            print("---------------------------------------")
            for row in rows:
                print(" | ".join(str(col) for col in row))
    
        except sqlite3.Error as e:
            print(f"[ERROR] Unable to fetch equipment: {e}")

    def insert_equipment(self):
        """
        Inserts a new equipment record into the database.
        """
        try:
            name = input("Enter equipment name: ")
    
            print("\nAvailable Equipment Types: Cardio, Strength, Flexibility, Recovery")
            equipment_type = input("Enter equipment type (exactly as shown): ")
    
            quantity = int(input("Enter quantity: "))
            gym_id = 1  # Hardcoded because there is only one gym
            
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO Equipment (name, type, quantity, gymId)
                VALUES (?, ?, ?, ?)
            """, (name, equipment_type, quantity, gym_id))
            self.conn.commit()
            print("[INFO] Equipment inserted successfully.")
    
        except sqlite3.Error as e:
            print(f"[ERROR] Failed to insert equipment: {e}")

    def update_equipment(self):
        """
        Updates the quantity of an existing equipment item.
        """
        cursor = self.conn.cursor()
    
        # FIRST: Show list of equipment
        cursor.execute("""
            SELECT equipmentId, name, type
            FROM Equipment;
        """)
        equipment = cursor.fetchall()

        if not equipment:
            print("No equipment found to update.")
            return

        print("\nAvailable Equipment:")
        print("Equip ID | Name | Type")
        print("----------------------")
        for eq in equipment:
            print(f"{eq[0]} | {eq[1]} | {eq[2]}")

        equip_id = int(input("Enter equipment ID to update: "))

        # --- NEW: prompt for fields except gymId ---
        new_name = input("Enter new equipment name: ")        # <--- Added
        new_type = input("Enter new equipment type: ")        # <--- Added
        new_quantity = int(input("Enter new quantity: "))    # <--- Added

        # --- UPDATED SQL: include only name, type, quantity ---
        cursor.execute(
            """
            UPDATE Equipment
            SET name = ?, type = ?, quantity = ?
            WHERE equipmentId = ?
            """,
            (new_name, new_type, new_quantity, equip_id)
        )
        self.conn.commit()
        print(f"[INFO] Equipment {equip_id} updated successfully.")


    def delete_equipment(self):
        """
        Deletes an equipment item from the database.
        """
        try:
            cursor = self.conn.cursor()
    
            # FIRST: Show list of equipment
            cursor.execute("""
                SELECT equipmentId, name, type, quantity
                FROM Equipment;
            """)
            equipment_list = cursor.fetchall()
    
            if not equipment_list:
                print("No equipment found to delete.")
                return
    
            print("\nAvailable Equipment:")
            print("Equipment ID | Name | Type | Quantity")
            print("---------------------------------------")
            for eq in equipment_list:
                print(f"{eq[0]} | {eq[1]} | {eq[2]} | {eq[3]}")
    
            # THEN: Ask for Equipment ID
            equipment_id = int(input("\nEnter equipment ID to delete: "))
    
            # Validate ID exists
            cursor.execute("SELECT name FROM Equipment WHERE equipmentId = ?", (equipment_id,))
            result = cursor.fetchone()
            if not result:
                print("[ERROR] Equipment ID not found.")
                return
    
            confirm = input(f"Are you sure you want to delete equipment '{result[0]}'? (Y/N): ").strip().lower()
            if confirm != 'y':
                print("Deletion cancelled.")
                return
    
            # Delete Equipment
            cursor.execute("DELETE FROM Equipment WHERE equipmentId = ?", (equipment_id,))
            self.conn.commit()
            print("[INFO] Equipment deleted successfully.")
    
        except sqlite3.Error as e:
            print(f"[ERROR] Failed to delete equipment: {e}")

class GymManagementApp:
    """
    Main application class for managing the gym database.
    Provides menus to manage members, classes, and equipment.
    """
    def __init__(self):
        """
        Initializes GymManagementApp with no active database connection.
        """
        self.db = DatabaseConnection()
        self.member_manager = None
        self.class_manager = None
        self.equipment_manager = None

    def run(self):
        """
        Starts the application: connects to the database and launches the main menu.
        """
        db_name = input("Enter database name (e.g., XYZGym.sqlite): ")
        self.db.connect(db_name)
        if self.db.conn is None:
            print("Exiting program.")
            return
        self.member_manager = MemberManager(self.db.conn)
        self.class_manager = ClassManager(self.db.conn)
        self.equipment_manager = EquipmentManager(self.db.conn)
        self.main_menu()
        self.db.close()

    def main_menu(self):
        """
       Displays the main menu to navigate between sections.
       """
        while True:
            print("\n--- Main Menu ---")
            print("1. Members Menu")
            print("2. Classes Menu")
            print("3. Equipment Menu")
            print("4. Logout and Exit")
            choice = input("Enter your choice: ")
            if choice == "1":
                self.members_menu()
            elif choice == "2":
                self.classes_menu()
            elif choice == "3":
                self.equipment_menu()
            elif choice == "4":
                print("Logging out...")
                break
            else:
                print("Invalid choice. Please try again.")

    def members_menu(self):
        """
       Displays the members menu and handles member-related actions.
       """
        while True:
            print("\n--- Members Menu ---")
            print("1. Display all members")
            print("2. Add new member")
            print("3. Update member")
            print("4. Delete member")
            print("5. Find members by class")
            print("6. Return to Main Menu")
            choice = input("Enter your choice: ")
            if choice == "1":
                self.member_manager.display_all_members()
            elif choice == "2":
                self.member_manager.add_member()
            elif choice == "3":
                self.member_manager.update_member()
            elif choice == "4":
                self.member_manager.delete_member()
            elif choice == "5":
                self.member_manager.find_members_by_class()
            elif choice == "6":
                break
            else:
                print("Invalid choice. Please try again.")

    def classes_menu(self):
        """
        Displays the classes menu and handles class-related actions.
        """
        while True:
            print("\n--- Classes Menu ---")
            print("1. List classes and attendance")
            print("2. Add new class")
            print("3. Update class")
            print("4. Delete class")
            print("5. Return to Main Menu")
            choice = input("Enter your choice: ")
            if choice == "1":
                self.class_manager.list_classes_and_attendance()
            elif choice == "2":
                self.class_manager.add_class()
            elif choice == "3":
                self.class_manager.update_class()
            elif choice == "4":
                self.class_manager.delete_class()
            elif choice == "5":
                break
            else:
                print("Invalid choice. Please try again.")

    def equipment_menu(self):
        """
        Displays the equipment menu and handles equipment-related actions.
        """
        while True:
            print("\n--- Equipment Menu ---")
            print("1. Show all equipment")
            print("2. Insert new equipment")
            print("3. Update equipment")
            print("4. Delete equipment")
            print("5. Return to Main Menu")
            choice = input("Enter your choice: ")
            if choice == "1":
                self.equipment_manager.show_all_equipment()
            elif choice == "2":
                self.equipment_manager.insert_equipment()
            elif choice == "3":
                self.equipment_manager.update_equipment()
            elif choice == "4":
                self.equipment_manager.delete_equipment()
            elif choice == "5":
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    app = GymManagementApp()
    app.run()
