#numify.py

#converts numbers as strings from imported csv file into into floats

import csv

file = open('file.csv')			# opens file
wrapper = csv.reader(file)		# puts in wrapper with csv.reader
#table = wrapper 

length = len(wrapper)

for row in wrapper:
	print("row is", row)