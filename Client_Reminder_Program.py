from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import os
import logging
from dotenv import load_dotenv

# Explicitly load the environment file
load_dotenv(dotenv_path="C:/Users/roger/source/repos/Client Reminder Program/Client Reminder Program/environment.env")

# Access environment variables
DATA_FILE = os.getenv("DATA_FILE_PATH")
FLASK_DEBUG = os.getenv("FLASK_DEBUG", "False").lower() in ("true", "1", "yes")
SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

# Validate the DATA_FILE path
if not DATA_FILE:
    raise ValueError("DATA_FILE_PATH is not set in the .env file.")
if not os.path.exists(DATA_FILE):
    raise FileNotFoundError(f"The data file was not found at: {DATA_FILE}")

# Initialize Flask app
app = Flask(__name__)

# Configure Flask app
app.secret_key = SECRET_KEY

# Configure logging
logging.basicConfig(level=getattr(logging, LOG_LEVEL, logging.INFO))

# Route for the home page
@app.route("/")
def home():
    logging.info("Rendering the home page.")
    return render_template("index.html")  # HTML file to serve the form

# Route for form submission
@app.route("/submit", methods=["POST"])
def submit():
    case_number = request.form.get("case_number")
    logging.info(f"Received case number: {case_number}")
    return redirect(url_for("update_form", case_number=case_number))

# Route for the update form
@app.route("/update/<case_number>")
def update_form(case_number):
    logging.info(f"Fetching data for case number: {case_number}")
    client_data = fetch_client_data(case_number)
    if not client_data:
        logging.warning(f"No data found for case number: {case_number}")
        return f"Error: No client found with Case Number {case_number}"
    return render_template("update_form.html", **client_data)

# Route to handle update form submission
@app.route("/update_submit", methods=["POST"])
def update_submit():
    case_number = request.form.get("case_number")
    logging.info(f"Updating data for case number: {case_number}")
    # TODO: Add form data processing logic here
    return f"Case Number {case_number} updated successfully!"

# Helper function to fetch client data
def fetch_client_data(case_number):
    try:
        df = pd.read_excel(DATA_FILE)
        logging.info("Loaded Excel file successfully.")
        # Ensure Case Number column is a string and clean whitespace
        df["Case Number"] = df["Case Number"].astype(str).str.strip()
        # Find the row for the provided case number
        client_row = df[df["Case Number"] == case_number]
        if client_row.empty:
            logging.warning(f"No matching data for case number: {case_number}")
            return None
        logging.info(f"Data found for case number: {case_number}")
        return client_row.iloc[0].to_dict()
    except FileNotFoundError:
        logging.error(f"Data file not found: {DATA_FILE}")
        return None
    except Exception as e:
        logging.error(f"Error fetching client data: {e}")
        return None

# Run the Flask app
if __name__ == "__main__":
    logging.info("Starting Flask app...")
    app.run(debug=FLASK_DEBUG)




