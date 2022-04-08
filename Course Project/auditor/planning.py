"""
def get_certification(takeoff,student):
Returns the certification classification for this student at the time of takeoff.
The certification is represented by an int, and must be the value PILOT_NOVICE, 
PILOT_STUDENT, PILOT_CERTIFIED, PILOT_50_HOURS, or PILOT_INVALID.

Parameter takeoff: The takeoff time of this flight
Precondition: takeoff is a datetime object

Parameter student: The student pilot
Precondition: student is 10-element list of strings representing a pilot
"""


# Get the takeoff time
    ##convert takeoff time from lessons

# Get the pilot credentials
    ##get row from studens csv for student import it and get cert back. 
    ## get pilot credentials from takeoff time and flight history

# Get the pilot minimums
    # get instrument rating from takeofftime & student
    # get endorsement takeoff & student
    # check if daytime flight
    # get minimums using cert, area, instructed, vfr, daytime, minimums csv



def has_instrument_rating(takeoff,student):
def has_advanced_endorsement(takeoff,student):


def daytime(time,daycycle):
#Returns true if the time takes place during the day.

def get_minimums(cert, area, instructed, vfr, daytime, minimums):
"""
Returns the most advantageous minimums for the given flight category.

~~ NEXT ~~

# Get the weather conditions
    #get weather dictionary of just that day from def get_weather_report
    #split into:
        #visibility
        #winds
        #ceiling
    # check
        # bad_visibility (visibility, minimum)
        # bad_winds (winds, maxwind, maxcross)
        # bad_ceiling (ceiling,minimum)

# Check for a violation and add to result if so

