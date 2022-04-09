"""
Module to check violations for a flight lesson.

This module processes the primary violations, which are violations of weather restrictions. 
Weather restrictions express the minimum conditions that a pilot is allowed to fly in.  
So if a pilot has a ceiling minimum of 2000 feet, and there is cloud cover at 1500 feet, 
the pilot should not fly.To understand weather minimums, you have to integrate three 
different files: daycycle.json (for sunrise and sunset), weather.json (for hourly weather 
observations at the airport), and minimums.csv (for the schools minimums set by agreement 
with the insurance agency). You should look at those files BRIEFLY to familiarize yourself 
with them.

This module can get overwhelming if you panic and think too much about the big picture.  
Like a good software developer, you should focus on the specifications and do a little
at a time.  While these functions may seem like they require a lot of FAA knowledge, all
of the information you need is in the specifications. They are complex specifications,
but all of the information you need is there.  Combined with the provided unit tests
in tests.py, this assignment is very doable.

It may seem weird that these functions only check weather conditions at the time of 
takeoff and not the entire time the flight is in the air.  This is standard procedure 
for this insurance company.  The school is only liable if they let a pilot take off in 
the wrong conditions.  If the pilot stays up in adverse conditions, responsibility shifts 
to the pilot.

The preconditions for many of these functions are quite messy.  While this makes writing 
the functions simpler (because the preconditions ensure we have less to worry about), 
enforcing these preconditions can be quite hard. That is why it is not necessary to 
enforce any of the preconditions in this module.

Author: Michael Dickey
Date: Apr 3 2022
"""
import utils
import pilots
import os.path
import datetime
from dateutil.parser import parse
import dateutil
import csv
import json 


# WEATHER FUNCTIONS
def bad_visibility(visibility,minimum):
    """
    Returns True if the visibility measurement violates the minimum, False otherwise
    
    A valid visibility measurement is EITHER the string 'unavailable', or a dictionary 
    with (up to) four values: 'minimum', 'maximum',  'prevailing', and 'units'. Only 
    'prevailing' and 'units' are required; the other two are optional. The units may be 
    'FT' (feet) or 'SM' for (statute) miles, and explain how to interpret other three 
    fields, which are all floats.
    
    This function should compare ths visibility 'minimum' (if it exists) against the 
    minimum parameter. Else it compares the 'prevailing' visibility. This function returns
    True if minimum is more than the measurement. If the visibility is 'unavailable', 
    then this function returns True (indicating bad record keeping).
    
    Example: Suppose we have the following visibility measurement.
        
        {
            "prevailing": 21120.0,
            "minimum": 1400.0,
            "maximum": 21120.0,
            "units": "FT"
        }
    
    Given the above measurement, this function returns True if visibility is 0.25 (miles)
    and False if it is 1.
    
    Parameter visibility: The visibility information
    Precondition: visibility is a valid visibility measurement, as described above.
    (e.g. either a dictionary or the string 'unavailable')
    
    Parameter minimum: The minimum allowed visibility (in statute miles)
    Precondition: minimum is a float or int
    """

    # verify inputs
    ###print(" ")
    ###print(" RUNNING bad_visibility")
    ###print(" visibility is:", visibility, "type(visibility) is: ", type(visibility))
    ###print(" minimum is: ", minimum, "type(minimum) is: ", type(minimum))

    # set initial vars
    minimum_present = False


    if visibility == 'unavailable':
        ###print("  visibility is unavailalbe, returning True")
        return True 

    # get prevailing
    prevailing = visibility['prevailing']
    ###print("  prevailing is: ", prevailing)

    # get minimum if provided
    try:
        minimum_observed = visibility['minimum']
        minimum_present = True
        ###print(" minimum_observed is: ", minimum_observed)
    except:
        pass 
    
    # get units
    units = visibility['units']
    ###print("  units are: ", units)

    if units == 'FT':
        ###print(" units are in feet, converting to SM")
        prevailing = prevailing/5280
        ###print("   prevailing is now:", prevailing, "SM")
    

    """
    This function should compare ths visibility 'minimum' (if it exists) against the 
    minimum parameter. Else it compares the 'prevailing' visibilit
    """

    if minimum_present == True:
        ###print("  minimum observation present, comparing min req with min obs")
        if units == 'FT':
            minimum_observed = minimum_observed/5280
            ###print("   minimum_observed is: ", minimum_observed)

    units = 'SM'

    if units == 'SM':
        ###print(" units are SM, processing")
        
        if minimum_present == True:
            if minimum_observed < minimum:
                ###print("   minimum_observed is less than minimum, bad visibility, returning True")
                return True
            if minimum_observed == minimum:
                ###print("   minimum_observed equal to minimum_present, ok")
                return False
            if minimum_observed > minimum:
                ###print("   minimum_observed > minimum, good viz")
                return False


        if prevailing < minimum:
            #print("   prevailing is less than minimum, bad visibility, returning True")
            return True

        if prevailing == minimum:
            #print("   prevailing equals minimum")
            return False

        if prevailing > minimum:
            #print("   prevailing viz greater than minimum, good visibility")
            return False





def bad_winds(winds,maxwind,maxcross):
    """
    Returns True if the wind measurement violates the maximums, False otherwise
    
    A valid wind measurement is EITHER the string 'calm', the string 'unavailable' or 
    a dictionary with (up to) four values: 'speed', 'crosswind', 'gusts', and 'units'. 
    Only 'speed' and 'units' are required if it is a dictionary; the other two are 
    optional. The units are either be 'KT' (knots) or 'MPS' (meters per second), and 
    explain how to interpret other three fields, which are all floats.
    
    This function should compare 'speed' or 'gusts' against the maxwind parameter
    (whichever is worse) and 'crosswind' against the maxcross. If either measurement is greater
    than the allowed maximum, this function returns True.
    
    If the winds are 'calm', then this function always returns False. If the winds are
    'unavailable', then this function returns True (indicating bad record keeping).
    
    For conversion information, 1 MPS is roughly 1.94384 knots.
    
    Example: Suppose we have the following wind measurement.
        
        {
            "speed": 12.0,
            "crosswind": 10.0,
            "gusts": 18.0,
            "units": "KT"
        }
    
    Given the above measurement, this function returns True if maxwind is 15 or maxcross is 5.
    If both maxwind is 20 and maxcross is 10, it returns False.  (If 'units' were 'MPS'
    it would be false in both cases).
    
    Parameter winds: The wind speed information
    Precondition: winds is a valid wind measurement, as described above.
    (e.g. either a dictionary, the string 'calm', or the string 'unavailable')
    
    Parameter maxwind: The maximum allowable wind speed (in knots)
    Precondition: maxwind is a float or int
    
    Parameter maxcross: The maximum allowable crosswind speed (in knots)
    Precondition: maxcross is a float or int
    """

    ##print(" ")
    ##print("  >> checking bad_winds << ")

    # verify input
    ##print(" winds is: ", winds)
    ##print(" maxwind is: ", maxwind)
    ##print(" maxcross is: ", maxcross)

    # check initial violations
    if winds == 'calm':
        ##print("  wind is calm, returning False for bad_winds")
        return False

    if winds == 'unavailable':
        ##print("  wind speed unavailable, returning True")
        return True

    winds_speed = 0
    winds_crosswind = 0 
    winds_gusts = 0 
    winds_units = ''

    # get local vars  
    try: 
        winds_speed = winds['speed']
    except:
        pass
    try:
        winds_crosswind = winds['crosswind']
    except:
        pass
    try:
        winds_gusts = winds['gusts']
    except:
        pass
    try:
        winds_units = winds['units']
    except:
        pass

    # set locals
    knots = 1.94384

    # if MPS convert all to KTs
    if winds_units == 'MPS':
        ##print("  winds['units'] = MPS converting to KTs")
        winds_speed = winds_speed * knots
        winds_crosswind = winds_crosswind * knots
        winds_gusts = winds_gusts * knots 
        winds_units = 'KT'

    ##print(" winds_speed:", winds_speed, "winds_gusts:", winds_gusts,"winds_crosswind:", winds_crosswind)

    if winds_gusts > maxwind:
        #print("  wind gusts too high", winds['gusts'], "returning True")
        return True

    if winds_speed > maxwind:
        #print("  wind speed too high", winds['speed'], "returning True")
        return True 

    if winds_crosswind > maxcross:
        #print("  wind_crosswind too high:", winds_crosswind, "returning True")
        return True 

    #print( "   wind speeds are ok, returning False")
    return False

def bad_ceiling(ceiling,minimum):
    """
    Returns True if the ceiling measurement violates the minimum, False otherwise
    
    A valid ceiling measurement is EITHER the string 'clear', the string 'unavailable', 
    or a list of cloud layer measurements. A cloud layer measurement is a dictionary with 
    three required keys: 'type', 'height', and 'units'.  Type is one of 'a few', 
    'scattered', 'broken', 'overcast', or 'indefinite ceiling'. The value 'units' must 
    be 'FT', and specifies the units for the float associated with 'height'.
    
    If the ceiling is 'clear', then this function always returns False. If the ceiling 
    is 'unavailable', then this function returns True (indicating bad record keeping).
    Otherwise, it compares the minimum allowed ceiling against the lowest cloud layer 
    that is either 'broken', 'overcast', or 'indefinite ceiling'.
    
    Example: Suppose we have the following ceiling measurement.
        
        [
            {
                "cover": "clouds",
                "type": "scattered",
                "height": 700.0,
                "units": "FT"
            },
            {
                "type": "overcast",
                "height": 1200.0,
                "units": "FT"
            }
        ]
    
    Given the above measurement, this function returns True if minimum is 2000,
    but False if it is 1000.
    
    Parameter ceiling: The ceiling information
    Precondition: ceiling is a valid ceiling measurement, as described above.
    (e.g. either a dictionary, the string 'clear', or the string 'unavailable')
        
    Parameter minimum: The minimum allowed ceiling (in feet)
    Precondition: minimum is a float or int
    """


    #print(" >> running bad_ceiling <<")

    # verify inputs
    #print(" ceiling is:", ceiling)
    #print(" minimum is:", minimum)
    #print(" type(ceiling) is: ", type(ceiling))

    # initial conditions assessments
    if ceiling == 'clear':
        #print("  ceiling is clear, returning false on bad_ceiling")
        return False

    if ceiling == 'unavailable':
        #print("  ceiling is unavailable")
        return True 

    ceiling_dict = ceiling[0]
    #print(" ceiling_dict is: ", ceiling_dict)

    # get all heights from all list entries
    heights = []
    entries = len(ceiling)
    #print(" num of ceiling entries is: ", entries)
    for entries_index in range(len(ceiling)):
        #print("  ", ceiling[entries_index])
        # don't include clouds types of 'a few' and 'scattered'
        if ceiling[entries_index]['type'] != 'a few':
            if ceiling[entries_index]['type'] != 'scattered':
                heights.append(ceiling[entries_index]['height'])

    #print("   heights is: ", heights)
  
    try:
        if min(heights) < minimum:
            #print("   min cloud height is less than ", minimum, "returning True for bad_ceiling")
            return True 

        if min(heights) >= minimum:
            #print("   min cloud height is greater than ", minimum,"returning false for bad_ceiling")
            return False 
    except:
        return False     

def get_weather_report(takeoff,weather):
    """
    Returns the most recent weather report at or before take-off.
    
    The weather is a dictionary whose keys are ISO formatted timestamps and whose values 
    are weather reports.  For example, here is an example of a (small portion of) a
    weather dictionary:
        
        {
            "2017-04-21T08:00:00-04:00": {
                "visibility": {
                "prevailing": 10.0,
                "units": "SM"
            },
            "wind": {
                "speed": 13.0,
                "crosswind": 2.0,
                "units": "KT"
            },
            "temperature": {
                "value": 13.9,
                "units": "C"
            },
            "sky": [
                {
                    "cover": "clouds",
                    "type": "broken",
                    "height": 700.0,
                    "units": "FT"
                }
            ],
            "code": "201704211056Z"
        },
        "2017-04-21T07:00:00-04:00": {
            "visibility": {
                "prevailing": 10.0,
                "units": "SM"
            },
            "wind": {
                "speed": 13.0,
                "crosswind": 2.0,
                "units": "KT"
            },
            "temperature": {
                "value": 13.9,
                "units": "C"
            },
            "sky": [
                {
                    "type": "overcast",
                    "height": 700.0,
                    "units": "FT"
                }
            ],
            "code": "201704210956Z"
        }
        ...
    },
    
    If there is a report whose timestamp matches the ISO representation of takeoff, 
    this function uses that report.  Otherwise it searches the dictionary for the most
    recent report before takeoff.  If there is no such report, it returns None.
    
    Example: If takeoff was as 8 am on April 21, 2017 (Eastern), this function returns 
    the value for key '2017-04-21T08:00:00-04:00'.  If there is no additional report at
    9 am, a 9 am takeoff would use this value as well.
    
    Parameter takeoff: The takeoff time
    Precondition: takeoff is a datetime object
    
    Paramater weather: The weather report dictionary 
    Precondition: weather is a dictionary formatted as described above
    """
    # HINT: Looping through the dictionary is VERY slow because it is so large
    # You should convert the takeoff time to an ISO string and search for that first.
    # Only loop through the dictionary as a back-up if that fails.
    
    # Search for time in dictionary
    # As fall back, find the closest time before takeoff

    #print(" ")
    #print(" >> Running get_weather_report <<")

    # verify inputs
    #print(" takeoff is: ", takeoff)
    #print(" weather is: ", weather)
    #print("  type(takeoff) is: ", type(takeoff))

    ## get ready for converting
    takeoff_dt = takeoff
    takeoff_txt = str(takeoff)
    #print("  takeoff_txt is: ", str(takeoff_txt))
    
    ## strip out values
    takeoff_year = takeoff_txt[0:4]
    takeoff_month = takeoff_txt[5:7]
    takeoff_day = takeoff_txt[8:10]
    takeoff_hour = takeoff_txt[11:13]
    takeoff_offset = takeoff_txt[20:22]

    #print("   takeoff_year: ", takeoff_year)
    #print("   takeoff_month: ", takeoff_month)
    #print("   takeoff_day: ", takeoff_day)
    #print("   takeoff_hour: ", takeoff_hour)
    #print("   takeoff_offset: ", takeoff_offset)


    # convert to iso format
    takeoff_iso = takeoff.isoformat()

    #print("  takeoff_iso is: ", takeoff_iso)

    # get dictionary entry for that hour
    try:
        takeoff_hour_dictionary = weather[takeoff_iso]
        #print(takeoff_hour_dictionary)
        # get weather code
        code = takeoff_hour_dictionary['code']
        #print("  code is: ", code)
        return takeoff_hour_dictionary
    except:
        pass 

    # ROUND DOWN to nearest hour
    # 2017-10-12T11:30:00-04:00
    previous_hour_takeoff_txt = str(takeoff.year) + "-" + str(takeoff.month) + "-" + str(takeoff.day) + " " + str(takeoff.hour) + ':00:00'
    #print("  previous_hour_takeoff_txt is: ", previous_hour_takeoff_txt)
    previous_hour_takeoff_naive = parse(previous_hour_takeoff_txt)
    #print("  previous_hour_takeoff is: ", str(previous_hour_takeoff_naive))
    #print("  type(previous_hour_takeoff_naive) is: ", type(previous_hour_takeoff_naive))
    #tz = dateutil.tz.tz.tzoffset(None, -14400)      # manually create offset and add it
    tz = takeoff.tzinfo                             # grab offset from original takeoff datetime object
    previous_hour_takeoff = previous_hour_takeoff_naive.replace(tzinfo=tz)
    #print("   previous_hour_takeoff is: ", previous_hour_takeoff)
    previous_hour_takeoff_iso = previous_hour_takeoff.isoformat()
    #print("   previous_hour_takeoff_iso is: ", previous_hour_takeoff_iso)


    # get dictionary entry for previous hour
    try:
        takeoff_hour_dictionary = weather[previous_hour_takeoff_iso]
        #print(takeoff_hour_dictionary)
        # get weather code
        code = takeoff_hour_dictionary['code']
        #print("  code is: ", code)
        return takeoff_hour_dictionary
    except:
        pass 



    # ROUND DOWN AND GO BACKWARDS one hour. 

    ## subtract 1 hour from hours
    #print("takeoff_hour is: ", takeoff_hour)
    takeoff_hour = int(takeoff_hour) - 1
    if len(str(takeoff_hour)) < 2:
        takeoff_hour = "0" + str(takeoff_hour)
    else:
        takeoff_hour = str(takeoff_hour)
 
    previous_hour_takeoff_txt = str(takeoff.year) + "-" + str(takeoff.month) + "-" + str(takeoff.day) + " " + str(takeoff_hour) + ':00:00'   #note takeof_hour not takeoff.hour
    #print("  previous_hour_takeoff_txt is: ", previous_hour_takeoff_txt)
    previous_hour_takeoff_naive = parse(previous_hour_takeoff_txt)
    #print("  previous_hour_takeoff is: ", str(previous_hour_takeoff_naive))
    #print("  type(previous_hour_takeoff_naive) is: ", type(previous_hour_takeoff_naive))
    #tz = dateutil.tz.tz.tzoffset(None, -14400)      # manually create offset and add it
    tz = takeoff.tzinfo                             # grab offset from original takeoff datetime object
    previous_hour_takeoff = previous_hour_takeoff_naive.replace(tzinfo=tz)
    #print("   previous_hour_takeoff is: ", previous_hour_takeoff)
    previous_hour_takeoff_iso = previous_hour_takeoff.isoformat()
    #print("   previous_hour_takeoff_iso is: ", previous_hour_takeoff_iso)

    try:
        takeoff_hour_dictionary = weather[previous_hour_takeoff_iso]
        #print(takeoff_hour_dictionary)
        # get weather code
        code = takeoff_hour_dictionary['code']
        #print("  code is: ", code)
        return takeoff_hour_dictionary
    except:
        pass 

   
    # convert to different timezone and try again    


    ## remove hour from offset
    #print(type(takeoff_offset))
    takeoff_offset = int(takeoff_offset) - 1
    #print(" takeoff_offset is: ", takeoff_offset)
    if len(str(takeoff_offset)) < 2:
        takeoff_offset = "0" + str(takeoff_offset)
    else:
        takeoff_offset = str(takeoff_offset)
    #print(" takeoff_offset is: ", takeoff_offset)

    ## add hour to hours
    #print("takeoff_hour is: ", takeoff_hour)
    takeoff_hour = int(takeoff_hour) + 1
    if len(str(takeoff_hour)) < 2:
        takeoff_hour = "0" + str(takeoff_hour)
    else:
        takeoff_hour = str(takeoff_hour)

    # create new time
    takeoff_thistz_text = takeoff_year + "-" + takeoff_month + "-" + takeoff_day + " " + takeoff_hour + ":00:00" + "-" + takeoff_offset + ":00"
    #print("takeoff_thistz_txt is: ", takeoff_thistz_text)
    takeoff_thistz_dt = parse(takeoff_thistz_text)
    #print(takeoff_thistz_dt)
    #print(" takeoff original is: ", str(takeoff_dt))
    #print(" takeoff this tz is: ", str(takeoff_thistz_dt))
    #if takeoff_thistz_dt == takeoff_dt:
        #print(" these two datetimes match")
    takeoff_thistz_iso = takeoff_thistz_dt.isoformat()
    #print(" takeoff_thistz_iso is: ", takeoff_thistz_iso)

    # try dictionary entry for new timezone adjusted dt
    try:
        takeoff_hour_dictionary = weather[takeoff_thistz_iso]
        #print(takeoff_hour_dictionary)
        # get weather code
        code = takeoff_hour_dictionary['code']
        #print("  code is: ", code)
        return takeoff_hour_dictionary
    except:
        pass 

    #return takeoff_hour_dictionary


def get_weather_violation(weather,minimums):
    """
    Returns a string representing the type of weather violation (empty string if flight is ok)
    
    The weather reading is a dictionary with the keys: 'visibility', 'wind', and 'sky'.
    These correspond to a visibility, wind, and ceiling measurement, respectively. It
    may have other keys as well, but these can be ignored. For example, this is a possible 
    weather value:
        
        {
            "visibility": {
                "prevailing": 21120.0,
                "minimum": 1400.0,
                "maximum": 21120.0,
                "units": "FT"
            },
            "wind": {
                "speed": 12.0,
                "crosswind": 3.0,
                "gusts": 18.0,
                "units": "KT"
            },
            "temperature": {
                "value": -15.6,
                "units": "C"
            },
            "sky": [
                {
                    "cover": "clouds",
                    "type": "broken",
                    "height": 2100.0,
                    "units": "FT"
                }
            ],
            "weather": [
                "light snow"
            ]
        }
    
    The minimums is a list of the four minimums ceiling, visibility, and max windspeed,
    and max crosswind speed in that order.  Ceiling is in feet, visibility is in statute
    miles, max wind and cross wind speed are both in knots. For example, 
    [3000.0,10.0,20.0,8.0] is a potential minimums list.
    
    This function uses bad_visibility, bad_winds, and bad_ceiling as helpers. It returns
    'Visibility' if the only problem is bad visibility, 'Wind' if the only problem is 
    wind, and 'Ceiling' if the only problem is the ceiling.  If there are multiple
    problems, it returns 'Weather', It returns 'Unknown' if no weather reading is 
    available (e.g. weather is None).  Finally, it returns '' (the empty string) if 
    the weather is fine and there are no violations.
    
    Parameter weather: The weather measure
    Precondition: weather is dictionary containing a visibility, wind, and ceiling measurement,
    or None if no weather reading is available.
    
    Parameter minimums: The safety minimums for ceiling, visibility, wind, and crosswind
    Precondition: minimums is a list of four floats
    """

    # verify inputs
    #print(" weather is: ", weather)
    #print(" minimums is: ", minimums)
    minimum_ceiling = minimums[0]
    minimum_visibility = minimums[1]
    max_windspeed = minimums[2]
    max_crosswind = minimums[3]
    #print(" minimum_ceiling is:    ", minimum_ceiling)
    #print(" minimum_visibility is: ", minimum_visibility)
    #print(" max_windspeed is:      ", max_windspeed)
    #print(" max_crosswind is:      ", max_crosswind)

    # accumulators
    number_of_violations = 0

    # check initial determinents
    if weather == None:
        result = 'Unknown'
        return result


    # check visibility
    """
    def bad_visibility(visibility,minimum): 
    Returns True if the visibility measurement violates the minimum, False otherwise
        Example: Suppose we have the following visibility measurement.
        
        {
            "prevailing": 21120.0,
            "minimum": 1400.0,
            "maximum": 21120.0,
            "units": "FT"
        }
    
    """

    weather_observations = weather['visibility']
    #print(" weather_observations is: ", weather_observations)
    #print(" type(weather_observations) is: ", type(weather_observations))
    visibility_is_bad = bad_visibility(weather_observations,minimum_visibility)

    if visibility_is_bad == True:
        #print(" visibility violation")
        number_of_violations = number_of_violations + 1


    # check for bad winds
    #def bad_winds(winds,maxwind,maxcross):
    """
    Returns True if the wind measurement violates the maximums, False otherwise
    A valid wind measurement is EITHER the string 'calm', the string 'unavailable' or 
    a dictionary with (up to) four values: 'speed', 'crosswind', 'gusts', and 'units'. 
            Example: Suppose we have the following wind measurement.
        
        {
            "speed": 12.0,
            "crosswind": 10.0,
            "gusts": 18.0,
            "units": "KT"
        }
    
    Parameter winds: The wind speed information
    Precondition: winds is a valid wind measurement, as described above.
    (e.g. either a dictionary, the string 'calm', or the string 'unavailable')
    
    Parameter maxwind: The maximum allowable wind speed (in knots)
    Precondition: maxwind is a float or int
    
    Parameter maxcross: The maximum allowable crosswind speed (in knots)
    Precondition: maxcross is a float or int
    """

    wind_observations = weather['wind']
    #print(" wind_observations is: ", wind_observations)
    #print(" type(wind_observations) is: ", type(wind_observations))
    
    winds_are_bad = bad_winds(wind_observations,float(max_windspeed),float(max_crosswind))

    if winds_are_bad == True:
        #print(" wind violation")
        number_of_violations = number_of_violations + 1


    # check for bad cieling:
    #def bad_ceiling(ceiling,minimum):
    """
    Returns True if the ceiling measurement violates the minimum, False otherwise
    Example: Suppose we have the following ceiling measurement.
        
        [
            {
                "cover": "clouds",
                "type": "scattered",
                "height": 700.0,
                "units": "FT"
            },
            {
                "type": "overcast",
                "height": 1200.0,
                "units": "FT"
            }
        ]
    
    Given the above measurement, this function returns True if minimum is 2000,
    but False if it is 1000.
    
    Parameter ceiling: The ceiling information
    Precondition: ceiling is a valid ceiling measurement, as described above.
    (e.g. either a dictionary, the string 'clear', or the string 'unavailable')
        
    Parameter minimum: The minimum allowed ceiling (in feet)
    Precondition: minimum is a float or int
    """

    ceiling_observations = weather['sky']
    #print(" ceiling_observations is: ", ceiling_observations)
    ceiling_is_bad = bad_ceiling(ceiling_observations,minimum_ceiling)

    if ceiling_is_bad == True:
        #print(" ceiling violation")
        number_of_violations = number_of_violations + 1



    """
    This function uses bad_visibility, bad_winds, and bad_ceiling as helpers. It returns
    'Visibility' if the only problem is bad visibility, 'Wind' if the only problem is 
    wind, and 'Ceiling' if the only problem is the ceiling.  If there are multiple
    problems, it returns 'Weather', It returns 'Unknown' if no weather reading is 
    available (e.g. weather is None).  Finally, it returns '' (the empty string) if 
    the weather is fine and there are no violations.
    """

    

    if visibility_is_bad == True:
        if winds_are_bad == False:
            if ceiling_is_bad == False:
                #print("   visibility is the only violation - returning 'Visibility")
                return 'Visibility'

    if winds_are_bad == True:
        if visibility_is_bad == False:
            if ceiling_is_bad == False:
                #print("   Wind is the only violation - returning 'Wind'")
                return 'Winds'

    if ceiling_is_bad == True:
        if visibility_is_bad == False:
            if winds_are_bad == False:
                #print("   ceiling is the only violation - returning 'Ceiling'")
                return 'Ceiling'

    if number_of_violations > 1:
        #print("   more than 1 violation - returning 'Weather'")
        return 'Weather'

    
    #print( " ")

    result = ''
    return result



# FILES TO AUDIT
# Sunrise and sunset
DAYCYCLE = 'daycycle.json'
# Hourly weather observations
WEATHER  = 'weather.json'
# The list of insurance-mandated minimums
MINIMUMS = 'minimums.csv'
# The list of all registered students in the flight school
STUDENTS = 'students.csv'
# The list of all take-offs (and landings)
LESSONS  = 'lessons.csv'


def list_weather_violations(directory):
    """
    Returns the (annotated) list of flight reservations that violate weather minimums.
    
    This function reads the data files in the given directory (the data files are all
    identified by the constants defined above in this module).  It loops through the
    list of flight lessons (in lessons.csv), identifying those takeoffs for which
    get_weather_violation() is not the empty string.
    
    This function returns a list that contains a copy of each violating lesson, together 
    with the violation appended to the lesson.
    
    Example: Suppose that the lessons
        
        S00687  548QR  I061  2017-01-08T14:00:00-05:00  2017-01-08T16:00:00-05:00  VFR  Pattern
        S00758  548QR  I072  2017-01-08T09:00:00-05:00  2017-01-08T11:00:00-05:00  VFR  Pattern
        S00971  426JQ  I072  2017-01-12T13:00:00-05:00  2017-01-12T15:00:00-05:00  VFR  Pattern
    
    violate for reasons of 'Winds', 'Visibility', and 'Ceiling', respectively (and are the
    only violations).  Then this function will return the 2d list
        
        [[S00687, 548QR, I061, 2017-01-08T14:00:00-05:00, 2017-01-08T16:00:00-05:00, VFR, Pattern, Winds],
         [S00758, 548QR, I072, 2017-01-08T09:00:00-05:00, 2017-01-08T11:00:00-05:00, VFR, Pattern, Visibility],
         [S00971, 426JQ, I072, 2017-01-12T13:00:00-05:00, 2017-01-12T15:00:00-05:00, VFR, Pattern, Ceiling]]
    
    REMEMBER: VFR flights are subject to minimums with VMC in the row while IFR flights 
    are subject to minimums with IMC in the row.  The examples above are all VFR flights.
    If we changed the second lesson to
    
        S00758, 548QR, I072, 2017-01-08T09:00:00-05:00, 2017-01-08T11:00:00-05:00, IFR, Pattern
    
    then it is possible it is no longer a visibility violation because it is subject to
    a different set of minimums.
    
    Parameter directory: The directory of files to audit
    Precondition: directory is the name of a directory containing the files 'daycycle.json',
    'weather.json', 'minimums.csv', 'students.csv', and 'lessons.csv'
    """

    #print(" directory is: ", directory)

    # Load in all of the files

    ## open daycycle.json
    path_daycycle_json = os.path.join(directory,'daycycle.json')
    file_daycycle_json = open(path_daycycle_json)
    text_daycycle_json = file_daycycle_json.read()
    file_daycycle_json_wrapped = json.loads(text_daycycle_json)
    #print("file_daycycle_json_wrapped", file_daycycle_json_wrapped)
    #print(" type(file_daycycle_json_wrapped) is: ", type(file_daycycle_json_wrapped))

    ## open weather.json
    path_weather_json = os.path.join(directory,'weather.json')
    file_weather_json = open(path_weather_json)
    text_weather_json = file_weather_json.read()
    file_weather_json_wrapped = json.loads(text_weather_json)
    #print("file_weather_json_wrapped is:", file_weather_json_wrapped)
    #print(" type(file_weather_json_wrapped) is: ", type(file_weather_json_wrapped))


    ## open students.csv
    path_students_csv = os.path.join(directory,'students.csv')
    file_students_csv = open(path_students_csv)
    file_students_csv_wrapped = csv.reader(file_students_csv)
    #for row in file_students_csv_wrapped:
    #    #print(row)

    ## open minimums.csv
    path_minimums_csv = os.path.join(directory,'minimums.csv')
    file_minimums_csv = open(path_minimums_csv)
    file_minimums_csv_wrapped = csv.reader(file_minimums_csv)
    #for row in file_minimums_csv_wrapped:
    #    #print(row)

    ## open lessons.csv
    path_lessons_csv = os.path.join(directory,'lessons.csv')
    file_lessons_csv = open(path_lessons_csv)
    file_lessons_csv_wrapped = csv.reader(file_lessons_csv)
    #print(" type(file_lessons_csv_wrapped) is: ", file_lessons_csv_wrapped)
    
    
    # CONVERT MINIMUM CSV INTO A TABLE
    #print("  > converting minimums csv to table < ")
    minimums_table = []
    row_index = 0
    for row in file_minimums_csv_wrapped:
        current_row_table = []
        #print(" row_index is: ", row_index, row)
        for column_index in range(len(row)):
            #print("  column_index is: ", column_index, "content: ", row[column_index])  
            current_row_table.append(row[column_index])
            #print("  current_row_table is: ", current_row_table)            
        row_index = row_index + 1
        minimums_table.append(current_row_table)
    #print(" len minimums_table is: ", len(minimums_table))



    # CONVERT STUDENTS CSV INTO A TABLE
    #print("  > converting students csv into table < ")
    students_table = []
    row_index = 0
    for row in file_students_csv_wrapped:
        current_row_table = []
        #print(" row_index is: ", row_index, row)
        for column_index in range(len(row)):
            #print("  column_index is: ", column_index, "content: ", row[column_index])  
            current_row_table.append(row[column_index])
            #print("  current_row_table is: ", current_row_table)
        row_index = row_index + 1
        students_table.append(current_row_table)
    #print(" len students_table is: ", len(students_table))

    

    # CONVERT LESSONS CSV INTO TABLE
    #print("  > converting lessons csv into table < ")
    violations_check_table = []
    row_index = 0
    ## checking lessons
    for row in file_lessons_csv_wrapped:
        current_row_table = []
        #print(" row_index is: ", row_index, row)
        for column_index in range(len(row)):
            #print("  column_index is: ", column_index, "content: ", row[column_index])                        
            current_row_table.append(row[column_index])
            #print("  current_row_table is: ", current_row_table)
        if row_index > 0:
            violations_check_table.append(current_row_table)
        row_index = row_index + 1
        
    #print(" len violations_check_table is: ", len(violations_check_table))

    """
    ## checking to make sure table is constructed properly
    #print(" violations_check_table: ", violations_check_table)
    #print(violations_check_table[0])
    #print(violations_check_table[10])
    #print(violations_check_table[100])
    #print(violations_check_table[1000])
    """

    """
    ## testing appending a row:
    violations_check_table[0].append('test append')
    #print(violations_check_table[0])
    """

    # For each of the lessons
    # Get the takeoff time
    # Get the pilot credentials
    # Get the pilot minimums
    # Get the weather conditions
    # Check for a violation and add to result if so

    # open up each row, 


    # ANALYZE LESSONS TABLE AND PRODUCE VIOLATIONS
    #print(" ")
    violations_count = 0
    row_index = 0
    column_index = 0
    lessons_length = len(violations_check_table)
    lessons_width = len(violations_check_table[0])
    #print(" lessons_length is:", lessons_length, "lessons_width is: ", lessons_width)

    for row_index in range(lessons_length):    #uncomment when ready for full testing
    #for row_index in range(1):                 #just to make testing quicker
        #print(" ")
        #print("  row_index: ", row_index, violations_check_table[row_index])
        
        if row_index >= 0:
            # get values from lessons table for evaluating
            student_id = violations_check_table[row_index][0]
            instructor = violations_check_table[row_index][2]
            takeoff_time = violations_check_table[row_index][3]
            flight_filed = violations_check_table[row_index][5]
            flight_area = violations_check_table[row_index][6]

            #print("   student_id:  ", student_id)
            #print("   instructor:  ", instructor)
            #print("   takeoff_time:", takeoff_time)
            #print("   flight_filed:", flight_filed)
            #print("   flight_area: ", flight_area)

            #convert takeoff_time to datetime obj
            #print("  >> converting takeoff to datetime obj << ")
            takeoff_time_dt = parse(takeoff_time)
            #print("      takeoff_time_dt:", str(takeoff_time_dt))
            #print("   ", takeoff_time_dt, type(takeoff_time_dt))

            # Get the pilot credentials
            #print("  >> checking pilot credentials << ")
            ##get row from studens csv for student import it and get cert back. 
            ### search for student id in students.csv 
            #print("   student_id from lessons table is: ", student_id)
            student_history_row = []
            for student_table_index_row in range(len(students_table)):
                #print("    students_table[0] is ", repr(students_table[student_table_index_row][0]))
                if student_id == students_table[student_table_index_row][0]:
                    #print("      FOUND STUDENT ID MATCHES", student_id, students_table[student_table_index_row][0])
                    for column_index in range(len(students_table[0])):
                        student_history_row.append(students_table[student_table_index_row][column_index])
                    #print("       student_history_row is: ", student_history_row)

            ### check credentials with get_certification
            #print("      created student history row, checking pilot credentials ")
            certification = pilots.get_certification(takeoff_time_dt, student_history_row)
            #print("       certification is: ", certification)
            
            
            # Get the Pilot Minimums
            #print("  >> checking pilot minimums << ")
            
            ## get instrument rating 
            instrument_rating = pilots.has_instrument_rating(takeoff_time_dt, student_history_row)
            #print("   has instrument_rating : ", instrument_rating)

            ## get advanced endorsement status
            advanced_endorcement = pilots.has_advanced_endorsement(takeoff_time_dt, student_history_row)
            #print("   has advanced_endorcement : ", advanced_endorcement)

            ## set instructed to true or false 
            #print("   instructor is: ", instructor)
            if instructor == '':
                instructed = False
            if instructor != '':
                instructed = True

            ## set instrument rating:
            # if flight is filed as VFR then vfr for get minimums is true
            if flight_filed == 'VFR':
                flight_filed_as_vfr = True
            if flight_filed == 'IFR':
                flight_filed_as_vfr = False


            daytime = utils.daytime(takeoff_time_dt,file_daycycle_json_wrapped)  
            #print("   daytime is: ", daytime)          

            ## get minimums using cert, area, instructed, vfr, daytime, minimums_csv
            #print("  >>> verifying data for checking pilot minimums <<< ")
            #print("    certification is: ", certification)
            #print("    area is: ", flight_area)
            #print("    instructed is: ", instructed)
            #print("    instrument_rating is: ", instrument_rating, " *from def(has_instrment_rating)")
            #print("    flight_filed is: ", flight_filed)
            #print("    daytime is: ", daytime)
            #print("    minimum_table len is: ", len(minimums_table))

            pilot_minimums = pilots.get_minimums(certification, flight_area, instructed, flight_filed_as_vfr, daytime, minimums_table)
            #print("    ~ pilot_minimums are: ", pilot_minimums)
            # get pilot minimum values
            flight_ceiling_min =  pilot_minimums[0]
            flight_visibility_min =  pilot_minimums[1]
            flight_wind_max = pilot_minimums[2]
            flight_crosswind_max = pilot_minimums[3]
            #print("      ceiling is:    ", flight_ceiling_min)
            #print("      visibility is: ", flight_visibility_min)
            #print("      wind is:       ", flight_wind_max)
            #print("      crosswind is:  ", flight_crosswind_max)

            """
            #print("  >> convert time to iso << ")               #get_weather actual converts to iso
            takeoff_time_iso = takeoff_time_dt.isoformat()
            #print("   takeoff_time_iso is :", takeoff_time_iso)
            """

            # Get weather report
            #print("  >> getting weather report from get_weather_report <<")
            weather_at_flight = get_weather_report(takeoff_time_dt,file_weather_json_wrapped)
            #print("   weather_at_flight is: ", weather_at_flight)

            # get weather_report_visibility
            weather_report_visibility = weather_at_flight['visibility']
            #print("  weather_report_visibility is", weather_report_visibility)

            # get weather_report_winds
            weather_report_winds = weather_at_flight['wind']
            #print("  weather_report_winds is: ", weather_report_winds)

            # get weather_report_ceiling
            weather_report_ceiling = weather_at_flight['sky']
            #print("  weather_report_ceiling is: ", weather_report_ceiling)

            
            #Not necessary as get_weather_violations checks all these
            # CHECK visiblity
            visibility_bad = bad_visibility(weather_report_visibility,flight_visibility_min)
            #print("  _visibility_bad = ", visibility_bad)

            # CHECK winds
            winds_bad = bad_winds(weather_report_winds,flight_wind_max,flight_crosswind_max)
            #print("  _wind_bad =       ", winds_bad)
            
            # CHECK ceiling
            ceiling_bad = bad_ceiling(weather_report_ceiling,flight_ceiling_min)
            #print("  _ceiling_bad =    ", ceiling_bad)
            

            #print(" >> >>  checking VIOLATIONS << << ")
            
            violation = get_weather_violation(weather_at_flight,pilot_minimums)
            #print(" violation is: ", repr(violation))
            if violation != '':
                violations_count = violations_count + 1
                #print(" ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                #print(" ~~~~~~~~~~~~~~~~~~~~~~VIOLATION FOUND ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                #print(" ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

            """
            ## testing appending a row:
            violations_check_table[0].append('test append')
            #print(violations_check_table[0])

            flight_area = violations_check_table[row_index][6]
            """
            
            #print(" ")
            #print(" UPDATING VIOLATIONS RESULTS TABLE ")
            #print(" current row : ", violations_check_table[row_index])
            violations_check_table[row_index].append(violation)
            #print(" current row : ", violations_check_table[row_index])
            

    #print(" ")
    #print(" violations count: ", violations_count)
    #print(" ")

    #print(violations_check_table[0])
    #print(violations_check_table[1])

    violations_result_table = []

    #print("  >> CREATE RESULT TABLE  <<  ")
    violations_table_length = len(violations_check_table)
    violations_table_width = len(violations_check_table[0])
    #print(" violations_table_length is : ", violations_table_length)    
    #print(" violations_table_width is: ", violations_table_width)
    
    for row_index in range(violations_table_length):
        #print("  row is: ", violations_check_table[row_index])
        if violations_check_table[row_index][7] != '':
            #print("   appending row to violations_result_table")
            violations_result_table.append(violations_check_table[row_index])

    #for row in violations_result_table:
        #print(row)


    #print("   violations found: ", violations_count)

    return violations_result_table
