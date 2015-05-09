'''
Created on Mar 26, 2015

@author: Liyan Xu; Hongmou Zhang
'''
from data_access import DataAccess
from society import Society

# Define scenario name temporarily
scenario_name = ''


def step_go(database, society_instance, start_year, end_year, simulation_count):

    #Do statistics and add records to stat table in database
#     add_stat_results(society_instance)
    
    # Do the simulation
    Society.step_go(society_instance, start_year, end_year, simulation_count)
    
    # Then save updated tables in database
    save_results_to_db(database, society_instance)



def CreateScenario(db, model_table_name, model_table, hh_table_name, hh_table, pp_table_name, pp_table, simulation_depth, start_year, end_year):
    
    # Set up a scenario name
    set_up_scenario_name()
    
    # Initialize society: create society, household, person, etc instances
    soc = Society(db, model_table_name, model_table, hh_table_name, hh_table, pp_table_name, pp_table)
    
    #Start simulation
    for simulation_count in range(simulation_depth):
        step_go(db, soc, start_year, end_year, simulation_count)


    # Temporarily adding this - signaling the end of run.
    print 'Success!'


# Set up scenario name from UI inputs
# Should check for already existing names, otherwise later results will be added to the existing table, causing troubles
def set_up_scenario_name():
    name = 'test_scenario'
    return name

scenario_name = set_up_scenario_name()



def add_stat_results(society_instance):
    pass
    
    
def save_results_to_db(database, society_instance):
    
    # Determine household, people,and land table names
    # Format: Scenario_name + household/people/land
    new_hh_table_name = scenario_name + '_household'
    new_pp_table_name = scenario_name + '_persons'
    new_land_table_name = scenario_name + '_land'
    
        
    # Saving the Household table in the database
 
     
    # If the table with that name does not exist in the database
    # i.e. in the first round of iteration,
    # Then first create a new table, then insert the records.
    # Otherwise, just find the right table, and then insert the records.
    if DataAccess.get_table(database, new_hh_table_name) == None: 
     
        # Create a new Household table from the variable list of Household Class
        new_household_table_formatter = '('
        for var in society_instance.hh_var_list:
            # Add household variables to the formatter
            new_household_table_formatter += var[0] + ' ' + var[2] + ','  
        new_household_table_formatter = new_household_table_formatter[0: len(new_household_table_formatter) - 1] + ')'
     
        create_table_order = "create table " + new_hh_table_name +''+ new_household_table_formatter
        DataAccess.create_table(database, create_table_order)
        DataAccess.db_commit(database)
 
        # Then insert all households into the new table
        # InsertContent = ''
        for HID in society_instance.hh_dict:
            # Make the insert values for this household
            new_household_record_content = '('
            for var in society_instance.hh_var_list:
                # If the value is string, add quotes
                if var[2] == 'VARCHAR' and getattr(society_instance.hh_dict[HID], var[0]) != None: 
                    new_household_record_content += '\''+ unicode(getattr(society_instance.hh_dict[HID], var[0]))+ '\','
                else:
                    new_household_record_content += unicode(getattr(society_instance.hh_dict[HID], var[0]))+ ','
            # Change the ending comma to a closing parenthesis
            new_household_record_content = new_household_record_content[0:len(new_household_record_content)-1] + ')'
            # Insert one household record
            insert_table_order = "insert into " + new_hh_table_name + ' values ' + new_household_record_content.replace('None','Null') +';'
            DataAccess.insert_table(database, insert_table_order)
        DataAccess.db_commit(database)  
 
     
    else:
        # Just insert all households into the new table
        # InsertContent = ''
        for HID in society_instance.hh_dict:
            # Make the insert values for this household
            new_household_record_content = '('
            for var in society_instance.hh_var_list:
                # If the value is string, add quotes
                if var[2] == 'VARCHAR' and getattr(society_instance.hh_dict[HID], var[0]) != None: 
                    new_household_record_content += '\''+ unicode(getattr(society_instance.hh_dict[HID], var[0]))+ '\','
                else:
                    new_household_record_content += unicode(getattr(society_instance.hh_dict[HID], var[0]))+ ','
            # Change the ending comma to a closing parenthesis
            new_household_record_content = new_household_record_content[0:len(new_household_record_content)-1] + ')'
            # Insert one household record
            insert_table_order = "insert into " + new_hh_table_name + ' values ' + new_household_record_content.replace('None','Null') +';'
            DataAccess.insert_table(database, insert_table_order)
        DataAccess.db_commit(database)        



    # Saving the Person table in the database
 
     
    # If the table with that name does not exist in the database
    # i.e. in the first round of iteration,
    # Then first create a new table, then insert the records.
    # Otherwise, just find the right table, and then insert the records.
    if DataAccess.get_table(database, new_pp_table_name) == None: # This is most indecent... see dataaccess for details
     
        # Create a new Person table from the variable list of Person Class
        new_person_table_formatter = '('
        for var in society_instance.pp_var_list:
            # Add person variables to the formatter
            new_person_table_formatter += var[0] + ' ' + var[2] + ','  
        new_person_table_formatter = new_person_table_formatter[0: len(new_person_table_formatter) - 1] + ')'
     
        create_table_order = "create table " + new_pp_table_name +''+ new_person_table_formatter
        DataAccess.create_table(database, create_table_order)
        DataAccess.db_commit(database)
 
#         # Then insert all persons into the new table
#         # InsertContent = ''
#         for PID in society_instance.pp_dict:
#             # Make the insert values for this person
#             new_person_record_content = '('
#             for var in society_instance.pp_var_list:
#                 # If the value is string, add quotes
#                 if var[2] == 'VARCHAR' and getattr(society_instance.pp_dict[PID], var[0]) != None: 
#                     new_person_record_content += '\''+ unicode(getattr(society_instance.pp_dict[PID], var[0]))+ '\','
#                 else:
#                     new_person_record_content += unicode(getattr(society_instance.pp_dict[PID], var[0]))+ ','
#             # Change the ending comma to a closing parenthesis
#             new_person_record_content = new_person_record_content[0:len(new_person_record_content)-1] + ')'
#             # Insert one person record
#             insert_table_order = "insert into " + new_pp_table_name + ' values ' + new_person_record_content.replace('None','Null') +';'
#             DataAccess.insert_table(database, insert_table_order)
#         DataAccess.db_commit(database)  
#  
#      
#     else:
#         # Just insert all persons into the new table
#         # InsertContent = ''
#         for PID in society_instance.pp_dict:
#             # Make the insert values for this person
#             new_person_record_content = '('
#             for var in society_instance.pp_var_list:
#                 # If the value is string, add quotes
#                 if var[2] == 'VARCHAR' and getattr(society_instance.pp_dict[PID], var[0]) != None: 
#                     new_person_record_content += '\''+ unicode(getattr(society_instance.pp_dict[PID], var[0]))+ '\','
#                 else:
#                     new_person_record_content += unicode(getattr(society_instance.pp_dict[PID], var[0]))+ ','
#             # Change the ending comma to a closing parenthesis
#             new_person_record_content = new_person_record_content[0:len(new_person_record_content)-1] + ')'
#             # Insert one person record
#             insert_table_order = "insert into " + new_pp_table_name + ' values ' + new_person_record_content.replace('None','Null') +';'
#             DataAccess.insert_table(database, insert_table_order)
#         DataAccess.db_commit(database)  

        # Then insert all persons into the new table
        # InsertContent = ''
        for HID in society_instance.hh_dict:
            for PID in society_instance.hh_dict[HID].own_pp_dict:
                # Make the insert values for this person
                new_person_record_content = '('
                for var in society_instance.pp_var_list:
                    # If the value is string, add quotes
                    if var[2] == 'VARCHAR' and getattr(society_instance.hh_dict[HID].own_pp_dict[PID], var[0]) != None: 
                        new_person_record_content += '\''+ unicode(getattr(society_instance.hh_dict[HID].own_pp_dict[PID], var[0]))+ '\','
                    else:
                        new_person_record_content += unicode(getattr(society_instance.hh_dict[HID].own_pp_dict[PID], var[0]))+ ','
                # Change the ending comma to a closing parenthesis
                new_person_record_content = new_person_record_content[0:len(new_person_record_content)-1] + ')'
                # Insert one person record
                insert_table_order = "insert into " + new_pp_table_name + ' values ' + new_person_record_content.replace('None','Null') +';'
                DataAccess.insert_table(database, insert_table_order)
            DataAccess.db_commit(database)  
 
     
    else:
        # Just insert all persons into the new table
        # InsertContent = ''
        for HID in society_instance.hh_dict:
            for PID in society_instance.hh_dict[HID].own_pp_dict:
                # Make the insert values for this person
                new_person_record_content = '('
                for var in society_instance.pp_var_list:
                    # If the value is string, add quotes
                    if var[2] == 'VARCHAR' and getattr(society_instance.hh_dict[HID].own_pp_dict[PID], var[0]) != None: 
                        new_person_record_content += '\''+ unicode(getattr(society_instance.hh_dict[HID].own_pp_dict[PID], var[0]))+ '\','
                    else:
                        new_person_record_content += unicode(getattr(society_instance.hh_dict[HID].own_pp_dict[PID], var[0]))+ ','
                # Change the ending comma to a closing parenthesis
                new_person_record_content = new_person_record_content[0:len(new_person_record_content)-1] + ')'
                # Insert one person record
                insert_table_order = "insert into " + new_pp_table_name + ' values ' + new_person_record_content.replace('None','Null') +';'
                DataAccess.insert_table(database, insert_table_order)
            DataAccess.db_commit(database)  



  






