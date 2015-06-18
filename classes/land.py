'''
Created on May 26, 2015

@author: Liyan Xu
'''

class Land(object):
    '''
    The land class
    '''


    def __init__(self, record, VarList, current_year):
        '''
        Construct the land class from the land table in the DB, and then add some other user-defined attributes.

        record - a record in the land table in the DB.       
        VarList - the variable (or field) list of the land table in the DB   
        VarList = {paramName1: paramOrder1, paramName2: paramOrder2, ...}   
        
        '''
        
        # Set the attributes (var) and their values (record) from the land table in the DB.                
        for var in VarList:
            setattr(self, var[0], record[var[1]])

        # Set the current time stamp
        self.StatDate = current_year
        
        # Define the variable indicating if the land is actually farmed
        self.actual_farming = False
        
        # Define the variables related to vegetation succession.
        self.succession_length = 0 # The time length of vegetation succession.
    
        # Define a switch indicating whether the land parcel, if it is farmland, is reverted to forest beginning this year
        self.IsG2G_this_year = False
        
    
    
    
    def land_cover_succession(self, current_year, model_parameters):
        '''
        The natural succession process of land cover.
        '''
        
        # Determine the length of vegetation succession
        if self.SStartyear != 0:
            self.succession_length = current_year - self.SStartyear
            
        
            if self.LandCover == 'Cultivate' and self.IsG2G == 1:
                if self.succession_length == int(model_parameters['CultivatedSuccessionYear']):
                    self.LandCover = 'Grass'
                    self.SStartyear = current_year
                       
            
            elif self.LandCover == 'Construction' and self.IsC2G == 1:
                if self.succession_length == int(model_parameters['ConstructionSuccessionYear']):
                    self.LandCover = 'Grass'
                    self.SStartyear = current_year        
            
            elif self.LandCover == 'Grass':
                if self.succession_length == int(model_parameters['GrassSuccessionYear']):
                    self.LandCover = 'Shrubbery'
                    self.SStartyear = current_year
                    
            
            elif self.LandCover == 'Shrubbery':
                if self.succession_length == int(model_parameters['ShrubberySuccessionYear']):
                    self.LandCover = 'Mixed'
                    self.SStartyear = current_year
        
        
        
        
        
        
        
        
        
        