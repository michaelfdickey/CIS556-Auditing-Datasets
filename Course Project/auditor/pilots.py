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

    #print(" ------------- CHECKING PILOT certifications ----------------------")
    # verify input
    ##print(" takeoff is: ", takeoff, "type(takeoff) is:", type(takeoff))
    ##print(" student_row is: ", student)

    """
    # display student info
    #print("  student_id :", student[0])
    #print("  last name  :", student[1])
    #print("  first name :", student[2])
    #print("  joined     :", student[3])
    #print("  solo       :", student[4])
    #print("  license    :", student[5])
    #print("  50 hours   :", student[6])
    #print("  instrument :", student[7])
    #print("  advanced   :", student[8])
    #print("  multiengine:", student[9])
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
    #print("   student_milestones: ", student_milestones)

    # evaluate flight
    #print("    takeoff is: ", str(takeoff))
    
    ## PILOT_INVALID = -1  # The certification of this pilot is unknown
    #print("    joined  is: ", str(student_milestones['joined']))
    #print("   ++++takeoff is: ", takeoff)
    #print("   ++++student_milestones['joined'] is: ", student_milestones['joined'])
    #print("   ++++type(takeoff)is ", type(takeoff))
    #print("   ++++type(student_milestones['joined'] is ", type(student_milestones['joined']))
    #print("   ++++type(student_milesones['solo']) is: ", type(student_milestones['solo']))
    #print("   ++++student_milestones['solo'] is: ", student_milestones['solo'])

    #print("   ++++ takeoff is: ", str(takeoff))
    #print("   ++++ joined is : ", str(student_milestones['joined']))
    #print("   ++++ solo is   : ", str(student_milestones['solo']))
    #print("   ++++ license is: ", str(student_milestones['license']))
    #print("   ++++ 50hours is: ", str(student_milestones['50hours']))

    #print("   ++++ takeoff.tzinfo is: ", takeoff.tzinfo)

    # give student milestone flight tz info
    #takeoff has tz info, student milestone does not
    if takeoff.tzinfo != None:
        #print("    RUNNING checks to convert to aware datetimes")
        if student_milestones['joined'].tzinfo == None:
            tz = takeoff.tzinfo
            student_milestones_joined_naive = student_milestones['joined']
            student_milestones_joined_aware = student_milestones_joined_naive.replace(tzinfo=tz)
            #print("   ++++ student_milestones_joined_aware is  : ", student_milestones_joined_aware)
        
        #if student_milestones['joined'].tzinfo != None:
        #    student_milestones_joined_aware = student_milestones['joined']
        #    print("   ++++student_milestones_joined_aware is     :", student_milestones_joined_aware)

        if student_milestones['solo'] != '':                #skips if empty
            if student_milestones['solo'].tzinfo == None:
                tz = takeoff.tzinfo
                student_milestones_solo_naive = student_milestones['solo']
                student_milestones_solo_aware = student_milestones_solo_naive.replace(tzinfo=tz)
                #print("   ++++ student_milestones_solo_aware is    : ", student_milestones_solo_aware)

        if student_milestones['license'] != '':
            if student_milestones['license'].tzinfo == None:
                student_milestones_license_naive = student_milestones['license']
                student_milestones_license_aware = student_milestones_license_naive.replace(tzinfo=tz)
                #print("   ++++ student_milestones_license_aware is  :", student_milestones_license_aware)
        
        if student_milestones['50hours'] != '':
            if student_milestones['50hours'].tzinfo == None:
                student_milestones_50hours_naive = student_milestones['50hours']
                student_milestones_50hours_aware = student_milestones_50hours_naive.replace(tzinfo=tz)
                #print("   ++++ student_milestones_50hours_aware is: ", student_milestones_50hours_aware)


        if student_milestones['instrument'] != '':
            if student_milestones['instrument'].tzinfo == None:
                student_milestones_instrument_naive = student_milestones['instrument']
                student_milestones_instrument_aware = student_milestones_instrument_naive.replace(tzinfo=tz)


    #print("   ++++ takeoff is:                          :", takeoff)



    # both have no tz info
    if takeoff.tzinfo == None:
        
        if student_milestones['joined'].tzinfo == None:
            student_milestones_joined_aware = student_milestones['joined']
            #print("   ++++student_milestones_joined_aware is     :", student_milestones_joined_aware)

        if student_milestones['solo'] != '':
            if student_milestones['solo'].tzinfo == None:
                student_milestones_solo_aware = student_milestones['solo']
                #print("   ++++student_milestones_solo_aware is       :", student_milestones_solo_aware)

        if student_milestones['license'] != '':
            if student_milestones['license'].tzinfo == None:
                student_milestones_license_aware = student_milestones['license']
                #print("   ++++student_milestones_license_aware is    :", student_milestones_license_aware)

        if student_milestones['50hours'] != '':
            if student_milestones['50hours'].tzinfo == None:
                student_milestones_50hours_aware = student_milestones['50hours']
                #print("   ++++student_milestones_50hours_aware is    :", student_milestones_50hours_aware)

        if student_milestones['instrument'] != '':
            if student_milestones['instrument'].tzinfo == None:
                student_milestones_instrument_aware = student_milestones['instrument']
                #print("   ++++student_milestones_instrument_aware is :", student_milestones_instrument_aware)



    # test and return certification status comparing takeoff against milestones
    ## joined only
    try:
        if takeoff < student_milestones_joined_aware:
            #print(" ++++ ++++PILOT_INVALID")
            return -1
    except:
        pass 

    # joined but solo blank
    try:
        if takeoff > student_milestones_joined_aware:
            #print("    ++++ takeoff is > joined ")
            if student_milestones['solo'] == '':
                #print(" ++++ ++++PILOT_NOVICE")
                return 0
    except:
        pass 

    # joined but before solo
    try:
        if takeoff > student_milestones_joined_aware:
            #print("    ++++ takeoff is > joined but < solo ")
            if takeoff < student_milestones_solo_aware:
                #print(" ++++ ++++PILOT_NOVICE")
                return 0
    except:
        pass 

    # soloed but license blank
    try:
        if takeoff > student_milestones_solo_aware:
            if student_milestones['license'] == '':
                #print(" ++++ ++++ PILOT_STUDENT")
                return 1 
    except:
        pass 

    # soloed but before license
    try:
        if takeoff > student_milestones_solo_aware:
            if takeoff < student_milestones_license_aware:
                #print(" ++++ ++++ PILOT_STUDENT")
                return 1
    except:
        pass 

    # licese but 50hours blank
    try:
        if takeoff > student_milestones_license_aware:
            if student_milestones['50hours'] == '':
                #print(" ++++ ++++ license < takoff PILOT_CERTIFIED")
                return 2
    except:
        pass 

    # license but before 50hours
    try:
        if takeoff > student_milestones_license_aware:
            if takeoff < student_milestones_50hours_aware:
                #print(" ++++ ++++ license < takeoff < 50hours PILOT_CERTIFIED")
                return 2
    except:
        pass 

    # 50hours but instrument blank
    try: 
        if takeoff > student_milestones_50hours_aware:
            #if student_milestones['instrument'] == '':
            #print(" ++++ ++++ 50hours < takeoff PILOT_50_HOURS")
            return 3 
    except:
        pass 

    return -1

    """usefull in stretch goals, but cert check doesn't go past 50 hours in required course
    # 50 hours but before instrument
    try:
        if takeoff > student_milestones_50hours_aware:
            if takeoff < student_milestones_instrument_aware:
                print(" ++++ ++++ 50hours < takeoff < instrument PILOT_50_HOURS")
                return 3 
    except:
        pass 
    """

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
    ##print(" takeoff is: ", takeoff, "type(takeoff) is: ", type(takeoff))
    ##print(" student is: ", student)

    """
    # display all student info
    #print("  student_id :", student[0])
    #print("  last name  :", student[1])
    #print("  first name :", student[2])
    #print("  joined     :", student[3])
    #print("  solo       :", student[4])
    #print("  license    :", student[5])
    #print("  50 hours   :", student[6])
    #print("  instrument :", student[7])
    #print("  advanced   :", student[8])
    #print("  multiengine:", student[9])
    """

    # no instrument rating at all, always false
    if student[7] == '':
        ##print("  student has no instrument rating, returning False")
        return False

    # if license has a date then convert to datetime.datetime object
    if student[7] != '':
        ##print("  student has an instrument rating, ", student[7])
        instrument_date = parse(student[7])
        ##print("  instrument_date is: ", str(instrument_date))

    # check if takeoff is after instrument date
    #print(" +++++takeoff is:         ", str(takeoff))
    #print(" +++++instrument_date is: ", str(instrument_date))

    if takeoff.tzinfo != None:
        if instrument_date.tzinfo == None:
            tz = takeoff.tzinfo
            instrument_date_naive = instrument_date
            instrument_date = instrument_date.replace(tzinfo=tz)


    if takeoff > instrument_date:
        ##print("  student was instrument rated at time of takeoff")
        return True 
    else:
        ##print("  student was not instrument rated at time of takeoff")
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
        ##print("  student has no instrument rating, returning False")
        return False

    # if advanced has a date then convert to datetime.datetime object
    if student[8] != '':
        ##print("  student has an instrument rating, ", student[8])
        advanced_date = parse(student[8])
        ##print("  advanced_date is: ", str(advanced_date))

    # check if takeoff is after instrument date
    #print(" +++++takeoff is:         ", str(takeoff))
    #print(" +++++advanced_date is:   ", str(advanced_date))

    if takeoff.tzinfo != None:
        if advanced_date.tzinfo == None:
            tz = takeoff.tzinfo
            advanced_date_naive = advanced_date
            advanced_date = advanced_date_naive.replace(tzinfo=tz)

    # check if takeoff is after advanced date
    if takeoff > advanced_date:
        ##print("  student was instrument rated at time of takeoff")
        return True 
    else:
        ##print("  student was not instrument rated at time of takeoff")
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
        ##print("  student has no multiengine rating, returning False")
        return False

    # if multiengine has a date then convert to datetime.datetime object
    if student[9] != '':
        ##print("  student has an multiengine rating, ", student[9])
        multiengine_date = parse(student[9])
        ##print("  multiengine_date is: ", str(multiengine_date))

    # check if takeoff is after multiengine date
    if takeoff > multiengine_date:
        ##print("  student was multiengine rated at time of takeoff")
        return True 
    else:
        ##print("  student was not multiengine rated at time of takeoff")
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
    If the value is 'Student', it is a match if category is PILOT_STUDENT or higher.  
    If the value is 'Certified, it is a match if cert is PILOT_CERTIFIED or higher. 
    If it is '50 Hours', it is only a match if cert is PILOT_50_HOURS. 
    The value 'Dual'  only matches if instructed is True.
    
    The second column (CONDITIONS) has values 'VMC' and 'IMC'. 
    A flight filed as VFR (visual flight rules) is subject to VMC (visual meteorological conditions) minimums.  
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
    
    #print("  ")
    #print("  Running get_minimums")
    #print("  >>>>> NEXT TEST CASE <<<<< ")
    #print("  ")
    
    # verify inputs:
    #print(" verifying inputs:")
    #print("  cert is:       ", cert)
    #print("  area is:       ", area)
    #print("  instructed is: ", instructed)
    #print("  vfr is:        ", vfr)
    #print("  daytime is:    ", daytime)
    ##print("  minimums is:", minimums)

    """
    for row in minimums:
        #print(row)
    """

    # Check pilot certifications
    """
    # certification references
    # PILOT_INVALID = -1     # The certification of this pilot is unknown
    # PILOT_NOVICE  = 0      # A pilot that has joined the school, but has not soloed
    # PILOT_STUDENT = 1      # A pilot that has soloed but does not have a license
    # PILOT_CERTIFIED = 2    # A pilot that has a license, but has under 50 hours post license 
    # PILOT_50_HOURS  = 3    # A pilot that 50 hours post license
    """
    """
    The first column (CATEGORY) has values 'Student', 'Certified', '50 Hours', or 'Dual'.
    If the value 'Student', it is a match if cert is PILOT_STUDENT or higher.  If
    the value is 'Certified, it is a match if cert is PILOT_CERTIFIED or higher. If
    it is '50 Hours', it is only a match if cert is PILOT_50_HOURS. The value 'Dual' 
    only matches if instructed is True.
    """    
    #print(" ------------- CHECKING PILOT minimums ----------------------")
    #print(" checking certifications", cert, "instructed is: ", instructed)
    if cert == -1:
        #print("  PILOT_INVALID")
        allowed_categories = []
    if cert == 0:
        #print("  PILOT_NOVICE")
        allowed_categories = []
    if cert == 1:
        #print("  PILOT_STUDENT")
        allowed_categories = ['Student']
    if cert == 2:
        #print("  PILOT_CERTIFIED")
        allowed_categories = ['Student','Certified']
    if cert == 3:
        #print("  PILOT_50_HOURS")
        allowed_categories = ['Student','Certified','50 Hours']

    #print("   category is:", allowed_categories)    

    if instructed == True:
        #print("    adding Dual since instructor = true")
        allowed_categories.append('Dual')
        #print("   category is:", allowed_categories)  

    ## NO FLIGHT ALLOWED conditions:
    if cert == -1:
        if instructed == False:
            #print(" pilot should not be flying alone, return None")
            return None

    if cert == 0:
        if instructed == False:
            #print(" pilot has not soloed and should note be flying alone, return None")
            return None

    if cert == 1:
        if instructed == False:
            if vfr == False:
                #print("  pilot not certified for IFR flight alone, returning None")
                return None

    if cert == 1:
        if instructed == False:
                if vfr == False:
                    if daytime == False:
                        #print(" pilot is student, flying at night alone and vfr false ")
                        return None

    

     #check conditions
    """
    The second column (CONDITIONS) has values 'VMC' and 'IMC'. 
    A flight filed as VFR (visual flight rules) is subject to VMC (visual meteorological conditions) minimums.
    Similarly, a fight filed as IFR is subject to IMC minimums.
    """
    """
    **Conditions** describe the overall visibility of the flight. 
    The conditions are either `VMC` (visual meteorological conditions) or “IMC” (instrument meteorological conditions). 
    A pilot is either flying VFR (visual flight rules) or IFR (instrument flight rules). 
    A pilot flying IFR may fly in either VMC or IMC conditions, but a pilot flying VFR may only fly in VMC conditions
    """
    """
    Parameter vfr: Whether the pilot has filed this as an VFR flight
    Precondition: vfr is a boolean
    """
    #print(" checking conditions, vfr: ", vfr, "day:", daytime)
    if vfr == True:
        allowed_conditions = ['VMC']
    if vfr == False:
        allowed_conditions = ['IMC','VMC']
    #print("   conditions are: ", allowed_conditions)


    # check area
    """
    The third column (AREA) has values 'Pattern', 'Practice Area', 'Local', 
    'Cross Country', or 'Any'. Flights that are in the pattern or practice area match
    'Local' as well.  All flights match 'Any'.
    """
    """
    **Area** is the area in which the flight takes place. “Pattern” is a tight pattern around the airport
     (where the flight school is hosted). “Practice Area” is an area away from the airport but very nearby.
      “Cross Country” is a flight to another airport.
    """
    #print(" checking area:", area)
    if area == "Pattern":
        allowed_areas = ['Pattern','Any','Local']
    if area == "Practice Area":
        allowed_areas = ['Practice Area','Local','Any']
    if area == "Local":
        allowed_areas = ['Practice','Practice Area','Any']
    if area == "Any":
        allowed_areas = ['Pattern','Practice Area','Local','Cross Country','Any']
    if area == "Cross Country":
        allowed_areas = ['Cross Country','Any']
    #print("   allowed_areas are: ", allowed_areas)


    # check time
    """
    **Time** is either night or day.
    The fourth column (TIME) has values 'Day' or 'Night'. The value 'Day' is only 
    a match if daytime is True. If it is False, 'Night' is the only match.
    """
    #print(" checking daytime, daytime is:", daytime)
    if daytime == True:
        allowed_time = ['Day']
    if daytime == False:
        allowed_time = ['Night']
    #print("   allowed_time is: ", allowed_time)





    #check categories in mininum for matching rows 
    ## loop through rows in mininum checking against list of allowed categories and capturing matching rows
    #print("  checking rows that match allowed categories: ", allowed_categories)
    category_matching_rows = []
    for row_index in range(len(minimums)):
        ##print(row_index, (minimums[row_index]))
        for allowed_cat_index in range(len(allowed_categories)):
            if minimums[row_index][0] == allowed_categories[allowed_cat_index]:
                ##print("    category found, row: ", row_index, minimums[row_index])
                category_matching_rows.append(row_index)
    #print("     category_matching_rows are: ", category_matching_rows)


    
    # check conditions in minimum for matching rows
    #print("  checking rows that match allowed conditions", allowed_conditions)
    conditions_matching_rows = []
    for row_index in range(len(minimums)):
        for allowed_conditions_index in range(len(allowed_conditions)):
            if minimums[row_index][1] == allowed_conditions[allowed_conditions_index]:
                ##print("    condition found, row:",row_index, minimums[row_index])
                conditions_matching_rows.append(row_index)
    #print("     conditions_matching_rows are: ", conditions_matching_rows)


    # check areas in minimums for matching rows
    #print("  checking rows that match allowed areas", allowed_areas)
    areas_matching_rows = []
    for row_index in range(len(minimums)):
        for allowed_areas_index in range(len(allowed_areas)):
            if minimums[row_index][2] == allowed_areas[allowed_areas_index]:
                ##print("    area found, row: ", row_index, minimums[row_index])
                areas_matching_rows.append(row_index)
    #print("    areas_matching_rows are: ", areas_matching_rows)


    # check times in minimums for matching rows
    #print("  checking times that match allowed times", allowed_time)
    times_matching_rows = []
    for row_index in range(len(minimums)):
        for allowed_time_index in range(len(allowed_time)):
            if minimums[row_index][3] == allowed_time[allowed_time_index]:
                ##print("    time found, row: ", row_index, minimums[row_index])
                times_matching_rows.append(row_index)
    #print("   times_matching_rows are: ", times_matching_rows)


    # find rows that match all the catagories
    #print(" category_matching_rows", category_matching_rows)
    #print(" conditions_matching_rows", conditions_matching_rows)
    #print(" areas_matching_rows", areas_matching_rows)
    #print(" times_matching_rows", times_matching_rows)

    matching_rows = []
    for current_category_row in category_matching_rows:
        ##print("  current_category_row: ", current_category_row)
        for current_condition_row in conditions_matching_rows:
            ##print("   current_condition_row is: ", current_condition_row)
            for current_area_row in areas_matching_rows:
                ##print("    current_area_row is: ", current_area_row)
                for current_time_row in times_matching_rows:
                    ##print("      current_time_row is: ", current_time_row)
                    if current_category_row == current_condition_row:
                        if current_condition_row == current_area_row:
                            if current_area_row == current_time_row:
                                #print("  matching row found: ", current_category_row, current_condition_row, current_area_row, current_time_row)
                                matching_rows.append(current_time_row)

    #print(" matching rows are: ", matching_rows)

    if matching_rows == []:
        #print(" no matching rows: returning None")
        return None
    
    ### GET MININUM CIELING AND VISIBILITY AND MAX WIND AND CROSSWIND
    #print(" data from avaialable matching rows:")
    #for row in matching_rows:
        #print("  minimums[row]", row, minimums[row])

    # get cieling from each matching row
    allowed_cielings = []
    for row in matching_rows:
        allowed_cielings.append(float(minimums[row][4]))
    #print("   allowed_cielings are: ", allowed_cielings)

    # get visibility from each matching row
    allowed_visibility = []
    for row in matching_rows:
        allowed_visibility.append(float(minimums[row][5]))
    #print("   allowed_visibility are: ", allowed_visibility)

    # get wind from each matching row
    allowed_winds = []
    for row in matching_rows:
        allowed_winds.append(float(minimums[row][6]))
    #print("   allowed_winds are: ", allowed_winds)

    # crosswind from each matching row 
    allowed_crosswinds = []
    for row in matching_rows:
        allowed_crosswinds.append(float(minimums[row][7]))
    #print("   allowed_crosswinds are: ", allowed_crosswinds)

    # return min from ciel and vis and max from wind and crosswind
    #sort for min & max
    allowed_cielings.sort(reverse=True)
    allowed_visibility.sort()
    allowed_winds.sort()
    allowed_crosswinds.sort()

    #print(" FINAL values to return", float(min(allowed_cielings)), float(min(allowed_visibility)), float(max(allowed_winds)), float(max(allowed_crosswinds)))
    minimums_result = []
    minimums_result.append(float(min(allowed_cielings)))
    minimums_result.append(float(min(allowed_visibility)))
    minimums_result.append(float(max(allowed_winds)))
    minimums_result.append(float(max(allowed_crosswinds)))
    #print("     >> RETURNING RESULT >> minimums_result = ", minimums_result)
    
    return minimums_result