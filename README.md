# CIS556-Auditing-Datasets

## opening, reading, writing and updating common filetypes: text, CSV, and JSON

## reading json files
```
import json
file_opened = open(filename) 			# open file
text_to_import = file_opened.read()		# read file contents
json_text = json.loads(text_to_import)		# convert file to readable format
file_opened.close()				# close file
return json_text				# return contents
```

## writing json files
```
import json
data = {'a':1, 'b':True, 'c':'hello'}		#create data (dictionary, list, etc)

text_to_write = json.dumps(data)		#converts to json format
	#OR
text_to_write = json.dumps(data,indent=4)	#pretty json format with linebreaks

file = open('file2.json','w')			#create the file and open it
file.write(text_to_write)			#write the text to the file
file.close()					#remember to close it
```
