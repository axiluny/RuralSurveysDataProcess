'''
Created on Mar 25, 2015

@author: Hongmou
'''
import pyodbc
# from household import Household


class DataAccess(object):
    '''
    Class for accessing data from the database
    '''
    
    def __init__(self, dbname, dbdriver):
        '''
        Constructor for DataAccess
        dbname: path+name of 
        '''
        self.connector = pyodbc.connect('DRIVER={};DBQ={}'.format(dbdriver, dbname))
        self.cursor = self.connector.cursor()



    # Get a table by a given name in the database; create a pointer to that table
    def get_table (self, table_name):
        
        try:
    
            table_cursor = self.cursor.execute('SELECT * FROM ' + table_name)
            table = table_cursor.fetchall()        
        
            return table
        
        except pyodbc.ProgrammingError: #This is ridiculously indecent... How to get a None value decently here?
            return None


        
    # Get the variables list for a table by a given name in the database
    def get_var_list(self, table_name):

        var_list = list()
        for row in self.cursor.columns(table=table_name):
            var_list.append((row.column_name, row.ordinal_position-1, row.type_name))        
    
        return var_list
    

    # Create a new table in the database by an order, which is a "create table from ..." sql order in string format
    def create_table(self, order):
        self.cursor.execute(order)
    
    # Insert a new record to a table in the database by an order, similar as "create_table"
    def insert_table(self, order):
        self.cursor.execute(order)
    
    # Commit an activity in the database
    def db_commit(self):
        self.connector.commit()        

    