"""
A simple function comparing datetime objects.

Author: Michael Dickey
Date:   Mar 30 2022
"""
import datetime


def is_before(d1,d2):
    """
    Returns True if event d1 happens before d2.
    
    Values d1 and d2 can EITHER be date objects or datetime objects.If a date object,
    assume that it happens at midnight of that day. 
    
    Parameter d1: The first event
    Precondition: d1 is EITHER a date object or a datetime object
    
    Parameter d2: The first event
    Precondition: d2 is EITHER a date object or a datetime object
    """
    # HINT: Check the type of d1 or d2. If not a datetime, convert it for comparison

    # verify input
    print(" d1 is: ", d1, ", d2 is: ", d2)
    print(" d1 type: ", type(d1))
    print(" d2 type: ",type(d2))
    #print(" ")

    # set initial values:
    result = False

    # if types match
    if type(d1) == type(d2):
        print("  they are the same type")
        if d1 < d2:
            print("   d1 is less than d2")
            print("   returning True")
            result = True
            return result
        else:
            print("   d1 is NOT less than d2")
            print("   returning False")
            result = False 
            return result

    #print(" ")

    # convert d1 datetime.datetime
    if isinstance(d1, datetime.datetime) == False:
        print("  d1 type: ", type(d1))
        print("  d1 is not datetime.datetime, converting")
        d1 = datetime.datetime(d1.year,d1.month,d1.day,0,0,0)
        print("    d1 is now: ", str(d1))

    #print(" ")

    # convert d2 datetime.datetime
    if isinstance(d2, datetime.datetime) == False:
        print("  d2 type: ",type(d2))
        print("  d2 is not datetime.datetime, converting")
        d2 = datetime.datetime(d2.year,d2.month,d2.day,0,0,0)
        print("    d2 is now: ", str(d2))

    #print(" ")

    # if types match
    if type(d1) == type(d2):
        print("  they are the same type")
        if d1 < d2:
            print("   d1 is less than d2")
            print("   returning True")
            result = True
            return result

    #print(" ")

    #return False result
    print("    d1 is not less than d2, returning False")
    return result