'''
Created on Mar 25, 2015

@author: Hongmou
'''
import copy
import random

from person import Person
from data_access import DataAccess

class Household(object):
    '''
    This is the definition of the household class
    '''
    
    
    def __init__(self, record, VarList, db, pp_table_name, pp_table):
        '''
        Constructor of Household
        VarList = {paramName1: paramOrder1, paramName2: paramOrder2, ...}
        '''       
    
        for var in VarList:
            setattr(self, var[0], record[var[1]])


        self.hh_var_list = VarList
        self.pp_var_list = DataAccess.get_var_list(db, pp_table_name)
        
        # Define person list in the household
        self.own_pp_list = []
        
        # Add respective persons into the person list of the household
        for pp in pp_table:
            if pp.HID == self.HID:
                pp_temp = Person(pp, self.pp_var_list)
                
                self.own_pp_list.append(pp_temp)
            
  
    
    def step_go(self, current_year, db, hh_table_name, hh_table, pp_table_name, pp_table):
        
        # Update current time stamp
        self.StatDate = current_year
        
#         for pp in self.own_pp_list:
#             Person.step_go(pp, current_year)

        '''
        The following codes are for testing adding new household instances, and the save them to the database.
        20150409 Liyan Xu
        '''
        
        # Define returned tuple
        res = tuple()
        
        # Test code for creating a new household
        if random.random() < 0.1: # Temporarily allow 10% chance to generate new households
            if len(self.own_pp_list) >= 2: # And only if the current household has more than 2 (include 2) members
                res = self.create_new_household(self.own_pp_list[1], current_year) # Then create a new household with the second member being head of the new household
        
            else: # No new household created
                res_list = [self]
                res = (False, res_list) # False indicates no new household created
        
        else: # No new household created
            res_list = [self]
            res = (False, res_list)
        
        return res
        

    
    
    # Create a new household with a given household head
    def create_new_household(self, Person, current_year):
        
        new_hh = copy.deepcopy(self)
#         new_hh = Household(hh_table, self.hh_var_list, db, pp_table_name, pp_table) # Why this isn't working?        
        
        # Reset all properties
        for var in new_hh.hh_var_list:
            setattr(new_hh, var[0], None)        
        
        # Grant new properties
        new_hh.Hname = self.Hname + 'n'
        new_hh.StatDate = current_year
        
        # Temporarily manipulating HIDs so that the household dictionary gets non-duplicate indices
        new_hh.HID = self.HID
        
        if current_year == 2015:
            if new_hh.HID[:1] == 'g':
                new_hh.HID = 'G' + self.HID[1:]
            elif new_hh.HID[:1] == 'w':
                new_hh.HID = 'W' + self.HID[1:]
        else:
            if new_hh.HID[:1] == 'g' or new_hh.HID[:1] == 'G':
                new_hh.HID = self.HID[:2] + 'C' + self.HID[3:]
            elif new_hh.HID[:1] == 'w' or new_hh.HID[:1] == 'W':
                new_hh.HID = self.HID[:2] + 'C' + self.HID[3:]
        
        
        # Clear new_hh.own_pp_list
        
        
        # Add new household head to new_hh.own_pp_list
        
        
        # Lastly, take care of the original household
#         self.own_pp_list.remove(self.own_pp_list(1)) # Remove that person from the original household        
        
        
        # Return a tuple. True indicates a new household generated. Both original and new household instances are also returned in a list.
        res_list = [self, new_hh]
        res = (True, res_list)
        
        return res
 