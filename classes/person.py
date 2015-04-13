'''
Created on Apr 5, 2015

@author: Liyan Xu; Hongmou Zhang
'''
import random
import copy
from enum import Enum

class Person(object):
    
    Education_type = Enum('Education_type','uneducated primary secondary high_school college graduate' )

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
        self.pp_var_list = VarList
        
        self.is_alive = True
        self.is_college = False
        self.marriage_length = 0 #This value should have been given in the original database!
            
        
    def step_go(self, current_year):

        # Update current time stamp
        self.StatDate = current_year
        
        # Define returned list
        res = list()

        
        # Personal demographic dynamics
        if self.is_alive == True: # Must be true for now 20150410
            self.grow()
            
            if self.decease() == True: # If the person dies
                self.is_alive = False # Mark the one as not alive
                res = [self]
            
            else:
                self.get_education()
                
                if self.is_college == False:  # Temporarily not allow anyone to go to college
                    if self.IsMarry == True:
                        if self.divorce() == False: # Temporarily not allow anyone to divorce
                            res = self.childbirth(current_year)
                    else:
                        self.marry()
                        res = [self]
        
        return res
                        
    
    def grow(self):
        self.Age += 1        
    
    
    def decease(self):
        
        if random.random() < 0.05: # Temporarily let one's chance to die is 5%
            return True
        
        else:
            return False
    
    
    
    def get_education(self):
        pass
    
    def marry(self):
        pass
    
    def divorce(self):
        if 1 > 2:#Never let anyone to divorce for now/20150407
            return True
        
        else:
            self.marriage_length += 1 
            return False
    
    def childbirth(self, current_year):
        
        if self.Gender == 0: # Only women can give birth.
            if random.random() < 0.1: # Temporarily allow 10% chance to give birth           
                res = self.add_person(current_year)
            else:
                res = [self]
        
        else:            
            res = [self]
        
        return res
    
    
    def add_person(self, current_year):

        new_pp = copy.deepcopy(self)        

        # Reset all properties
        for var in new_pp.pp_var_list:
            setattr(new_pp, var[0], None)       
            
        # Grant new properties
        new_pp.Pname = self.Pname + 'n'
        new_pp.Age = 0
        new_pp.Gender = int(round(random.random(), 0))
        new_pp.StatDate = current_year
        
        # Temporarily manipulating PIDs so that the persons dictionary gets non-duplicate indices
        new_pp.PID = self.PID
        
        if current_year == 2015:
            if new_pp.PID[:1] == 'g':
                new_pp.PID = 'G' + self.PID[1:]
            elif new_pp.PID[:1] == 'w':
                new_pp.PID = 'W' + self.PID[1:]
        else:
            if new_pp.PID[:1] == 'g' or new_pp.PID[:1] == 'G':
                new_pp.PID = self.PID[:2] + 'C' + self.PID[3:]
            elif new_pp.PID[:1] == 'w' or new_pp.PID[:1] == 'W':
                new_pp.PID = self.PID[:2] + 'C' + self.PID[3:]            

            
        res = [self, new_pp]
        return res
             
    

    