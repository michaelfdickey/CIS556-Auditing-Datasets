
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

"""
PS D:\temp> python create_dicts.py
{'id': '2011-10-01', 'name': '2020-10-19', 'flight': ''}
"""

