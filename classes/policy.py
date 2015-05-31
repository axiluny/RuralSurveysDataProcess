'''
Created on May 30, 2015

@author: Liyan Xu
'''

class Policy(object):
    '''
    The Policy Class
    '''


    def __init__(self, record, VarList):
        '''
        
        '''
        
        # Set the attributes (var) and their values (record) from the policy programs table in the DB.                
        for var in VarList:
            setattr(self, var[0], record[var[1]])
        