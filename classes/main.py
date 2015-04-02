'''
Created on Mar 25, 2015

@author: Hongmou Zhang; Liyan Xu

Adapted and redeveloped from the original WolongABM Visual Basic program;
by Liyan Xu, Yansheng Yang, Hong You, and Hailong Li;
with major improvements.

'''

from data_access import DataAccess
from household import Household
from main_submodules import CreateScenario


dbname = 'C:/20120824/Wolong4Run.mdb'
dbdriver = '{Microsoft Access Driver (*.mdb)}'
household_table_name = 'HouseholdTable_all_selected'

#rounds of iteration (years)
simulation_depth=30


# Get the database
def reset_DB():
    database = DataAccess(dbname, dbdriver)
    return database

# Initialize system: load data from database; return the pointers.
def __init__():
    
    household_var_list = DataAccess.get_var_list(db, household_table_name)
    household_table = DataAccess.get_table(db,household_table_name)
    household_dict = DataAccess.make_dict(db, household_table, household_var_list)
    
    return household_table

#     print household_var_list
#     print household_dict['g1c1z001'].Hname

    '''
     How to cite these variables outside this module?
    '''

db = reset_DB()
household_table = __init__()



CreateScenario(household_table, simulation_depth)










