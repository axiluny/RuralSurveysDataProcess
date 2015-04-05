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
    
    #����һ����ͥ���ϣ����Դ�����м�ͥʵ�������湹�캯����Ϊ���ʼ����ֵ
    hh_list = list()


    def __init__(self, db, model_table_name, model_table, hh_table_name, hh_table):
        '''
        Constructor

        '''
        self.model_var_list = DataAccess.get_var_list(db, model_table_name)
        self.model_table = DataAccess.get_table(db, model_table_name)
        #������Ӧ�ö���͸�ֵ����Model variables
        
        self.hh_var_list = DataAccess.get_var_list(db, hh_table_name)
        self.hh_dict = DataAccess.make_dict(db, hh_table, self.hh_var_list)
        
        #�������hh_list�����ͥʵ��
        self.hh_list.append(object)
        
    def StepGo(self):
        pass
        


