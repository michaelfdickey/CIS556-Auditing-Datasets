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