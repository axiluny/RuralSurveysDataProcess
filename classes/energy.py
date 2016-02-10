'''
Created on Jun 10, 2015

@author: xuliy_000
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
        
        self.energy_demand = exp (6.069 + 0.205 * self.hh_energy_type + 0.05 * hh.own_capital_properties.hh_size + 
                                  0.009 * hh.own_capital_properties.house_rooms) / 0.18
        
    
    
    def get_electricity_consumption(self, hh, model_parameters):
        
        # If the household has engaged in the lodging business
        is_lodging = int()
        
        if hh.own_capital_properties.lodging_income != 0:
            is_lodging = 1
        else:
            is_lodging = 0
        

        # Calculate electricity consumption
        electricity_demand = float()
                
        electricity_demand = exp (5.684 + 0.216 * self.hh_energy_type + 0.072 * hh.own_capital_properties.house_area + 
                                            0.447 * is_lodging / float(model_parameters['ElectricitySubsidisedPrice']) 
        
        
        if electricity_demand <= self.energy_demand:
            self.electricity_consumption = electricity_demand

        else:
            self.electricity_consumption = self.energy_demand
            
                
    
    def get_firewood_consumption(self, hh, model_parameters):
        
        # GetFirewoodConsumption = (m_dEnergyDemand - m_dElectricityConsumption) * m_clsSociety.ElectricityToFirewoodRatio
        
        pass
    
    
    def get_carbon_footprint(self, hh, model_parameters):
        
        # GetCarbonFootprint = m_dElectricityConsumption * m_clsSociety.ElectricityToCarbon + m_dFirewoodConsumption * m_clsSociety.FirewoodToCarbon
        
        pass
    
    
    def get_firewood_collection_area(self, hh, model_parameters):
        pass
    