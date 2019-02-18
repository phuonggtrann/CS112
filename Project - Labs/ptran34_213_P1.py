#-------------------------------------------------------------------------------
# Name: PHUONG TRRAN
# G#: G01082824
# Project 1
# Due Date: 09/09/2018
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

# assumes the following prices: 
#   one Headless Hat: two galleons
#   one Boxing Telescope: 12 sickles and 26 knuts
#   one Canary Cream: seven sickles
# 
# Conversion rates:
#   1 galleon == 17 sickles
#   1 sickle  == 29 knuts
#
# assume all three parameters (num_hats, num_tels, num_creams) are
# non-negative integers.

# Take in number of hats, telescope and cream then store them in 'checkout'
def checkout(num_hats, num_tels, num_creams):
	# create more variables as needed!
	total = 0
	# calculating the price of hats in knuts.
	price_hats = num_hats*2*17*29
	# calculate the price of boxing telescopes in knuts.
	price_tels = num_tels*(12*29+26)
	#calculate the price of Canary Creams in knuts.
	price_creams = num_creams*7*29
	# calculate how many knuts to pay given the order, and return that amount.
	total = price_hats + price_tels + price_creams
	# if you did store your answer in ans, then this works:
	return total
# ------------------------------------------------------------------------------

# assume the minutes parameter is an non-negative integer.
# how many fortnights, days, hours, and minutes are included in that period?

# Take in minutes and store them in 'timing'
def timing(minutes):
	
	# calculating the number of minutes left.
	num_minutes = minutes%60
	
	# calculating the number of hours
	num_hours = (minutes//60)%24
	
	#calculating the number of days. (60*24 is conversion from minutes to day)
	num_days = (minutes//(60*24))%14 
	
	# calculating the number of fortnights.(60*24*4 is conversion from minutes to fortnights)
	num_fortnights = minutes//(60*24*14)
	
	# as always you can name your variables what you want, but
	# if you use these names, this return statement is what we need.
	
	# lastly, returning the answer
	return (num_fortnights, num_days, num_hours, num_minutes)

# ------------------------------------------------------------------------------

# Extra credit!

# assume dist and time are non-negative integers.
# assume k is a positive integer.

# Take in distance, time, k and store them in 'catch_bus'
def catch_bus(dist, time, k):

    # Calculating the velocity.
    if dist%time == 0: 
    	catch_vel = dist/time
    	
    # else = rounding velocity up to make it an integer 
    # Can't round down because will miss buss therefore +1 to round up
    else: catch_vel = (dist//time)+1
    
    # Making the velocity multiple of k. 
    # If k isn't divisible to k then +1 until catch_vel is the smalles division of k.
    while (catch_vel%k) !=0:
    	catch_vel +=1
   
    # else = when vel is divisible to k
    # lastly, return the answer
    else:
    	return catch_vel
  	
# ------------------------------------------------------------------------------