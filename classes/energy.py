'''
Created on Jun 10, 2015

@author: xuliyan
'''

import math


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
        self.firewood_consumption_in_kwh = 0
        self.carbon_footprint = 0
    
    
    
    def energy_step_go(self, hh, model_parameters):
        
        self.get_household_energy_type(hh, model_parameters)
        self.get_energy_demand(hh, model_parameters)
        self.get_electricity_consumption(hh, model_parameters)
        self.get_firewood_consumption(hh, model_parameters)
    
        self.get_carbon_footprint(hh, model_parameters)
        self.get_firewood_collection_area(hh, model_parameters)
    
    
    
    def get_household_energy_type(self, hh, model_parameters):
        
        if hh.business_type == 0:
            self.hh_energy_type = 1
            
        elif hh.business_type == 1:
            self.hh_energy_type = 2
        
        else:
            self.hh_energy_type = 3
    
    
    
    
    def get_energy_demand(self, hh, model_parameters):
        
        self.energy_demand = math.exp ((6.069 + 0.205 * self.hh_energy_type + 0.05 * hh.own_capital_properties.hh_size + 
                                  0.009 * hh.own_capital_properties.house_rooms)) / 0.18
        


    
    
    def get_electricity_consumption(self, hh, model_parameters):
        
        # If the household has engaged in the lodging business
        is_lodging = int()
        
        if hh.own_capital_properties.lodging_income != 0:
            is_lodging = 1
        else:
            is_lodging = 0
        
        # Calculate potential electricity demand
        potential_elec_demand = math.exp ((5.684 + 0.216 * self.hh_energy_type + 0.072 * hh.own_capital_properties.hh_size +
                                     0.447 * is_lodging)) / float(model_parameters['ElectricitySubsidisedPrice'])
        
        # Get the actual electricity consumption
        if potential_elec_demand <= self.energy_demand:
            self.electricity_consumption = potential_elec_demand
        else:
            self.electricity_consumption = self.energy_demand
                
    
    
    def get_firewood_consumption(self, hh, model_parameters):
        
        self.firewood_consumption = (self.energy_demand - self.electricity_consumption) * float(model_parameters['ElectricityToFirewoodRatio'])
        self.firewood_consumption_in_kwh = self.energy_demand - self.electricity_consumption

    
    
    def get_carbon_footprint(self, hh, model_parameters):
        
        self.carbon_footprint = (self.electricity_consumption * float(model_parameters['ElectricityToCarbon']) + 
                                 self.firewood_consumption * float(model_parameters['FirewoodToCarbon']))
        
    
    
    def get_firewood_collection_area(self, hh, model_parameters):
        pass
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    