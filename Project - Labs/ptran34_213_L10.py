# Name: PHUONG TRAN
# G#: G01082824
# Lab 10
# Due Date: 11/12/2018
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

def get(xs, index, response=None):
    try:
        return (xs[index]) # If the index is found in xs

    except:
        return response # If there is an index error

def classify(input_string):
    new_string = input_string.split(' ')
    tup=([],[])
    for x in new_string:
        try: # if x is int
            int(x)
            tup[0].append(int(x))
        except: # if x is not an int
            if x !='': # if x is not empty string
                tup[1].append(x)
    return tup # return answer as tuple

def shelve(inventory, product_list):
    for update in product_list:
        if update[0] not in inventory:
            if update[1] < 0:
                raise ValueError('negative amount for ' + update[0]) # Raise error if value is negative
            else:
                inventory[update[0]]=update[1]
        else:
            if (inventory[update[0]] + update[1]) < 0:
                raise ValueError('negative amount for '+ update[0])
            else:
                inventory[update[0]] += update[1]
    return None # return None since u modified given dict


