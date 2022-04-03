utils.get_for_id was unable to find student 'S00324' in 
[
['STUDENT', 'AIRPLANE', 'INSTRUCTOR', 'TAKEOFF', 'LANDING', 'FILED', 'AREA'], 
['S00309', '738GG', 'I076', '2015-01-12T09:00:00-05:00', '2015-01-12T11:00:00-05:00', 'VFR', 'Pattern'], 
['S00308', '133CZ', 'I053', '2015-01-13T09:00:00-05:00', '2015-01-13T12:00:00-05:00', 'VFR', 'Practice Area'], 
['S00324', '426JQ', 'I053', '2015-02-04T11:00:00-05:00', '2015-02-04T14:00:00-05:00', 'VFR', 'Cross Country'], 
['S00319', '811AX', 'I072', '2015-02-06T13:00:00-05:00', '2015-02-06T15:00:00-05:00', 'VFR', 'Pattern'], 
['S00321', '738GG', 'I072', '2015-02-08T10:00:00-05:00', '2015-02-08T13:00:00-05:00', 'VFR', 'Practice Area'], 
['S00308', '811AX', 'I072', '2015-02-23T09:00:00-05:00', '2015-02-23T13:00:00-05:00', 'VFR', 'Cross Country']
]
Line 335 of tests\test_utils.py: assert_equals(result, FILE1[3]



	# convert dates to date-time objects
    #for date in student[3:9]:
    #    print("   date is:",date)




    
    """
    # get components of date
    date_temp = date_joined
    print("    date_joined is: ", date_joined)
    year = date_temp[0:4]
    month = date_temp[5:7]
    day = date_temp[8:10]
    print("    year is:", repr(year), "month is: ", repr(month), "day is:",repr(day))
    """
