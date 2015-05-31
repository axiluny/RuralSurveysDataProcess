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
        
        '''
        
        # Set the attributes (var) and their values (record) from the land table in the DB.                
        for var in VarList:
            setattr(self, var[0], record[var[1]])

        # Set the current time stamp
        self.StatDate = current_year
        
        # Define the variables related to vegetation succession.
        self.succession_start_year = int()
        self.succession_length = int() # The time length of vegetation succession.
    
    
    def land_cover_succession(self, current_year):
        
        # Determine the length of vegetation succession
        self.succession_length = current_year - self.succession_start_year
        
        if self.LandCover == 'Cultivate':
            pass
        elif self.LandCover == 'Construction':
            pass
        elif self.LandCover == 'Grass':
            pass
        elif self.LandCover == 'Shrubbery':
            pass
        
        
        
        
        
        
        
        
        
        
        