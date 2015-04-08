'''
Created on Apr 5, 2015

@author: xuliy_000
'''

class Person(object):

    '''
    This is the definition of the person class
    '''
    
    def __init__(self, record, VarList):
        '''
        Constructor of Person
        VarList = {paramName1: paramOrder1, paramName2: paramOrder2, ...}
        '''
        for var in VarList:
            setattr(self, var[0], record[var[1]])
    
        # Define other attributes of the person
        self.is_alive = True
        self.is_college = False
        self.marriage_length = 0 #This value should have been given in the original database!
    
        
    def step_go(self, current_year):

        # Update current time stamp
#         if self.StatDate == None: # This should not be working for newly added (born) persons. Work on it. Should introduce current_year variable.
        self.StatDate = current_year

        
        # Personal demographic dynamics
        if self.is_alive == True:
            self.grow()
            
            if self.is_die() == False:
                self.get_education()
                
                if self.is_college == False:
                    if self.IsMarry == True:
                        if self.divorce() == False:
                            self.childbirth()
                    else:
                        self.marry()
                        
    
    def grow(self):
        self.Age += 1        
    
    
    def is_die(self):
        pass
    
    
    def get_education(self):
        pass
    
    def marry(self):
        pass
    
    def divorce(self):
        if 1 > 2:#Never let anyone to divorce for now
            return True
        
        else:
            self.marriage_length += 1 
            return False
    
    def childbirth(self):
        # can be something like this
        return person()