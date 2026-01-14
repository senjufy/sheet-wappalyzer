import pandas as pd

try:
    # Read the Excel file
    df = pd.read_excel('leads.xlsx')
    
    # Print the column headers
    print("File Columns:")
    print(list(df.columns))
    
    # Print the first 5 rows to show the structure
    print("\nFile Head:")
    print(df.head())
    
except FileNotFoundError:
    print("Error: The file 'leads.xlsx' was not found.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
