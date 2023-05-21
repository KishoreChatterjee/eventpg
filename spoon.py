from flask import Flask, request, render_template, redirect, url_for, flash
import json
from database import Database
import sqlite3

#define the flask app and route
app = Flask(__name__, template_folder='static/templates')
app.secret_key = 'mysecretkey'

# create an instance of the Database class to connect to the database
db = Database(host='localhost', user='root', password='', database='parties')


@app.route("/")
def home():
    return render_template("spoon.html", message="Invalid email or password")

@app.route("/signup", methods=["POST"])
def signup():
    email = request.form["email2"]
    password = request.form["password2"]
    confirm_password = request.form["password3"]
    print(email)
    print(password)
    if len(email) == 0 or len(password) == 0 or len(confirm_password) == 0:
        flash("Please fill in all fields", "warning")
        return redirect(url_for("home"))
    elif password != confirm_password:
        flash("Passwords do not match", "warning")
        return redirect(url_for("home"))
    else:
        with open("login.json") as f:
            data = json.load(f)

        for user in data["user_login"]:
            if user["email"] == email:
                flash("User already exists", "warning")
                return redirect(url_for("home"))

        new_user = {
            "email": email,
            "password": password
        }
        data["user_login"].append(new_user)

        with open("login.json", "w") as f:
            json.dump(data, f, indent=4)

        flash("Account created successfully!", "success")
        return redirect(url_for("home"))

@app.route("/login", methods=["POST"])
def login():
    print("login page")# Get the email and password from the form data
    email = request.form["email"]
    password = request.form["password"]


    # Check if the email and password are valid
    if len(email) == 0 or len(password) == 0:
        flash("Please fill in all fields", "warning")
        return redirect(url_for("home"))
    else:
        with open('login.json') as f:
            data = json.load(f)

        for users in data['user_login']:
            if users['email'] == email and users['password'] == password:
                flash("Logged in successfully!", "success")
                return redirect(url_for("home"))

        flash("Invalid email or password", "warning")
        return redirect(url_for("home"))

@app.route("/login.json", methods=["GET"])
def login_json():
    with open('login.json') as f:
        data = json.load(f)

    return json.dumps(data['user_login'])


@app.route('/event_dashboard')
def event_dashboard():
    events = db.get_all_events()

    return render_template('EventDB.html', events=events)

@app.route('/register', methods=['POST'])
def register():
    event_name = request.form['event-name']
    event_date_time = request.form['event-date-time']
    contact_email = request.form['contact-person-email']

    if db.check_registration_exists(event_name, event_date_time, contact_email):
        flash("Registration already exists", "warning")
    else:
        event_location = request.form['event-location']
        registration_deadline = request.form['registration-deadline']
        registration_fee = request.form['registration-fee']
        contact_name = request.form['contact-person-name']

        db.register(event_name, event_date_time, event_location,registration_deadline, registration_fee, contact_name, contact_email)
        flash("Registration created successfully!", "success")

    return redirect(url_for('event_dashboard'))


if __name__ == "__main__":
    app.run(debug=True)
