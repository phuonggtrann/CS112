# Name: PHUONG TRAN
# G#: G01082824
# Lab 13
# Due Date: 12/10/2018
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
def recursive_len(xs):
    if xs==[]:  # Check if xs is empty
        return 0
    else:
        return (1+recursive_len(xs[1:])) # Use slicing to remove 1 elemenet from list
    # And use recursion

def lucas(n):
    # 0 and 1 is the first 2 variables
    if n==0:
        return 2
    elif n==1:
        return 1
    # If n is greater than 1, use recursive
    else:
        return (lucas(n-1)+lucas(n-2))
        
def binary(n):
    # 1 and 0 is no longer diviable there for return themshelves in type string
    if n==1:
        return str(1)
    elif n==0:
        return str(0)
    # If n is greater than 0, use recursion
    elif n>=2:
        return str(binary(n//2))+str(n%2)

def remove_duplicates(msg): # Recursion is used after msg is sliced [1:]
    # If msg is empty, return empty string
    if len(msg) == 0:
        return ''
    # If length of msg is greater than 0
    else:
        if len(msg) == 1: # If length of msg is 1
            return msg[0] + remove_duplicates('') # Add the first char of msg + recursion
        if msg[0] != msg[1]: # If length of msg is greater than 1 and not equal
            # Add the first char of msg + recursion
            return msg[0] + remove_duplicates(msg[1:])
        else: # In other situations not listed above
            return remove_duplicates(msg[1:]) # Return only recursion


