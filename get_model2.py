import mysql.connector
import json

# Replace these values with your database credentials
host = 'localhost'
database = 'wr-osticket-db'  # Replace with your database name
user = 'ahmed'  # Replace with your MySQL username
password = ''  # Replace with your MySQL password



# Connect to your MySQL database
conn = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database
)

# Create a cursor
cursor = conn.cursor()

# Define the SQL query
query = """SELECT 
  entry_id,
  CASE
        WHEN e.field_id = 39 THEN 'Manufacturer'
        WHEN e.field_id = 40 THEN 'Model'
        WHEN e.field_id = 41 THEN 'Year of Manufacturer'
        ELSE "ECU Number"
    END AS "Fields", 
   value FROM 
ost_form_entry_values e WHERE e.field_id IN (39,40,41,42)"""

# Execute the query
cursor.execute(query)

# Fetch all the results
results = cursor.fetchall()

# Define a list to hold the data
data_list = []

# Iterate through the results and create a dictionary for each row
for result in results:
    data_dict = {
        "entry_id": result[0],
        "Fileds": result[1],  # Replace with the actual field name
        "value": result[2]  # Replace with the actual field name
        # Add more fields as needed
    }
    data_list.append(data_dict)

# Close the cursor and database connection
cursor.close()
conn.close()

# Create a JSON object
json_data = json.dumps(data_list, indent=4)

with open('model_data_All_fields.json', 'w') as outfile:
    outfile.write(json_data)