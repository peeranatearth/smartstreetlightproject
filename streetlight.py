
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import json
import math
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
api = Api(app)
CORS(app)

db = mysql.connector.connect(
	host="35.225.231.240",
	user="root",
	passwd="12345",
	database="streetlight"
);

sql = "SELECT COUNT(*) FROM `light_history` WHERE location=%s AND sensor_data=TRUE"
sqlLatestData = "SELECT * FROM `light_history` WHERE `location`=%s ORDER BY `datetime` DESC LIMIT 1"

class streetlight_status(Resource):
        def get(self, province, district):
		data = {};

		cursor = db.cursor(prepared=True);
		cursor.execute(sql, (district,))
		result = cursor.fetchone()

		cursor = db.cursor(prepared=True);
		cursor.execute(sqlLatestData, (district,));
		latestData = cursor.fetchone()
		print(result)
		print(district)
		print(latestData[2])

		if len(result) != 0:
			if result[0] == 0:
				data = {}
			else:
				data = {
                                        "projectid":"SmartStreetlight",
                                        "sensorid":59011602,
					"location": [13.727263, 100.776324],
					"lighton": str(latestData[2] != 0),
					"usagelefthours": str(50000 - math.ceil(result[0] / 4.0 / 60.0)),
					"usedmins": str(math.ceil(result[0] / 4.0))
				}

		return data

api.add_resource(streetlight_status, '/api/v1/province/<province>/district/<district>/smart_streetlight')

if __name__ == '__main__':
	app.run(host = '0.0.0.0', port='18080', threaded=True)
