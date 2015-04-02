'''
Created on Mar 25, 2015

@author: Hongmou
'''

class Household(object):
    '''
    This is the definition of household class
    '''
    

    def __init__(self, record, VarList):
        '''
        Constructor of Household
        VarList = {paramName1: paramOrder1, paramName2: paramOrder2, ...}
        '''
        for var in VarList:
            setattr(self, var[0], record[var[1]])