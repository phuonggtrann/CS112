#-------------------------------------------------------------------------------
# Name: Phuong Tran
# G#: G01082824
# Lab 5
# Due Date: 10/01/2018
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

#--------------------------------------------------------------------------------

# Task 1:
# Given a list
# If item in that list equal to key then return index of that item
# Other return none

# Create a function that take in 2 arguments
def location(xs, key):
	# Initialize variable
	index = 0
	
	# Create a loop to check every item in that list
	for x in xs:
		# Condition if x is equal to key, end loop and return index of x
		if x == key:
			break
		# Condition if x is not equal to key, increase index by 1 and continue the loop
		else:
			index +=1
	# If there is no value that match key then return None
	else:
		index = None
	# Finally, return index of xs
	return index
			
#--------------------------------------------------------------------------------	

# Task 2:
# Given an index and return the index in fibonacci's sequence

# Create a function and take in 1 argument
def fibonacci(n):
	# Initialize variables
	x=0
	ans = 0
	# Create a list to store sequences in. 
	# Store 1,1 in first since it is the beginning numbers of fibonacci's sequence
	fibs = [1,1]
	
	# While loop is use to find the sum of 2 previous two
	while x<n:
		# Add new numbers to the list
		fibs.append(fibs[x]+fibs[x+1])
		# x variable is increase by 1 each loop
		x+=1
	# For loop is used to check every item in fibs[] list
	for y in range(len(fibs)):
		# Condition: compare if y is equal to the given number
		if y==n:
			# Assign ans to the value at index y then end the loop (break)
			ans = fibs[y]
			break
	# Finally, return value of given index
	return ans

#--------------------------------------------------------------------------------

# Task 3:
# Given a positive integer
# Return integer whose isn't bigger than given integer

# Create a function and take in 1 argument
def int_sqrt(n):
	# Initialize needed variable
    a = 0
	# Use while loop and run until a square is less than or equal given number n
    while a * a <= n:
    	# If a square is still less than or equal, a is increase by 1
        a += 1
    # Finally, return a
    return a - 1

#--------------------------------------------------------------------------------
 # Task 4:
 # Given list of intetgers
 # Return the sum of all even numbers

# Create a function and take in 1 arguments
def sum_evens_2d(xss):
	# Initialize variable
	total = 0
	# Use for loop to check every item in given list
	for x in xss:
		# If it is list inside a list then check every item inside that nested list
		# by using another for loop
		if type(x) == list:
			for y in x:
				# Checking if that number is even then add it to total
				if y % 2 == 0:
					total += y
		# If not then add 1 to x and continue the loop
		else:
			total += x
	# Finally, return the total
	return total

