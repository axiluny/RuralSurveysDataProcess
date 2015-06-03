'''
Created on May 30, 2015

@author: Liyan Xu
'''

import copy
import random


class BusinessSector(object):
    '''
    The business sectors class
    '''


    def __init__(self, record, VarList):
        '''
        
        '''
        
        # Set the attributes (var) and their values (record) from the business sector table in the DB.                
        for var in VarList:
            setattr(self, var[0], record[var[1]])
            
        
        self.own_cash_percent = 0.8




    def is_available(self, capital, risk_type):
        
        if self.SectorName == 'Agriculture':
            if (365* capital.labor - self.LaborCost * capital.av_farmland) > 0 and capital.av_farmland > 0:
                return True
            
        elif self.SectorName == 'TempWork':
            if (365* capital.male_labor - self.LaborCost) > 0:
                return True

        elif self.SectorName == 'FreightTrans':
            if capital.av_male_labor > 0:
                if capital.av_truck > 0:
                    return True
                elif capital.cash > self.EntryThreshold:
                    return True
                elif capital.cash > self.EntryThreshold * self.own_cash_percent and capital.debt <= 0 and risk_type == False:
                    return True

        elif self.SectorName == 'PassengerTrans':
            if capital.av_male_labor > 0:
                if capital.av_minibus > 0:
                    return True
                elif capital.cash > self.EntryThreshold:
                    return True
                elif capital.cash > self.EntryThreshold * self.own_cash_percent and capital.debt <= 0 and risk_type == False:
                    return True

        elif self.SectorName == 'TractorTrans':
            if capital.av_male_labor > 0:
                if capital.av_tractor > 0:
                    return True
                elif capital.cash > self.EntryThreshold:
                    return True
                elif capital.cash > self.EntryThreshold * self.own_cash_percent and capital.debt <= 0 and risk_type == False:
                    return True
  
        elif self.SectorName == 'Lodging':
            if capital.av_male_labor > 0:
                if capital.cash > self.EntryThreshold:
                    return True
                elif capital.cash > self.EntryThreshold * self.own_cash_percent and capital.debt <= 0 and risk_type == False:
                    return True
     
        elif self.SectorName == 'PrivateBusiness':
            if capital.av_male_labor > 0:
                if capital.cash > self.EntryThreshold:
                    return True
                
        elif self.SectorName == 'Lending':
            if capital.cash > self.EntryThreshold and capital.debt <= 0:
                return True
 
        elif self.SectorName == 'Renting':
            if capital.av_rooms > 0:
                return True          


    def calculate_business_revenue(self, capital, risk_type, risk_effective, model_parameters):
        '''
        capital: household's own capital properties (factors of production) i.e. household_class.own_capital_properties
        risk_type: household's attitude toward risks. True - risk aversion; False - risk appetite;
        risk_effective: whether the random risk factor takes effect in the calculation. True - real world; False: hypothetical.
        '''
        
        # Make a new capital instance as a temporary variable
        new_capital = copy.deepcopy(capital)
        
        # Define other temporary variables
        revenue = float()
        max_farm = float()
        max_labor = float()
        max_cash = float()
        max_vehicle = float()
        loan = float()
        floor_cost = float()
        new_room = float()
        lodging_rooms = int()
        private_business_rooms = int()
        lending_amount = float()
        
        
        if self.SectorName == 'Agriculture':
            '''
            Formula: revenue * [1 - risk_factor * rnd(-1, 1)] * farmland_area * location_factor * neighborhood_factor
            # Temporarily not including the neighborhood factor
            '''
            
            # Find the specific labor cost as determined by the household's terrain type.
            if capital.location_type == 1: # hilly
                spec_labor_cost = self.LaborCost + 18
            else: # plain
                spec_labor_cost = self.LaborCost - 8
            
            # Find the maximum farm land area cultivatable as permitted by the household's available labor.
            max_farm = (new_capital.av_labor * 365) / spec_labor_cost            
            if max_farm > new_capital.av_farmland:
                max_farm = new_capital.av_farmland
            
            # Calculate the revenue.
            if risk_effective == True:
                revenue = self.Revenue * (1 - (1 - 2 * random.random()) * self.Risk) * max_farm * (1 - capital.location_type * 0.2)
            else:
                if risk_type == True:
                    revenue = self.Revenue * (1 - self.Risk) * max_farm * (1 - capital.location_type * 0.2)
                else:
                    revenue = self.Revenue * (1 + self.Risk) * max_farm * (1 - capital.location_type * 0.2)
            
            # Update household's capital properties
            new_capital.av_farmland = self.plus(new_capital.av_farmland - max_farm)
            new_capital.av_labor = self.plus(new_capital.av_labor - max_farm * spec_labor_cost / 365)
            
            new_capital.labor_cost += max_farm * spec_labor_cost / 365
            new_capital.agriculture_income += revenue
            new_capital.cash += revenue
            
            
        elif self.SectorName == 'TempWork':
            '''
            Formula: revenue * [1 - risk_factor * rnd(-1, 1)] * labor_inputs
            # labor_inputs - in days
            '''
            
            max_labor = new_capital.av_young_male_labor
            
            if risk_effective == True:
                revenue = self.Revenue * (1 + (1 - 2 * random.random()) * self.Risk) * self.LaborCost * max_labor
            else:
                if risk_type == True:
                    revenue = self.Revenue * (1 - self.Risk) * self.LaborCost * max_labor
                else:
                    revenue = self.Revenue * (1 + self.Risk) * self.LaborCost * max_labor
            
            new_capital.av_labor = self.plus(new_capital.av_labor -  max_labor * self.LaborCost / 365)
            new_capital.av_male_labor = self.plus(new_capital.av_male_labor - max_labor * self.LaborCost / 365)
            new_capital.av_young_male_labor = self.plus(new_capital.av_young_male_labor - max_labor * self.LaborCost / 365)
            
            new_capital.labor_cost += self.LaborCost * max_labor / 365
            new_capital.temp_job_income += revenue
            new_capital.cash += revenue


        elif self.SectorName == 'FreightTrans':
            '''
            Formula: revenue * [1 - risk_factor * rnd(-1, 1)] * truck_num
            '''
            
            # Consider whether to purchase a truck first
            if new_capital.av_male_labor > new_capital.av_truck:
                # If the household has spare male labor
                loan = 0
                
                if new_capital.cash < self.EntryThreshold:
                    # household's own cash capital is insufficient for buying a truck
                    if risk_type == False:
                        # only the risk appetite household would raise loans
                        if new_capital.debt <= 0:
                            if new_capital.cash >= self.EntryThreshold * self.own_cash_percent:
                                loan = self.EntryThreshold - new_capital.cash
                                
                                if risk_effective == True:
                                    # refresh household's capital properties only in the real world case;
                                    new_capital.cash = 0
                                
                                new_capital.debt += loan
                                new_capital.truck += 1
                                new_capital.av_truck += 1
                
                else:
                    # household can afford a new truck without raising loans
                    if risk_effective == True:
                        new_capital.cash = new_capital.cash - self.EntryThreshold
        
                    new_capital.truck += 1
                    new_capital.av_truck += 1
            
            # one male labor matches one truck
            if new_capital.av_male_labor < new_capital.av_truck:
                max_vehicle = new_capital.av_male_labor
            else:
                max_vehicle = new_capital.av_truck
            
            # Do the business
            if risk_effective == True:
                revenue = self.Revenue * (1 + (1 - 2 * random.random()) * self.Risk) * max_vehicle
            else:
                if risk_type == True:
                    revenue = self.Revenue * (1 - self.Risk) * max_vehicle
                else:
                    revenue = self.Revenue * (1 + self.Risk) * max_vehicle
            
            # Update household's capital properties
            new_capital.av_labor = self.plus(new_capital.av_labor - max_vehicle * self.LaborCost / 365)
            new_capital.av_male_labor = self.plus(new_capital.av_male_labor - max_vehicle * self.LaborCost / 365)
            
            new_capital.labor_cost += max_vehicle * self.LaborCost / 365
            new_capital.av_truck = self.plus(new_capital.truck - max_vehicle)
            
            new_capital.freight_trans_income += revenue
            new_capital.cash += revenue
                    


        elif self.SectorName == 'PassengerTrans':
            '''
            Formula: revenue * [1 - risk_factor * rnd(-1, 1)] * passenger_car_num
            '''
            
            # Consider whether to purchase a minibus first
            if new_capital.av_male_labor > new_capital.av_minibus:
                # If the household has spare male labor
                loan = 0
                
                if new_capital.cash < self.EntryThreshold:
                    # household's own cash capital is insufficient for buying a minibus
                    if risk_type == False:
                        # only the risk appetite household would raise loans
                        if new_capital.debt <= 0:
                            if new_capital.cash >= self.EntryThreshold * self.own_cash_percent:
                                loan = self.EntryThreshold - new_capital.cash
                                
                                if risk_effective == True:
                                    # refresh household's capital properties only in the real world case;
                                    new_capital.cash = 0
                                
                                new_capital.debt += loan
                                new_capital.minibus += 1
                                new_capital.av_minibus += 1
                
                else:
                    # household can afford a new minibus without raising loans
                    if risk_effective == True:
                        new_capital.cash = new_capital.cash - self.EntryThreshold
        
                    new_capital.minibus += 1
                    new_capital.av_minibus += 1
            
            # one male labor matches one minibus
            if new_capital.av_male_labor < new_capital.av_minibus:
                max_vehicle = new_capital.av_male_labor
            else:
                max_vehicle = new_capital.av_minibus
            
            # Do the business
            if risk_effective == True:
                revenue = self.Revenue * (1 + (1 - 2 * random.random()) * self.Risk) * max_vehicle
            else:
                if risk_type == True:
                    revenue = self.Revenue * (1 - self.Risk) * max_vehicle
                else:
                    revenue = self.Revenue * (1 + self.Risk) * max_vehicle
            
            # Update household's capital properties
            new_capital.av_labor = self.plus(new_capital.av_labor - max_vehicle * self.LaborCost / 365)
            new_capital.av_male_labor = self.plus(new_capital.av_male_labor - max_vehicle * self.LaborCost / 365)
            
            new_capital.labor_cost += max_vehicle * self.LaborCost / 365
            new_capital.av_minibus = self.plus(new_capital.minibus - max_vehicle)
            
            new_capital.passenger_trans_income += revenue
            new_capital.cash += revenue


        elif self.SectorName == 'TractorTrans':
            '''
            Formula: revenue * [1 - risk_factor * rnd(-1, 1)] * tractor_num
            '''
             
            # Consider whether to purchase a tractor first
            if new_capital.av_male_labor > new_capital.av_tractor:
                # If the household has spare male labor
                loan = 0
                 
                if new_capital.cash < self.EntryThreshold:
                    # household's own cash capital is insufficient for buying a tractor
                    if risk_type == False:
                        # only the risk appetite household would raise loans
                        if new_capital.debt <= 0:
                            if new_capital.cash >= self.EntryThreshold * self.own_cash_percent:
                                loan = self.EntryThreshold - new_capital.cash
                                 
                                if risk_effective == True:
                                    # refresh household's capital properties only in the real world case;
                                    new_capital.cash = 0
                                 
                                new_capital.debt += loan
                                new_capital.tractor += 1
                                new_capital.av_tractor += 1
                 
                else:
                    # household can afford a new tractor without raising loans
                    if risk_effective == True:
                        new_capital.cash = new_capital.cash - self.EntryThreshold
         
                    new_capital.tractor += 1
                    new_capital.av_tractor += 1
             
            # one male labor matches one tractor
            if new_capital.av_male_labor < new_capital.av_tractor:
                max_vehicle = new_capital.av_male_labor
            else:
                max_vehicle = new_capital.av_tractor
             
            # Do the business
            if risk_effective == True:
                revenue = self.Revenue * (1 + (1 - 2 * random.random()) * self.Risk) * max_vehicle
            else:
                if risk_type == True:
                    revenue = self.Revenue * (1 - self.Risk) * max_vehicle
                else:
                    revenue = self.Revenue * (1 + self.Risk) * max_vehicle
             
            # Update household's capital properties
            new_capital.av_labor = self.plus(new_capital.av_labor - max_vehicle * self.LaborCost / 365)
            new_capital.av_male_labor = self.plus(new_capital.av_male_labor - max_vehicle * self.LaborCost / 365)
             
            new_capital.labor_cost += max_vehicle * self.LaborCost / 365
            new_capital.av_tractor = self.plus(new_capital.minibus - max_vehicle)
             
            new_capital.tractor_trans_income += revenue
            new_capital.cash += revenue

  
        elif self.SectorName == 'Lodging':
            '''
            Formula: revenue * (1 - rnd(0, 1) * risk_factor) * lodging_rooms
            risk_factor indicates un-occupancy rate. risk_factor = 0 indicate full occupancy.
            '''
            
            # Consider whether to build new rooms first
            floor_cost = new_capital.homestead * float(model_parameters['HomesteadAreaCost'])
            
            if new_capital.homestead > 0:
                if new_capital.buildings_area / new_capital.homestead < 6: # maximum 6 floors
                    
                    loan = 0
                    if new_capital.cash < floor_cost: # Own fund insufficient for building a new floor
                        if risk_type == False:
                            if new_capital.debt <= 0: 
                                if new_capital.cash > floor_cost * self.own_cash_percent:
                                    loan = floor_cost - new_capital.cash
                                    
                                    if risk_effective == True:
                                        new_capital.cash = 0
                                    
                                    new_capital.debt += loan
                                    new_room = new_capital.homestead
                                else:
                                    new_room = 0
                    else:
                        if risk_effective == True:
                            new_capital.cash = new_capital.cash - floor_cost
                        
                        new_room = new_capital.homestead
                
                    
                    new_capital.buildings_area += new_room
                    new_capital.building_rooms += new_room / float(model_parameters['RoomArea'])
                    new_capital.av_rooms += new_room / float(model_parameters['RoomArea'])
            
            
            # Determine maximum scale of business
            if new_capital.av_rooms > new_capital.av_labor * 365 / self.LaborCost:
                lodging_rooms = int(new_capital.av_labor * 365 / self.LaborCost)
            else:
                lodging_rooms = int(new_capital.av_rooms)
                            
            # Do the business
            if risk_effective == True:
                revenue = self.Revenue * (1 - random.random() * self.Risk) * lodging_rooms
            else:
                if risk_type == True:
                    revenue = self.Revenue * (1 - self.Risk) * lodging_rooms
                else:
                    revenue = self.Revenue * lodging_rooms
                                    
            # Update household's capital properties
            new_capital.av_labor = self.plus(new_capital.av_labor - lodging_rooms * self.LaborCost / 365)
            
            new_capital.labor_cost += lodging_rooms * self.LaborCost / 365
            new_capital.av_rooms = self.plus(new_capital.av_rooms - lodging_rooms)
            
            new_capital.lodging_income += revenue
            new_capital.cash += revenue            
            
            
            
     
        elif self.SectorName == 'PrivateBusiness':
            '''
            Formula: revenue * (1 - rnd(-1, 1) * risk_factor) * private_business_rooms
            '''
            
            # Determine maximum scale of business
            if new_capital.av_rooms > new_capital.av_labor * 365 / self.LaborCost:
                private_business_rooms = int(new_capital.av_labor * 365 / self.LaborCost)
            else:
                private_business_rooms = int(new_capital.av_rooms)
            
            if risk_effective == True:
                revenue = self.Revenue * (1 - (1 - 2 * random.random()) * self.Risk) * private_business_rooms
            else:
                if risk_type == True:
                    revenue = self.Revenue * (1 - self.Risk) * private_business_rooms
                else:
                    revenue = self.Revenue * (1 + self.Risk) * private_business_rooms

            # Update household's capital properties
            new_capital.av_labor = self.plus(new_capital.av_labor - private_business_rooms * self.LaborCost / 365)
            
            new_capital.labor_cost += private_business_rooms * self.LaborCost / 365
            new_capital.av_rooms = self.plus(new_capital.av_rooms - private_business_rooms)
            
            new_capital.private_business_income += revenue
            new_capital.cash += revenue              
            
                
        elif self.SectorName == 'Lending':
            '''
            Formula: revenue * (1 - rnd(0, 1) * risk_factor) * lending_amount
            revenue refers to APR here
            risk_factor indicates the default rate
            '''
             
            if new_capital.cash >= self.EntryThreshold:
                lending_amount = new_capital.cash

            # Do the business             
            if risk_effective == True:
                revenue = self.Revenue * (1 - random.random() * self.Risk) * lending_amount
            else:
                if risk_type == True:
                    revenue = self.Revenue * (1 - self.Risk) * lending_amount
                else:
                    revenue = self.Revenue * lending_amount
 
            # Update household's capital properties            
            new_capital.lending_income += revenue
            new_capital.cash += revenue                
            
 
        elif self.SectorName == 'Renting':
            '''
            Formula: revenue * (1 - rnd(0, 1) * risk_factor) * rented_out_rooms
            risk_factor indicates the un-occupancy rate
            '''
            # Consider whether to build new rooms first
            floor_cost = new_capital.homestead * float(model_parameters['HomesteadAreaCost'])
            
            if new_capital.homestead > 0:
                if new_capital.buildings_area / new_capital.homestead < 6: # maximum 6 floors
                    
                    loan = 0
                    if new_capital.cash < floor_cost: # Own fund insufficient for building a new floor
                        if risk_type == False:
                            if new_capital.debt <= 0: 
                                if new_capital.cash > floor_cost * self.own_cash_percent:
                                    loan = floor_cost - new_capital.cash
                                    
                                    if risk_effective == True:
                                        new_capital.cash = 0
                                    
                                    new_capital.debt += loan
                                    new_room = new_capital.homestead
                                else:
                                    new_room = 0
                    else:
                        if risk_effective == True:
                            new_capital.cash = new_capital.cash - floor_cost
                        
                        new_room = new_capital.homestead
                
                    
                    new_capital.buildings_area += new_room
                    new_capital.building_rooms += new_room / float(model_parameters['RoomArea'])
                    new_capital.av_rooms += new_room / float(model_parameters['RoomArea'])
            
            # Do the business
            if risk_effective == True:
                revenue = self.Revenue * (1 - random.random() * self.Risk) * new_capital.av_rooms
            else:
                if risk_type == True:
                    revenue = self.Revenue * (1 - self.Risk) * new_capital.av_rooms
                else:
                    revenue = self.Revenue * new_capital.av_rooms

            # Update household's capital properties            
            new_capital.av_rooms = 0
            new_capital.renting_income += revenue
            new_capital.cash += revenue 


        return new_capital
        
        
        
        
        
        
    def plus (self, number):
        '''
        Auxiliary function.
        '''
        if number < 0:
            number = 0
        
        return number
            
        
        
        
        
        
        
        


