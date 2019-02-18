# Name: PHUONG TRAN
# G#: G01082824
# Lab 7
# Due Date: 10/22/2018
#-------------------------------------------------------------------------------
# Honor Code Statement: I received no assistance on this assignment that
# violates the ethical guidelines set forth by professor and class syllabus.
#-------------------------------------------------------------------------------
# References: (list resources used - remember, projects are individual effort!)
#-------------------------------------------------------------------------------
# Comments and assumptions: A note to the grader as to any problems or
# uncompleted aspects of the assignment, as well as any assumptions about the
# meaning of the specification.
#-------------------------------------------------------------------------------
# NOTE: width of source code should be <=80 characters to be readable on-screen.
#2345678901234567890123456789012345678901234567890123456789012345678901234567890
#       10        20        30        40        50        60        70        80
#-------------------------------------------------------------------------------

# Create a function, take in 3 arguments and 1 optional
def rank3(x,y,z, ascending=True):
    total=x+y+z
    # Finding min
    min = x
    if min>y:
        min=y
    if min>z:
        min=z
    # Finding max
    max = x
    if max < y:
        max = y
    if max < z:
        max = z
    # If there is no argument, ascending is default True
    if ascending:
        in_rank=(min,total-min-max,max)
    # If ascending is False
    else:
        in_rank=(max,total-min-max,min) # Total-min-max = the middle number of 3
    # Finally, rertun answer
    return in_rank
# Create a function, take in 2 arguments and 1 optional argument
def remove(val, xs, limit=None):
    # If there is argument for limit and it has to bigger than 0
    if(limit!=None and limit>0):
        # Range take care of how many time it loop through
        for x in range(limit):
            for i in xs:
                if(i==val):
                    xs.remove(i)
                    break # Break to make sure it only remove 1 occurrance
    # Same for above if there is no argument for limit
    if limit==None:
        for a in range(xs.count(val)+1): # Range(xs.count(val)+1 because all the count should be inclusive
            for i in xs:
                if(i==val):
                    xs.remove(i)
    # Return answer
    return None
# Create a function take in 2 arguments and 1 optional argument
def filter_chars(msg, keeps='abcdefghijklmnopqrstuvwxyz'): # Set default for optional argument -> alphabet
    # Initialize needed variable
    new_msg=''
    for a in msg:
        if a.lower() in keeps: # lower to make all the str lower case -> Don't need to check upper case
            new_msg+=a # Added satisfied-condition string to new_msg
    # Return answer
    return new_msg
# Create a function, take in 1 argument and 1 optional argument
def relocate_evens(data,new_home=None):
    # initialize needed variable
    rem=[]
    if new_home==None: # If there is no argument for new_home
        new_list=[]
        for x in data:
            if x%2==0:
                new_list.append(x) # Create another list to store in
                rem.append(x) # Store variable that you append to new_list
        for y in rem: # Remove all that variables you have appended from data
            data.remove(y)
        # Return the answer
        return new_list
    else: # If therer is an argument for new_home
        for x in data:
            if x%2==0:
                new_home.append(x) # Add the satisfied-condition variable to new_home
                rem.append(x) # Same as above
        # Same as above
        for y in rem:
            data.remove(y)
        return new_home




