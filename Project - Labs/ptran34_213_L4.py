#-------------------------------------------------------------------------------
# Name: Phuong Tran
# Lab 4
# Due Date: 09/19/2018
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

# this time, the template does not have as much guidance - please
# look at at the actual project specification for the rules and
# meanings of each function. You can modify any part of the template
# code to get the job done (abiding by the project's rules). For
# instance, you might want a different start value, or to use multiple
# return statements. This template is only offered in order to help
# you get started, it is not truly required in any sense for the 
# project. The function and parameter names must remain the same (e.g.,
# discount and age/major/is_in_military/gpa), but you can use any names you want
# inside of the functions (indented).
#--------------------------------------------------------------------------------

def middle(a,b,c):
    ans = 0
    total = a+b+c

    min = a
    if min > b:
        min = b
    if min > c:
        min = c

    max = a
    if max < b:
        max = b
    if max < c:
        max = c

    ans = total - min - max

    return ans