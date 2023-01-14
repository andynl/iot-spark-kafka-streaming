from flask import Flask
from flask_pymongo import PyMongo
from flask.json import jsonify

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/sensors"
mongo_client = PyMongo(app)
db = mongo_client.db

@app.route('/', methods=['GET'])
def get_sensor():
    print(db.sensors.find({}))
    return jsonify([i for i in db.sensors.find({}, {'_id': False})])

if __name__ == '__main__':
    app.run(debug=True)