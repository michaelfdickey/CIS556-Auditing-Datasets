#new offset


import os.path
import datetime
from dateutil.parser import parse
import dateutil

takeoff_txt = '2017-03-12 02:00:00-05:00'
takeoff_dt = parse(takeoff_txt)
print("takeoff_dt:", takeoff_dt)
print(str(takeoff_dt))

takeoff_year = takeoff_txt[0:4]
takeoff_month = takeoff_txt[5:7]
takeoff_day = takeoff_txt[8:10]
takeoff_hour = takeoff_txt[11:13]
takeoff_offset = takeoff_txt[20:22]

print("takeoff_year: ", takeoff_year)
print("takeoff_month: ", takeoff_month)
print("takeoff_day: ", takeoff_day)
print("takeoff_hour: ", takeoff_hour)
print("takeoff_offset: ", takeoff_offset)

# remove hour from offset
print(type(takeoff_offset))
takeoff_offset = int(takeoff_offset) - 1
print(" takeoff_offset is: ", takeoff_offset)
if len(str(takeoff_offset)) < 2:
	takeoff_offset = "0" + str(takeoff_offset)
else:
	takeoff_offset = str(takeoff_offset)
print(" takeoff_offset is: ", takeoff_offset)


# add hour to hours
print("takeoff_hour is: ", takeoff_hour)
takeoff_hour = int(takeoff_hour) + 1
if len(str(takeoff_hour)) < 2:
	takeoff_hour = "0" + str(takeoff_hour)
else:
	takeoff_hour = str(takeoff_hour)


# create new time
takeoff_thistz_text = takeoff_year + "-" + takeoff_month + "-" + takeoff_day + " " + takeoff_hour + ":00:00" + "-" + takeoff_offset + ":00"
print("takeoff_thistz_txt is: ", takeoff_thistz_text)
takeoff_thistz_dt = parse(takeoff_thistz_text)
print(takeoff_thistz_dt)
print(" takeoff original is: ", str(takeoff_dt))
print(" takeoff this tz is: ", str(takeoff_thistz_dt))
if takeoff_thistz_dt == takeoff_dt:
	print(" these two datetimes match")


"""
#https://stackoverflow.com/questions/68764819/converting-other-time-zones-into-local-time-zone-offset

print(str(takeoff_dt))

offsethours = -4
new_takeoff_dt = datetime(takeoff_dt).replace(tzinfo=timezone(timedelta(hours=offsethours)))

print(str(new_takeoff_dt))
"""

"""
>> Running get_weather_report <<
 takeoff is:  2017-03-12 03:00:00-05:00
  type(takeoff) is:  <class 'datetime.datetime'>
  takeoff_iso is:  2017-03-12T03:00:00-05:00
  previous_hour_takeoff_txt is:  2017-3-12 3:00:00
  previous_hour_takeoff is:  2017-03-12 03:00:00
  type(previous_hour_takeoff_naive) is:  <class 'datetime.datetime'>
   previous_hour_takeoff is:  2017-03-12 03:00:00-05:00
   previous_hour_takeoff_iso is:  2017-03-12T03:00:00-05:00
Traceback (most recent call last):
"""

test case 1
takeoff 	"2017-10-12 11:30:00-04:00"
correct 	"2017-10-12T11:00:00-04:00"  #round down to nearest hour
incorrect 	"2017-10-12T10:00:00-04:00"  # go backwards a full hour


test case 6
takeoff 	"2017-03-12T03:00:00-05:00"
correct     "2017-03-12T02:00:00-05:00"
			"2017-03-12T03:00:00-05:00"
incorrect 	"2017-03-12T04:00:00-04:00"


test case 8
takeoff 	"2017-12-27 23:00:00-05:00"