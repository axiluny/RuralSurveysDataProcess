'''
Created on May 30, 2015

@author: Liyan Xu
'''

import copy

class Policy(object):
    '''
    The Policy Class deals with the policy programs and their behaviors (mainly referring to modifying households'
    capital property conditions.
    '''


    def __init__(self, record, VarList):
        '''
        Construct the person policy from the policy table in the DB.

        record - a record in the policy table in the DB.
        VarList - the variable (or field) list of the policy table in the DB.
        VarList = {paramName1: paramOrder1, paramName2: paramOrder2, ...}   
        '''        
        # Set the attributes (var) and their values (record) from the policy programs table in the DB.                
        for var in VarList:
            setattr(self, var[0], record[var[1]])
    
    
    
    def apply_policy_terms(self, hh_capital, model_parameters):
        '''
        Apply the policy terms and thereby modify the household's capital property conditions accordingly.
        hh_capital - the household's capital properties (a capital_property class instance).
        model_parameters: global model parameters dictionary.
        '''

        # Make a copy of the hh_capital parameter        
        new_hh_capital = copy.deepcopy(hh_capital)
        
        revenue = float()
        
        
        if self.PolicyType == 'FarmToForest_After':
            if new_hh_capital.farm_to_forest == 0: # Never joined in the program
                new_hh_capital.farm_to_forest = hh_capital.farmland
                new_hh_capital.farmland = 0
                new_hh_capital.av_farmland = 0
                
                for land_parcel in new_hh_capital.land_properties_list:
                    if land_parcel.LandCover == 'Cultivate':
                        # Mark it as a reverted parcel this year
                        land_parcel.IsG2G_this_year = True

            
            revenue = new_hh_capital.farm_to_forest * self.CompensateStandard
            new_hh_capital.cash += revenue
            new_hh_capital.compensational_revenues += revenue
            
            
            
#         elif self.PolicyType == 'FarmToForest_Before':
#             revenue = new_hh_capital.pre_ftof * self.CompensateStandard
#             new_hh_capital.cash += revenue
#             new_hh_capital.compensational_revenues += revenue            
#  
#  
#         elif self.PolicyType == 'FarmToBamboo_Before':
#             revenue = new_hh_capital.pre_ftob * self.CompensateStandard
#             new_hh_capital.cash += revenue
#             new_hh_capital.compensational_revenues += revenue   
#              
#              
#         elif self.PolicyType == 'ForestProtection':
#             revenue = new_hh_capital.is_tianbao * self.CompensateStandard
#             new_hh_capital.cash += revenue
#             new_hh_capital.compensational_revenues += revenue   
        
        
            '''
            The following two programs involved transfers between households, rather than those from the government to households
            '''
        elif self.PolicyType == 'FarmToHomestead_Before':
            pass
        
        elif self.PolicyType == 'TakeInFarmToHomestead_Before':
            pass
        
        return new_hh_capital
        
        