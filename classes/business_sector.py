'''
Created on May 30, 2015

@author: Liyan Xu
'''

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

#         elif self.SectorName == 'TractorTrans':
#             if capital.av_male_labor > 0:
#                 if capital.av_tractor > 0:
#                     return True
#                 elif capital.cash > self.EntryThreshold:
#                     return True
#                 elif capital.cash > self.EntryThreshold * self.own_cash_percent and capital.debt <= 0 and risk_type == False:
#                     return True
  
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
                
#         elif self.SectorName == 'Lending':
#             if capital.cash > self.EntryThreshold and capital.debt <= 0:
#                 return True
# 
#         elif self.SectorName == 'Renting':
#             if capital.av_rooms > 0:
#                 return True          


    def calculate_business_revenue(self, capital, risk_type, risk_effective):
        pass
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        


