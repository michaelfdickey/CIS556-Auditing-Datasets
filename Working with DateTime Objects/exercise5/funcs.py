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
    print(" timestamp is: ", timestamp, "tz is: ", tz)

    # try to convert with parse function
    try:
        dt_timestamp = parse(timestamp)
        print(" dt_timestamp is: ", dt_timestamp)
    except:
        ## if invalid return none
        return None

    # check if it has a timezone (even if empty)
    if dt_timestamp.tzinfo != None:
        print("  dt_timestamp has a tz and is a valid datetime object, returning dt_timestamp")
        return dt_timestamp

    if dt_timestamp.tzinfo == None:
        print("  dt_timestamp tzinfo is None, adding tz")

        ## if no timezone and tz = none, return datetime
        if tz == None:
            print("   tz argument was blank: ", tz, "returning datetime as is")
            print("   dt_timestamp is: ", dt_timestamp)
            return dt_timestamp

        ## if no timezone and tz!=None give datetime tz
        if tz != None:
            if isinstance(tz, str) == False:    #ignore if tz isn't empty but also isn't a string
                print("   no timezone in timestamp, tz not empty, adding tz to datetime object")
                print("    dt_timestamp is: ", dt_timestamp)
                print("    tz is: ", tz)
                print("    type(tz) is: ", type(tz))

                dt_timestamp_new = dt_timestamp.replace(tzinfo=tz)

                return dt_timestamp_new

        ## if tz is string convert and localize it
        if isinstance(tz, str) == True:
            print("    tz is: ", repr(tz))
            print("    tz is a string, converting with pytz")
            tza = pytz.timezone(tz)
            print("    tz is now: ", repr(tza))
            print("    type(tza) is: ", type(tza))

            print("     str(dt_timestamp) is: ", repr(str(dt_timestamp)))
            dt_timestamp_new = dt_timestamp.replace(tzinfo=tza)
            print("     str(dt_timestamp_new) is: ", repr(str(dt_timestamp_new)))

            dt_timestamp_localized = tza.localize(dt_timestamp)

            #tzb = tza.localize()     
            #dt_timestamp_localized = tz.localize(dt_timestamp_new)

            print("      dt_timestamp_localized is: ", dt_timestamp_localized)

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
    pass                    # Implement this function

