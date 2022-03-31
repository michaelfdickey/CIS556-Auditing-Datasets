"""
A simple function computing time elapsed

Author: Michael Dickey
Date:   Mar 30 2022
"""
import datetime


def past_a_week(d1,d2):
    """
    Returns True if event d2 happens at least a week (7 days) after d1.
    
    If d1 is after d2, or less than a week has passed, this function returns False.
    Values d1 and d2 can EITHER be date objects or datetime objects.If a date object,
    assume that it happens at midnight of that day. 
    
    Parameter d1: The first event
    Precondition: d1 is EITHER a date objects or a datetime object
    
    Parameter d2: The first event
    Precondition: d2 is EITHER a date objects or a datetime object
    """
    # HINT: Check the type of d1 or d2. If not a datetime, convert it for comparison

    # verify inputs
    print(" d1 is: ", d1, " d2 is: ", d2)
    print(" type(d1) is: ", type(d1))
    print(" type(d2) is: ", type(d2))

    # set initial variables
    result = False

    # convert datetime.date to datetime.datetime
    if isinstance(d1, datetime.datetime) == False:
        print("  d1 is not datetime.datetime, converting")
        d1 = datetime.datetime(d1.year,d1.month,d1.day,0,0,0)

    if isinstance(d2, datetime.datetime) == False:
        print("  d2 is not datetime.datetime, converting")
        d2 = datetime.datetime(d2.year,d2.month,d2.day,0,0,0)

    print("   d1 is: ", d1, " d2 is: ", d2)

    # check if d1 after d2, return false if it is
    if d1 > d2:
        print("  d1 is after d2, returning False")
        result = False
        return result

    # get time delta d1 and d2
    time_diff = d2 - d1
    print("   time_diff is: ", time_diff)
    print("   time_diff.days is: ", time_diff.days)


    # evaluate if timeD > 1 week
    if time_diff.days >= 7:
        print("    more than a week has passed, returning True")
        result = True
        return result


    # else return False
    return result
