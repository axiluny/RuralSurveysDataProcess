'''
Created on May 26, 2015

@author: Liyan Xu
'''

from land import *



class CapitalProperty(object):
    '''
    Households' factors of production: properties and related behaviors
    '''


    def __init__(self, hh, land_dict, model_parameters):
        '''
        Construct the capital property class from attributes of a household instance hh.
        hh - an instance of the household class.
        '''
        
        # Monetary assets and liabilities
        self.netsavings = hh.NetSavings # Net savings of the household; netsavings = cash - debt 
        self.cash = hh.Cash # Positive values only
        self.debt  = hh.Debt # Positive values only; Positive values indicate household in debt
        
        
        # Land properties
        # Define the list of land parcels (instances of the land class) of the household
        self.land_properties_list = list()

        # And then fill it with records in the land_dict (society_instance.land_dict)
        for ParcelID in land_dict:              
            if land_dict[ParcelID].HID == hh.HID:
                self.land_properties_list.append(land_dict[ParcelID])
                    
        # Get the household's numerical land properties from the list
        self.farmland = 0
        self.homestead = 0
        
        for land_parcel in self.land_properties_list:
            if land_parcel.LandCover == 'Cultivate':
                self.farmland += (float(land_parcel.Shape_Area) / float(666.7))
#             elif land_parcel.LandCover== 'Construction':
#                 self.homestead += land_parcel.Shape_Area / 666.7
                '''
                Before the homestead shape problems in the database is solved,
                just use hh.Homestead as source of household homestead data,
                rather than getting it from the land properties list
                '''       
        # Other land properties of the household, mainly real-estate properties
        self.homestead = hh.Homestead
        self.house_area = hh.HouseArea
        self.house_rooms = int(self.house_area / float(model_parameters['RoomArea'])) # buildings in numbers of rooms; 30 m^2 per room
                
        self.location_type = hh.LocType # Location terrain types: 1 - hilly; 0 - plain.
                   
        
        # Labor (Human capitals)
        self.hh_size = int()
        self.labor = int()
        self.male_labor = int()
        self.female_labor = int()
        self.young_male_labor = int()
        
        self.kids = int()
        self.preschool_kids = int()
        self.primary_school_kids = int()
        self.secondary_school_kids = int()
        self.high_school_kids = int()
        self.college_kids = int()
        
        self.update_labors(hh)

                
                
        # Other specific factors of production
#         self.minibus = hh.Minibus
#         self.truck = hh.Truck
        
        
        # Policy-related factors
        self.pre_ftof = hh.PreFToF
        self.pre_ftob = hh.PreFToB
        self.is_tianbao = hh.IsTianbao
        
        self.farm_to_forest = float(0) # A "container" to store the FToF area incurred during simulation
        
        
        # Available factors; temporary "containers" during simulation
        self.av_farmland = float()
        self.av_homestead = float()
        self.av_house_area = float()        
        self.av_house_rooms = int()
#         self.av_minibus = int()
#         self.av_truck = int()
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
        self.lodging_income = float()
        self.private_business_income = float()
        self.lending_income = float()
        self.renting_income = float()
        
#         self.total_business_income = float()
        self.compensational_revenues = float()
        
    
    
    
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
        for land_parcel in self.land_properties_list:
            land_parcel.actual_farming = False

        # Farmland
        self.farmland = 0
        for land_parcel in self.land_properties_list:
            if land_parcel.LandCover == 'Cultivate':
                self.farmland += (float(land_parcel.Shape_Area) / float(666.7))        
        
        self.av_farmland = self.farmland
        self.av_homestead = self.homestead
        self.av_house_rooms = (self.house_area - self.homestead) / 30
#         self.av_minibus = self.minibus
#         self.av_truck = self.truck
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
        self.lodging_income = 0
        self.private_business_income = 0
        self.lending_income = 0
        self.renting_income = 0        
        
#         self.total_business_income = 0
        self.compensational_revenues = 0
        
    
    def update_labors(self, hh):
        '''
        Update the household's human resource conditions according to its latest demographic status
        '''
        
        self.hh_size = 0
        self.labor = 0
        self.male_labor = 0
        self.female_labor = 0
        self.young_male_labor = 0

        self.kids = 0
        self.preschool_kids = 0
        self.primary_school_kids = 0
        self.secondary_school_kids = 0
        self.high_school_kids = 0
        self.college_kids = 0

        
        
        for PID in hh.own_pp_dict:
            if hh.own_pp_dict[PID].is_alive == 1:
                
                self.hh_size += 1
                
                if hh.own_pp_dict[PID].is_student == True:
                    if hh.own_pp_dict[PID].Education == 'uneducated' and hh.own_pp_dict[PID].Age >= 4:
                        self.preschool_kids += 1
                    elif hh.own_pp_dict[PID].Education == 'primary':
                        self.primary_school_kids += 1
                    elif hh.own_pp_dict[PID].Education == 'secondary':
                        self.secondary_school_kids += 1
                    elif hh.own_pp_dict[PID].Education == 'high_school':
                        self.high_school_kids += 1
                    elif hh.own_pp_dict[PID].Education == 'college':
                        self.college_kids += 1
                    
                
                if hh.own_pp_dict[PID].Age >= 18 and hh.own_pp_dict[PID].moved_out == False:
                    # For now, no upper age limit for being a labor
                    # Those who go to college do not count as household labors
                    
                    self.labor += 1
                    
                    if hh.own_pp_dict[PID].Gender == 1:
                        self.male_labor += 1
                        if hh.own_pp_dict[PID].Age <= 45:
                            self.young_male_labor += 1
                    else:
                        self.female_labor += 1
                
                else:
                    self.kids += 1
    
    
    def get_monetary_value(self):
        
        value = self.cash # Need to elaborate
        
        return value
    
    
    def get_total_business_income(self):
        
        total_business_income = self.agriculture_income + self.temp_job_income + self.freight_trans_income \
                     + self.passenger_trans_income + self.lodging_income + self.private_business_income \
                     + self.lending_income + self.renting_income
        
        return total_business_income
    
    
    def merge_capital_properties(self, soc, out_HID, in_HID):
        '''
        Merge one household's (out_HID) all capital properties (self) into another's (in_HID)
        self is the household with HID "out_HID"
        '''
        
        for item in self.__dict__:
            if item != 'land_properties_list':
            # land_properties is a LandClass object and cannot be simply added to each other; Deal with them later
                          
#                 if soc.hh_dict[in_HID] is not None:
                soc.hh_dict[in_HID].own_capital_properties.__dict__[item] = soc.hh_dict[in_HID].own_capital_properties.__dict__[item] + self.__dict__[item]
                
                # Then reset the original household's capital properties in hh_dict
                self.__dict__[item] = 0
            
            else:
                # Deal with the land properties
                for land_parcel in soc.hh_dict[out_HID].own_capital_properties.land_properties_list:
                    soc.hh_dict[in_HID].own_capital_properties.land_properties_list.append(land_parcel)
                    soc.hh_dict[out_HID].own_capital_properties.land_properties_list.remove(land_parcel)
        
        

    def update_household_capital_properties(self, hh):
        '''
        Write the household's capital properties conditions back to the respective variables of the household class instance
        '''

        # Monetary assets and liabilities        
        hh.NetSavings = self.netsavings
        hh.Cash = self.cash
        hh.Debt = self.debt
        
        
        # Land properties        
        hh.FarmlandArea = self.farmland
        hh.HouseArea = self.house_area
        hh.Homestead = self.homestead
         
        hh.LocType = self.location_type
        
                                
        # Other specific factors of production
#         hh.Minibus = self.minibus 
#         hh.Truck = self.truck
        
        # Incomes
        hh.AgricultureIncome = self.agriculture_income
        hh.TempJobIncome = self.temp_job_income
        hh.TruckIncome = self.freight_trans_income
        hh.PassengerIncome = self.passenger_trans_income
        hh.LodgingIncome = self.lodging_income
        hh.PrivateBusinessIncome = self.private_business_income
        hh.LendingIncome = self.lending_income
        hh.RentingIncome = self.renting_income
        
        hh.AnnualCompensation = self.compensational_revenues        
        hh.AnnualTotalIncome = self.get_total_business_income() + self.compensational_revenues
        
        # hh.AnnualCompensation is assigned in the policy class        
        
        # Land
        hh.FToFArea = self.farm_to_forest
        hh.AbandonedFarmlandArea = self.av_farmland # available farmland at the end of each simulation circle is considered "abandoned"
        
        # Policy-related land changes
        
        