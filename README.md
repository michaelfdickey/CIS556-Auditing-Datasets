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

Included in the tests folder are modules **__main__.py** and **__init__.py**.

**__main__.py**:

- May have an input function to get information from user and a print statement to display the result
- Has to be in the folder in order for the application to run
- Should only contain script code; all other code, including function definitions, should go in other modules
- This has been completed for you

**__init__.py**

- Tells you exactly what you should import

## Files you’ll need to work on:

- **utils.py**: 

- - File and date functions
  - You've already finished these in previous course modules; you just need to cut and paste that work into this file

- **pilots.py**: 

- - Classifies pilot skill level
  - Necessary to find the right weather restrictions
  - Hardest function in the assignment

- **violations.py**: 

- - Checks for weather violations
  - Compare the set restrictions to the current weather
  - Most complex module in the project
  - Many functions; bulk of the work in the project

- **app.py**: Run the application (or test it)

Optional files for an extra challenge:

- **endorsements.py**: 

- - Additional flight violations
  - Verifies that the pilot is certified for specific plane
  - Not that hard; just have to learn more files

- **inspections.py**: 

- - Verification of plane maintenance
  - This is much harder; not broken up into helpers
  - Only for students who want a real challenge


## Loop through two associated lists and create a dictionary from those

```

# Loop through two associated lists and create a dictionary from those

key_names = ['id','name','flight']
dates = ['2011-10-01','2020-10-19','']

student_milestones = {}

keys = range(3)
date_index = 0

for key in key_names:
  #print(key)
  student_milestones[key] = dates[date_index]
  date_index = date_index + 1

print(student_milestones)
```

result:
```
PS D:\temp> python create_dicts.py
{'id': '2011-10-01', 'name': '2020-10-19', 'flight': ''}
"""
```