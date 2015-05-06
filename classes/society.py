'''
Created on Mar 26, 2015

@author: Liyan Xu; Hongmou Zhang
'''
import copy

from data_access import DataAccess
from household import Household
from person import Person


class Society(object):
    '''
    This is the definition of society class
    
    Creating household, person, etc. lists and dictionaries.
    '''


    def __init__(self, db, model_table_name, model_table, hh_table_name, hh_table, pp_table_name, pp_table):
        '''
        Constructor

        '''
        self.current_year = 0
        
        # Create a dictionary to store model parameters, indexed by Variable_Name, and contents are Variable_Value      
#         self.model_var_list = DataAccess.get_var_list(db, model_table_name)
        self.model_parameters_dict = dict()
        
        for record in model_table:
            self.model_parameters_dict[record.Variable_Name] = record.Variable_Value
          
        
        # Get the variable lists for household and person classes 
        self.hh_var_list = DataAccess.get_var_list(db, hh_table_name)
        self.pp_var_list = DataAccess.get_var_list(db, pp_table_name)


        # Define a dictionary to store all the household instances, indexed by HID
        self.hh_dict = dict()
                
        # Add household instances to hh_dict
        for hh in hh_table:
            hh_temp = Household(hh, self.hh_var_list, db, pp_table_name, pp_table)
            self.hh_dict[hh_temp.HID] = hh_temp # Indexed by HID
        
     
        # Define a dictionary to store all the person instances, indexed by PID
        self.pp_dict = dict()
        
        # Add person instances to pp_dict
        for pp in pp_table:
            pp_temp = Person(pp, self.pp_var_list)
            self.pp_dict[pp_temp.PID] = pp_temp # Indexed by PID


        
    def step_go(self, start_year, end_year, simulation_count, db, hh_table_name, hh_table, pp_table_name, pp_table,):
        
        self.current_year = start_year + simulation_count

        self.cur_hh_dict = dict()
        self.cur_pp_dict = dict()
        
        
        self.agents_update(db, hh_table_name, hh_table, pp_table_name, pp_table)
        
        self.marriage()
        
        self.child_birth()
               
            
    def agents_update(self, db, hh_table_name, hh_table, pp_table_name, pp_table):
        # household and people status update; everything except for marriage and child birth

        for HID in self.hh_dict:
            temp_list = Household.annual_update(self.hh_dict[HID], self.current_year, db, hh_table_name, hh_table, pp_table_name, pp_table, self.model_parameters_dict)
                
            for h in temp_list:
                self.cur_hh_dict[h.HID] = h
                 
                for PID in h.own_pp_dict:
                    self.cur_pp_dict[h.own_pp_dict[PID].PID] = h.own_pp_dict[PID]
        
                    
        self.hh_dict = self.cur_hh_dict # Indexed by HID        
        self.pp_dict = self.cur_pp_dict # Indexed by PID
            
    
    def marriage(self):
        # Select all person agents who get married this year
        marry_list = list()
         
        for PID in self.pp_dict:
            if self.pp_dict[PID].is_married_this_year == True:
                marry_list.append(self.pp_dict[PID])
         
         
        # Make matches
        for pp in marry_list:
            if pp.is_married_this_year == True:
                if pp.Gender == 1: #Male
                    # Find him a spouse
                    for sp in marry_list: # sp = spouse
                        if sp.Gender == 0 and pp.HID != sp.HID and sp.is_married_this_year == True: # spouse must be a female and from a different household
                            pp.is_married_this_year = False
                            sp.is_married_this_year = False # Remove the two persons from the "to be married" list
                             
                            # Assign household affiliation for the new couple
                            if len(self.hh_dict[pp.HID].own_pp_dict) == 1: # if the male is the only member of his original household
                                self.add_person_to_household(sp, pp.HID) # then just add his new wife to his household
                                 
                            else:
                                self.create_new_household(pp) # Create a new household with the male pp being the household head
                                self.add_person_to_household(sp, pp.HID) # Add the spouse to the newly created household
                             
                else: #Female
                    # Find her a spouse
                    for sp in marry_list:
                        if sp.Gender == 1 and pp.HID != sp.HID and sp.is_married_this_year == True:
                            pp.is_married_this_year = False
                            sp.is_married_this_year = False # Remove the two persons from the "to be married" list
                             
                            # Assign household affiliation for the new couple
                            if len(self.hh_dict[sp.HID].own_pp_dict) == 1: # if her spouse is the only member of his original household
                                self.add_person_to_household(pp, sp.HID) # then just add her to her husband's household
                                 
                            else:
                                self.create_new_household(sp) # Create a new household with her spouse sp(male) being the household head
                                self.add_person_to_household(pp, sp.HID) # Add herself to the newly created household
                         
    
    
    def child_birth(self):
        pass


    
    def create_new_household(self, pp):

        new_hh = copy.deepcopy(self.hh_dict[pp.HID])     
         
        # Record the original HID
        ori_hid = pp.HID
         
        # Reset all household properties, and clear own_pp_dict and cur_own_pp_dict
        for var in new_hh.hh_var_list:
            setattr(new_hh, var[0], None)        

        new_hh.own_pp_dict = dict()
        new_hh.cur_own_pp_dict = dict()
        
         
        # Assign a new HID for the new household
        new_hh.HID = self.get_new_hid(pp)
         
        # Grant other new household properties
        new_hh.Hname = pp.Hname
        new_hh.StatDate = self.current_year
                          
        # Add new household head to new_hh.own_pp_dict
        new_hh.own_pp_dict[pp.PID] = pp   
                  
        # Remove the new household head from his original household's persons dict
        del self.hh_dict[ori_hid].own_pp_dict[pp.PID]
                  
        # Add the newly created household to Society's household dict
        self.hh_dict[new_hh.HID] = new_hh



    
    def add_person_to_household(self, pp, HID):
        pass
    
    
    
    def get_new_hid(self, pp):
        group_hid_list = list()
        
        for HID in self.hh_dict:
            if HID[:5] == pp.HID[:5]: # if the first 5 digits (indicating village and group affiliation) are identical
                group_hid_list.append(HID)
        
        new_id_num = int(max(group_hid_list)[5:])+1
        
        if int(new_id_num/100) != 0: # if the new id number is in hundreds
            new_id = max(group_hid_list)[:5] + str(new_id_num)
        elif int(new_id_num/100) == 0 and int(new_id_num/10) != 0: # if the new id number is in tens
            new_id = max(group_hid_list)[:5] + '0' + str(new_id_num)
        else:
            new_id = max(group_hid_list)[:5] + '00' + str(new_id_num)
        
        return new_id
        