# Name: PHUONG TRAN
# G#: G01082824
# Lab 12
# Due Date: 12/05/2018
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

class Pokemon:
    def __init__(self, name, species, combat_power, can_fly):
        self.name = name
        self.species = species
        self.combat_power = combat_power
        self.can_fly = can_fly
    def __str__(self):
        return "%s('%s', '%s', '%d')" % (self.__class__.__name__, self.name, self.species, self.combat_power)
    def __repr__(self):
        return self.__str__()
    def __eq__(self, other):
        if self.name==other.name and self.species==other.species and self.combat_power==other.combat_power and self.can_fly==other.can_fly:
            return True
        else:
            return False
    def battle(self, other):
        if self.combat_power > other.combat_power:
            return True
        elif self.combat_power < other.combat_power:
            return False
        elif self.combat_power == other.combat_power:
            return None

class Pokebox:
    def __init__(self, members=None):
        self.members = members
    def __str__(self):
        if self.members == None:
            return "%s([])" % (self.__class__.__name__)
        else:
            answer = "%s([" % (self.__class__.__name__)
            for a in self.members:
                answer += Pokemon.__str__(a) + ','
            answer=answer[0:-1]
            answer += '])'
            return answer
    def add_pokemon(self,p):
        self.members.append(p)
        return None
    def count_top_combatants(self, powers):
        count = 0
        if self.members == 0:
            return count
        else:
            for a in self.members:
                if a.combat_power > powers:
                    count +=1
                else:
                    continue
        return count
    def flying_type_available(self):
        pokemon_fly = False
        if self.members == None:
            return pokemon_fly
        else:
            for x in self.members:
                if x.can_fly:
                    pokemon_fly = True
            return pokemon_fly