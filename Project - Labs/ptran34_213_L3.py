#-------------------------------------------------------------------------------
#	Name:	Phuong Tran
#	G#: G01082824
#	Lab 3
#	Due	Date:	09/17/2018
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

def is_even(n):
	# at the end, we'll return whatever current value
	# that's in ans as our return value. Somewhere in 
	# this function, you should re-assign it to be
	# either True or to False.
	ans = None
	
	# make decisions with if-else structures to determine
	# whether n is even (divisible by two) or not. Then,
	# set ans to equal True or equal False as your answer.
	
	# YOUR CODE GOES HERE. (Since it's an example, we've
	# already written "your code" - four lines).
	
	if n % 2 == 0 :
		ans = True
	else:
		ans = False
	
	# make this the last line of your function definition
	return ans

#-------------------------------------------------------------------------------

# TASK 1

# given a non-negative integer, this function returns a
# string (it does not print!) matching the letter grade
# for our class (check the syllabus).

# Declare function "letter_grade" which take in 1 argument.
def letter_grade(score):
	
	# Initialize 'ans'
	ans = ''
	
	# Check condition if score is or below 59.
	if score <= 59:
		ans = 'F'
	
	# Check condition if score is between 59 and 70.
	elif score > 59 and score < 70:
		ans = 'D'
	
	# Check condition if score is between 70 and 72.
	elif score >= 70 and score < 72:
		ans = 'C-'
	
	# Check condition if score is between 72 and 78.
	elif score >= 72 and score < 78:
		ans = 'C'
	
	# Check condition if score is between 78 and 80.
	elif score >= 78 and score < 80:
		ans = 'C+'
	
	# Check condition if score is between 80 and 82.
	elif score >= 80 and score < 82:
		ans = 'B-'
	
	# Check condition if score is between 82 and 88.
	elif score >= 82 and score < 88:
		ans = 'B'
		
	# Check condition if score is between 88 and 90.
	elif score >= 88 and score < 90:
		ans = 'B+'
		
	# Check condition if score is between 90 and 92.
	elif score >= 90 and score < 92:
		ans = 'A-'
		
	# Check condition if score is between 92 and 98.
	elif score >= 92 and score < 98:
		ans = 'A'
	
	# Check other conditions in which not listed above.
	else:
		ans = 'A+'
	
	# Finally, return answer
	return ans

#-------------------------------------------------------------------------------

# TASK 2

# without calling the max(), min(), or any sorting functionality,
# this function determines the two largest values of the three 
# and returns their sum. The integers might be negative. When
# there's a tie between two numbers, it doesn't actually matter
# which one you choose.

# Declare function 'sum2biggest' which take in 3 arguments.
def sum2biggest(a, b, c):
	
	# starting value for variable ans. Replace it with the
	# actual answer integer before reaching the return stmt.
	
	# Initialize 'total' equal to sum of 3 integer
	total = a + b + c
	
	# Assigned min equal to a
	min = a
	
	
	# find the sum of the two largest values. Re-assign the
	# answer to the ans variable.
	# YOUR CODE GOES HERE
	
	# Find the smallest
	# Check condition if min is greater than b then replace min with b
	if min > b:
		min = b
	# Check condition if min is greater than c then replace min with c
	if min > c:
		min = c
	
	# Subtract min from total to get sum of the 2 biggest number
	total = total - min

	# Finally, return total of sum of 2 biggest
	return total

#-------------------------------------------------------------------------------

	