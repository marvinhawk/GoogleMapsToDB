#
# 1.0. Google Maps to Database
# Input: sanitised KML file saved as .xml
# Output: CSV file with or without headers
#

from xml.etree import ElementTree as ET
import csv

class Location:
	name = ""
	latitude = 0
	longitude = 0

locations = []

headers = 0

print("Input XML file")
while(True):
	filename = input()
	if filename.endswith('.xml'):
		try:
			infile = open(filename)
			break
		except IOError:
			print("Couldn't open {}".format(filename))
	else:
		print("Not an XML file")

outfile = filename.split('.')[0] + '-output.csv'

tree = ET.parse(infile)
root = tree.getroot()

for placemark in root.iter('Placemark'):
	location = Location()
	location.name = placemark[0].text
	
	rawcoordinates = placemark[2][0].text
	cleancoordinates = rawcoordinates.split()
	latLon = cleancoordinates[0].split(',')
	location.latitude = latLon[0]
	location.longitude = latLon[1]

	locations.append(location)

f = open(outfile, 'w')

writer = csv.writer(f)

while(headers != 'yes' and headers != 'y' and headers != 'no' and headers != 'n'):
	print('Include headers?')
	headers = input()
	if headers == 'yes' or headers == 'y':
		writer.writerow(('Name', 'Latitude', 'Longitude'))

for location in locations:
	writer.writerow((location.name, location.latitude, location.longitude))

f.close()
print("CSV file created")
