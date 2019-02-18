# Name: PHUONG TRAN
# G#: G01082824
# Lab 9
# Due Date: 11/5/2018
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

def counts(xs):
  count_val={} # Create a dictionary
  for a in xs: # for loop going through each element in given list
        count_val[a]=xs.count(a) # create a key pair in dictionary
  return count_val # Finally, return answer

def weeklies(plant_d):
    weekly_water=[] # Create an empty list
    for a in plant_d: # go through each key in dict
        if plant_d.get(a)=='weekly': # use d.get() to get the key's value and compare
            weekly_water.append(a) # if the value is weekly then add the key to created list
    weekly_water.sort() # sort the answer
    return weekly_water # finally, return answer


def closest(d, what, here):
    import math # import math for distance calculation
    close = None # Initialize needed variables
    temp = list(d.keys())
    if len(d)>0:
        # math formula of the first key-value in given dict
        d_0 = math.sqrt(((temp[0][1] - here[1]) ** 2) + ((temp[0][0] - here[0]) ** 2))
        for a in temp:
            d_1 = (math.sqrt(((a[1] - here[1]) ** 2) + ((a[0] - here[0]) ** 2)))
            if d_0 >= d_1: # Checking for smaller value
                if d[a] == what:
                    close = a
    return close # Finally, return answer

def file_counts(filename):
    xs=[] # Create empty list
    file = open(filename) # open given file
    for line in file: # go through each line in the txt file
        xs.append(int(line)) # add it to the list, change str to int
    file.close() # close file after done
    return counts(xs) # return the return of count function
