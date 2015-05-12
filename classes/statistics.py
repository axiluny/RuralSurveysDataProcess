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
        '''
        
        self.StatID = ''
        self.ScenarioVersion = ''
        self.StatDate = int()
        self.Variable = ''
        self.StatValue = float()
    
    
    
    
    def get_population_count(self, soc, scenario_name):
         
        pp_ct = 0
         
        # Get the statistics
        for HID in soc.hh_dict:
            if soc.hh_dict[HID].is_exist == 1:
                 
                for PID in soc.hh_dict[HID].own_pp_dict:
                    if soc.hh_dict[HID].own_pp_dict[PID].is_alive == 1:
                        pp_ct += 1 # total population
         
        # Add population
        self.ScenarioVersion = scenario_name
        self.StatDate = soc.current_year 
        self.Variable = 'Total_Population'
        self.StatValue = pp_ct
        self.StatID = self.Variable + '_' + str(self.StatDate)
                 
        soc.stat_dict[self.StatID] = self



    def get_household_count(self, soc, scenario_name):
         
        hh_ct = 0
         
        # Get the statistics
        for HID in soc.hh_dict:
            if soc.hh_dict[HID].is_exist == 1:
                
                hh_ct += 1 # total (existing) household count
                 
         
        # Add population
        self.ScenarioVersion = scenario_name
        self.StatDate = soc.current_year 
        self.Variable = 'Household_Count'
        self.StatValue = hh_ct
        self.StatID = self.Variable + '_' + str(self.StatDate)
                 
        soc.stat_dict[self.StatID] = self
