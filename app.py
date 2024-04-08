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
        'port': 21037,
        'user': 'mayari',
        'password': 'Mayari123!',
        'database': 'MCO2', # change this to the correct database name
    },
    {
        'host': 'ccscloud.dlsu.edu.ph',
        'port': 21038,
        'user': 'mayari',
        'password': 'Mayari123!',
        'database': 'MCO2', # change this to the correct database name
    }
]

# Function to execute SQL query on the database within a transaction
def execute_query_in_transaction(query, db_config, values=None):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    result = None  # Initialize result here
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

@app.route('/')
def index():
    return render_template('index.html')

# Read operation with search
@app.route('/read')
def read_data():
    search_term = request.args.get('search_term', default='', type=str)
    master_node = db_configs[0]
    if not is_node_online(master_node):
        master_node = db_configs[1]
    query = "SELECT * FROM clinics WHERE clinicid = %s"
    values = (search_term,)

    try:
        results = execute_query_in_transaction(query, master_node, values)
        if not results:
            master_node = db_configs[2]
            results = execute_query_in_transaction(query, master_node, values)
    except mysql.connector.Error as err:
        return str(err)
    return render_template('read.html', results=results)

# Update operation
@app.route('/update', methods=['POST'])
def update_data():
    data = request.form
    values = (data['new_value'], data['id'])
    value = (data['id'],)
    failed_node = None
    search_query = "SELECT Province FROM clinics WHERE clinicid = %s"
    if is_node_online(db_configs[0]):
        master_node = db_configs[0]
    else:
        master_node = db_configs[1]
        failed_node = db_configs[0]
    query = "UPDATE clinics SET IsHospital= %s WHERE clinicid= %s" # change mytable to correct table name
    try:
        if is_node_online(db_configs[0]):
            execute_query_in_transaction(query, master_node, values)
            results = execute_query_in_transaction(search_query, master_node, value)
            result = results[0][0]
            if result == 'Manila' or result == 'Batangas' or result == 'Laguna' or result == 'Bulacan' or result == 'Rizal' or result == 'Cavite' or result == 'Pangasinan' or result == 'Benguet' or result == 'Pampanga' or result == 'Nueva Ecija' or result == 'La Union' or result == 'Quezon' or result == 'Masbate' or result == 'Bataan' or result == 'Occidental Mindoro' or result == 'Cagayan' or result == 'Ilocos Sur' or result == 'Camarines Sur' or result == 'Albay' or result == 'Palawan' or result == 'Ilocos Norte' or result == 'Isabela' or result == 'Catanduanes' or result == 'Camarines Norte' or result == 'Nueva Vizcaya' or result == 'Zambales' or result == 'Tarlac' or result == 'Oriental Mindoro' or result == 'Sorsogon' or result == 'Mountain Province' or result == 'Angeles' or result == 'Marinduque' or result == 'Aurora' or result == 'Batanes' or result == 'Romblon' or result == 'Abra':
                if not is_node_online(db_configs[1]):
                    failed_node = db_configs[1]
                else:
                    master_node = db_configs[1]
                    execute_query_in_transaction(query, master_node, values)
            else:
                if not is_node_online(db_configs[2]):
                    failed_node = db_configs[2]
                else:
                    master_node = db_configs[2]
                    execute_query_in_transaction(query, master_node, values)
        else:
            results = execute_query_in_transaction(search_query, master_node, value)
            if not results:
                master_node = db_configs[2]
                execute_query_in_transaction(query, master_node, values)
            else:
                execute_query_in_transaction(query, master_node, values)
        while failed_node is not None:
            time.sleep(5)
            if is_node_online(failed_node):
                execute_query_in_transaction(query, failed_node, values)
                failed_node = None
    except mysql.connector.Error as err:
        return str(err)
    return render_template('update.html')

# Insert operation
@app.route('/insert', methods=['POST'])
def insert_data():
    data = request.form
    failed_node = None
    if is_node_online(db_configs[0]):
        master_node = db_configs[0]
    else:
        master_node = db_configs[1]
        failed_node = db_configs[0]
    query = "INSERT INTO clinics (clinicid, IsHospital, Province) VALUES (%s, %s, %s)" # change mytable to correct table name
    values = (data['value1'], data['value3'], data['value2'])  # Adjust the keys as needed
    if data['value2'] == 'Manila' or data['value2'] == 'Batangas' or data['value2'] == 'Laguna' or data['value2'] == 'Bulacan' or data['value2'] == 'Rizal' or data['value2'] == 'Cavite' or data['value2'] == 'Pangasinan' or data['value2'] == 'Benguet' or data['value2'] == 'Pampanga' or data['value2'] == 'Nueva Ecija' or data['value2'] == 'La Union' or data['value2'] == 'Quezon' or data['value2'] == 'Masbate' or data['value2'] == 'Bataan' or data['value2'] == 'Occidental Mindoro' or data['value2'] == 'Cagayan' or data['value2'] == 'Ilocos Sur' or data['value2'] == 'Camarines Sur' or data['value2'] == 'Albay' or data['value2'] == 'Palawan' or data['value2'] == 'Ilocos Norte' or data['value2'] == 'Isabela' or data['value2'] == 'Catanduanes' or data['value2'] == 'Camarines Norte' or data['value2'] == 'Nueva Vizcaya' or data['value2'] == 'Zambales' or data['value2'] == 'Tarlac' or data['value2'] == 'Oriental Mindoro' or data['value2'] == 'Sorsogon' or data['value2'] == 'Mountain Province' or data['value2'] == 'Angeles' or data['value2'] == 'Marinduque' or data['value2'] == 'Aurora' or data['value2'] == 'Batanes' or data['value2'] == 'Romblon' or data['value2'] == 'Abra':
        province = "Luzon"
    else:
        province = "Visayas/Mindanao"
    try:
        if is_node_online(db_configs[0]):
            execute_query_in_transaction(query, master_node, values)
            if province == "Luzon":
                if not is_node_online(db_configs[1]):
                    failed_node = db_configs[1]
                else:
                    master_node = db_configs[1]
                    execute_query_in_transaction(query, master_node, values)
            else:
                if not is_node_online(db_configs[2]):
                    failed_node = db_configs[2]
                else:
                    master_node = db_configs[2]
                    execute_query_in_transaction(query, master_node, values)
        else:
            if province == "Visayas/Mindanao":
                master_node = db_configs[2]
                execute_query_in_transaction(query, master_node, values)
            else:
                execute_query_in_transaction(query, master_node, values)
        while failed_node is not None:
            time.sleep(5)
            if is_node_online(failed_node):
                execute_query_in_transaction(query, failed_node, values)
                failed_node = None
    except mysql.connector.Error as err:
        return str(err)
    return render_template('insert.html')

# Report operation
@app.route('/report')
def generate_report():
    master_node = db_configs[0]
    if not is_node_online(db_configs[0]):
        master_node = db_configs[1]
    query = "SELECT count(clinicid) AS NoOfClinics FROM clinics WHERE IsHospital = 'True'" # change mytable to correct table name
    try:
        if is_node_online(db_configs[0]):
            result = execute_query_in_transaction(query, master_node)
            results = result[0][0] if result else 0
        else: 
            # Execute the first query
            result1 = execute_query_in_transaction(query, master_node)
            master_node = db_configs[2]
            # Execute the second query
            result2 = execute_query_in_transaction(query, master_node)
            value1 = result1[0][0] if result1 else 0  # Use 0 if result1 is empty
            value2 = result2[0][0] if result2 else 0  # Use 0 if result2 is empty
            results = value1 + value2
    except mysql.connector.Error as err:
        return str(err)
    return render_template('report.html', results=results)


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