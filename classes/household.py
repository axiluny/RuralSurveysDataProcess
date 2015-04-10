'''
Created on Mar 25, 2015

@author: Hongmou
'''
import copy
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
        
        new_hh = copy.deepcopy(self)
#         new_hh = Household(hh_table, self.hh_var_list, db, pp_table_name, pp_table) # Why this isn't working?

        new_hh.Hname = self.Hname + '1'
        # Temporarily manipulating HIDs so that the household dictionary gets non-duplicate indices
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
         
         
#         for pp in new_hh.own_pp_list:
#             new_hh.own_pp_list.remove(pp)
         
        new_hh_list = [self, new_hh]
        return new_hh_list

    