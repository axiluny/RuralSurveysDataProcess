'''
Created on Mar 26, 2015

@author: Liyan Xu; Hongmou Zhang
'''
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
        self.model_var_list = DataAccess.get_var_list(db, model_table_name)
        self.model_parameters_dict = dict()
        
        for record in model_table:
            self.model_parameters_dict[record.Variable_Name] = record.Variable_Value

        # How to cite a model parameter        
#         print self.model_parameters_dict['SecondarySchoolCostPerKidII']
           
        
        # Get the variable lists for household and person classes 
        self.hh_var_list = DataAccess.get_var_list(db, hh_table_name)
        self.pp_var_list = DataAccess.get_var_list(db, pp_table_name)


        # Define a list to store all the household instances, and a dictionary to store and index all the household instances
        self.hh_list = list()
        self.hh_dict = dict()
                
        # Add household instances to hh_list and hh_dict
        for hh in hh_table:
            hh_temp = Household(hh, self.hh_var_list, db, pp_table_name, pp_table)
            self.hh_list.append(hh_temp)
            self.hh_dict[hh_temp.HID] = hh_temp # Indexed by HID
     

        # Define a list to store all the person instances and a dictionary to store and index all the person instances
        self.pp_list = list()
        self.pp_dict = dict()
        
        # Add person instances to pp_list and pp_dict
        for pp in pp_table:
            pp_temp = Person(pp, self.pp_var_list)
            self.pp_list.append(pp_temp)
            self.pp_dict[pp_temp.PID] = pp_temp # Indexed by PID

        
    def step_go(self, start_year, end_year, simulation_count, db, hh_table_name, hh_table, pp_table_name, pp_table,):
        
        self.current_year = start_year + simulation_count
        self.cur_hh_list = list()
        self.cur_hh_dict = dict()
        
        self.cur_pp_list = list()
        self.cur_pp_dict = dict()
        
        for hh in self.hh_list:
            temp_list = Household.step_go(hh, self.current_year, db, hh_table_name, hh_table, pp_table_name, pp_table, self.model_parameters_dict)
               
            for h in temp_list:
                self.cur_hh_list.append(h)
                self.cur_hh_dict[h.HID] = h
                
                for p in h.own_pp_list:
                    self.cur_pp_list.append(p)
                    self.cur_pp_dict[p.PID] = p
             
             
        self.hh_list = self.cur_hh_list            
        self.hh_dict = self.cur_hh_dict # Indexed by HID        
        
        self.pp_list = self.cur_pp_list
        self.pp_dict = self.cur_pp_dict # Indexed by PID
          
    
        


