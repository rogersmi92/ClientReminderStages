from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import os
import logging
from dotenv import load_dotenv
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime
import pandas as pd
import logging

from datetime import datetime
import pandas as pd
import logging

from datetime import datetime
import pandas as pd
import logging


# Explicitly load the environment file
load_dotenv(dotenv_path="C:/Users/roger/source/repos/Client Reminder Program/environment.env")

# Access environment variables
DATA_FILE = os.getenv("DATA_FILE_PATH")
FLASK_DEBUG = os.getenv("FLASK_DEBUG", "False").lower() in ("true", "1", "yes")
SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

# Validate the DATA_FILE path
if not DATA_FILE:
    raise ValueError("DATA_FILE_PATH is not set in the .env file. Please check environment.env.")
if not os.path.exists(DATA_FILE):
    raise FileNotFoundError(f"The data file was not found at the specified path: {DATA_FILE}. Ensure the file path is correct.")

# Configure logging
logging.basicConfig(level=getattr(logging, LOG_LEVEL, logging.INFO))


# Initialize Flask app
app = Flask(__name__)

# Place near Flask initialization
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"  # Redirect unauthenticated users to the login page

# Create User Class
class User(UserMixin):
    """Represents a logged-in user."""
    def __init__(self, email, role):
        self.id = email
        self.role = role

# How to load user data
@login_manager.user_loader
def load_user(email):
    logging.info(f"Loading user: {email}")
    staff_data = load_excel_data("Staff")
    if staff_data.empty:
        logging.error("Staff sheet is empty or not found.")
        return None

    staff = staff_data[staff_data["Email"] == email]
    if not staff.empty:
        logging.info(f"User {email} loaded successfully.")
        return User(email=staff.iloc[0]["Email"], role=staff.iloc[0]["Role"])
    logging.warning(f"User {email} not found.")
    return None

# Configure Flask app
app.secret_key = SECRET_KEY

# Configure logging
logging.basicConfig(level=getattr(logging, LOG_LEVEL, logging.INFO))

from flask_login import login_required, current_user

@app.route("/staff")
@login_required
def staff():
    # Example dashboard content
    if current_user.role != "Staff" and current_user.role != "Admin":
        return "Unauthorized", 403

    return render_template("staff_dashboard.html", user=current_user)


import pandas as pd
import logging

DATA_FILE = r"C:\Users\roger\source\repos\Client Reminder Program\HousingHelp.xlsx"

def load_excel_data(sheet_name):
    """
    Load data from the specified sheet in the Excel file.
    :param sheet_name: Name of the Excel sheet to load.
    :return: A pandas DataFrame containing the sheet's data, or an empty DataFrame if an error occurs.
    """
    try:
        # Load the specified sheet from the Excel file
        df = pd.read_excel(DATA_FILE, sheet_name=sheet_name)
        logging.info(f"Successfully loaded data from sheet: {sheet_name}")
        return df
    except FileNotFoundError:
        logging.error(f"Excel file not found at path: {DATA_FILE}")
        return pd.DataFrame()
    except ValueError as ve:
        logging.error(f"Error loading sheet '{sheet_name}': {ve}")
        return pd.DataFrame()
    except Exception as e:
        logging.error(f"Unexpected error while loading Excel data: {e}")
        return pd.DataFrame()

# Route for the home page
@app.route("/")
def home():
    logging.info("Rendering the home page.")
    return render_template("index.html")

# Route for staff login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        logging.info(f"Login attempt for email: {email}")
        staff_data = load_excel_data("Staff")
        staff = staff_data[staff_data["Email"] == email]
        if staff.empty:
            logging.warning(f"Login failed: Email {email} not found.")
            return "Invalid email or password", 401

        hashed_password = staff.iloc[0]["Password"]
        if not verify_password(hashed_password, password):
            logging.warning(f"Login failed: Invalid password for email {email}.")
            return "Invalid email or password", 401

        user = User(email=staff.iloc[0]["Email"], role=staff.iloc[0]["Role"])
        login_user(user)
        logging.info(f"User {email} logged in successfully.")
        return redirect("/dashboard")

    return render_template("login.html")

# Logout route
@app.route("/logout")
@login_required
def logout():
    logout_user()
    logging.info("User logged out successfully.")
    return redirect("/login")

# Dashboard route
@app.route("/dashboard")
@login_required
def dashboard():
    return f"Welcome, {current_user.id}! Your role is {current_user.role}."

# Admin-only route
@app.route("/admin_only")
@login_required
def admin_only():
    if current_user.role != "Admin":
        logging.warning(f"Unauthorized access attempt by user: {current_user.id}")
        return "Unauthorized", 403
    logging.info(f"Admin panel accessed by user: {current_user.id}")
    return "Admin panel"

# Route for form submission
@app.route("/submit", methods=["POST"])
def submit():
    case_number = request.form.get("case_number")
    if not case_number:
        logging.warning("No case number provided in the form.")
        return render_template("error.html", message="Please provide a case number."), 400
    logging.info(f"Received case number: {case_number}")
    return redirect(url_for("update_form", case_number=case_number))

# Route to update form
@app.route("/update/<case_number>")
def update_form(case_number):
    logging.info(f"Fetching data for case number: {case_number}")
    try:
        client_data = fetch_client_data(case_number)
        if not client_data:
            logging.warning(f"No data found for case number: {case_number}")
            return render_template("error.html", message=f"No client found with Case Number {case_number}"), 404

        logging.info(f"Data fetched successfully for case number: {case_number}")
        return render_template("update_form.html", case_number=case_number, client_data=client_data)
    except Exception as e:
        logging.error(f"Error fetching data for case number {case_number}: {e}")
        return render_template("error.html", message="An error occurred while fetching client data."), 500

# Route to handle form submission and update client data
@app.route("/update_submit", methods=["POST"])
def update_submit():
    case_number = request.form.get("case_number")
    if not case_number:
        logging.error("Case number not provided in the form.")
        return render_template("error.html", message="Please provide a case number."), 400

    logging.info(f"Updating data for case number: {case_number}")

    full_name = request.form.get("full_name")
    dob = request.form.get("dob")
    counselor = request.form.get("counselor")

    try:
        df = pd.read_excel(DATA_FILE, sheet_name="MainSheet")
        df["Case Number"] = df["Case Number"].astype(str).str.strip()
        case_number = str(case_number).strip()

        client_row_index = df[df["Case Number"] == case_number].index
        if client_row_index.empty:
            logging.warning(f"No matching data for case number: {case_number}")
            return render_template("error.html", message=f"No client found with Case Number {case_number}"), 404

        row_index = client_row_index[0]
        changes = {}
        if full_name:
            changes["Name"] = (df.at[row_index, "Name"], full_name)
            df.at[row_index, "Name"] = full_name
        if dob:
            changes["DOB"] = (df.at[row_index, "DOB"], dob)
            df.at[row_index, "DOB"] = dob
        if counselor:
            changes["Counselor"] = (df.at[row_index, "Counselor"], counselor)
            df.at[row_index, "Counselor"] = counselor

        # Log changes
        log_entries = []
        for field, (old_value, new_value) in changes.items():
            log_entries.append({
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Case Number": case_number,
                "Field": field,
                "Old Value": old_value,
                "New Value": new_value,
            })

        log_df_new = pd.DataFrame(log_entries)

        # Save updated data
        with pd.ExcelWriter(DATA_FILE, mode="a", engine="openpyxl", if_sheet_exists="replace") as writer:
            df.to_excel(writer, sheet_name="MainSheet", index=False)
            if "ChangeLog" in pd.ExcelFile(DATA_FILE).sheet_names:
                existing_log = pd.read_excel(DATA_FILE, sheet_name="ChangeLog")
                combined_log = pd.concat([existing_log, log_df_new], ignore_index=True)
                combined_log.to_excel(writer, sheet_name="ChangeLog", index=False)
            else:
                log_df_new.to_excel(writer, sheet_name="ChangeLog", index=False)

        logging.info(f"Data for case number {case_number} updated successfully with change log.")
        return f"Case Number {case_number} updated successfully, and changes logged."

    except FileNotFoundError:
        logging.error(f"Excel file not found at {DATA_FILE}")
        return render_template("error.html", message="Data file not found. Please check the file path."), 500
    except Exception as e:
        logging.error(f"An error occurred while updating data: {e}")
        return render_template("error.html", message=f"An unexpected error occurred: {e}"), 500




def fetch_client_data(case_number):
    try:
        df = pd.read_excel(DATA_FILE, sheet_name="MainSheet")
        logging.info("Loaded Excel file successfully.")

        if "Case Number" not in df.columns:
            logging.error("Missing 'Case Number' column in the Excel file.")
            return {"error": "Missing 'Case Number' column in the data file."}

        df["Case Number"] = df["Case Number"].astype(str).str.strip()
        case_number = str(case_number).strip()

        client_row = df[df["Case Number"] == case_number]
        if client_row.empty:
            logging.warning(f"No matching data for case number: {case_number}")
            return {"error": f"No client found with case number {case_number}"}

        client_data = client_row.iloc[0].to_dict()
        logging.debug(f"Fetched client data: {client_data}")
        return client_data
    except FileNotFoundError:
        logging.error(f"Data file not found: {DATA_FILE}")
        return {"error": "Data file not found."}
    except Exception as e:
        logging.error(f"Error fetching client data: {e}")
        return {"error": f"Unexpected error: {e}"}

def hash_password(password):
    return generate_password_hash(password)

def verify_password(hashed_password, input_password):
    return check_password_hash(hashed_password, input_password)

def hash_all_staff_passwords():
    staff_data = load_excel_data("Staff")
    if staff_data.empty:
        logging.error("No staff data found.")
        return

    for index, row in staff_data.iterrows():
        if not isinstance(row["Password"], str):
            logging.warning(f"Invalid password format for {row['Email']}. Skipping...")
            continue
        if row["Password"].startswith("pbkdf2:"):
            logging.info(f"Password for {row['Email']} already hashed. Skipping...")
            continue
        hashed_password = hash_password(row["Password"])
        staff_data.at[index, "Password"] = hashed_password
        logging.info(f"Password for {row['Email']} hashed successfully.")

    save_excel_data("Staff", staff_data)
    logging.info("Staff sheet updated with hashed passwords.")

import atexit

def on_exit():
    logging.info("Shutting down Flask app gracefully...")

atexit.register(on_exit)

if __name__ == "__main__":
    logging.info("Starting Flask app...")
    app.run(debug=FLASK_DEBUG)
