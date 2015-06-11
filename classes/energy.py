'''
Created on Jun 10, 2015

@author: xuliy_000
'''

class Energy(object):
    '''
    The Energy Class.
    '''


    def __init__(self):
        '''
        '''
        self.hh_energy_type = 0
        
        self.energy_demand = 0
        self.electricity_consumption = 0
        self.firewood_consumption = 0
        self.carbon_footprint = 0
    
    
    
    def annual_energy_step_go(self, hh, model_parameters):
        
        self.get_household_energy_type(hh, model_parameters)
        self.get_energy_demand(hh, model_parameters)
        self.get_electricity_consumption(hh, model_parameters)
        self.get_firewood_consumption(hh, model_parameters)
    
        self.get_carbon_footprint(hh, model_parameters)
        self.get_firewood_collection_area(hh, model_parameters)
    
    
    
    def get_household_energy_type(self, hh, model_parameters):
        pass
    
    
    def get_energy_demand(self, hh, model_parameters):
        pass
    
    
    def get_electricity_consumption(self, hh, model_parameters):
        pass
    
    
    def get_firewood_consumption(self, hh, model_parameters):
        pass
    
    
    def get_carbon_footprint(self, hh, model_parameters):
        pass
    
    
    def get_firewood_collection_area(self, hh, model_parameters):
        pass
    