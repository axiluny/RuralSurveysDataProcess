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
    
    
        
        
        
    '''
    Single Variables
    '''
    
    '''
    Basic Demographics
    '''
    
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
        self.Variable = 'Population'
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
        self.Variable = 'Existing Household'
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
        self.Variable = 'Dissolved Household'
        self.StatValue = dhh_ct
        self.StatID = self.Variable + '_' + str(self.StatDate)
                 
        soc.stat_dict[self.StatID] = self    
    
    
    '''
    Basic Economic Statistics
    '''
    
    def get_total_net_savings(self, soc, scenario_name):
        
        total_net_savings = 0
        
        # Get the statistics
        for HID in soc.hh_dict:
            if soc.hh_dict[HID].is_exist == 1:
                
                total_net_savings += soc.hh_dict[HID].own_capital_properties.netsavings
                
         
        # Add the statistics
        self.ScenarioVersion = scenario_name
        self.StatDate = soc.current_year 
        self.Variable = 'Total Net Savings'
        self.StatValue = total_net_savings
        self.StatID = self.Variable + '_' + str(self.StatDate)
                 
        soc.stat_dict[self.StatID] = self 
            
    
    def get_total_cash_savings(self, soc, scenario_name):
        
        total_cash_savings = 0
        
        # Get the statistics
        for HID in soc.hh_dict:
            if soc.hh_dict[HID].is_exist == 1:
                
                total_cash_savings += soc.hh_dict[HID].own_capital_properties.cash
                
         
        # Add the statistics
        self.ScenarioVersion = scenario_name
        self.StatDate = soc.current_year 
        self.Variable = 'Total Cash Savings'
        self.StatValue = total_cash_savings
        self.StatID = self.Variable + '_' + str(self.StatDate)
                 
        soc.stat_dict[self.StatID] = self      
    
    
    def get_total_debt(self, soc, scenario_name):
        
        total_debt = 0
        
        # Get the statistics
        for HID in soc.hh_dict:
            if soc.hh_dict[HID].is_exist == 1:
                
                total_debt += soc.hh_dict[HID].own_capital_properties.debt
                
         
        # Add the statistics
        self.ScenarioVersion = scenario_name
        self.StatDate = soc.current_year 
        self.Variable = 'Total Debt'
        self.StatValue = total_debt
        self.StatID = self.Variable + '_' + str(self.StatDate)
                 
        soc.stat_dict[self.StatID] = self


    def get_gross_annual_income(self, soc, scenario_name):
        
        gross_annual_income = 0
        
        # Get the statistics
        for HID in soc.hh_dict:
            if soc.hh_dict[HID].is_exist == 1:
                
                gross_annual_income += soc.hh_dict[HID].AnnualTotalIncome
                
         
        # Add the statistics
        self.ScenarioVersion = scenario_name
        self.StatDate = soc.current_year 
        self.Variable = 'Gross Annual Income'
        self.StatValue = gross_annual_income
        self.StatID = self.Variable + '_' + str(self.StatDate)
                 
        soc.stat_dict[self.StatID] = self        


    def get_gross_business_revenues(self, soc, scenario_name):
        gross_business_revenues = 0
        
        # Get the statistics
        for HID in soc.hh_dict:
            if soc.hh_dict[HID].is_exist == 1:
                
                gross_business_revenues += soc.hh_dict[HID].own_capital_properties.total_business_income
                
         
        # Add the statistics
        self.ScenarioVersion = scenario_name
        self.StatDate = soc.current_year 
        self.Variable = 'Gross Business Revenues'
        self.StatValue = gross_business_revenues
        self.StatID = self.Variable + '_' + str(self.StatDate)
                 
        soc.stat_dict[self.StatID] = self       
    
    
    def get_gross_compensational_revenues(self, soc, scenario_name):
        gross_compensational_revenues = 0
        
        # Get the statistics
        for HID in soc.hh_dict:
            if soc.hh_dict[HID].is_exist == 1:
                
                gross_compensational_revenues += soc.hh_dict[HID].AnnualCompensation
                
         
        # Add the statistics
        self.ScenarioVersion = scenario_name
        self.StatDate = soc.current_year 
        self.Variable = 'Gross Compensational Revenues'
        self.StatValue = gross_compensational_revenues
        self.StatID = self.Variable + '_' + str(self.StatDate)
                 
        soc.stat_dict[self.StatID] = self
                

    def get_annual_income_per_person(self, soc, scenario_name):
        
        gross_annual_income = 0
        pp_ct = 0
        
        # Get the statistics
        for HID in soc.hh_dict:
            if soc.hh_dict[HID].is_exist == 1:
                
                gross_annual_income += soc.hh_dict[HID].AnnualTotalIncome

                for PID in soc.hh_dict[HID].own_pp_dict:
                    if soc.hh_dict[HID].own_pp_dict[PID].is_alive == 1:
                        pp_ct += 1
         
        # Add the statistics
        self.ScenarioVersion = scenario_name
        self.StatDate = soc.current_year 
        self.Variable = 'Annual Income per Person'
        self.StatValue = gross_annual_income / pp_ct
        self.StatID = self.Variable + '_' + str(self.StatDate)
                 
        soc.stat_dict[self.StatID] = self  


    def get_annual_income_per_household(self, soc, scenario_name):
        
        gross_annual_income = 0
        hh_ct = 0
        
        # Get the statistics
        for HID in soc.hh_dict:
            if soc.hh_dict[HID].is_exist == 1:
                
                gross_annual_income += soc.hh_dict[HID].AnnualTotalIncome
                hh_ct += 1
         
        # Add the statistics
        self.ScenarioVersion = scenario_name
        self.StatDate = soc.current_year 
        self.Variable = 'Annual Income per Household'
        self.StatValue = gross_annual_income / hh_ct
        self.StatID = self.Variable + '_' + str(self.StatDate)
                 
        soc.stat_dict[self.StatID] = self  


    def get_trucks_count(self, soc, scenario_name):
        trucks_count = 0
        
        # Get the statistics
        for HID in soc.hh_dict:
            if soc.hh_dict[HID].is_exist == 1:
                
                trucks_count += soc.hh_dict[HID].own_capital_properties.truck
                
         
        # Add the statistics
        self.ScenarioVersion = scenario_name
        self.StatDate = soc.current_year 
        self.Variable = 'Trucks Count'
        self.StatValue = trucks_count
        self.StatID = self.Variable + '_' + str(self.StatDate)
                 
        soc.stat_dict[self.StatID] = self      


    def get_minibuses_count(self, soc, scenario_name):
        minibuses_count = 0
        
        # Get the statistics
        for HID in soc.hh_dict:
            if soc.hh_dict[HID].is_exist == 1:
                
                minibuses_count += soc.hh_dict[HID].own_capital_properties.minibus
                
         
        # Add the statistics
        self.ScenarioVersion = scenario_name
        self.StatDate = soc.current_year 
        self.Variable = 'Minibuses Count'
        self.StatValue = minibuses_count
        self.StatID = self.Variable + '_' + str(self.StatDate)
                 
        soc.stat_dict[self.StatID] = self     

    '''
    Income and employment by sectors
    '''

    def get_total_agriculture_income(self, soc, scenario_name):
        
        total_agriculture_income = 0
        
        # Get the statistics
        for HID in soc.hh_dict:
            if soc.hh_dict[HID].is_exist == 1:
                
                total_agriculture_income += soc.hh_dict[HID].own_capital_properties.agriculture_income
                
         
        # Add the statistics
        self.ScenarioVersion = scenario_name
        self.StatDate = soc.current_year 
        self.Variable = 'Agriculture Income'
        self.StatValue = total_agriculture_income
        self.StatID = self.Variable + '_' + str(self.StatDate)
                 
        soc.stat_dict[self.StatID] = self   


    def get_total_tempjob_income(self, soc, scenario_name):
        
        total_tempjob_income = 0
        
        # Get the statistics
        for HID in soc.hh_dict:
            if soc.hh_dict[HID].is_exist == 1:
                
                total_tempjob_income += soc.hh_dict[HID].own_capital_properties.temp_job_income
                
         
        # Add the statistics
        self.ScenarioVersion = scenario_name
        self.StatDate = soc.current_year 
        self.Variable = 'Temp Job Income'
        self.StatValue = total_tempjob_income
        self.StatID = self.Variable + '_' + str(self.StatDate)
                 
        soc.stat_dict[self.StatID] = self   


    def get_total_freighttrans_income(self, soc, scenario_name):
        
        total_freighttrans_income = 0
        
        # Get the statistics
        for HID in soc.hh_dict:
            if soc.hh_dict[HID].is_exist == 1:
                
                total_freighttrans_income += soc.hh_dict[HID].own_capital_properties.freight_trans_income
                
         
        # Add the statistics
        self.ScenarioVersion = scenario_name
        self.StatDate = soc.current_year 
        self.Variable = 'Freight Trans Income'
        self.StatValue = total_freighttrans_income
        self.StatID = self.Variable + '_' + str(self.StatDate)
                 
        soc.stat_dict[self.StatID] = self   


    def get_total_passengertrans_income(self, soc, scenario_name):
        
        total_passengertrans_income = 0
        
        # Get the statistics
        for HID in soc.hh_dict:
            if soc.hh_dict[HID].is_exist == 1:
                
                total_passengertrans_income += soc.hh_dict[HID].own_capital_properties.passenger_trans_income
                
         
        # Add the statistics
        self.ScenarioVersion = scenario_name
        self.StatDate = soc.current_year 
        self.Variable = 'Passenger Trans Income'
        self.StatValue = total_passengertrans_income
        self.StatID = self.Variable + '_' + str(self.StatDate)
                 
        soc.stat_dict[self.StatID] = self  
            
        
        
    def get_total_lodging_income(self, soc, scenario_name):
        
        total_lodging_income = 0
        
        # Get the statistics
        for HID in soc.hh_dict:
            if soc.hh_dict[HID].is_exist == 1:
                
                total_lodging_income += soc.hh_dict[HID].own_capital_properties.lodging_income
                
         
        # Add the statistics
        self.ScenarioVersion = scenario_name
        self.StatDate = soc.current_year 
        self.Variable = 'Lodging Income'
        self.StatValue = total_lodging_income
        self.StatID = self.Variable + '_' + str(self.StatDate)
                 
        soc.stat_dict[self.StatID] = self          
        
        
        
     
        
        
        
    def get_total_renting_income(self, soc, scenario_name):
        
        total_renting_income = 0
        
        # Get the statistics
        for HID in soc.hh_dict:
            if soc.hh_dict[HID].is_exist == 1:
                
                total_renting_income += soc.hh_dict[HID].own_capital_properties.renting_income
                
         
        # Add the statistics
        self.ScenarioVersion = scenario_name
        self.StatDate = soc.current_year 
        self.Variable = 'Renting Income'
        self.StatValue = total_renting_income
        self.StatID = self.Variable + '_' + str(self.StatDate)
                 
        soc.stat_dict[self.StatID] = self          


    def get_agriculture_employment_ratio(self, soc, scenario_name):
        
        agriculture_employment = 0
        hh_ct = 0
        
        # Get the statistics
        for HID in soc.hh_dict:
            if soc.hh_dict[HID].is_exist == 1:
                
                hh_ct += 1
                
                for sector in soc.hh_dict[HID].own_current_sectors:
                    if sector.SectorName == 'Agriculture':
                        agriculture_employment += 1
                         
        # Add the statistics
        self.ScenarioVersion = scenario_name
        self.StatDate = soc.current_year 
        self.Variable = 'Agriculture Employment Ratio'
        self.StatValue = float(agriculture_employment) / float(hh_ct)
        self.StatID = self.Variable + '_' + str(self.StatDate)
                 
        soc.stat_dict[self.StatID] = self


    def get_tempjob_employment_ratio(self, soc, scenario_name):
        
        tempjob_employment = 0
        hh_ct = 0
        
        # Get the statistics
        for HID in soc.hh_dict:
            if soc.hh_dict[HID].is_exist == 1:
                
                hh_ct += 1
                
                for sector in soc.hh_dict[HID].own_current_sectors:
                    if sector.SectorName == 'TempJob':
                        tempjob_employment += 1
                         
        # Add the statistics
        self.ScenarioVersion = scenario_name
        self.StatDate = soc.current_year 
        self.Variable = 'Temp Jobs Employment Ratio'
        self.StatValue = float(tempjob_employment) / float(hh_ct)
        self.StatID = self.Variable + '_' + str(self.StatDate)
                 
        soc.stat_dict[self.StatID] = self


    def get_freighttrans_employment_ratio(self, soc, scenario_name):
        
        freighttrans_employment = 0
        hh_ct = 0
        
        # Get the statistics
        for HID in soc.hh_dict:
            if soc.hh_dict[HID].is_exist == 1:
                
                hh_ct += 1
                
                for sector in soc.hh_dict[HID].own_current_sectors:
                    if sector.SectorName == 'FreightTrans':
                        freighttrans_employment += 1
                         
        # Add the statistics
        self.ScenarioVersion = scenario_name
        self.StatDate = soc.current_year 
        self.Variable = 'Freight Trans Employment Ratio'
        self.StatValue = float(freighttrans_employment) / float(hh_ct)
        self.StatID = self.Variable + '_' + str(self.StatDate)
                 
        soc.stat_dict[self.StatID] = self


    def get_passengertrans_employment_ratio(self, soc, scenario_name):
        
        passengertrans_employment = 0
        hh_ct = 0
        
        # Get the statistics
        for HID in soc.hh_dict:
            if soc.hh_dict[HID].is_exist == 1:
                
                hh_ct += 1
                
                for sector in soc.hh_dict[HID].own_current_sectors:
                    if sector.SectorName == 'PassengerTrans':
                        passengertrans_employment += 1
                         
        # Add the statistics
        self.ScenarioVersion = scenario_name
        self.StatDate = soc.current_year 
        self.Variable = 'Passenger Trans Employment Ratio'
        self.StatValue = float(passengertrans_employment) / float(hh_ct)
        self.StatID = self.Variable + '_' + str(self.StatDate)
                 
        soc.stat_dict[self.StatID] = self        


    def get_lodging_employment_ratio(self, soc, scenario_name):
        
        lodging_employment = 0
        hh_ct = 0
        
        # Get the statistics
        for HID in soc.hh_dict:
            if soc.hh_dict[HID].is_exist == 1:
                
                hh_ct += 1
                
                for sector in soc.hh_dict[HID].own_current_sectors:
                    if sector.SectorName == 'Lodging':
                        lodging_employment += 1
                         
        # Add the statistics
        self.ScenarioVersion = scenario_name
        self.StatDate = soc.current_year 
        self.Variable = 'Lodging Employment Ratio'
        self.StatValue = float(lodging_employment) / float(hh_ct)
        self.StatID = self.Variable + '_' + str(self.StatDate)
                 
        soc.stat_dict[self.StatID] = self


    def get_renting_employment_ratio(self, soc, scenario_name):
        
        renting_employment = 0
        hh_ct = 0
        
        # Get the statistics
        for HID in soc.hh_dict:
            if soc.hh_dict[HID].is_exist == 1:
                
                hh_ct += 1
                
                for sector in soc.hh_dict[HID].own_current_sectors:
                    if sector.SectorName == 'Renting':
                        renting_employment += 1
                         
        # Add the statistics
        self.ScenarioVersion = scenario_name
        self.StatDate = soc.current_year 
        self.Variable = 'Renting Employment Ratio'
        self.StatValue = float(renting_employment) / float(hh_ct)
        self.StatID = self.Variable + '_' + str(self.StatDate)
                 
        soc.stat_dict[self.StatID] = self


    '''
    Land variables
    '''
    
    def get_total_farmland_area(self, soc, scenario_name):
        
        farmland_area = 0
        
        # Get the statistics
        for HID in soc.hh_dict:
            if soc.hh_dict[HID].is_exist == 1:
                
                farmland_area += soc.hh_dict[HID].own_capital_properties.farmland
                         
        # Add the statistics
        self.ScenarioVersion = scenario_name
        self.StatDate = soc.current_year 
        self.Variable = 'Total Farmland Area'
        self.StatValue = farmland_area
        self.StatID = self.Variable + '_' + str(self.StatDate)
                 
        soc.stat_dict[self.StatID] = self


    def get_abandoned_farmland_area(self, soc, scenario_name):
        
        abandoned_farmland_area = 0
        
        # Get the statistics
        for HID in soc.hh_dict:
            if soc.hh_dict[HID].is_exist == 1:
                
                abandoned_farmland_area += soc.hh_dict[HID].own_capital_properties.av_farmland
                         
        # Add the statistics
        self.ScenarioVersion = scenario_name
        self.StatDate = soc.current_year 
        self.Variable = 'Total Abandoned Farmland Area'
        self.StatValue = abandoned_farmland_area
        self.StatID = self.Variable + '_' + str(self.StatDate)
                 
        soc.stat_dict[self.StatID] = self
    
    
    

    '''
    Composite Indicators
    '''
    
    def get_sectors_income_structure(self, soc, scenario_name):
        
        self.ScenarioVersion = scenario_name
        self.StatDate = soc.current_year
        self.Variable = 'Sectors Income Structure'
        self.StatValue = 0
        self.StatID = self.Variable + '_' + str(self.StatDate)
        
        self.CompositeIndicator = 1 # Make it a composite indicator

        soc.stat_dict[self.StatID] = self 
        
        
    def get_sectors_employment_structure(self, soc, scenario_name):
        
        self.ScenarioVersion = scenario_name
        self.StatDate = soc.current_year
        self.Variable = 'Sectors Employment Structure'
        self.StatValue = 0
        self.StatID = self.Variable + '_' + str(self.StatDate)
        
        self.CompositeIndicator = 1 # Make it a composite indicator

        soc.stat_dict[self.StatID] = self         
        
        
        
        
        
        
        
        
           