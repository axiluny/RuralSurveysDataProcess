'''
Created on Mar 25, 2015

@author: Liyan Xu; Hongmou Zhang
'''
# import copy
import random
import math

from person import Person
from data_access import DataAccess
from capital_property import CapitalProperty
from business_sector import *
from policy import *

class Household(object):
    '''
    This is the definition of the household class
    '''
    
    
    def __init__(self, record, VarList, current_year, db, pp_table_name, pp_table, model_parameters):
        '''
        Construct the household class from the household table in the DB, and then add some other user-defined attributes.

        record indicates a record in the household table in the DB.
        
        VarList is the variable (or field) list of the household table in the DB   
        VarList = {paramName1: paramOrder1, paramName2: paramOrder2, ...}
        
        Also initialize the household's own person instances here from the person table in the DB.
        Also initialize the household's capital properties instance here.     
        '''       
        
        # Set the attributes (var) and their values (record) from the household table in the DB.
        for var in VarList:
            setattr(self, var[0], record[var[1]])

        # Set the household and person variables (attributes) lists
        self.hh_var_list = VarList
        self.pp_var_list = DataAccess.get_var_list(db, pp_table_name)


        # Set the current time stamp
        self.StatDate = current_year
        
        
        # Define own persons (members) dict of the household, indexed by PID
        self.own_pp_dict = dict()

        
        # Add respective persons into the persons dict of the household
        for pp in pp_table:
            if pp.HID == self.HID:
                pp_temp = Person(pp, self.pp_var_list, current_year)
                self.own_pp_dict[pp_temp.PID] = pp_temp # Indexed by PID
        

        
        # Initialize the household's capital properties instance
        self.own_capital_properties = CapitalProperty(self, model_parameters)
        
        # Define an empty list of available business sectors
        self.own_av_business_sectors = list()
        
        # Define an empty list of participant policy programs
        self.own_policy_programs = list()
        
        
        # Define a variable indicating household type
        '''
        1 - Max Labor, Min Risk;
        2 - Min Labor, Min Risk;
        3 - Max Labor, Max Risk;
        4 - Min Labor, Max Risk;
        '''
        self.hh_type = int()
        
        # Define a switch variable indicating whether the household is dissolved in the current year
        self.is_dissolved_this_year = False
  


    
    def household_demographic_update(self, current_year, model_parameters):
        '''
        Annual demographic updates of the household.
        '''
        
        # Update the current time stamp
        self.StatDate = current_year
        
        # Reset the "dissolved this year" switch
        # Note this is before the household existence bifurcation. 
        # So all households in society.hh_dict get this switch reset (every year).
        self.is_dissolved_this_year = False
        
        
        # Only the existing households proceed.
        if self.is_exist == 1:
            
            temp_pp_list = list()
                                
            # Annual population dynamics (personal demographic status updates)
            for PID in self.own_pp_dict:
                temp_pp_list.append(Person.personal_demographic_update(self.own_pp_dict[PID], current_year, model_parameters))

            # Reset own persons (members) dict (own_pp_dict)
            self.own_pp_dict = dict()
                        
            # Refresh own_pp_list                    
            for p in temp_pp_list:
                self.own_pp_dict[p.PID] = p
                                                    
                                                                
            # If the updated household has no members, mark it as non-exist.
            alive_members_count = 0
            for PID in self.own_pp_dict:
                if self.own_pp_dict[PID].is_alive == 1:
                    alive_members_count += 1
                    
            if alive_members_count == 0:        
                self.is_exist = 0
                self.is_dissolved_this_year = True # Turn on this switch so that the household could be dissolved later in the society class
            

            # Then deal with the deceased persons
            for p in temp_pp_list:         
                # If p dies this year and p's spouse lives
                if p.is_died_this_year == True and p.SpouseID != '0' and self.own_pp_dict[p.SpouseID].is_alive == 1:
                                       
                    # Then p's spouse's marital status changes
                    self.own_pp_dict[p.SpouseID].IsMarry = 0
                    self.own_pp_dict[p.SpouseID].SpouseID = '0'
   
                    # And p's own marital status is also marked changed
                    self.own_pp_dict[p.PID].IsMarry = 0
                    self.own_pp_dict[p.PID].SpouseID = '0'     
        
        return self



    
    def household_capital_properties_update(self):
        self.own_capital_properties.refresh(self)
    
    
    
    
    def housedhold_categorization(self):
        
#         # Define the two dimensional variables
#         p_risk = float()
#         p_labor = float()
        
        # Define other variables in the formula
        # is_truck
        if self.own_capital_properties.truck > 0:
            is_truck = 1
        else:
            is_truck = 0
        
        # is_minibus
        if self.own_capital_properties.minibus > 0:
            is_minibus = 1
        else:
            is_minibus = 0
        
        # house_size
        house_size = self.own_capital_properties.buildings_area
        if house_size == None:
            house_size = 0
        
        high_school_kids = self.own_capital_properties.high_school_kids
        
        
        
#         p_risk = math.exp(6.702 + 0.749 * is_truck + 1.748 * is_minibus + 0.004 * house_size - 1.436 * high_school_kids + 0.775 * self.NonRural - 0.005 * self.Elevation) / (1 + math.exp(6.702 + 0.749 * is_truck + 1.748 * is_minibus + 0.004 * house_size - 1.436 * high_school_kids + 0.775 * self.NonRural - 0.005 * self.Elevation))
        p_risk = random.random()
        
        p_labor = math.exp(0.461 * self.own_capital_properties.labor) / (1 + math.exp(0.461 * self.own_capital_properties.labor))

        
        if p_risk < 0.5:
            if p_labor > 0.5:
                self.hh_type = 1
            else:
                self.hh_type = 2
        else:
            if p_labor > 0.5:
                self.hh_type = 3
            else:
                self.hh_type = 4




    def household_business_revenue(self, business_sector_dict, model_parameters):
        '''
        The process of a household doing business.
        business_sector_dict: all business sectors. i.e. society.business_sector_dict.
        '''
        
        self.get_available_business(self.own_capital_properties, business_sector_dict)
        
        self.get_rank_available_business(self.own_capital_properties, self.own_av_business_sectors, model_parameters)
        
        self.do_business(self.own_capital_properties, self.own_av_business_sectors)



        
    
    def get_available_business(self, hh_capital, business_sector_dict):
        '''
        Get the available (enter-able) business sectors list for the household.
        hh_capital: household's capital properties (factors of production) i.e. self.own_capital_properties;
        business_sector_dict: all business sectors. i.e. society.business_sector_dict.
        '''
        
        # Reset the own available business sectors list
        self.own_av_business_sectors = list()
        
        if self.hh_type == 1 or self.hh_type == 2:
            # Risk aversion. No loans. risk_type = True
            for SectorName in business_sector_dict:
                if business_sector_dict[SectorName].is_available(hh_capital, True) == True:
                    self.own_av_business_sectors.append(business_sector_dict[SectorName])
        
        else:
            # Risk appetite. risk_type = False
            for SectorName in business_sector_dict:
                if business_sector_dict[SectorName].is_available(hh_capital, False) == True:
                    self.own_av_business_sectors.append(business_sector_dict[SectorName])            
        
        
        
    
    def get_rank_available_business(self, hh_capital, business_list, model_parameters):
        '''
        Rank the business sectors in the household's available business sectors list according to the household's specific preference.
        hh_capital: household's capital properties (factors of production);
        business_list: the available business sectors list for the household.
        '''
        
        temp_sectors_list = list()
        
        if self.hh_type == 1:
            '''
            Max Labor, Min Risk - risk_type = True
            '''
            
            # Get the hypothetical profit of each sector if entered
            for sector in business_list:
                profit = sector.calculate_business_revenue(hh_capital, True, False, model_parameters).cash - hh_capital.cash
                temp_sectors_list.append((profit, sector))
                
            # Rank the sectors by profit descendedly
            temp_sectors_list.sort(reverse = True)
            
            # Refresh the household's available business sectors list
            self.own_av_business_sectors = list()
            
            # Always place agriculture (if enter-able) in the first place
            for item in temp_sectors_list:
                if item[1].SectorName == 'Agriculture':
                    self.own_av_business_sectors.append(item[1])
                    temp_sectors_list.remove(item)
            
            # Then add other sectors
            for item in temp_sectors_list:
                self.own_av_business_sectors.append(item[1])
            
            
        elif self.hh_type == 2:
            '''
            Min Labor, Min Risk
            '''
            
            pass
        elif self.hh_type == 3:
            '''
            Max Labor, Max Risk
            '''
            pass
        elif self.hh_type == 4:
            '''
            Min Labor, Max Risk;
            '''
            pass
        
    




    
    def do_business(self, hh_capital, business_list):
        pass
    
    
    
    