import xml.etree.ElementTree as ET
import geojson
import time
import datetime
import psycopg2
import urllib.request
import shutil
from shutil import copyfile

#stations_id = [
#	'IKNFLITT3',
#	'ICOLOGNE64',
#	'INORDRHE723',
#	'ICOLOGNE202',
#	'ICOLOGNE205',
#	'INRWCOLO2',
#	'ICOLOGNE208',
#	'INORDRHE191',
#	'ICOLOGNE211'
#	]

#Set Timestamp
ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
st_file = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H:%M:%S')

#Create Connection to pg and set a cursor // 
conn = psycopg2.connect(" DATABASE SETTINGS IN HERE ")
cur = conn.cursor()

#Copy current file to last
copyfile('data/current.geojson', 'data/last.geojson')

#Read last
last_file = open("data/last.geojson", "rt")
contents = last_file.read()
last_json = geojson.loads(contents)
last_file.close()

#Method for filtering redundant data; i[:3] is ['lat', 'lng', 'ts'] and it only itterates through the last result
def check_moved(element):
	for i in last_json:
		if element == i[:3]:
			return True

#Download current file
urllib.request.urlretrieve('https://api.nextbike.net/maps/nextbike-live.xml?city=14', 'data/nextbike-live.xml')

#Download Weather-Data from wunderground.com for Stations in Cologne
#for x in stations_id:
#	url = 'http://api.wunderground.com/api/11cc4d8cbaef94bf/geolookup/conditions/forecast/q/pws:'+x+'.json'
#	file_name = 'data/weather/'+str(st_file)+'_'+x+'.json'
#	urllib.request.urlretrieve(url, file_name)

#Parse xml-data from nextbike
tree = ET.parse('data/nextbike-live.xml')
root = tree.getroot()

#Initialise List Variable for current api-call
curr_data = []

#This loop runs through the parsed xml, and clean the data
for place in root.iter('place'):
	#curr_data.append(place.attrib)

	#Those are the Values we use from the api-call
	bike_number = place.get('bike_numbers')
	bike_lat = place.get('lat')
	bike_lng = place.get('lng')

	#Here we sort empty bike-stations out and split bikes that are on the same station.
	#An item is a further line in the pg-db
	if bike_number is not None:
		if ',' in str(bike_number):
			x = bike_number.split(',')
			for bike_number in x:
				item = [bike_number, bike_lat, bike_lng, st]
		else:
			item = [bike_number, bike_lat, bike_lng, st]

		#print(item[:3])
		if check_moved(item[:3]) != True:
			#Insert the data to our pg-db 
			cur.execute("INSERT into bikes(bikeid, lat, lng, ts) VALUES (%s, %s, %s, %s)", item)
		
		#Append item to current data list
		curr_data.append(item)

#Dump data from list as json and save it in filesystem
json_out = geojson.dumps(curr_data)
with open('data/current.geojson', 'w') as f:
    f.write(json_out)
f.closed

#Commit changes and close db-connection
conn.commit()
conn.close()
