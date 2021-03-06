"""
Functions for parsing time values from text.  

While these functions are similar to functions found in the assignment, they 
are missing timezone information.  The next exercise will modify these 
functions to make them compatible with the assignment.

Author: Michael Dickey
Date:   Mar 30 2022
"""

import datetime
from dateutil.parser import parse

def str_to_time(timestamp):
    """
    Returns the datetime object for the given timestamp (or None if the stamp is invalid)
    
    This function should just use the parse function in dateutil.parser to convert the
    timestamp to a datetime object.  If it is not a valid date (so the parser crashes), 
    this function should return None.
    
    Parameter timestamp: The time stamp to convert
    Precondition: timestamp is a string
    """
    # Hint: Use a try-except to return None if parsing fails

    # verify input data
    print(" timestamp is: ", timestamp)

    # try to convert it with parse, return if succseful, don't crash if not
    try:
        result = parse(timestamp)
        print(" ", result)
        return result
    except:
        pass




def sunset(date,daycycle):
    """
    Returns the sunset datetime (day and time) for the given date
    
    This function looks up the sunset from the given daycycle dictionary. If the
    daycycle dictionary is missing the necessary information, this function 
    returns the value None.
    
    A daycycle dictionary has keys for several years (as int).  The value for each year
    is also a dictionary, taking strings of the form 'mm-dd'.  The value for that key 
    is a THIRD dictionary, with two keys "sunrise" and "sunset".  The value for each of 
    those two keys is a string in 24-hour time format.
    
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
    
    Parameter date: The date to check
    Precondition: date is a date object
    
    Parameter daycycle: The daycycle dictionary
    Precondition: daycycle is a valid daycycle dictionary, as described above
    """
    # HINT: ISO FORMAT IS 'yyyy-mm-ddThh:mm'.  
    # For the sunrise value, construct a string in ISO format and call str_to_time.

    # verify inputs
    print(" date is: ", date)
    #print(" daycycle is: ", daycycle)
    print(" type(date) is: ", type(date))

    # convert to datetime.datetime
    if isinstance(date, datetime.datetime) == False:
        print("  this is not a datetime.datetime object, converting")
        date = datetime.datetime(date.year,date.month,date.day,0,0,0)
        print("  date is now: ", str(date), " and type(date): ", type(date))

    # looks up the sunset day and time for that date and returns it
    ## gets year and year dictionary
    print(" type(daycycle) is: ", type(daycycle))
    print(" date.year is: ", date.year)
    year = str(date.year)                           #year in dictionary is int
    
    try:
        year_dictionary = daycycle[year]                #gets the dictionary for the whole year
        #print("  year_dictionary is: ", year_dictionary)
    except:
        return None 

    ## process month and day to get mm-dd dict
    month = str(date.month)
    day = str(date.day)
    print("  month is: ", month, "day is: ", day)
    
    if len(month) < 2:
        print("   month is single digit, converting")
        month = "0" + month
        print("   month is now: ", month)

    if len(day) < 2:
        print("   day is single digit, converting")
        day = "0" + day
        print("   day is now: ", day)

    mmdd = month + "-" + day
    print("  mmdd is: ", repr(mmdd))

    day_dictionary = year_dictionary[mmdd]
    print("  day_dictionary is: ", day_dictionary)

    ## get sunset time and hours and minutes
    sunset_time = day_dictionary['sunset']
    print("  sunset_time is: ", sunset_time)

    hours = sunset_time[0:2]
    print("   hours is: ", hours)

    minutes = sunset_time[3:5]
    print("   minutes is: ", minutes)

    # build string in ISO FORMAT IS 'yyyy-mm-ddThh:mm'.  
    sunset_time_ISO = year + "-" + month + "-" + day + "T" + hours + ":" + minutes 
    print("   sunset_time_ISO is: ", sunset_time_ISO)

    # call str_to_time to convert
    result = str_to_time(sunset_time_ISO)
    print("    result is: ", result)

    # return result
    return result

    print( " ")

