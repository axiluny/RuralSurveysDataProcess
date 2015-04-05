'''
Created on Mar 26, 2015

@author: xuliy_000
'''
from data_access import DataAccess
from household import Household

# import main


class Society(object):
    '''
    This is the definition of society class
    
    Creating household, person, etc. lists and dictionaries.
    '''
    
    #定义一个家庭集合，用以存放所有家庭实例；下面构造函数里为其初始化赋值
    hh_list = list()


    def __init__(self, db, model_table_name, model_table, hh_table_name, hh_table):
        '''
        Constructor

        '''
        self.model_var_list = DataAccess.get_var_list(db, model_table_name)
        self.model_table = DataAccess.get_table(db, model_table_name)
        #接下来应该定义和赋值所有Model variables
        
        self.hh_var_list = DataAccess.get_var_list(db, hh_table_name)
        self.hh_dict = DataAccess.make_dict(db, hh_table, self.hh_var_list)
        
        #在这里给hh_list加入家庭实例
        self.hh_list.append(object)
        
    def StepGo(self):
        pass
        


