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
        self.StatUnit = ''

        
        '''
        # Properties for special statistics items
        
        composite indicators - indicates whether the statistics item is a composite indicator, such as 'Income Structure among Sectors'
            0 - No; 1 - Yes. 0 by default.
        
        map layers - indicates whether the statistics item is a map layer (not actually a statistics item)
            0 - No; 1 - Yes. 0 by default.
                    
        '''                
        # composite indicators
        self.CompositeIndicator = 0
        
        # map layers
        self.MapLayer = 0
    
        '''
        Property indicating if the starting point statistics is meaningful.
        E.g. income variables are "void" at the starting point since no economic activities have taken place yet;
        while land use variable are meaningful at the starting point.
        '''    
        self.StartingPointEffective = int()
        
        
    '''
    Single Variables
    '''
    
    '''
    Basic Demographics
    '''
    
    def get_population_count(self, society_instance, scenario_name):
         
        pp_ct = 0
         
        # Get the statistics
        for HID in society_instance.hh_dict:
            if society_instance.hh_dict[HID].is_exist == 1:
                 
                for PID in society_instance.hh_dict[HID].own_pp_dict:
                    if society_instance.hh_dict[HID].own_pp_dict[PID].is_alive == 1:
                        pp_ct += 1 # total population
         
        # Add the statistics
        self.ScenarioVersion = scenario_name
        self.StatDate = society_instance.current_year 
        self.Variable = 'I-01 Population'
        self.StatValue = pp_ct
        self.StatUnit = 'Persons'
        self.StatID = self.Variable + '_' + str(self.StatDate)
        
        self.StartingPointEffective = 1
                 
        society_instance.stat_dict[self.StatID] = self



    def get_household_count(self, society_instance, scenario_name):
         
        hh_ct = 0
         
        # Get the statistics
        for HID in society_instance.hh_dict:
            if society_instance.hh_dict[HID].is_exist == 1:
                
                hh_ct += 1 # total (existing) household count
                 
         
        # Add the statistics
        self.ScenarioVersion = scenario_name
        self.StatDate = society_instance.current_year 
        self.Variable = 'I-02 Existing Household'
        self.StatValue = hh_ct
        self.StatUnit = 'Households'
        self.StatID = self.Variable + '_' + str(self.StatDate)
        
        self.StartingPointEffective = 1
                 
        society_instance.stat_dict[self.StatID] = self


    def get_dissolved_household_count(self, society_instance, scenario_name):
         
        dhh_ct = 0
         
        # Get the statistics
        for HID in society_instance.hh_dict:
            if society_instance.hh_dict[HID].is_exist == 0:
                
                dhh_ct += 1 # total (existing) household count
                 
         
        # Add the statistics
        self.ScenarioVersion = scenario_name
        self.StatDate = society_instance.current_year 
        self.Variable = 'I-03 Dissolved Household'
        self.StatValue = dhh_ct
        self.StatUnit = 'Households'
        self.StatID = self.Variable + '_' + str(self.StatDate)
        
        self.StartingPointEffective = 0
                 
        society_instance.stat_dict[self.StatID] = self    
    
    '''
    Demographics - Education
    '''

    def get_preschool_stu(self, society_instance, scenario_name):
         
        preschool_stu = 0
         
        # Get the statistics
        for HID in society_instance.hh_dict:
            if society_instance.hh_dict[HID].is_exist == 1:
                 
                for PID in society_instance.hh_dict[HID].own_pp_dict:
                    if society_instance.hh_dict[HID].own_pp_dict[PID].Education == 'preschool':
                        preschool_stu += 1 # total population
         
        # Add the statistics
        self.ScenarioVersion = scenario_name
        self.StatDate = society_instance.current_year 
        self.Variable = 'I-04 Preschool'
        self.StatValue = preschool_stu
        self.StatUnit = 'Persons'
        self.StatID = self.Variable + '_' + str(self.StatDate)
        
        self.StartingPointEffective = 1
                 
        society_instance.stat_dict[self.StatID] = self



    def get_primaryschool_stu(self, society_instance, scenario_name):
         
        primaryschool_stu = 0
         
        # Get the statistics
        for HID in society_instance.hh_dict:
            if society_instance.hh_dict[HID].is_exist == 1:
                 
                for PID in society_instance.hh_dict[HID].own_pp_dict:
                    if society_instance.hh_dict[HID].own_pp_dict[PID].Education == 'primary':
                        primaryschool_stu += 1 # total population
         
        # Add the statistics
        self.ScenarioVersion = scenario_name
        self.StatDate = society_instance.current_year 
        self.Variable = 'I-05 Primary School'
        self.StatValue = primaryschool_stu
        self.StatUnit = 'Persons'
        self.StatID = self.Variable + '_' + str(self.StatDate)
        
        self.StartingPointEffective = 1
                 
        society_instance.stat_dict[self.StatID] = self
    

    def get_secondaryschool_stu(self, society_instance, scenario_name):
         
        secondaryschool_stu = 0
         
        # Get the statistics
        for HID in society_instance.hh_dict:
            if society_instance.hh_dict[HID].is_exist == 1:
                 
                for PID in society_instance.hh_dict[HID].own_pp_dict:
                    if society_instance.hh_dict[HID].own_pp_dict[PID].Education == 'secondary':
                        secondaryschool_stu += 1 # total population
         
        # Add the statistics
        self.ScenarioVersion = scenario_name
        self.StatDate = society_instance.current_year 
        self.Variable = 'I-06 Secondary School'
        self.StatValue = secondaryschool_stu
        self.StatUnit = 'Persons'
        self.StatID = self.Variable + '_' + str(self.StatDate)
        
        self.StartingPointEffective = 1
                 
        society_instance.stat_dict[self.StatID] = self



    def get_highschool_stu(self, society_instance, scenario_name):
         
        highschool_stu = 0
         
        # Get the statistics
        for HID in society_instance.hh_dict:
            if society_instance.hh_dict[HID].is_exist == 1:
                 
                for PID in society_instance.hh_dict[HID].own_pp_dict:
                    if society_instance.hh_dict[HID].own_pp_dict[PID].Education == 'high_school':
                        highschool_stu += 1 # total population
         
        # Add the statistics
        self.ScenarioVersion = scenario_name
        self.StatDate = society_instance.current_year 
        self.Variable = 'I-07 High School'
        self.StatValue = highschool_stu
        self.StatUnit = 'Persons'
        self.StatID = self.Variable + '_' + str(self.StatDate)
        
        self.StartingPointEffective = 1
                 
        society_instance.stat_dict[self.StatID] = self    



    def get_college_stu(self, society_instance, scenario_name):
         
        college_stu = 0
         
        # Get the statistics
        for HID in society_instance.hh_dict:
            if society_instance.hh_dict[HID].is_exist == 1:
                 
                for PID in society_instance.hh_dict[HID].own_pp_dict:
                    if society_instance.hh_dict[HID].own_pp_dict[PID].Education == 'college':
                        college_stu += 1 # total population
         
        # Add the statistics
        self.ScenarioVersion = scenario_name
        self.StatDate = society_instance.current_year 
        self.Variable = 'I-08 College'
        self.StatValue = college_stu
        self.StatUnit = 'Persons'
        self.StatID = self.Variable + '_' + str(self.StatDate)
        
        self.StartingPointEffective = 1
                 
        society_instance.stat_dict[self.StatID] = self    



    def get_uneducated(self, society_instance, scenario_name):
         
        uneducated = 0
         
        # Get the statistics
        for HID in society_instance.hh_dict:
            if society_instance.hh_dict[HID].is_exist == 1:
                 
                for PID in society_instance.hh_dict[HID].own_pp_dict:
                    if society_instance.hh_dict[HID].own_pp_dict[PID].Education == 'uneducated':
                        uneducated += 1 # total population
         
        # Add the statistics
        self.ScenarioVersion = scenario_name
        self.StatDate = society_instance.current_year 
        self.Variable = 'I-09 Uneducated'
        self.StatValue = uneducated
        self.StatUnit = 'Persons'
        self.StatID = self.Variable + '_' + str(self.StatDate)
        
        self.StartingPointEffective = 1
                 
        society_instance.stat_dict[self.StatID] = self    


    
    
    '''
    Basic society_instanceial indicators
    '''
        
    def get_pref_labor_risk_aversion_hh_count(self, society_instance, scenario_name):
        
        tpye_1_hh_ct = 0
         
        # Get the statistics
        for HID in society_instance.hh_dict:
            if society_instance.hh_dict[HID].is_exist == 1 and society_instance.hh_dict[HID].hh_preference_type == 1:
                
                tpye_1_hh_ct += 1
                 
         
        # Add the statistics
        self.ScenarioVersion = scenario_name
        self.StatDate = society_instance.current_year 
        self.Variable = 'II-01 Pref Labor_Risk Aversion HH Count'
        self.StatValue = tpye_1_hh_ct
        self.StatUnit = 'Households'
        self.StatID = self.Variable + '_' + str(self.StatDate)
        
        self.StartingPointEffective = 0
                 
        society_instance.stat_dict[self.StatID] = self          
    
    
    def get_pref_leisure_risk_aversion_hh_count(self, society_instance, scenario_name):
        
        tpye_2_hh_ct = 0
         
        # Get the statistics
        for HID in society_instance.hh_dict:
            if society_instance.hh_dict[HID].is_exist == 1 and society_instance.hh_dict[HID].hh_preference_type == 2:
                
                tpye_2_hh_ct += 1
                 
         
        # Add the statistics
        self.ScenarioVersion = scenario_name
        self.StatDate = society_instance.current_year 
        self.Variable = 'II-02 Pref Leisure_Risk Aversion HH Count'
        self.StatValue = tpye_2_hh_ct
        self.StatUnit = 'Households'
        self.StatID = self.Variable + '_' + str(self.StatDate)
        
        self.StartingPointEffective = 0
                 
        society_instance.stat_dict[self.StatID] = self              
    

    def get_pref_labor_risk_appetite_hh_count(self, society_instance, scenario_name):
        
        tpye_3_hh_ct = 0
         
        # Get the statistics
        for HID in society_instance.hh_dict:
            if society_instance.hh_dict[HID].is_exist == 1 and society_instance.hh_dict[HID].hh_preference_type == 3:
                
                tpye_3_hh_ct += 1
                 
         
        # Add the statistics
        self.ScenarioVersion = scenario_name
        self.StatDate = society_instance.current_year 
        self.Variable = 'II-03 Pref Labor_Risk Appetite HH Count'
        self.StatValue = tpye_3_hh_ct
        self.StatUnit = 'Households'
        self.StatID = self.Variable + '_' + str(self.StatDate)
        
        self.StartingPointEffective = 0
                 
        society_instance.stat_dict[self.StatID] = self     


    def get_pref_leisure_risk_appetite_hh_count(self, society_instance, scenario_name):
        
        tpye_4_hh_ct = 0
         
        # Get the statistics
        for HID in society_instance.hh_dict:
            if society_instance.hh_dict[HID].is_exist == 1 and society_instance.hh_dict[HID].hh_preference_type == 4:
                
                tpye_4_hh_ct += 1
                 
         
        # Add the statistics
        self.ScenarioVersion = scenario_name
        self.StatDate = society_instance.current_year 
        self.Variable = 'II-04 Pref Leisure_Risk Appetite HH Count'
        self.StatValue = tpye_4_hh_ct
        self.StatUnit = 'Households'
        self.StatID = self.Variable + '_' + str(self.StatDate)
        
        self.StartingPointEffective = 0
                 
        society_instance.stat_dict[self.StatID] = self 


    def get_housedhold_business_type_0_count(self, society_instance, scenario_name):
        
        business_type_0_hh_ct = 0
        
        # Get the statistics
        for HID in society_instance.hh_dict:
            if society_instance.hh_dict[HID].is_exist == 1 and society_instance.hh_dict[HID].business_type == 0:
                
                business_type_0_hh_ct += 1

        # Add the statistics
        self.ScenarioVersion = scenario_name
        self.StatDate = society_instance.current_year 
        self.Variable = 'II-05 Agriculture Only Households Count'
        self.StatValue = business_type_0_hh_ct
        self.StatUnit = 'Households'
        self.StatID = self.Variable + '_' + str(self.StatDate)
        
        self.StartingPointEffective = 0
                 
        society_instance.stat_dict[self.StatID] = self 


    def get_housedhold_business_type_1_count(self, society_instance, scenario_name):
        
        business_type_1_hh_ct = 0
        
        # Get the statistics
        for HID in society_instance.hh_dict:
            if society_instance.hh_dict[HID].is_exist == 1 and society_instance.hh_dict[HID].business_type == 1:
                
                business_type_1_hh_ct += 1

        # Add the statistics
        self.ScenarioVersion = scenario_name
        self.StatDate = society_instance.current_year 
        self.Variable = 'II-06 Agriculture and One Other Business Households Count'
        self.StatValue = business_type_1_hh_ct
        self.StatUnit = 'Households'
        self.StatID = self.Variable + '_' + str(self.StatDate)
        
        self.StartingPointEffective = 0
                 
        society_instance.stat_dict[self.StatID] = self 


    def get_housedhold_business_type_2_count(self, society_instance, scenario_name):
        
        business_type_2_hh_ct = 0
        
        # Get the statistics
        for HID in society_instance.hh_dict:
            if society_instance.hh_dict[HID].is_exist == 1 and society_instance.hh_dict[HID].business_type == 2:
                
                business_type_2_hh_ct += 1

        # Add the statistics
        self.ScenarioVersion = scenario_name
        self.StatDate = society_instance.current_year 
        self.Variable = 'II-07 Agriculture and More than One Other Businesses Households Count'
        self.StatValue = business_type_2_hh_ct
        self.StatUnit = 'Households'
        self.StatID = self.Variable + '_' + str(self.StatDate)
        
        self.StartingPointEffective = 0
                 
        society_instance.stat_dict[self.StatID] = self 
    
    
    '''
    Basic Economic Statistics
    '''
    
    def get_total_net_savings(self, society_instance, scenario_name):
        
        total_net_savings = 0
        
        # Get the statistics
        for HID in society_instance.hh_dict:
            if society_instance.hh_dict[HID].is_exist == 1:
                
                total_net_savings += society_instance.hh_dict[HID].own_capital_properties.netsavings
                
         
        # Add the statistics
        self.ScenarioVersion = scenario_name
        self.StatDate = society_instance.current_year 
        self.Variable = 'III-01 Total Household Net Savings'
        self.StatValue = total_net_savings
        self.StatUnit = 'Yuan (RMB)'
        self.StatID = self.Variable + '_' + str(self.StatDate)
                 
        self.StartingPointEffective = 1

        society_instance.stat_dict[self.StatID] = self 
            
    
    def get_total_cash_savings(self, society_instance, scenario_name):
        
        total_cash_savings = 0
        
        # Get the statistics
        for HID in society_instance.hh_dict:
            if society_instance.hh_dict[HID].is_exist == 1:
                
                total_cash_savings += society_instance.hh_dict[HID].own_capital_properties.cash
                
         
        # Add the statistics
        self.ScenarioVersion = scenario_name
        self.StatDate = society_instance.current_year 
        self.Variable = 'III-02 Total Household Cash Reserve'
        self.StatValue = total_cash_savings
        self.StatUnit = 'Yuan (RMB)'
        self.StatID = self.Variable + '_' + str(self.StatDate)
                 
        self.StartingPointEffective = 1

        society_instance.stat_dict[self.StatID] = self      
    
    
    def get_total_debt(self, society_instance, scenario_name):
        
        total_debt = 0
        
        # Get the statistics
        for HID in society_instance.hh_dict:
            if society_instance.hh_dict[HID].is_exist == 1:
                
                total_debt += society_instance.hh_dict[HID].own_capital_properties.debt
                
         
        # Add the statistics
        self.ScenarioVersion = scenario_name
        self.StatDate = society_instance.current_year 
        self.Variable = 'III-03 Total Household Debt'
        self.StatValue = total_debt
        self.StatUnit = 'Yuan (RMB)'
        self.StatID = self.Variable + '_' + str(self.StatDate)
                 
        self.StartingPointEffective = 1

        society_instance.stat_dict[self.StatID] = self


    def get_gross_annual_income(self, society_instance, scenario_name):
        
        gross_annual_income = 0
        
        # Get the statistics
        for HID in society_instance.hh_dict:
            if society_instance.hh_dict[HID].is_exist == 1:
                
                gross_annual_income += society_instance.hh_dict[HID].own_capital_properties.get_total_business_income()\
                                    + society_instance.hh_dict[HID].own_capital_properties.compensational_revenues
                
         
        # Add the statistics
        self.ScenarioVersion = scenario_name
        self.StatDate = society_instance.current_year 
        self.Variable = 'III-04 Gross Annual Household Income'
        self.StatValue = gross_annual_income
        self.StatUnit = 'Yuan (RMB)'
        self.StatID = self.Variable + '_' + str(self.StatDate)
                 
        self.StartingPointEffective = 0

        society_instance.stat_dict[self.StatID] = self        


    def get_gross_business_revenues(self, society_instance, scenario_name):
        gross_business_revenues = 0
        
        # Get the statistics
        for HID in society_instance.hh_dict:
            if society_instance.hh_dict[HID].is_exist == 1:
                
                gross_business_revenues += society_instance.hh_dict[HID].own_capital_properties.get_total_business_income()
                
         
        # Add the statistics
        self.ScenarioVersion = scenario_name
        self.StatDate = society_instance.current_year 
        self.Variable = 'III-05 Gross Annual Household Business Revenues'
        self.StatValue = gross_business_revenues
        self.StatUnit = 'Yuan (RMB)'
        self.StatID = self.Variable + '_' + str(self.StatDate)
                 
        self.StartingPointEffective = 0

        society_instance.stat_dict[self.StatID] = self       
    
    
    def get_gross_compensational_revenues(self, society_instance, scenario_name):
        gross_compensational_revenues = 0
        
        # Get the statistics
        for HID in society_instance.hh_dict:
            if society_instance.hh_dict[HID].is_exist == 1:
                
                gross_compensational_revenues += society_instance.hh_dict[HID].own_capital_properties.compensational_revenues
                
         
        # Add the statistics
        self.ScenarioVersion = scenario_name
        self.StatDate = society_instance.current_year 
        self.Variable = 'III-06 Gross Annual Household Compensational Revenues'
        self.StatValue = gross_compensational_revenues
        self.StatUnit = 'Yuan (RMB)'
        self.StatID = self.Variable + '_' + str(self.StatDate)
                 
        self.StartingPointEffective = 0

        society_instance.stat_dict[self.StatID] = self
                

    def get_annual_income_per_person(self, society_instance, scenario_name):
        
        gross_annual_income = 0
        pp_ct = 0
        
        # Get the statistics
        for HID in society_instance.hh_dict:
            if society_instance.hh_dict[HID].is_exist == 1:
                
                gross_annual_income += society_instance.hh_dict[HID].own_capital_properties.get_total_business_income()\
                                    + society_instance.hh_dict[HID].own_capital_properties.compensational_revenues
                                    
                for PID in society_instance.hh_dict[HID].own_pp_dict:
                    if society_instance.hh_dict[HID].own_pp_dict[PID].is_alive == 1:
                        pp_ct += 1
         
        # Add the statistics
        self.ScenarioVersion = scenario_name
        self.StatDate = society_instance.current_year 
        self.Variable = 'III-07 Annual Income per Person'
        self.StatValue = gross_annual_income / pp_ct
        self.StatUnit = 'Yuan (RMB)'
        self.StatID = self.Variable + '_' + str(self.StatDate)
                 
        self.StartingPointEffective = 0

        society_instance.stat_dict[self.StatID] = self  


    def get_annual_income_per_household(self, society_instance, scenario_name):
        
        gross_annual_income = 0
        hh_ct = 0
        
        # Get the statistics
        for HID in society_instance.hh_dict:
            if society_instance.hh_dict[HID].is_exist == 1:
                
                gross_annual_income += society_instance.hh_dict[HID].own_capital_properties.get_total_business_income()\
                                    + society_instance.hh_dict[HID].own_capital_properties.compensational_revenues
                
                hh_ct += 1
         
        # Add the statistics
        self.ScenarioVersion = scenario_name
        self.StatDate = society_instance.current_year 
        self.Variable = 'III-08 Annual Income per Household'
        self.StatValue = gross_annual_income / hh_ct
        self.StatUnit = 'Yuan (RMB)'
        self.StatID = self.Variable + '_' + str(self.StatDate)
                 
        self.StartingPointEffective = 0

        society_instance.stat_dict[self.StatID] = self  


#     def get_trucks_count(self, society_instance, scenario_name):
#         trucks_count = 0
#         
#         # Get the statistics
#         for HID in society_instance.hh_dict:
#             if society_instance.hh_dict[HID].is_exist == 1:
#                 
#                 trucks_count += society_instance.hh_dict[HID].own_capital_properties.truck
#                 
#          
#         # Add the statistics
#         self.ScenarioVersion = scenario_name
#         self.StatDate = society_instance.current_year 
#         self.Variable = 'III-09 Trucks Count'
#         self.StatValue = trucks_count
#         self.StatUnit = 'Trucks'
#         self.StatID = self.Variable + '_' + str(self.StatDate)
#                  
#         self.StartingPointEffective = 1
# 
#         society_instance.stat_dict[self.StatID] = self      
# 
# 
#     def get_minibuses_count(self, society_instance, scenario_name):
#         minibuses_count = 0
#         
#         # Get the statistics
#         for HID in society_instance.hh_dict:
#             if society_instance.hh_dict[HID].is_exist == 1:
#                 
#                 minibuses_count += society_instance.hh_dict[HID].own_capital_properties.minibus
#                 
#          
#         # Add the statistics
#         self.ScenarioVersion = scenario_name
#         self.StatDate = society_instance.current_year 
#         self.Variable = 'III-10 Minibuses Count'
#         self.StatValue = minibuses_count
#         self.StatUnit = 'Mini-buses'
#         self.StatID = self.Variable + '_' + str(self.StatDate)
#                  
#         self.StartingPointEffective = 1
# 
#         society_instance.stat_dict[self.StatID] = self     

    '''
    Income and employment by sectors
    '''

    def get_total_agriculture_income(self, society_instance, scenario_name):
        
        total_agriculture_income = 0
        
        # Get the statistics
        for HID in society_instance.hh_dict:
            if society_instance.hh_dict[HID].is_exist == 1:
                
                total_agriculture_income += society_instance.hh_dict[HID].own_capital_properties.agriculture_income
                
         
        # Add the statistics
        self.ScenarioVersion = scenario_name
        self.StatDate = society_instance.current_year 
        self.Variable = 'IV-01 Total Agriculture Income'
        self.StatValue = total_agriculture_income
        self.StatUnit = 'Yuan (RMB)'
        self.StatID = self.Variable + '_' + str(self.StatDate)
                 
        self.StartingPointEffective = 0

        society_instance.stat_dict[self.StatID] = self   


    def get_total_tempjob_income(self, society_instance, scenario_name):
        
        total_tempjob_income = 0
        
        # Get the statistics
        for HID in society_instance.hh_dict:
            if society_instance.hh_dict[HID].is_exist == 1:
                
                total_tempjob_income += society_instance.hh_dict[HID].own_capital_properties.temp_job_income
                
         
        # Add the statistics
        self.ScenarioVersion = scenario_name
        self.StatDate = society_instance.current_year 
        self.Variable = 'IV-02 Total Temp Job Income'
        self.StatValue = total_tempjob_income
        self.StatUnit = 'Yuan (RMB)'
        self.StatID = self.Variable + '_' + str(self.StatDate)
                 
        self.StartingPointEffective = 0

        society_instance.stat_dict[self.StatID] = self   


    def get_total_freighttrans_income(self, society_instance, scenario_name):
        
        total_freighttrans_income = 0
        
        # Get the statistics
        for HID in society_instance.hh_dict:
            if society_instance.hh_dict[HID].is_exist == 1:
                
                total_freighttrans_income += society_instance.hh_dict[HID].own_capital_properties.freight_trans_income
                
         
        # Add the statistics
        self.ScenarioVersion = scenario_name
        self.StatDate = society_instance.current_year 
        self.Variable = 'IV-03 Total Freight Trans Income'
        self.StatValue = total_freighttrans_income
        self.StatUnit = 'Yuan (RMB)'
        self.StatID = self.Variable + '_' + str(self.StatDate)
                 
        self.StartingPointEffective = 0

        society_instance.stat_dict[self.StatID] = self   


    def get_total_passengertrans_income(self, society_instance, scenario_name):
        
        total_passengertrans_income = 0
        
        # Get the statistics
        for HID in society_instance.hh_dict:
            if society_instance.hh_dict[HID].is_exist == 1:
                
                total_passengertrans_income += society_instance.hh_dict[HID].own_capital_properties.passenger_trans_income
                
         
        # Add the statistics
        self.ScenarioVersion = scenario_name
        self.StatDate = society_instance.current_year 
        self.Variable = 'IV-04 Total Passenger Trans Income'
        self.StatValue = total_passengertrans_income
        self.StatUnit = 'Yuan (RMB)'
        self.StatID = self.Variable + '_' + str(self.StatDate)
                 
        self.StartingPointEffective = 0

        society_instance.stat_dict[self.StatID] = self  
            
        
        
    def get_total_lodging_income(self, society_instance, scenario_name):
        
        total_lodging_income = 0
        
        # Get the statistics
        for HID in society_instance.hh_dict:
            if society_instance.hh_dict[HID].is_exist == 1:
                
                total_lodging_income += society_instance.hh_dict[HID].own_capital_properties.lodging_income
                
         
        # Add the statistics
        self.ScenarioVersion = scenario_name
        self.StatDate = society_instance.current_year 
        self.Variable = 'IV-05 Total Lodging Income'
        self.StatValue = total_lodging_income
        self.StatUnit = 'Yuan (RMB)'
        self.StatID = self.Variable + '_' + str(self.StatDate)
                 
        self.StartingPointEffective = 0

        society_instance.stat_dict[self.StatID] = self          
             
        
        
        
    def get_total_renting_income(self, society_instance, scenario_name):
        
        total_renting_income = 0
        
        # Get the statistics
        for HID in society_instance.hh_dict:
            if society_instance.hh_dict[HID].is_exist == 1:
                
                total_renting_income += society_instance.hh_dict[HID].own_capital_properties.renting_income
                
         
        # Add the statistics
        self.ScenarioVersion = scenario_name
        self.StatDate = society_instance.current_year 
        self.Variable = 'IV-06 Total Renting Income'
        self.StatValue = total_renting_income
        self.StatUnit = 'Yuan (RMB)'
        self.StatID = self.Variable + '_' + str(self.StatDate)
                 
        self.StartingPointEffective = 0

        society_instance.stat_dict[self.StatID] = self          


    def get_agriculture_employment_ratio(self, society_instance, scenario_name):
        
        agriculture_employment = 0
        hh_ct = 0
        
        # Get the statistics
        for HID in society_instance.hh_dict:
            if society_instance.hh_dict[HID].is_exist == 1:
                
                hh_ct += 1
                
                for sector in society_instance.hh_dict[HID].own_current_sectors:
                    if sector.SectorName == 'Agriculture':
                        agriculture_employment += 1
                         
        # Add the statistics
        self.ScenarioVersion = scenario_name
        self.StatDate = society_instance.current_year 
        self.Variable = 'IV-07 Agriculture Employment Ratio'
        self.StatValue = float(agriculture_employment * 100) / float(hh_ct)
        self.StatUnit = 'Percent'
        self.StatID = self.Variable + '_' + str(self.StatDate)
                 
        self.StartingPointEffective = 0

        society_instance.stat_dict[self.StatID] = self


    def get_tempjob_employment_ratio(self, society_instance, scenario_name):
        
        tempjob_employment = 0
        hh_ct = 0
        
        # Get the statistics
        for HID in society_instance.hh_dict:
            if society_instance.hh_dict[HID].is_exist == 1:
                
                hh_ct += 1
                
                for sector in society_instance.hh_dict[HID].own_current_sectors:
                    if sector.SectorName == 'TempJob':
                        tempjob_employment += 1
                         
        # Add the statistics
        self.ScenarioVersion = scenario_name
        self.StatDate = society_instance.current_year 
        self.Variable = 'IV-08 Temp Jobs Employment Ratio'
        self.StatValue = float(tempjob_employment * 100) / float(hh_ct)
        self.StatUnit = 'Percent'
        self.StatID = self.Variable + '_' + str(self.StatDate)
                 
        self.StartingPointEffective = 0

        society_instance.stat_dict[self.StatID] = self


    def get_freighttrans_employment_ratio(self, society_instance, scenario_name):
        
        freighttrans_employment = 0
        hh_ct = 0
        
        # Get the statistics
        for HID in society_instance.hh_dict:
            if society_instance.hh_dict[HID].is_exist == 1:
                
                hh_ct += 1
                
                for sector in society_instance.hh_dict[HID].own_current_sectors:
                    if sector.SectorName == 'FreightTrans':
                        freighttrans_employment += 1
                         
        # Add the statistics
        self.ScenarioVersion = scenario_name
        self.StatDate = society_instance.current_year 
        self.Variable = 'IV-09 Freight Trans Employment Ratio'
        self.StatValue = float(freighttrans_employment * 100) / float(hh_ct)
        self.StatUnit = 'Percent'
        self.StatID = self.Variable + '_' + str(self.StatDate)
                 
        self.StartingPointEffective = 0

        society_instance.stat_dict[self.StatID] = self


    def get_passengertrans_employment_ratio(self, society_instance, scenario_name):
        
        passengertrans_employment = 0
        hh_ct = 0
        
        # Get the statistics
        for HID in society_instance.hh_dict:
            if society_instance.hh_dict[HID].is_exist == 1:
                
                hh_ct += 1
                
                for sector in society_instance.hh_dict[HID].own_current_sectors:
                    if sector.SectorName == 'PassengerTrans':
                        passengertrans_employment += 1
                         
        # Add the statistics
        self.ScenarioVersion = scenario_name
        self.StatDate = society_instance.current_year 
        self.Variable = 'IV-10 Passenger Trans Employment Ratio'
        self.StatValue = float(passengertrans_employment * 100) / float(hh_ct)
        self.StatUnit = 'Percent'
        self.StatID = self.Variable + '_' + str(self.StatDate)
                 
        self.StartingPointEffective = 0

        society_instance.stat_dict[self.StatID] = self        


    def get_lodging_employment_ratio(self, society_instance, scenario_name):
        
        lodging_employment = 0
        hh_ct = 0
        
        # Get the statistics
        for HID in society_instance.hh_dict:
            if society_instance.hh_dict[HID].is_exist == 1:
                
                hh_ct += 1
                
                for sector in society_instance.hh_dict[HID].own_current_sectors:
                    if sector.SectorName == 'Lodging':
                        lodging_employment += 1
                         
        # Add the statistics
        self.ScenarioVersion = scenario_name
        self.StatDate = society_instance.current_year 
        self.Variable = 'IV-11 Lodging Employment Ratio'
        self.StatValue = float(lodging_employment * 100) / float(hh_ct)
        self.StatUnit = 'Percent'
        self.StatID = self.Variable + '_' + str(self.StatDate)
                 
        self.StartingPointEffective = 0

        society_instance.stat_dict[self.StatID] = self


    def get_renting_employment_ratio(self, society_instance, scenario_name):
        
        renting_employment = 0
        hh_ct = 0
        
        # Get the statistics
        for HID in society_instance.hh_dict:
            if society_instance.hh_dict[HID].is_exist == 1:
                
                hh_ct += 1
                
                for sector in society_instance.hh_dict[HID].own_current_sectors:
                    if sector.SectorName == 'Renting':
                        renting_employment += 1
                         
        # Add the statistics
        self.ScenarioVersion = scenario_name
        self.StatDate = society_instance.current_year 
        self.Variable = 'IV-12 Renting Employment Ratio'
        self.StatValue = float(renting_employment * 100) / float(hh_ct)
        self.StatUnit = 'Percent'
        self.StatID = self.Variable + '_' + str(self.StatDate)
                 
        self.StartingPointEffective = 0

        society_instance.stat_dict[self.StatID] = self


    '''
    Land variables
    '''
    
    def get_total_farmland_area(self, society_instance, scenario_name):
        
        farmland_area = 0

        # Get the statistics
        for ParcelID in society_instance.land_dict:
            if society_instance.land_dict[ParcelID].LandCover == 'Cultivate':
                farmland_area += society_instance.land_dict[ParcelID].Shape_Area / 666.7
        
        
        '''
        Another way: get the farmland area household by household
        '''
#         for HID in society_instance.hh_dict:
#             if society_instance.hh_dict[HID].is_exist == 1:
#                  
#                 farmland_area += society_instance.hh_dict[HID].own_capital_properties.farmland
                         
        # Add the statistics
        self.ScenarioVersion = scenario_name
        self.StatDate = society_instance.current_year 
        self.Variable = 'V-01 Total Farmland Area'
        self.StatValue = farmland_area
        self.StatUnit = 'Chinese Acres (1 CA = 0.067 Hectare)'
        self.StatID = self.Variable + '_' + str(self.StatDate)
                 
        self.StartingPointEffective = 1

        society_instance.stat_dict[self.StatID] = self


    def get_abandoned_farmland_area(self, society_instance, scenario_name):
        
        abandoned_farmland_area = 0
        
        # Get the statistics
        if society_instance.current_year == society_instance.start_year:
            abandoned_farmland_area = 0
        else:        
            for HID in society_instance.hh_dict:
                if society_instance.hh_dict[HID].is_exist == 1:
                    '''
                    The two methods should yield the same results
                    '''
                    
    #                 abandoned_farmland_area += society_instance.hh_dict[HID].own_capital_properties.av_farmland
                    
                    for land_parcel in society_instance.hh_dict[HID].own_capital_properties.land_properties_list:
                        if land_parcel.actual_farming == False:
                            abandoned_farmland_area += land_parcel.Shape_Area / 666.7
                         
                         
        # Add the statistics
        self.ScenarioVersion = scenario_name
        self.StatDate = society_instance.current_year 
        self.Variable = 'V-02 Total Abandoned Farmland Area'
        self.StatValue = abandoned_farmland_area
        self.StatUnit = 'Chinese Acres (1 CA = 0.067 Hectare)'
        self.StatID = self.Variable + '_' + str(self.StatDate)
                 
        self.StartingPointEffective = 1

        society_instance.stat_dict[self.StatID] = self
    

    def get_reverted_farmland_area(self, society_instance, scenario_name):
        
        reverted_farmland_area = 0
        
        # Get the statistics
        for HID in society_instance.hh_dict:
            if society_instance.hh_dict[HID].is_exist == 1:
                
                reverted_farmland_area += society_instance.hh_dict[HID].own_capital_properties.farm_to_forest
                         
        # Add the statistics
        self.ScenarioVersion = scenario_name
        self.StatDate = society_instance.current_year 
        self.Variable = 'V-03 Total Reverted Farmland Area'
        self.StatValue = reverted_farmland_area
        self.StatUnit = 'Chinese Acres (1 CA = 0.067 Hectare)'
        self.StatID = self.Variable + '_' + str(self.StatDate)
                 
        self.StartingPointEffective = 1

        society_instance.stat_dict[self.StatID] = self    
    
    

    def get_total_construction_land_area(self, society_instance, scenario_name):
        
        construction_area = 0
        
        # Get the statistics
        for ParcelID in society_instance.land_dict:
            if society_instance.land_dict[ParcelID].LandCover == 'Construction':
                construction_area += society_instance.land_dict[ParcelID].Shape_Area / 666.7
        
        
        # Add the statistics
        self.ScenarioVersion = scenario_name
        self.StatDate = society_instance.current_year 
        self.Variable = 'V-04 Total Construction Land Area'
        self.StatValue = construction_area
        self.StatUnit = 'Chinese Acres (1 CA = 0.067 Hectare)'
        self.StatID = self.Variable + '_' + str(self.StatDate)
                 
        self.StartingPointEffective = 1

        society_instance.stat_dict[self.StatID] = self         


    def get_total_grassland_area(self, society_instance, scenario_name):
        
        grassland_area = 0
        
        # Get the statistics
        for ParcelID in society_instance.land_dict:
            if society_instance.land_dict[ParcelID].LandCover == 'Grass':
                grassland_area += society_instance.land_dict[ParcelID].Shape_Area / 666.7
        
        
        # Add the statistics
        self.ScenarioVersion = scenario_name
        self.StatDate = society_instance.current_year 
        self.Variable = 'V-05 Total Grassland Area'
        self.StatValue = grassland_area
        self.StatUnit = 'Chinese Acres (1 CA = 0.067 Hectare)'
        self.StatID = self.Variable + '_' + str(self.StatDate)
                 
        self.StartingPointEffective = 1

        society_instance.stat_dict[self.StatID] = self       


    def get_total_bamboo_area(self, society_instance, scenario_name):
        
        bamboo_area = 0
        
        # Get the statistics
        for ParcelID in society_instance.land_dict:
            if society_instance.land_dict[ParcelID].LandCover == 'Bamboo':
                bamboo_area += society_instance.land_dict[ParcelID].Shape_Area / 666.7
        
        
        # Add the statistics
        self.ScenarioVersion = scenario_name
        self.StatDate = society_instance.current_year 
        self.Variable = 'V-06 Total Bamboo Forest Area'
        self.StatValue = bamboo_area
        self.StatUnit = 'Chinese Acres (1 CA = 0.067 Hectare)'
        self.StatID = self.Variable + '_' + str(self.StatDate)
                 
        self.StartingPointEffective = 1

        society_instance.stat_dict[self.StatID] = self  

    

    def get_total_shrubbery_area(self, society_instance, scenario_name):
        
        shrubbery_area = 0
        
        # Get the statistics
        for ParcelID in society_instance.land_dict:
            if society_instance.land_dict[ParcelID].LandCover == 'Shrubbery':
                shrubbery_area += society_instance.land_dict[ParcelID].Shape_Area / 666.7
        
        
        # Add the statistics
        self.ScenarioVersion = scenario_name
        self.StatDate = society_instance.current_year 
        self.Variable = 'V-07 Total Shrubbery Area'
        self.StatValue = shrubbery_area
        self.StatUnit = 'Chinese Acres (1 CA = 0.067 Hectare)'
        self.StatID = self.Variable + '_' + str(self.StatDate)
                 
        self.StartingPointEffective = 1

        society_instance.stat_dict[self.StatID] = self  



    def get_total_broadleaf_area(self, society_instance, scenario_name):
        
        broadleaf_area = 0
        
        # Get the statistics
        for ParcelID in society_instance.land_dict:
            if society_instance.land_dict[ParcelID].LandCover == 'Broad-leaved Forest':
                broadleaf_area += society_instance.land_dict[ParcelID].Shape_Area / 666.7
        
        
        # Add the statistics
        self.ScenarioVersion = scenario_name
        self.StatDate = society_instance.current_year 
        self.Variable = 'V-08 Total Broad-leaved Forest Area'
        self.StatValue = broadleaf_area
        self.StatUnit = 'Chinese Acres (1 CA = 0.067 Hectare)'
        self.StatID = self.Variable + '_' + str(self.StatDate)
                 
        self.StartingPointEffective = 1

        society_instance.stat_dict[self.StatID] = self  



    def get_total_mixed_forest_area(self, society_instance, scenario_name):
        
        mixed_forest_area = 0
        
        # Get the statistics
        for ParcelID in society_instance.land_dict:
            if society_instance.land_dict[ParcelID].LandCover == 'Mixed Forest':
                mixed_forest_area += society_instance.land_dict[ParcelID].Shape_Area / 666.7
        
        
        # Add the statistics
        self.ScenarioVersion = scenario_name
        self.StatDate = society_instance.current_year 
        self.Variable = 'V-09 Total Mixed Forest Area'
        self.StatValue = mixed_forest_area
        self.StatUnit = 'Chinese Acres (1 CA = 0.067 Hectare)'
        self.StatID = self.Variable + '_' + str(self.StatDate)
                 
        self.StartingPointEffective = 1

        society_instance.stat_dict[self.StatID] = self  



    def get_total_coniferous_area(self, society_instance, scenario_name):
        
        coniferous_area = 0
        
        # Get the statistics
        for ParcelID in society_instance.land_dict:
            if society_instance.land_dict[ParcelID].LandCover == 'Coniferous Forest':
                coniferous_area += society_instance.land_dict[ParcelID].Shape_Area / 666.7
        
        
        # Add the statistics
        self.ScenarioVersion = scenario_name
        self.StatDate = society_instance.current_year 
        self.Variable = 'V-10 Total Coniferous Forest Area'
        self.StatValue = coniferous_area
        self.StatUnit = 'Chinese Acres (1 CA = 0.067 Hectare)'
        self.StatID = self.Variable + '_' + str(self.StatDate)
                 
        self.StartingPointEffective = 1

        society_instance.stat_dict[self.StatID] = self  
        
    
    '''
    Energy
    '''
    def get_total_energy_demand(self, society_instance, scenario_name):
        
        total_energy_demand = 0
        
        # Get the statistics
        for HID in society_instance.hh_dict:
            if society_instance.hh_dict[HID].is_exist == 1:
                total_energy_demand += society_instance.hh_dict[HID].energy.energy_demand
        
        
        # Add the statistics
        self.ScenarioVersion = scenario_name
        self.StatDate = society_instance.current_year 
        self.Variable = 'VI-01 Total Energy Demand'
        self.StatValue = total_energy_demand
        self.StatUnit = 'kWh'
        self.StatID = self.Variable + '_' + str(self.StatDate)
                 
        self.StartingPointEffective = 1

        society_instance.stat_dict[self.StatID] = self  
    
    

    def get_total_electricity_consumption(self, society_instance, scenario_name):
        
        total_electricity_consumption = 0
        
        # Get the statistics
        for HID in society_instance.hh_dict:
            if society_instance.hh_dict[HID].is_exist == 1:
                total_electricity_consumption += society_instance.hh_dict[HID].energy.electricity_consumption
        
        
        # Add the statistics
        self.ScenarioVersion = scenario_name
        self.StatDate = society_instance.current_year 
        self.Variable = 'VI-02 Total Electricity Consumption'
        self.StatValue = total_electricity_consumption
        self.StatUnit = 'kWh'
        self.StatID = self.Variable + '_' + str(self.StatDate)
                 
        self.StartingPointEffective = 1

        society_instance.stat_dict[self.StatID] = self      
    


    def get_total_firewood_consumption(self, society_instance, scenario_name):
        
        total_firewood_consumption = 0
        
        # Get the statistics
        for HID in society_instance.hh_dict:
            if society_instance.hh_dict[HID].is_exist == 1:
                total_firewood_consumption += society_instance.hh_dict[HID].energy.firewood_consumption
        
        
        # Add the statistics
        self.ScenarioVersion = scenario_name
        self.StatDate = society_instance.current_year 
        self.Variable = 'VI-03 Total Firewood Consumption'
        self.StatValue = total_firewood_consumption
        self.StatUnit = 'kg'
        self.StatID = self.Variable + '_' + str(self.StatDate)
                 
        self.StartingPointEffective = 1

        society_instance.stat_dict[self.StatID] = self 
    

    def get_total_firewood_consumption_in_kwh(self, society_instance, scenario_name):
        
        total_firewood_consumption_in_kwh = 0
        
        # Get the statistics
        for HID in society_instance.hh_dict:
            if society_instance.hh_dict[HID].is_exist == 1:
                total_firewood_consumption_in_kwh += society_instance.hh_dict[HID].energy.firewood_consumption_in_kwh
        
        
        # Add the statistics
        self.ScenarioVersion = scenario_name
        self.StatDate = society_instance.current_year 
        self.Variable = 'VI-04 Total Firewood Consumption in kWh'
        self.StatValue = total_firewood_consumption_in_kwh
        self.StatUnit = 'kWh'
        self.StatID = self.Variable + '_' + str(self.StatDate)
                 
        self.StartingPointEffective = 1

        society_instance.stat_dict[self.StatID] = self     
    


    def get_total_carbon_footprint(self, society_instance, scenario_name):
        
        total_carbon_footprint = 0
        
        # Get the statistics
        for HID in society_instance.hh_dict:
            if society_instance.hh_dict[HID].is_exist == 1:
                total_carbon_footprint += society_instance.hh_dict[HID].energy.carbon_footprint
        
        
        # Add the statistics
        self.ScenarioVersion = scenario_name
        self.StatDate = society_instance.current_year 
        self.Variable = 'VI-05 Total Carbon Footprint'
        self.StatValue = total_carbon_footprint
        self.StatUnit = 'kg'
        self.StatID = self.Variable + '_' + str(self.StatDate)
                 
        self.StartingPointEffective = 1

        society_instance.stat_dict[self.StatID] = self 
    

    '''
    Others
    '''
    def get_ownerless_land_area(self, society_instance, scenario_name):
        
        ownerless_land_area = 0
        
        # Get the statistics
        for land_parcel in society_instance.ownerless_land:
            ownerless_land_area += land_parcel.Shape_Area / 666.7
        
        
        # Add the statistics
        self.ScenarioVersion = scenario_name
        self.StatDate = society_instance.current_year 
        self.Variable = 'VII-01 Owenrless Land Area'
        self.StatValue = ownerless_land_area
        self.StatUnit = 'Chinese Acres (1 CA = 0.067 Hectare)'
        self.StatID = self.Variable + '_' + str(self.StatDate)
                 
        self.StartingPointEffective = 1

        society_instance.stat_dict[self.StatID] = self  


    def get_uninherited_money(self, society_instance, scenario_name):
        
        uninherited_money = 0
        
        # Get the statistics
        uninherited_money = society_instance.ownerless_money
        
        
        # Add the statistics
        self.ScenarioVersion = scenario_name
        self.StatDate = society_instance.current_year 
        self.Variable = 'VII-02 Uninherited Money'
        self.StatValue = uninherited_money
        self.StatUnit = 'Yuan'
        self.StatID = self.Variable + '_' + str(self.StatDate)
                 
        self.StartingPointEffective = 1

        society_instance.stat_dict[self.StatID] = self  
















    '''
    Composite Indicators
    '''

    def get_education_structure(self, society_instance, scenario_name):
        
        self.ScenarioVersion = scenario_name
        self.StatDate = society_instance.current_year
        self.Variable = '1 Population by Education Levels'
        self.StatValue = 0
        self.StatUnit = 'Yuan (RMB)'
        self.StatID = self.Variable + '_' + str(self.StatDate)
        
        self.CompositeIndicator = 1 # Make it a composite indicator

        self.StartingPointEffective = 0

        society_instance.stat_dict[self.StatID] = self 

    
    def get_sectors_income_structure(self, society_instance, scenario_name):
        
        self.ScenarioVersion = scenario_name
        self.StatDate = society_instance.current_year
        self.Variable = '2 Total Income by Sectors'
        self.StatValue = 0
        self.StatUnit = 'Yuan (RMB)'
        self.StatID = self.Variable + '_' + str(self.StatDate)
        
        self.CompositeIndicator = 1 # Make it a composite indicator

        self.StartingPointEffective = 0

        society_instance.stat_dict[self.StatID] = self 
        
        
    def get_sectors_employment_structure(self, society_instance, scenario_name):
        
        self.ScenarioVersion = scenario_name
        self.StatDate = society_instance.current_year
        self.Variable = '3 Employment by Sectors'
        self.StatValue = 0
        self.StatUnit = ''
        self.StatID = self.Variable + '_' + str(self.StatDate)
        
        self.CompositeIndicator = 1 # Make it a composite indicator

        self.StartingPointEffective = 0

        society_instance.stat_dict[self.StatID] = self         
        
        
    def get_household_preference_type_structures(self, society_instance, scenario_name):
        
        self.ScenarioVersion = scenario_name
        self.StatDate = society_instance.current_year
        self.Variable = '4 Household Preference Types'
        self.StatValue = 0
        self.StatUnit = ''
        self.StatID = self.Variable + '_' + str(self.StatDate)
        
        self.CompositeIndicator = 1 # Make it a composite indicator

        self.StartingPointEffective = 0

        society_instance.stat_dict[self.StatID] = self         
 


    def get_household_business_type_structures(self, society_instance, scenario_name):
        
        self.ScenarioVersion = scenario_name
        self.StatDate = society_instance.current_year
        self.Variable = '5 Household Business Types'
        self.StatValue = 0
        self.StatUnit = ''
        self.StatID = self.Variable + '_' + str(self.StatDate)
        
        self.CompositeIndicator = 1 # Make it a composite indicator

        self.StartingPointEffective = 0

        society_instance.stat_dict[self.StatID] = self  
        
        
   
    def get_landuse_landcover_structures(self, society_instance, scenario_name):
        
        self.ScenarioVersion = scenario_name
        self.StatDate = society_instance.current_year
        self.Variable = '6 Land-use/Land Cover Structure'
        self.StatValue = 0
        self.StatUnit = ''
        self.StatID = self.Variable + '_' + str(self.StatDate)
        
        self.CompositeIndicator = 1 # Make it a composite indicator

        self.StartingPointEffective = 1

        society_instance.stat_dict[self.StatID] = self       
        
        

    def get_energy_consumption_structures(self, society_instance, scenario_name):
        
        self.ScenarioVersion = scenario_name
        self.StatDate = society_instance.current_year
        self.Variable = '7 Energy Consumption Structure'
        self.StatValue = 0
        self.StatUnit = ''
        self.StatID = self.Variable + '_' + str(self.StatDate)
        
        self.CompositeIndicator = 1 # Make it a composite indicator

        self.StartingPointEffective = 1

        society_instance.stat_dict[self.StatID] = self       
        


    '''
    Map layers
    '''
    def get_lulc_map_layer(self, society_instance, scenario_name):

        self.ScenarioVersion = scenario_name
        self.StatDate = society_instance.current_year
        self.Variable = 'Land-use/land cover'
        self.StatValue = 0
        self.StatUnit = ''
        self.StatID = self.Variable + '_' + str(self.StatDate)
        
        self.MapLayer = 1 # Make it a map layer

        self.StartingPointEffective = 1

        society_instance.stat_dict[self.StatID] = self
        
        
        
        
                        
           