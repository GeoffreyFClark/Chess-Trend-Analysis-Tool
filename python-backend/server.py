from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Members API Route
@app.route('/members')
def members():
    return ({'members': ['member1', 'member2', 'member3']})

if __name__ == "__main__":
    app.run(debug=True)