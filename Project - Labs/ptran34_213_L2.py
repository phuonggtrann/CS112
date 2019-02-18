#-------------------------------------------------------------------------------
#	Name:	Phuong Tran
#	G#: G01082824
#	Lab 2
#	Due	Date:	09/10/2018
#-------------------------------------------------------------------------------
#	Honor	Code	Statement:	I	received	no	assistance	on	this	assignment	that
#	violates	the	ethical	guidelines	set	forth	by	professor	and	class	syllabus.
#-------------------------------------------------------------------------------
#	References:	(list	resources	used	- remember,	projects	are	individual	effort!)
#-------------------------------------------------------------------------------
#	Comments	and assumptions:	A	note	to	the	grader	as	to	any	problems	or	
#	uncompleted	aspects	of	the	assignment,	as	well	as	any	assumptions	about	the
#	meaning	of	the	specification.
#-------------------------------------------------------------------------------
#	NOTE: width	of	source	code	should	be	<=80	characters	to	be	readable	on-screen.
#2345678901234567890123456789012345678901234567890123456789012345678901234567890
#							10								20								30								40								50								60								70								80
#-------------------------------------------------------------------------------
# TASK 0 (example)

# EXAMPLE: this function is implemented for you, to show 
# what a function definition looks like, and how the
# 'student' added four lines to complete the definition.

def add3(x, y, z):
	# at the end, we'll return whatever current value
	# that's in ans as our return value. It's often
	# useful to create the variable with a starting 
	# value and then update it later on with reassignments
	# as needed.
	ans = 0
	
	# make decisions and perform calculations using all the 
	# coding tricks you've learned so far. Since we're
	# writing a function, all our code is indented inside
	# the function to the same amount.
	
	# YOUR CODE GOES HERE. (Since it's an example, we've
	# already written "your code" - four lines).
	
	ans = x + y + z
		
	# make this the last line of your function definition,
	# so that the function sends whatever value ans has
	# as the output.
	return ans

# TRY IT OUT!
#  - After saving this file, open up a terminal to the same directory.
#  - use the python program to load this code for interactive use:
#     on mac:   python3 -i tempate2E.py
#     on pc:    python  -i tempate2E.py
#  
#  - At the >>> prompt (which lets you know that python is
#    ready for expressions), call this function:
#    >>> add3(1,2,3)
#    6
#    >>> add3(100,100,100)
#    300
#    
#  - that's all there is to it! Use the same process on the next
#    tasks, which you'll be implementing yourself.


#-------------------------------------------------------------------------------

# TASK 1

# this function accepts a quantity of feet and a quantity of inches that describes something's full height; we want to combine them into a single
# answer of how many inches tall the thing is (where the answer can of
# course be much larger than 12).
# 
# assume num_feet and num_inches are both integers, that num_inches is
# from 0-11, and that num_feet isn't negative.

# Take in and store value in inch_feet
def inch_height (num_feet, num_inches):
	
	# let's start a variable for our answer, with some default value.
	
	# convert num_feet to inches unit
	temp = num_feet*12
	
	# now, do any calculations you need to get to the answer.
	
	# Take the sum of temp and num_inches to get full height in inches.
	ans = temp + num_inches
	
	# lastly, we return the answer.
	return ans	


#-------------------------------------------------------------------------------

# TASK 2

# there are two parameters (inputs): 
#  - price_per_gallon, a non-negative float number indicating how much a single
#                      gallon of gasoline costs
#  - num_gallons, a non-negative float number indicating how many gallons of gas
#                      we are purchasing
# 
# Calculate how much that amount of gas will cost at that price.

# Take in price per gallon and number of gallons then store them in gas_cost
def gas_cost(price_per_gallon, num_gallons):
	
	# we will return this variable at the end; let's start it at zero so we
	# can create it.
	cost = 0
	
	# add code here that assigns the correct value to cost.
	
	# The cost is the product of price and number of gallon
	cost = price_per_gallon * num_gallons
	
	# now we return the answer.
	return cost


#-------------------------------------------------------------------------------