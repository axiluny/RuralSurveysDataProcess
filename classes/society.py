'''
Created on Mar 26, 2015

@author: Liyan Xu; Hongmou Zhang
'''
import copy
import random

from data_access import DataAccess
from household import Household
# from person import Person


class Society(object):
    '''
    This is the definition of society class
    
    Creating household, person, etc. lists and dictionaries.
    '''


    def __init__(self, db, model_table_name, model_table, hh_table_name, hh_table, pp_table_name, pp_table, stat_table_name, stat_table, simulation_depth, start_year, end_year):

        self.current_year = start_year
        
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
            hh_temp = Household(hh, self.hh_var_list, self.current_year, db, pp_table_name, pp_table)
            self.hh_dict[hh_temp.HID] = hh_temp # Indexed by HID

        # Also define a current hh dict to store only the existing households
        self.cur_hh_dict = self.hh_dict # At initiation the two dicts are identical
        
        
        
        # Get the variable list for the statistics class
        self.stat_var_list = DataAccess.get_var_list(db, stat_table_name)
        
        # Define a statistics dictionary; indexed by Variable Names
        self.stat_dict = dict()
        
        
        # A counter for debugging
        self.count = 0
        
        
    
        
    




        
    def step_go(self, start_year, end_year, simulation_count):
        
        # Update current year tag
        self.current_year = start_year + simulation_count + 1
                    
        # Then do the followings step by step
        self.agents_update()
        
        self.marriage()
        
        self.child_birth()
        
        # Debugging code
#         print self.count
        


               
            
    def agents_update(self):
        # household and people status update; everything except for marriage and child birth
        
        temp_hh_list = list()
        
        # Annual household status update
        for HID in self.hh_dict:
            temp_hh_list.append(Household.annual_update(self.hh_dict[HID], self.current_year, self.model_parameters_dict))

        # Reset households and current households dicts
        self.hh_dict = dict()
        self.cur_hh_dict = dict()
        
        # Refresh hh_dict and cur_hh_dict
        for h in temp_hh_list:
            self.hh_dict[h.HID] = h                        
            
            if h.is_exist == 1: # Only existing households are added to current hh dict
                self.cur_hh_dict[h.HID] = h
            

    
    def marriage(self):
        
        marry_list = list()
        
        # Get the "to be married this year" list
        for HID in self.cur_hh_dict:
            for PID in self.cur_hh_dict[HID].cur_own_pp_dict:
                p = self.cur_hh_dict[HID].cur_own_pp_dict[PID]
                
                if p.is_married_this_year == True:
                    marry_list.append(p)
                    
        # Make matches
        for pp in marry_list:            
            if pp.is_married_this_year == True:
                # Reset the markers
                found = False
                new_hh = False            
                                
                                    
                if pp.Gender == 1: #Male                
                    # Find him a spouse
                    for sp in marry_list:
                                        
                        if sp.Gender == 0 and pp.HID != sp.HID and sp.is_married_this_year == True: # spouse must be a female and from a different household
                            # Make the match     
                            pp.is_married_this_year = False
                            sp.is_married_this_year = False # Remove the two persons from the "to be married" list
                            
                            found = True
                            break
                    
                    if found == True:
                        pp.IsMarry = 1
                        sp.IsMarry = 1                                                                               
                        pp.SpouseID = sp.PID
                        sp.SpouseID = pp.PID
                                                
                        # Determine whether to establish a new household                
                        siblings = self.get_siblings(pp)
                                
                        if len(siblings) != 0:
                            for sib in siblings:
                                if sib.HID == pp.HID and sib.Age < pp.Age: # If pp has any younger brothers in his household
                                    new_hh = True # Then establish a new household
                            
                        # Assign household affiliation for the new couple 
                        if new_hh == True:                                        
                            # Create a new household with the male pp being the household head
                            self.create_new_household(pp)
                            self.add_person_to_household(sp, pp.HID) # Add sp to the newly created household as pp's spouse
                            
                            # Modify the FatherID/MotherID of any children of pp and sp
                            # And if either one of the new couple has any unmarried children, add them into the new household
                            # Father
                            if self.get_children(pp) is not None:
                                for kid in self.get_children(pp):
                                    kid.MotherID = sp.PID        
                                                                
                                    if kid.IsMarry == 0:
                                        self.add_person_to_household(kid, pp.HID)

                            # Mother                         
                            if self.get_children(sp) is not None:
                                for kid in self.get_children(sp):
                                    kid.FatherID = pp.PID
                                    
                                    if kid.IsMarry == 0:
                                        self.add_person_to_household(kid, pp.HID)
                                                                               
                        else:
                            self.add_person_to_household(sp, pp.HID)
                            # If the female sp has any children, add them into the new household
                            if self.get_children(sp) is not None:
                                for kid in self.get_children(sp):
                                    kid.FatherID = pp.PID
                                    
                                    if kid.IsMarry == 0:
                                        self.add_person_to_household(kid, pp.HID)
                                                            
                    else:
                        # If failed to find a match    
                        pp.is_married_this_year = False                        
                            

                                    
                                              
                else: #Female
                    # Find her a spouse       
                    for sp in marry_list:
    
                        if sp.Gender == 1 and pp.HID != sp.HID and sp.is_married_this_year == True: # spouse must be a female and from a different household
                            # Make the match                    
                            pp.is_married_this_year = False
                            sp.is_married_this_year = False # Remove the two persons from the "to be married" list

                            found = True
                            break
                        
                    if found == True:                    
                        pp.IsMarry = 1
                        sp.IsMarry = 1 
                        pp.SpouseID = sp.PID
                        sp.SpouseID = pp.PID             
                                   
                        # Determine whether to establish a new household                
                        siblings = self.get_siblings(sp)
                                
                        if len(siblings) != 0:
                            for sib in siblings:
                                if sib.HID == sp.HID and sib.Age < sp.Age: # If pp has any younger brothers in his household
                                    new_hh = True # Then establish a new household

                        # Assign household affiliation for the new couple 
                        if new_hh == True:                                        
                            # Create a new household with the male sp being the household head
                            self.create_new_household(sp)
                            self.add_person_to_household(pp, sp.HID) # # Add pp to the newly created household as sp's spouse
                            
                            # Modify the FatherID/MotherID of any children of pp and sp
                            # And if either one of the new couple has any unmarried children, add them into the new household
                            # Mother
                            if self.get_children(pp) is not None:
                                for kid in self.get_children(pp):
                                    kid.FatherID = sp.PID                                    
                                    
                                    if kid.IsMarry == 0:
                                        self.add_person_to_household(kid, sp.HID)

                                                    
                            # Father                         
                            if self.get_children(sp) is not None:
                                for kid in self.get_children(sp):
                                    kid.MotherID = pp.PID
                                    
                                    if kid.IsMarry == 0:                                    
                                        self.add_person_to_household(kid, sp.HID)
                                        
                        else:
                            self.add_person_to_household(pp, sp.HID)
                            # If the female pp has any children, add them into the new household
                            if self.get_children(pp) is not None:
                                for kid in self.get_children(sp):
                                    kid.FatherID = sp.PID
                                    
                                    if kid.IsMarry == 0:
                                        self.add_person_to_household(kid, sp.HID)
                        
                    else:
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
            self.add_person_to_household(new_baby, mom.HID)





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

        new_pp.Gender = self.assign_gender()
        new_pp.Age = 0
        new_pp.R2HHH = self.get_relation_to_hh_head(new_pp, 'child')
        new_pp.IsMarry = 0

        new_pp.MotherID = mom.PID
        new_pp.FatherID = mom.SpouseID
        new_pp.SpouseID = '0'
        
        new_pp.Education = 'uneducated'
#         new_pp.Ethnicity = self.cur_pp_dict[mom.SpouseID].Ethnicity
        
        new_pp.is_alive = 1
        
        
        new_pp.is_college = False
        new_pp.moved_out = False        
        new_pp.is_married_this_year = False
        new_pp.marriage_length = 0        
        new_pp.is_giving_birth_this_year = False
        
        new_pp.StatDate = self.current_year

        return new_pp
    
    
    
    
    
    
    def create_new_household(self, pp):

        # Make a new household instance
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
        pp.R2HHH = '3_00_1'


        # Remove the new household head (pp) from his original household's persons dict
        del self.hh_dict[ori_hid].own_pp_dict[pp.PID]   
        del self.cur_hh_dict[ori_hid].cur_own_pp_dict[pp.PID]
                                          
        # Add the new household head (pp) to new_hh.own_pp_dict and current own pp dict
        new_hh.own_pp_dict[pp.PID] = pp
        new_hh.cur_own_pp_dict[pp.PID] = pp
                  
        # Add the newly created household to Society's household dict
        self.hh_dict[new_hh.HID] = new_hh
        self.cur_hh_dict[new_hh.HID] = new_hh
        



    
    


    
    def add_person_to_household(self, pp, HID):
        # Adding the person pp into the household with HID = HID;
        # r_2_hh_head indicates pp's position when joining the household, of which values include 'spouse', 'child', etc

        if pp.Age != 0: # Not newborn kids
            # Record the original HID
            ori_hid = pp.HID

            # Remove the person from his/her original household's persons dict
            del self.hh_dict[ori_hid].own_pp_dict[pp.PID]          
            del self.cur_hh_dict[ori_hid].cur_own_pp_dict[pp.PID]
            
            
            # Modify the personal properties of the newly added person
            pp.HID = HID
            pp.Hname = self.cur_hh_dict[HID].Hname 
            pp.R2HHH = self.get_relation_to_hh_head(pp, 'spouse')       
            
            # Add the person to household members dict
            self.hh_dict[HID].own_pp_dict[pp.PID] = pp
            self.cur_hh_dict[HID].cur_own_pp_dict[pp.PID] = pp
            
            # If the original household then has no members, mark it as non-exist.
            if len(self.cur_hh_dict[ori_hid].cur_own_pp_dict) == 0:
                self.hh_dict[ori_hid].is_exist = 0
                
                # Also need to delete the dissolved household from current hh dict
                # But should keep its record in the non-current hh_dict
                del self.cur_hh_dict[ori_hid]
        
        
        else: # Newborn kids
            # Add the person to household members dict
            self.hh_dict[HID].own_pp_dict[pp.PID] = pp
            self.cur_hh_dict[HID].cur_own_pp_dict[pp.PID] = pp




    # Dissolve a household with no live members.
    def dissolve_household(self, HID):
                
        # Deal with household properties that were left behind
        self.legacy()



    def legacy(self):
        pass



    
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
        temp_pid_list = list()

        # Find the PIDs in this household that begin with its HID
        for PID in self.hh_dict[pp.HID].own_pp_dict: 
            if PID[:-2] == pp.HID:
                temp_pid_list.append(PID)

        if len(temp_pid_list) != 0:
            temp_pid = max(temp_pid_list)
            new_id_num = int(temp_pid[-2:]) + 1
            
            if int(new_id_num/10) != 0: # if the new id number is in tens
                new_id = pp.HID + str(new_id_num)
            else:
                new_id = pp.HID + '0' + str(new_id_num)
        
        else:
            new_id = pp.HID + '01' # First member in the household with a PID that begins with its own HID
        
        return new_id
    
    

    
    
    # Get all siblings of a person; returned in a list of person instances
    def get_siblings(self, pp):
    
        sibling_list = list()
        
        if pp.FatherID == 0 and pp.MotherID == 0: # Then find siblings within the household by R2HHH
            
            for HID in self.cur_hh_dict:
                if HID == pp.HID:
                    for PID in self.cur_hh_dict[HID].cur_own_pp_dict:
                        sb = self.cur_hh_dict[HID].cur_own_pp_dict[PID]
                        
                        if pp.R2HHH == '3_00_1': # pp is household head

                            if sb.R2HHH == '3_01_1' or sb.R2HHH == '3_02_1' or sb.R2HHH == '3_03_1' or sb.R2HHH == '3_04_1' or sb.R2HHH == '3_05_1':
                                sibling_list.append(sb)
                                
                        elif pp.R2HHH == '4_00_1' or pp.R2HHH == '4_01_1' or pp.R2HHH == '4_02_1' or pp.R2HHH == '4_03_1' or pp.R2HHH == '4_04_1' or pp.R2HHH == '4_05_1' or pp.R2HHH == '4_06_1' or pp.R2HHH == '4_07_1' or pp.R2HHH == '4_08_1' or pp.R2HHH == '4_09_1':
                        # pp is in the 4th generation
                            if sb.R2HHH == '4_00_1' or sb.R2HHH == '4_01_1' or sb.R2HHH == '4_02_1' or sb.R2HHH == '4_03_1' or sb.R2HHH == '4_04_1' or sb.R2HHH == '4_05_1' or sb.R2HHH == '4_06_1' or sb.R2HHH == '4_07_1' or sb.R2HHH == '4_08_1' or sb.R2HHH == '4_09_1':
                                if pp.PID != sb.PID:
                                    sibling_list.append(sb)
                        
                        elif pp.R2HHH == '5_00_1' or pp.R2HHH == '5_01_1' or pp.R2HHH == '5_02_1' or pp.R2HHH =='5_03_1':
                        # pp is in the 5th generation
                            if sb.R2HHH == '5_00_1' or sb.R2HHH == '5_01_1' or sb.R2HHH == '5_02_1' or sb.R2HHH =='5_03_1':
                                if pp.PID != sb.PID:
                                    sibling_list.append(sb)
        
        else:
            if pp.FatherID == 0: # Then find siblings by mother ID
                
                for HID in self.cur_hh_dict:
                    for PID in self.cur_hh_dict[HID].cur_own_pp_dict:
                        sb = self.cur_hh_dict[HID].cur_own_pp_dict[PID]
                        
                        if sb.MotherID == pp.MotherID:
                            sibling_list.append(sb)
            
            else: # Then find siblings by father ID
                
                for HID in self.cur_hh_dict:
                    for PID in self.cur_hh_dict[HID].cur_own_pp_dict:
                        sb = self.cur_hh_dict[HID].cur_own_pp_dict[PID]
                        
                        if sb.FatherID == pp.FatherID:
                            sibling_list.append(sb)
                
        return sibling_list
    

    def get_father(self, pp):
        for HID in self.cur_hh_dict:
            for PID in self.cur_hh_dict[HID].cur_own_pp_dict:
                ff = self.cur_hh_dict[HID].cur_own_pp_dict[PID]
                    
                if ff.PID == pp.FatherID:
                    return ff
        
        # If not found, return None
        return None
                

    def get_mother(self, pp):
        for HID in self.cur_hh_dict:
            for PID in self.cur_hh_dict[HID].cur_own_pp_dict:
                mm = self.cur_hh_dict[HID].cur_own_pp_dict[PID]
                    
                if mm.PID == pp.MotherID:
                    return mm
        
        # If not found, return None
        return None    


    def get_children(self, pp):
        # Define returned list
        kid_list = list()
        
        for HID in self.cur_hh_dict:
            for PID in self.cur_hh_dict[HID].cur_own_pp_dict:
                kid = self.cur_hh_dict[HID].cur_own_pp_dict[PID]
                
                if pp.Gender == 1: # Male
                    if kid.FatherID == pp.PID:
                        kid_list.append(kid)
                else: # Female
                    if kid.MotherID == pp.PID:
                        kid_list.append(kid)
        
        return kid_list

    
#     def get_father(self, pp):
# 
#         if pp.FatherID == 0: # Then find father within the household by R2HHH     
#             
#             for HID in self.cur_hh_dict:
#                 if HID == pp.HID:
#                     for PID in self.cur_hh_dict[HID].cur_own_pp_dict:
#                         ff = self.cur_hh_dict[HID].cur_own_pp_dict[PID]
#                         
#                         if pp.R2HHH == '2_00_1':
#                             if ff.PID == '1_00_1':
#                                 return ff
#                         
#                         if pp.R2HHH == '3_00_1' or pp.R2HHH == '3_01_1' or pp.R2HHH == '3_02_1' or pp.R2HHH == '3_03_1' or pp.R2HHH == '3_04_1' or pp.R2HHH == '3_05_1':
#                             if ff.PID == '2_00_1':
#                                 return ff
#                         
#                         if pp.R2HHH == '4_00_1' or pp.R2HHH == '4_01_1' or pp.R2HHH == '4_02_1' or pp.R2HHH == '4_03_1' or pp.R2HHH == '4_04_1' or pp.R2HHH == '4_05_1' or pp.R2HHH == '4_06_1' or pp.R2HHH == '4_07_1' or pp.R2HHH == '4_08_1' or pp.R2HHH == '4_09_1':
#                             if ff.PID == '3_00_1':
#                                 return ff
#                         
#                         if pp.R2HHH == '5_00_1' or pp.R2HHH == '5_01_1' or pp.R2HHH == '5_02_1' or pp.R2HHH =='5_03_1':
#                             if ff.PID == '4_00_1': # Need elaboration
#                                 return ff
# 
#         
#         else:
#             for HID in self.cur_hh_dict:
#                 for PID in self.cur_hh_dict[HID].cur_own_pp_dict:
#                     ff = self.cur_hh_dict[HID].cur_own_pp_dict[PID]
#                     
#                     if ff.PID == pp.FatherID:
#                         return ff

    # This submodule needs elaboration. 
    def get_relation_to_hh_head(self, pp, role):
        # "Role" indicates as what role the person, pp, is added to the household (thus needs getting the relationship to the household head;
        # There are only two possible roles, child or spouse;
        # If child, the only possible relationships are sons(daughters), grandsons(grand-daughters), grand-grand children, etc;
        # If spouse, the only possible relationships are wives, daughters-in-law, grand-daughters-in-law, etc
        
        relation = ''
        
#         if role == 'child':
#             if self.get_father(pp).R2HHH == '3_00_1':
#                 relation = '4' # Need elaborate
#                 
#             elif self.get_father(pp).R2HHH == '4_00_1': # Need elaborate
#                 relation = '5'
#         
#         else: # spouse
#             if self.cur_hh_dict[pp.HID].cur_own_pp_dict[pp.SpouseID].R2HHH == '3_00_1':
#                 relation = '3_00_0'
#             
#             elif self.cur_hh_dict[pp.HID].cur_own_pp_dict[pp.SpouseID].R2HHH == '4_00_1': # Need elaborate
#                 relation = '4_00_0'
#                 
#             elif self.cur_hh_dict[pp.HID].cur_own_pp_dict[pp.SpouseID].R2HHH == '5_00_1': # Need elaborate
#                 relation = '5_00_0'
                    
        return relation
    
    # Random assign a gender to a newly created Person
    def assign_gender(self):
        return int(round(random.random(), 0))
    
    
    
    