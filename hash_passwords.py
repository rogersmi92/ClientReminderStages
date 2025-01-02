
import pandas as pd
from werkzeug.security import generate_password_hash

DATA_FILE = r"C:\Users\roger\source\repos\Client Reminder Program\HousingHelp.xlsx"

def hash_all_staff_passwords():
    """Hash all plaintext passwords in the Staff sheet."""
    try:
        # Load the Excel file
        staff_data = pd.read_excel(DATA_FILE, sheet_name="Staff")

        # Check and hash passwords
        for index, row in staff_data.iterrows():
            if not isinstance(row["Password"], str):
                print(f"Invalid password format for {row['Email']}. Skipping...")
                continue
            if row["Password"].startswith("pbkdf2:"):
                print(f"Password for {row['Email']} already hashed. Skipping...")
                continue
            hashed_password = generate_password_hash(row["Password"])
            staff_data.at[index, "Password"] = hashed_password
            print(f"Password for {row['Email']} hashed successfully.")

        # Save the updated Staff sheet back to the Excel file
        with pd.ExcelWriter(DATA_FILE, mode="a", engine="openpyxl", if_sheet_exists="replace") as writer:
            staff_data.to_excel(writer, sheet_name="Staff", index=False)
        print("Staff sheet updated with hashed passwords.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    hash_all_staff_passwords()

    import pandas as pd
from werkzeug.security import generate_password_hash

DATA_FILE = r"C:\Users\roger\source\repos\Client Reminder Program\HousingHelp.xlsx"

def hash_all_staff_passwords():
    """Hash all plaintext passwords in the Staff sheet."""
    try:
        # Load the Excel file
        print(f"Loading Excel file from: {DATA_FILE}")
        staff_data = pd.read_excel(DATA_FILE, sheet_name="Staff")

        print("Initial Staff Data:")
        print(staff_data)

        # Check and hash passwords
        for index, row in staff_data.iterrows():
            if not isinstance(row["Password"], str):
                print(f"Invalid password format for {row['Email']}. Skipping...")
                continue
            if row["Password"].startswith("pbkdf2:"):
                print(f"Password for {row['Email']} already hashed. Skipping...")
                continue
            hashed_password = generate_password_hash(row["Password"])
            staff_data.at[index, "Password"] = hashed_password
            print(f"Password for {row['Email']} hashed successfully.")

        print("Updated Staff Data:")
        print(staff_data)

        # Save the updated Staff sheet back to the Excel file
        with pd.ExcelWriter(DATA_FILE, mode="a", engine="openpyxl", if_sheet_exists="replace") as writer:
            staff_data.to_excel(writer, sheet_name="Staff", index=False)
        print("Staff sheet updated with hashed passwords.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    hash_all_staff_passwords()

    import pandas as pd

DATA_FILE = r"C:\Users\roger\source\repos\Client Reminder Program\HousingHelp.xlsx"

# Debug: Print sheet names
excel_data = pd.ExcelFile(DATA_FILE)
print(f"Available sheets: {excel_data.sheet_names}")
