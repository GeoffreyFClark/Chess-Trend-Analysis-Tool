import os
from flask import Flask, jsonify, request
from flask_cors import CORS
import oracledb
from config import OracleConfig
import json
from dotenv import load_dotenv
import datetime
import queryhelper
from sql_gen_query import create_sql_query


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


# 5 Hard-Coded Complex Trend SQL Queries
def sql_complex_trend_query_1():
    return "SELECT * FROM games2 FETCH FIRST 2 ROWS ONLY"

def sql_complex_trend_query_2():
    return queryhelper.query2()

def sql_complex_trend_query_3():
    return queryhelper.query3()

def sql_complex_trend_query_4():
    return "SELECT * FROM games2 FETCH FIRST 8 ROWS ONLY"

def sql_complex_trend_query_5():
    return "SELECT * FROM games2 FETCH FIRST 10 ROWS ONLY"


@app.route('/api/sql-complex-trend-query-<int:query_id>', methods=['GET'])
def handle_complex_query(query_id):
    query_function = globals().get(f'sql_complex_trend_query_{query_id}')
    if query_function:
        return execute_query(query_function())
    return jsonify({'error': 'Invalid query id'}), 404


def execute_query(query):
    try:
        with oracledb.connect(user=db.username, password=db.password, dsn=db.connection_string) as connection:
            cursor = connection.cursor()
            app.logger.info(f"Executing SQL Query: {query}")
            cursor.execute(query)
            rows = cursor.fetchall()
            results = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]
            cursor.close()
            return jsonify(results), 200
    except Exception as e:
        app.logger.error(f"SQL Execution Error: {str(e)}")
        return jsonify({'error': str(e)}), 500



def test_execute_query():
    with oracledb.connect(user=db.username, password=db.password, dsn=db.connection_string) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM GAMES2 FETCH FIRST 100 ROWS ONLY")
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
    data = request.get_json()
    app.logger.info(f"Received POST data: {data}")
    try:
        sql_query = create_sql_query(
            date_min=str(data['startDate']),
            date_max=str(data['endDate']),
            elo_min=int(data['eloRange'][0]),
            elo_max=int(data['eloRange'][1]),
            turns_min=int(data['numTurns'][0]),
            turns_max=int(data['numTurns'][1]),
            moves=data['openingMoves'],
            data_metric=data['dataChoice'],
            graph_by=str(data['graphBy']),
            player=data.get('player', ''),
            opening_color=(data['openingColor'].lower() == 'black')
        )
        print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA", sql_query)
        return execute_query(sql_query)
    except KeyError as e:
        app.logger.error(f"Key Error in request parameters: {str(e)}")
        return jsonify({'error': 'Bad Request', 'message': f'Missing parameter: {str(e)}'}), 400
    except ValueError as e:
        app.logger.error(f"Value Error in request parameters: {str(e)}")
        return jsonify({'error': 'Bad Request', 'message': f'Invalid parameter value: {str(e)}'}), 400



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
