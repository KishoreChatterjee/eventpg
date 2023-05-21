import mysql.connector
import requests
from datetime import datetime

class Database:
    def __init__(self, host, user, password, database):
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cur = self.conn.cursor()
        self.cur.execute("SHOW TABLES LIKE 'events'")
        result = self.cur.fetchone()
        if not result:
            self.cur.execute(
                "CREATE TABLE events (id INT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(255), description TEXT, image_url TEXT, event_date DATE)")
            print("Table created successfully")
        else:
            self.cur.execute("SHOW COLUMNS FROM events LIKE 'event_date'")
            result = self.cur.fetchone()
            if not result:
                self.cur.execute("ALTER TABLE events ADD COLUMN event_date DATE")
                print("Column added successfully")

        self.cur.execute("SHOW TABLES LIKE 'registrations'")
        result = self.cur.fetchone()
        if not result:
            self.cur.execute(
                "CREATE TABLE registrations (id INT PRIMARY KEY AUTO_INCREMENT, event_id INT, event_name VARCHAR(255), event_date_time VARCHAR(255), event_location VARCHAR(255), registration_deadline DATE, registration_fee INT, contact_name VARCHAR(255), contact_email VARCHAR(255))")
            print("Table created successfully")

    def add_event(self, name, description, image_url, event_date):
        sql = "INSERT INTO events (name, description, image_url, event_date) VALUES (%s, %s, %s, %s)"
        values = (name, description, image_url, event_date)
        self.cur.execute(sql, values)
        self.conn.commit()

    def get_all_events(self):
        self.cur.execute("SELECT * FROM events")
        rows = self.cur.fetchall()
        return [{'id': row[0], 'name': row[1], 'description': row[2], 'image_url': row[3], 'event_date': row[4]} for row in rows]

    def add_event_from_api(self, api_url):
        response = requests.get(api_url)
        events = response.json()
        for event in events:
            name = event['name']
            description = event['description']
            image_url = event['image_url']
            event_date = datetime.strptime(event['event_date'], '%Y-%m-%d').date()
            self.add_event(name, description, image_url, event_date)


    def register(self, event_name, event_date_time, event_location, registration_deadline, registration_fee, contact_name, contact_email):
        self.cur.execute("INSERT INTO registrations (event_name, event_date_time, event_location, registration_deadline, registration_fee, contact_name, contact_email) VALUES (%s, %s, %s, %s, %s, %s, %s)", (event_name, event_date_time, event_location, registration_deadline, registration_fee, contact_name, contact_email))
        self.conn.commit()

    def check_registration_exists(self, event_name, event_date_time, contact_email):
        self.cur.execute(
            "SELECT id FROM registrations WHERE event_name = %s AND event_date_time = %s AND contact_email = %s",
            (event_name, event_date_time, contact_email))
        result = self.cur.fetchone()
        if not result:
            return False
        event_id = result[0]
        self.cur.fetchall()  # Clear any pending results

        self.cur.execute("SELECT * FROM registrations WHERE event_id = %s AND contact_email = %s",
                         (event_id, contact_email))
        result = self.cur.fetchone()
        if result and result['event_name'] == event_name and result['event_date_time'] == event_date_time:
            return True
        else:
            return False

    def __del__(self):
        self.conn.close()


# Creating an instance of the Database class
db = Database(host='localhost', user='root', password='', database='parties')

# Adding an event to the database
db.add_event(name='Birthday Party', description='Come celebrate my birthday with me!', image_url='https://www.rd.com/wp-content/uploads/2022/07/Happy-Birthday-Messages-FT.jpg?fit=700,1024', event_date='2023-04-20')
db.add_event(name='Marriage receiption', description="Celebrate our marriage with us at our reception party!", image_url='https://vakilsearch.com/blog/wp-content/uploads/2022/05/shutterstock_1697156779-1.jpg', event_date='2023-04-28')
db.add_event(name='Sports event', description="Join us for an exciting day of friendly competition and fun at our annual sports event!", image_url='https://img.freepik.com/free-vector/sport-equipment-concept_1284-13034.jpg?w=360', event_date='2023-04-28')

# Adding events from an API to the database
#db.add_event_from_api(api_url='https://example.com/api/events')
