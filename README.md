# CIS556-Auditing-Datasets

## reading json files
```
import json
file_opened = open(filename) 			# open file
text_to_import = file_opened.read()		# read file contents
json_text = json.loads(text_to_import)	# convert file to readable format
file_opened.close()						    # close file
return json_text						# return contents
```