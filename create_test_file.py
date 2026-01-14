import pandas as pd

# Create a DataFrame with sample URLs
data = {'URLs': ['https://www.python.org', 'https://www.djangoproject.com', 'https://flask.palletsprojects.com']}
df = pd.DataFrame(data)

# Write the DataFrame to an Excel file
try:
    df.to_excel('leads.xlsx', index=False, header=False)
    print("Successfully created 'leads.xlsx' with sample data.")
except Exception as e:
    print(f"Error creating 'leads.xlsx': {e}")
