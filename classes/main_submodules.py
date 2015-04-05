'''
Created on Mar 26, 2015

@author: xuliy_000
'''
from data_access import DataAccess
from society import Society
from household import Household




def CreateScenario(db, model_table_name, model_table, hh_table_name, hh_table, simulation_depth):
    #Initialize society: create household, person, etc dictionaries
    soc = Society(db, model_table_name, model_table, hh_table_name, hh_table)
 
    print soc.hh_dict['g1c1z001'].Hname
    a = soc.model_table
    print a[1]
    
    #Start simulation
    
#     for i in range(simulation_depth):
#         StepGo()
#         DataAccess.SaveResultsToDB()


def StepGo():
    Society.StepGo()
    #Then update Tables
    #Then do statistics





  






