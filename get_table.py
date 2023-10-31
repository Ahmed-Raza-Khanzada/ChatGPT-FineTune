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

# Modified SQL query
sql_query = """
SELECT
    t.ticket_id,
    e.created AS "Message Time",
    CASE
        WHEN e.type = 'M' THEN 'User Message'
        WHEN e.type = 'R' THEN 'Response'
        ELSE e.type
    END AS "Message Type",
    e.body AS "Message Content",

FROM
    ost_ticket t
JOIN
    ost_thread_entry e ON t.ticket_id = e.thread_id
WHERE
    e.type IN ('M', 'R')
ORDER BY
    t.ticket_id, e.created;

"""
# sql_query = """
# SELECT entry_id,value FROM ost_form_entry_values WHERE field_id = 40;
# """

try:
    cursor.execute(sql_query)
    results = cursor.fetchall()

    # Process the results
    data_list = []
    for result in results:
        ticket_id, message_time, message_type, message_content,value = result
        # entry_id ,value = result
        data_list.append({
            "Ticket ID": ticket_id,
            "Message Time": message_time,
            "Message Type": message_type,
            "Message Content": message_content,
            "Value": value
        })
        # data_list.append({
        #     "entry_id": entry_id,
     
        #     "Value": value
        # })

    # Convert to JSON
    json_data = json.dumps(data_list, indent=4, cls=DateTimeEncoder)

    # Write to file
    with open('ticket_messages.json', 'w') as json_file:
        json_file.write(json_data)

    print("JSON data has been written to 'ticket_messages.json'.")

except mysql.connector.Error as err:
    print(f"Error: {err}")
finally:
    cursor.close()
    connection.close()
