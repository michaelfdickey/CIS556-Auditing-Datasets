
from dateutil.parser import parse
from pytz import timezone
import datetime

input   = '2016-05-12T16:23'
correct = parse(input+'-4:00')
tz = correct.tzinfo
#result  = funcs.str_to_time(input,correct.tzinfo)
print("tz is: ", tz)


g = cert.replace(tzinfo=event.tzinfo)
# g is new date-time object
# cert is the date with out timezone info
# event is the date with timezone


>>> cert
datetime.datetime(2019, 7, 10, 0, 0)
>>> event
datetime.datetime(2019, 9, 25, 13, 45, 15, tzinfo=tzoffset(None, -14400))
>>> g
datetime.datetime(2019, 7, 10, 0, 0, tzinfo=tzoffset(None, -14400))
>>>




>>> correct.tzinfo
tzoffset(None, -14400)
>>> timestamp
"2016-05-12T16:23"
>>> dt_timestamp
"2016-05-12 16:23:00"



dt_timestamp_new = dt_timestamp.replace(tzinfo=event.tzinfo)