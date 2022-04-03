"""
Module providing utility functions for this project.

These functions are general purpose utilities used by other modules in this project.
Some of these functions were exercises in early course modules and should be copied
over into this file.

The preconditions for many of these functions are quite messy.  While this makes writing 
the functions simpler (because the preconditions ensure we have less to worry about), 
enforcing these preconditions can be quite hard. That is why it is not necessary to 
enforce any of the preconditions in this module.

Author: Michael Dickey
Date: Apr 02 2022
"""
import csv
import json
import datetime
import pytz
from dateutil.parser import parse


def read_csv(filename):
    """
    Returns the contents read from the CSV file filename.
    
    This function reads the contents of the file filename and returns the contents as
    a 2-dimensional list. Each element of the list is a row, with the first row being
    the header. Cells in each row are all interpreted as strings; it is up to the 
    programmer to interpret this data, since CSV files contain no type information.
    
    Parameter filename: The file to read
    Precondition: filename is a string, referring to a file that exists, and that file 
    is a valid CSV file
    """
    
    #print(" running read_csv")

    # verify input
    #print(" filename is: ", filename)

    # create accumlator
    table_result = []

    # open csv file
    file = open(filename)

    # put in csv wrapper
    wrapped_file = csv.reader(file)

    # iterate through file and add each row to a new list
    for row in wrapped_file:
        #print(row)
        table_result.append(row)

    # close file
    file.close()

    # returns table
    #print(table_result)
    return table_result


def write_csv(data,filename):
    """
    Writes the given data out as a CSV file filename.
    
    To be a proper CSV file, data must be a 2-dimensional list with the first row 
    containing only strings.  All other rows may be any Python value.  Dates are
    converted using ISO formatting. All other objects are converted to their string
    representation.
    
    Parameter data: The Python value to encode as a CSV file
    Precondition: data is a  2-dimensional list of strings
    
    Parameter filename: The file to read
    Precondition: filename is a string representing a path to a file with extension
    .csv or .CSV.  The file may or may not exist.
    """
    # print tracing
    #print(" running write_csv")

    # verify input
    #print(" data is: ", data)
    #print(" data type is: ", type(data))
    #print(" filename is: ", filename)

    # create/open file
    file_to_write = open(filename,'w',newline='')

    # wrap file as a csv
    wrapped_file = csv.writer(file_to_write)

    # iterate through data and write to csv file
    for row in data:
        #print("  row is: ", row)
        wrapped_file.writerow(row)

    # close file
    file_to_write.close()


def read_json(filename):
    """
    Returns the contents read from the JSON file filename.
    
    This function reads the contents of the file filename, and will use the json module
    to covert these contents in to a Python data value.  This value will either be a
    a dictionary or a list. 
    
    Parameter filename: The file to read
    Precondition: filename is a string, referring to a file that exists, and that file 
    is a valid JSON file
    """
    # verify input
    #print(" filename is: ", filename)
    #print(" running read_json")

    # open file
    file_opened = open(filename)

    # read file contents
    text_to_import = file_opened.read()

    # convert file to readable format
    json_text = json.loads(text_to_import)
    #print(" json_text is: ", json_text)
    #print(" type(json_text) is: ", type(json_text))

    # close file
    file_opened.close()

    # return contents
    return json_text


def str_to_time(timestamp,tz=None):
    """
    Returns the datetime object for the given timestamp (or None if stamp is invalid)
    
    This function should just use the parse function in dateutil.parser to
    convert the timestamp to a datetime object.  If it is not a valid date (so
    the parser crashes), this function should return None.
    
    If the timestamp has a timezone, then it should keep that timezone even if
    the value for tz is not None.  Otherwise, if timestamp has no timezone and 
    tz if not None, this this function will assign that timezone to the datetime 
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
    #print(" time is: ", time)

    # convert time input to a valid datetime object
    #print(" type(time) is: ", type(time))

    # get year
    year = time.year
    #print(" year is: ", year)   

    # get year dictionary
    year_dictionary = daycycle[str(year)]
    ##print(" year_dictionary is: ", year_dictionary)

    # get mm-dd
    ## get month
    month = str(time.month)
    #print(" month is: ", month)
    if len(month) < 2:
        month = "0" + month
        #print("  month is now: ", month)
    
    ## get day
    day = str(time.day)
    #print(" day is: ", day)
    if len(day) < 2:
        day = "0" + day 
        #print("  day is now: ", day)

    mmdd = month + "-" + day
    #print(" mmdd is: ", mmdd)
    
    # get mmdd dictionary
    month_dictionary = year_dictionary[mmdd]
    #print(" month_dictionary is: ", month_dictionary)

    
    # get sunrise info
    sunrise = month_dictionary['sunrise']
    #print(" sunrise is: ", sunrise)
    
    ## get hours and minutes for sunrise
    sunrise_hours = sunrise[0:2]
    if sunrise_hours[0] == '0':
        sunrise_hours = (sunrise_hours[1:2])
        #print("   sunrise_hours is now: ", sunrise_hours)
    
    sunrise_minutes = sunrise[3:5]
    if sunrise_minutes[0] == '0':
        sunrise_minutes = (sunrise_minutes[1:])
        #print("   sunrise_minutes is now: ", sunrise_minutes)

    #print("   sunrise_hours is: ", sunrise_hours, "sunrise_minutes is: ", sunrise_minutes)
    

    # get sunset info 
    sunset = month_dictionary['sunset']
    #print(" sunset is: ", sunset)

    ## get hours and minutes for sunset
    sunset_hours = sunset[0:2]
    if sunset_hours[0] == '0':
        sunset_hours = (sunset_hours[1:2])
        #print("   sunset_hours is now: ", sunset_hours)

    sunset_minutes = sunset[3:5]
    if sunset_minutes[0] == '0':
        sunset_minutes = (sunset_minutes[1:])
        #print("   sunset_minutes is now: ", sunset_minutes)

    #print("   sunset_hours is: ", sunset_hours, "sunset_minutes is: ", sunset_minutes)


    # create sunrise, sunset, and now objects:
    #print("   time.tzinfo is: ", time.tzinfo)
    is_aware = time.tzinfo != None              # does time have a tz?
    #print("   is_aware is: ", is_aware)
    
    if is_aware == True:
        #print("    time has a tz")
        tz = pytz.timezone('America/New_York')                                                                          #sunrise/set tz from daycycle.json        
        
        # create sunrise
        sunrise_naive = datetime.datetime(int(year),int(month),int(day),int(sunrise_hours),int(sunrise_minutes))        #create datetime object without tz
        #print("      sunrise is: ", sunrise)
        sunrise = tz.localize(sunrise_naive)                                                                            #localize it with tz.localize method
        #print("      sunrise is: ", sunrise)

        # create sunset
        sunset_naive = datetime.datetime(int(year),int(month),int(day),int(sunset_hours),int(sunset_minutes))
        #print("      sunset is: ", sunset)
        sunset = tz.localize(sunset_naive)
        #print("      sunset is: ", sunset)

        # create now
        now = time


    if is_aware == False:
        #print("    time has no tz")
        pass


    # check values
    #print("   sunrise is: ", sunrise)
    #print("   now is:     ", now)
    #print("   sunset is:  ", sunset)

    # evaluate
    if now <= sunrise:
        #print(" now is before sunrise, returning false")
        return False

    if now > sunrise:
        
        if now < sunset:
            #print(" sunrise < now < sunset is true ")
            return True

        if now >= sunset:
            #print(" now is after sunset, returning false")
            return False


def get_for_id(id,table):
    """
    Returns (a copy of) a row of the table with the given id.
    
    Table is a two-dimensional list where the first element of each row is an identifier
    (string).  This function searches table for the row with the matching identifier and
    returns a COPY of that row. If there is no match, this function returns None.
    
    This function is useful for extract rows from a table of pilots, a table of instructors,
    or even a table of planes.
    
    Parameter id: The id of the student or instructor
    Precondition: id is a string
    
    Parameter table: The 2-dimensional table of data
    Precondition: table is a non-empty 2-dimension list of strings
    """

    #print(" running get_for_id")

    # verify data
    #print("  id is: ", repr(id))
    #print("  type(id) is: ", type(id))
    #print("  table is: ", table)
    #print("  type(table) is: ", type(table))

    # set initial vars
    #print("  table[0] is: ", table[0])
    table_rows = len(table)
    table_columns = len(table[0])
    #print(" table_rows is: ", table_rows, "table_columns is: ", table_columns)
    row_index = 0
    column_index = 0
    result_row = []
    found_row = None
    

    # read table rows and columns
    try:
        for row_index in range(table_rows):           
            #print(" row_index:", row_index, table[row_index])
            for column_index in range(table_columns):
                #print("   column_index is: ", column_index, "content is: ", table[row_index][column_index])
                cell_content = table[row_index][column_index]
                #print("   cell_content is: ", cell_content)               
                if cell_content == id:
                    #print("    id found ", id, " in ", table[row_index])
                    #print("    row_index is: ", row_index)
                    found_row = row_index
            row_index = row_index + 1


    except:
        return None 

    # create a list from row defined by given id
    if found_row != None:
        #print("  id is: ", repr(id))
        #print("  found_row is: ", found_row)
        #print("   row contents is ", table[found_row])
        ## loop through columsn in row and built result copy row
        result_row = table[found_row]
        #print("   result_row is: ", result_row)

        #print(" ")
        return result_row

