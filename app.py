from flask import Flask, request, render_template
import mysql.connector
import time

app = Flask(__name__)

# Database connection details for each node
db_configs = [
    {
        'host': 'ccscloud.dlsu.edu.ph',
        'port': 21036,
        'user': 'mayari',
        'password': 'Mayari123!',
        'database': 'MCO2', # change this to the correct database name
    },
    {
        'host': 'ccscloud.dlsu.edu.ph',
        'port': 20037,
        'user': 'mayari',
        'password': 'Mayari123!',
        'database': 'MCO2', # change this to the correct database name
    },
    {
        'host': 'ccscloud.dlsu.edu.ph',
        'port': 20038,
        'user': 'mayari',
        'password': 'Mayari123!',
        'database': 'MCO2', # change this to the correct database name
    }
]

# Function to execute SQL query on the database within a transaction
def execute_query_in_transaction(query, db_config, values=None):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    try:
        # Start transaction
        connection.start_transaction(isolation_level='READ COMMITTED')
        
        # Execute query
        cursor.execute(query, values)
        result = cursor.fetchall()
        # Commit transaction
        connection.commit()
    except mysql.connector.Error as err:
        # Rollback transaction on error
        connection.rollback()
        raise err
    finally:
        # Close cursor and connection
        cursor.close()
        connection.close()
        return result


# Read operation with search
@app.route('/read')
def read_data():
    search_term = request.args.get('search_term', default='', type=str)
    master_node = db_configs[0]
    query = "SELECT * FROM mytable WHERE clinicid LIKE %s" # change mytable to correct table name
    values = (f"%{search_term}%",)

    try:
        results = execute_query_in_transaction(query, master_node, values)
        return render_template('index.html', results=results)
    except mysql.connector.Error as err:
        return str(err)

# Update operation
@app.route('/update', methods=['POST'])
def update_data():
    data = request.form
    master_node = db_configs[0]
    query = "UPDATE mytable SET IsHospital=%s WHERE clinicid=%s" # change mytable to correct table name
    values = (data['new_value'], data['id'])
    try:
        execute_query_in_transaction(query, master_node)
    except mysql.connector.Error as err:
        return str(err)
    return 'Updated successfully'

# Insert operation
@app.route('/insert', methods=['POST'])
def insert_data():
    data = request.form
    master_node = db_configs[0]
    query = "INSERT INTO mytable (clinicid, RegionName, IsHospital) VALUES (%s, %s, %s)" # change mytable to correct table name
    values = (data['value1'], data['value2'], data['value3'])  # Adjust the keys as needed
    try:
        execute_query_in_transaction(query, master_node, values)
    except mysql.connector.Error as err:
        return str(err)
    return 'Inserted successfully'

# Report operation
@app.route('/report')
def read_data():
    master_node = db_configs[0]
    query = "SELECT count(clinicid) AS NoOfClinics FROM mytable WHERE IsHospital = 'True'" # change mytable to correct table name
    try:
        results = execute_query_in_transaction(query, master_node)
    except mysql.connector.Error as err:
        return str(err)
    return render_template('index.html', results1=results)


# Function to check if a node is online
def is_node_online(node):
    try:
        connection = mysql.connector.connect(**node)
        connection.close()
        return True
    except mysql.connector.Error:
        return False
    

if __name__ == '__main__':
    app.run(debug=True)