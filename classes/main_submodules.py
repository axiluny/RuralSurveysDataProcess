'''
Created on Mar 26, 2015

@author: xuliy_000
'''
from data_access import DataAccess
from society import Society
from household import Household



def CreateScenario(hh_table, simulation_depth):
    #Initialize society: create household, person, etc dictionaries
    soc = Society(hh_table)
    
    #Start simulation
    
#     for i in range(simulation_depth):
#         StepGo()
#         DataAccess.SaveResultsToDB()


def StepGo():
    Society.StepGo()
    #Then update Tables
    #Then do statistics





  






