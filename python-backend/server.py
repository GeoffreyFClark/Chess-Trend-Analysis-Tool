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
from flask_sqlalchemy import SQLAlchemy  
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()

app = Flask(__name__)
CORS(app) # This is fine for development, but for production we need to restrict to our frontend domain for security
# CORS(app, resources={r"/api/*": {"origins": "http://OurFrontendDomain.com"}})

# config database instance
db = OracleConfig()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ChessDB_Users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
user_db = SQLAlchemy(app)



app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')  
jwt = JWTManager(app)

# -------------------------------- Models --------------------------------------

class User(user_db.Model):
    id = user_db.Column(user_db.Integer, primary_key=True)
    username = user_db.Column(user_db.String(25), unique=True, nullable=False)
    email = user_db.Column(user_db.String(100), unique=True, nullable=False)
    password_hash = user_db.Column(user_db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_resource_ids(self):
        return [resource.id for resource in self.resources]


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
def sql_complex_trend_query_1(date_min="01-JAN-1942", date_max="12-DEC-2023", elo_min=100, elo_max=3900, turns_min=1, turns_max=201, moves="", graph_by="year", player="", opening_color="", queryNumber=1):
    return queryhelper.query1(date_min, date_max, elo_min, elo_max, turns_min, turns_max, moves, graph_by, player, opening_color, queryNumber)

def sql_complex_trend_query_2(date_min="01-JAN-1942", date_max="12-DEC-2023", elo_min=100, elo_max=3900, turns_min=1, turns_max=201, moves="", graph_by="year", player="", opening_color="", queryNumber=2):
    return queryhelper.query2(date_min, date_max, elo_min, elo_max, turns_min, turns_max, moves, graph_by, player, opening_color, queryNumber)

def sql_complex_trend_query_3(date_min="01-JAN-1942", date_max="12-DEC-2023", elo_min=100, elo_max=3900, turns_min=1, turns_max=201, moves="", graph_by="year", player="", opening_color="", queryNumber=3):
    return queryhelper.query3(date_min, date_max, elo_min, elo_max, turns_min, turns_max, moves, graph_by, player, opening_color, queryNumber)

def sql_complex_trend_query_4(date_min="01-JAN-1942", date_max="12-DEC-2023", elo_min=100, elo_max=3900, turns_min=1, turns_max=201, moves="", graph_by="year", player="", opening_color="", queryNumber=4):
    return queryhelper.query4(date_min, date_max, elo_min, elo_max, turns_min, turns_max, moves, graph_by, player, opening_color, queryNumber)

def sql_complex_trend_query_5(date_min="01-JAN-1942", date_max="12-DEC-2023", elo_min=100, elo_max=3900, turns_min=1, turns_max=201, moves="", graph_by="year", player="", opening_color="", queryNumber=5):
    return queryhelper.query5(date_min, date_max, elo_min, elo_max, turns_min, turns_max, moves, graph_by, player, opening_color, queryNumber)



# ------------------------------------ API Endpoints ----------------------------------------------

# Register endpoint
@app.route('/api/register', methods=['POST'])
def register():
    username = request.json.get('username')
    email = request.json.get('email')
    password = request.json.get('password')

    if User.query.filter_by(username=username).first() is not None:
        return jsonify({"message": "Username already exists"}), 400

    user = User(username=username, email=email)
    user.set_password(password)
    user_db.session.add(user)
    user_db.session.commit()

    return jsonify({"message": "User created successfully"}), 201


# Login endpoint
@app.route('/api/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token)

    return jsonify({"message": "Invalid username or password"}), 401


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



def execute_hardcoded_query(queryNumber, query):
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


@jwt_required()
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


@jwt_required
@app.route('/api/sql-complex-trend-query-<int:query_id>', methods=['POST'])
def handle_complex_query(query_id):
    data = request.get_json()
    app.logger.info(f"Received POST data: {data}")
    query_function = globals().get(f'sql_complex_trend_query_{query_id}')
    try:
        return execute_hardcoded_query(data['queryNumber'], query_function(
            date_min='JAN-' + str(data['startDate']),
            date_max='DEC-' + str(data['endDate']),
            elo_min=int(data['eloRange'][0]),
            elo_max=int(data['eloRange'][1]),
            turns_min=int(data['numTurns'][0]),
            turns_max=int(data['numTurns'][1]),
            moves=data['openingMoves'],
            graph_by=str(data['graphBy']),
            player=data.get('player', ''),
            opening_color=(data['openingColor'].lower() == 'black'),
            queryNumber=int(data['queryNumber']),
        ))
    except KeyError as e:
        app.logger.error(f"Key Error in request parameters: {str(e)}")
        return jsonify({'error': 'Bad Request', 'message': f'Missing parameter: {str(e)}'}), 400
    except ValueError as e:
        app.logger.error(f"Value Error in request parameters: {str(e)}")
        return jsonify({'error': 'Bad Request', 'message': f'Invalid parameter value: {str(e)}'}), 400


@jwt_required()
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
            opening_color=(data['openingColor'].lower() == 'black'),
        )
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
