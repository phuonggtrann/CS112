#-------------------------------------------------------------------------------
# Name: PHUONG TRAN
# G#: G01082824
# Project 3
# Due Date: 10/07/2018
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

# Given positive integer
# Return sum of positive integer

# Create a function that take 1 argument
def sum_divisors(n):
    # since n is a divisor for itself, initialize total equal to n
    total = n
    # Check every integer between 1 to n
    for x in range(1,n):
        # if n is divisible to that number, add that number to total
        if n % x == 0:
            total+=x
    # Finally, return total
    return total

# Given the precision
# Return the pi number according to the precision

# Create a function that take in 1 argument
def pi(precision):
    # Since 4 is the first variable in pi, assign 4 to y
    y= 4
    # Initialize other needed variable
    total=0
    x=0
    # In ccondition which the precision is equal or bigger the first variable in pi
    if precision >= y:
        total = y
    # While loop since i don't know how many time it will loop through
    # Absolute to find the positive value of y
    while abs(y)>=precision:
        # Leibniz formula
        y = (4*((-1)**x))/(2*x+1)
        total +=y
        # x is increment by 1 to calculate the next variable using Leibniz formula
        x +=1
    # Finally, return the total
    return total

# Given a list of number
# Return the difference between min and max

# Create a function that take in 1 argument
def span(nums):
    # In case there is no value in given list
    if len(nums) == 0:
        ans = 0
        return ans

    # Finding the smallest
    # Assign small to the first item in the list then loop through
    # Small will change if smaller number detected
    small = nums[0]
    for x in nums:
        if small > x:
            small = x

    # Finding the biggest
    # Assign big to the first item in the list then loop through
    # Big will change if bigger number detected
    big = nums[0]
    for y in nums:
        if big < y:
            big = y
    # Find the differentiation between big and small
    ans = big - small
    # Finally, return the answer
    return ans

# Given a list of number
# Return neighboring value

# Create a function that take in 1 argument
def single_steps(nums):
    # Initialize variable
    count = 0
    # If there is no item in given list
    if len(nums) == 0:
        return count
    # For loop to check every element in the list
    # len(num)-1 because we don't need to check neighbor for the last element.
    # Already check in the previous element
    for x in range(len(nums)-1):
        # Check if that element and the element next to it is neighbor
        if abs(nums[x] - nums[x+1]) == 1:
            # If yes then +1
            count +=1
    # Finally, return the answer
    return count

# Given a list of value
# Return a copy but echo removes

# Create a function that take in 1 argument
def remove_echo(xs):
    # If there is no item in given list
    if len(xs) == 0:
        # Return the answer immediately
        return xs
    # Create a new list and store the first item in given list in
    # Assign temp with the first element in given list
    new_xs = [xs[0]]
    temp = xs[0]
    # For loop to check every element in the loop
    for x in xs:
        # If the item is not echo
        # Add item to new list and reassign temp with new item
        if x != temp:
            new_xs.append(x)
            temp = x
    # Finally, return answer
    return new_xs

# Given a list of numbers
# Return product of even numbers

# Create a function that take in 1 argument
def even_product_2d(grid):
    # Initialize variable
    product = 1
    # For loop to check every element in given list
    for x in grid:
        # Because list is nested list -> use another for loop to check the nested list
        for y in x:
            # Check if y is even
            if y%2 ==0:
                # If yes, multiply it with product
                product *=y
    # Finally, return product as answer
    return product

# Extra credit
# Given 2d grid
# Return number of isolated cells

# Creat a function that take in 1 argument
def count_isolated(grid):
    # Initialize variable
    count = 0
    count_temp = 0
    # Create ind=[] to store index of not_empty characters
    ind = []
    # Create not_empty to store not_empty characters
    not_empty = []
    # For loop to check every item in given list
    for x in grid:
        # Use another loop because it's nested list
        for y in x:
            # Check if item is not empty
            if y != '.':
                # if that char is unique
                if x.count(y) == 1:
                    not_empty.append(y) # Store that character in not_empty=[]
                    # Store character'index in ind=[]
                    ind.append(grid.index(x))  # index of x in grid (row)
                    ind.append(x.index(y))  # index of y in x in grid (column)
                if x.count(y) > 1: # If there is more than 1 identified character
                    not_empty.append(y) # Store the character in not_temp=[]
                    # Store character'index in ind=[]
                    ind.append(grid.index(x)) # index of x in grid (row)
                    ind.append(x.index(y)) # index of y in x in grid (column)
                    x[x.index(y)] = ' '
    # If there are all empty cells
    if len(not_empty) == 0:
        return 0
    # if there is only 1 characters, then it's automatically isolated
    if len(not_empty) == 1:
        return 1
    # If there is more than 1 characters
    if len(not_empty) >= 2:
        # Check the index of that character to ALL other character's index
        for a in range(0, len(ind), 2):
            # Refresh count_temp
            # after finish checking 1 character with all other characters in not_empty[]
            count_temp = 0
            # Rance increase by 2 because a characters has 2 index (column and row)
            for c in range(0, len(ind), 2):
                # If same row, check column's difference
                # a, c because I stored index of x first
                # a+1, c+1 because I stored index of y after index of x
                if ind[a]==ind[c] and abs(ind[a+1]-ind[c+1])>= 2: # horizontal check
                    count_temp += 1
                # Same column, check row's difference
                if ind[a+1]==ind[c+1] and abs(ind[a]-ind[c])>= 2: # vertical check
                    count_temp += 1
                # Different row, different column -> diagonal check
                if ind[a]!=ind[c] and ind[a+1]!=ind[c+1]:
                    if abs(ind[a+1]-ind[c+1])>= 2 or abs(ind[a]-ind[c])>= 2:
                        count_temp += 1
            # len(non_empty)-1 because
            # in order for that character to be isolated
            # it has to be isolated with all other characters, except itself
            if count_temp == len(not_empty) - 1:
                # If a character is isolated to all other characters
                # count's increased by 1
                count += 1
    # Finally, return the answer
    return count








