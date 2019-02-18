#-------------------------------------------------------------------------------
# Name: PHUONG TRAN
# G#: G01082824
# Project 4
# Due Date: 10/28/2018
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

# Create a function, take in 1 argument
def show(map):
    # Initialize needed variable
    ans = ''
    max = 0 # The biggest variable in lists of list
    temp =0 # Initial len of current check variable

    # Finding max
    for a in map:
        for b in a:
            if b>max:
                max = b
    len_max=len(str(max)) # Finding length of biggest variable

    # Adding answer string
    for x in map: # nested for loop because 2-dimension list
        for y in range(len(x)):
            temp = len(str(x[y])) # Updating len of the currently variable each loop
            while temp!=len_max: # Break if the len of current variable and max is balanced
                ans+=' ' # Adding space to balance the len between variables
                temp+=1 # Keep track of len of current variable
            if y == len(x)-1: # If variable locates in the last column then no space added
                ans += str(x[y]) +'\n'
            else: # Otherwise, add space
                ans += str(x[y]) +' '

    # Finally, return asnwer
    return ans

# Create a function and take in 1 2d list (map)
def highest_point(map):
    # Initialized needed variable
    row=0
    column=0
    max=0

    # Check every element in 2d list
    for x in range(len(map)):
        for y in range(len(map[0])):
            if map[x][y] > max: # Finding max
                max=map[x][y] # Update max
                column = y # Update column
                row = x # Update row
    if max == 0: # In case there is no land (0 = water)
        return None # Return answer if condition satisfied
    else:
        highest = (row, column) # Otherwise, return tuple
        return highest # Return answer if condition satisfied

# Create a function, take in 2d list and location (row and column)
def on_map(map, r, c):
    position = False # Set default answer (position) to false
    if r >= 0 or c >= 0: # No negative r,c allowed
        if len(map)-1 >= r and len(map[0])-1 >= c: # Have to be in map range
            position = True # If satisfied all above condition then answer is true
    # Finally, return answer
    return position

# Create a function, take in 2d list and location (row and column)
def is_map(map):
    meet_criteria = True # Set default answer to be true

    # Conditions that make the answer false
    if len(map)==0: # in case there is nothing in the list
        meet_criteria = False # Assigned false to answer
    if len(map)>0: # if there is a 2d list
        for a in map: # Check each row
            if len(a) != len(map[0]): # 2d list has to be same length
                meet_criteria = False
            else:
                for b in a:
                    if type(b)!= int: # has to be in type int
                        meet_criteria = False
                    elif b<0: # Can't be negative
                        meet_criteria = False

    # Finally, return the answer
    return meet_criteria

# Create a function, take in 2d list and location (row and column)
def neighbors(map, r, c):
    neighbor=[] # Create empty list
    for a in range(r-1,r+2): # r-1 and r+2 b/c in neighbor range of given location
        for b in range(c-1,c+2): # Same as above
            if a!=r or b!=c: # not append the given location
                if 0<=a<=(len(map)-1): # Make sure it's still in index range
                    if 0<=b<=(len(map[0])-1): # Same as above
                        neighbor.append((a,b)) # Add a tuple to created list
    # Finally, return answer
    return neighbor

# Create a function, take in 2d list and location (row and column)
def water_adjacent(map, r,c):
    near_water = on_map(map,r,c) # Check if the given location is on given map
    if near_water : # if true
        for a in neighbors(map,r,c): # call in neighbor function, check each tuple
            if map[a[0]][a[1]]==0: # If there is a water spot
                near_water=True # answer is true
                break # no futher check needed
            else:
                near_water=False # if there is no water spot, return false
    # Finally, return asnwer
    return near_water

# Create a function, take in 2d list
def count_coastline(map):
    count = 0 # Initialize needed variable

    for r in range(len(map)):
        for c in range(len(map[0])):
            if map[r][c]!=0: # the check spot has to be land
                if water_adjacent(map,r,c): # if neighbor of current spot is water
                    count+=1 # Increase count by 1
    # finally, return answer
    return count

# Create a function, take in 2d list and location (row and column)
def on_ridge(map, r, c):
    qualified_neighbor = [] # create empty list
    ridge = on_map(map,r,c) # ridge is the value (type bool) of call in func on_map

    if ridge: # if given location is on given map
        for a in neighbors(map,r,c):
            # in case the check spot is land and lower than given spot
            if map[a[0]][a[1]]!=0 and map[a[0]][a[1]]<map[r][c]:
                qualified_neighbor.append(a) # add it to created string
        if len(qualified_neighbor)<2: # if there is only 1 qualified neighbor,
            ridge=False # no further check needed
        else:
            for x in qualified_neighbor: # check tuple with other tuples in same list
                for y in qualified_neighbor:
                    if abs(x[1]-y[1])==2: # Horizontal and Diagonal check
                        if x[0]==y[0]  or abs(x[0]-y[0])==2: #Horizontal - Diagonal check
                            ridge= True
                            break # no further check needed
                    if abs(x[0]-y[0])==2 and x[1]==y[1]: # Vertical check
                        ridge= True
                        break
                    else: # in other situation, remain false
                        ridge=False
    # Finally, return answer
    return ridge

# Create a function, take in 2d list and location (row and column)
def is_peak(map, r ,c):
    peak = on_map(map,r,c) # Check if the given location is on given map
    if peak: # if peak is true
        for a in neighbors(map,r,c): # check every tuple in call in neighbors func
            if map[a[0]][a[1]]>= map[r][c]: # if neighbor land is not lower
                peak=False # assign peak with false
                break # no further check needed
    # Finally, return answer
    return peak

# Create a function, take in two 2d list
def join_map_side(map1, map2):
    join_side = [] # create empty list
    if len(map1)!= len(map2): # if length of the 2 map is not equal
        return None # return none
    else: # otherwise
        for a in range(len(map1)):
            # adding list to complete answer
            join_side.append(map1[a]+map2[a]) # Add each element of 2 lists together
        # Finally, return answer
        return join_side

# Create a function, take in two 2d list
def join_map_below(map1, map2):
    join_below=[] # create empty list (answer list)
    temp=[] # Create another empty list
    if len(map1[0])!= len(map2[0]): # if the length of given maps isn't euqal
        return None # return nothing
    else: # otherwise
        # Check and add every element in the first map into temporary list
        for a in map1:
            for b in a:
                temp.append(b)
        # Check and add every element in the second map into temporary list
        for x in map2:
            for y in x:
                temp.append(y)
        # Slicing it out and add it to the answer list
        for c in range(0, len(temp),len(map1[0])):
            join_below.append(temp[c:c+len(map1[0])])
        # Finally, return the answer list
        return join_below

# Create a function, take in 2d list and 2 positions
def crop(map, r1, c1, r2, c2):
    map_crop=[] # Create an empty list

    if  r1>r2 or c1>c2: # in case 2nd position bigger than 1st position
        return map_crop # return empty list
    else: # otherwise
        for x in range(r1,r2+1):
            if x>len(map)-1: # Out of row's index case
                break
            if r2>len(map[0])-1: # Out of column's index case
                # crop from 1st given col to the last col
                map_crop.append(map[x][c1:len(map[0])]) # Add the list to answer list
            if r2<=len(map[0])-1: # if not
                # crop from 1st given col to the 2nd given col
                map_crop.append(map[x][c1:c2+1]) # Add the list to answer list
    # Finally, return answer list
    return map_crop

# Create a function, take in 2d list and a non-negative int
def flooded_map(map, rise):
    # Create 2 empty list, answer list and temporary list
    temp = []
    after_flooded = []
    # Check every element in 2d map (nested for loops)
    for a in map:
        for b in a:
            if b <= rise: # if b isn't taller than water rise
                temp.append(0) # add b to temporary list
            else: # if b is taller then water rise
                temp.append(b - rise) # add the difference of b and water rise to temp list
    for b in range(0, len(temp), len(map[0])):# len(temp) b/c include last value of temp list
                                              # len(map[0]) b/c answer list need to have same row and column
        # Add list to the answer list
        after_flooded.append(temp[b:b + len(map[0])]) # use slicing to set up 2d list
    # Finally, return the answer list
    return after_flooded

# Create a function, take in 2d list and a non-negative int
def flood_map(map, rise):
    for a in map:
        for b in range(len(a)): # Range b/c i want to use index
            if a[b]<=rise: # if that spot isn't taller than water rise
                a[b]=0 # Change the value of that spot to 0
            else: # otherwise
                a[b]-=rise # Change value of that spot to difference of value of that spot and water rise value
    # Since original list is modified, return nothing
    return None

# Create a function, take in 2d list, a location (r,c) and a direction string
def find_land(map, r, c, dir):
    step=0 # Initialize needed variable
    while on_map(map,r,c): # The current spot has to be on map
        if map[r][c] != 0: # Until we are on land
            return step # return number of steps
        else: # if current spot is water
            step+=1
        # Checking direction and increase row or column by 1 depend on given direction
        if 'S' in dir:
            r+=1
        if 'N' in dir:
            r-=1
        if 'W' in dir:
            c-=1
        if 'E' in dir:
            c+=1

# Create a function, take in 2d list
def reorient(map):
    # create 2 empty lists
    new_reo = []
    temp = []
    # Using range() because index will be used
    for x in range(len(map[0])):
        for y in range(len(map)):
            # Add that value to temp list
            temp.append(map[(len(map) - 1) - y][x]) # Checking from last index of y
    for a in range(0, len(temp), len(map)): # column will be row and row will be column
        new_reo.append(temp[a:a + len(map)]) # Use slicing to set up new 2d list
    # Finally, return the answer list
    return new_reo

# Extra credit
# Create a function, take in 2d list and location (row and column)
def get_island_spots(map,r,c):
    temp=[(r,c)] # Create an temporary list with tuple (r,c)
    answer=[] # Create an empty answer list
    while len(temp)>0: # while the temp list isn't empty
        for a in temp: # Check every element in the temp list
            temp.remove(a) # remove that element after checking
            if map[a[0]][a[1]]!=0 and a not in answer:
                answer.append(a) # Add it to the answer list if it's not yet in answer list
                temp.extend(neighbors(map,a[0],a[1])) # Add neighbor of reomoved spot to continue checking
    # Sort the answer
    answer.sort()
    # Finally, erturn the answer list
    return answer

# Create a function, take in 2d list and  2 location
def connected_spots(map, r1, c1, r2, c2):
    # Call in function get_island_spots with starting point at (r1,c1)
    # # in case the (r2,c2) is in get_island_spots list
    if (r2,c2) in get_island_spots(map, r1, c1):
        return True # return true
    else:
        return False # if not then return false

# Create a function, take in 2d list and a location
def remove_island(map, r, c):
    # Check every 'connected' element in get_island_spots
    for x in get_island_spots(map,r,c):
        map[x[0]][x[1]]=0 # Change the value to 0
    # The map is modified so no return is needed (return none)
    return None


