'''
Created on May 11, 2015

@author: Liyan Xu
'''

class StatClass(object):
    '''
    This is the statistics class.
    '''

    def __init__(self):
        '''
        Constructor of StatClass
        '''
        
        self.StatID = ''
        self.ScenarioVersion = ''
        self.StatDate = int()
        self.Variable = ''
        self.StatValue = float()
        self.CompositeIndicator = 0
        # Indicates whether the statistics item is a composite indicator, such as 'Income Structure among Sectors'
        # 0 - No; 1 - Yes.
        # 0 by default.
    
    
    
    
    def get_population_count(self, soc, scenario_name):
         
        pp_ct = 0
         
        # Get the statistics
        for HID in soc.hh_dict:
            if soc.hh_dict[HID].is_exist == 1:
                 
                for PID in soc.hh_dict[HID].own_pp_dict:
                    if soc.hh_dict[HID].own_pp_dict[PID].is_alive == 1:
                        pp_ct += 1 # total population
         
        # Add the statistics
        self.ScenarioVersion = scenario_name
        self.StatDate = soc.current_year 
        self.Variable = 'Total_Population'
        self.StatValue = pp_ct
        self.StatID = self.Variable + '_' + str(self.StatDate)
                 
        soc.stat_dict[self.StatID] = self



    def get_household_count(self, soc, scenario_name):
         
        hh_ct = 0
         
        # Get the statistics
        for HID in soc.hh_dict:
            if soc.hh_dict[HID].is_exist == 1:
                
                hh_ct += 1 # total (existing) household count
                 
         
        # Add the statistics
        self.ScenarioVersion = scenario_name
        self.StatDate = soc.current_year 
        self.Variable = 'Household_Count'
        self.StatValue = hh_ct
        self.StatID = self.Variable + '_' + str(self.StatDate)
                 
        soc.stat_dict[self.StatID] = self


    def get_dissolved_household_count(self, soc, scenario_name):
         
        dhh_ct = 0
         
        # Get the statistics
        for HID in soc.hh_dict:
            if soc.hh_dict[HID].is_exist == 0:
                
                dhh_ct += 1 # total (existing) household count
                 
         
        # Add the statistics
        self.ScenarioVersion = scenario_name
        self.StatDate = soc.current_year 
        self.Variable = 'Dissolved_Household_Count'
        self.StatValue = dhh_ct
        self.StatID = self.Variable + '_' + str(self.StatDate)
                 
        soc.stat_dict[self.StatID] = self    
    
    
    
    def get_total_cash_savings(self, soc, scenario_name):
        
        total_cash_savings = 0
        
        # Get the statistics
        for HID in soc.hh_dict:
            if soc.hh_dict[HID].is_exist == 1:
                
                total_cash_savings = total_cash_savings + soc.hh_dict[HID].own_capital_properties.cash
                
         
        # Add the statistics
        self.ScenarioVersion = scenario_name
        self.StatDate = soc.current_year 
        self.Variable = 'Total_Cash_Savings'
        self.StatValue = total_cash_savings
        self.StatID = self.Variable + '_' + str(self.StatDate)
                 
        soc.stat_dict[self.StatID] = self      
    
    
    def get_total_debt(self, soc, scenario_name):
        
        total_debt = 0
        
        # Get the statistics
        for HID in soc.hh_dict:
            if soc.hh_dict[HID].is_exist == 1:
                
                total_debt = total_debt + soc.hh_dict[HID].own_capital_properties.debt
                
         
        # Add the statistics
        self.ScenarioVersion = scenario_name
        self.StatDate = soc.current_year 
        self.Variable = 'Total_Debt'
        self.StatValue = total_debt
        self.StatID = self.Variable + '_' + str(self.StatDate)
                 
        soc.stat_dict[self.StatID] = self



    def get_total_agriculture_income(self, soc, scenario_name):
        
        total_agriculture_income = 0
        
        # Get the statistics
        for HID in soc.hh_dict:
            if soc.hh_dict[HID].is_exist == 1:
                
                total_agriculture_income = total_agriculture_income + soc.hh_dict[HID].own_capital_properties.agriculture_income
                
         
        # Add the statistics
        self.ScenarioVersion = scenario_name
        self.StatDate = soc.current_year 
        self.Variable = 'Total_Agriculture_Income'
        self.StatValue = total_agriculture_income
        self.StatID = self.Variable + '_' + str(self.StatDate)
                 
        soc.stat_dict[self.StatID] = self   


    def get_total_tempjob_income(self, soc, scenario_name):
        
        total_tempjob_income = 0
        
        # Get the statistics
        for HID in soc.hh_dict:
            if soc.hh_dict[HID].is_exist == 1:
                
                total_tempjob_income = total_tempjob_income + soc.hh_dict[HID].own_capital_properties.temp_job_income
                
         
        # Add the statistics
        self.ScenarioVersion = scenario_name
        self.StatDate = soc.current_year 
        self.Variable = 'Total_Temp_Job_Income'
        self.StatValue = total_tempjob_income
        self.StatID = self.Variable + '_' + str(self.StatDate)
                 
        soc.stat_dict[self.StatID] = self   


    def get_total_freighttrans_income(self, soc, scenario_name):
        
        total_freighttrans_income = 0
        
        # Get the statistics
        for HID in soc.hh_dict:
            if soc.hh_dict[HID].is_exist == 1:
                
                total_freighttrans_income = total_freighttrans_income + soc.hh_dict[HID].own_capital_properties.freight_trans_income
                
         
        # Add the statistics
        self.ScenarioVersion = scenario_name
        self.StatDate = soc.current_year 
        self.Variable = 'Total_Freight_Trans_Income'
        self.StatValue = total_freighttrans_income
        self.StatID = self.Variable + '_' + str(self.StatDate)
                 
        soc.stat_dict[self.StatID] = self   


    def get_total_passengertrans_income(self, soc, scenario_name):
        
        total_passengertrans_income = 0
        
        # Get the statistics
        for HID in soc.hh_dict:
            if soc.hh_dict[HID].is_exist == 1:
                
                total_passengertrans_income = total_passengertrans_income + soc.hh_dict[HID].own_capital_properties.passenger_trans_income
                
         
        # Add the statistics
        self.ScenarioVersion = scenario_name
        self.StatDate = soc.current_year 
        self.Variable = 'Total_Passenger_Trans_Income'
        self.StatValue = total_passengertrans_income
        self.StatID = self.Variable + '_' + str(self.StatDate)
                 
        soc.stat_dict[self.StatID] = self  
            
        
        
    def get_total_lodging_income(self, soc, scenario_name):
        
        total_lodging_income = 0
        
        # Get the statistics
        for HID in soc.hh_dict:
            if soc.hh_dict[HID].is_exist == 1:
                
                total_lodging_income = total_lodging_income + soc.hh_dict[HID].own_capital_properties.lodging_income
                
         
        # Add the statistics
        self.ScenarioVersion = scenario_name
        self.StatDate = soc.current_year 
        self.Variable = 'Total_Lodging_Income'
        self.StatValue = total_lodging_income
        self.StatID = self.Variable + '_' + str(self.StatDate)
                 
        soc.stat_dict[self.StatID] = self          
        
        
        
     
        
        
        
    def get_total_renting_income(self, soc, scenario_name):
        
        total_renting_income = 0
        
        # Get the statistics
        for HID in soc.hh_dict:
            if soc.hh_dict[HID].is_exist == 1:
                
                total_renting_income = total_renting_income + soc.hh_dict[HID].own_capital_properties.renting_income
                
         
        # Add the statistics
        self.ScenarioVersion = scenario_name
        self.StatDate = soc.current_year 
        self.Variable = 'Total_Renting_Income'
        self.StatValue = total_renting_income
        self.StatID = self.Variable + '_' + str(self.StatDate)
                 
        soc.stat_dict[self.StatID] = self          


    
    def get_sectors_income_structure(self, soc, scenario_name):
        
        self.ScenarioVersion = scenario_name
        self.StatDate = soc.current_year
        self.Variable = 'Sectors_Income_Structure'
        self.StatValue = 0
        self.StatID = self.Variable + '_' + str(self.StatDate)
        
        self.CompositeIndicator = 1 # Make it a composite indicator

        soc.stat_dict[self.StatID] = self 
        
        
        
        
        
        
        
        
        
        
        
           