"""
file.py
-----------
This file connects our XYZGym.sqlite database and executes 10 different 
queries based onthe command-line arguments and prints the results.
"""

import sqlite3
from sqlite3 import Error
import sys

def create_connection(db_file="XYZGym.sqlite"):
    """
    Create and return a connection to the SQLite database.
    If the database file does not exist, it will be created.
    """
    conn = None
    try:
        # Connect to the database (or create it if it doesn't exist)
        conn = sqlite3.connect(db_file)
        # Enable foreign keys support - very important for our relational constraints
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        print(f"[INFO] Connection established: SQLite version {sqlite3.version}")
    except Error as e:
        # Inform us if there's any error when connecting
        print(f"[ERROR] Could not connect to database: {e}")
    return conn



def close_connection(conn):
    """Close the connection to the database."""
    if conn:
        conn.close()
        print("[INFO] Connection closed.")



def query1(conn):
    """
    Query 1:
    Retrieve a list of all gym members.
    Display member name, email, age, and membership plan.
    """
    # SQL query to join Member, Payment, and MembershipPlan tables
    sql = """
        SELECT m.name, m.email, m.age, mp.planType
        FROM Member m
        JOIN Payment p ON m.memberId = p.memberId
        JOIN MembershipPlan mp ON p.planId = mp.planId;
    """
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()  # fetch all rows returned by the query
        print("[INFO] Query 1: List of all gym members")
        print("Member Name | Email | Age | Membership Plan")
        print("------------------------------------------------")
        # Loop through each row and print the columns
        for row in rows:
            print(" | ".join(str(col) for col in row))
    except Error as e:
        print(f"[ERROR] Query 1 failed: {e}")



def query2(conn):
    """
    Query 2:
    Count the number of classes available at each gym facility.
    """
    # SQL to count classes grouped by gym location
    sql = """
        SELECT gf.location, COUNT(c.classId) AS class_count
        FROM Class c
        JOIN GymFacility gf ON c.gymID = gf.gymId
        GROUP BY gf.gymId;
    """
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        print("[INFO] Query 2: Count of classes at each gym facility")
        print("Gym Location | Number of Classes")
        print("-------------------------------------")
        for row in rows:
            print(" | ".join(str(col) for col in row))
    except Error as e:
        print(f"[ERROR] Query 2 failed: {e}")



def query3(conn, class_id):
    """
    Query 3:
    Retrieve the names of members attending a specific class.
    Parameter:
      class_id (integer) - the ID of the class.
    """
    # SQL to get member names for a given class
    sql = """
        SELECT m.name
        FROM Member m
        JOIN Attends a ON m.memberId = a.memberId
        WHERE a.classId = ?;
    """
    try:
        cursor = conn.cursor()
        # Passing class_id as a parameter to avoid SQL injection
        cursor.execute(sql, (class_id,))
        rows = cursor.fetchall()
        print(f"[INFO] Query 3: Members attending class {class_id}")
        if rows:
            for row in rows:
                print(row[0])
        else:
            print("No members found for this class.")
    except Error as e:
        print(f"[ERROR] Query 3 failed: {e}")



def query4(conn, equipment_type):
    """
    Query 4:
    List all equipment of a specific type.
    Parameter:
      equipment_type (string) - the type of equipment (e.g., Cardio, Strength).
    """
    # SQL query to select equipment by type
    sql = """
        SELECT name, type, quantity
        FROM Equipment
        WHERE type = ?;
    """
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (equipment_type,))
        rows = cursor.fetchall()
        print(f"[INFO] Query 4: Equipment of type '{equipment_type}'")
        if rows:
            for row in rows:
                print(" | ".join(str(col) for col in row))
        else:
            print(f"No equipment found of type '{equipment_type}'.")
    except Error as e:
        print(f"[ERROR] Query 4 failed: {e}")



def query5(conn):
    """
    Query 5:
    Find all members with expired memberships.
    A membership is considered expired if membershipEndDate is before the current date.
    """
    # SQL query to check membership end dates
    sql = """
        SELECT memberId, name, membershipEndDate
        FROM Member
        WHERE membershipEndDate < date('now');
    """
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        print("[INFO] Query 5: Members with expired memberships")
        print("Member ID | Name | Membership End Date")
        print("-------------------------------------------")
        if rows:
            for row in rows:
                print(" | ".join(str(col) for col in row))
        else:
            print("No expired memberships found.")
    except Error as e:
        print(f"[ERROR] Query 5 failed: {e}")



def query6(conn, instructor_id):
    """
    Query 6:
    Get the list of classes taught by a specific instructor.
    Display instructor name, phone, class name, class type, duration, and capacity.
    Parameter:
      instructor_id (integer) - the ID of the instructor.
    """
    # SQL join to retrieve classes for a given instructor
    sql = """
        SELECT i.name, i.phone, c.className, c.classType, c.duration, c.classCapacity
        FROM Class c
        JOIN Instructor i ON c.instructorId = i.instructorId
        WHERE i.instructorId = ?;
    """
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (instructor_id,))
        rows = cursor.fetchall()
        print(f"[INFO] Query 6: Classes taught by instructor {instructor_id}")
        print("Instructor Name | Phone | Class Name | Class Type | Duration | Capacity")
        print("----------------------------------------------------------------------------")
        if rows:
            for row in rows:
                print(" | ".join(str(col) for col in row))
        else:
            print("No classes found for this instructor.")
    except Error as e:
        print(f"[ERROR] Query 6 failed: {e}")



def query7(conn):
    """
    Query 7:
    Calculate the average age of members with active memberships and those with expired memberships.
    Active memberships: membershipEndDate >= date('now')
    Expired memberships: membershipEndDate < date('now')
    """
    try:
        cursor = conn.cursor()
        # Calculate average age for active memberships
        cursor.execute("SELECT AVG(age) FROM Member WHERE membershipEndDate >= date('now')")
        active_avg = cursor.fetchone()[0]
        
        # Calculate average age for expired memberships
        cursor.execute("SELECT AVG(age) FROM Member WHERE membershipEndDate < date('now')")
        expired_avg = cursor.fetchone()[0]
        
        print("[INFO] Query 7: Average age of members")
        print(f"Active Memberships: {active_avg if active_avg is not None else 'N/A'}")
        print(f"Expired Memberships: {expired_avg if expired_avg is not None else 'N/A'}")
    except Error as e:
        print(f"[ERROR] Query 7 failed: {e}")



def query8(conn):
    """
    Query 8:
    Find the top three instructors who teach the most classes along with the count of classes they teach.
    """
    # SQL to group by instructor and count classes, then limit to the top three
    sql = """
        SELECT i.name, COUNT(c.classId) AS class_count
        FROM Class c
        JOIN Instructor i ON c.instructorId = i.instructorId
        GROUP BY i.instructorId
        ORDER BY class_count DESC
        LIMIT 3;
    """
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        print("[INFO] Query 8: Top three instructors by number of classes taught")
        print("Instructor Name | Number of Classes")
        print("--------------------------------------")
        if rows:
            for row in rows:
                print(" | ".join(str(col) for col in row))
        else:
            print("No instructor data found.")
    except Error as e:
        print(f"[ERROR] Query 8 failed: {e}")



def query9(conn, class_type):
    """
    Query 9:
    Find the members who have attended all classes of a specific type.
    Parameter:
      class_type (string) - the type of the class (e.g., Yoga, HIIT).
    """
    try:
        cursor = conn.cursor()
        # First, determine the total number of classes available for the given type
        cursor.execute("SELECT COUNT(*) FROM Class WHERE classType = ?", (class_type,))
        total_classes = cursor.fetchone()[0]
        if total_classes == 0:
            print(f"[INFO] No classes found of type '{class_type}'.")
            return
        # SQL to find members who attended exactly the total count of classes of that type
        sql = """
            SELECT m.memberId, m.name
            FROM Member m
            JOIN Attends a ON m.memberId = a.memberId
            JOIN Class c ON a.classId = c.classId
            WHERE c.classType = ?
            GROUP BY m.memberId, m.name
            HAVING COUNT(DISTINCT c.classId) = ?;
        """
        cursor.execute(sql, (class_type, total_classes))
        rows = cursor.fetchall()
        print(f"[INFO] Query 9: Members who attended all classes of type '{class_type}'")
        if rows:
            for row in rows:
                print(f"Member ID: {row[0]} | Name: {row[1]}")
        else:
            print("No member has attended all classes of this type.")
    except Error as e:
        print(f"[ERROR] Query 9 failed: {e}")



def query10(conn):
    """
    Query 10:
    Get all members who attended classes in the last month along with class names and types.
    """
    # SQL to join tables and group attendance in the last month
    sql = """
        SELECT m.name,
               COUNT(*) AS total_classes,
               GROUP_CONCAT(c.className, ', ') AS classes_attended,
               GROUP_CONCAT(DISTINCT c.classType, ', ') AS class_types
        FROM Attends a
        JOIN Member m ON a.memberId = m.memberId
        JOIN Class c ON a.classId = c.classId
        WHERE a.attendanceDate >= date('now', '-1 month')
        GROUP BY m.memberId, m.name;
    """
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        print("[INFO] Query 10: Recent class attendance (last month)")
        if rows:
            print("Member Name | Total Classes Attended | Classes Attended | Class Types")
            print("================================================================================")
            for row in rows:
                print(" | ".join(str(col) for col in row))
        else:
            print("No classes attended in the last month.")
    except Error as e:
        print(f"[ERROR] Query 10 failed: {e}")



def main():
    # Ensure the user provided at least the query number argument
    if len(sys.argv) < 2:
        print("Usage: python QueryApp.py <query_number> [additional parameters]")
        sys.exit(1)
    
    query_number = sys.argv[1]
    # Establish connection to the database
    conn = create_connection()
    
    if conn is None:
        print("[ERROR] Failed to establish database connection.")
        sys.exit(1)
    
    try:
        # Dispatch to the appropriate query based on the command-line argument.
        if query_number == '1':
            query1(conn)
        elif query_number == '2':
            query2(conn)
        elif query_number == '3':
            if len(sys.argv) < 3:
                print("Usage: python QueryApp.py 3 <classId>")
                sys.exit(1)
            # Convert argument to integer for the class ID
            class_id = int(sys.argv[2])
            query3(conn, class_id)
        elif query_number == '4':
            if len(sys.argv) < 3:
                print("Usage: python QueryApp.py 4 <equipment_type>")
                sys.exit(1)
            equipment_type = sys.argv[2]
            query4(conn, equipment_type)
        elif query_number == '5':
            query5(conn)
        elif query_number == '6':
            if len(sys.argv) < 3:
                print("Usage: python QueryApp.py 6 <instructorId>")
                sys.exit(1)
            instructor_id = int(sys.argv[2])
            query6(conn, instructor_id)
        elif query_number == '7':
            query7(conn)
        elif query_number == '8':
            query8(conn)
        elif query_number == '9':
            if len(sys.argv) < 3:
                print("Usage: python QueryApp.py 9 <classType>")
                sys.exit(1)
            class_type = sys.argv[2]
            query9(conn, class_type)
        elif query_number == '10':
            query10(conn)
        else:
            print("Invalid query number. Please provide a query number between 1 and 10.")
    except Error as e:
        print(f"[ERROR] An error occurred: {e}")
    finally:
        # Always close the database connection when done
        close_connection(conn)



if __name__ == '__main__':
    main()
