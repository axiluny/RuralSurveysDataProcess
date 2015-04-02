'''
Created on Mar 26, 2015

@author: xuliy_000
'''
from data_access import DataAccess
import main


class Society(object):
    '''
    This is the definition of society class
    
    Creating household, person, etc. lists and dictionaries.
    '''


    def __init__(self, hh_table):
        '''
        Constructor

        '''
        household_var_list = DataAccess.get_var_list(main.db, main.household_table_name)
        household_dict = DataAccess.make_dict(main.db, hh_table, household_var_list)
        
        print household_dict['g1c1z001'].Hname
        
    def StepGo(self):
        pass
        


