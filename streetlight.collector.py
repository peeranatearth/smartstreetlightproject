import mysql.connector
import time

import requests;

db = mysql.connector.connect(
	host="35.225.231.240",
	user="root",
	passwd="12345",
	database="streetlight"
)

def getDataFromDict(d):
	data = d['sensor_data']
	id = d['sensor_id']
	type = d['type']
	location = d['location']

	return data, id, type, location

def getDataFromMagel():
	response = requests.get("https://www.aismagellan.io/api/things/pull/cb0dd550-4fe4-11e9-96dd-9fb5d8a71344")
	data = response.json();
	data['location'] = '1A';

	return [data];

def getDataFromApi():
	response = requests.get("http://35.222.51.59:8080/sensors/project_id/SmartStreetlight")
	data = response.json();

	return data;

sql = "INSERT INTO `light_history` (`location`, `sensor_data`, `sensor_id`, `type`) VALUES (%s, %s, %s, %s)"

while (True):
	sensor_datas = getDataFromMagel()
	dbcursor = db.cursor()

	for streetlight in sensor_datas:
		data, id, type, location = getDataFromDict(streetlight)
		value = ( location, data, id, type, )
		dbcursor.execute(sql, value)

	db.commit();

	print "Record inserted."
	time.sleep(15)
