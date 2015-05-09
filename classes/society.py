'''
Created on Mar 26, 2015

@author: Liyan Xu; Hongmou Zhang
'''
import copy
import random

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

        # Also define a current hh dict to store only the existing households
        self.cur_hh_dict = self.hh_dict # At initiation the two dicts are identical
        
     
#         # Define a dictionary to store all the person instances, indexed by PID
#         self.pp_dict = dict()
#         
#         # Add person instances to pp_dict
#         for pp in pp_table:
#             pp_temp = Person(pp, self.pp_var_list)
#             self.pp_dict[pp_temp.PID] = pp_temp # Indexed by PID
# 
#         # Also define a current pp dict to store only the alive persons
#         self.cur_pp_dict = self.pp_dict # At initiation the two dicts are identical



        
    def step_go(self, start_year, end_year, simulation_count):
        
        self.current_year = start_year + simulation_count
        
        self.agents_update()
        
        self.marriage()
        
        self.child_birth()


               
            
    def agents_update(self):
        # household and people status update; everything except for marriage and child birth
        
        temp_hh_list = list()

        for HID in self.hh_dict:
            temp_hh_list.append(Household.annual_update(self.hh_dict[HID], self.current_year, self.model_parameters_dict))
        
        # Refresh households and current households dicts
        self.hh_dict = dict()
        self.cur_hh_dict = dict()
        
#         self.pp_dict =  dict()
#         self.cur_pp_dict = dict()
        
        for h in temp_hh_list:
            self.hh_dict[h.HID] = h                        
#             for PID in h.own_pp_dict:
#                 self.pp_dict[PID] = h.own_pp_dict[PID]
            
            if h.is_exist == 1: # Only existing households are added to current hh dict
                self.cur_hh_dict[h.HID] = h
#                 for PID in h.cur_own_pp_dict:
#                     self.cur_pp_dict[PID] = h.cur_own_pp_dict[PID]                 

    
    def marriage(self):
        
        marry_list = list()
        
        # Get the "to be married this year" list
        for HID in self.cur_hh_dict:
            for PID in self.cur_hh_dict[HID].cur_own_pp_dict:
                pp = self.cur_hh_dict[HID].cur_own_pp_dict[PID]
                
                if pp.is_married_this_year == True:
                    marry_list.append(pp)
                    
        
        for pp in marry_list:
            
            if pp.is_married_this_year == True:
                    
                if pp.Gender == 1: #Male                
                    # Find him a spouse
                    for sp in marry_list:
                                        
                        if sp.Gender == 0 and pp.HID != sp.HID and sp.is_married_this_year == True: # spouse must be a female and from a different household
                            # Make the match        
                            pp.is_married_this_year = False
                            sp.is_married_this_year = False # Remove the two persons from the "to be married" list
                                                    
                            pp.SpouseID = sp.PID
                            sp.SpouseID = pp.PID
                                                      
                            # Assign household affiliation for the new couple
                            if len(self.cur_hh_dict[pp.HID].cur_own_pp_dict) == 1: # if the male is the only member of his original household
                                self.add_person_to_household(sp, pp.HID, 'spouse') # then just add his new wife to his household
                                break
                                                      
                            else:
                                self.create_new_household(pp) # Create a new household with the male pp being the household head
                                self.add_person_to_household(sp, pp.HID, 'spouse') # Add the spouse to the newly created household
                                break
                        
                        
                    # If failed to find a match    
                    pp.is_married_this_year = False 
                                    
                                              
                else: #Female
                    # Find her a spouse       
                    for sp in marry_list:
    
                        if sp.Gender == 1 and pp.HID != sp.HID and sp.is_married_this_year == True: # spouse must be a female and from a different household
                            # Make the match                    
                            pp.is_married_this_year = False
                            sp.is_married_this_year = False # Remove the two persons from the "to be married" list
                    
                            pp.SpouseID = sp.PID
                            sp.SpouseID = PID
                                                                              
                            # Assign household affiliation for the new couple
                            if len(self.cur_hh_dict[sp.HID].cur_own_pp_dict) == 1: # if her spouse is the only member of his original household
                                self.add_person_to_household(pp, sp.HID, 'spouse') # then just add her to her husband's household
                                break
                                              
                            else:
                                self.create_new_household(sp) # Create a new household with her spouse sp(male) being the household head
                                self.add_person_to_household(pp, sp.HID, 'spouse') # Add herself to the newly created household
                                break

    
                    # If failed to find a match    
                    pp.is_married_this_year = False 



    
    def child_birth(self):
        
        mom_list = list()
        
        for HID in self.cur_hh_dict:
            for PID in self.cur_hh_dict[HID].cur_own_pp_dict:
                pp = self.cur_hh_dict[HID].cur_own_pp_dict[PID]
                
                if pp.is_giving_birth_this_year == True:
                    mom_list.append(pp)
                
        for mom in mom_list:
            new_baby = self.create_new_person(mom)
            self.add_person_to_household(new_baby, mom.HID, 'child')




    
    def create_new_household(self, pp):

        new_hh = copy.deepcopy(self.cur_hh_dict[pp.HID])     
         
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
        new_hh.Hname = pp.Pname
        new_hh.StatDate = self.current_year
        new_hh.NonRural = self.cur_hh_dict[ori_hid].NonRural
        new_hh.is_exist = 1
        
        # Modify the new household head's personal properties to match the new household
        pp.HID = new_hh.HID
        pp.Hname = new_hh.Hname
        pp.R2HHH = '31'
                                          
        # Add the new household head to new_hh.own_pp_dict and current own pp dict
        new_hh.own_pp_dict[pp.PID] = pp
        new_hh.cur_own_pp_dict[pp.PID] = pp
                  
        # Remove the new household head from his original household's persons dict
        del self.hh_dict[ori_hid].own_pp_dict[pp.PID]        
        del self.cur_hh_dict[ori_hid].cur_own_pp_dict[pp.PID]
                  
        # Add the newly created household to Society's household dict
        self.hh_dict[new_hh.HID] = new_hh
        self.cur_hh_dict[new_hh.HID] = new_hh
        

    def create_new_person(self, mom):
        # The only occasion to create a new person instance is the birth of a new baby. mom indicates the mother.

        new_pp = copy.deepcopy(mom)

        # Reset all properties
        for var in new_pp.pp_var_list:
            setattr(new_pp, var[0], None)       
            
        # Grant new properties
        new_pp.HID = mom.HID
        new_pp.Hname = mom.Hname
        
        new_pp.PID = self.get_new_pid(mom)
        new_pp.Pname = mom.Pname + 'c'

        new_pp.Gender = self.get_gender()
        new_pp.Age = 0
        new_pp.R2HHH = self.get_relation_to_hh_head(new_pp, 'child')
        new_pp.IsMarry = 0

        new_pp.MotherID = mom.PID
        new_pp.FatherID = mom.SpouseID
        new_pp.SpouseID = None
        
        new_pp.Education = 'uneducated'
#         new_pp.Ethnicity = self.cur_pp_dict[mom.SpouseID].Ethnicity
        
        new_pp.is_alive = 1
        new_pp.StatDate = self.current_year
        
#         # Add the newly created person to self.pp_dict
#         self.pp_dict[new_pp.PID] = new_pp
#         self.cur_pp_dict[new_pp.PID] = new_pp

        return new_pp

    
    


    
    def add_person_to_household(self, pp, HID, r_2_hh_head):
        # Adding the person pp into the household with HID = HID;
        # r_2_hh_head indicates pp's relationship to the household head, of which values include 'spouse', 'child', etc

        if r_2_hh_head == 'spouse':
            # Record the original HID
            ori_hid = pp.HID
            
            # Modify the personal properties of the newly added person
            pp.HID = HID
            pp.Hname = self.cur_hh_dict[HID].Hname 
            pp.R2HHH = self.get_relation_to_hh_head(pp, r_2_hh_head)       
            
            # Add the person to household members dict
            self.hh_dict[HID].own_pp_dict[pp.PID] = pp
            self.hh_dict[HID].cur_own_pp_dict[pp.PID] = pp
            
            self.cur_hh_dict[HID].own_pp_dict[pp.PID] = pp
            self.cur_hh_dict[HID].cur_own_pp_dict[pp.PID] = pp
    
            # Remove the person from his/her original household's persons dict
            del self.hh_dict[ori_hid].own_pp_dict[pp.PID]
#             del self.hh_dict[ori_hid].cur_own_pp_dict[pp.PID]
# 
#             del self.cur_hh_dict[ori_hid].own_pp_dict[pp.PID]             
            del self.cur_hh_dict[ori_hid].cur_own_pp_dict[pp.PID] 
        
        
        elif r_2_hh_head == 'child':
            # Add the person to household members dict
            self.hh_dict[HID].own_pp_dict[pp.PID] = pp
#             self.hh_dict[HID].cur_own_pp_dict[pp.PID] = pp
#             
#             self.cur_hh_dict[HID].own_pp_dict[pp.PID] = pp
            self.cur_hh_dict[HID].cur_own_pp_dict[pp.PID] = pp


    
    def get_new_hid(self, pp):
        group_hid_list = list()
        
        for HID in self.hh_dict: # Must use full hh_dict including non-existing hhs, because HIDs are indexed and thus are not allowed to duplicate
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
    
    
    def get_new_pid(self, pp):
        household_member_list = list()
        
        for HID in self.cur_hh_dict:
            if HID == pp.HID: # Find pp's household
                for PID in self.cur_hh_dict[HID].cur_own_pp_dict: 
                    household_member_list.append(self.hh_dict[HID].cur_own_pp_dict[PID])
        
        new_id_num = int(len(household_member_list)+1)
        
        if int(new_id_num/10) != 0: # if the new id number is in tens
            new_id = pp.HID + str(new_id_num)
        else:
            new_id = pp.HID + '0' + str(new_id_num)
        
        return new_id
    
    
    # This submodule needs elaboration. 
    def get_relation_to_hh_head(self, pp, r_2_hh_head):
        
        relation = ''
        
        if r_2_hh_head == 'spouse':
            relation = '32'
        elif r_2_hh_head == 'child':
            relation = '41' # Need elaboration
        
        return relation
    
    
    # Random assign a gender to a newly created Person
    def get_gender(self):
        return int(round(random.random(), 0))
    
    
    