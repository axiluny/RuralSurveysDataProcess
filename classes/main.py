'''
Created on Mar 25, 2015

@author: Hongmou Zhang; Liyan Xu

Adapted and redeveloped from the original WolongABM Visual Basic program;
by Liyan Xu, Yansheng Yang, Hong You, and Hailong Li;
with major improvements.

'''
from data_access import DataAccess
import main_submodules


dbname = 'C:/WolongRun/WolongDB.mdb'
dbdriver = '{Microsoft Access Driver (*.mdb)}'

model_table_name = 'ModelTable'
household_table_name = 'HouseholdTable'
person_table_name = 'PersonTable'

# Rounds of iteration (years)
simulation_depth = 2

# Starting and ending year of simulation
start_year = 2015
end_year = 2030


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


main_submodules.CreateScenario(db, model_table_name, model_table, household_table_name, household_table, person_table_name, person_table, simulation_depth, start_year, end_year)










