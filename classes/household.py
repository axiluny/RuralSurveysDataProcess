'''
Created on Mar 25, 2015

@author: Liyan Xu; Hongmou Zhang
'''
# import copy
# import random

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
        
        # Define own persons (members) dict of the household, indexed by PID
        self.own_pp_dict = dict()
        # Also define a current persons (members) dict of the household to store only the alive persons, who enter the current iteration.
        self.cur_own_pp_dict = dict()
        
        # Add respective persons into the persons dict of the household
        for pp in pp_table:
            if pp.HID == self.HID:
                pp_temp = Person(pp, self.pp_var_list)
                self.own_pp_dict[pp_temp.PID] = pp_temp # Indexed by PID
        
        self.cur_own_pp_dict = self.own_pp_dict
  


    
    def annual_update(self, current_year, model_parameters):
        
        # Update current time stamp
        self.StatDate = current_year

                
        if self.is_exist == 1: # If the household exists
            
            temp_pp_list = list()
        
            # First run population dynamics
            for PID in self.own_pp_dict:
                temp_pp_list.append(Person.annual_update(self.own_pp_dict[PID], current_year, model_parameters))
            
            
            # Refresh own persons (members) and current members dicts
            self.own_pp_dict = dict()
            self.cur_own_pp_dict = dict()
                        
            for p in temp_pp_list:
                self.own_pp_dict[p.PID] = p
                    
                if p.is_alive == 1: # Only persons who are alive are added to hh.cur_own_pp_list
                    self.cur_own_pp_dict[p.PID] = p                

            
            # If the updated household has no members, dissolve it.
            if len(self.cur_own_pp_dict) == 0:
                res = self.dissolve_household()
                            
            else:
                res = self
        
        else: # If the household no longer exists
            res = self # Do nothing to it.
            
        
        return res

    
    
    def dissolve_household(self):
        
        # Mark household a non-exist
        self.is_exist = 0
        
        # Deal with household properties
        self.legacy()
        
        return self

    
    
    def legacy(self):
        pass
    
    