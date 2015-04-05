'''
Created on Mar 25, 2015

@author: Hongmou Zhang; Liyan Xu

Adapted and redeveloped from the original WolongABM Visual Basic program;
by Liyan Xu, Yansheng Yang, Hong You, and Hailong Li;
with major improvements.

'''
from data_access import DataAccess
from household import Household
from society import Society
import main_submodules


dbname = 'C:/20120824/Wolong4Run.mdb'
dbdriver = '{Microsoft Access Driver (*.mdb)}'

model_table_name = 'ModelTable'
household_table_name = 'HouseholdTable_all_selected'
person_table_name = 'PersonTable_all_selected'

#rounds of iteration (years)
simulation_depth=30



'''
 When the database is loaded in the app, do the following.
'''

# Get the working database
db = DataAccess(dbname, dbdriver)

# Get the table pointers
model_table = DataAccess.get_table(db, model_table_name)
household_table = DataAccess.get_table(db, household_table_name)
person_table = DataAccess.get_table(db, person_table_name)



'''
 When "Create Scenario - Run" button is pushed in the app, do the following.
'''

# household_var_list = DataAccess.get_var_list(db, household_table_name)
# household_dict = DataAccess.make_dict(db, household_table, household_var_list)
# person_var_list = DataAccess.get_var_list(db, person_table_name)
# person_dict = DataAccess.make_dict(db, person_table, person_var_list)
#  
# print household_dict['g1c1z001'].Hname
# print person_dict['g1c1z002'].Hname


main_submodules.CreateScenario(db, model_table_name, model_table, household_table_name, household_table, simulation_depth)











