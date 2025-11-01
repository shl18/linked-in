#!/usr/bin/env python3
"""
Create a sample Excel file for LinkedIn contacts
"""

import pandas as pd

# Sample data
data = {
    'Name': ['John Doe', 'Jane Smith', 'Bob Johnson', 'Alice Brown', 'Charlie Wilson'],
    'LinkedIn URL': [
        'https://www.linkedin.com/in/johndoe',
        'https://www.linkedin.com/in/janesmith', 
        'https://www.linkedin.com/in/bobjohnson',
        'https://www.linkedin.com/in/alicebrown',
        'https://www.linkedin.com/in/charliewilson'
    ],
    'Industry': ['Technology', 'Marketing', 'Finance', 'Healthcare', 'Education']
}

# Create DataFrame
df = pd.DataFrame(data)

# Save to Excel file
df.to_excel('sample_contacts.xlsx', index=False)

print("Sample Excel file created: sample_contacts.xlsx")
print("Columns: Name, LinkedIn URL, Industry")
print("You can use this as a template for your own contacts.")
