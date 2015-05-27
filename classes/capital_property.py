'''
Created on May 26, 2015

@author: Liyan Xu
'''

from land import *


class CapitalProperty(object):
    '''
    Households' factors of production: properties and related behaviors
    '''


    def __init__(self, hh):
        '''
        hh = an instance of the household class.
        '''
        
        # Monetary assets and liabilities
        self.cash = hh.Capital
        self.debt  = hh.TotalLoan
        self.lending = 0
        
        
        # Land properties
        self.land_properties = Land(hh)
        
        self.farmland = hh.FarmlandAreaAfter
        self.location_type = hh.LocType # Location types: 1 - hilly; 0 - plain.
        
        if self.location_type == 1:
            self.old_homestead = hh.Homestead
        else: # Temporary adding these two lines to ensure all hh have same capital property structures
            self.old_homestead = 0       
        
        self.buildings_area = hh.RebuildHouseArea        
        self.building_rooms = int(self.buildings_area/30) # buildings in numbers of rooms; 30 m^2 per room
        
        if self.buildings_area < 200:
            self.homestead = self.buildings_area
        elif self.buildings_area >= 200 and self.buildings_area <400:
            self.homestead = self.buildings_area / 2
        else:
            self.homestead = self.buildings_area / 3
        
        
        # Labor (Human capitals)
        self.labor = int()
        self.male_labor = int()
        self.female_labor = int()
        self.young_male_labor = int()
        
        self.update_labors(hh)

                
                
        # Other specific factors of production
        self.minibus = hh.Minibus
        self.truck = hh.Truck
        self.tractor = hh.Tractor
        
        
        # Policy-related factors
        self.land_policy = hh.LandPolicy
        self.pre_farm_to_forest = hh.PreReturnToForest
        self.pre_farm_to_bamboo = hh.PreReturnToBamboo
        self.pre_occupied_farm = hh.ExchangedLandArea
        self.is_tianbao = hh.IsTianbao
        
        self.farm_to_forest = 0 # A "container" to store the FTF area incurred during simulation
        
        
        # Available factors; temporary "containers" during simulation
        self.av_farmland = float()
        self.av_homestead = float()
        self.av_rooms = int()
        self.av_room_areas = float()
        self.av_minibus = int()
        self.av_truck = int()
        self.av_tractor = int()
        self.av_labor = float()
        self.av_male_labor = float()
        self.av_female_labor = float()
        self.av_young_male_labor = float()
        
        self.labor_cost = float() # temporary variable during simulation
        
        
        # Income variables; temporary variables during simulation
        self.agriculture_income = float()
        self.temp_job_income = float()
        self.freight_trans_income = float()
        self.passenger_trans_income = float()
        self.tracor_trans_income = float()
        self.lodging_income = float()
        self.private_business_income = float()
        self.lending_income = float()
        self.renting_income = float()
        
    
    
    
    def refresh(self, hh):
        '''
        Refresh household's own factors every year after demographics simulation but before economic activities simulation
        Reset the temporary variables (available factors and incomes)
        Update labor status (changed as a result of the demographics simulation
        All other factor variables (household's existing factor properties) remain unchanged
        '''
                
        # Update labors
        self.update_labors(hh)
        
        # Reset available factors
        self.av_farmland = self.farmland
        self.av_homestead = self.homestead
        self.av_rooms = (self.buildings_area - self.homestead) / 30
        self.av_minibus = self.minibus
        self.av_truck = self.truck
        self.av_tractor = self.tractor
        self.av_labor = self.labor
        self.av_male_labor = self.male_labor
        self.av_female_labor = self.female_labor
        self.av_young_male_labor = self.young_male_labor
        
        self.labor_cost = 0
        
        
        # Reset Incomes
        self.agriculture_income = 0
        self.temp_job_income = 0
        self.freight_trans_income = 0
        self.passenger_trans_income = 0
        self.tracor_trans_income = 0
        self.lodging_income = 0
        self.private_business_income = 0
        self.lending_income = 0
        self.renting_income = 0        
        
    
    def update_labors(self, hh):
        
        self.labor = 0
        self.male_labor = 0
        self.female_labor = 0
        self.young_male_labor = 0
        
        
        for PID in hh.own_pp_dict:
            if hh.own_pp_dict[PID].is_alive == 1:
                if hh.own_pp_dict[PID].Age >= 18: # For now, no upper age limit
                    self.labor += 1
                    
                    if hh.own_pp_dict[PID].Gender == 1:
                        self.male_labor += 1
                        if hh.own_pp_dict[PID].Age <= 45:
                            self.young_male_labor += 1
                    else:
                        self.female_labor += 1        
        
    
    def merge_capital_properties(self, soc, out_HID, in_HID):
        '''
        Merge one household's (out_HID) all capital properties (self) into another's (in_HID)
        self is the household with HID "out_HID"
        '''
        
        for item in self.__dict__:
            if item != 'land_properties':
            # land_properties is a LandClass object and cannot be simply added to each other; Deal with them later
                          
#                 if soc.hh_dict[in_HID] is not None:
                soc.hh_dict[in_HID].own_capital_properties.__dict__[item] = soc.hh_dict[in_HID].own_capital_properties.__dict__[item] + self.__dict__[item]
                
                # Then reset the original household's capital properties in hh_dict
                self.__dict__[item] = 0
            
            else:
                # Deal with the land properties
                pass
        
        

            
        