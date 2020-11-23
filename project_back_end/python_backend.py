from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
import json
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})

app.config['DBNAME'] = 'INFS740db'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/INFS740db'

mongo = PyMongo(app)

def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError


@app.route('/create', methods=['POST'])
def add_studyplan():
	db_operations_user = mongo.db.students
	data = request.get_json()
	db_operations_user.insert_one(data)
	res = jsonify('Successfully')
	return res


@app.route('/getallSP')
def getallStudyPlan():
	db_operations_user = mongo.db.students
	result = db_operations_user.distinct('studyPlans')
	res = dumps(result)
	return res	

if __name__ == '__main__':
	app.run(debug=True)
