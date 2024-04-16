import os
from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_cors import CORS
import oracledb
from config import OracleConfig
import json
from dotenv import load_dotenv
import datetime

load_dotenv()

app = Flask(__name__)
CORS(app) # This is fine for development, but for production we need to restrict to our frontend domain for security
# CORS(app, resources={r"/api/*": {"origins": "http://OurFrontendDomain.com"}})

# config database instance
db = OracleConfig()


# initializes the session with the database
def init_session(connection):
    cursor = oracledb.Cursor(connection)
    cursor.execute("""
        ALTER SESSION SET
            TIME_ZONE = 'UTC'
            NLS_DATE_FORMAT = 'YYYY-MM-DD HH24:MI'""")
    return cursor

# Closes database cursor and connection
def end_connection(connection, cursor):
    cursor.close()
    connection.close()


def convert_datetime(data):
    """ Converts datetime objects to strings in a dictionary. """
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, datetime.datetime):
                data[key] = value.strftime('%Y-%m-%d %H:%M:%S')
    return data


def execute_query(query):
    with oracledb.connect(user=db.username, password=db.password, dsn=db.connection_string) as connection:
        with init_session(connection) as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
            results = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]
            results = [convert_datetime(row) for row in results]
            json_object = json.dumps(results, indent=4)
            with open("sample.json", "w") as outfile:
                outfile.write(json_object)
            return results



def test_execute_query():
    with oracledb.connect(user=db.username, password=db.password, dsn=db.connection_string) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM GAMES FETCH FIRST 100 ROWS ONLY")
            rows = cursor.fetchall()
            results = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]

            results = [convert_datetime(row) for row in results]
            json_object = json.dumps(results, indent=4)
            with open("sample.json", "w") as outfile:
                outfile.write(json_object)
            return results


@app.route('/api/query-openings', methods=['POST'])
def query_openings():
    data = request.json
    print(data)
    # moves = data['moves']
    # filters = data['filters']

    # Query Oracle database for resulting moves based on previously input moves and filters

    # followup_moves_in_database = query_database(moves, filters)

    # Sample response
    followup_moves_in_database = "e4 = 2534", "d4 = 1745", "Nf3 = 927"
    
    return jsonify(followup_moves_in_database)


@app.route('/api/query-results', methods=['POST'])
def query_results():
    data = request.json
    opening_moves = data['openingMoves']
    filters = data['filters']
    # Query Oracle database for winrates over time based on selected opening moves and filters
    # results = query_winrate_over_time(opening_moves, filters)
    results = {}  # Replace with actual database query result
    return jsonify(results)


@app.route('/api/test-query', methods=['GET'])
def api_test_query():
    app.logger.info("Handling /api/test-query request")
    try:
        results = test_execute_query()
        app.logger.info(f"Query returned {len(results)} results")
        return jsonify(results), 200
    except Exception as e:
        app.logger.error(f"An error occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store'
    return response



if __name__ == "__main__":
    app.run(debug=True)
