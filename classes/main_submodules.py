'''
Created on Mar 26, 2015

@author: Liyan Xu
'''

from data_access import DataAccess
from society import Society
import stat_module

from PyQt4 import QtCore, QtGui
from PyQt4.Qt import QMessageBox, QColorDialog
from PyQt4.QtCore import Qt

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy

import os
from shutil import *

# Also need to import arcpy. But this takes a while. Better import it before actual using it, in export_map submodule.

'''
Globals, Constants, and other declarations.
'''
# GUI components location
greetings_image_location = 'C:\WolongRun\GUI Resources\Resources\The Urbanization Lab.png'
greetings_map_location = 'C:\WolongRun\GUI Resources\Resources\greetings_map_blank.png'
icons_path = 'C:\WolongRun\GUI Resources\SEEMS Icons'


# Global constants for database managements
db_file_name = 'WolongSEEMSDB.mdb'
input_dbpath = 'C:/WolongRun'
output_dbpath = 'C:/WolongRun/Results_Output'
input_db_location = str(input_dbpath + '\\' + db_file_name)
output_db_location = str(output_dbpath + '\\' + db_file_name)

dbdriver = '{Microsoft Access Driver (*.mdb)}'

model_table_name = 'ModelTable'
household_table_name = 'HouseholdTable'
person_table_name = 'PersonTable'
land_table_name = 'LandUseTable'
business_sector_table_name = 'BusinessSectorTable'
policy_table_name = 'PolicyTable'
stat_table_name = 'StatTable'
version_table_name = 'VersionTable'

# Get the input database (the output database is get later when initiating the GUI)
input_db = DataAccess(input_db_location, dbdriver)


# Arcpy workspace
arcpy_workspace = output_dbpath + '\\' + db_file_name
# Input ArcMap .mxd map name
input_mxd = 'SEEMS_Map.mxd'
# Input ArcMap .mxd map file path
input_mxd_path = r'C:\WolongRun\GIS Resources'
# Input Layer styles location
layer_styles_location = r'C:\WolongRun\GIS Resources\layer_styles\LandUse.lyr'
# External materials path
output_gis_path = "C:\WolongRun\Results_Output"


# Make a dictionary of composite statistics indicators
composite_indicators_dict = {'1 Population by Education Levels': ['I-04 Preschool', 'I-05 Primary School', 'I-06 Secondary School', 
                                'I-07 High School', 'I-08 College', 'I-09 Uneducated'],                             
                             '2 Total Income by Sectors': ['IV-01 Total Agriculture Income', 'IV-02 Total Temp Job Income', 
                                'IV-05 Total Lodging Income', 'IV-06 Total Renting Income'], 
                             '3 Employment by Sectors': ['IV-07 Agriculture Employment Ratio', 'IV-08 Temp Jobs Employment Ratio',
                                'IV-09 Freight Trans Employment Ratio', 'IV-10 Passenger Trans Employment Ratio',
                                'IV-11 Lodging Employment Ratio', 'IV-12 Renting Employment Ratio'], 
                             '4 Household Preference Types': ['II-01 Pref Labor_Risk Aversion HH Count', 'II-02 Pref Leisure_Risk Aversion HH Count',
                                'II-03 Pref Labor_Risk Appetite HH Count', 'II-04 Pref Leisure_Risk Appetite HH Count'],
                             '5 Household Business Types': ['II-05 Agriculture Only Households Count',
                                'II-06 Agriculture and One Other Business Households Count', 
                                'II-07 Agriculture and More than One Other Businesses Households Count'], 
                             '6 Land-use/Land Cover Structure': ['V-01 Total Farmland Area', 'V-04 Total Construction Land Area',
                                'V-05 Total Grassland Area', 'V-06 Total Bamboo Forest Area', 'V-07 Total Shrubbery Area', 
                                'V-08 Total Broad-leaved Forest Area', 'V-09 Total Mixed Forest Area',
                                'V-10 Total Coniferous Forest Area'],
                             '7 Energy Consumption Structure' : ['VI-02 Total Electricity Consumption', 'VI-04 Total Firewood Consumption in kWh']}




'''
The main submodules 
'''



def create_scenario(output_db, scenario_name, model_table_name, model_table, hh_table_name, hh_table, 
                    pp_table_name, pp_table, land_table_name, land_table, 
                    business_sector_table_name, business_sector_table, policy_table_name, policy_table, 
                    stat_table_name, stat_table, simulation_depth, start_year, 
                    pp_save_interval, hh_save_interval, land_save_interval,
                    gui):

    # Set up an initial value (1%) when clicked so that the user knows it's running.
    refresh_progress_bar(simulation_depth, gui)

    # Insert a record in the VersionTables in the output database files
    refresh_version_table(output_db, scenario_name, start_year, simulation_depth, pp_save_interval, hh_save_interval, land_save_interval)
     
    # Initialize the society class: create society, household, person, etc instances
    soc = Society(input_db, model_table_name, model_table, hh_table_name, hh_table, pp_table_name, pp_table, 
                  land_table_name, land_table, business_sector_table_name, business_sector_table, 
                  policy_table_name, policy_table, stat_table_name, stat_table, 
                  start_year)
      
    #Start simulation
    for iteration_count in range(simulation_depth):
        step_go(output_db, soc, start_year, iteration_count, scenario_name, pp_save_interval, hh_save_interval, land_save_interval, gui)
  
        # Set value for the progress bar
        refresh_progress_bar((iteration_count + 1) * 100, gui)







def step_go(output_db, society_instance, start_year, iteration_count, scenario_name, pp_save_interval, hh_save_interval, land_save_interval, gui):
    
    # If it's the first round of iteration, just get the stats and save the records to database
    # Else, proceed with the simulation in society.society_step_go, and then get the stats and save the records to database
    if iteration_count == 0:  
        # Do statistics and add records to the statistics dictionary in the society instance
        add_stat_results(society_instance, scenario_name)
        
        # Then save updated tables in the output database
        save_results_to_db(output_db, society_instance, scenario_name, iteration_count, pp_save_interval, hh_save_interval, land_save_interval)
        
        # Export maps
        if gui.ckb_save_landuse_status.isChecked() == True:
            export_maps(output_db, society_instance, scenario_name, iteration_count, pp_save_interval, hh_save_interval, land_save_interval, gui)
        
    # Do the simulation
    Society.society_step_go(society_instance, start_year, iteration_count)

    add_stat_results(society_instance, scenario_name)
    
    save_results_to_db(output_db, society_instance, scenario_name, iteration_count, pp_save_interval, hh_save_interval, land_save_interval)

    if gui.ckb_save_landuse_status.isChecked() == True:
        export_maps(output_db, society_instance, scenario_name, iteration_count, pp_save_interval, hh_save_interval, land_save_interval, gui)





def add_stat_results(society_instance, scenario_name):

    # Reset the statistics dictionary
    society_instance.stat_dict = dict()
    
    '''
    Single variables
    '''
    # Total population
    pp = stat_module.StatClass()
    stat_module.StatClass.get_population_count(pp, society_instance, scenario_name)

    # Household count
    hh = stat_module.StatClass()
    stat_module.StatClass.get_household_count(hh, society_instance, scenario_name)
     
    # Dissolved household count
    dhh = stat_module.StatClass()
    stat_module.StatClass.get_dissolved_household_count(dhh, society_instance, scenario_name)
    
    # Preschool students count
    prstu = stat_module.StatClass()
    stat_module.StatClass.get_preschool_stu(prstu,society_instance, scenario_name)

    # Primary school students count
    pristu = stat_module.StatClass()
    stat_module.StatClass.get_primaryschool_stu(pristu, society_instance, scenario_name)

    # Secondary school students count
    scstu = stat_module.StatClass()
    stat_module.StatClass.get_secondaryschool_stu(scstu, society_instance, scenario_name)

    # High school students count
    histu = stat_module.StatClass()
    stat_module.StatClass.get_highschool_stu(histu, society_instance, scenario_name)

    # College students count
    clstu = stat_module.StatClass()
    stat_module.StatClass.get_college_stu(clstu, society_instance, scenario_name)

    # Uneducated population count
    unedu = stat_module.StatClass()
    stat_module.StatClass.get_uneducated(unedu, society_instance, scenario_name)

    
    
    # Type 1 households count - Prefers labor/risk aversion
    ty1h = stat_module.StatClass()
    stat_module.StatClass.get_pref_labor_risk_aversion_hh_count(ty1h, society_instance, scenario_name)
    
    # Type 2 households count - Prefers leisure/risk aversion
    ty2h = stat_module.StatClass()
    stat_module.StatClass.get_pref_leisure_risk_aversion_hh_count(ty2h, society_instance, scenario_name)
    
    # Type 3 households count - Prefers labor/risk appetite
    ty3h = stat_module.StatClass()
    stat_module.StatClass.get_pref_labor_risk_appetite_hh_count(ty3h, society_instance, scenario_name)
    
    # Type 4 households count - Prefers leisure/risk appetite
    ty4h = stat_module.StatClass()
    stat_module.StatClass.get_pref_leisure_risk_appetite_hh_count(ty4h, society_instance, scenario_name)

    # Type 0 business household count - agriculture only
    ty0bh = stat_module.StatClass()
    stat_module.StatClass.get_housedhold_business_type_0_count(ty0bh, society_instance, scenario_name)

    # Type 1 business household count - agriculture and one other business
    ty1bh = stat_module.StatClass()
    stat_module.StatClass.get_housedhold_business_type_1_count(ty1bh, society_instance, scenario_name)

    # Type 2 business household count - agriculture and more than one other businesses
    ty2bh = stat_module.StatClass()
    stat_module.StatClass.get_housedhold_business_type_2_count(ty2bh, society_instance, scenario_name)

    
    # Total net savings
    tns = stat_module.StatClass()
    stat_module.StatClass.get_total_net_savings(tns, society_instance, scenario_name)
    
    # Total cash savings
    tc = stat_module.StatClass()
    stat_module.StatClass.get_total_cash_savings(tc, society_instance, scenario_name)
     
    # Total debt
    tb = stat_module.StatClass()
    stat_module.StatClass.get_total_debt(tb, society_instance, scenario_name)    
     
    # Gross annual income
    gai = stat_module.StatClass()
    stat_module.StatClass.get_gross_annual_income(gai, society_instance, scenario_name)
    
    # Gross business revenues
    gbr = stat_module.StatClass()
    stat_module.StatClass.get_gross_business_revenues(gbr, society_instance, scenario_name)
    
    # Gross Compensational Revenues
    gcr = stat_module.StatClass()
    stat_module.StatClass.get_gross_compensational_revenues(gcr, society_instance, scenario_name)
    
    # Annual income per person
    aipp = stat_module.StatClass()
    stat_module.StatClass.get_annual_income_per_person(aipp, society_instance, scenario_name)
    
    # Annual income per household
    aiph = stat_module.StatClass()
    stat_module.StatClass.get_annual_income_per_household(aiph, society_instance, scenario_name)
    
#     # Trucks count
#     trk = stat_module.StatClass()
#     stat_module.StatClass.get_trucks_count(trk, society_instance, scenario_name)
#     
#     # Minibuses count
#     mnb = stat_module.StatClass()
#     stat_module.StatClass.get_minibuses_count(mnb, society_instance, scenario_name)
    
    # Total agriculture income
    agi = stat_module.StatClass()
    stat_module.StatClass.get_total_agriculture_income(agi, society_instance, scenario_name)
     
    # Total temporary job income
    tji = stat_module.StatClass()
    stat_module.StatClass.get_total_tempjob_income(tji, society_instance, scenario_name)
     
    # Total freight transportation income
    fti = stat_module.StatClass()
    stat_module.StatClass.get_total_freighttrans_income(fti, society_instance, scenario_name)
     
    # Total passenger transportation income
    pti = stat_module.StatClass()
    stat_module.StatClass.get_total_passengertrans_income(pti, society_instance, scenario_name)
     
    # Total lodging income
    lgi = stat_module.StatClass()
    stat_module.StatClass.get_total_lodging_income(lgi, society_instance, scenario_name)
         
    # Total renting income
    rti = stat_module.StatClass()
    stat_module.StatClass.get_total_renting_income(rti, society_instance, scenario_name)    
    
    # Agriculture Employment Ratio
    ager = stat_module.StatClass()
    stat_module.StatClass.get_agriculture_employment_ratio(ager, society_instance, scenario_name)
    
    # Temporary Jobs Employment Ratio
    tjer = stat_module.StatClass()
    stat_module.StatClass.get_tempjob_employment_ratio(tjer, society_instance, scenario_name)
    
    # Freight transportation employment ratio
    fter = stat_module.StatClass()
    stat_module.StatClass.get_freighttrans_employment_ratio(fter, society_instance, scenario_name)
    
    # Passenger transportation employment ratio
    pter = stat_module.StatClass()
    stat_module.StatClass.get_passengertrans_employment_ratio(pter, society_instance, scenario_name)
    
    # Lodging employment ratio
    lger = stat_module.StatClass()
    stat_module.StatClass.get_lodging_employment_ratio(lger, society_instance, scenario_name)
    
    # Renting employment ratio
    rter = stat_module.StatClass()
    stat_module.StatClass.get_renting_employment_ratio(rter, society_instance, scenario_name)
    
    # Total farmland area
    tfa = stat_module.StatClass()
    stat_module.StatClass.get_total_farmland_area(tfa, society_instance, scenario_name)
    
    # Total abandoned farmland area
    tafa = stat_module.StatClass()
    stat_module.StatClass.get_abandoned_farmland_area(tafa, society_instance, scenario_name)
    
    # Total reverted farmland Area
    trfa = stat_module.StatClass()
    stat_module.StatClass.get_reverted_farmland_area(trfa, society_instance, scenario_name)
    
    # Total construction land area
    tcla = stat_module.StatClass()
    stat_module.StatClass.get_total_construction_land_area(tcla, society_instance, scenario_name)
    
    # Total grassland area
    tgla = stat_module.StatClass()
    stat_module.StatClass.get_total_grassland_area(tgla, society_instance, scenario_name)
    
    # Total bamboo area
    tbba = stat_module.StatClass()
    stat_module.StatClass.get_total_bamboo_area(tbba, society_instance, scenario_name)
    
    # Total shrubbery land area
    tsla = stat_module.StatClass()
    stat_module.StatClass.get_total_shrubbery_area(tsla, society_instance, scenario_name)

    # Total braodleaf forest area
    tblfa = stat_module.StatClass()
    stat_module.StatClass.get_total_broadleaf_area(tblfa, society_instance, scenario_name)
    
    # Total mixed forest area
    tmfa = stat_module.StatClass()
    stat_module.StatClass.get_total_mixed_forest_area(tmfa, society_instance, scenario_name)
    
    # Total coniferous forest area
    tcfa = stat_module.StatClass()
    stat_module.StatClass.get_total_coniferous_area(tcfa, society_instance, scenario_name)    
    
    # Total energy demand
    ted = stat_module.StatClass()
    stat_module.StatClass.get_total_energy_demand(ted, society_instance, scenario_name)
    
    # Total electricity consumption
    tec = stat_module.StatClass()
    stat_module.StatClass.get_total_electricity_consumption(tec, society_instance, scenario_name)
    
    # Total firewood consumption
    tfc = stat_module.StatClass()
    stat_module.StatClass.get_total_firewood_consumption(tfc, society_instance, scenario_name)

    # Total firewood consumption in kWh
    tfckwh = stat_module.StatClass()
    stat_module.StatClass.get_total_firewood_consumption_in_kwh(tfckwh, society_instance, scenario_name)
    
    # Total carbon footprint
    tcfp = stat_module.StatClass()
    stat_module.StatClass.get_total_carbon_footprint(tcfp, society_instance, scenario_name)
    
    
    # Ownerless land area
    owlla = stat_module.StatClass()
    stat_module.StatClass.get_ownerless_land_area(owlla, society_instance, scenario_name)
    
    # Uninherited money
    uihrt = stat_module.StatClass()
    stat_module.StatClass.get_uninherited_money(uihrt, society_instance, scenario_name)
    
    
    '''
    Composite indicators
    '''
    # Education structures
    edus = stat_module.StatClass()
    stat_module.StatClass.get_education_structure(edus, society_instance, scenario_name)    
    
    # Sectors income structure
    sis = stat_module.StatClass()
    stat_module.StatClass.get_sectors_income_structure(sis, society_instance, scenario_name)

    # Sectors employment structure
    ses = stat_module.StatClass()
    stat_module.StatClass.get_sectors_employment_structure(ses, society_instance, scenario_name)
    
    # Household preference type structure
    hpts = stat_module.StatClass()
    stat_module.StatClass.get_household_preference_type_structures(hpts, society_instance, scenario_name)

    # Household business type structure
    hbts = stat_module.StatClass()
    stat_module.StatClass.get_household_business_type_structures(hbts, society_instance, scenario_name)
    
    # Land-use/Land cover structure
    lulcs = stat_module.StatClass()
    stat_module.StatClass.get_landuse_landcover_structures(lulcs, society_instance, scenario_name)
    
    # Energy consumption structure
    ecs = stat_module.StatClass()
    stat_module.StatClass.get_energy_consumption_structures(ecs, society_instance, scenario_name)

   

    '''
    Map layers
    '''
    # landuse/land cover
    lulcmap = stat_module.StatClass()
    stat_module.StatClass.get_lulc_map_layer(lulcmap, society_instance, scenario_name)
    
    
    
    
def save_results_to_db(output_database, society_instance, scenario_name, iteration_count, pp_save_interval, hh_save_interval, land_save_interval):
    
    # Determine household, people,and land table names
    # Format: Scenario_name + household/people/land
    new_hh_table_name = scenario_name + '_households'
    new_pp_table_name = scenario_name + '_persons'
    new_land_table_name = scenario_name + '_land'

    
    
    '''    
    # Saving the Household table in the output_database
    '''
    # Check saving intervals first
    if iteration_count % int(hh_save_interval) == 0:
        # Only save results to the output_database at designated iterations
      
        # If the table with that name does not exist in the output_database
        # i.e. in the first round of iteration,
        # Then first create a new table, then insert the records.
        # Otherwise, just find the right table, and then insert the records.
#         if DataAccess.get_table(output_database, new_hh_table_name) == None: 
        if not output_database.cursor.tables(table=new_hh_table_name).fetchone():
            # Create a new Household table from the variable list of Household Class
            new_household_table_formatter = '('
            for var in society_instance.hh_var_list:
                # Add household variables to the formatter
                new_household_table_formatter += var[0] + ' ' + var[2] + ','  
            new_household_table_formatter = new_household_table_formatter[0: len(new_household_table_formatter) - 1] + ')'
         
            create_table_order = "create table " + new_hh_table_name +''+ new_household_table_formatter
            DataAccess.create_table(output_database, create_table_order)
            DataAccess.db_commit(output_database)
     
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
                DataAccess.insert_record_to_table(output_database, insert_table_order)
            DataAccess.db_commit(output_database)  
     
         
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
                DataAccess.insert_record_to_table(output_database, insert_table_order)
            DataAccess.db_commit(output_database)        


    '''
    # Saving the Person table in the output_database
    '''
    if iteration_count % int(pp_save_interval) == 0:

#         if DataAccess.get_table(output_database, new_pp_table_name) == None: # This is most indecent... see dataaccess for details
        if not output_database.cursor.tables(table=new_pp_table_name).fetchone():         
            # Create a new Person table from the variable list of Person Class
            new_person_table_formatter = '('
            for var in society_instance.pp_var_list:
                # Add person variables to the formatter
                new_person_table_formatter += var[0] + ' ' + var[2] + ','  
            new_person_table_formatter = new_person_table_formatter[0: len(new_person_table_formatter) - 1] + ')'
         
            create_table_order = "create table " + new_pp_table_name +''+ new_person_table_formatter
            DataAccess.create_table(output_database, create_table_order)
            DataAccess.db_commit(output_database)
    
    
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
                    DataAccess.insert_record_to_table(output_database, insert_table_order)
                DataAccess.db_commit(output_database)  
     
         
        else:
            
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
                    DataAccess.insert_record_to_table(output_database, insert_table_order)
                DataAccess.db_commit(output_database)  




    '''
    # Saving the Land table in the output_database
    '''
    if iteration_count % int(land_save_interval) == 0:
    
#         if DataAccess.get_table(output_database, new_land_table_name) == None: # This is most indecent... see dataaccess for details
        if not output_database.cursor.tables(table=new_land_table_name).fetchone():               
            # Create a new Land table from the variable list of Land Class
            new_land_table_formatter = '('
            for var in society_instance.land_var_list:
                # Add person variables to the formatter
                new_land_table_formatter += var[0] + ' ' + var[2] + ','  
            new_land_table_formatter = new_land_table_formatter[0: len(new_land_table_formatter) - 1] + ')'
         
            create_table_order = "create table " + new_land_table_name +''+ new_land_table_formatter
            DataAccess.create_table(output_database, create_table_order)
            DataAccess.db_commit(output_database)
    
    
            for ParcelID in society_instance.land_dict:
                # Make the insert values for this land parcel
                new_land_record_content = '('
                for var in society_instance.land_var_list:
                    # If the value is string, add quotes
                    if var[2] == 'VARCHAR' and getattr(society_instance.land_dict[ParcelID], var[0]) != None: 
                        new_land_record_content += '\''+ unicode(getattr(society_instance.land_dict[ParcelID], var[0]))+ '\','
                    else:
                        new_land_record_content += unicode(getattr(society_instance.land_dict[ParcelID], var[0]))+ ','
                # Change the ending comma to a closing parenthesis
                new_land_record_content = new_land_record_content[0:len(new_land_record_content)-1] + ')'
                # Insert one land parcel record
                insert_table_order = "insert into " + new_land_table_name + ' values ' + new_land_record_content.replace('None','Null') +';'
                DataAccess.insert_record_to_table(output_database, insert_table_order)
            DataAccess.db_commit(output_database)  
     
         
        else:

            for ParcelID in society_instance.land_dict:
                # Make the insert values for this household
                new_land_record_content = '('
                for var in society_instance.land_var_list:
                    # If the value is string, add quotes
                    if var[2] == 'VARCHAR' and getattr(society_instance.land_dict[ParcelID], var[0]) != None: 
                        new_land_record_content += '\''+ unicode(getattr(society_instance.land_dict[ParcelID], var[0]))+ '\','
                    else:
                        new_land_record_content += unicode(getattr(society_instance.land_dict[ParcelID], var[0]))+ ','
                # Change the ending comma to a closing parenthesis
                new_land_record_content = new_land_record_content[0:len(new_land_record_content)-1] + ')'
                # Insert one land parcel record
                insert_table_order = "insert into " + new_land_table_name + ' values ' + new_land_record_content.replace('None','Null') +';'
                DataAccess.insert_record_to_table(output_database, insert_table_order)
            DataAccess.db_commit(output_database)        




    '''
    # Saving the Statistics table in the output_database  
    '''  
    # The data table "StatTable" should be pre-created in the output_database
    # So no need to consider the case when a such table does not exist.
    for StatID in society_instance.stat_dict:
        # Make the insert values for this household
        stat_record_content = '('
        for var in society_instance.stat_var_list:
            # If the value is string, add quotes
            if var[2] == 'VARCHAR' and getattr(society_instance.stat_dict[StatID], var[0]) != None: 
                stat_record_content += '\''+ unicode(getattr(society_instance.stat_dict[StatID], var[0]))+ '\','
            else:
                stat_record_content += unicode(getattr(society_instance.stat_dict[StatID], var[0]))+ ','
        # Change the ending comma to a closing parenthesis
        stat_record_content = stat_record_content[0:len(stat_record_content)-1] + ')'
        # Insert one household record
        insert_table_order = "insert into " + stat_table_name + ' values ' + stat_record_content.replace('None','Null') +';'
        DataAccess.insert_record_to_table(output_database, insert_table_order)
    DataAccess.db_commit(output_database)           






def export_maps(database, society_instance, scenario_name, iteration_count, pp_save_interval, hh_save_interval, land_save_interval, gui):

    # Import arcpy first.
    import arcpy
    from arcpy import env

    # Set Arcpy environment settings
    env.workspace = arcpy_workspace
    
    # Set output workspace
    outWorkspace = arcpy_workspace
    
    # Set output path for external files (.mxd maps, .png map figures, etc) for the specific scenario version
    # Create one if it does not already exist.
    version_output_gis_path = output_gis_path + '\\' + scenario_name
    if os.path.isdir(version_output_gis_path) == False:
        os.makedirs(version_output_gis_path)
    
    # Copy the .mxd map into the version's output path, and rename it with a _scenarioname suffix.
    input_mxd_location = input_mxd_path + '\\' + input_mxd
    output_mxd = version_output_gis_path + '\\' + input_mxd[:-4] + '_' + scenario_name + '.mxd'
    if os.path.isfile(output_mxd) == False:
        copyfile(input_mxd_location, output_mxd)


    # Make a folder to store the exported shapefiles
    export_shapefile_path = version_output_gis_path + '\\export_shapefiles'
    if os.path.isdir(export_shapefile_path) == False:
        os.makedirs(export_shapefile_path)    

    # Make a folder to store the exported .png map figures
    export_png_path = version_output_gis_path + '\\export_maps_png' 
    if os.path.isdir(export_png_path) == False:
        os.makedirs(export_png_path)


    # Get the LandUse feature class name respective to the specific post-earthquake restoration scenario
    if gui.rbt_S1_Onsite.isChecked() == True:
        land_feature_name = 'LandUse_S1'
    elif gui.rbt_S2_VilGroups.isChecked() == True:
        land_feature_name = 'LandUse_S2'              
    elif gui.rbt_S3_Townctrs.isChecked() == True:
        land_feature_name = 'LandUse_S3'        
    

    # Check saving intervals. Only export maps along with a land table saved.
    if iteration_count % int(land_save_interval) == 0:

        map_save_year = society_instance.current_year
        new_landuse_feature_name = 'LandUse_' + scenario_name + '_' + str(map_save_year) + '.shp'
        

        # Get the map file (.mxd)
        map_mxd = arcpy.mapping.MapDocument(output_mxd)


        # Get the legend, and set not to auto add newly added items into the legend.
        legend = arcpy.mapping.ListLayoutElements(map_mxd, "LEGEND_ELEMENT", "Legend")[0]
        legend.autoAdd = False
        

        # Export the base feature (LandUse feature) as a shapefile as the working feature for map display
        arcpy.FeatureClassToFeatureClass_conversion (land_feature_name, export_shapefile_path, new_landuse_feature_name)        
        
        
        # Make a layer from the copied feature.
        new_landuse_feature_full_path = str(export_shapefile_path + '\\' + new_landuse_feature_name)
        arcpy.MakeFeatureLayer_management(new_landuse_feature_full_path, new_landuse_feature_name)

        # Get the database table for the land records respective to the map
        insert_land_table_name = str( '"' + scenario_name + '_land"')
        insert_land_table = DataAccess.get_table(database, insert_land_table_name)

        # Read relevant records from the land table and save the records in a dictionary indexed by ParcelID of land records
        to_be_inserted_dict = dict()
        
        for record in insert_land_table:
            if record.StatDate == map_save_year:
                to_be_inserted_dict[record.ParcelID] = record.LandCover

        # Update values in field LandCover in the shapefile's attribute table to reflect the new land cover status
        features = arcpy.UpdateCursor(new_landuse_feature_full_path)
        for feature in features:            
            feature.LandCover = to_be_inserted_dict[feature.ParcelID]
            features.updateRow(feature)


        # Apply the predefined symbology to the new layer. 
        layer = arcpy.mapping.Layer(new_landuse_feature_full_path)
        arcpy.ApplySymbologyFromLayer_management(layer, layer_styles_location)
        
        
        # Add the layer to every data frame in the .mxd map, and then turn off the original land use layers
        for i in range(3):
            d_f = arcpy.mapping.ListDataFrames(map_mxd)[i]
            map_mxd.activeView = d_f
                    
            arcpy.mapping.AddLayer(d_f, layer, "AUTO_ARRANGE")
            
            current_layers = arcpy.mapping.ListLayers(map_mxd, "*", d_f)
            original_layer_names = ['LandUse_S1', 'LandUse_S2', 'LandUse_S3']
            for ly in current_layers:
                if ly.name in original_layer_names:
                    ly.visible = False
            
            arcpy.RefreshTOC()
            arcpy.RefreshActiveView()
                            
            map_mxd.save()


        # Output the map as a .PNG image
        # The [:-4] slicing is for removing the '.shp' extension
        new_landuse_map_png_name = str(export_png_path + '\\' + new_landuse_feature_name[:-4] + '.png')
        
        arcpy.mapping.ExportToPNG(map_mxd, new_landuse_map_png_name, resolution=165)        
                
        

        '''
        The following codes are the operations that are based on features in the geodatabase;
        However, this technical approach would lead to new features created in the database,
        and these features can't be deleted from the database (encounters the "schema lock" when trying to do so) 
        when the scenario version is deleted.
        
        
        # Make a copy of the base feature (LandUse feature) as the working feature for map display
        arcpy.CopyFeatures_management('LandUse', str(outWorkspace + '/' + new_landuse_feature_name))

        # Make a layer from the copied feature.
        arcpy.MakeFeatureLayer_management(new_landuse_feature_name, new_landuse_feature_name)

        # Get the database table for the land records respective to the map
        insert_land_table_name = str( '"' + scenario_name + '_land"')
        insert_land_table = DataAccess.get_table(database, insert_land_table_name)

        # Read relevant records from the land table and save the records in a dictionary indexed by ParcelID of land records
        to_be_inserted_dict = dict()
        
        for record in insert_land_table:
            if record.StatDate == map_save_year:
                to_be_inserted_dict[record.ParcelID] = record.LandCover

        # Update values in field LandCover to reflect the new land cover status
        for ParcelID in to_be_inserted_dict:
            update_table_order = "UPDATE " + new_landuse_feature_name + " SET LandCover = '"  + str(to_be_inserted_dict[ParcelID]) + "' WHERE ParcelID = " + str(ParcelID)
        
            DataAccess.update_table(database, update_table_order)
            DataAccess.db_commit(database)

        # Apply the predefined symbology to the new layer        
        layer = arcpy.mapping.Layer(new_landuse_feature_name)
        arcpy.ApplySymbologyFromLayer_management(layer, layer_styles_location)
        d_f = arcpy.mapping.ListDataFrames(map_mxd)[0]
        arcpy.mapping.AddLayer(d_f, layer, "AUTO_ARRANGE")
        map_mxd.save()

        # Output the map as a .PNG image
        new_landuse_map_png_name = str(export_png_path + '\\' + new_landuse_feature_name + '.png')
        
        arcpy.mapping.ExportToPNG(map_mxd, new_landuse_map_png_name, resolution=165)
        '''






def delete_scenario_version(version_name, database, gui):
    '''
    Remove a scenario version from the VersionTable;
    Also remove all the statistics records related to this scenario version in the StatTable;
    Also drop the households, persons, and land tables related to this scenario version in the database.
    '''

    # Delete the scenario version's record from the VersionTable
    delete_version_record_order = str("delete from " + version_table_name + " where ScenarioName = '" + version_name + "'")
    DataAccess.delete_record_from_table(database, delete_version_record_order)
    DataAccess.db_commit(database)


    # Delete the related statistics from the StatTable 
    delete_stat_record_order = str("delete from " + stat_table_name + " where ScenarioVersion = '" + version_name + "'")
    DataAccess.delete_record_from_table(database, delete_stat_record_order)
    DataAccess.db_commit(database)    
    
    
    # Drop the tables
    if database.cursor.tables(table=str(version_name + '_households')).fetchone(): # if the table exists
        drop_hh_table_order = str('drop table ' + version_name + '_households')
        DataAccess.drop_table(database, drop_hh_table_order)
    
    if database.cursor.tables(table=str(version_name + '_persons')).fetchone():    
        drop_pp_table_order = str('drop table ' + version_name + '_persons')
        DataAccess.drop_table(database, drop_pp_table_order)
    if database.cursor.tables(table=str(version_name + '_land')).fetchone():           
        drop_land_table_order = str('drop table ' + version_name + '_land')
        DataAccess.drop_table(database, drop_land_table_order)
    
    DataAccess.db_commit(database)
    
    # Remove the respective GIS output folder and all its contents (the .mxd file, the shapefiles, and the .png map figures)
    version_output_gis_path = str(output_gis_path + '\\' + version_name)
    if os.path.isdir(version_output_gis_path) == True:    
        rmtree(version_output_gis_path)


    '''
    The following codes got "ERROR 000464: Cannot get exclusive schema lock." all the time. 
    Leave this for now. Liyan. 20150619.
    
#     # Delete the respective features in the database
#     # Import arcpy first.
#     import arcpy
#     from arcpy import env
#     # Set Arcpy environment settings
#     env.workspace = arcpy_workspace
#     
#     # Delete the features
#     arcpy.Delete_management("LandUse_a003_2016")
    '''
    
    # Refresh the automatically displayed new scenario name in the GUI
    gui.add_default_new_scenario_name()
    
    # Return True if succeeded.
    return True


def refresh_progress_bar(progress, gui):
    gui.prb_progressBar.setValue(progress)



def refresh_version_table(database, scenario_name, start_year, simulation_depth, pp_save_interval, hh_save_interval, land_save_interval):
    
    order = str("insert into VersionTable values ('" + scenario_name +"', '', " + str(start_year) + ', ' 
                + str(start_year + simulation_depth) + ", " 
                + str(hh_save_interval) +", " + str(pp_save_interval) + ", " + str(land_save_interval) + ");")
    
    DataAccess.insert_record_to_table(database, order)
    DataAccess.db_commit(database)
    
    


'''
GUI design and Events handling

'''


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s
 
try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)



class Ui_frm_SEEMS_main(object):
      
  
    def setupUi(self, frm_SEEMS_main):
           
        '''
        The followings are PyQt auto-generated codes from the Qt Designer.
        Up until otherwise indicated.
        '''
        
        # Set up the main window frame
        frm_SEEMS_main.setObjectName(_fromUtf8("frm_SEEMS_main"))
        frm_SEEMS_main.resize(1397, 819)

        # Set up the central widget and its layouts
        self.centralwidget = QtGui.QWidget(frm_SEEMS_main)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        
        # Set up the control panel widget. The control panel has 3 tabs.
        self.tab_controlpanel = QtGui.QTabWidget(self.centralwidget)
        self.tab_controlpanel.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.tab_controlpanel.setObjectName(_fromUtf8("tab_controlpanel"))
        
        # First tab -  Scenarios Manager
        self.scenarios_manager = QtGui.QWidget()
        self.scenarios_manager.setObjectName(_fromUtf8("scenarios_manager"))
        self.horizontalLayout_8 = QtGui.QHBoxLayout(self.scenarios_manager)
        self.horizontalLayout_8.setObjectName(_fromUtf8("horizontalLayout_8"))
        self.gbx_scenario_container = QtGui.QGroupBox(self.scenarios_manager)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gbx_scenario_container.sizePolicy().hasHeightForWidth())
        self.gbx_scenario_container.setSizePolicy(sizePolicy)
        self.gbx_scenario_container.setMaximumSize(QtCore.QSize(700, 16777215))
        self.gbx_scenario_container.setTitle(_fromUtf8(""))
        self.gbx_scenario_container.setObjectName(_fromUtf8("gbx_scenario_container"))
        self.verticalLayout = QtGui.QVBoxLayout(self.gbx_scenario_container)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gbx_setup_a_scenario = QtGui.QGroupBox(self.gbx_scenario_container)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gbx_setup_a_scenario.sizePolicy().hasHeightForWidth())
        self.gbx_setup_a_scenario.setSizePolicy(sizePolicy)
        self.gbx_setup_a_scenario.setObjectName(_fromUtf8("gbx_setup_a_scenario"))
        self.verticalLayout_7 = QtGui.QVBoxLayout(self.gbx_setup_a_scenario)
        self.verticalLayout_7.setObjectName(_fromUtf8("verticalLayout_7"))
        self.formLayout_3 = QtGui.QFormLayout()
        self.formLayout_3.setObjectName(_fromUtf8("formLayout_3"))
        self.lbl_input_scenario_name = QtGui.QLabel(self.gbx_setup_a_scenario)
        self.lbl_input_scenario_name.setObjectName(_fromUtf8("lbl_input_scenario_name"))
        self.formLayout_3.setWidget(0, QtGui.QFormLayout.LabelRole, self.lbl_input_scenario_name)
        self.txt_input_scenario_name = QtGui.QLineEdit(self.gbx_setup_a_scenario)
        self.txt_input_scenario_name.setObjectName(_fromUtf8("txt_input_scenario_name"))
        self.formLayout_3.setWidget(0, QtGui.QFormLayout.FieldRole, self.txt_input_scenario_name)
        self.verticalLayout_7.addLayout(self.formLayout_3)
        self.groupBox = QtGui.QGroupBox(self.gbx_setup_a_scenario)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setMaximumSize(QtCore.QSize(16777215, 100))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout_6 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout_6.setObjectName(_fromUtf8("gridLayout_6"))
        self.horizontalLayout_13 = QtGui.QHBoxLayout()
        self.horizontalLayout_13.setObjectName(_fromUtf8("horizontalLayout_13"))
        self.rbt_S1_Onsite = QtGui.QRadioButton(self.groupBox)
        self.rbt_S1_Onsite.setChecked(True)
        self.rbt_S1_Onsite.setObjectName(_fromUtf8("rbt_S1_Onsite"))
        self.horizontalLayout_13.addWidget(self.rbt_S1_Onsite)
        self.rbt_S2_VilGroups = QtGui.QRadioButton(self.groupBox)
        self.rbt_S2_VilGroups.setObjectName(_fromUtf8("rbt_S2_VilGroups"))
        self.horizontalLayout_13.addWidget(self.rbt_S2_VilGroups)
        self.rbt_S3_Townctrs = QtGui.QRadioButton(self.groupBox)
        self.rbt_S3_Townctrs.setObjectName(_fromUtf8("rbt_S3_Townctrs"))
        self.horizontalLayout_13.addWidget(self.rbt_S3_Townctrs)
        self.gridLayout_6.addLayout(self.horizontalLayout_13, 0, 0, 1, 1)
        self.verticalLayout_7.addWidget(self.groupBox)
        self.gbx_set_simulation_period = QtGui.QGroupBox(self.gbx_setup_a_scenario)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gbx_set_simulation_period.sizePolicy().hasHeightForWidth())
        self.gbx_set_simulation_period.setSizePolicy(sizePolicy)
        self.gbx_set_simulation_period.setMaximumSize(QtCore.QSize(16777215, 100))
        self.gbx_set_simulation_period.setObjectName(_fromUtf8("gbx_set_simulation_period"))
        self.gridLayout_2 = QtGui.QGridLayout(self.gbx_set_simulation_period)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.lbl_set_simulation_start_year = QtGui.QLabel(self.gbx_set_simulation_period)
        self.lbl_set_simulation_start_year.setObjectName(_fromUtf8("lbl_set_simulation_start_year"))
        self.gridLayout_2.addWidget(self.lbl_set_simulation_start_year, 0, 0, 1, 1)
        self.sbx_set_simulation_start_year = QtGui.QSpinBox(self.gbx_set_simulation_period)
        self.sbx_set_simulation_start_year.setMaximum(3000)
        self.sbx_set_simulation_start_year.setProperty("value", 2015)
        self.sbx_set_simulation_start_year.setObjectName(_fromUtf8("sbx_set_simulation_start_year"))
        self.gridLayout_2.addWidget(self.sbx_set_simulation_start_year, 0, 1, 1, 1)
        self.lbl_set_simulation_end_year = QtGui.QLabel(self.gbx_set_simulation_period)
        self.lbl_set_simulation_end_year.setObjectName(_fromUtf8("lbl_set_simulation_end_year"))
        self.gridLayout_2.addWidget(self.lbl_set_simulation_end_year, 0, 2, 1, 1)
        self.sbx_set_simulation_end_year = QtGui.QSpinBox(self.gbx_set_simulation_period)
        self.sbx_set_simulation_end_year.setMaximum(3000)
        self.sbx_set_simulation_end_year.setProperty("value", 2020)
        self.sbx_set_simulation_end_year.setObjectName(_fromUtf8("sbx_set_simulation_end_year"))
        self.gridLayout_2.addWidget(self.sbx_set_simulation_end_year, 0, 3, 1, 1)
        self.verticalLayout_7.addWidget(self.gbx_set_simulation_period)
        self.gbx_results_saving_options = QtGui.QGroupBox(self.gbx_setup_a_scenario)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gbx_results_saving_options.sizePolicy().hasHeightForWidth())
        self.gbx_results_saving_options.setSizePolicy(sizePolicy)
        self.gbx_results_saving_options.setObjectName(_fromUtf8("gbx_results_saving_options"))
        self.verticalLayout_6 = QtGui.QVBoxLayout(self.gbx_results_saving_options)
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lbl_save_hh = QtGui.QLabel(self.gbx_results_saving_options)
        self.lbl_save_hh.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lbl_save_hh.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_save_hh.setObjectName(_fromUtf8("lbl_save_hh"))
        self.gridLayout.addWidget(self.lbl_save_hh, 0, 1, 1, 1)
        self.txt_save_hh_interval = QtGui.QLineEdit(self.gbx_results_saving_options)
        self.txt_save_hh_interval.setMaximumSize(QtCore.QSize(50, 16777215))
        self.txt_save_hh_interval.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.txt_save_hh_interval.setObjectName(_fromUtf8("txt_save_hh_interval"))
        self.gridLayout.addWidget(self.txt_save_hh_interval, 0, 2, 1, 1)
        self.lbl_save_hh_years = QtGui.QLabel(self.gbx_results_saving_options)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_save_hh_years.sizePolicy().hasHeightForWidth())
        self.lbl_save_hh_years.setSizePolicy(sizePolicy)
        self.lbl_save_hh_years.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_save_hh_years.setObjectName(_fromUtf8("lbl_save_hh_years"))
        self.gridLayout.addWidget(self.lbl_save_hh_years, 0, 3, 1, 1)
        self.ckb_save_hh_status = QtGui.QCheckBox(self.gbx_results_saving_options)
        self.ckb_save_hh_status.setEnabled(False)
        self.ckb_save_hh_status.setAcceptDrops(False)
        self.ckb_save_hh_status.setChecked(True)
        self.ckb_save_hh_status.setObjectName(_fromUtf8("ckb_save_hh_status"))
        self.gridLayout.addWidget(self.ckb_save_hh_status, 0, 0, 1, 1)
        self.verticalLayout_6.addLayout(self.gridLayout)
        self.gridLayout_4 = QtGui.QGridLayout()
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.lbl_save_pp = QtGui.QLabel(self.gbx_results_saving_options)
        self.lbl_save_pp.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_save_pp.setObjectName(_fromUtf8("lbl_save_pp"))
        self.gridLayout_4.addWidget(self.lbl_save_pp, 0, 1, 1, 1)
        self.txt_save_pp_interval = QtGui.QLineEdit(self.gbx_results_saving_options)
        self.txt_save_pp_interval.setMaximumSize(QtCore.QSize(50, 16777215))
        self.txt_save_pp_interval.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.txt_save_pp_interval.setObjectName(_fromUtf8("txt_save_pp_interval"))
        self.gridLayout_4.addWidget(self.txt_save_pp_interval, 0, 2, 1, 1)
        self.lbl_save_pp_years = QtGui.QLabel(self.gbx_results_saving_options)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_save_pp_years.sizePolicy().hasHeightForWidth())
        self.lbl_save_pp_years.setSizePolicy(sizePolicy)
        self.lbl_save_pp_years.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_save_pp_years.setObjectName(_fromUtf8("lbl_save_pp_years"))
        self.gridLayout_4.addWidget(self.lbl_save_pp_years, 0, 3, 1, 1)
        self.ckb_save_person_status = QtGui.QCheckBox(self.gbx_results_saving_options)
        self.ckb_save_person_status.setEnabled(False)
        self.ckb_save_person_status.setCheckable(True)
        self.ckb_save_person_status.setChecked(True)
        self.ckb_save_person_status.setObjectName(_fromUtf8("ckb_save_person_status"))
        self.gridLayout_4.addWidget(self.ckb_save_person_status, 0, 0, 1, 1)
        self.verticalLayout_6.addLayout(self.gridLayout_4)
        self.gridLayout_5 = QtGui.QGridLayout()
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.txt_save_land_interval = QtGui.QLineEdit(self.gbx_results_saving_options)
        self.txt_save_land_interval.setMaximumSize(QtCore.QSize(50, 16777215))
        self.txt_save_land_interval.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.txt_save_land_interval.setObjectName(_fromUtf8("txt_save_land_interval"))
        self.gridLayout_5.addWidget(self.txt_save_land_interval, 0, 2, 1, 1)
        self.lbl_save_land = QtGui.QLabel(self.gbx_results_saving_options)
        self.lbl_save_land.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_save_land.setObjectName(_fromUtf8("lbl_save_land"))
        self.gridLayout_5.addWidget(self.lbl_save_land, 0, 1, 1, 1)
        self.lbl_save_land_years = QtGui.QLabel(self.gbx_results_saving_options)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_save_land_years.sizePolicy().hasHeightForWidth())
        self.lbl_save_land_years.setSizePolicy(sizePolicy)
        self.lbl_save_land_years.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_save_land_years.setObjectName(_fromUtf8("lbl_save_land_years"))
        self.gridLayout_5.addWidget(self.lbl_save_land_years, 0, 3, 1, 1)
        self.ckb_save_landuse_status = QtGui.QCheckBox(self.gbx_results_saving_options)
        self.ckb_save_landuse_status.setObjectName(_fromUtf8("ckb_save_landuse_status"))
        self.gridLayout_5.addWidget(self.ckb_save_landuse_status, 0, 0, 1, 1)
        self.verticalLayout_6.addLayout(self.gridLayout_5)
        self.verticalLayout_7.addWidget(self.gbx_results_saving_options)
        self.btn_start_simulation = QtGui.QPushButton(self.gbx_setup_a_scenario)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_start_simulation.sizePolicy().hasHeightForWidth())
        self.btn_start_simulation.setSizePolicy(sizePolicy)
        self.btn_start_simulation.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.btn_start_simulation.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.btn_start_simulation.setObjectName(_fromUtf8("btn_start_simulation"))
        self.verticalLayout_7.addWidget(self.btn_start_simulation)
        self.prb_progressBar = QtGui.QProgressBar(self.gbx_setup_a_scenario)
        self.prb_progressBar.setProperty("value", 0)
        self.prb_progressBar.setObjectName(_fromUtf8("prb_progressBar"))
        self.verticalLayout_7.addWidget(self.prb_progressBar)
        self.verticalLayout.addWidget(self.gbx_setup_a_scenario)
        spacerItem = QtGui.QSpacerItem(20, 16777215, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.gbx_manage_scenarios = QtGui.QGroupBox(self.gbx_scenario_container)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gbx_manage_scenarios.sizePolicy().hasHeightForWidth())
        self.gbx_manage_scenarios.setSizePolicy(sizePolicy)
        self.gbx_manage_scenarios.setObjectName(_fromUtf8("gbx_manage_scenarios"))
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.gbx_manage_scenarios)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.lbl_select_manage_scenario = QtGui.QLabel(self.gbx_manage_scenarios)
        self.lbl_select_manage_scenario.setObjectName(_fromUtf8("lbl_select_manage_scenario"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.lbl_select_manage_scenario)
        self.cmb_select_manage_scenario = QtGui.QComboBox(self.gbx_manage_scenarios)
        self.cmb_select_manage_scenario.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContentsOnFirstShow)
        self.cmb_select_manage_scenario.setObjectName(_fromUtf8("cmb_select_manage_scenario"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.cmb_select_manage_scenario)
        self.verticalLayout_5.addLayout(self.formLayout)
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.btn_rename_scenario = QtGui.QPushButton(self.gbx_manage_scenarios)
        self.btn_rename_scenario.setObjectName(_fromUtf8("btn_rename_scenario"))
        self.horizontalLayout_7.addWidget(self.btn_rename_scenario)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem1)
        self.btn_delete_scenario = QtGui.QPushButton(self.gbx_manage_scenarios)
        self.btn_delete_scenario.setObjectName(_fromUtf8("btn_delete_scenario"))
        self.horizontalLayout_7.addWidget(self.btn_delete_scenario)
        self.verticalLayout_5.addLayout(self.horizontalLayout_7)
        self.verticalLayout.addWidget(self.gbx_manage_scenarios)
        self.horizontalLayout_8.addWidget(self.gbx_scenario_container)
        self.greetings_widget = QtGui.QWidget(self.scenarios_manager)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.greetings_widget.sizePolicy().hasHeightForWidth())
        self.greetings_widget.setSizePolicy(sizePolicy)
        self.greetings_widget.setObjectName(_fromUtf8("greetings_widget"))
        self.horizontalLayout_8.addWidget(self.greetings_widget)
        self.tab_controlpanel.addTab(self.scenarios_manager, _fromUtf8(""))



        # Second tab - Results - Charts
        self.results_charts = QtGui.QWidget()
        self.results_charts.setObjectName(_fromUtf8("results_charts"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.results_charts)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.gbx_review_plot_container = QtGui.QGroupBox(self.results_charts)
        self.gbx_review_plot_container.setMaximumSize(QtCore.QSize(700, 16777215))
        self.gbx_review_plot_container.setTitle(_fromUtf8(""))
        self.gbx_review_plot_container.setObjectName(_fromUtf8("gbx_review_plot_container"))
        self.verticalLayout_9 = QtGui.QVBoxLayout(self.gbx_review_plot_container)
        self.verticalLayout_9.setObjectName(_fromUtf8("verticalLayout_9"))
        self.gpb_select_plot_data_type = QtGui.QGroupBox(self.gbx_review_plot_container)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gpb_select_plot_data_type.sizePolicy().hasHeightForWidth())
        self.gpb_select_plot_data_type.setSizePolicy(sizePolicy)
        self.gpb_select_plot_data_type.setObjectName(_fromUtf8("gpb_select_plot_data_type"))
        self.gridLayout_3 = QtGui.QGridLayout(self.gpb_select_plot_data_type)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.rbt_single_variable_time_series = QtGui.QRadioButton(self.gpb_select_plot_data_type)
        self.rbt_single_variable_time_series.setObjectName(_fromUtf8("rbt_single_variable_time_series"))
        self.gridLayout_3.addWidget(self.rbt_single_variable_time_series, 0, 0, 1, 1)
        self.rbt_multi_variable_time_series = QtGui.QRadioButton(self.gpb_select_plot_data_type)
        self.rbt_multi_variable_time_series.setObjectName(_fromUtf8("rbt_multi_variable_time_series"))
        self.gridLayout_3.addWidget(self.rbt_multi_variable_time_series, 0, 1, 1, 1)
        self.rbt_single_variable_cross_section = QtGui.QRadioButton(self.gpb_select_plot_data_type)
        self.rbt_single_variable_cross_section.setObjectName(_fromUtf8("rbt_single_variable_cross_section"))
        self.gridLayout_3.addWidget(self.rbt_single_variable_cross_section, 1, 0, 1, 1)
        self.verticalLayout_9.addWidget(self.gpb_select_plot_data_type)
        self.gbx_select_plot_scenario_and_variable = QtGui.QGroupBox(self.gbx_review_plot_container)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gbx_select_plot_scenario_and_variable.sizePolicy().hasHeightForWidth())
        self.gbx_select_plot_scenario_and_variable.setSizePolicy(sizePolicy)
        self.gbx_select_plot_scenario_and_variable.setObjectName(_fromUtf8("gbx_select_plot_scenario_and_variable"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.gbx_select_plot_scenario_and_variable)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.formLayout_4 = QtGui.QFormLayout()
        self.formLayout_4.setObjectName(_fromUtf8("formLayout_4"))
        self.lbl_select_review_scenario = QtGui.QLabel(self.gbx_select_plot_scenario_and_variable)
        self.lbl_select_review_scenario.setObjectName(_fromUtf8("lbl_select_review_scenario"))
        self.formLayout_4.setWidget(0, QtGui.QFormLayout.LabelRole, self.lbl_select_review_scenario)
        self.cmb_select_review_scenario = QtGui.QComboBox(self.gbx_select_plot_scenario_and_variable)
        self.cmb_select_review_scenario.setObjectName(_fromUtf8("cmb_select_review_scenario"))
        self.formLayout_4.setWidget(0, QtGui.QFormLayout.FieldRole, self.cmb_select_review_scenario)
        self.lbl_select_review_variable = QtGui.QLabel(self.gbx_select_plot_scenario_and_variable)
        self.lbl_select_review_variable.setObjectName(_fromUtf8("lbl_select_review_variable"))
        self.formLayout_4.setWidget(1, QtGui.QFormLayout.LabelRole, self.lbl_select_review_variable)
        self.cmb_select_review_variable = QtGui.QComboBox(self.gbx_select_plot_scenario_and_variable)
        self.cmb_select_review_variable.setObjectName(_fromUtf8("cmb_select_review_variable"))
        self.formLayout_4.setWidget(1, QtGui.QFormLayout.FieldRole, self.cmb_select_review_variable)
        self.verticalLayout_2.addLayout(self.formLayout_4)
        self.verticalLayout_9.addWidget(self.gbx_select_plot_scenario_and_variable)
        self.gbx_select_plot_period_and_type = QtGui.QGroupBox(self.gbx_review_plot_container)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gbx_select_plot_period_and_type.sizePolicy().hasHeightForWidth())
        self.gbx_select_plot_period_and_type.setSizePolicy(sizePolicy)
        self.gbx_select_plot_period_and_type.setObjectName(_fromUtf8("gbx_select_plot_period_and_type"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.gbx_select_plot_period_and_type)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.gbx_plot_period = QtGui.QGroupBox(self.gbx_select_plot_period_and_type)
        self.gbx_plot_period.setObjectName(_fromUtf8("gbx_plot_period"))
        self.verticalLayout_11 = QtGui.QVBoxLayout(self.gbx_plot_period)
        self.verticalLayout_11.setObjectName(_fromUtf8("verticalLayout_11"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.formLayout_5 = QtGui.QFormLayout()
        self.formLayout_5.setObjectName(_fromUtf8("formLayout_5"))
        self.lbl_select_plot_start_year = QtGui.QLabel(self.gbx_plot_period)
        self.lbl_select_plot_start_year.setObjectName(_fromUtf8("lbl_select_plot_start_year"))
        self.formLayout_5.setWidget(0, QtGui.QFormLayout.LabelRole, self.lbl_select_plot_start_year)
        self.sbx_select_plot_start_year = QtGui.QSpinBox(self.gbx_plot_period)
        self.sbx_select_plot_start_year.setMaximum(3000)
        self.sbx_select_plot_start_year.setProperty("value", 0)
        self.sbx_select_plot_start_year.setObjectName(_fromUtf8("sbx_select_plot_start_year"))
        self.formLayout_5.setWidget(0, QtGui.QFormLayout.FieldRole, self.sbx_select_plot_start_year)
        self.horizontalLayout_4.addLayout(self.formLayout_5)
        self.formLayout_6 = QtGui.QFormLayout()
        self.formLayout_6.setObjectName(_fromUtf8("formLayout_6"))
        self.lbl_select_plot_end_year = QtGui.QLabel(self.gbx_plot_period)
        self.lbl_select_plot_end_year.setObjectName(_fromUtf8("lbl_select_plot_end_year"))
        self.formLayout_6.setWidget(0, QtGui.QFormLayout.LabelRole, self.lbl_select_plot_end_year)
        self.sbx_select_plot_end_year = QtGui.QSpinBox(self.gbx_plot_period)
        self.sbx_select_plot_end_year.setMaximum(3000)
        self.sbx_select_plot_end_year.setProperty("value", 0)
        self.sbx_select_plot_end_year.setObjectName(_fromUtf8("sbx_select_plot_end_year"))
        self.formLayout_6.setWidget(0, QtGui.QFormLayout.FieldRole, self.sbx_select_plot_end_year)
        self.horizontalLayout_4.addLayout(self.formLayout_6)
        self.verticalLayout_11.addLayout(self.horizontalLayout_4)
        self.verticalLayout_3.addWidget(self.gbx_plot_period)
        self.gbx_plot_type = QtGui.QGroupBox(self.gbx_select_plot_period_and_type)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gbx_plot_type.sizePolicy().hasHeightForWidth())
        self.gbx_plot_type.setSizePolicy(sizePolicy)
        self.gbx_plot_type.setMaximumSize(QtCore.QSize(16777215, 100))
        self.gbx_plot_type.setObjectName(_fromUtf8("gbx_plot_type"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.gbx_plot_type)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.rbt_bar_chart = QtGui.QRadioButton(self.gbx_plot_type)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rbt_bar_chart.sizePolicy().hasHeightForWidth())
        self.rbt_bar_chart.setSizePolicy(sizePolicy)
        self.rbt_bar_chart.setObjectName(_fromUtf8("rbt_bar_chart"))
        self.horizontalLayout_2.addWidget(self.rbt_bar_chart)
        self.rbt_line_chart = QtGui.QRadioButton(self.gbx_plot_type)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rbt_line_chart.sizePolicy().hasHeightForWidth())
        self.rbt_line_chart.setSizePolicy(sizePolicy)
        self.rbt_line_chart.setObjectName(_fromUtf8("rbt_line_chart"))
        self.horizontalLayout_2.addWidget(self.rbt_line_chart)
        self.rbt_histogram = QtGui.QRadioButton(self.gbx_plot_type)
        self.rbt_histogram.setObjectName(_fromUtf8("rbt_histogram"))
        self.horizontalLayout_2.addWidget(self.rbt_histogram)
        self.verticalLayout_3.addWidget(self.gbx_plot_type)
        self.verticalLayout_9.addWidget(self.gbx_select_plot_period_and_type)
        spacerItem2 = QtGui.QSpacerItem(20, 16777215, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_9.addItem(spacerItem2)
        self.btn_review_plot = QtGui.QPushButton(self.gbx_review_plot_container)
        self.btn_review_plot.setObjectName(_fromUtf8("btn_review_plot"))
        self.verticalLayout_9.addWidget(self.btn_review_plot)
        self.horizontalLayout_3.addWidget(self.gbx_review_plot_container)
        self.canvas_widget = QtGui.QWidget(self.results_charts)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.canvas_widget.sizePolicy().hasHeightForWidth())
        self.canvas_widget.setSizePolicy(sizePolicy)
        self.canvas_widget.setObjectName(_fromUtf8("canvas_widget"))
        self.horizontalLayout_3.addWidget(self.canvas_widget)
        self.tab_controlpanel.addTab(self.results_charts, _fromUtf8(""))


        # Third tab - Results - Maps
        self.results_maps = QtGui.QWidget()
        self.results_maps.setObjectName(_fromUtf8("results_maps"))
        self.horizontalLayout_6 = QtGui.QHBoxLayout(self.results_maps)
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.gbx_map_container = QtGui.QGroupBox(self.results_maps)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gbx_map_container.sizePolicy().hasHeightForWidth())
        self.gbx_map_container.setSizePolicy(sizePolicy)
        self.gbx_map_container.setMaximumSize(QtCore.QSize(700, 16777215))
        self.gbx_map_container.setTitle(_fromUtf8(""))
        self.gbx_map_container.setObjectName(_fromUtf8("gbx_map_container"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.gbx_map_container)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.gpb_map_settings = QtGui.QGroupBox(self.gbx_map_container)
        self.gpb_map_settings.setObjectName(_fromUtf8("gpb_map_settings"))
        self.verticalLayout_8 = QtGui.QVBoxLayout(self.gpb_map_settings)
        self.verticalLayout_8.setObjectName(_fromUtf8("verticalLayout_8"))
        self.formLayout_10 = QtGui.QFormLayout()
        self.formLayout_10.setObjectName(_fromUtf8("formLayout_10"))
        self.lbl_select_map_scenario = QtGui.QLabel(self.gpb_map_settings)
        self.lbl_select_map_scenario.setObjectName(_fromUtf8("lbl_select_map_scenario"))
        self.formLayout_10.setWidget(0, QtGui.QFormLayout.LabelRole, self.lbl_select_map_scenario)
        self.cmb_select_map_scenario = QtGui.QComboBox(self.gpb_map_settings)
        self.cmb_select_map_scenario.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContentsOnFirstShow)
        self.cmb_select_map_scenario.setObjectName(_fromUtf8("cmb_select_map_scenario"))
        self.formLayout_10.setWidget(0, QtGui.QFormLayout.FieldRole, self.cmb_select_map_scenario)
        self.lbl_select_map_layer = QtGui.QLabel(self.gpb_map_settings)
        self.lbl_select_map_layer.setObjectName(_fromUtf8("lbl_select_map_layer"))
        self.formLayout_10.setWidget(1, QtGui.QFormLayout.LabelRole, self.lbl_select_map_layer)
        self.cmb_select_map_layer = QtGui.QComboBox(self.gpb_map_settings)
        self.cmb_select_map_layer.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContentsOnFirstShow)
        self.cmb_select_map_layer.setObjectName(_fromUtf8("cmb_select_map_layer"))
        self.formLayout_10.setWidget(1, QtGui.QFormLayout.FieldRole, self.cmb_select_map_layer)
        self.verticalLayout_8.addLayout(self.formLayout_10)
        self.formLayout_2 = QtGui.QFormLayout()
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.lbl_select_map_year = QtGui.QLabel(self.gpb_map_settings)
        self.lbl_select_map_year.setObjectName(_fromUtf8("lbl_select_map_year"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.lbl_select_map_year)
        self.lbl_map_current_year = QtGui.QLabel(self.gpb_map_settings)
        self.lbl_map_current_year.setText(_fromUtf8(""))
        self.lbl_map_current_year.setObjectName(_fromUtf8("lbl_map_current_year"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.FieldRole, self.lbl_map_current_year)
        self.verticalLayout_8.addLayout(self.formLayout_2)
        self.sld_select_map_year = QtGui.QSlider(self.gpb_map_settings)
        self.sld_select_map_year.setOrientation(QtCore.Qt.Horizontal)
        self.sld_select_map_year.setTickPosition(QtGui.QSlider.TicksBelow)
        self.sld_select_map_year.setObjectName(_fromUtf8("sld_select_map_year"))
        self.verticalLayout_8.addWidget(self.sld_select_map_year)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.lbl_map_start_year = QtGui.QLabel(self.gpb_map_settings)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_map_start_year.sizePolicy().hasHeightForWidth())
        self.lbl_map_start_year.setSizePolicy(sizePolicy)
        self.lbl_map_start_year.setText(_fromUtf8(""))
        self.lbl_map_start_year.setObjectName(_fromUtf8("lbl_map_start_year"))
        self.horizontalLayout_5.addWidget(self.lbl_map_start_year)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem3)
        self.lbl_map_end_year = QtGui.QLabel(self.gpb_map_settings)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_map_end_year.sizePolicy().hasHeightForWidth())
        self.lbl_map_end_year.setSizePolicy(sizePolicy)
        self.lbl_map_end_year.setText(_fromUtf8(""))
        self.lbl_map_end_year.setObjectName(_fromUtf8("lbl_map_end_year"))
        self.horizontalLayout_5.addWidget(self.lbl_map_end_year)
        self.verticalLayout_8.addLayout(self.horizontalLayout_5)
        self.verticalLayout_4.addWidget(self.gpb_map_settings)
        spacerItem4 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem4)
        self.btn_show_map = QtGui.QPushButton(self.gbx_map_container)
        self.btn_show_map.setObjectName(_fromUtf8("btn_show_map"))
        self.verticalLayout_4.addWidget(self.btn_show_map)
        self.horizontalLayout_6.addWidget(self.gbx_map_container)
        self.map_display_widget = QtGui.QWidget(self.results_maps)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.map_display_widget.sizePolicy().hasHeightForWidth())
        self.map_display_widget.setSizePolicy(sizePolicy)
        self.map_display_widget.setObjectName(_fromUtf8("map_display_widget"))
        self.horizontalLayout_6.addWidget(self.map_display_widget)
        self.tab_controlpanel.addTab(self.results_maps, _fromUtf8(""))

        
        # Add the control panel widget            
        self.horizontalLayout.addWidget(self.tab_controlpanel)
        frm_SEEMS_main.setCentralWidget(self.centralwidget)        
                
        # Other window components - menu, status bar, etc.
        self.menubar = QtGui.QMenuBar(frm_SEEMS_main)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1397, 31))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        frm_SEEMS_main.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(frm_SEEMS_main)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        frm_SEEMS_main.setStatusBar(self.statusbar)
        self.actionAbout = QtGui.QAction(frm_SEEMS_main)
        self.actionAbout.setObjectName(_fromUtf8("actionAbout"))
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(frm_SEEMS_main)
        self.tab_controlpanel.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(frm_SEEMS_main)
    
    
        '''
        The following lines in this submodule are developers added codes.

        First, Check if there exists an output database file;
        And if not, make a copy of the input database file to store the output results 
        (so that to keep the input (original) database clean)    
        '''
        if os.path.isfile(output_db_location) == False:
            copyfile(input_db_location, output_db_location)
            
        output_db = DataAccess(output_db_location, dbdriver)        
        
        '''
        Second, events handling 
        '''
        
        # Scenario management
        self.btn_start_simulation.clicked.connect(self.btn_start_simulation_onclick)        
        self.btn_delete_scenario.clicked.connect(self.btn_delete_scenario_onclick)
        
        
        # Results review - charts
        self.cmb_select_review_scenario.currentIndexChanged.connect(self.cmb_select_review_scenario_onchange)

        self.rbt_single_variable_time_series.toggled.connect(self.rbt_single_variable_time_series_ontoggled)
        self.rbt_single_variable_cross_section.toggled.connect(self.rbt_single_variable_cross_section_ontoggled)
        self.rbt_multi_variable_time_series.toggled.connect(self.rbt_multi_variable_time_series_ontoggled)
        
        self.cmb_select_review_variable.currentIndexChanged.connect(self.cmb_select_review_variable_onchange)

        self.btn_review_plot.clicked.connect(self.btn_review_plot_onclick)
        
        # Results review - maps          
        self.cmb_select_map_scenario.currentIndexChanged.connect(self.cmb_select_map_scenario_onchange)
        self.sld_select_map_year.valueChanged.connect(self.sld_select_map_year_onchange)
        self.btn_show_map.clicked.connect(self.btn_show_map_onclick)

        # Other window components
        self.actionAbout.triggered.connect(self.action_menu_help_about)
        

        '''
        Next, manually add some widgets.
        '''
        # Display a greetings image in the first tab (scenarios manager)
        # Create a QVBoxLayout within the widget for embedding
        self.greeting_lyt = QtGui.QVBoxLayout(self.greetings_widget)
        # Call ImageViewer class to display the image
        greetings_imgage = ImageViewer(widget=self.greetings_widget, layout=self.greeting_lyt, image_path=greetings_image_location, scalable=False)
        self.greeting_lyt.addWidget(greetings_imgage.imageLabel)

        # Display a plot space in the second tab (results - charts)
        self.make_plot_space(widget = self.canvas_widget)   
                
        # Display an empty map in the third (results - maps) tab's map drawing area
        # The map will be automatically replaced by the first scenario's first map layer image if there exists such a scenario, so whatever image here would do.
        self.map_layout = QtGui.QVBoxLayout(self.map_display_widget)
        self.map = ImageViewer(widget=self.map_display_widget, layout=self.map_layout, image_path=greetings_map_location, scalable=True)
        self.map_layout.addWidget(self.map.scrollArea)
                
        # Add a toolbar for map display controls
        self.add_toolbar(frm_SEEMS_main)
        


        '''
        Finally, initialize the GUI components
        '''        
#         # Automatically add a default new scenario name at initiation
        self.add_default_new_scenario_name()

        # Initialize the scenario selection combo boxes in the control panel
        self.refresh_scenario_combobox(self.cmb_select_manage_scenario)
        self.refresh_scenario_combobox(self.cmb_select_review_scenario)
        self.refresh_scenario_combobox(self.cmb_select_map_scenario)
        
        # Initialize the map layer selection combo box in the control panel
        self.refresh_map_tab_map_layers()

        # Temporarily set some input components disabled (read-only)
        self.txt_save_hh_interval.setDisabled(True)
        self.txt_save_pp_interval.setDisabled(True)
        


    def retranslateUi(self, frm_SEEMS_main):
        frm_SEEMS_main.setWindowTitle(_translate("frm_SEEMS_main", "SEEMS  -  Socio-Econ-Ecosystem Multipurpose Simulator", None))
        self.gbx_setup_a_scenario.setTitle(_translate("frm_SEEMS_main", "Setup a New Scenario", None))
        self.lbl_input_scenario_name.setText(_translate("frm_SEEMS_main", "Scenario Name:", None))
        self.groupBox.setTitle(_translate("frm_SEEMS_main", "Post-Earthquake Restoration Options", None))
        self.rbt_S1_Onsite.setText(_translate("frm_SEEMS_main", "On Site", None))
        self.rbt_S2_VilGroups.setText(_translate("frm_SEEMS_main", "To Village Groups", None))
        self.rbt_S3_Townctrs.setText(_translate("frm_SEEMS_main", "To Township Centers", None))
        self.gbx_set_simulation_period.setTitle(_translate("frm_SEEMS_main", "Set Simulation Period", None))
        self.lbl_set_simulation_start_year.setText(_translate("frm_SEEMS_main", "Start Year:", None))
        self.lbl_set_simulation_end_year.setText(_translate("frm_SEEMS_main", "End Year:", None))
        self.gbx_results_saving_options.setTitle(_translate("frm_SEEMS_main", "Results Saving Options", None))
        self.lbl_save_hh.setText(_translate("frm_SEEMS_main", " Every", None))
        self.txt_save_hh_interval.setText(_translate("frm_SEEMS_main", "1", None))
        self.lbl_save_hh_years.setText(_translate("frm_SEEMS_main", "Year(s)", None))
        self.ckb_save_hh_status.setText(_translate("frm_SEEMS_main", "Save Household Status", None))
        self.lbl_save_pp.setText(_translate("frm_SEEMS_main", " Every", None))
        self.txt_save_pp_interval.setText(_translate("frm_SEEMS_main", "1", None))
        self.lbl_save_pp_years.setText(_translate("frm_SEEMS_main", "Year(s)", None))
        self.ckb_save_person_status.setText(_translate("frm_SEEMS_main", "Save Person Status", None))
        self.txt_save_land_interval.setText(_translate("frm_SEEMS_main", "4", None))
        self.lbl_save_land.setText(_translate("frm_SEEMS_main", " Every", None))
        self.lbl_save_land_years.setText(_translate("frm_SEEMS_main", "Year(s)", None))
        self.ckb_save_landuse_status.setText(_translate("frm_SEEMS_main", "Save LandUse Status", None))
        self.btn_start_simulation.setText(_translate("frm_SEEMS_main", "Start Simulation", None))
        self.gbx_manage_scenarios.setTitle(_translate("frm_SEEMS_main", "Manage Scenarios", None))
        self.lbl_select_manage_scenario.setText(_translate("frm_SEEMS_main", "Select Scenario:", None))
        self.btn_rename_scenario.setText(_translate("frm_SEEMS_main", "Rename", None))
        self.btn_delete_scenario.setText(_translate("frm_SEEMS_main", "Delete", None))
        self.tab_controlpanel.setTabText(self.tab_controlpanel.indexOf(self.scenarios_manager), _translate("frm_SEEMS_main", "Scenarios Manager", None))
        self.gpb_select_plot_data_type.setTitle(_translate("frm_SEEMS_main", "Plot Data Type", None))
        self.rbt_single_variable_time_series.setText(_translate("frm_SEEMS_main", "Single Variable Time Series", None))
        self.rbt_multi_variable_time_series.setText(_translate("frm_SEEMS_main", "Multi Variable Time Series", None))
        self.rbt_single_variable_cross_section.setText(_translate("frm_SEEMS_main", "Single Variable Cross Section", None))
        self.gbx_select_plot_scenario_and_variable.setTitle(_translate("frm_SEEMS_main", "Scenario and Variable", None))
        self.lbl_select_review_scenario.setText(_translate("frm_SEEMS_main", "Select Scenario:", None))
        self.lbl_select_review_variable.setText(_translate("frm_SEEMS_main", "Select Variable:", None))
        self.gbx_select_plot_period_and_type.setTitle(_translate("frm_SEEMS_main", "Plot Period and Type", None))
        self.gbx_plot_period.setTitle(_translate("frm_SEEMS_main", "Plot Period", None))
        self.lbl_select_plot_start_year.setText(_translate("frm_SEEMS_main", "Select Start Year:", None))
        self.lbl_select_plot_end_year.setText(_translate("frm_SEEMS_main", "Select End Year:", None))
        self.gbx_plot_type.setTitle(_translate("frm_SEEMS_main", "Plot Type", None))
        self.rbt_bar_chart.setText(_translate("frm_SEEMS_main", "(Stacked) Bars", None))
        self.rbt_line_chart.setText(_translate("frm_SEEMS_main", "(Multiple) Lines", None))
        self.rbt_histogram.setText(_translate("frm_SEEMS_main", "Histogram", None))
        self.btn_review_plot.setText(_translate("frm_SEEMS_main", "Plot", None))
        self.tab_controlpanel.setTabText(self.tab_controlpanel.indexOf(self.results_charts), _translate("frm_SEEMS_main", "Results - Charts", None))
        self.gpb_map_settings.setTitle(_translate("frm_SEEMS_main", "Map Settings", None))
        self.lbl_select_map_scenario.setText(_translate("frm_SEEMS_main", "Select Scenario:", None))
        self.lbl_select_map_layer.setText(_translate("frm_SEEMS_main", "Select Map Layer:", None))
        self.lbl_select_map_year.setText(_translate("frm_SEEMS_main", "Select Map Year:", None))
        self.btn_show_map.setText(_translate("frm_SEEMS_main", "Show Map", None))
        self.tab_controlpanel.setTabText(self.tab_controlpanel.indexOf(self.results_maps), _translate("frm_SEEMS_main", "Results - Maps", None))
        self.menuHelp.setTitle(_translate("frm_SEEMS_main", "Help", None))
        self.actionAbout.setText(_translate("frm_SEEMS_main", "About", None))




    def btn_start_simulation_onclick(self):
        
        
        model_table_name = 'ModelTable'
        household_table_name = 'HouseholdTable'
        person_table_name = 'PersonTable'
        land_table_name = 'LandUseTable'
        business_sector_table_name = 'BusinessSectorTable'
        policy_table_name = 'PolicyTable'
        stat_table_name = 'StatTable'
        version_table_name = 'VersionTable'            

            
        # Update household_table_name and land_table_name according to the GUI input                    
        if self.rbt_S1_Onsite.isChecked() == True:
            household_table_name = household_table_name + '_S1'
            land_table_name = land_table_name + '_S1'
        elif self.rbt_S2_VilGroups.isChecked() == True:
            household_table_name = household_table_name + '_S2'
            land_table_name = land_table_name + '_S2'                
        elif self.rbt_S3_Townctrs.isChecked() == True:
            household_table_name = household_table_name + '_S3'
            land_table_name = land_table_name + '_S3'               
        
        
        
        # Get scenario settings from user inputs
        output_db = DataAccess(output_db_location, dbdriver)
        
        scenario_name = str(self.txt_input_scenario_name.text())
        start_year = self.sbx_set_simulation_start_year.value()
        end_year = self.sbx_set_simulation_end_year.value()
        simulation_depth = end_year - start_year

        hh_save_interval = self.txt_save_hh_interval.text()
        pp_save_interval = self.txt_save_pp_interval.text()
        land_save_interval = self.txt_save_land_interval.text()

        # Check for already existing names first.
        version_table = DataAccess.get_table(output_db, version_table_name)        
        # Get the scenario list.
        scenario_list = list()
        for version in version_table:
            scenario_list.append(str(version[0]))
        
        if scenario_name in scenario_list:
            # Show an Error Message
            msb = QMessageBox()
            msb.setText('The Scenario name has been taken. Make a new one.       ')
            msb.setWindowTitle('SEEMS Run')
            msb.exec_()
        
        else:
            # Run the simulation.

            # Setup the progress bar in the GUI
            self.prb_progressBar.setMinimum(0)
            self.prb_progressBar.setMaximum(simulation_depth * 100)
                      
            # Run the simulation
#             try:
            self.statusbar.showMessage('Running simulation...')

     
            # Get the table pointers
            model_table = DataAccess.get_table(input_db, model_table_name)
            household_table = DataAccess.get_table(input_db, household_table_name)
            person_table = DataAccess.get_table(input_db, person_table_name)
            land_table = DataAccess.get_table(input_db, land_table_name)
            business_sector_table = DataAccess.get_table(input_db, business_sector_table_name)
            policy_table = DataAccess.get_table(input_db, policy_table_name)
            stat_table = DataAccess.get_table(input_db, stat_table_name)
            version_table = DataAccess.get_table(input_db, version_table_name)
            

            # Create the scenario
            create_scenario(output_db, scenario_name, model_table_name, model_table, household_table_name, household_table, 
                            person_table_name, person_table, land_table_name, land_table, 
                            business_sector_table_name, business_sector_table, policy_table_name, policy_table, 
                            stat_table_name, stat_table, simulation_depth, start_year, 
                            pp_save_interval, hh_save_interval, land_save_interval,
                            self)

            # When simulation is done, refresh the default scenario name
            self.add_default_new_scenario_name()
    
            # Then refresh control panel tabs
            self.refresh_scenario_combobox(self.cmb_select_manage_scenario)
            self.refresh_scenario_combobox(self.cmb_select_review_scenario)
            self.refresh_scenario_combobox(self.cmb_select_map_scenario)

            self.refresh_map_tab_map_layers()
            
            # Refresh the status bar
            self.statusbar.showMessage('Simulation complete')
          
            # Show a message box indicating the completion of run.
            msb = QMessageBox()
            msb.setText('The Simulation is Complete!        ')
            msb.setWindowTitle('SEEMS Run')
            msb.exec_()
            
#             except:
#                 # If the run is unsuccessful, revert to the starting point by deleting any tables or records
#                 # that had been inserted to the database.
#                 # And display an error message.
#                 delete_scenario_version(scenario_name, output_db, self)
#                 
#                 # Refresh the status bar
#                 self.statusbar.showMessage('Simulation failed')
#                   
#                   
#                 # Show an Error Message
#                 msb = QMessageBox()
#                 msb.setText('The Simulation is Unsuccessful. Check Codes.        ')
#                 msb.setWindowTitle('SEEMS Run')
#                 msb.exec_()
            


    def add_default_new_scenario_name(self):
        '''
        Note that the codes here is based on scenario names that begin with "_S00x_" ...
        '''
        # Refresh the version_table cursor.
        output_db = DataAccess(output_db_location, dbdriver)
        
        version_table = DataAccess.get_table(output_db, version_table_name)
        
        # Get the scenario list.
        scenario_list = list()
        for version in version_table:
            scenario_list.append(str(version[0]))
        
        if len(scenario_list) == 0:
            new_scenario_name = '_S001'
        else:        
            new_scenario_name_num = int(max(scenario_list)[2:5]) + 1

            if int(new_scenario_name_num/100) != 0: # if the new scenario number is in hundreds
                new_scenario_name = max(scenario_list)[:2] + str(new_scenario_name_num) + max(scenario_list)[5:]
            elif int(new_scenario_name_num/100) == 0 and int(new_scenario_name_num/10) != 0: # if the new scenario number is in tens
                new_scenario_name = max(scenario_list)[:2] + '0' + str(new_scenario_name_num) + max(scenario_list)[5:]
            else:
                new_scenario_name = max(scenario_list)[:2] + '00' + str(new_scenario_name_num) + max(scenario_list)[5:]
        
        self.txt_input_scenario_name.setText(new_scenario_name)



    def btn_delete_scenario_onclick(self):
        
        output_db = DataAccess(output_db_location, dbdriver)
        
        if delete_scenario_version(self.cmb_select_manage_scenario.currentText(), output_db, self):
            
            # Refresh the control panel scenario selection combo boxes
            self.refresh_scenario_combobox(self.cmb_select_manage_scenario)
            self.refresh_scenario_combobox(self.cmb_select_review_scenario)
            self.refresh_scenario_combobox(self.cmb_select_map_scenario)
                        
            # Show a Succeeded Message
            msb = QMessageBox()
            msb.setText('Scenario Deleted!        ')
            msb.setWindowTitle('SEEMS')
            msb.exec_()    
            
            
        else:
            # Refresh the control panel scenario selection combo boxes
            self.refresh_scenario_combobox(self.cmb_select_manage_scenario)
            self.refresh_scenario_combobox(self.cmb_select_review_scenario)
            self.refresh_scenario_combobox(self.cmb_select_map_scenario)

                                    
            # Show an Error Message
            msb = QMessageBox()
            msb.setText('Delete Scenario Failed!        ')
            msb.setWindowTitle('SEEMS')
            msb.exec_()            



    def refresh_scenario_combobox(self, combobox):
        '''
        Refresh a scenario selection combo box.
        '''
        
        # Refresh the version_table cursor
        output_db = DataAccess(output_db_location, dbdriver)
        
        version_table = DataAccess.get_table(output_db, version_table_name)
            
        # Get the scenario list for the select scenario combo boxes in the GUI/Results Review tab to display
        scenario_list = list()
        
#         # Get the current scenario list in the select review scenario combo box
#         displayed_scenarios = [combobox.itemText(i) for i in range(combobox.count())]
        
        combobox.clear()
        
        # Add the newly created scenario version to scenario_list
        for version in version_table:
#             if version.ScenarioName not in displayed_scenarios:
            scenario_list.append(str(version.ScenarioName))        
                    
        # add the new scenario list to the respective combo box
        if len(scenario_list) != 0:
            combobox.addItems(scenario_list)
            '''
            # The addItems action will automatically trigger the 'onChange' event of the combo box 
            # and call the respective event handling submodule to refresh the select variable combo box
            '''




    def refresh_review_tab_variable_combobox(self, single_variable, cross_section):
                    
        # Refresh the stat_table cursor
        output_db = DataAccess(output_db_location, dbdriver)
        
        stat_table = DataAccess.get_table(output_db, stat_table_name) 

        # Clear current select variable combo box
        self.cmb_select_review_variable.clear()
            
        # Get the variable list for the selected scenario        
        variable_list = list()

        for record in stat_table:
            if record.ScenarioVersion == self.cmb_select_review_scenario.currentText():
                if record.Variable not in variable_list:

                    if single_variable == True: # Single variable; exclude the composite indicators
                        if record.CompositeIndicator == 0 and record.MapLayer == 0:
                            variable_list.append(record.Variable)
                    else: # Multiple variables; include only the composite indicators
                        if record.CompositeIndicator == 1:
                            variable_list.append(record.Variable)


        # Proceed only when the variable list is not empty.
        '''
        Because any changes in the select scenario combo box will triger this submodule,
        and this may include the occasion of deleting a scenario,
        when nothing will be added into the variable list. 
        '''
        if len(variable_list) != 0:
                    
            # Sort the variables list
            variable_list.sort()
            
            # add the items to variable combo box
            self.cmb_select_review_variable.addItems(variable_list)


    

    def rbt_single_variable_time_series_ontoggled(self):
        self.refresh_review_tab_variable_combobox(single_variable = True, cross_section = False)
        
        
        
    def rbt_single_variable_cross_section_ontoggled(self):
        self.refresh_review_tab_variable_combobox(single_variable = True, cross_section = True)
        
        
        
    def rbt_multi_variable_time_series_ontoggled(self):
        self.refresh_review_tab_variable_combobox(single_variable = False, cross_section = False)



    def cmb_select_review_scenario_onchange(self):
        
        # Determine which variables to load according to "chart type" radio button selection.
        if self.rbt_single_variable_time_series.isChecked():
            self.refresh_review_tab_variable_combobox(single_variable = True, cross_section = False)
            
        elif self.rbt_single_variable_cross_section.isChecked():
            self.refresh_review_tab_variable_combobox(single_variable = True, cross_section = True)
            
        elif self.rbt_multi_variable_time_series.isChecked():
            self.refresh_review_tab_variable_combobox(single_variable = False, cross_section = False)
            
        else:
            # If no radio button is checked, just load the single variables.
            self.refresh_review_tab_variable_combobox(single_variable = True, cross_section = False)   



    def cmb_select_review_variable_onchange(self):
        
        # Refresh the stat_table cursor
        output_db = DataAccess(output_db_location, dbdriver)
        
        stat_table = DataAccess.get_table(output_db, stat_table_name) 
        
        # Get the time stamps list respective to the current variable
        year_list = list()

        for record in stat_table:
            if record.ScenarioVersion == self.cmb_select_review_scenario.currentText() \
            and record.Variable == self.cmb_select_review_variable.currentText():
                if record.StatDate not in year_list:
                    year_list.append(record.StatDate)
        
                
        # Update the plot start and end year spinboxes
        if len(year_list) != 0:     
            for stat in stat_table:
                if stat.ScenarioVersion == self.cmb_select_review_scenario.currentText() \
                and stat.Variable == self.cmb_select_review_variable.currentText():
                    if stat.StartingPointEffective == 0:            
                        self.sbx_select_plot_start_year.setProperty("value", min(year_list) + 1)
                        break
                    else:
                        self.sbx_select_plot_start_year.setProperty("value", min(year_list))
                        break
                    
            if self.rbt_single_variable_cross_section.isChecked():# Cross-section data
                self.sbx_select_plot_end_year.setProperty("value", 0)
                self.sbx_select_plot_end_year.setDisabled(True)     
            else: # Time series data 
                self.sbx_select_plot_end_year.setDisabled(False)
                self.sbx_select_plot_end_year.setProperty("value", max(year_list))
        



    def make_plot_space(self, widget):
        
        # Create a QVBoxLayout within the widget for embedding.
        self.lyt = QtGui.QVBoxLayout(widget)

        # Create a canvas instance
        self.mc = MplCanvas(widget)
        
        self.mc.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.mc.updateGeometry()

        
        # Create a matplotlib toolbar
        self.mpl_toolbar = NavigationToolbar(self.mc, widget)
           
        # Add the canvas and toolbar instances into the VBox Layout
        self.lyt.addWidget(self.mc)        
        self.lyt.addWidget(self.mpl_toolbar)    



    def btn_review_plot_onclick(self):
        '''
        The Plot button in the 'Results - Charts' Tab of the Control Panel
        '''

        # Note that data must be read from the database, rather than lists and dictionaries in the program, 
        # for users may need to make plots after the iteration (running of main simulation program).
        
        # Read the statistics table.
        output_db = DataAccess(output_db_location, dbdriver)
            
        stat_table = DataAccess.get_table(output_db, stat_table_name)
        
        # Get the plot title
        plot_title = str(self.cmb_select_review_variable.currentText())        
        
        
        # Define x and y axes units
        x_unit = 'Year'
        y_unit = ''

        # Determine the plot start year
        plot_start_year = self.sbx_select_plot_start_year.value()

        # Define the plot series list       
        plot_series_list = list()
        
        # Assign values for the variable lists        
        # Define a list containing the (x, y) data points (in the form of tuples)
        plot_xy_tuple_list = list()
        
        
        # Conditioning on the chart type
        if self.rbt_single_variable_time_series.isChecked():
            
            data_type = 'timeseries'
                
            for st in stat_table:            
                # Look only the records for the current scenario version
                if st.ScenarioVersion == self.cmb_select_review_scenario.currentText():
                    # Find the variable
                    if st.Variable == str(self.cmb_select_review_variable.currentText()):    
                        series_name = st.Variable
                        y_unit = st.StatUnit
                        
                        # Assign values for the variable
                        if st.StatDate >= plot_start_year and st.StatDate <= self.sbx_select_plot_end_year.value():                
                            plot_xy_tuple_list.append((st.StatDate, st.StatValue))
    
            # Sort the list by the order of the x dimension
            plot_xy_tuple_list.sort()
            
            # Make the x and y data for inputting to the plot submodule
            x_data = list()
            y_data_temp = list()
            
            for j in range(len(plot_xy_tuple_list)):
                x_data.append(plot_xy_tuple_list[j][0])
                y_data_temp.append(plot_xy_tuple_list[j][1])
            
            y_data = (series_name, y_data_temp)
            plot_series_list.append(y_data)
        
                
        elif self.rbt_multi_variable_time_series.isChecked():
            
            data_type = 'timeseries'
            
            # Make the plot series list
            for indicator in composite_indicators_dict:
                if self.cmb_select_review_variable.currentText() == indicator: 
                    
                    for variable in composite_indicators_dict[indicator]:     
                        plot_xy_tuple_list = list()
                        
                        for st in stat_table:
                            # Find the currently selected scenario
                            if st.Variable == variable \
                            and st.ScenarioVersion == self.cmb_select_review_scenario.currentText() \
                            and st.StatDate >= plot_start_year \
                            and st.StatDate <= self.sbx_select_plot_end_year.value():                          
                                
                                y_unit = st.StatUnit
                                plot_xy_tuple_list.append((st.StatDate, st.StatValue))
                                
                        plot_xy_tuple_list.sort()        
                
                        # Make the x and y data for inputting to the plot submodule
                        x_data = list()
                        y_data_temp = list()
                        
                        for j in range(len(plot_xy_tuple_list)):
                            x_data.append(plot_xy_tuple_list[j][0])
                            y_data_temp.append(plot_xy_tuple_list[j][1])
                        
                        y_data = (variable, y_data_temp)
                        
                        plot_series_list.append(y_data)


        elif self.rbt_single_variable_cross_section.isChecked():
            data_type = 'crosssection'

        
        
        else: # No plot data type radio button is checked
            # Show a Noticing Message
            msb = QMessageBox()
            msb.setText('Please select a plot data type        ')
            msb.setWindowTitle('SEEMS')
            msb.exec_()                
            

        # Draw the plot
        # First, remove any existing canvas contents
        self.lyt.removeWidget(self.mc)
        self.lyt.removeWidget(self.mpl_toolbar)
        
        # Then create a new canvas instance
        self.mc = MplCanvas(self.canvas_widget)
        
        self.mc.plot(data_type, plot_title, x_data, plot_series_list, x_unit, y_unit, self)



    def refresh_map_tab_map_layers(self):
        # Refresh the stat_table cursor
        output_db = DataAccess(output_db_location, dbdriver)
        
        stat_table = DataAccess.get_table(output_db, stat_table_name) 

        # Clear current select map layer combo box
        self.cmb_select_map_layer.clear()
        
        # Get the maps layer records in the stat table
        layer_list = list()

        for record in stat_table:
            if record.ScenarioVersion == self.cmb_select_map_scenario.currentText():
                if record.Variable not in layer_list and record.MapLayer == 1:
                    layer_list.append(record.Variable)

        if len(layer_list) != 0:
                    
            # Sort the variables list
            layer_list.sort()
                        
            # add the items to variable combo box
            self.cmb_select_map_layer.addItems(layer_list)



    def cmb_select_map_scenario_onchange(self):

        # Refresh the version_table cursor
        output_db = DataAccess(output_db_location, dbdriver)
        
        version_table = DataAccess.get_table(output_db, version_table_name)
        
        # Refresh the map layer selection combo box
        self.refresh_map_tab_map_layers()
        
        start_time = int()
        end_time = int()
        land_interval = int()
        
        # Refresh the map year selection slider bar
        for record in version_table:
            
            if record.ScenarioName == self.cmb_select_map_scenario.currentText():
                start_time = record.StartTime
                end_time = record.EndTime
                land_interval = record.LandInterval
                break

        if start_time != 0 and end_time != 0 and land_interval != 0:
            # Set up the year selection slider bar.
            self.sld_select_map_year.setMinimum(start_time)
            self.sld_select_map_year.setMaximum(end_time)
            self.sld_select_map_year.setSingleStep(land_interval)
            self.sld_select_map_year.setTickInterval(land_interval)
            
            # Set up the start year and end year labels that are attached to the slider bar.
            self.lbl_map_start_year.setText(str(start_time))
            self.lbl_map_end_year.setText(str(end_time))        

    
    
    
    def sld_select_map_year_onchange(self):

        output_db = DataAccess(output_db_location, dbdriver)
        
        version_table = DataAccess.get_table(output_db, version_table_name)

        start_time = int()
        end_time = int()
        land_interval = int()
 
        for record in version_table:
            if record.ScenarioName == self.cmb_select_map_scenario.currentText():
                start_time = record.StartTime
                end_time = record.EndTime
                land_interval = record.LandInterval
                break          
 
        # Update the map display
        if start_time != 0 and end_time != 0 and land_interval != 0:
                
            if self.sld_select_map_year.value() == start_time \
            or (self.sld_select_map_year.value() - start_time - 1) % land_interval == 0:
                # Update the current map year label display
                self.lbl_map_current_year.setText(str(self.sld_select_map_year.value()))
                
                # Update map display
                self.display_map(map_scenario=self.cmb_select_map_scenario.currentText(), 
                                 map_layer=self.cmb_select_map_layer.currentText(), 
                                 map_year=self.sld_select_map_year.value())

                    
     


    def btn_show_map_onclick(self):

        # Get the map display settings from the GUI inputs
        map_scenario = self.cmb_select_map_scenario.currentText()
        map_layer = self.cmb_select_map_layer.currentText()
        map_year = self.sld_select_map_year.value()
        
        # Display the image
        self.display_map(map_scenario, map_layer, map_year)


    
    
    def display_map(self, map_scenario, map_layer, map_year):
#         if map_layer == 'Land-use/land cover':
        layer = 'LandUse_'
        
        
        export_png_path = output_gis_path + '\\' + map_scenario + '\\export_maps_png'         
                
        landuse_layer_name = layer + map_scenario + '_' + str(map_year)
        new_map_image_path = str(export_png_path + '\\' + landuse_layer_name + '.png')
        
        self.map_layout.removeWidget(self.map.scrollArea)            
        self.map = ImageViewer(widget=self.map_display_widget, layout=self.map_layout, image_path=new_map_image_path, scalable=True)
        self.map_layout.addWidget(self.map.scrollArea)
        



#     def display_image(self, widget, path, scalable):
#         '''
#         Display a .PNG image in a predefined widget
#         widget: the parent widget to host the layout
#         layout: the layout to contain the image (QLabel widget)
#         path: path to the image to be displayed
#         scalable: boolean variable indicating whether to enable scaling of the displayed image
#         '''
#         # Create a QVBoxLayout within the widget for embedding
#         self.greeting_lyt = QtGui.QVBoxLayout(widget)
#         
#         # Call ImageViewer class to display the image
#         ImageViewer(widget=widget, layout=self.greeting_lyt, image_path=path, scalable=scalable)
        


    def action_menu_help_about(self):
        help_about_dialog = QtGui.QDialog()
        help_about_dialog_ui = Ui_SEEMS_help_about()
        help_about_dialog_ui.setupUi(help_about_dialog)
        help_about_dialog.exec_()
        
              
        
    def add_toolbar(self, frm_SEEMS_main):
        
        # Find the icons
        zoom_in_icon_location = str(icons_path + '\\ZoomIn.png')
        zoom_out_icon_location = str(icons_path + '\\ZoomOut.png')
        zoom_actual_size_icon_location = str(icons_path + '\\ZoomActualSize.png')

        # Define the actions
        action_zoom_in = QtGui.QAction(QtGui.QIcon(zoom_in_icon_location), 'Zoom In', frm_SEEMS_main)        
        action_zoom_out = QtGui.QAction(QtGui.QIcon(zoom_out_icon_location), 'Zoom Out', frm_SEEMS_main)
        action_zoom_actual_size = QtGui.QAction(QtGui.QIcon(zoom_actual_size_icon_location), 'Zoom Actual Size', frm_SEEMS_main)
        
        # Define the action events
        action_zoom_in.triggered.connect(self.zoom_in)
        action_zoom_out.triggered.connect(self.zoom_out)
        action_zoom_actual_size.triggered.connect(self.zoom_actual_size)
        
        # Add the toolbar
        self.toolbar = frm_SEEMS_main.addToolBar('Image View Controls')
        
        # Add actions into the toolbar
        self.toolbar.addAction(action_zoom_in)
        self.toolbar.addAction(action_zoom_out)
        self.toolbar.addAction(action_zoom_actual_size)        


    def zoom_in(self):
#         self.img.imageLabel.resize(3 * self.img.imageLabel.pixmap().size())
        self.map.zoomIn()
    
    def zoom_out(self):
        self.map.zoomOut()
    
    def zoom_actual_size(self):
        self.map.fitActualSize()
        
        

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None):
        fig = Figure()
        self.axes = fig.add_subplot(111)
        
        # Set if the axes is cleared every time plot() is called.
        self.axes.hold(True)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)




    def plot(self, data_type, plot_title, x_data, y_data, x_unit, y_unit, gui):
        '''
        Make a plot.
        
        data_type = 'crosssection' / 'timeseries'
        plot_title - the title of the plot.
        
        x_data - a simple list of numbers
        y_data - a list of tuples; each tuple is in the form of (series_name, [series_data_list]).

        x_unit - unit of the x axis
        y_unit - unit of the y axis       
        '''
        

        if data_type == 'timeseries':

            # Determine the chart type
            if gui.rbt_bar_chart.isChecked():                

                for i in range(len(y_data)):
                    if i == 0:
                        accu_series= numpy.subtract(y_data[i][1], y_data[i][1]) 
                    else:
                        accu_series= numpy.add(accu_series, y_data[i - 1][1]) 
                      
                    self.axes.bar(x_data, y_data[i][1], bottom = accu_series, color = numpy.random.rand(3,1), label = y_data[i][0])                        
                              
                # Set plot title
                self.axes.set_title(plot_title)
 
                # Set the x and y axes labels
                self.axes.set_xlabel(str(x_unit))
                self.axes.set_ylabel(str(y_unit))

#                 # Set the x and y axes ticks
#                 self.axes.set_xticklabels(time_stamps)
         
                # Set the legend and position the legend below the chart area                
                # Shrink current axis's height by 20% on the bottom
                box = self.axes.get_position()
                self.axes.set_position([box.x0, box.y0 + box.height * 0.2, box.width, box.height * 0.8])                
                # Put a legend below the x axis
                self.axes.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), fancybox=True, shadow=True, ncol=2)
                
                
            elif gui.rbt_line_chart.isChecked():
                for i in range(len(y_data)):                    
                    self.axes.plot(x_data, y_data[i][1], color = numpy.random.rand(3,1), label = y_data[i][0])                        
                             
                # Set plot title
                self.axes.set_title(plot_title)
 
                # Set the x and y axes labels
                self.axes.set_xlabel(str(x_unit))
                self.axes.set_ylabel(str(y_unit))             
         
                # Set the legend and position the legend below the chart area                
                # Shrink current axis's height by 20% on the bottom
                box = self.axes.get_position()
                self.axes.set_position([box.x0, box.y0 + box.height * 0.2, box.width, box.height * 0.8])                
                # Put a legend below the x axis
                self.axes.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), fancybox=True, shadow=True, ncol=2)
 
                  
            else: # Bar chart by default
                for i in range(len(y_data)):
                    if i == 0:
                        accu_series= numpy.subtract(y_data[i][1], y_data[i][1]) 
                    else:
                        accu_series= numpy.add(accu_series, y_data[i - 1][1]) 
                      
                    self.axes.bar(x_data, y_data[i][1], bottom = accu_series, color = numpy.random.rand(3,1), label = y_data[i][0])                        
                              
                # Set plot title
                self.axes.set_title(plot_title)
 
                # Set the x and y axes labels
                self.axes.set_xlabel(str(x_unit))
                self.axes.set_ylabel(str(y_unit))
         
                # Set the legend and position the legend below the chart area                
                # Shrink current axis's height by 20% on the bottom
                box = self.axes.get_position()
                self.axes.set_position([box.x0, box.y0 + box.height * 0.2, box.width, box.height * 0.8])                
                # Put a legend below the x axis
                self.axes.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), fancybox=True, shadow=True, ncol=2)
        
        
        elif data_type == 'crosssection':
            pass


        # Create a new toolbar
        gui.mpl_toolbar = NavigationToolbar(gui.mc, gui.canvas_widget)

#         # Add the widegts to the vbox
        gui.lyt.addWidget(gui.mc)
        gui.lyt.addWidget(gui.mpl_toolbar)




class Ui_SEEMS_help_about(object):
    def setupUi(self, SEEMS_help_about):
        SEEMS_help_about.setObjectName(_fromUtf8("SEEMS_help_about"))
        SEEMS_help_about.resize(475, 300)
        self.btn_OK = QtGui.QPushButton(SEEMS_help_about)
        self.btn_OK.setGeometry(QtCore.QRect(180, 250, 112, 34))
        self.btn_OK.setObjectName(_fromUtf8("btn_OK"))
        self.lbl_SEEMS_about = QtGui.QLabel(SEEMS_help_about)
        self.lbl_SEEMS_about.setGeometry(QtCore.QRect(10, 30, 451, 201))
        self.lbl_SEEMS_about.setObjectName(_fromUtf8("lbl_SEEMS_about"))

        self.retranslateUi(SEEMS_help_about)
        QtCore.QMetaObject.connectSlotsByName(SEEMS_help_about)
        
        '''
        Event handling
        '''
#         self.btn_OK.clicked.connect(self.btn_OK_onclicked)
        self.btn_OK.clicked.connect(SEEMS_help_about.close)


    def retranslateUi(self, SEEMS_help_about):
        SEEMS_help_about.setWindowTitle(_translate("SEEMS_help_about", "SEEMS - About", None))
        self.btn_OK.setText(_translate("SEEMS_help_about", "OK", None))
        self.lbl_SEEMS_about.setText(_translate("SEEMS_help_about", 
            "<html><head/><body><p align=\"center\">SEEMS - Socio-Econ-Ecosystem Multipurpose Simulator</p> \
            <p align=\"center\">v 0.9.0</p><p align=\"center\">Created by Liyan Xu and Hongmou Zhang</p> \
            <p align=\"center\">@MIT</p><p align=\"center\">2015.6.9</p></body></html>", None))





class ImageViewer(QtGui.QWidget):
    def __init__(self, widget, layout, image_path, scalable):
        super(ImageViewer, self).__init__()

#         self.printer = QtGui.QPrinter()
        self.createActions()
        
        self.scaleFactor = 1.0

        self.imageLabel = QtGui.QLabel()
        self.imageLabel.setBackgroundRole(QtGui.QPalette.Base)
        self.imageLabel.setPixmap(QtGui.QPixmap(image_path))

        
        if scalable == True:
            self.imageLabel.setScaledContents(True)
            
            self.scrollArea = QtGui.QScrollArea(widget)
            self.scrollArea.setBackgroundRole(QtGui.QPalette.Dark)
            self.scrollArea.setWidget(self.imageLabel)
            self.scrollArea.setAlignment(QtCore.Qt.AlignCenter)
                        
#             layout.addWidget(self.scrollArea)

        
        else:
            self.imageLabel.setScaledContents(False)
            self.imageLabel.setAlignment(QtCore.Qt.AlignCenter)           

#             layout.addWidget(self.imageLabel)





    def createActions(self):

        self.zoomInAct = QtGui.QAction("Zoom &In (25%)", self,
                shortcut="Ctrl++", enabled=False, triggered=self.zoomIn)

        self.zoomOutAct = QtGui.QAction("Zoom &Out (25%)", self,
                shortcut="Ctrl+-", enabled=False, triggered=self.zoomOut)

        self.normalSizeAct = QtGui.QAction("&Normal Size", self,
                shortcut="Ctrl+S", enabled=False, triggered=self.normalSize)

        self.fitToWindowAct = QtGui.QAction("&Fit to Window", self,
                enabled=False, checkable=True, shortcut="Ctrl+F",
                triggered=self.fitActualSize)
        
#         self.printAct = QtGui.QAction("&Print...", self, shortcut="Ctrl+P",
#                 enabled=False, triggered=self.print_)


    def zoomIn(self):
        self.scaleImage(1.25)

    def zoomOut(self):
        self.scaleImage(0.8)

    def normalSize(self):
        self.imageLabel.adjustSize()
        self.scaleFactor = 1.0

    def fitActualSize(self):
        fitToWindow = self.fitToWindowAct.isChecked()
        self.scrollArea.setWidgetResizable(fitToWindow)
        if not fitToWindow:
            self.normalSize()

        self.updateActions()

    def updateActions(self):
        self.zoomInAct.setEnabled(not self.fitToWindowAct.isChecked())
        self.zoomOutAct.setEnabled(not self.fitToWindowAct.isChecked())
        self.normalSizeAct.setEnabled(not self.fitToWindowAct.isChecked())

    def scaleImage(self, factor):
        self.scaleFactor *= factor
        self.imageLabel.resize(self.scaleFactor * self.imageLabel.pixmap().size())

        self.adjustScrollBar(self.scrollArea.horizontalScrollBar(), factor)
        self.adjustScrollBar(self.scrollArea.verticalScrollBar(), factor)

        self.zoomInAct.setEnabled(self.scaleFactor < 3.0)
        self.zoomOutAct.setEnabled(self.scaleFactor > 0.333)

    def adjustScrollBar(self, scrollBar, factor):
        scrollBar.setValue(int(factor * scrollBar.value() + ((factor - 1) * scrollBar.pageStep()/2)))
        

#     def print_(self):
#         dialog = QtGui.QPrintDialog(self.printer, self)
#         if dialog.exec_():
#             painter = QtGui.QPainter(self.printer)
#             rect = painter.viewport()
#             size = self.imageLabel.pixmap().size()
#             size.scale(rect.size(), QtCore.Qt.KeepAspectRatio)
#             painter.setViewport(rect.x(), rect.y(), size.width(), size.height())
#             painter.setWindow(self.imageLabel.pixmap().rect())
#             painter.drawPixmap(0, 0, self.imageLabel.pixmap())


