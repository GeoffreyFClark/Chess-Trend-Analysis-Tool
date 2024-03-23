import os
from flask import Flask, jsonify, render_template
from flask_cors import CORS
import oracledb

username = "willsonr"
password = "H2O3uPTkiLJUJQqVAPPQdnUh"
hostname = "oracle.cise.ufl.edu"
port = 1521
sid = 'orcl'

oracledb.init_oracle_client(lib_dir=r"C:\Program Files\Oracle\instantclient_21_13", config_dir=r"C:\Program Files\Oracle\instantclient_21_13\network\admin\TSAfiles")
dsn_tns = oracledb.makedsn(hostname, port, sid=sid)
connection = oracledb.connect(dsn=dsn_tns, user=username, password=password)

cursor = oracledb.Cursor(connection)
result = cursor.fetchall()

cursor.close()
connection.close()

def init_session(connection, requestedTag_ignored):
    cursor = connection.cursor()
    cursor.execute("""
        ALTER SESSION SET
            TIME_ZONE = 'UTC'
            NLS_DATE_FORMAT = 'YYYY-MM-DD HH24:MI'""")


# start_pool(): starts the connection pool
def start_pool():

    pool_min = 4
    pool_max = 4
    pool_inc = 0
    pool_gmd = oracledb.SPOOL_ATTRVAL_WAIT

    print("Connecting to", os.environ.get("PYTHON_CONNECTSTRING"))

    pool = oracledb.create_pool(user=os.environ.get("PYTHON_USERNAME"),
                                password=os.environ.get("PYTHON_PASSWORD"),
                                dsn=os.environ.get("PYTHON_CONNECTSTRING"),
                                min=pool_min,
                                max=pool_max,
                                increment=pool_inc,
                                threaded=True,
                                getmode=pool_gmd,
                                sessionCallback=init_session)

    return pool

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return "Welcome to the demo app"

# Members API Route
@app.route('/members')
def members():
    return ({'members': ['member1', 'member2', 'member3']})

@app.route('/airports', methods=['GET'])
def get_airports():
    # Establish connection (same as above)
    # Execute query to fetch airports from the database
    # Process the result
    # Return data as JSON
    return jsonify(result)


def execute_query():
    # Connect to the Oracle database
    connection = oracledb.connect("username", "password", "database")

    # Create a cursor
    cursor = connection.cursor()

    # Execute the SQL query
    cursor.execute('SELECT * FROM AIRPORT')

    # Fetch all rows
    rows = cursor.fetchall()

    # Close the cursor and connection
    cursor.close()
    connection.close()

    return rows


# Route to display the results in the browser
@app.route('/')
def display_results():
    # Call the execute_query function to get the results
    results = execute_query()

    # Render a template with the results
    return render_template('results.html', results=results)

if __name__ == "__main__":
    app.run(debug=True)

