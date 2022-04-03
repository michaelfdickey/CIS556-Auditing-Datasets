"""
Module determining pilot certifications, ratings, and endorsements.

The restrictions that we place on a pilot depend on their qualifications.  There are three
ways to think about a pilot.  

(1) Certifications.  These are what licenses a pilot has.  We also use these to classify
where the student is in the licensing process.  Is the student post solo (can fly without
instructor), but before license?  Is the student 50 hours past their license (a threshold 
that helps with insurance)?

(2) Ratings.  These are extra add-ons that a pilot can add to a license. For this project,
the only rating is Instrument Rating, which allows a pilot to fly through adverse weather
using only instruments.

(3) Endorsements. These are permission to fly certain types of planes solo.  Advanced 
allows a pilot to fly a plane with retractable landing gear. Multiengine allows a pilot
to fly a plane with more than one engine.

The file pilots.csv is a list of all pilots in the school, together with the dates that
they earned these certifications, ratings, and endorsements.  Specifically, this CSV file
has the following header:
    
    ID  LASTNAME  FIRSTNAME  JOINED  SOLO  LICENSE  50 HOURS  INSTRUMENT  ADVANCED  MULTIENGINE

The first three columns are strings, while all other columns are dates.

The functions in this class take a row from the pilot table and determine if a pilot has
a certain qualification at the time of takeoff. As this program is auditing the school 
over a course of a year, a student may not be instrument rated for one flight but might
be for another.

The preconditions for many of these functions are quite messy.  While this makes writing 
the functions simpler (because the preconditions ensure we have less to worry about), 
enforcing these preconditions can be quite hard. That is why it is not necessary to 
enforce any of the preconditions in this module.

Author: Michael Dickey
Date: Apr 02 2022
"""
import utils
import datetime
from dateutil.parser import parse


# CERTIFICATION CLASSIFICATIONS
# The certification of this pilot is unknown
PILOT_INVALID = -1
# A pilot that has joined the school, but has not soloed
PILOT_NOVICE  = 0
# A pilot that has soloed but does not have a license
PILOT_STUDENT = 1
# A pilot that has a license, but has under 50 hours post license
PILOT_CERTIFIED = 2
# A pilot that 50 hours post license
PILOT_50_HOURS  = 3


def get_certification(takeoff,student):
    """
    Returns the certification classification for this student at the time of takeoff.
    
    The certification is represented by an int, and must be the value PILOT_NOVICE, 
    PILOT_STUDENT, PILOT_CERTIFIED, PILOT_50_HOURS, or PILOT_INVALID. It is PILOT_50_HOURS 
    if the student has certified '50 Hours' before this flight takeoff.  It is 
    PILOT_CERTIFIED if the student has a private license before this takeoff and 
    PILOT_STUDENT is the student has soloed before this takeoff.  A pilot that has only
    just joined the school is PILOT_NOVICE.  If the flight takes place before the student
    has even joined the school, the result is PILOT_INVALID.
    
    Recall that a student is a 10-element list of strings.  The first three elements are
    the student's identifier, last name, and first name.  The remaining elements are all
    timestamps indicating the following in order: time joining the school, time of first 
    solo, time of private license, time of 50 hours certification, time of instrument 
    rating, time of advanced endorsement, and time of multiengine endorsement.
    
    Parameter takeoff: The takeoff time of this flight
    Precondition: takeoff is a datetime object
    
    Parameter student: The student pilot
    Precondition: student is 10-element list of strings representing a pilot
    """

    # verify input
    #print(" takeoff is: ", takeoff, "type(takeoff) is:", type(takeoff))
    #print(" student_row is: ", student)

    """
    # display student info
    print("  student_id :", student[0])
    print("  last name  :", student[1])
    print("  first name :", student[2])
    print("  joined     :", student[3])
    print("  solo       :", student[4])
    print("  license    :", student[5])
    print("  50 hours   :", student[6])
    print("  instrument :", student[7])
    print("  advanced   :", student[8])
    print("  multiengine:", student[9])
    """

    # construct datetime.datetime object
    ## create lists from milestones and dates to use to create dictionary below
    student_milestone_keys = ['joined','solo','license','50hours','instrument','advanced','multiengine']
    student_flight_dates =  [student[3],student[4],student[5],student[6],student[7],student[8],student[9]]
    #print("   student_milestone_keys: ", student_milestone_keys)
    #print("   student_flight_dates: ", student_flight_dates)

    ## create initial values for iterating through lists and to create dict
    create_dict_keys = range(7)
    flight_dates_index = 0
    student_milestones = {}

    ## creates a dicitonary of milestone / dates key/value pairs and tries to convert each date to a datetime.datetime object
    ## if failes just adds '' as the value
    for key in student_milestone_keys:
        #print("    ", key)
        try:
            student_milestones[key] = parse(student_flight_dates[flight_dates_index])
        except:
            student_milestones[key] = student_flight_dates[flight_dates_index]      
        flight_dates_index = flight_dates_index + 1
    
    ## check result
    #print("    student_milestones: ", student_milestones)

    # evaluate flight
    #print("    takeoff is: ", str(takeoff))
    
    ## PILOT_INVALID = -1  # The certification of this pilot is unknown
    #print("    joined  is: ", str(student_milestones['joined']))
    try:
        if takeoff < student_milestones['joined']:
            #print(" PILOT_INVALID")
            return -1
    except:
        # date is invalid
        return -1 

    ##PILOT_NOVICE = 0 # A pilot that has joined the school, but has not soloed
    #print("    solo    is: ", str(student_milestones['solo']))
    try:
        if takeoff > student_milestones['joined']:
            if takeoff < student_milestones['solo']:
                #print(" PILOT_NOVICE")
                return 0 
    except:
        if takeoff > student_milestones['joined']:
            #print(" PILOT_NOVICE")
            return 0 

    ##PILOT_STUDENT = 1  A pilot that has soloed but does not have a license
    #print("    license is: ", str(student_milestones['license']))
    try:
        if takeoff > student_milestones['solo']:
            if takeoff < student_milestones['license']:
                #print(" PILOT_STUDENT")
                return 1 
    except:
        if takeoff > student_milestones['solo']:        #for when previous date is met, but there are no additional dates to compare
            #print(" PILOT_STUDENT")
            return 1   


    ##PILOT_CERTIFIED = 2 #    # A pilot that has a license, but has under 50 hours post license
    try:
        if takeoff > student_milestones['license']:
            if takeoff < student_milestones['50hours']:
                #print(" PILOT_CERTIFIED")
                return 2 
    except:
        if takeoff > student_milestones['license']:
            #print(" PILOT_CERTIFIED")
            return 2 

    ##PILOT_50_HOURS  = 3 A pilot that 50 hours post license
    #print("    50hours is: ", str(student_milestones['50hours']))
    try:
        if takeoff > student_milestones['50hours']:
            #print(" PILOT_50_HOURS")
            return 3 
    except:
        pass 
    


def has_instrument_rating(takeoff,student):
    """
    Returns True if the student has an instrument rating at the time of takeoff, False otherwise
    
    Recall that a student is a 10-element list of strings.  The first three elements are
    the student's identifier, last name, and first name.  The remaining elements are all
    timestamps indicating the following in order: time joining the school, time of first 
    solo, time of private license, time of 50 hours certification, time of instrument 
    rating, time of advanced endorsement, and time of multiengine endorsement.
    
    NOTE: Just because a pilot has an instrument rating does not mean that every flight
    with that pilot is an IFR flight.  It just means the pilot could choose to use VFR
    or IFR rules.
    
    Parameter takeoff: The takeoff time of this flight
    Precondition: takeoff is a datetime object
    
    Parameter student: The student pilot
    Precondition: student is 10-element list of strings representing a pilot
    """

    # verify input
    #print(" takeoff is: ", takeoff, "type(takeoff) is: ", type(takeoff))
    #print(" student is: ", student)

    """
    # display all student info
    print("  student_id :", student[0])
    print("  last name  :", student[1])
    print("  first name :", student[2])
    print("  joined     :", student[3])
    print("  solo       :", student[4])
    print("  license    :", student[5])
    print("  50 hours   :", student[6])
    print("  instrument :", student[7])
    print("  advanced   :", student[8])
    print("  multiengine:", student[9])
    """

    # no instrument rating at all, always false
    if student[7] == '':
        #print("  student has no instrument rating, returning False")
        return False

    # if license has a date then convert to datetime.datetime object
    if student[7] != '':
        #print("  student has an instrument rating, ", student[7])
        instrument_date = parse(student[7])
        #print("  instrument_date is: ", str(instrument_date))

    # check if takeoff is after instrment date
    if takeoff > instrument_date:
        #print("  student was instrument rated at time of takeoff")
        return True 
    else:
        #print("  student was not instrument rated at time of takeoff")
        return False

def has_advanced_endorsement(takeoff,student):
    """
    Returns True if the student has an endorsement to fly an advanced plane at the time of takeoff.
    
    The function returns False otherwise.
    
    Recall that a student is a 10-element list of strings.  The first three elements are
    the student's identifier, last name, and first name.  The remaining elements are all
    timestamps indicating the following in order: time joining the school, time of first 
    solo, time of private license, time of 50 hours certification, time of instrument 
    rating, time of advanced endorsement, and time of multiengine endorsement.
    
    Parameter takeoff: The takeoff time of this flight
    Precondition: takeoff is a datetime object
    
    Parameter student: The student pilot
    Precondition: student is 10-element list of strings representing a pilot
    """
    
    # no advanced rating at all, always false
    if student[8] == '':
        #print("  student has no instrument rating, returning False")
        return False

    # if advanced has a date then convert to datetime.datetime object
    if student[8] != '':
        #print("  student has an instrument rating, ", student[8])
        advanced_date = parse(student[8])
        #print("  advanced_date is: ", str(advanced_date))

    # check if takeoff is after advanced date
    if takeoff > advanced_date:
        #print("  student was instrument rated at time of takeoff")
        return True 
    else:
        #print("  student was not instrument rated at time of takeoff")
        return False



def has_multiengine_endorsement(takeoff,student):
    """
    Returns True if the student has an endorsement to fly an multiengine plane at the time of takeoff.
    
    The function returns False otherwise.
    
    Recall that a student is a 10-element list of strings.  The first three elements are
    the student's identifier, last name, and first name.  The remaining elements are all
    timestamps indicating the following in order: time joining the school, time of first 
    solo, time of private license, time of 50 hours certification, time of instrument 
    rating, time of advanced endorsement, and time of multiengine endorsement.
    
    Parameter takeoff: The takeoff time of this flight
    Precondition: takeoff is a datetime object
    
    Parameter student: The student pilot
    Precondition: student is 10-element list of strings representing a pilot
    """

    # no multiengine rating at all, always false
    if student[9] == '':
        #print("  student has no multiengine rating, returning False")
        return False

    # if multiengine has a date then convert to datetime.datetime object
    if student[9] != '':
        #print("  student has an multiengine rating, ", student[9])
        multiengine_date = parse(student[9])
        #print("  multiengine_date is: ", str(multiengine_date))

    # check if takeoff is after multiengine date
    if takeoff > multiengine_date:
        #print("  student was multiengine rated at time of takeoff")
        return True 
    else:
        #print("  student was not multiengine rated at time of takeoff")
        return False


def get_minimums(cert, area, instructed, vfr, daytime, minimums):
    """
    Returns the most advantageous minimums for the given flight category.
    
    The minimums is the 2-dimensional list (table) of minimums, including the header.
    The header for this table is as follows:
        
        CATEGORY  CONDITIONS  AREA  TIME  CEILING  VISIBILITY  WIND  CROSSWIND
    
    The values in the first four columns are strings, while the values in the last
    four columns are numbers.  CEILING is a measurement in ft, while VISIBILITY is in
    miles.  Both WIND and CROSSWIND are speeds in knots.
    
    This function first searches the table for rows that match the function parameters. 
    It is possible for more than one row to be a match.  

    A row is a match if ALL four of the first four columns match.
    
    The first column (CATEGORY) has values 'Student', 'Certified', '50 Hours', or 'Dual'.
    If the value 'Student', it is a match if category is PILOT_STUDENT or higher.  If
    the value is 'Certified, it is a match if category is PILOT_CERTIFIED or higher. If
    it is '50 Hours', it is only a match if category is PILOT_50_HOURS. The value 'Dual' 
    only matches if instructed is True.
    
    The second column (CONDITIONS) has values 'VMC' and 'IMC'. A flight filed as VFR 
    (visual flight rules) is subject to VMC (visual meteorological conditions) minimums.  
    Similarly, a fight filed as IFR is subject to IMC minimums.
    
    The third column (AREA) has values 'Pattern', 'Practice Area', 'Local', 
    'Cross Country', or 'Any'. Flights that are in the pattern or practice area match
    'Local' as well.  All flights match 'Any'.
    
    The fourth column (TIME) has values 'Day' or 'Night'. The value 'Day' is only 
    a match if daytime is True. If it is False, 'Night' is the only match.
    
    Once the function finds the all matching rows, it searches for the most advantageous
    values for CEILING, VISIBILITY, WIND, and CROSSWIND. Lower values of CEILING and
    VISIBILITY are better.  Higher values for WIND and CROSSWIND are better.  It then
    returns this four values as a list of four floats (in the same order they appear)
    in the table.
    
    Example: Suppose minimums is the table
        
        CATEGORY   CONDITIONS  AREA           TIME  CEILING  VISIBILITY  WIND  CROSSWIND
        Student    VMC         Pattern        Day   2000     5           20    8
        Student    VMC         Practice Area  Day   3000     10          20    8
        Certified  VMC         Local          Day   3000     5           20    20
        Certified  VMC         Practice Area  Night 3000     10          20    10
        50 Hours   VMC         Local          Day   3000     10          20    10
        Dual       VMC         Any            Day   2000     10          30    10
        Dual       IMC         Any            Day   500      0.75        30    20
    
    The call get_minimums(PILOT_CERTIFIED,'Practice Area',True,True,True,minimums) matches
    all of the following rows:
        
        Student    VMC         Practice Area  Day   3000     10          20    8
        Certified  VMC         Local          Day   3000     5           20    20
        Dual       VMC         Any            Day   2000     10          30    10
    
    The answer in this case is [2000,5,30,20]. 2000 and 5 are the least CEILING and 
    VISIBILITY values while 30 and 20 are the largest wind values.
    
    If there are no rows that match the parameters (e.g. a novice pilot with no 
    instructor), this function returns None.
    
    Parameter cert: The pilot certification
    Precondition: cert is in int and one PILOT_NOVICE, PILOT_STUDENT, PILOT_CERTIFIED, 
    PILOT_50_HOURS, or PILOT_INVALID.
    
    Parameter area: The flight area for this flight plan
    Precondition: area is a string and one of 'Pattern', 'Practice Area' or 'Cross Country'
    
    Parameter instructed: Whether an instructor is present
    Precondition: instructed is a boolean
    
    Parameter vfr: Whether the pilot has filed this as an VFR flight
    Precondition: vfr is a boolean
    
    Parameter daytime: Whether this flight is during the day
    Precondition: daytime is boolean
    
    Parameter minimums: The table of allowed minimums
    Precondition: minimums is a 2d-list (table) as described above, including header
    """
    # Find all rows that can apply to this student
    # Find the best values for each column of the row
    
    print("Running get_minimums")

    # verify inputs:
    print(" verifying inputs:")
    print("  cert is:", cert)
    print("  area is:", area)
    print("  instructed is: ", instructed)
    print("  vfr is: ", vfr)
    print("  daytime is: ", daytime)
    #print("  minimums is:", minimums)


    # certification references
    # PILOT_INVALID = -1 
    # PILOT_NOVICE  = 0      # A pilot that has joined the school, but has not soloed
    # PILOT_STUDENT = 1      # A pilot that has soloed but does not have a license
    # PILOT_CERTIFIED = 2    # A pilot that has a license, but has under 50 hours post license 
    # PILOT_50_HOURS  = 3    # A pilot that 50 hours post license