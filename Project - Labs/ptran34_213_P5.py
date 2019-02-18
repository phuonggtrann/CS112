# Name: PHUONG TRAN
# G#: G01082824
# Project 5
# Due Date: 11/11/2018
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

def read_votes(filename):
    db1={} # Create empty dictionary
    # Check filename's format
    if filename[len(filename)-3:len(filename)] != 'csv':
        return False # Return False if filename is not csv file
    else:
        votes = open(filename)
        votes_data = votes.read()
        votes.close() # Close after finish
        votes_data = votes_data.split('\n') # Make a list after txt file is transfer to string
        votes_data = votes_data[1:-1] # Don't take title and the last '\n'
        for line in range(len(votes_data)):
            temp = votes_data[line].split(',') # split each candidate by ','
            votes_data[line] = temp # Then modified the new list at modified-index
        for x in votes_data:
            if x[0] not in db1: # If that state is not a key in db dict
                db1[x[0]]=[] # Create a new key who value is a list
            else:
                continue
        for y in votes_data:
            if int(y[3])>=0 and int(y[4])>=0: # popular and electoral vote can't be negative number
                candidate = (y[1],y[2], int(y[3]), int(y[4])) # Create a tuple for each candidate
                if len(db1[y[0]])<1: # If the value for that state is empty then just add them in
                    db1[y[0]].append(candidate)
                else:
                    for compare in range(len(db1[y[0]])):
                        if y[1]<db1[y[0]][compare][0]: # Compare name to sort it alphabetically
                            db1[y[0]].insert(compare, candidate)
                            break
                        # If the compare name is bigger than other -> add them in the last index of the list
                        elif y[1] > db1[y[0]][compare][0] and compare ==len(db1[y[0]])-1:
                            db1[y[0]].append(candidate)
        return db1 # Finally, return database dictionaryr

def write_votes(db, filename):
    # Return False if wrong filename format or empty dictionary
    if filename[len(filename)-3:len(filename)] != 'csv': # Check if the file name is in correct format
        return False
    if len(db)<1: # Check if the given db is not empty
        return False
    else:
        temp_str=None # Initialize needed variable
        votes = open(filename, mode='w')
        for state in db:
            for cand in db[state]:
                temp_str ='' # reset temp str after finish writing 1 candidate
                temp_str = state +','+cand[0]+','+cand[1]+','+str(cand[2])+','+str(cand[3])+'\n'
                votes.write(temp_str)
        votes.close() # Close after finish
        return True # Return true for succeed

def read_abbreviations(filename):
    db2={} # Create empty dictionary
    if filename[len(filename)-3:len(filename)] != 'csv': # Check if the filename format is correct
        return False # if not return False
    else:
        abb = open(filename, mode='r', encoding='utf-8') # .csv file open
        abb_data = abb.read() # Read through all of the csv file
        abb.close() # Close afterrr done using
        abb_data = abb_data.split('\n') # Split by newline and return a list
        abb_data = abb_data[1:-1] # Don't take the title and the last newline ('')
        for line in range(len(abb_data)):
            temp = abb_data[line].split(',') # Split the candidate again into list (nested big list)
            abb_data[line] = temp # Modified the big list after splitting
        for x in abb_data:
            db2[x[0]]=x[1] # Create key-value pair and add them to the dictionaryr
    return db2 # Finally, return the dictionary

def add_candidate(db, state, name, party, popular_votes, electoral_votes):
    candidate_tuple= (name, party,popular_votes,electoral_votes) # Tuple format for candidate
    if state in db: # if the state is in given db
        candidate=[]
        state_cand = db[state] # list of tuple of candidates in given states
        for x in state_cand:
            candidate.append(x[0]) # add candidate name in given list
        if name in candidate: # if candidate is already in that state
            for cand_info in range(len(state_cand)):
                if state_cand[cand_info][0]==name:
                    (db[state])[cand_info]= candidate_tuple # Update the candidate's information
        else: # If the candidate doesn't exist in given state
            for compare_cand in range(len(state_cand)):
                # Add the candidate in with given information and in alphabetical order
                if name < state_cand[compare_cand][0]:
                    db[state].insert(compare_cand,candidate_tuple)
                    break
                elif name > state_cand[compare_cand][0] and compare_cand == len(state_cand)-1:
                    db[state].append(candidate_tuple)
                    break # Add the candidate's information only one time then immediately leave the loop
    else: # If the given state is not in given dict
        db[state]=[candidate_tuple] # Create new key-pair value
    return None

def remove_candidate(db, name, state=None):
    if state==None: # if state is not giving
        for pair in db.items():#db.value() is the outer list # pair = (key, val[()])
            # Remove that candidate in every state
            for cand_name in pair[1]: # val = [(name, info),]
                if cand_name[0]==name:
                    db[pair[0]].remove(cand_name)
    # If state is given and state has to be in given db
    if state != None:
        if state in db:
            for cand2 in db[state]:
                if cand2[0] == name:
                    db[state].remove(cand2) # Remove that candidate in given state
        else:
            return False # If state is not in db, return False
    # Removing state point to empty list
    dbc=db.copy() # Make a copy of given dict so that len(dict) doesn't change during iteration
    for check_len in dbc.items():
        if len(db[check_len[0]]) < 1: # If the value of that key is empty then delete that key-value pair
            del db[check_len[0]]
    return None

def incorporate_precinct(db, name, state, popular_votes_increment): # popular_vote's index = 2
    popular_vote=None
    # If state is exist
    if state in db:
        state_cand=[]
        # List of candidate's names
        for candidate in db[state]:
            state_cand.append(candidate[0])
        if name in state_cand: # If that candidate is in given state
            for cand in range(len(db[state])):
                if (db[state])[cand][0]==name:
                    # Calculate new popular vote after increment
                    popular_vote= (db[state])[cand][2]+popular_votes_increment
                    if popular_vote > 0: # Popular vote can't be negative
                        (db[state])[cand]= (name,(db[state])[cand][1], popular_vote, (db[state])[cand][3])
                        break # Modified the tuple of that candidate
                    else: # If the popular vote turn out to be false
                        db[state].pop(cand) # delete that tuple
                        break # Leave the loop immediately after delete
    # If name is not in that state or state is not in that dict
        else:
            return False
    else:
        return False
    # a state can't point to empty list
    if len(db[state])==0:
        del db[state] # Delete key-pair value if the key's value is empty
    return None

def merge_votes(db, name1, name2, new_name, new_party, state=None):
    combine_candidate =[]
    new_popular = 0
    new_electoral = 0
    # If state is given
    if state != None:
        # Finding 2 candidates
        for cand in db[state]:
            if cand[0] == name1 or cand[0]==name2:
                combine_candidate.append(cand) # Add the given candidate's tuple in list if they're in that state
        # Delete old candidate info in given state
        if len(combine_candidate)>=1:
            for y in combine_candidate:
                db[state].remove(y)
                # Calculate new popular and electoral votes
                new_popular += y[2]
                new_electoral += y[3]
            # Update new tuple for merge candidate
            new_candidate = (new_name, new_party, new_popular, new_electoral)
            # Add new combine information in
            if len(db[state])>=1:
                for compare_cand in range(len(db[state])):
                    # comparison is done for alphabetical check
                    if new_name < (db[state])[compare_cand][0]:
                        db[state].insert(compare_cand, new_candidate)
                        break # Add only 1 time
                    # If the adding name is bigger than everything then append it into the last index
                    elif new_name > (db[state])[compare_cand][0] and compare_cand == len(db[state]) - 1:
                        db[state].append(new_candidate)
            else: # if that state's value is empty
                db[state].append(new_candidate)
    # If state is not given, the logic an coding is basically the same
    else:
        for a in db:
            # Refresh list after going over 1 state (key) in db dictionary
            new_popular = 0
            new_electoral = 0
            combine_candidate =[]
            for cand in db[a]:
                if cand[0] == name1 or cand[0] == name2:
                    combine_candidate.append(cand)
            # Delete old candidate info in given state
            if len(combine_candidate) >= 1:
                for y in combine_candidate:
                    db[a].remove(y)
                    new_popular += y[2]
                    new_electoral += y[3]
                new_candidate = (new_name, new_party, new_popular, new_electoral)
                # Add new combine information in
                if len(db[a])>=1:
                    for compare_cand in range(len(db[a])):
                        if new_name < (db[a])[compare_cand][0]:
                            db[a].insert(compare_cand, new_candidate)
                            break
                        elif new_name > (db[a])[compare_cand][0] and compare_cand == len(db[a]) - 1:
                            db[a].append(new_candidate)
                else: # if key's value is an empty list
                    db[a].append(new_candidate)
    return None

def number_of_votes(db, name, category='popular',numbering='tally', state=None):
    # The optional argument need to be correct spelling
    if (category == 'popular' or category == 'electoral') and (numbering == 'tally' or numbering == 'percent'):
        candidate_total = 0
        total_vote = 0
        state_candidate = []
        # If state is given
        if state != None:
            if state in db:
                for cand in db[state]:
                    state_candidate.append(cand[0]) # Store candidate name of that state in a list
                    # calculate the total vote of that candidate as well as total vote of the whole state
                    if category == 'popular':
                        total_vote += cand[2]
                        if cand[0] == name:
                            candidate_total += cand[2]
                    if category == 'electoral':
                        total_vote += cand[3]
                        if cand[0] == name:
                            candidate_total += cand[3]
                # If candidate is not in that state, return false
                if name not in state_candidate:
                    return False
            # If state is not in dictionary, return false
            else:
                return False
        # if state is not given, go through every state and take the total the same as above
        if state == None:
            for a in db:
                for cand in db[a]:
                    if category == 'popular':
                        total_vote += cand[2]
                        if cand[0] == name:
                            candidate_total += cand[2]
                    if category == 'electoral':
                        total_vote += cand[3]
                        if cand[0] == name:
                            candidate_total += cand[3]
        # if optional argument is percent then candidate/total *100
        if numbering == 'percent':
            candidate_total = (candidate_total / total_vote) * 100
            return round(candidate_total, 2)
        # if optional argument is tally then return candidate total
        if numbering == 'tally':
            return candidate_total
    else: # if the argument is wrong spelling
        return False

def popular_votes_performance(db, name,numbering, order='max'):
    # if optional argument is wrong spelling
    if order != 'max' and order != 'min':
        return False
    else: # if not wrong spelling
        temp=None
        state_name = ''
        order_data=[]
        for a in db:
            # call in function to calculate the popular votes
            if number_of_votes(db, name, 'popular', numbering, a) == False:
                continue
            else:
                temp= number_of_votes(db,name, 'popular', numbering,a) # calculate the number of votes
                order_data.append([a,temp]) # add it into a list with state (type=tuple)
        if len(order_data)<1: # no candidate found
            return False
        else:
            # compare the data
            big_small = order_data[0][1]
            for a in order_data:
                if order=='max':
                    if a[1]>big_small:
                        big_small=a[1]
                        state_name=a[0]
                if order=='min':
                    if a[1]<big_small:
                        big_small=a[1]
                        state_name=a[0]
            # Call in function to find full name and return full name found
            if state_name in read_abbreviations('abbreviations.csv'):
                return read_abbreviations('abbreviations.csv')[state_name]
            else: # if there is no full name found return False
                return False

def candidates_difference(db, name1, name2, order='smallest'):
    # if optional argument is wrong spelling
    if order != 'smallest' and order!='largest':
        return False
    else:
        cand1=None
        cand2=None
        order_data=[]
        different = 0
        dif_state= ''
        for a in db:
            state_candidate = [] # Refresh list after each state
            for name in db[a]:
                state_candidate.append(name[0])
            if name1 in state_candidate and name2 in state_candidate:
                # call in function to calculate popupar vote percent of 2 candidates
                cand1= number_of_votes(db, name1, 'popular', 'percent', a)
                cand2= number_of_votes(db, name2, 'popular', 'percent', a)
                different = abs(cand1-cand2) # calculate the different
                order_data.append((a,different)) # Add the difference of that state into a list
        if len(order_data)<1: # If the list is empty return False
            return False
        else:
            temp=order_data[0][1] # Initialize variable for temp
            for x in order_data:
                if order=='smallest': # Finding smallest
                    if x[1]<temp:
                        temp=x[1]
                        dif_state=x[0]
                if order=='largest': # Finding biggest
                    if x[1]>temp:
                        temp=x[1]
                        dif_state=x[0]
        # Call in function to find full name
        if dif_state in read_abbreviations('abbreviations.csv'):
            return read_abbreviations('abbreviations.csv')[dif_state]
        else:  # if full name not found, return Fale
            return False




