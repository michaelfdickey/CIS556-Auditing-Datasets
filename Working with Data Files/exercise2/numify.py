#numify.py

#converts numbers as strings from imported csv file into into floats

import csv

file = open('file.csv')			# opens file
wrapper = csv.reader(file)		# puts in wrapper with csv.reader


for rpos in range(len(wrapper)):
	print("rpos is:", rpos)