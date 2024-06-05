import pandas as pd
import csv
from tkinter import Tk, filedialog

# Initialize Tkinter
root = Tk()
root.withdraw()  # Hide the main window

# Prompt the user to select the first Excel file
print("Select the first Excel file:")
file_path_1 = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])

# Prompt the user to select the second CSV file
print("Select the second CSV file:")
file_path_2 = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])

# Load the data from the Excel file (file_path_1) into memory
df1 = pd.read_excel(file_path_1)

# Load only the second column (column B) of the CSV file (file_path_2) into memory
with open(file_path_2, 'r') as csvfile:
    csv_reader = csv.reader(csvfile)
    data = [row[1] for row in csv_reader]  # Extract values from the second column only

# Convert the data to DataFrame
df2 = pd.DataFrame(data, columns=['Processed Email Alias'])  # Assign column name

# Preprocess the values in the second column (column B) of the CSV file
def preprocess_email_alias(email_alias):
    # Remove the '@' symbol
    email_alias = email_alias.replace('@', '')
    # Replace underscores with spaces
    email_alias = email_alias.replace('_', ' ')
    # Delete the 'aber-' prefix if it exists
    if email_alias.startswith('aber-'):
        email_alias = email_alias[len('aber-'):]
    return email_alias.lower()  # Convert to lowercase for case-insensitive comparison

# Apply preprocessing to the values in the 'Processed Email Alias' column
df2['Processed Email Alias'] = df2['Processed Email Alias'].apply(preprocess_email_alias)

# Add the 'Processed Email Alias' column to df1 after processing the email alias
df1['Processed Email Alias'] = df1['Email alias'].str.lower()

# Compare the values in column A of the Excel file with the processed values from column B of the CSV file
matches = df1['Processed Email Alias'].isin(df2['Processed Email Alias'])

# Create a DataFrame with the results
comparison_results = df1.copy()
comparison_results['Match'] = matches

# Save the comparison results to a new Excel file
output_file_path = 'comparison_results.xlsx'
comparison_results.to_excel(output_file_path, index=False)

print(f"Comparison results saved to {output_file_path}")
