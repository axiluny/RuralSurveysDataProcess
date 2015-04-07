'''
Created on Mar 25, 2015

@author: Hongmou
'''
from person import Person
from data_access import DataAccess

class Household(object):
    '''
    This is the definition of the household class
    '''
    
    
    def __init__(self, record, VarList, db, pp_table_name, pp_table):
        '''
        Constructor of Household
        VarList = {paramName1: paramOrder1, paramName2: paramOrder2, ...}
        '''       
        
        for var in VarList:
            setattr(self, var[0], record[var[1]])


        self.pp_var_list = DataAccess.get_var_list(db, pp_table_name)
        
        # Define person list in the household
        self.pp_list = []
        
        # Add respective persons into the person list of the household
        for pp in pp_table:
            if pp.HID == self.HID:
                pp_temp = Person(pp, self.pp_var_list)
                
                self.pp_list.append(pp_temp)
            
    
    
    def step_go(self, start_year, end_year):
        
        # Update current year record
        if self.StatDate == None:
            self.StatDate = start_year
                    
        else:
            self.StatDate += 1
        
        
        for pp in self.pp_list:
            Person.step_go(pp, start_year, end_year)
    