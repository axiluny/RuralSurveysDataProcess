'''
Created on May 30, 2015

@author: Liyan Xu
'''

import copy

class Policy(object):
    '''
    The Policy Class
    '''


    def __init__(self, record, VarList):
        '''
        This is the policy class
        '''        
        # Set the attributes (var) and their values (record) from the policy programs table in the DB.                
        for var in VarList:
            setattr(self, var[0], record[var[1]])
    
    
    
    def apply_policy_terms(self, hh_capital, model_parameters):
        
        new_hh_capital = copy.deepcopy(hh_capital)
        
        revenue = float()
        
        
        if self.PolicyType == 'FarmToForest_After':
            if new_hh_capital.farm_to_forest == 0: # Never joined in the program
                new_hh_capital.farm_to_forest = hh_capital.farmland
                new_hh_capital.farmland = 0
                new_hh_capital.av_farmland = 0
            
            revenue = new_hh_capital.farm_to_forest * self.CompensateStandard
            new_hh_capital.cash += revenue
            new_hh_capital.compensational_revenues += revenue
            
            
        elif self.PolicyType == 'FarmToForest_Before':
            pass
        elif self.PolicyType == 'FarmToBamboo_Before':
            pass
        elif self.PolicyType == 'ForestProtection':
            pass
        
        
        return new_hh_capital
        
        