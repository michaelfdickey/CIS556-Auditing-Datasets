"""
Functions for simple reading to and writing from a file.

Author: Michael Dickey
Date:   Mar 24 2022
"""


def count_lines(filepath):
    """
    Returns the number of lines in the given file.
    
    Lines are separated by the '\n' character, which is standard for Unix files.
    
    Parameter filepath: The file to be read
    Precondition: filepath is a string with the FULL PATH to a text file
    """
    # HINT: Remember, you can use a file in a for-loop
    
    # verify input
    print("filepath is: ", filepath)

    # create accumulator
    number_of_lines = 0 

    file_to_count = open(filepath)

    # test to confirm open and read file
    """
    text = file_to_count.read()
    print(text)
    """

    for line in file_to_count:
        number_of_lines = number_of_lines + 1 

    print("number_of_lines is: ", number_of_lines)

    return number_of_lines


def write_numbers(filepath,n):
    """
    Writes the numbers 0..n-1 to a file.
    
    Each number is on a line by itself.  So the first line of the file is 0,
    the second line is 1, and so on. Lines are separated by the '\n' character, 
    which is standard for Unix files.  The last line (the one with the number
    n-1) should NOT end in '\n'
    
    Parameter filepath: The file to be written
    Precondition: filepath is a string with the FULL PATH to a text file
    
    Parameter n: The number of lines to write
    Precondition: n is an int > 0.
    """
    # HINT: You can only write strings to a file, so convert the numbers first
    pass            # Implement me

