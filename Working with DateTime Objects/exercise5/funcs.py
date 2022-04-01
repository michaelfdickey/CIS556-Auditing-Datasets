"""
Functions for parsing time values and determining daylight hours.

Both of these functions will be used in the main project.  You should hold on to them.

Author: Michael Dickey
Date:   Mar 31 2022
"""

import datetime
import pytz
from dateutil.parser import parse


def str_to_time(timestamp,tz=None):
    """
    Returns the datetime object for the given timestamp (or None if stamp is invalid)
    
    This function should just use the parse function in dateutil.parser to
    convert the timestamp to a datetime object.  If it is not a valid date (so
    the parser crashes), this function should return None.
    
    If the timestamp has a timezone, then it should keep that timezone even if
    the value for tz is not None.  Otherwise, if timestamp has no timezone and 
    tz is not None, this this function will assign that timezone to the datetime 
    object. 
    
    The value for tz can either be a string or a time OFFSET. If it is a string, 
    it will be the name of a timezone, and it should localize the timestamp. If 
    it is an offset, that offset should be assigned to the datetime object.
    
    Parameter timestamp: The time stamp to convert
    Precondition: timestamp is a string
    
    Parameter tz: The timezone to use (OPTIONAL)
    Precondition: tz is either None, a string naming a valid time zone,
    or a time zone OFFSET.
    """
    # HINT: Use the code from the previous exercise and update the timezone
    # Use localize if timezone is a string; otherwise replace the timezone if not None

    # verify inputs
    #print(" timestamp is: ", timestamp, "tz is: ", tz)

    # try to convert with parse function
    try:
        dt_timestamp = parse(timestamp)
        #print(" dt_timestamp is: ", dt_timestamp)
    except:
        ## if invalid return none
        return None

    # check if it has a timezone (even if empty)
    if dt_timestamp.tzinfo != None:
        #print("  dt_timestamp has a tz and is a valid datetime object, returning dt_timestamp")
        return dt_timestamp

    if dt_timestamp.tzinfo == None:
        #print("  dt_timestamp tzinfo is None, adding tz")

        ## if no timezone and tz = none, return datetime
        if tz == None:
            #print("   tz argument was blank: ", tz, "returning datetime as is")
            #print("   dt_timestamp is: ", dt_timestamp)
            return dt_timestamp

        ## if no timezone and tz!=None give datetime tz
        if tz != None:
            if isinstance(tz, str) == False:    #ignore if tz isn't empty but also isn't a string
                #print("   no timezone in timestamp, tz not empty, adding tz to datetime object")
                #print("    dt_timestamp is: ", dt_timestamp)
                #print("    tz is: ", tz)
                #print("    type(tz) is: ", type(tz))

                dt_timestamp_new = dt_timestamp.replace(tzinfo=tz)

                return dt_timestamp_new

        ## if tz is string convert and localize it
        if isinstance(tz, str) == True:
            #print("    tz is: ", repr(tz))
            #print("    tz is a string, converting with pytz")
            tza = pytz.timezone(tz)
            #print("    tz is now: ", repr(tza))
            #print("    type(tza) is: ", type(tza))

            #print("     str(dt_timestamp) is: ", repr(str(dt_timestamp)))
            dt_timestamp_new = dt_timestamp.replace(tzinfo=tza)
            #print("     str(dt_timestamp_new) is: ", repr(str(dt_timestamp_new)))

            dt_timestamp_localized = tza.localize(dt_timestamp)

            #tzb = tza.localize()     
            #dt_timestamp_localized = tz.localize(dt_timestamp_new)

            #print("      dt_timestamp_localized is: ", dt_timestamp_localized)

            return dt_timestamp_localized
        
        

    # return result

def daytime(time,daycycle):
    """
    Returns true if the time takes place during the day.
    
    A time is during the day if it is after sunrise but before sunset, as
    indicated by the daycycle dicitionary.
    
    A daycycle dictionary has keys for several years (as int).  The value for
    each year is also a dictionary, taking strings of the form 'mm-dd'.  The
    value for that key is a THIRD dictionary, with two keys "sunrise" and
    "sunset".  The value for each of those two keys is a string in 24-hour
    time format.
    
    For example, here is what part of a daycycle dictionary might look like:
    
        "2015": {
            "01-01": {
                "sunrise": "07:35",
                "sunset":  "16:44"
            },
            "01-02": {
                "sunrise": "07:36",
                "sunset":  "16:45"
            },
            ...
        }
    
    In addition, the daycycle dictionary has a key 'timezone' that expresses the
    timezone as a string. This function uses that timezone when constructing
    datetime objects from this set.  If the time parameter does not have a timezone,
    we assume that it is in the same timezone as the daycycle dictionary
    
    Parameter time: The time to check
    Precondition: time is a datetime object
    
    Parameter daycycle: The daycycle dictionary
    Precondition: daycycle is a valid daycycle dictionary, as described above
    """
    # HINT: Use the code from the previous exercise to get sunset AND sunrise
    # Add a timezone to time if one is missing (the one from the daycycle)


    # verify inputs
    print(" time is: ", time)

    # convert time input to a valid datetime object
    print(" type(time) is: ", type(time))

    # get year
    year = time.year 
    print(" year is: ", year)   

    # get year dictionary
    year_dictionary = daycycle[str(year)]
    #print(" year_dictionary is: ", year_dictionary)

    # get mm-dd
    ## get month
    month = str(time.month)
    print(" month is: ", month)
    if len(month) < 2:
        month = "0" + month
        print("  month is now: ", month)
    
    ## get day
    day = str(time.day)
    print(" day is: ", day)
    if len(day) < 2:
        day = "0" + day 
        print("  day is now: ", day)

    mmdd = month + "-" + day
    print(" mmdd is: ", mmdd)
    
    # get mmdd dictionary
    month_dictionary = year_dictionary[mmdd]
    print(" month_dictionary is: ", month_dictionary)

    # get sumrise
    sunrise = month_dictionary['sunrise']
    print(" sunrise is: ", sunrise)
    
    ## create sunrise datetime.time object
    sunrise_hours = sunrise[0:2]
    if sunrise_hours[0] == '0':
        sunrise_hours = (sunrise_hours[1:2])
        print("   sunrise_hours is now: ", sunrise_hours)
    
    sunrise_minutes = sunrise[3:5]
    if sunrise_minutes[0] == '0':
        sunrise_minutes = (sunrise_minutes[1:])
        print("   sunrise_minutes is now: ", sunrise_minutes)

    print("   sunrise_hours is: ", sunrise_hours, "sunrise_minutes is: ", sunrise_minutes)

    sunrise = datetime.time(int(sunrise_hours),int(sunrise_minutes))
    print(" sunrise.time object is: ", sunrise)
    print(" type(sunrise) is: ", type(sunrise))

    

    # get sunset
    sunset = month_dictionary['sunset']
    print(" sunset is: ", sunset)

    ## create sunset datetime.time object
    sunset_hours = sunset[0:2]
    if sunset_hours[0] == '0':
        sunset_hours = (sunset_hours[1:2])
        print("   sunset_hours is now: ", sunset_hours)

    sunset_minutes = sunset[3:5]
    if sunset_minutes[0] == '0':
        sunset_minutes = (sunset_minutes[1:])
        print("   sunset_minutes is now: ", sunset_minutes)

    print("   sunset_hours is: ", sunset_hours, "sunset_minutes is: ", sunset_minutes)

    sunset = datetime.time(int(sunset_hours),int(sunset_minutes))
    print(" sunset.time object is: ", sunset)
    print(" type(sunset) is: ", type(sunset))


    # create now date-time object hour-min from time
    
    hour = time.hour
    print(" hour is: ", hour)
    minute = time.minute 
    print(" minute is: ", minute)
    now = datetime.time(hour,minute)
    print(" now is: ", now, "type(now) is: ", type(now))


    # check values
    print("   sunrise is: ", sunrise)
    print("   now is:     ", now)
    print("   sunset is:  ", sunset)

    # evaluate
    if now < sunrise:
        return False

    if now > sunrise:
        
        if now < sunset:
            print(" sunrise < now < sunset is true ")
            return True

        if now > sunset:
            return False
