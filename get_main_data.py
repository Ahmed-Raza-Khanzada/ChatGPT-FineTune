import mysql.connector
import json
from datetime import datetime

# Custom JSON Encoder to handle datetime objects
class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        return super().default(o)

# Database credentials
host = 'localhost'
user = 'ahmed'
password = ''
database = 'wr-osticket-db'

# Establish connection
connection = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database
)
cursor = connection.cursor()

sql_query = """SELECT
    te.thread_id,
    te.created AS "Message Time",
    CASE
        WHEN te.type = 'M' THEN 'User Message'
        WHEN te.type = 'R' THEN 'Response'
        ELSE te.type
    END AS "Message Type",
    te.body AS "Message Content",
    MAX(CASE WHEN fev.field_id = 39 THEN fev.value END) AS Manufacturer,
    MAX(CASE WHEN fev.field_id = 40 THEN fev.value END) AS Model,
    MAX(CASE WHEN fev.field_id = 41 THEN fev.value END) AS "Year of Manufacture",
    MAX(CASE WHEN fev.field_id = 42 THEN fev.value END) AS "ECU Number",
    GROUP_CONCAT(fev.field_id ORDER BY fev.field_id) AS field_id

FROM
    ost_thread_entry te
JOIN
    ost_thread th ON te.thread_id = th.id
JOIN
    ost_form_entry fe ON th.object_id = fe.object_id
JOIN
    ost_form_entry_values fev ON fe.id = fev.entry_id AND fev.field_id IN (39, 40, 41, 42)
JOIN
    ost_ticket t ON te.thread_id = t.ticket_id

WHERE
    te.type IN ('M', 'R')

GROUP BY
    te.thread_id, te.created, te.type, te.body

ORDER BY
    te.thread_id, te.created;
"""

# Establish a database connection
try:
    unique_idss = []
    cursor.execute(sql_query)
    results = cursor.fetchall()
    print("Data Fetched is completed")
    # Process the results
    data_list = []
    for result in results:
       
        ticket_id, message_time, message_type, message_content, Manufacturer,Model,year_of_manufacture,ecu_number,field_id= result
        # entry_id ,value = result
        data_list.append({
            "Thread ID": ticket_id,
            "Message Time": message_time,
            "Message Type": message_type,
            "Message Content": message_content,
            "Manufacturer": Manufacturer,
            "Model": Model,
            "Year of Manufacture": year_of_manufacture,
            "ECU Number": ecu_number,
            "Field ID": field_id
           
        })
        if ticket_id not in unique_idss:
            unique_idss.append(ticket_id)
    json_data = json.dumps(data_list, indent=4, cls=DateTimeEncoder)

    # Write to file
    with open('Final_Ticket_messages.json', 'w') as json_file:
        json_file.write(json_data)
    print(len(set(unique_idss)))
    print("JSON data has been written to 'ticket_messages.json'.")

except mysql.connector.Error as err:
    print(f"Error: {err}")
finally:
    cursor.close()
    connection.close()
