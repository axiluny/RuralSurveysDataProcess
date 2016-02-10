'''
Created on May 30, 2015

@author: Liyan Xu
'''

import copy
import random


class BusinessSector(object):
    '''
    This is the business sectors class.
    It deals with the basic properties of business sectors in which the households engage,
    and determine whether a household can enter a sector, and calculate the revenues and costs in doing so.
    '''


    def __init__(self, record, VarList):
        '''
        Construct the business sectors class from the business sector table in the DB, and then add some other user-defined attributes.

        record - a record in the business sector table in the DB.       
        VarList - the variable (or field) list of the business sector table in the DB   
        VarList = {paramName1: paramOrder1, paramName2: paramOrder2, ...}  
        '''
        
        # Set the attributes (var) and their values (record) from the business sector table in the DB.                
        for var in VarList:
            setattr(self, var[0], record[var[1]])
            
        # A temporary variable, indicating the minimal own capital ratio (or a "down payment") required to raise a loan.
        self.own_cash_percent = 0.8




    def is_doable(self, capital, risk_type):
        '''
        Determine whether a household with a certain capital properties (capital) and risk preference can engage in a business.
        capital - household's own capital properties (factors of production) i.e. household_class.own_capital_properties
        risk_type - household's preference toward risks. True - risk aversion; False - risk appetite;
        '''
        
        if self.SectorName == 'Agriculture':
#             if (365* capital.labor - self.LaborCost * capital.av_farmland) > 0 and capital.av_farmland > 0: # Can't understand first condition... 20160117
            if capital.labor > 0 and capital.av_farmland > 0:
                return True
            
        elif self.SectorName == 'TempJob':
            if (365* capital.male_labor - self.LaborCost) > 0:
                return True

#         elif self.SectorName == 'FreightTrans':
#             if capital.av_male_labor > 0:
#                 if capital.av_truck > 0:
#                     return True
#                 elif capital.cash > self.EntryThreshold:
#                     return True
#                 elif capital.cash > self.EntryThreshold * self.own_cash_percent and capital.debt <= 0 and risk_type == False:
#                     return True
# 
#         elif self.SectorName == 'PassengerTrans':
#             if capital.av_male_labor > 0:
#                 if capital.av_minibus > 0:
#                     return True
#                 elif capital.cash > self.EntryThreshold:
#                     return True
#                 elif capital.cash > self.EntryThreshold * self.own_cash_percent and capital.debt <= 0 and risk_type == False:
#                     return True
#   
        elif self.SectorName == 'Lodging':
            if capital.av_male_labor > 0:
                if capital.cash > self.EntryThreshold:
                    return True
                elif capital.cash > self.EntryThreshold * self.own_cash_percent and capital.debt <= 0 and risk_type == False:
                    return True
      
        elif self.SectorName == 'Renting':
            if capital.av_house_rooms > 0:
                return True          





    def calculate_business_revenue(self, capital, model_parameters, risk_type, risk_effective):
        '''
        capital - household's own capital properties (factors of production) i.e. household_class.own_capital_properties
        risk_type - household's preference toward risks. True - risk aversion; False - risk appetite;
        risk_effective - whether the random risk factor takes effect in the calculation. True - real world; False: hypothetical.
        '''
        
        # Make a new capital instance as a temporary variable
        new_capital = copy.deepcopy(capital)
        
        # Define other temporary variables
        revenue = float()
        max_farm = float()
        max_labor = float()
        max_vehicle = float()
        loan = float()
        floor_cost = float()
        new_room_area = float()
        lodging_rooms = int()

        
        
        if self.SectorName == 'Agriculture':
            '''
            Formula: revenue * [1 - risk_factor * rnd(-1, 1)] * farmland_area * location_factor * neighborhood_factor
            # Temporarily not including the neighborhood factor
            '''
            
            # Find the specific labor cost as determined by the household's terrain type.
            if capital.location_type == 1: # hilly
                spec_labor_cost = self.LaborCost * 1.2
            else: # plain
                spec_labor_cost = self.LaborCost
            
            # Find the theoretical maximum farm land area cultivatable as permitted by the household's available labor.
            theoretical_max_farm = (new_capital.av_labor * 365) / spec_labor_cost
            
            # Then determine the actual maximum farm-able land area (smallest land area unit is the land parcel)
            max_farm = 0
                       
            if theoretical_max_farm > new_capital.av_farmland:
                max_farm = new_capital.av_farmland
                for land_parcel in new_capital.land_properties_list:
                    land_parcel.actual_farming = True
            else:
                for land_parcel in new_capital.land_properties_list:
                    max_farm += land_parcel.Shape_Area / 666.7
                    land_parcel.actual_farming = True
                    
                    if max_farm > theoretical_max_farm:
                        max_farm = max_farm - land_parcel.Shape_Area / 666.7
                        land_parcel.actual_farming = False
            
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
#             new_capital.total_business_income += revenue
            new_capital.cash += revenue
            
            
            
        elif self.SectorName == 'TempJob':
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
#             new_capital.total_business_income += revenue
            new_capital.cash += revenue



#         elif self.SectorName == 'FreightTrans':
#             '''
#             Formula: revenue * [1 - risk_factor * rnd(-1, 1)] * truck_num
#             '''
#             
#             # Consider whether to purchase a truck first
#             if new_capital.av_male_labor > new_capital.av_truck:
#                 # If the household has spare male labor
#                 loan = 0
#                 
#                 if new_capital.cash < self.EntryThreshold:
#                     # household's own cash capital is insufficient for buying a truck
#                     if risk_type == False:
#                         # only the risk appetite household would raise loans
#                         if new_capital.debt <= 0:
#                             if new_capital.cash >= self.EntryThreshold * self.own_cash_percent:
#                                 loan = self.EntryThreshold - new_capital.cash
#                                 
#                                 if risk_effective == True:
#                                     # refresh household's capital properties only in the real world case;
#                                     new_capital.cash = 0
#                                 
#                                 new_capital.debt += loan
#                                 new_capital.truck += 1
#                                 new_capital.av_truck += 1
#                 
#                 else:
#                     # household can afford a new truck without raising loans
#                     if risk_effective == True:
#                         new_capital.cash = new_capital.cash - self.EntryThreshold
#         
#                     new_capital.truck += 1
#                     new_capital.av_truck += 1
#             
#             # one male labor matches one truck
#             if new_capital.av_male_labor < new_capital.av_truck:
#                 max_vehicle = new_capital.av_male_labor
#             else:
#                 max_vehicle = new_capital.av_truck
#             
#             # Do the business
#             if risk_effective == True:
#                 revenue = self.Revenue * (1 + (1 - 2 * random.random()) * self.Risk) * max_vehicle
#             else:
#                 if risk_type == True:
#                     revenue = self.Revenue * (1 - self.Risk) * max_vehicle
#                 else:
#                     revenue = self.Revenue * (1 + self.Risk) * max_vehicle
#             
#             # Update household's capital properties
#             new_capital.av_labor = self.plus(new_capital.av_labor - max_vehicle * self.LaborCost / 365)
#             new_capital.av_male_labor = self.plus(new_capital.av_male_labor - max_vehicle * self.LaborCost / 365)
#             
#             new_capital.labor_cost += max_vehicle * self.LaborCost / 365
#             new_capital.av_truck = self.plus(new_capital.truck - max_vehicle)
#             
#             new_capital.freight_trans_income += revenue
# #             new_capital.total_business_income += revenue
#             new_capital.cash += revenue
#                     
# 
# 
#         elif self.SectorName == 'PassengerTrans':
#             '''
#             Formula: revenue * [1 - risk_factor * rnd(-1, 1)] * passenger_car_num
#             '''
#             
#             # Consider whether to purchase a minibus first
#             if new_capital.av_male_labor > new_capital.av_minibus:
#                 # If the household has spare male labor
#                 loan = 0
#                 
#                 if new_capital.cash < self.EntryThreshold:
#                     # household's own cash capital is insufficient for buying a minibus
#                     if risk_type == False:
#                         # only the risk appetite household would raise loans
#                         if new_capital.debt <= 0:
#                             if new_capital.cash >= self.EntryThreshold * self.own_cash_percent:
#                                 loan = self.EntryThreshold - new_capital.cash
#                                 
#                                 if risk_effective == True:
#                                     # refresh household's capital properties only in the real world case;
#                                     new_capital.cash = 0
#                                 
#                                 new_capital.debt += loan
#                                 new_capital.minibus += 1
#                                 new_capital.av_minibus += 1
#                 
#                 else:
#                     # household can afford a new minibus without raising loans
#                     if risk_effective == True:
#                         new_capital.cash = new_capital.cash - self.EntryThreshold
#         
#                     new_capital.minibus += 1
#                     new_capital.av_minibus += 1
#             
#             # one male labor matches one minibus
#             if new_capital.av_male_labor < new_capital.av_minibus:
#                 max_vehicle = new_capital.av_male_labor
#             else:
#                 max_vehicle = new_capital.av_minibus
#             
#             # Do the business
#             if risk_effective == True:
#                 revenue = self.Revenue * (1 + (1 - 2 * random.random()) * self.Risk) * max_vehicle
#             else:
#                 if risk_type == True:
#                     revenue = self.Revenue * (1 - self.Risk) * max_vehicle
#                 else:
#                     revenue = self.Revenue * (1 + self.Risk) * max_vehicle
#             
#             # Update household's capital properties
#             new_capital.av_labor = self.plus(new_capital.av_labor - max_vehicle * self.LaborCost / 365)
#             new_capital.av_male_labor = self.plus(new_capital.av_male_labor - max_vehicle * self.LaborCost / 365)
#             
#             new_capital.labor_cost += max_vehicle * self.LaborCost / 365
#             new_capital.av_minibus = self.plus(new_capital.minibus - max_vehicle)
#             
#             new_capital.passenger_trans_income += revenue
# #             new_capital.total_business_income += revenue
#             new_capital.cash += revenue

  
  
        elif self.SectorName == 'Lodging':
            '''
            Formula: revenue * (1 - rnd(0, 1) * risk_factor) * lodging_rooms
            risk_factor indicates un-occupancy rate. risk_factor = 0 indicate full occupancy.
            '''
            
            # Consider whether to build new rooms first
            floor_cost = new_capital.homestead * float(model_parameters['HomesteadAreaCost'])
            
            if new_capital.homestead > 0:
                if new_capital.house_area / new_capital.homestead < 6: # maximum 6 floors
                    
                    loan = 0
                    if new_capital.cash < floor_cost: # Own fund insufficient for building a new floor
                        if risk_type == False:
                            if new_capital.debt <= 0: 
                                if new_capital.cash > floor_cost * self.own_cash_percent:
                                    loan = floor_cost - new_capital.cash
                                    
                                    if risk_effective == True:
                                        new_capital.cash = 0
                                    
                                    new_capital.debt += loan
                                    new_room_area = new_capital.homestead
                                else:
                                    new_room_area = 0
                    else:
                        if risk_effective == True:
                            new_capital.cash = new_capital.cash - floor_cost
                        
                        new_room_area = new_capital.homestead
                
                    
                    new_capital.house_area += new_room_area
                    new_capital.house_rooms += int (new_room_area / float(model_parameters['RoomArea']))
                    new_capital.av_house_rooms += new_room_area / float(model_parameters['RoomArea'])
            
            
            # Determine maximum scale of business
            if new_capital.av_house_rooms > new_capital.av_labor * 365 / self.LaborCost:
                lodging_rooms = int(new_capital.av_labor * 365 / self.LaborCost)
            else:
                lodging_rooms = int(new_capital.av_house_rooms)
                            
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
            new_capital.av_house_rooms = self.plus(new_capital.av_house_rooms - lodging_rooms)
            
            new_capital.lodging_income += revenue
#             new_capital.total_business_income += revenue
            new_capital.cash += revenue            
                        
                        
 
        elif self.SectorName == 'Renting':
            '''
            Formula: revenue * (1 - rnd(0, 1) * risk_factor) * rented_out_rooms
            risk_factor indicates the un-occupancy rate
            '''
            # Consider whether to build new rooms first
            floor_cost = new_capital.homestead * float(model_parameters['HomesteadAreaCost'])
            
            if new_capital.homestead > 0:
                if new_capital.house_area / new_capital.homestead < 6: # maximum 6 floors
                    
                    loan = 0
                    if new_capital.cash < floor_cost: # Own fund insufficient for building a new floor
                        if risk_type == False:
                            if new_capital.debt <= 0: 
                                if new_capital.cash > floor_cost * self.own_cash_percent:
                                    loan = floor_cost - new_capital.cash
                                    
                                    if risk_effective == True:
                                        new_capital.cash = 0
                                    
                                    new_capital.debt += loan
                                    new_room_area = new_capital.homestead
                                else:
                                    new_room_area = 0
                    else:
                        if risk_effective == True:
                            new_capital.cash = new_capital.cash - floor_cost
                        
                        new_room_area = new_capital.homestead
                
                    
                    new_capital.house_area += new_room_area
                    new_capital.house_rooms += int (new_room_area / float(model_parameters['RoomArea']))
                    new_capital.av_house_rooms += new_room_area / float(model_parameters['RoomArea'])
            
            # Do the business
            if risk_effective == True:
                revenue = self.Revenue * (1 - random.random() * self.Risk) * new_capital.av_house_rooms
            else:
                if risk_type == True:
                    revenue = self.Revenue * (1 - self.Risk) * new_capital.av_house_rooms
                else:
                    revenue = self.Revenue * new_capital.av_house_rooms

            # Update household's capital properties            
            new_capital.av_house_rooms = 0
            new_capital.renting_income += revenue
#             new_capital.total_business_income += revenue
            new_capital.cash += revenue 


        return new_capital
        
        
        
        
        
        
    def plus (self, number):
        '''
        Auxiliary function.
        '''
        if number < 0:
            number = 0
        
        return number
            
        
        
        
        
        
        
        


