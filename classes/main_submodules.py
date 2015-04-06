'''
Created on Mar 26, 2015

@author: xuliy_000
'''
from data_access import DataAccess
from society import Society
from household import Household


def step_go(society_instance):

    #Do statistics and add records to stat table in database
#     DataAccess.add_stat_results(society_instance)
    
    # Do the simulation
    Society.step_go(society_instance)
    
    # Then save updated tables in database
#     DataAccess.save_results_to_db(society_instance)



def CreateScenario(db, model_table_name, model_table, hh_table_name, hh_table, pp_table_name, pp_table, simulation_depth):
    
    # Initialize society: create society, household, person, etc instances
    soc = Society(db, model_table_name, model_table, hh_table_name, hh_table, pp_table_name, pp_table)

    '''
     Debug Codes
    ''' 
#     print soc.hh_dict['g1c1z001'].Hname
#     a = soc.model_table
#     print a[1]
# 
#     print soc.hh_list[1].Hname
#     print soc.hh_list[1].pp_var_list[2]
#     print soc.hh_list[0].pp_list[0].Hname
#     print soc.hh_list[1].pp_list[1].IdentityID
#     for hh in soc.hh_list:
#         print hh.Hname
#     for pp in soc.hh_list[0].pp_list:
#         print pp.Pname

    
    #Start simulation

#     i = 0
#     for i in range(simulation_depth):
#         step_go(soc)
#         i = i + 1










  






