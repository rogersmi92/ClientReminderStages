from flask import Flask, render_template, request
import pandas as pd  # Import pandas for data handling

# Path to your Excel file
DATA_FILE = "Client_Data.xlsx"  # Update this to your file's actual name/path


def fetch_client_data(case_number):
    try:
        # Load the data from the Excel file
        df = pd.read_excel(DATA_FILE)
        print("Loaded columns:", df.columns)  # Debugging: Print the column names

        # Find the row corresponding to the given case number
        client_row = df[df["Case Number"] == case_number]

        if client_row.empty:
            return None  # Return None if no match is found

        # Convert the row to a dictionary for easy access
        return client_row.iloc[0].to_dict()

    except FileNotFoundError:
        return None

