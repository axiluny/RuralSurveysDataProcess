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
from energy import *

class Household(object):
    '''
    This is the definition of the household class
    '''
    
    
    def __init__(self, record, VarList, current_year, db, pp_table_name, pp_table, land_dict, model_parameters):
        '''
        Construct the household class from the household table in the DB, and then add some other user-defined attributes.

        record - a record in the household table in the DB.       
        VarList - the variable (or field) list of the household table in the DB   
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
        

        
        # Initialize the household's capital properties class instance
        self.own_capital_properties = CapitalProperty(self, land_dict, model_parameters)
        
        # Define an empty list of available business sectors,
        # and another empty list of the business sectors that the household is in in the current year
        self.own_av_business_sectors = list()
        self.own_current_sectors = list()
        
        # Define an empty list of participant policy programs
        self.own_policy_programs = list()


        # Initialize the household's energy class instance
        self.energy = Energy()
        
        
        # Define a variable indicating the household's preference type
        '''
        1 - Max Labor, Min Risk;
        2 - Min Labor, Min Risk;
        3 - Max Labor, Max Risk;
        4 - Min Labor, Max Risk;
        '''
        self.hh_preference_type = int()
        
        # Also define a variable indicating the preference toward risks
        '''
        True - risk aversion; False - risk appetite;
        '''
        self.hh_risk_type = True
        
        
        # Define a variable indicating the household's business type
        '''
        0 - agriculture only
        1 - agriculture and another business sectors; or one business sector which is not agriculture
        2 - agriculture and more than one other business sectors
        '''
        self.business_type = int()
        
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
         
         

        # Annual population dynamics (personal demographic status updates)             
        temp_pp_list = list()
                             
        for PID in self.own_pp_dict:
            temp_pp_list.append(Person.personal_demographic_update(self.own_pp_dict[PID], current_year, model_parameters))
        
        # Reset own persons (members) dict (own_pp_dict)
        self.own_pp_dict = dict()
                     
        # Refresh own_pp_list                    
        for p in temp_pp_list:
            self.own_pp_dict[p.PID] = p


        # Only the existing households proceed.
        if self.is_exist == 1:                                                     
                                                                 
            # Count alive members of the household who is not moved out
            alive_members_count = 0
            for PID in self.own_pp_dict:
                if self.own_pp_dict[PID].is_alive == 1 and self.own_pp_dict[PID].moved_out == False:
                    alive_members_count += 1

            # If the updated household has no alive and not-moved-out members, mark it as non-exist.                     
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
    
    
    
    def household_economy(self, policies, business_sectors, model_parameters):
        '''
        The (annual) economic activities of the household. Including household's preference categorization, 
        policy-related decision-making,and production and consumption activities.
        '''
        
        # Determine the household's preferences
        self.housedhold_categorization()

        # Make policy decisions
        self.household_policy_decision(policies, business_sectors, model_parameters)
    
        # Do the business
        # The second parameter, risk_effective = True, indicating it is a "real world" run this time,
        # as opposed to the two "hypothetical" runs in the previous step, the policy decision step,
        # when risk_effective = False. i.e. random factors don't take effect in households' economy decision-making process.
        self.own_capital_properties = self.household_business_revenue(self.own_capital_properties, 
                                                    business_sectors, model_parameters, risk_effective=True)
        
        # Household's final accountings for the year
        self.household_final_accounting(model_parameters)        
    
    
    
    
    def housedhold_categorization(self):

        '''
        Categorize the households according to their preferences toward risk and labor/leisure trade-off
        
        For combined (risk + labor/leisure) household preference types:
            1 - Max Labor, Min Risk;
            2 - Min Labor, Min Risk;
            3 - Max Labor, Max Risk;
            4 - Min Labor, Max Risk;
                
        For risk preference types:
            True - risk aversion; False - risk appetite;
        '''        


        # Risk Preference
        # Define variables in the formula for risk preference determination
#         # is_truck
#         if self.own_capital_properties.truck > 0:
#             is_truck = 1
#         else:
#             is_truck = 0
#         
#         # is_minibus
#         if self.own_capital_properties.minibus > 0:
#             is_minibus = 1
#         else:
#             is_minibus = 0
        
        # house_size
        house_size = self.own_capital_properties.house_area
        
        high_school_kids = self.own_capital_properties.high_school_kids
        
        
        
#         p_risk = math.exp(6.702 + 0.749 * is_truck + 1.748 * is_minibus + 0.004 * house_size -
#                            1.436 * high_school_kids + 0.775 * self.NonRural - 
#                            0.005 * self.Elevation) / (1 + math.exp(6.702 + 0.749 * is_truck + 1.748 * is_minibus + 
#                                                                    0.004 * house_size - 1.436 * high_school_kids + 
#                                                                    0.775 * self.NonRural - 0.005 * self.Elevation))

        p_risk = math.exp(6.702 + 0.004 * house_size - 1.436 * high_school_kids + 0.775 * self.NonRural - 
                           0.005 * self.Elevation) / (1 + math.exp(6.702 + 0.004 * house_size - 1.436 * high_school_kids + 
                                                                   0.775 * self.NonRural - 0.005 * self.Elevation))


        # Labor Preference
#         p_labor = math.exp(0.461 * self.own_capital_properties.labor) / (1 + math.exp(0.461 * self.own_capital_properties.labor))
        labor_pref = 0
        if self.own_capital_properties.young_male_labor == 0 and self.own_capital_properties.kids == 0:
            labor_pref = 0
        else:
            labor_pref = 1
        
        
        if p_risk < 0.5:
            if labor_pref == 1:
                self.hh_preference_type = 1
                self.hh_risk_type = True
            else:
                self.hh_preference_type = 2
                self.hh_risk_type = True
        else:
            if labor_pref == 1:
                self.hh_preference_type = 3
                self.hh_risk_type = False
            else:
                self.hh_preference_type = 4
                self.hh_risk_type = False



    def household_policy_decision(self, policy_dict, business_sector_dict, model_parameters):
        
        if self.own_capital_properties.farm_to_forest != 0: # Has already joined the farm to forest program
            
            # Just apply the policies from the last year
            self.household_apply_policy(model_parameters)        
                
        elif self.own_capital_properties.farm_to_forest == 0 and self.own_capital_properties.farmland != 0:
            # Has not yet joined the farm to forest program, but has the potential to do so (household has farmland).
        
            hyp_capital_1 = copy.deepcopy(self.own_capital_properties)
            hyp_capital_2 = copy.deepcopy(self.own_capital_properties)
            
            # Reset the self.own_policy_programs list
            self.own_policy_programs = list()
            
            # First, run the business and get the hypothetical household capital properties condition when no OPTIONAL policy programs apply.
            # Note that the household's capital properties have been updated in the application process of the programs
            for PolicyType in policy_dict:
                if policy_dict[PolicyType].IsCompulsory == 1: # Only consider the compulsory programs
                    hyp_capital_1 = Policy.apply_policy_terms(policy_dict[PolicyType], hyp_capital_1, model_parameters)
                    self.own_policy_programs.append(policy_dict[PolicyType])
    
            # Get all compensational revenues
            compensation_1 = hyp_capital_1.cash - self.own_capital_properties.cash
                    
            # Do the business based on hyp_capital_1
            hyp_capital_1 = self.household_business_revenue(hyp_capital_1, business_sector_dict, model_parameters, risk_effective=False)           
            
            # Get the total household revenues in this occasion
            revenue_1 = hyp_capital_1.get_total_business_income() + compensation_1
    
            
            # Second, get the hypothetical household capital properties condition when ALL policy programs are applied
            # In this project's case, this means including an OPTIONAL program: the farmland to forest program
            for PolicyType in policy_dict:
                hyp_capital_2 = Policy.apply_policy_terms(policy_dict[PolicyType], hyp_capital_2, model_parameters)
    
            
            # Get all compensational revenues
            compensation_2 = hyp_capital_2.cash - self.own_capital_properties.cash
            
            # Do the business based on hyp_capital_2
            hyp_capital_2 = self.household_business_revenue(hyp_capital_2, business_sector_dict, model_parameters, risk_effective=False)
            
            # Get the total household revenues in this occasion        
            revenue_2 = hyp_capital_2.get_total_business_income() + compensation_2
            
            
            # Make the decision
            '''
            self.hh_preference_type:
            1 - Max Labor, Min Risk;
            2 - Min Labor, Min Risk;
            3 - Max Labor, Max Risk;
            4 - Min Labor, Max Risk;
            '''
            if self.hh_preference_type == 1 or self.hh_preference_type == 3: # Prefers Labor
                if revenue_2 > revenue_1:
                    # Then join in the programs
                    for PolicyType in policy_dict:
                        if policy_dict[PolicyType].IsCompulsory == 0: # Add the optional programs into household's own programs dictionary
                            self.own_policy_programs.append(policy_dict[PolicyType])

                            
            else: # Prefers Leisure
                if compensation_2 > self.get_min_living_cost(model_parameters):
                    # If all compensational revenues, including those from participation in the optional programs,
                    # is higher than the household's minimum living cost,
                    # Then join in the programs
                    for PolicyType in policy_dict:
                        if policy_dict[PolicyType].IsCompulsory == 0: # Add the optional programs into household's own programs dictionary
                            self.own_policy_programs.append(policy_dict[PolicyType])

            
            
            # When the decision is made, 
            # Apply the policies to get the renewed household's own capital properties condition
            # to get prepared for the "real world" run.
            self.household_apply_policy(model_parameters)
            
#             # If the household joins in the farmland to forest program this year, 
#             # remove the land parcels in their own_capital_properties.land_properties_list,
#             # and mark these farmland parcels' succession start year as this year.
#             for program in self.own_policy_programs:
#                 if program.PolicyType == 'FarmToForest_After':
#                     for farmland_parcel in self.own_capital_properties.land_properties_list:
#                         farmland_parcel.is_ftof = 1
#                         farmland_parcel.succession_start_year = self.StatDate
#                         self.own_capital_properties.land_properties_list.remove(farmland_parcel)




    def household_apply_policy(self, model_parameters):
        # Update the household's own capital properties conditions according to the policy decisions
        # and also get compensational revenues (done in the policy class)
        for program in self.own_policy_programs:
            self.own_capital_properties = Policy.apply_policy_terms(program, self.own_capital_properties, model_parameters)




    def household_business_revenue(self, hh_capital, business_sector_dict, model_parameters, risk_effective):
        '''
        The process of a household doing business.
        business_sector_dict: all business sectors. i.e. society.business_sector_dict.
        
        risk_effective - whether the random risk factor takes effect in the calculation. True - real world; False: hypothetical.
        '''
        
        self.get_available_business(hh_capital, business_sector_dict)
        
        self.get_rank_available_business(hh_capital, self.own_av_business_sectors, model_parameters)
        
        hh_capital = self.do_business(hh_capital, self.own_av_business_sectors, model_parameters, risk_effective)
        
        return hh_capital




        
    
    def get_available_business(self, hh_capital, business_sector_dict):
        '''
        Get the available (enter-able) business sectors list for the household.
        hh_capital: household's capital properties (factors of production) i.e. self.own_capital_properties;
        business_sector_dict: all business sectors. i.e. society.business_sector_dict.
        '''
        
        # Reset the own available business sectors list
        self.own_av_business_sectors = list()
        
        if self.hh_preference_type == 1 or self.hh_preference_type == 2:
            # Risk aversion. No loans. risk_type = True
            for SectorName in business_sector_dict:
                if business_sector_dict[SectorName].is_doable(hh_capital, risk_type=True) == True:
                    self.own_av_business_sectors.append(business_sector_dict[SectorName])
        
        else:
            # Risk appetite. risk_type = False
            for SectorName in business_sector_dict:
                if business_sector_dict[SectorName].is_doable(hh_capital, risk_type=False) == True:
                    self.own_av_business_sectors.append(business_sector_dict[SectorName])            
        
        
        
    
    def get_rank_available_business(self, hh_capital, business_list, model_parameters):
        '''
        Rank the business sectors in the household's available business sectors list according to the household's specific preference.
        hh_capital: household's capital properties (factors of production);
        business_list: the available business sectors list for the household.
        '''
        
        temp_sectors_list = list()
        
        if self.hh_preference_type == 1:
            '''
            Max Labor, Min Risk - risk_type = True
            '''            
            # Get the hypothetical profit of each sector if entered
            for sector in business_list:
                profit = sector.calculate_business_revenue(hh_capital, model_parameters, risk_type=True, risk_effective=False).cash - hh_capital.cash
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
            
            
        elif self.hh_preference_type == 2:
            '''
            Min Labor, Min Risk - risk_type = True
            '''
            # Get the hypothetical labor cost of each sector if entered
            for sector in business_list:
                labor_cost = sector.calculate_business_revenue(hh_capital, model_parameters, risk_type=True, risk_effective=False).labor_cost - hh_capital.labor_cost
                temp_sectors_list.append((labor_cost, sector))
                
            # Rank the sectors by labor cost ascendedly
            temp_sectors_list.sort()
            
            # Refresh the household's available business sectors list
            self.own_av_business_sectors = list()
            
            # Add sectors
            for item in temp_sectors_list:
                self.own_av_business_sectors.append(item[1])

            
        elif self.hh_preference_type == 3:
            '''
            Max Labor, Max Risk - risk_type = False
            '''
            # Get the hypothetical profit of each sector if entered
            for sector in business_list:
                profit = sector.calculate_business_revenue(hh_capital, model_parameters, risk_type=False, risk_effective=False).cash - hh_capital.cash
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
                
                
        elif self.hh_preference_type == 4:
            '''
            Min Labor, Max Risk - risk_type = False
            '''
            # Get the hypothetical labor cost of each sector if entered
            for sector in business_list:
                labor_cost = sector.calculate_business_revenue(hh_capital, model_parameters, risk_type=False, risk_effective=False).labor_cost - hh_capital.labor_cost
                temp_sectors_list.append((labor_cost, sector))
                
            # Rank the sectors by labor cost ascendedly
            temp_sectors_list.sort()
            
            # Refresh the household's available business sectors list
            self.own_av_business_sectors = list()
            
            # Add sectors
            for item in temp_sectors_list:
                self.own_av_business_sectors.append(item[1])            
        
    

    
    def do_business(self, hh_capital, business_list, model_parameters, risk_effective):
        '''
        risk_effective - whether the random risk factor takes effect in the calculation. True - real world; False: hypothetical.        
        '''
        
        # Reset the houosehold's current sector list
        self.own_current_sectors = list()
        
                
        if self.hh_preference_type == 1 or self.hh_preference_type == 3:
            '''
            1 - Max Labor, Min Risk; 3 - Max Labor, Max Risk;
            '''
            
            for sector in self.own_av_business_sectors:
                hh_capital = BusinessSector.calculate_business_revenue(sector, hh_capital, model_parameters, 
                                                                       self.hh_risk_type, risk_effective)
                self.own_current_sectors.append(sector)
                
                if hh_capital.av_labor <= 0:
                    # Exit condition: household running out of its labor resource
                    break
            
                
        elif self.hh_preference_type == 2 or self.hh_preference_type == 4:
            '''
            2 - Min Labor, Min Risk; 4 - Min Labor, Max Risk.
            '''                     
            
#             old_cash = hh_capital.cash
            
            for sector in self.own_av_business_sectors:               
                if hh_capital.get_total_business_income() + hh_capital.compensational_revenues >= self.get_min_living_cost(model_parameters):
                    # Exit condition: this year's total income >= minimal living cost
                    break 
                
                else:
                    hh_capital = BusinessSector.calculate_business_revenue(sector, hh_capital, model_parameters, 
                                                                           self.hh_risk_type, risk_effective)
                    self.own_current_sectors.append(sector)
                                                  
        return hh_capital        
        


    def household_final_accounting(self, model_parameters):
        '''
        Household's final cash capital = own_capital_properties.cash - actual_living_cost - loan_payments
        '''
        
        actual_living_cost = self.get_actual_living_cost(model_parameters)
        
        # Subtract living costs from cash reserve; if insufficient, go into debt.
        if self.own_capital_properties.cash < actual_living_cost:
            self.own_capital_properties.debt = self.own_capital_properties.debt + (actual_living_cost - self.own_capital_properties.cash)
            self.own_capital_properties.cash = 0
        else:
            self.own_capital_properties.cash = self.own_capital_properties.cash - actual_living_cost
        
        
        # Then pay the debts, if any, with up to half the household cash reserve.
        payment = self.own_capital_properties.cash / 2
        
        if self.own_capital_properties.debt > 0:
            if payment <= self.own_capital_properties.debt:
                self.own_capital_properties.cash = self.own_capital_properties.cash - payment
                self.own_capital_properties.debt = self.own_capital_properties.debt - payment
            
            else:
                self.own_capital_properties.cash = self.own_capital_properties.cash - self.own_capital_properties.debt
                self.own_capital_properties.debt = 0
                
        
        # Then calculate the household's net savings
        self.own_capital_properties.netsavings = self.own_capital_properties.cash - self.own_capital_properties.debt
        
        # Finally, update the household's capital properties from the Capital Property Class
        self.own_capital_properties.update_household_capital_properties(self)
    
    
    
    def get_min_living_cost(self, model_parameters):
        
        min_living_cost = self.own_capital_properties.preschool_kids * float(model_parameters['PreSchooleCostPerKidI'])\
                        + self.own_capital_properties.primary_school_kids * float(model_parameters['PrimarySchoolCostPerKidI'])\
                        + self.own_capital_properties.secondary_school_kids * float(model_parameters['SecondarySchoolCostPerKidI'])\
                        + self.own_capital_properties.high_school_kids * float(model_parameters['HighSchoolCostPerKidI'])\
                        + self.own_capital_properties.college_kids * float(model_parameters['CollegeCostPerKidI'])\
                        + ( len(self.own_pp_dict) - self.own_capital_properties.preschool_kids - self.own_capital_properties.primary_school_kids
                             - self.own_capital_properties.secondary_school_kids - self.own_capital_properties.high_school_kids
                              - self.own_capital_properties.college_kids) * float(model_parameters['EverydayCostPerCapitaI'])
        
        return min_living_cost
    
    
    
    
    def get_actual_living_cost(self, model_parameters):
        
        self.get_household_business_type()
        
        if self.business_type == 0:
            living_cost = self.own_capital_properties.preschool_kids * float(model_parameters['PreSchooleCostPerKidI'])\
                            + self.own_capital_properties.primary_school_kids * float(model_parameters['PrimarySchoolCostPerKidI'])\
                            + self.own_capital_properties.secondary_school_kids * float(model_parameters['SecondarySchoolCostPerKidI'])\
                            + self.own_capital_properties.high_school_kids * float(model_parameters['HighSchoolCostPerKidI'])\
                            + self.own_capital_properties.college_kids * float(model_parameters['CollegeCostPerKidI'])\
                            + ( len(self.own_pp_dict) - self.own_capital_properties.preschool_kids - self.own_capital_properties.primary_school_kids
                                 - self.own_capital_properties.secondary_school_kids - self.own_capital_properties.high_school_kids
                                  - self.own_capital_properties.college_kids) * float(model_parameters['EverydayCostPerCapitaI'])
            
        
        elif self.business_type == 1:
            living_cost = self.own_capital_properties.preschool_kids * float(model_parameters['PreSchooleCostPerKidII'])\
                            + self.own_capital_properties.primary_school_kids * float(model_parameters['PrimarySchoolCostPerKidII'])\
                            + self.own_capital_properties.secondary_school_kids * float(model_parameters['SecondarySchoolCostPerKidII'])\
                            + self.own_capital_properties.high_school_kids * float(model_parameters['HighSchoolCostPerKidII'])\
                            + self.own_capital_properties.college_kids * float(model_parameters['CollegeCostPerKidII'])\
                            + ( len(self.own_pp_dict) - self.own_capital_properties.preschool_kids - self.own_capital_properties.primary_school_kids
                                 - self.own_capital_properties.secondary_school_kids - self.own_capital_properties.high_school_kids
                                  - self.own_capital_properties.college_kids) * float(model_parameters['EverydayCostPerCapitaII'])
        
        else:
            living_cost = self.own_capital_properties.preschool_kids * float(model_parameters['PreSchooleCostPerKidIII'])\
                            + self.own_capital_properties.primary_school_kids * float(model_parameters['PrimarySchoolCostPerKidIII'])\
                            + self.own_capital_properties.secondary_school_kids * float(model_parameters['SecondarySchoolCostPerKidIII'])\
                            + self.own_capital_properties.high_school_kids * float(model_parameters['HighSchoolCostPerKidIII'])\
                            + self.own_capital_properties.college_kids * float(model_parameters['CollegeCostPerKidIII'])\
                            + ( len(self.own_pp_dict) - self.own_capital_properties.preschool_kids - self.own_capital_properties.primary_school_kids
                                 - self.own_capital_properties.secondary_school_kids - self.own_capital_properties.high_school_kids
                                  - self.own_capital_properties.college_kids) * float(model_parameters['EverydayCostPerCapitaIII'])

        
        
        self.AnnualTotalExpense = living_cost
        
        return living_cost    
    
    
    
    
    
    def get_household_business_type(self):
        
        if len(self.own_current_sectors) == 1 and self.own_current_sectors[0].SectorName == 'Agriculture':
            self.business_type = 0
        elif  len(self.own_current_sectors) == 2:
            if self.own_current_sectors[0].SectorName == 'Agriculture' or self.own_current_sectors[1].SectorName == 'Agriculture':
                self.business_type = 1
        else:
            self.business_type = 2
        
        self.HouseholdBusinessType = self.business_type
    




    