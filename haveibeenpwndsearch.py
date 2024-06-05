import pandas as pd

# Prompt the user for the file paths
file_path_1 = input("Enter the path to the first Excel file: ")
file_path_2 = input("Enter the path to the second Excel file: ")

# Load the data from the Excel files
df1 = pd.read_excel(file_path_1)
df2 = pd.read_excel(file_path_2)

# Preprocess the 'Email alias' column
def preprocess_email_alias(email_alias):
    # Remove the '@' symbol
    email_alias = email_alias.replace('@', '')
    # Replace underscores with spaces
    email_alias = email_alias.replace('_', ' ')
    # Delete the 'aber-' prefix if it exists
    if email_alias.startswith('aber-'):
        email_alias = email_alias[len('aber-'):]
    return email_alias.lower()  # Convert to lowercase for case-insensitive comparison

# Apply preprocessing to the 'Email alias' column
df2['Processed Email Alias'] = df2['Email alias'].apply(preprocess_email_alias)

# Convert the 'User' column to lowercase for case-insensitive comparison
df1['User'] = df1['User'].str.lower()

# Compare the processed 'Email alias' with the 'User' column from the first file
matches = df2['Processed Email Alias'].isin(df1['User'])

# Create a DataFrame with the results
comparison_results = df2.copy()
comparison_results['Match'] = matches

# Save the comparison results to a new Excel file
output_file_path = 'comparison_results.xlsx'
comparison_results.to_excel(output_file_path, index=False)

print(f"Comparison results saved to {output_file_path}")
