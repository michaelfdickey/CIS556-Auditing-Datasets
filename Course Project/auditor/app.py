"""
Module that validates the flight school's records.

This is the primary module that does all of the work. It loads the files, loops through
the lessons, and searches for any takeoffs that violate insurance requirements.

Technically, we could have put many of these functions in __main__.py.  That is the
main module of this application anyway.  However, for testing purposes we want all
functions in modules and we only want script code in the file __main__.py

Author: Michael Dickey
Date: Apr 9 2022
"""
import utils
import tests
import os.path
import violations
import csv

# Uncomment for the extra credit
#import endorsements
#import inspections


def discover_violations(directory,output):
    """
    Searches the dataset directory for any flight lessons the violation regulations.
    
    This function will call list_weather_violations() to get the list of weather violations.
    If list_endorsment_violations (optional) is completed, it will call that too, as
    well as list_inspection_violations.  It will concatenate all of these 2d lists
    into a single 2d list of violations (so a flight may be listed more than once for
    each of the three types of violations).
    
    If the parameter output is not None, it will create the CSV file with name output
    and write the 2d list of violations to this file.  This CSV file should have the
    following header:
    
        STUDENT,AIRPLANE,INSTRUCTOR,TAKEOFF,LANDING,FILED,AREA,REASON
    
    Regardless of whether output is None, this function will print out the number of
    violations, as follows:
    
        '23 violations found.'
    
    If no violations are found, it will say
    
        'No violations found.'
    
    Parameter directory: The directory of files to audit
    Precondition: directory is the name of a directory containing the files 'daycycle.json',
    'weather.json', 'minimums.csv', 'students.csv', 'teachers.csv', 'lessons.csv',
    'fleet.csv', and 'repairs.csv'.
    
    Parameter output: The CSV file to store the results
    Precondition: output is None or a string that is a valid file name
    """

    # verify input
    #print(" --------RUNNING DISCOVER VIOLATIONS -----------")
    #print(" directory is: ", directory)
    #print(" output is: ", output)


    #print(" getting violations.list_weather_violations")
    discovered_weather_violations = violations.list_weather_violations(directory)
    number_discovered_violations = len(discovered_weather_violations)
    
    #print(" discovered_weather_violations are ", discovered_weather_violations)

    # create output csv table
    discovered_violations_table = []
    header_row = ['STUDENT','AIRPLANE','INSTRUCTOR','TAKEOFF','LANDING','FILED','AREA','REASON']
    discovered_violations_table.append(header_row)
    
    # populate new table with products of list_weather_violations
    for row in discovered_weather_violations:
        discovered_violations_table.append(row)
        #print(row)

    #print(" discovered_violations_table: ")
    #print("  ", discovered_violations_table)
    #for row in discovered_violations_table:
    #    print("  ", row)

    # prepare output filename and write csv file
    if output != None:
        output_csv_file = open(output,'w',newline='')
        output_csv_wrapped = csv.writer(output_csv_file)
        for row in discovered_violations_table:
            output_csv_wrapped.writerow(row)
        output_csv_file.close()

    number = number_discovered_violations

    if number == 0:
        print("No violations found.")
    if number == 1:
        print(number,"violation found.")
    if number > 1:
        print(number,"violations found.")


def execute(args):
    """
    Executes the application or prints an error message if executed incorrectly.
    
    The arguments to the application (EXCLUDING the application name) are provided to
    the list args. This list should contain either 1 or 2 elements.  If there is one
    element, it should be the name of the data set folder or the value '--test'.  If
    there are two elements, the first should be the data set folder and the second
    should be the name of a CSV file (for output of the results).
    
    If the user calls this script incorrectly (with the wrong number of arguments), this
    function prints:
    
        Usage: python auditor dataset [output.csv]
    
    This function does not do much error checking beyond counting the number of arguments.
    
    Parameter args: The command line arguments for the application (minus the application name)
    Precondition: args is a list of strings
    """

    # verify input
    #print(" args:",args)

    # get number of args
    number_of_args = len(args)
    #print(" number_of_args:", number_of_args)

    if number_of_args == 0:
        print("Usage: python auditor dataset [output.csv]")

    if number_of_args == 1:
        #print(" number_of_args is 1")
        #if --test used, run tests.test_all()
        if args[0] == '--test':
            #print("  executing test scripts, running tests.test_all")
            tests.test_all()
        
        else:
            #if datafile provided, run it with discover_violations
            #print("  arg is: ", args[0], "running discover_violations" )
            discover_violations(args[0],None)

    if number_of_args == 2:
        if args[0] == '--test':
            print("Usage: python auditor dataset [output.csv]") 
        if args[1] == '--test':
            print("Usage: python auditor dataset [output.csv]") 
        #print(" number_of_args is 2, running discover_violations with ", args[0], ",", args[1])
        discover_violations(args[0],args[1])
    
    if number_of_args > 2:
        print("Usage: python auditor dataset [output.csv]") 