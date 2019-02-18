# Name: PHUONG TRAN
# G#: G01082824
# Project 6
# Due Date: 12/08/2018
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

###### The below comment is for all class objects in this project######
# __init__ is syntax constructor, same syntax for each class but different variables
# Most of the __str__() and __repr__() method is using string formatting.
# __eq__ method is base on syntax
# Exception class to catch raised error

class Line:
    def __init__(self, name, area_code, number, is_active=True):
        self.name = name
        self.area_code= area_code
        self.number = number
        self.is_active = is_active
    def __str__(self):
        return ('%d-%d(%s)'%(self.area_code, self.number,self.name))
    def __repr__(self):
        return ("{}('{}', {}, {})".format(self.__class__.__name__,self.name,self.area_code,self.number))
    def __eq__(self,other):
        if (self.area_code == other.area_code) and (self.number == other.number):
            return True
        else:
            return False
    # Activate the line
    def activate(self):
        self.is_active = True
    # Deactivate the line
    def deactivate(self):
        self.is_active = False

class Call:
    def __init__(self, caller, callee, length):
        self.caller = caller
        self.callee = callee
        self.length = length
        if self.callee.is_active == False and self.caller.is_active == False:
            raise CallError('line ' + self.caller.__str__()+' not active')
        elif self.callee.is_active == False:
            raise CallError('line ' + self.callee.__str__() + ' not active')
        elif self.caller.is_active == False:
            raise CallError('line' + self.caller.__str__() + ' not active')
        if self.callee.area_code == self.caller.area_code and self.callee.number == self.caller.number:
            raise CallError('line ' + self.caller.__str__() + ' cannot call itself')
        if self.length <0:
            raise CallError('negative call length: %d' % self.length)
    def __str__(self):
        return "{}({}, {}, {})".format(self.__class__.__name__,self.caller.__repr__(),self.callee.__repr__(),self.length)
    def __repr__(self):
        return self.__str__()
    # Check is the 2 phone line is local or not (type: boolean)
    def is_local(self):
        if self.callee.area_code == self.caller.area_code:
            return True
        else:
            return False

class CallError(Exception):
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return "{}: {}".format(self.__class__.__name__, self.msg)
    def __repr__(self):
        return "{}('{}')".format(self.__class__.__name__, self.msg)

class PhonePlanError(Exception):
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return "{}: {}".format(self.__class__.__name__, self.msg)
    def __repr__(self):
        return "{}('{}')".format(self.__class__.__name__, self.msg)

class PlanType:
    def __init__(self, basic_rate, default_mins, rate_per_min, has_rollover=True):
        self.basic_rate = basic_rate
        self.default_mins = default_mins
        self.rate_per_min = rate_per_min
        self.has_rollover = has_rollover
    def __str__(self):
        return "%s(%.2f, %d, %.2f, %s)"%(self.__class__.__name__,self.basic_rate,self.default_mins,self.rate_per_min,self.has_rollover)
    def __repr__(self):
        return self.__str__()

class PhonePlan:
    def __init__(self, type, lines=None):
        self.type = type
        if lines == None:
            self.lines = []
        else:
            self.lines = lines
        self.calls= []
        self.balance=0
        self.rollover_mins=0
        self.mins_to_pay=0
    def __str__(self):
        return "{}({}, {}, [])".format(self.__class__.__name__, self.type.__str__(), self.lines)
    def __repr__(self):
        return self.__str__()
    # Activate all the line in that plan
    def activate_all(self):
        for a in self.lines:
            a.is_active = True
    # Deactivate all the line in that plan
    def deactivate_all(self):
        for b in self.lines:
            b.is_active = False
    def add_call(self, call):
        # If caller and caller in the same line, mins_to_pay doesn't count
        if call.caller in self.lines and call.callee in self.lines:
            self.calls.append(call)
            self.mins_to_pay = 0
        # If one of caller or callee is in the plan, add call to the call list and update mins_to_pay
        elif call.caller in self.lines or call.callee in self.lines:
            self.calls.append(call)
            if not call.is_local():
                self.mins_to_pay += call.length
        # If both caller and callee is not in the plan, raise error
        else:
            raise PhonePlanError('call cannot be added')
        return None
    def remove_call(self, call):
        if call in self.calls: # if call in call list, remove the call
            self.calls.remove(call)
        else: # If call is not in call list, raise error
            raise PhonePlanError('no such call to remove')
        return None
    def add_calls(self, calls):
        count=0
        for a in calls:
            try:
                self.add_call(a) # If call is succesfully added to call list, increase count by 1
                count+=1
            except: # If not, do nothing (pass)
                pass
        return count
    def make_call(self, caller, callee, length):
        try:
            call= Call(caller, callee, length) # create object class Call
        except CallError: # raise error if object can't be created
            return False
        try:
            self.add_call(call) # Try adding the call into call list
        except PhonePlanError: # raise error if call can't be added
            return False
        else:
            return True
    def mins_by_line(self, line):
        minutes = 0
        if line in self.lines:
            for a in self.calls: # Check every call in the call list
                # If given line is a callee or caller, update minutes
                if Line.__eq__(line, a.callee) or Line.__eq__(line, a.caller):
                    minutes += a.length
            return minutes
        else: # If line not in lines list, return 0
            return minutes
    def calls_by_line(self, line):
        count = 0
        if line in self.lines:
            for a in self.calls: # Check every call in the call list
                # If given line is a callee or caller, update count by 1
                if Line.__eq__(line, a.callee) or Line.__eq__(line, a.caller):
                    count += 1
            return count
        else: # If line not in lines list, return 0
            return count
    def add_line(self, line):
        if line in self.lines: # If line not in lines list, raise error
            raise PhonePlanError('duplicated line to add')
        else: # If line in lines list, add line to line list
            self.lines.append(line)
    def remove_line(self,line):
        if line in self.lines:
            self.lines.remove(line)
            for a in self.calls[:]: # Only remove if one of caller/callee is not in line
                if Line.__eq__(line, a.callee) and a.caller not in self.lines:
                    self.calls.remove(a)
                elif Line.__eq__(line, a.caller) and a.callee not in self.lines:
                    self.calls.remove(a)
        else: # If line not in lines list, raise error
            raise PhonePlanError('no such line to remove')
    def calculate_bill(self):
        temp=None
        # Check if mins_to_pay is more than default_mins
        # Update rollover if has_rollover is True
        if self.mins_to_pay <= self.type.default_mins:
            self.balance = self.type.basic_rate
            if self.type.has_rollover:
                temp=(self.type.default_mins - self.mins_to_pay)
                self.rollover_mins = self.rollover_mins + temp
        else:
            if self.type.has_rollover:
                if (self.mins_to_pay-self.type.default_mins) <= self.rollover_mins:
                    self.balance = self.type.basic_rate
                    temp=(self.mins_to_pay - self.type.default_mins)
                    self.rollover_mins = self.rollover_mins - temp
                else:
                    temp=(self.mins_to_pay-self.type.default_mins-self.rollover_mins)
                    self.balance=self.type.basic_rate+ temp*self.type.rate_per_min
                    self.rollover_mins = 0
            else:
                temp=(self.mins_to_pay-self.type.default_mins)
                self.balance=self.type.basic_rate+temp*self.type.rate_per_min
        # Reset mins_to_pay and call list
        self.mins_to_pay = 0
        self.calls =[]
        # Check if the amount is too large then deactivate the plan
        if self.balance > 4*self.type.basic_rate:
            self.deactivate_all()
    def pay_bill(self, amount=None):
        # Update balance base on given amount
        if amount == None and self.balance > 0:
            self.balance = 0
        elif amount == None and self.balance < 0:
            pass
        # Amount can't be negative
        if amount != None:
            if amount < 0:
                raise ValueError('amount to pay cannot be negative')
            else:
                self.balance -= amount
        # Check if the amount isn't too large then activate the plan
        if self.balance <= 4*self.type.basic_rate:
            self.activate_all()



            









