# Name: PHUONG TRAN
# G#: G01082824
# Lab 11
# Due Date: 12/03/2018
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

# Most of the return for __name__ is using string formatting
class Grade:
    def __init__(self, kind, name, percent):
        self.kind = kind
        self.name = name
        self.percent = percent
        if self.kind!='test' and self.kind!='lab' and self.kind!='project' and self.kind!='final':
            raise GradingError("no Grade kind '%s'" %self.kind)
    def __str__(self):
        return ('%s:%s(%d%%)' % (self.kind, self.name, self.percent))
    def __repr__(self):
        return ("%s('%s', '%s', %d)"%(self.__class__.__name__,self.kind,self.name,self.percent))
    def __eq__(self, other):
        return (self.kind == other.kind and self.name == other.name and self.percent == other.percent)
class GradeBook:
    def __init__(self):
        self.grades = []
    def __str__(self):
        ans = "%s:" % self.__class__.__name__ +'\n'
        # Go through each element in self.grade list and add the grade into the list
        for x in self.grades:
            ans += '\t'+Grade.__str__(x) +'\n'
        return ans
    def __repr__(self):
        return self.__str__()
    def add_grade(self, grade):
        self.grades.append(grade) # Add new grade into self.grades list
    def average_by_kind(self, kind):
        count=0 # Keep track of how many grade of the same kind
        total=0 # Keep track of the sum of the percent of grade of the same kind
        for a in self.grades:
            if a.kind == kind:
                total += a.percent
                count +=1
        return (total/count) # Return the avg
    def get_all_of(self,kind):
        kind_list =[] # Create empty list
        for a in self.grades:
            # Add object into a list if object's kind is the same as given kind
            if a.kind == kind:
                kind_list.append(a)
        return kind_list # Return a list with objects have the same kind
    def get_by_name(self, name):
        count=0 # Keep track of how many grade has given name
        for a in self.grades:
            if a.name == name:
                count+=1
                return a # Return the first object found
        if count == 0: # If none then raise error
            raise GradingError("no grade found named '%s'"% name)

class GradingError(Exception): # Use to catch errors have been raised
    def __init__(self,msg):
        self.msg = msg
    def __str__(self):
        return "%s: no Grade found named '%s'" % (self.__class__.__name__,self.msg)
    def __repr__(self):
        return "%s('''%s''')" %(self.__class__.__name__, self.msg)





