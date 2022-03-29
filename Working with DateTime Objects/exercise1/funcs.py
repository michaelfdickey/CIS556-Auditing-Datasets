"""
Functions for working with datetime objects.

Author: Michael Dickey
Date:   Mar 28 2022
"""
import datetime


def christmas_day(year):
    """
    Returns ISO day of the week for Christmas in the given year.
    
    The ISO day is an integer between 1 and 7.  It is 1 for Monday, 7 for Sunday 
    and the appropriate number for any day in-between. 
    
    Parameter year: The year to check for Christmas
    Precondition: years is an int > 0 (and a year using the Gregorian calendar)
    """
    # HINT: Make a date object and use the isoweekday method

    # verify inputs
    #print(" year is: ", year)

    # get day of week from dateimte.date.weekday
    christmas_day = datetime.date(year,12,25).weekday()

    #print(" christmas_day is: ", christmas_day)

    christmas_day = christmas_day + 1                       #because weekday only returns ints from 0 - 6

    return christmas_day

def iso_str(d,t):
    """
    Returns the ISO formatted string of data and time together.
    
    When combining, the time must be accurate to the microsecond.
    
    Parameter d: The month-day-year
    Precondition: d is a date object
    
    Parameter t: The time of day
    Precondition: t is a time object
    """
    # HINT: Combine date and time into a datetime and use isoformat

    # verify input
    print(" d is: ", d)
    print(" t is: ", t)

    # result example 2019-10-12T12:35:15.000205

    date = str(d)
    time = str(t)

    datetime_iso = date + 'T' + time
    print("  datetime_iso is: ", datetime_iso)

    return datetime_iso