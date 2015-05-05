'''
Created on Mar 25, 2015

@author: Liyan Xu; Hongmou Zhang
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
        
        # Define person list and dict of the household
        self.own_pp_list = list()
        self.own_pp_dict = dict()
        
        # Add respective persons into the person list and dict of the household
        for pp in pp_table:
            if pp.HID == self.HID:
                pp_temp = Person(pp, self.pp_var_list)
                
                self.own_pp_list.append(pp_temp)
                self.own_pp_dict[pp_temp.PID] = pp_temp # Indexed by PID            
  
    
    def annual_update(self, current_year, db, hh_table_name, hh_table, pp_table_name, pp_table, model_parameters):
        
        # Update current time stamp
        self.StatDate = current_year
        
        # First run population dynamics
        self.cur_own_pp_list = list()
        self.cur_own_pp_dict = dict()

        for pp in self.own_pp_list:
            temp_res = Person.annual_update(pp, current_year, model_parameters)
            
            for p in temp_res:
                if p.is_alive == True:
                    self.cur_own_pp_list.append(p)
                    self.cur_own_pp_dict[p.PID] = p                

        self.own_pp_list = self.cur_own_pp_list           
        self.own_pp_dict = self.cur_own_pp_dict # Indexed by PID       


        # Define returned list
        res = list()

        # If all household members die this year, dissolve the household.
        if len(self.own_pp_list) == 0:
            res = []
            self.legacy()
        
        else:
            res = [self]
        
        return res
        
#         '''
#         The following codes are for testing adding new household instances, or removing some household records, and then save the results to the database.
#         20150409 Liyan Xu
#         '''
#         
#         # Define returned list
#         res = list()
#         
#         # Test code for removing household records with no members (all died this year)
#         if len(self.own_pp_list) == 0:
#             res = []
#             self.legacy()
#         
#         else:
#                 
#             # Test code for creating a new household
#             if random.random() < 0.1: # Temporarily allow 10% chance to generate new households
#                 if len(self.own_pp_list) >= 2: # And only if the current household has more than 2 (include 2) members
#                     res = self.create_new_household(self.own_pp_list[1], current_year) # Then create a new household with the second member being head of the new household
#              
#                 else: # No new household created
#                     res = [self]
#              
#             else: # No new household created
#                 res = [self]
#         
#         return res



   
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
        
        
        # Clear new_hh.own_pp_list and new_hh.own_pp_dict
        new_hh.own_pp_list = list()
        new_hh.own_pp_dict = dict()
        
        
        # Add new household head to new_hh.own_pp_list
        new_hh.own_pp_list.append(Person)
        new_hh.own_pp_dict[Person.PID] = Person   
        
        # Lastly, take care of the original household
        self.own_pp_list.remove(Person) # Remove that person from the original household
        del self.own_pp_dict[Person.PID]
        
        
        # Return both original and new household instances in a list
        res = [self, new_hh]
        
        return res
    
    
    
    
    def legacy(self):
        pass
    
    
 