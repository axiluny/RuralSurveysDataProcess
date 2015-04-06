'''
Created on Mar 26, 2015

@author: xuliy_000
'''
from data_access import DataAccess
from household import Household

# import main


class Society(object):
    '''
    This is the definition of society class
    
    Creating household, person, etc. lists and dictionaries.
    '''
    
    # Define a list to store all the household instances
    hh_list = list()


    def __init__(self, db, model_table_name, model_table, hh_table_name, hh_table, pp_table_name, pp_table):
        '''
        Constructor

        '''
        self.model_var_list = DataAccess.get_var_list(db, model_table_name)
        self.model_table = DataAccess.get_table(db, model_table_name)
        # Define and give value to Model variables
        
        self.hh_var_list = DataAccess.get_var_list(db, hh_table_name)
#         self.hh_dict = DataAccess.make_dict(db, hh_table, self.hh_var_list)
        
        # Add household instances to hh_list
        for hh in hh_table:
            hh_temp = Household(hh, self.hh_var_list, db, pp_table_name, pp_table)
            self.hh_list.append(hh_temp)

        
    def step_go(self):
        for hh in self.hh_list:
            Household.step_go(hh)
            
    
        


