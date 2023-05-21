import mysql.connector

def clear_registration_table():
    try:
        conn = mysql.connector.connect(
            host='localhost', user='root', password='', database='parties'
        )
        cursor = conn.cursor()
        cursor.execute("TRUNCATE TABLE registrations")
        cursor.execute("TRUNCATE TABLE events")
        conn.commit()
        print("All registration entries have been deleted successfully")
    except mysql.connector.Error as error:
        print("Failed to delete registration entries: {}".format(error))
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            print("Database connection closed")

clear_registration_table()