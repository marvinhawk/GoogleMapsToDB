#! usr/bin/env python3
#
# 1.2.1 Google Maps to Database
# Input: KML file
# Output: Name and coordinates of locations in CSV file with or without headers
#


import re, csv

def openFile():
	print("Input KML file")
	while(True):
		filename = input()
		if filename.lower().endswith('.kml'):
			try:
				infile = open(filename)
				return (infile, filename)
			except IOError:
				print("Couldn't open {}".format(filename))
		else:
			print("Not a KML file")

def searchFile(text):
	class Location:
		idNum = 0
		name = ""
		latitude = 0
		longitude = 0
		comments = ""
	
	locations = []
	count = 0

	search = re.compile(r'''
		<Placemark>
		.*?
		<name>
		(.*?)
		</name>
		.*?
		<coordinates>
		(.*?)
		</coordinates>
		.*?
		</Placemark>
		''', re.DOTALL | re.VERBOSE)
	
	results = search.findall(text)

	for result in results:

		location = Location()

		if result[0].startswith('<![CDATA['):
			name = result[0][len('<![CDATA['):].rstrip(']]>')
		else:
			name = result[0]

		location.idNum = count
		location.name = name

		coordinates = result[1].strip().split(',')

		location.longitude = coordinates[0]
		location.latitude = coordinates[1]
		
		locations.append(location)
		
		count +=1

	return locations


def printFile(loc, name):
	outfile = name.split('.')[0] + '-output.csv'
	headers = 0

	f = open(outfile, 'w')

	writer = csv.writer(f)

	while(headers != 'yes' and headers != 'y' and headers != 'no' and headers != 'n'):
		print('Include headers?')
		headers = input()
		if headers == 'yes' or headers == 'y':
			writer.writerow(('ID', 'Name', 'Latitude', 'Longitude', 'Comments'))

	for location in loc:
		writer.writerow((location.idNum,
						location.name,
						location.latitude,
						location.longitude,
						location.comments))

	f.close()
	print("CSV file created")

infile, filename = openFile()

fileStr = infile.read()

places = searchFile(fileStr)

printFile(places, filename)