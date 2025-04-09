import pandas as pd
import mysql.connector


# Load the CSV file
csv_file = "/Users/brandonschwenke/Downloads/daily-sales-03-29-25-example-clean.csv"  # Replace with your file path
selected_columns = ['UPC', 'Description', 'Amt', 'Qty', 'Wgt']
df = pd.read_csv(csv_file, usecols=selected_columns)

# Connect to MySQL Database
conn = mysql.connector.connect(
    host="localhost", 
    user="root", 
    password="73173359", 
    database="TestProductManagement"
)

cursor = conn.cursor()

# Define the table name
table_name = "sales"

# Convert DataFrame to SQL INSERT statement
columns = ", ".join(df.columns)
placeholders = ", ".join(["%s"] * len(df.columns))
insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
df["Amt"] = df["Amt"].replace({"[$,]": ""}, regex=True).astype(float)

#FILTERING 
df = df.dropna(subset=["UPC"])  # Remove rows where UPC is NaN

df["Qty"] = df["Qty"].astype(str).str.replace(r"[^\d.]", "", regex=True).str.strip()
df["Qty"] = pd.to_numeric(df["Qty"], errors="coerce")  # Convert to number, NaN if invalid
df = df.dropna(subset=["Qty"])  # Drop rows where Qty is still NaN
df["Qty"] = df["Qty"].astype(int)  # Convert to integer


print(insert_query)


# Insert rows into database
for row in df.itertuples(index=False, name=None):
    cursor.execute(insert_query, row)

# Commit and close connection
conn.commit()
cursor.close()
conn.close()