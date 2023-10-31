import subprocess

# Replace these values with your database credentials
host = 'localhost'
user = 'ahmed'
password = ''
database = 'wr-osticket-db'

# Define the output file name
output_file = 'database_structure.sql'

try:
    # Construct the command to export the database structure
    command = f"mysqldump --no-data --host={host} --user={user} --password={password} {database} > {output_file}"

    # Execute the command using subprocess
    subprocess.run(command, shell=True, check=True)
    
    print(f"Database structure exported to {output_file}")

except subprocess.CalledProcessError as e:
    print(f"Error: {e}")
