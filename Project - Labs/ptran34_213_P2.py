#-------------------------------------------------------------------------------
# Name: Phuong Tran
# G#: G01082824
# Project 2
# Due Date: 09/23/2018
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

# Declare function which take in 4 arguments
# to determine whether a person has discount
def discount(age, major, is_in_military, gpa):

	# Initialize disc equal to False (type: Boolean)
	disc = False

	# Conditions in which disc is true (elder and military citizen)
	if age >= 65 or is_in_military == True:
		disc = True

	# Condition that discount is exclusive for Computer Science
	# that has gpa of 3.5 or higher
	elif major == 'Computer Science' and gpa >= 3.5:
		disc = True

	# other conditions that is not listed above
	else:
		disc = False

	# Return answer type Boolean
	return disc

# Declare another function that calculate the cost for each plan without discount
# Take in 3 arguments
def calculate_cost(plan, num_minutes, num_text):

	# Initialize cost
	cost = 0
	
	# Assign cost if the plan is 'basic'
	if plan =="basic":
		cost = 15.0

		# If the number of minutes for basic plan is exceed
		if num_minutes > 100:
			cost = cost + (num_minutes - 100)*1.50

		# If the number of texts for basic plan is exceed
		if num_text > 1000:
			cost = cost + (num_text - 1000)*0.75
	
	# Assign cost if plan is 'standard'
	if plan == 'standard':
		cost = 20.0

		# If the number of minutes for standard plan is exceed
		if num_minutes > 175:
			cost = cost + (num_minutes - 175)*1.25

		# If the number of texts for standard plan is exceed
		if num_text > 1500:
			cost = cost + (num_text - 1500)*0.5
	
	# Assign cost if plan is 'premium'
	if plan == 'premium':
		cost = 25.0

		# If the number of minutes for premium plan is exceed
		if num_minutes >250:
			cost = cost + (num_minutes - 250)*1

		# If the number of texts for premium plan is exceed
		if num_text > 2000:
			cost = cost + (num_text - 2000)*0.25

	# Return cost for chosen plan (type: Float)
	return float(cost)

# Declare a function to determine the most efficient plan
# Take in 5 arguments
def cost_efficient_plan(age, major, is_in_military, gpa, num_minutes, num_text):
	
	# Initialize needed variable
	plan_eff = ''
	cost_b = 0
	cost_s = 0
	cost_p = 0

	# Find the cost for specific plan by calling in calculate_cost() function

	# Find cost for basic plan
	# The cost for basic plan with discount
	if discount(age, major, is_in_military, gpa) == True:
		cost_b = (calculate_cost('basic', num_minutes, num_text))*0.80

	# The cost for basic plan without discount
	else:
		cost_b = calculate_cost('basic', num_minutes, num_text)
	
	# Find cost for standard plan
	cost_s = calculate_cost('standard', num_minutes, num_text)
	
	#Find cost for premium plan
	cost_p = calculate_cost('premium', num_minutes, num_text) 
		
	# Find the min
	# Initialize min equal to cost for basic plan
	min = cost_b

	# Condition in which min is replaced with 1 of 2 other variables
	if min > cost_s:
		min = cost_s
	if min > cost_p:
		min = cost_p

	# Assign min to answer
	# Compare plan_eff with cost_b, cost_s, cost_p
	if min == cost_b:
		plan_eff = 'basic'
	if min == cost_s:
		plan_eff = 'standard'
	if min == cost_p:
		plan_eff = 'premium'

	# Return the answer (type: String)
	return plan_eff

def plan_range(num_minutes):
	
	# Initialize needed variable
	chart = ''
	i=0
	temp = ''

	# Condition if num_minutes is not an integer
	if type(num_minutes)!= int:
		chart = 'error'
		return chart

	# Condition if num_minutes is an integer but is not a non-negative number
	elif type(num_minutes) == int:
		if num_minutes <0:
			chart = 'error'
			return chart

		# Condition in which num_minutes is a positive integer
		# Assign chart with the first row of table-like chart
		else:
			chart ='Mins\tBasic\tStd\tPremium\n'

	# Setting up a loop to make the table-like chart
	# i run from 0-9 (10 times loop)
	while i<10:

		# i is increment by 1 every time the loop progress
		i=i+1

		# Convert all the variable to type string
		# Call in calculate_cost() function to recalculate the cost
		min_s = str(num_minutes)
		cost_bt = str(calculate_cost('basic', num_minutes, 1000) * 0.80)
		cost_st = str(calculate_cost('standard', num_minutes, 1000))
		cost_pt = str(calculate_cost('premium', num_minutes, 1000))
		# Stack of the chart to build up table-like chart
		# \t for tab, \n for new line (String literals)
		chart = chart + min_s +'\t$' + cost_bt +'\t$' + cost_st +'\t$' + cost_pt +'\n'
		# num_minutes is increment by 10 every time the loop progress
		num_minutes +=10

	# Return chart (type: String)
	return chart


