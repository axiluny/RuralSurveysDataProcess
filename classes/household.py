'''
Created on Mar 25, 2015

@author: Liyan Xu; Hongmou Zhang
'''
# import copy
# import random

from person import Person
from data_access import DataAccess
from capital_property import CapitalProperty

class Household(object):
    '''
    This is the definition of the household class
    '''
    
    
    def __init__(self, record, VarList, current_year, db, pp_table_name, pp_table):
        '''
        Construct the household class from the household table in the DB, and then add some other user-defined attributes.

        record indicates a record in the household table in the DB.
        
        VarList is the variable (or field) list of the household table in the DB   
        VarList = {paramName1: paramOrder1, paramName2: paramOrder2, ...}
        
        Also initialize the household's own person instances here from the person table in the DB.
        Also initialize the household's capital properties instance here.     
        '''       
        
        # Set the attributes (var) and their values (record) from the household table in the DB.
        for var in VarList:
            setattr(self, var[0], record[var[1]])

        # Set the household and person variables (attributes) lists
        self.hh_var_list = VarList
        self.pp_var_list = DataAccess.get_var_list(db, pp_table_name)


        # Set the current time stamp
        self.StatDate = current_year
        
        
        # Define own persons (members) dict of the household, indexed by PID
        self.own_pp_dict = dict()

        
        # Add respective persons into the persons dict of the household
        for pp in pp_table:
            if pp.HID == self.HID:
                pp_temp = Person(pp, self.pp_var_list, current_year)
                self.own_pp_dict[pp_temp.PID] = pp_temp # Indexed by PID
        

        
        # Initialize the household's capital properties instance
        self.own_capital_properties = CapitalProperty(self)
        
        
        # Define a switch variable indicating whether the household is dissolved in the current year
        self.is_dissolved_this_year = False
  


    
    def annual_update(self, current_year, model_parameters):
        '''
        Annual demographic updates of the household.
        '''
        
        # Update the current time stamp
        self.StatDate = current_year
        
        # Reset the "dissolved this year" switch
        # Note this is before the household existence bifurcation. 
        # So all households in society.hh_dict get this switch reset (every year).
        self.is_dissolved_this_year = False
        
        
        # Only the existing households proceed.
        if self.is_exist == 1:
            
            temp_pp_list = list()
                                
            # Annual population dynamics (personal demographic status updates)
            for PID in self.own_pp_dict:
                temp_pp_list.append(Person.annual_update(self.own_pp_dict[PID], current_year, model_parameters))

            # Reset own persons (members) dict (own_pp_dict)
            self.own_pp_dict = dict()
                        
            # Refresh own_pp_list                    
            for p in temp_pp_list:
                self.own_pp_dict[p.PID] = p
                                                    
                                                                
            # If the updated household has no members, mark it as non-exist.
            alive_members_count = 0
            for PID in self.own_pp_dict:
                if self.own_pp_dict[PID].is_alive == 1:
                    alive_members_count += 1
                    
            if alive_members_count == 0:        
                self.is_exist = 0
                self.is_dissolved_this_year = True # Turn on this switch so that the household could be dissolved later in the society class
            

            # Then deal with the deceased persons
            for p in temp_pp_list:         
                # If p dies this year and p's spouse lives
                if p.is_died_this_year == True and p.SpouseID != '0' and self.own_pp_dict[p.SpouseID].is_alive == 1:
                                       
                    # Then p's spouse's marital status changes
                    self.own_pp_dict[p.SpouseID].IsMarry = 0
                    self.own_pp_dict[p.SpouseID].SpouseID = '0'
   
                    # And p's own marital status is also marked changed
                    self.own_pp_dict[p.PID].IsMarry = 0
                    self.own_pp_dict[p.PID].SpouseID = '0'     
        
        return self



    
    def household_capital_properties_update(self):
        self.own_capital_properties.refresh(self)
    


    
    
    