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
    
        
    # Get the variables list for a table by a given name in the database
    def get_var_list(self, table_name):

        var_list = list()
        for row in self.cursor.columns(table=table_name):
            var_list.append((row.column_name, row.ordinal_position-1, row.type_name))        
    
        return var_list
    
    # Get a table by a given name in the database; create a pointer to that table
    def get_table (self, table_name):
    
        table_cursor = self.cursor.execute('SELECT * FROM ' + table_name)
        table = table_cursor.fetchall()        
        
        return table

#     # Make a dictionary for a table by a given name and variables list
#     def make_dict(self, table, var_list):    
# 
#         dict_ins = dict()
#         for record in table:
#             temp = Household(record, var_list)     # For household objects only for now... 20150401
#             # Insert the household into the household dictionary indexed by HID
#             dict_ins[temp.HID] = temp
#     
#         return dict_ins


    def add_stat_results(self):
        pass
    
     

    def save_results_to_db(self):
        pass


#     # Write the household table to the Database
#     scenario_id = '1'
#     year = '2015'
# 
#     '''
#         CAUTION: The following part should be capsuled
#     '''
#     new_household_table_name = 'Household_' + year + '_' + scenario_id
#      
#     # Create a new Household table from the variable list
#     new_household_table_formatter = '('
#     for var in household_var_list:
#         # Add household variables to the formatter
#         new_household_table_formatter += var[0] + ' ' + var[2] + ','  
#     new_household_table_formatter = new_household_table_formatter[0: len(new_household_table_formatter) - 1] + ')'
#      
#     # Create the new household table
#     db.cursor.execute("create table " + new_household_table_name +''+ new_household_table_formatter)
#     db.connector.commit()
#     
#     
#     
#     # Insert all households into the new table
#     #InsertContent = ''
#     for HID in household_dict:
#         # Make the insert values for this household
#         new_household_record_content = '('
#         for var in household_var_list:
#             # If the value is string, add qoutes
#             if var[2] == 'VARCHAR' and getattr(household_dict[HID], var[0]) != None: 
#                 new_household_record_content += '\''+ unicode(getattr(household_dict[HID], var[0]))+ '\','
#             else:
#                 new_household_record_content += unicode(getattr(household_dict[HID], var[0]))+ ','
#         # Change the ending comma to a closing parenthesis
#         new_household_record_content = new_household_record_content[0:len(new_household_record_content)-1] + ')'
#         # Insert one household record
#         db.cursor.execute("insert into " + new_household_table_name + ' values ' + new_household_record_content.replace('None','Null') +';')
#     db.connector.commit()
#      
#      
#     print household_dict['g1c1z001'].Hname
#     