'''
Created on May 11, 2015

@author: xuliy_000
'''

class StatClass(object):
    '''
    This is the statistics class.
    '''

    def __init__(self):
        '''
        Constructor of StatClass
        VarList = {paramName1: paramOrder1, paramName2: paramOrder2, ...}
        '''
        
        self.StatID = ''
        self.ScenarioVersion = ''
        self.StatDate = int()
        self.Variable = ''
        self.StatValue = float()
    
    
#     def get_population_count(self, soc, current_year):
#             
#         stat_record = StatClass()
# 
#         pp_ct = 0
#         
#         # Get the statistics
#         for HID in self.hh_dict:
#             if self.hh_dict[HID].is_exist == 1:
#                 hh_ct += 1 # total household count
#                 
#                 for PID in self.hh_dict[HID].own_pp_dict:
#                     if self.hh_dict[HID].own_pp_dict[PID].is_alive == 1:
#                         pp_ct += 1 # total population
#         
#         # Add population
#         stat_record.ScenarioVersion = 'test'
#         stat_record.StatDate = current_year
#         stat_record.Variable = 'Total_Population'
#         stat_record.StatValue = pp_ct
#         stat_record.StatID = stat_record.Variable + '_' + str(stat_record.StatDate)
#                 
#         self.stat_dict[stat_record.StatID] = stat_record
#         
#         # Add household count
#         stat_record.ScenarioVersion = 'test'
#         stat_record.StatDate = current_year
#         stat_record.Variable = 'Household_Count'
#         stat_record.StatValue = hh_ct
#         stat_record.StatID = stat_record.Variable + '_' + str(stat_record.StatDate)
#                 
#         self.stat_dict[stat_record.StatID] = stat_record     
#         
#         
#     def get_household_count(self, current_year):
# 
#         stat_record = StatClass()
#                 
#         hh_ct = 0
#         pp_ct = 0
#         
#         # Get the statistics
#         for HID in self.hh_dict:
#             if self.hh_dict[HID].is_exist == 1:
#                 hh_ct += 1 # total household count
#                 
#                 for PID in self.hh_dict[HID].own_pp_dict:
#                     if self.hh_dict[HID].own_pp_dict[PID].is_alive == 1:
#                         pp_ct += 1 # total population
#         
#         # Add population
#         stat_record.ScenarioVersion = 'test'
#         stat_record.StatDate = current_year
#         stat_record.Variable = 'Total_Population'
#         stat_record.StatValue = pp_ct
#         stat_record.StatID = stat_record.Variable + '_' + str(stat_record.StatDate)
#                 
#         self.stat_dict[stat_record.StatID] = stat_record
#         
#         # Add household count
#         stat_record.ScenarioVersion = 'test'
#         stat_record.StatDate = current_year
#         stat_record.Variable = 'Household_Count'
#         stat_record.StatValue = hh_ct
#         stat_record.StatID = stat_record.Variable + '_' + str(stat_record.StatDate)
#                 
#         self.stat_dict[stat_record.StatID] = stat_record      
#                  