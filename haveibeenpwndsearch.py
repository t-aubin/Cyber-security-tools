# Make sure to install pandas
# Windows: pip install pandas
# Linux: pip3 install pandas

import pandas as pd
from tkinter import Tk, filedialog
import tkinter as tk
from datetime import datetime

def select_excel_file():
    root = Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls")])
    return file_path

def select_csv_file():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
    return file_path

def process_emails(pre_filtered_emails):
    processed_emails = []
    for email in pre_filtered_emails:
        # Remove "aber-" from the beginning
        if email.startswith("aber-"):
            email = email[5:]
        # Remove "@" and replace underscores with spaces
        email = email.replace("@", "").replace("_", " ")
        processed_emails.append(email.lower())
    return processed_emails

def main():
    excel_file_path = select_excel_file()
    csv_file_path = select_csv_file()

    if excel_file_path and csv_file_path:
        try:
            # Read the Excel file into a DataFrame
            df_excel = pd.read_excel(excel_file_path)

            # Prompt the user for input
            user_input = input("Enter a string to filter breaches (type 'All' to include all): ")

            # Filter the DataFrame based on the user input
            if user_input.lower() == 'all':
                filtered_df_excel = df_excel
            else:
                filtered_df_excel = df_excel[df_excel['Breaches'].str.contains(user_input, na=False)]

            # Get the 'Email alias' values for the filtered rows
            pre_filtered_emails = filtered_df_excel['Email alias'].tolist()

            # Process the emails
            processed_emails = process_emails(pre_filtered_emails)

            # Read the CSV file into a DataFrame
            df_csv = pd.read_csv(csv_file_path)

            # Filter the DataFrame
            filtered_df_csv = df_csv[(df_csv['Disabled'] == 'No') & (df_csv['User Classification'] == 'Human')]

            # Create the CS IDP list
            cs_idp_list = [user.lower() for user in filtered_df_csv['User'].tolist()]

            # Find matches
            matched_users = [email for email in processed_emails if email in cs_idp_list]

            # Get the number of matches
            num_matches = len(matched_users)
            print(f"Number of matches: {num_matches}")

            # Save matched users to a CSV file
            current_date = datetime.now().strftime("%Y-%m-%d")
            output_filename = f"{user_input}_matches_{current_date}.csv"
            pd.DataFrame(matched_users, columns=["Matched Users"]).to_csv(output_filename, index=False)
            print(f"Matched users saved to {output_filename}")

        except Exception as e:
            print(f"An error occurred while reading the files or processing the data: {e}")
    else:
        print("No file selected.")

if __name__ == "__main__":
    main()
