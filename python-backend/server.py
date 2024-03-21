from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # This is fine for development, but for production we need to restrict to our frontend domain for security
# CORS(app, resources={r"/api/*": {"origins": "http://OurFrontendDomain.com"}})


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


if __name__ == "__main__":
    app.run(debug=True)