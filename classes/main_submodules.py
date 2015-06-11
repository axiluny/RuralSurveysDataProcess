'''
Created on Mar 26, 2015

@author: Liyan Xu
'''

from data_access import DataAccess
from society import Society
import statistics

from PyQt4 import QtCore, QtGui
from PyQt4.Qt import QMessageBox, QColorDialog
from PyQt4.QtCore import Qt

# from matplotlib.backends.backend_agg import FigureCanvas
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import numpy

'''
Globals, Constants, and other declarations.
'''


# dbname = 'C:/WolongRun/test_db/SimplifiedDB.mdb'
dbname = 'C:/WolongRun/WolongDB'
dbdriver = '{Microsoft Access Driver (*.mdb)}'
 
model_table_name = 'ModelTable'
household_table_name = 'HouseholdTable'
person_table_name = 'PersonTable'
land_table_name = 'LanduseTable'
business_sector_table_name = 'BusinessSectorTable'
policy_table_name = 'PolicyTable'
stat_table_name = 'StatTable'
version_table_name = 'VersionTable'
 
# # Rounds of iteration (years)
# simulation_depth = 5
#  
# # Starting and ending year of simulation
# start_year = 2015
# end_year = 2030

 
# Get the working database
db = DataAccess(dbname, dbdriver)
 
# Get the table pointers
model_table = DataAccess.get_table(db, model_table_name)
household_table = DataAccess.get_table(db, household_table_name)
person_table = DataAccess.get_table(db, person_table_name)
land_table = DataAccess.get_table(db, land_table_name)
business_sector_table = DataAccess.get_table(db, business_sector_table_name)
policy_table = DataAccess.get_table(db, policy_table_name)
stat_table = DataAccess.get_table(db, stat_table_name)
version_table = DataAccess.get_table(db, version_table_name)



# Make a dictionary of composite statistics indicators
composite_indicators_dict = {'1 Total Income by Sectors': ['IV-01 Total Agriculture Income', 'IV-02 Total Temp Job Income', 
                                'IV-03 Total Freight Trans Income', 'IV-04 Total Passenger Trans Income',
                                'IV-05 Total Lodging Income', 'IV-06 Total Renting Income'], 
                             '2 Employment by Sectors': ['IV-07 Agriculture Employment Ratio', 'IV-08 Temp Jobs Employment Ratio',
                                'IV-09 Freight Trans Employment Ratio', 'IV-10 Passenger Trans Employment Ratio',
                                'IV-11 Lodging Employment Ratio', 'IV-12 Renting Employment Ratio'], 
                             '3 Household Preference Types': ['II-01 Pref Labor_Risk Aversion HH Count', 'II-02 Pref Leisure_Risk Aversion HH Count',
                                'II-03 Pref Labor_Risk Appetite HH Count', 'II-04 Pref Leisure_Risk Appetite HH Count'], 
                             '4 Land-use/Land Cover Structure': ['V-01 Total Farmland Area', 'V-04 Total Construction Land Area',
                                'V-05 Total Grassland Area', 'V-06 Total Shrubbery Area', 'V-07 Total Mingled Forest Area']}




'''
user created main submodules 
'''



def create_scenario(db, scenario_name, model_table_name, model_table, hh_table_name, hh_table, 
                    pp_table_name, pp_table, land_table_name, land_table, 
                    business_sector_table_name, business_sector_table, policy_table_name, policy_table, 
                    stat_table_name, stat_table, simulation_depth, start_year, gui):

    # Set up an initial value (1%) when clicked so that the user knows it's running.
    refresh_progress_bar(simulation_depth, gui)

    # Insert a record in the VersionTable
    refresh_version_table(db, scenario_name, start_year, simulation_depth)
    
    # Initialize the society class: create society, household, person, etc instances
    soc = Society(db, model_table_name, model_table, hh_table_name, hh_table, pp_table_name, pp_table, 
                  land_table_name, land_table, business_sector_table_name, business_sector_table, 
                  policy_table_name, policy_table, stat_table_name, simulation_depth, stat_table, 
                  start_year)
    
    #Start simulation
    for iteration_count in range(simulation_depth):
        step_go(db, soc, start_year, iteration_count, scenario_name)

        # Set value for the progress bar
        refresh_progress_bar((iteration_count + 1) * 100, gui)







def step_go(database, society_instance, start_year, iteration_count, scenario_name):
    
    # If it's the first round of iteration, just get the stats and save the records to database
    # Else, proceed with the simulation in society.step_go, and then get the stats and save the records to database
    if iteration_count == 0:  
        # Do statistics and add records to statistics table in database
        add_stat_results(society_instance, scenario_name)
        
        # Then save updated tables in database
        save_results_to_db(database, society_instance, scenario_name)
        
    # Do the simulation
    Society.step_go(society_instance, start_year, iteration_count)

    add_stat_results(society_instance, scenario_name)
    
    save_results_to_db(database, society_instance, scenario_name)




def add_stat_results(society_instance, scenario_name):

    # Reset the statistics dictionary
    society_instance.stat_dict = dict()
    
    '''
    Single variables
    '''
    # Total population
    pp = statistics.StatClass()
    statistics.StatClass.get_population_count(pp, society_instance, scenario_name)
     
    # Household count
    hh = statistics.StatClass()
    statistics.StatClass.get_household_count(hh, society_instance, scenario_name)
     
    # Dissolved household count
    dhh = statistics.StatClass()
    statistics.StatClass.get_dissolved_household_count(dhh, society_instance, scenario_name)
    
    # Type 1 households count - Prefers labor/risk aversion
    ty1h = statistics.StatClass()
    statistics.StatClass.get_pref_labor_risk_aversion_hh_count(ty1h, society_instance, scenario_name)
    
    # Type 2 households count - Prefers leisure/risk aversion
    ty2h = statistics.StatClass()
    statistics.StatClass.get_pref_leisure_risk_aversion_hh_count(ty2h, society_instance, scenario_name)
    
    # Type 3 households count - Prefers labor/risk appetite
    ty3h = statistics.StatClass()
    statistics.StatClass.get_pref_labor_risk_appetite_hh_count(ty3h, society_instance, scenario_name)
    
    # Type 4 households count - Prefers leisure/risk appetite
    ty4h = statistics.StatClass()
    statistics.StatClass.get_pref_leisure_risk_appetite_hh_count(ty4h, society_instance, scenario_name)
    
    # Total net savings
    tns = statistics.StatClass()
    statistics.StatClass.get_total_net_savings(tns, society_instance, scenario_name)
    
    # Total cash savings
    tc = statistics.StatClass()
    statistics.StatClass.get_total_cash_savings(tc, society_instance, scenario_name)
     
    # Total debt
    tb = statistics.StatClass()
    statistics.StatClass.get_total_debt(tb, society_instance, scenario_name)    
     
    # Gross annual income
    gai = statistics.StatClass()
    statistics.StatClass.get_gross_annual_income(gai, society_instance, scenario_name)
    
    # Gross business revenues
    gbr = statistics.StatClass()
    statistics.StatClass.get_gross_business_revenues(gbr, society_instance, scenario_name)
    
    # Gross Compensational Revenues
    gcr = statistics.StatClass()
    statistics.StatClass.get_gross_compensational_revenues(gcr, society_instance, scenario_name)
    
    # Annual income per person
    aipp = statistics.StatClass()
    statistics.StatClass.get_annual_income_per_person(aipp, society_instance, scenario_name)
    
    # Annual income per household
    aiph = statistics.StatClass()
    statistics.StatClass.get_annual_income_per_household(aiph, society_instance, scenario_name)
    
    # Trucks count
    trk = statistics.StatClass()
    statistics.StatClass.get_trucks_count(trk, society_instance, scenario_name)
    
    # Minibuses count
    mnb = statistics.StatClass()
    statistics.StatClass.get_minibuses_count(mnb, society_instance, scenario_name)
    
    # Total agriculture income
    agi = statistics.StatClass()
    statistics.StatClass.get_total_agriculture_income(agi, society_instance, scenario_name)
     
    # Total temporary job income
    tji = statistics.StatClass()
    statistics.StatClass.get_total_tempjob_income(tji, society_instance, scenario_name)
     
    # Total freight transportation income
    fti = statistics.StatClass()
    statistics.StatClass.get_total_freighttrans_income(fti, society_instance, scenario_name)
     
    # Total passenger transportation income
    pti = statistics.StatClass()
    statistics.StatClass.get_total_passengertrans_income(pti, society_instance, scenario_name)
     
    # Total lodging income
    lgi = statistics.StatClass()
    statistics.StatClass.get_total_lodging_income(lgi, society_instance, scenario_name)
         
    # Total renting income
    rti = statistics.StatClass()
    statistics.StatClass.get_total_renting_income(rti, society_instance, scenario_name)    
    
    # Agriculture Employment Ratio
    ager = statistics.StatClass()
    statistics.StatClass.get_agriculture_employment_ratio(ager, society_instance, scenario_name)
    
    # Temporary Jobs Employment Ratio
    tjer = statistics.StatClass()
    statistics.StatClass.get_tempjob_employment_ratio(tjer, society_instance, scenario_name)
    
    # Freight transportation employment ratio
    fter = statistics.StatClass()
    statistics.StatClass.get_freighttrans_employment_ratio(fter, society_instance, scenario_name)
    
    # Passenger transportation employment ratio
    pter = statistics.StatClass()
    statistics.StatClass.get_passengertrans_employment_ratio(pter, society_instance, scenario_name)
    
    # Lodging employment ratio
    lger = statistics.StatClass()
    statistics.StatClass.get_lodging_employment_ratio(lger, society_instance, scenario_name)
    
    # Renting employment ratio
    rter = statistics.StatClass()
    statistics.StatClass.get_renting_employment_ratio(rter, society_instance, scenario_name)
    
    # Total farmland area
    tfa = statistics.StatClass()
    statistics.StatClass.get_total_farmland_area(tfa, society_instance, scenario_name)
    
    # Total abandoned farmland area
    tafa = statistics.StatClass()
    statistics.StatClass.get_abandoned_farmland_area(tafa, society_instance, scenario_name)
    
    # Total Farmland to Forest Area
    tftfa = statistics.StatClass()
    statistics.StatClass.get_farmland_to_forest_area(tftfa, society_instance, scenario_name)
    
    # Total construction land area
    tcla = statistics.StatClass()
    statistics.StatClass.get_total_construction_land_area(tcla, society_instance, scenario_name)
    
    # Total grassland area
    tgla = statistics.StatClass()
    statistics.StatClass.get_total_grassland_area(tgla, society_instance, scenario_name)
    
    # Total shrubbery land area
    tsla = statistics.StatClass()
    statistics.StatClass.get_total_shrubbery_area(tsla, society_instance, scenario_name)
    
    # Total mingled forest area
    tmfa = statistics.StatClass()
    statistics.StatClass.get_total_mingled_forest_area(tmfa, society_instance, scenario_name)
    
    
    
    '''
    Composite indicators
    '''
    # Sectors income structure
    sis = statistics.StatClass()
    statistics.StatClass.get_sectors_income_structure(sis, society_instance, scenario_name)

    # Sectors employment structure
    ses = statistics.StatClass()
    statistics.StatClass.get_sectors_employment_structure(ses, society_instance, scenario_name)
    
    # Household preference type structure
    hpts = statistics.StatClass()
    statistics.StatClass.get_household_preference_type_structures(hpts, society_instance, scenario_name)
    
    # Land-use/Land cover structure
    lulcs = statistics.StatClass()
    statistics.StatClass.get_landuse_landcover_structures(lulcs, society_instance, scenario_name)
    
    
    
def save_results_to_db(database, society_instance, scenario_name):
    
    # Determine household, people,and land table names
    # Format: Scenario_name + household/people/land
    new_hh_table_name = scenario_name + '_households'
    new_pp_table_name = scenario_name + '_persons'
    new_land_table_name = scenario_name + '_land'
    
    stat_table_name = 'StatTable'
    
        
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
            DataAccess.insert_record_to_table(database, insert_table_order)
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
            DataAccess.insert_record_to_table(database, insert_table_order)
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
                DataAccess.insert_record_to_table(database, insert_table_order)
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
                DataAccess.insert_record_to_table(database, insert_table_order)
            DataAccess.db_commit(database)  





    # Saving the Land table in the database
      
    # If the table with that name does not exist in the database
    # i.e. in the first round of iteration,
    # Then first create a new table, then insert the records.
    # Otherwise, just find the right table, and then insert the records.
    if DataAccess.get_table(database, new_land_table_name) == None: # This is most indecent... see dataaccess for details
     
        # Create a new Land table from the variable list of Land Class
        new_land_table_formatter = '('
        for var in society_instance.land_var_list:
            # Add person variables to the formatter
            new_land_table_formatter += var[0] + ' ' + var[2] + ','  
        new_land_table_formatter = new_land_table_formatter[0: len(new_land_table_formatter) - 1] + ')'
     
        create_table_order = "create table " + new_land_table_name +''+ new_land_table_formatter
        DataAccess.create_table(database, create_table_order)
        DataAccess.db_commit(database)


        # Then insert all land parcels into the new table
        # InsertContent = ''
        for OBJECTID_1 in society_instance.land_dict:
            # Make the insert values for this land parcel
            new_land_record_content = '('
            for var in society_instance.land_var_list:
                # If the value is string, add quotes
                if var[2] == 'VARCHAR' and getattr(society_instance.land_dict[OBJECTID_1], var[0]) != None: 
                    new_land_record_content += '\''+ unicode(getattr(society_instance.land_dict[OBJECTID_1], var[0]))+ '\','
                else:
                    new_land_record_content += unicode(getattr(society_instance.land_dict[OBJECTID_1], var[0]))+ ','
            # Change the ending comma to a closing parenthesis
            new_land_record_content = new_land_record_content[0:len(new_land_record_content)-1] + ')'
            # Insert one land parcel record
            insert_table_order = "insert into " + new_land_table_name + ' values ' + new_land_record_content.replace('None','Null') +';'
            DataAccess.insert_record_to_table(database, insert_table_order)
        DataAccess.db_commit(database)  
 
     
    else:
        # Just insert all land parcels into the new table
        # InsertContent = ''
        for OBJECTID_1 in society_instance.land_dict:
            # Make the insert values for this household
            new_land_record_content = '('
            for var in society_instance.land_var_list:
                # If the value is string, add quotes
                if var[2] == 'VARCHAR' and getattr(society_instance.land_dict[OBJECTID_1], var[0]) != None: 
                    new_land_record_content += '\''+ unicode(getattr(society_instance.land_dict[OBJECTID_1], var[0]))+ '\','
                else:
                    new_land_record_content += unicode(getattr(society_instance.land_dict[OBJECTID_1], var[0]))+ ','
            # Change the ending comma to a closing parenthesis
            new_land_record_content = new_land_record_content[0:len(new_land_record_content)-1] + ')'
            # Insert one land parcel record
            insert_table_order = "insert into " + new_land_table_name + ' values ' + new_land_record_content.replace('None','Null') +';'
            DataAccess.insert_record_to_table(database, insert_table_order)
        DataAccess.db_commit(database)        





    # Saving the Statistics table in the database  
      
    # The data table "StatTable" should be pre-created in the database
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
        DataAccess.insert_record_to_table(database, insert_table_order)
    DataAccess.db_commit(database)           



def remove_scenario_version_from_database(version_name, database, gui):
    '''
    Remove a scenario version from the VersionTable;
    Also remove all the statistics records related to this scenario version in the StatTable;
    Also drop the households, persons, and land tables related to this scenario version in the database.
    '''

    # Delete the scenario version's record from the VersionTable
    delete_version_record_order = "delete from " + version_table_name + " where ScenarioName = '" + version_name + "'"
    DataAccess.delete_record_from_table(database, delete_version_record_order)
    DataAccess.db_commit(database)


    # Delete the related statistics from the StatTable 
    delete_stat_record_order = "delete from " + stat_table_name + " where ScenarioVersion = '" + version_name + "'"
    DataAccess.delete_record_from_table(database, delete_stat_record_order)
    DataAccess.db_commit(database)    
    
    
    # Drop the tables
    drop_hh_table_order = 'drop table ' + version_name + '_households'
    DataAccess.drop_table(database, drop_hh_table_order)
    drop_pp_table_order = 'drop table ' + version_name + '_persons'
    DataAccess.drop_table(database, drop_pp_table_order)
    drop_land_table_order = 'drop table ' + version_name + '_land'
    DataAccess.drop_table(database, drop_land_table_order)
    
    DataAccess.db_commit(database)


def refresh_progress_bar(progress, gui):
    gui.prb_progressBar.setValue(progress)



def refresh_version_table(database, scenario_name, start_year, simulation_depth):
    order = "insert into VersionTable values ('" + scenario_name +"', '', " + str(start_year) + ', ' + str(start_year + simulation_depth) +");"
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
        The followings are mainly PyQt auto-generated codes from the Qt Designer.
        With some user editions.
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
        self.tab_controlpanel.setMaximumSize(QtCore.QSize(550, 16777215))
        self.tab_controlpanel.setObjectName(_fromUtf8("tab_controlpanel"))
        
        # First tab -  Scenarios Setup
        self.scenarios_setup = QtGui.QWidget()
        self.scenarios_setup.setObjectName(_fromUtf8("scenarios_setup"))
        self.verticalLayout_6 = QtGui.QVBoxLayout(self.scenarios_setup)
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.formLayout_3 = QtGui.QFormLayout()
        self.formLayout_3.setObjectName(_fromUtf8("formLayout_3"))
        self.lbl_input_scenario_name = QtGui.QLabel(self.scenarios_setup)
        self.lbl_input_scenario_name.setObjectName(_fromUtf8("lbl_input_scenario_name"))
        self.formLayout_3.setWidget(0, QtGui.QFormLayout.LabelRole, self.lbl_input_scenario_name)
        self.txt_input_scenario_name = QtGui.QLineEdit(self.scenarios_setup)
        self.txt_input_scenario_name.setObjectName(_fromUtf8("txt_input_scenario_name"))
        self.formLayout_3.setWidget(0, QtGui.QFormLayout.FieldRole, self.txt_input_scenario_name)
        self.verticalLayout_6.addLayout(self.formLayout_3)
        self.gbx_set_simulation_period = QtGui.QGroupBox(self.scenarios_setup)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gbx_set_simulation_period.sizePolicy().hasHeightForWidth())
        self.gbx_set_simulation_period.setSizePolicy(sizePolicy)
        self.gbx_set_simulation_period.setMaximumSize(QtCore.QSize(16777215, 75))
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
        self.verticalLayout_6.addWidget(self.gbx_set_simulation_period)
        spacerItem = QtGui.QSpacerItem(20, 16777215, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_6.addItem(spacerItem)
        self.btn_start_simulation = QtGui.QPushButton(self.scenarios_setup)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_start_simulation.sizePolicy().hasHeightForWidth())
        self.btn_start_simulation.setSizePolicy(sizePolicy)
        self.btn_start_simulation.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.btn_start_simulation.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.btn_start_simulation.setObjectName(_fromUtf8("btn_start_simulation"))
        self.verticalLayout_6.addWidget(self.btn_start_simulation)
        self.prb_progressBar = QtGui.QProgressBar(self.scenarios_setup)
        self.prb_progressBar.setProperty("value", 0)
        self.prb_progressBar.setObjectName(_fromUtf8("prb_progressBar"))
        self.verticalLayout_6.addWidget(self.prb_progressBar)
        self.tab_controlpanel.addTab(self.scenarios_setup, _fromUtf8(""))



        # Second tab - Results Review
        self.results_review = QtGui.QWidget()
        self.results_review.setObjectName(_fromUtf8("results_review"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.results_review)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.formLayout_2 = QtGui.QFormLayout()
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.lbl_select_review_scenario = QtGui.QLabel(self.results_review)
        self.lbl_select_review_scenario.setObjectName(_fromUtf8("lbl_select_review_scenario"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.lbl_select_review_scenario)
        self.cmb_select_review_scenario = QtGui.QComboBox(self.results_review)
        self.cmb_select_review_scenario.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContentsOnFirstShow)
        self.cmb_select_review_scenario.setObjectName(_fromUtf8("cmb_select_review_scenario"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.FieldRole, self.cmb_select_review_scenario)
        self.lbl_select_review_variable = QtGui.QLabel(self.results_review)
        self.lbl_select_review_variable.setObjectName(_fromUtf8("lbl_select_review_variable"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.lbl_select_review_variable)
        self.cmb_select_review_variable = QtGui.QComboBox(self.results_review)
        self.cmb_select_review_variable.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContentsOnFirstShow)
        self.cmb_select_review_variable.setObjectName(_fromUtf8("cmb_select_review_variable"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.FieldRole, self.cmb_select_review_variable)
        self.verticalLayout_4.addLayout(self.formLayout_2)
        self.gbx_plot_period = QtGui.QGroupBox(self.results_review)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gbx_plot_period.sizePolicy().hasHeightForWidth())
        self.gbx_plot_period.setSizePolicy(sizePolicy)
        self.gbx_plot_period.setMaximumSize(QtCore.QSize(16777215, 75))
        self.gbx_plot_period.setObjectName(_fromUtf8("gbx_plot_period"))
        self.horizontalLayout_6 = QtGui.QHBoxLayout(self.gbx_plot_period)
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.formLayout_7 = QtGui.QFormLayout()
        self.formLayout_7.setObjectName(_fromUtf8("formLayout_7"))
        self.lbl_select_review_start_year = QtGui.QLabel(self.gbx_plot_period)
        self.lbl_select_review_start_year.setObjectName(_fromUtf8("lbl_select_review_start_year"))
        self.formLayout_7.setWidget(0, QtGui.QFormLayout.LabelRole, self.lbl_select_review_start_year)
        self.sbx_select_review_start_year = QtGui.QSpinBox(self.gbx_plot_period)
        self.sbx_select_review_start_year.setMaximum(3000)
        self.sbx_select_review_start_year.setProperty("value", 0)
        self.sbx_select_review_start_year.setObjectName(_fromUtf8("sbx_select_review_start_year"))
        self.formLayout_7.setWidget(0, QtGui.QFormLayout.FieldRole, self.sbx_select_review_start_year)
        self.horizontalLayout_6.addLayout(self.formLayout_7)
        self.formLayout_8 = QtGui.QFormLayout()
        self.formLayout_8.setObjectName(_fromUtf8("formLayout_8"))
        self.lbl_select_review_end_year = QtGui.QLabel(self.gbx_plot_period)
        self.lbl_select_review_end_year.setObjectName(_fromUtf8("lbl_select_review_end_year"))
        self.formLayout_8.setWidget(0, QtGui.QFormLayout.LabelRole, self.lbl_select_review_end_year)
        self.sbx_select_review_end_year = QtGui.QSpinBox(self.gbx_plot_period)
        self.sbx_select_review_end_year.setMaximum(3000)
        self.sbx_select_review_end_year.setProperty("value", 0)
        self.sbx_select_review_end_year.setObjectName(_fromUtf8("sbx_select_review_end_year"))
        self.formLayout_8.setWidget(0, QtGui.QFormLayout.FieldRole, self.sbx_select_review_end_year)
        self.horizontalLayout_6.addLayout(self.formLayout_8)
        self.verticalLayout_4.addWidget(self.gbx_plot_period)
        self.gbx_result_review_plot_type = QtGui.QGroupBox(self.results_review)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gbx_result_review_plot_type.sizePolicy().hasHeightForWidth())
        self.gbx_result_review_plot_type.setSizePolicy(sizePolicy)
        self.gbx_result_review_plot_type.setMaximumSize(QtCore.QSize(16777215, 75))
        self.gbx_result_review_plot_type.setObjectName(_fromUtf8("gbx_result_review_plot_type"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.gbx_result_review_plot_type)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.rdbtn_bar_chart = QtGui.QRadioButton(self.gbx_result_review_plot_type)
        self.rdbtn_bar_chart.setObjectName(_fromUtf8("rdbtn_bar_chart"))
        self.horizontalLayout_4.addWidget(self.rdbtn_bar_chart)
        self.rdbtn_line_chart = QtGui.QRadioButton(self.gbx_result_review_plot_type)
        self.rdbtn_line_chart.setObjectName(_fromUtf8("rdbtn_line_chart"))
        self.horizontalLayout_4.addWidget(self.rdbtn_line_chart)
        self.verticalLayout_4.addWidget(self.gbx_result_review_plot_type)
        spacerItem1 = QtGui.QSpacerItem(20, 16777215, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem1)
        self.btn_review_plot = QtGui.QPushButton(self.results_review)
        self.btn_review_plot.setObjectName(_fromUtf8("btn_review_plot"))
        self.verticalLayout_4.addWidget(self.btn_review_plot)
        self.tab_controlpanel.addTab(self.results_review, _fromUtf8(""))


        # Third tab - Data Analysis
        self.data_analysis = QtGui.QWidget()
        self.data_analysis.setObjectName(_fromUtf8("data_analysis"))
        self.verticalLayout = QtGui.QVBoxLayout(self.data_analysis)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gbx_cross_section_ana = QtGui.QGroupBox(self.data_analysis)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gbx_cross_section_ana.sizePolicy().hasHeightForWidth())
        self.gbx_cross_section_ana.setSizePolicy(sizePolicy)
        self.gbx_cross_section_ana.setObjectName(_fromUtf8("gbx_cross_section_ana"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.gbx_cross_section_ana)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.formLayout_9 = QtGui.QFormLayout()
        self.formLayout_9.setObjectName(_fromUtf8("formLayout_9"))
        self.lbl_select_cross_section_analysis_scenario = QtGui.QLabel(self.gbx_cross_section_ana)
        self.lbl_select_cross_section_analysis_scenario.setObjectName(_fromUtf8("lbl_select_cross_section_analysis_scenario"))
        self.formLayout_9.setWidget(0, QtGui.QFormLayout.LabelRole, self.lbl_select_cross_section_analysis_scenario)
        self.cmb_select_cross_section_analysis_scenario = QtGui.QComboBox(self.gbx_cross_section_ana)
        self.cmb_select_cross_section_analysis_scenario.setObjectName(_fromUtf8("cmb_select_cross_section_analysis_scenario"))
        self.formLayout_9.setWidget(0, QtGui.QFormLayout.FieldRole, self.cmb_select_cross_section_analysis_scenario)
        self.lbl_select_cross_section_analysis_variable = QtGui.QLabel(self.gbx_cross_section_ana)
        self.lbl_select_cross_section_analysis_variable.setObjectName(_fromUtf8("lbl_select_cross_section_analysis_variable"))
        self.formLayout_9.setWidget(1, QtGui.QFormLayout.LabelRole, self.lbl_select_cross_section_analysis_variable)
        self.cmb_select_cross_section_analysis_variable = QtGui.QComboBox(self.gbx_cross_section_ana)
        self.cmb_select_cross_section_analysis_variable.setObjectName(_fromUtf8("cmb_select_cross_section_analysis_variable"))
        self.formLayout_9.setWidget(1, QtGui.QFormLayout.FieldRole, self.cmb_select_cross_section_analysis_variable)
        self.lbl_select_cross_section_analysis_year = QtGui.QLabel(self.gbx_cross_section_ana)
        self.lbl_select_cross_section_analysis_year.setObjectName(_fromUtf8("lbl_select_cross_section_analysis_year"))
        self.formLayout_9.setWidget(2, QtGui.QFormLayout.LabelRole, self.lbl_select_cross_section_analysis_year)
        self.sbx_select_cross_section_analysis_year = QtGui.QSpinBox(self.gbx_cross_section_ana)
        self.sbx_select_cross_section_analysis_year.setMaximum(3000)
        self.sbx_select_cross_section_analysis_year.setProperty("value", 0)
        self.sbx_select_cross_section_analysis_year.setObjectName(_fromUtf8("sbx_select_cross_section_analysis_year"))
        self.formLayout_9.setWidget(2, QtGui.QFormLayout.FieldRole, self.sbx_select_cross_section_analysis_year)
        self.verticalLayout_2.addLayout(self.formLayout_9)
        self.gbx_cross_section_plot_type = QtGui.QGroupBox(self.gbx_cross_section_ana)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gbx_cross_section_plot_type.sizePolicy().hasHeightForWidth())
        self.gbx_cross_section_plot_type.setSizePolicy(sizePolicy)
        self.gbx_cross_section_plot_type.setMaximumSize(QtCore.QSize(16777215, 70))
        self.gbx_cross_section_plot_type.setObjectName(_fromUtf8("gbx_cross_section_plot_type"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.gbx_cross_section_plot_type)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.rdbtn_histogram = QtGui.QRadioButton(self.gbx_cross_section_plot_type)
        self.rdbtn_histogram.setObjectName(_fromUtf8("rdbtn_histogram"))
        self.horizontalLayout_2.addWidget(self.rdbtn_histogram)
        self.verticalLayout_2.addWidget(self.gbx_cross_section_plot_type)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem2)
        self.btn_cross_section_analysis_plot = QtGui.QPushButton(self.gbx_cross_section_ana)
        self.btn_cross_section_analysis_plot.setObjectName(_fromUtf8("btn_cross_section_analysis_plot"))
        self.verticalLayout_2.addWidget(self.btn_cross_section_analysis_plot)
        self.verticalLayout.addWidget(self.gbx_cross_section_ana)
        self.gbx_time_series_ana = QtGui.QGroupBox(self.data_analysis)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gbx_time_series_ana.sizePolicy().hasHeightForWidth())
        self.gbx_time_series_ana.setSizePolicy(sizePolicy)
        self.gbx_time_series_ana.setObjectName(_fromUtf8("gbx_time_series_ana"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.gbx_time_series_ana)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.formLayout_4 = QtGui.QFormLayout()
        self.formLayout_4.setObjectName(_fromUtf8("formLayout_4"))
        self.lbl_select_time_series_analysis_scenario = QtGui.QLabel(self.gbx_time_series_ana)
        self.lbl_select_time_series_analysis_scenario.setObjectName(_fromUtf8("lbl_select_time_series_analysis_scenario"))
        self.formLayout_4.setWidget(0, QtGui.QFormLayout.LabelRole, self.lbl_select_time_series_analysis_scenario)
        self.cmb_select_time_series_analysis_scenario = QtGui.QComboBox(self.gbx_time_series_ana)
        self.cmb_select_time_series_analysis_scenario.setObjectName(_fromUtf8("cmb_select_time_series_analysis_scenario"))
        self.formLayout_4.setWidget(0, QtGui.QFormLayout.FieldRole, self.cmb_select_time_series_analysis_scenario)
        self.lbl_select_time_series_analysis_variable = QtGui.QLabel(self.gbx_time_series_ana)
        self.lbl_select_time_series_analysis_variable.setObjectName(_fromUtf8("lbl_select_time_series_analysis_variable"))
        self.formLayout_4.setWidget(1, QtGui.QFormLayout.LabelRole, self.lbl_select_time_series_analysis_variable)
        self.cmb_select_time_series_analysis_variable = QtGui.QComboBox(self.gbx_time_series_ana)
        self.cmb_select_time_series_analysis_variable.setObjectName(_fromUtf8("cmb_select_time_series_analysis_variable"))
        self.formLayout_4.setWidget(1, QtGui.QFormLayout.FieldRole, self.cmb_select_time_series_analysis_variable)
        self.verticalLayout_3.addLayout(self.formLayout_4)
        self.gbx_time_series_plot_period = QtGui.QGroupBox(self.gbx_time_series_ana)
        self.gbx_time_series_plot_period.setObjectName(_fromUtf8("gbx_time_series_plot_period"))
        self.horizontalLayout_5 = QtGui.QHBoxLayout(self.gbx_time_series_plot_period)
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.formLayout_5 = QtGui.QFormLayout()
        self.formLayout_5.setObjectName(_fromUtf8("formLayout_5"))
        self.lbl_select_time_series_analysis_start_year = QtGui.QLabel(self.gbx_time_series_plot_period)
        self.lbl_select_time_series_analysis_start_year.setObjectName(_fromUtf8("lbl_select_time_series_analysis_start_year"))
        self.formLayout_5.setWidget(0, QtGui.QFormLayout.LabelRole, self.lbl_select_time_series_analysis_start_year)
        self.sbx_select_time_series_analysis_start_year = QtGui.QSpinBox(self.gbx_time_series_plot_period)
        self.sbx_select_time_series_analysis_start_year.setMaximum(3000)
        self.sbx_select_time_series_analysis_start_year.setProperty("value", 0)
        self.sbx_select_time_series_analysis_start_year.setObjectName(_fromUtf8("sbx_select_time_series_analysis_start_year"))
        self.formLayout_5.setWidget(0, QtGui.QFormLayout.FieldRole, self.sbx_select_time_series_analysis_start_year)
        self.horizontalLayout_5.addLayout(self.formLayout_5)
        self.formLayout_6 = QtGui.QFormLayout()
        self.formLayout_6.setObjectName(_fromUtf8("formLayout_6"))
        self.lbl_select_time_series_analysis_end_year = QtGui.QLabel(self.gbx_time_series_plot_period)
        self.lbl_select_time_series_analysis_end_year.setObjectName(_fromUtf8("lbl_select_time_series_analysis_end_year"))
        self.formLayout_6.setWidget(0, QtGui.QFormLayout.LabelRole, self.lbl_select_time_series_analysis_end_year)
        self.sbx_select_time_series_analysis_end_year = QtGui.QSpinBox(self.gbx_time_series_plot_period)
        self.sbx_select_time_series_analysis_end_year.setMaximum(3000)
        self.sbx_select_time_series_analysis_end_year.setProperty("value", 0)
        self.sbx_select_time_series_analysis_end_year.setObjectName(_fromUtf8("sbx_select_time_series_analysis_end_year"))
        self.formLayout_6.setWidget(0, QtGui.QFormLayout.FieldRole, self.sbx_select_time_series_analysis_end_year)
        self.horizontalLayout_5.addLayout(self.formLayout_6)
        self.verticalLayout_3.addWidget(self.gbx_time_series_plot_period)
        self.gbx_time_series_plot_type = QtGui.QGroupBox(self.gbx_time_series_ana)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gbx_time_series_plot_type.sizePolicy().hasHeightForWidth())
        self.gbx_time_series_plot_type.setSizePolicy(sizePolicy)
        self.gbx_time_series_plot_type.setMaximumSize(QtCore.QSize(16777215, 75))
        self.gbx_time_series_plot_type.setObjectName(_fromUtf8("gbx_time_series_plot_type"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.gbx_time_series_plot_type)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.rdbtn_stacked_bars_chart = QtGui.QRadioButton(self.gbx_time_series_plot_type)
        self.rdbtn_stacked_bars_chart.setObjectName(_fromUtf8("rdbtn_stacked_bars_chart"))
        self.horizontalLayout_3.addWidget(self.rdbtn_stacked_bars_chart)
        self.rdbtn_multiple_line_chart = QtGui.QRadioButton(self.gbx_time_series_plot_type)
        self.rdbtn_multiple_line_chart.setObjectName(_fromUtf8("rdbtn_multiple_line_chart"))
        self.horizontalLayout_3.addWidget(self.rdbtn_multiple_line_chart)
        self.verticalLayout_3.addWidget(self.gbx_time_series_plot_type)
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem3)
        self.btn_time_series_analysis_plot = QtGui.QPushButton(self.gbx_time_series_ana)
        self.btn_time_series_analysis_plot.setObjectName(_fromUtf8("btn_time_series_analysis_plot"))
        self.verticalLayout_3.addWidget(self.btn_time_series_analysis_plot)
        self.verticalLayout.addWidget(self.gbx_time_series_ana)
        self.tab_controlpanel.addTab(self.data_analysis, _fromUtf8(""))
        self.horizontalLayout.addWidget(self.tab_controlpanel)
        

        # A generic widget as the container of the matplotlib canvas, defined later.
        self.canvaswidget = QtGui.QWidget(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.canvaswidget.sizePolicy().hasHeightForWidth())
        self.canvaswidget.setSizePolicy(sizePolicy)
        self.canvaswidget.setObjectName(_fromUtf8("canvaswidget"))
        self.horizontalLayout.addWidget(self.canvaswidget)
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
        The following lines in this submodule are developers added codes
        '''
              
        # Create a QVBoxLayout within the canvas widget, such that the canvas embeds in the main window frame
        self.lyt = QtGui.QVBoxLayout(self.canvaswidget)

        # Create a canvas instance
        self.mc = MplCanvas(self.canvaswidget)
        
        # Create a matplotlib toolbar
        self.mpl_toolbar = NavigationToolbar(self.mc, self.canvaswidget)
           
        # Add the canvas and toolbar instances into the VBox Layout
        self.lyt.addWidget(self.mc)        
        self.lyt.addWidget(self.mpl_toolbar)        

        '''
        #         Another way to create a canvas, without introducing a seperately defined class
        #         # create a canvas
        #         fig = Figure()        
        #         self.mc = FigureCanvas(fig)
        # 
        #         self.mc.axes = fig.add_subplot(111)
        #         self.mc.axes.hold(True) 
        # 
        #         self.mc.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        #         self.mc.updateGeometry()          
        '''
        
        # Automatically add a default new scenario name
        self.add_default_new_scenario_name()
         
  
        # Events handling 
        self.btn_review_plot.clicked.connect(self.btn_review_plot_onclick)
        self.btn_time_series_analysis_plot.clicked.connect(self.btn_time_series_plot_onclick)
        
        self.cmb_select_review_scenario.currentIndexChanged.connect(self.cmb_select_scenario_onchange)
        self.cmb_select_cross_section_analysis_scenario.currentIndexChanged.connect(self.cmb_select_cross_section_analysis_scenario_onchange)
        self.cmb_select_time_series_analysis_scenario.currentIndexChanged.connect(self.cmb_select_time_series_analysis_scenario_onchange)
                 
        self.btn_start_simulation.clicked.connect(self.btn_start_simulation_onclick)
        
        self.actionAbout.triggered.connect(self.action_menu_help_about)
        
        # Initiate the results review and data analysis panels
        self.refresh_review_panel()
        self.refresh_analysis_panel()
        
  
  
    def retranslateUi(self, frm_SEEMS_main):
        frm_SEEMS_main.setWindowTitle(_translate("frm_SEEMS_main", "SEEMS  -  Socio-Econ-Ecosystem Multipurpose Simulator", None))
        self.lbl_input_scenario_name.setText(_translate("frm_SEEMS_main", "Scenario Name:", None))
        self.gbx_set_simulation_period.setTitle(_translate("frm_SEEMS_main", "Set Simulation Period", None))
        self.lbl_set_simulation_start_year.setText(_translate("frm_SEEMS_main", "Start Year:", None))
        self.lbl_set_simulation_end_year.setText(_translate("frm_SEEMS_main", "End Year:", None))
        self.btn_start_simulation.setText(_translate("frm_SEEMS_main", "Start Simulation", None))
        self.tab_controlpanel.setTabText(self.tab_controlpanel.indexOf(self.scenarios_setup), _translate("frm_SEEMS_main", "Scenarios Setup", None))
        self.lbl_select_review_scenario.setText(_translate("frm_SEEMS_main", "Select Scenario:", None))
        self.lbl_select_review_variable.setText(_translate("frm_SEEMS_main", "Select Variable:", None))
        self.gbx_plot_period.setTitle(_translate("frm_SEEMS_main", "Plot Period", None))
        self.lbl_select_review_start_year.setText(_translate("frm_SEEMS_main", "Start Year:", None))
        self.lbl_select_review_end_year.setText(_translate("frm_SEEMS_main", "End Year:", None))
        self.gbx_result_review_plot_type.setTitle(_translate("frm_SEEMS_main", "Plot Type", None))
        self.rdbtn_bar_chart.setText(_translate("frm_SEEMS_main", "Bar Chart", None))
        self.rdbtn_line_chart.setText(_translate("frm_SEEMS_main", "Line Chart", None))
        self.btn_review_plot.setText(_translate("frm_SEEMS_main", "Plot", None))
        self.tab_controlpanel.setTabText(self.tab_controlpanel.indexOf(self.results_review), _translate("frm_SEEMS_main", "Results Review", None))
        self.gbx_cross_section_ana.setTitle(_translate("frm_SEEMS_main", "Cross-section Data Analysis", None))
        self.lbl_select_cross_section_analysis_scenario.setText(_translate("frm_SEEMS_main", "Select Scenario:", None))
        self.lbl_select_cross_section_analysis_variable.setText(_translate("frm_SEEMS_main", "Select Variable:", None))
        self.lbl_select_cross_section_analysis_year.setText(_translate("frm_SEEMS_main", "Select Year:", None))
        self.gbx_cross_section_plot_type.setTitle(_translate("frm_SEEMS_main", "Plot Type", None))
        self.rdbtn_histogram.setText(_translate("frm_SEEMS_main", "Histogram", None))
        self.btn_cross_section_analysis_plot.setText(_translate("frm_SEEMS_main", "Plot", None))
        self.gbx_time_series_ana.setTitle(_translate("frm_SEEMS_main", "Time-series Data Analysis", None))
        self.lbl_select_time_series_analysis_scenario.setText(_translate("frm_SEEMS_main", "Select Scenario:", None))
        self.lbl_select_time_series_analysis_variable.setText(_translate("frm_SEEMS_main", "Select Variable:", None))
        self.gbx_time_series_plot_period.setTitle(_translate("frm_SEEMS_main", "Plot Period", None))
        self.lbl_select_time_series_analysis_start_year.setText(_translate("frm_SEEMS_main", "Select Start Year:", None))
        self.lbl_select_time_series_analysis_end_year.setText(_translate("frm_SEEMS_main", "Select End Year:", None))
        self.gbx_time_series_plot_type.setTitle(_translate("frm_SEEMS_main", "Plot Type", None))
        self.rdbtn_stacked_bars_chart.setText(_translate("frm_SEEMS_main", "Stacked Bars", None))
        self.rdbtn_multiple_line_chart.setText(_translate("frm_SEEMS_main", "Multiple Lines", None))
        self.btn_time_series_analysis_plot.setText(_translate("frm_SEEMS_main", "Plot", None))
        self.tab_controlpanel.setTabText(self.tab_controlpanel.indexOf(self.data_analysis), _translate("frm_SEEMS_main", "Data Analysis", None))
        self.menuHelp.setTitle(_translate("frm_SEEMS_main", "Help", None))
        self.actionAbout.setText(_translate("frm_SEEMS_main", "About", None))



    def btn_start_simulation_onclick(self):
        
        # Get scenario settings from user inputs
        scenario_name = str(self.txt_input_scenario_name.text())
        start_year = self.sbx_set_simulation_start_year.value()
        end_year = self.sbx_set_simulation_end_year.value()
        simulation_depth = end_year - start_year


        # Check for already existing names first.
        version_table = DataAccess.get_table(db, version_table_name)        
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


            create_scenario(db, scenario_name, model_table_name, model_table, household_table_name, household_table, 
                            person_table_name, person_table, land_table_name, land_table, 
                            business_sector_table_name, business_sector_table, policy_table_name, policy_table, 
                            stat_table_name, stat_table, simulation_depth, start_year, self)

            # When simulation is done, refresh the default scenario name
            self.add_default_new_scenario_name()
    
            # Then refresh the result review control and data analysis tabs
            self.refresh_review_panel()
            self.refresh_analysis_panel()
            
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
#                 remove_scenario_version_from_database(scenario_name, db, self)
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
        # Refresh the version_table cursor.
        version_table = DataAccess.get_table(db, version_table_name)
        
        # Get the scenario list.
        scenario_list = list()
        for version in version_table:
            scenario_list.append(str(version[0]))
        
        if len(scenario_list) == 0:
            new_scenario_name = 'a001'
        else:        
            new_scenario_name_num = int(max(scenario_list)[1:]) + 1

            if int(new_scenario_name_num/100) != 0: # if the new scenario number is in hundreds
                new_scenario_name = max(scenario_list)[:1] + str(new_scenario_name_num)
            elif int(new_scenario_name_num/100) == 0 and int(new_scenario_name_num/10) != 0: # if the new scenario number is in tens
                new_scenario_name = max(scenario_list)[:1] + '0' + str(new_scenario_name_num)
            else:
                new_scenario_name = max(scenario_list)[:1] + '00' + str(new_scenario_name_num)
        
        self.txt_input_scenario_name.setText(new_scenario_name)


    def cmb_select_scenario_onchange(self):
        # Refresh the stat_table cursor
        stat_table = DataAccess.get_table(db, stat_table_name) 

        # Clear current select variable combo box
        self.cmb_select_review_variable.clear()
            
        # Get the variable list and simulation length for the selected scenario        
        variable_list = list()
        year_list = list()

        for record in stat_table:
            if record.ScenarioVersion == self.cmb_select_review_scenario.currentText():
                if record.StatDate not in year_list:
                    year_list.append(record.StatDate)
                if record.Variable not in variable_list and record.CompositeIndicator == 0:
                    # Exclude the composite indicators
                    variable_list.append(record.Variable)

        
        # Sort the variables list
        variable_list.sort()
                    
        # add the items to variable combo box
        self.cmb_select_review_variable.addItems(variable_list)
        
        # Reset the plot start and end years display according to the respective scenario's settings.
        self.sbx_select_review_start_year.setProperty("value", min(year_list))
        self.sbx_select_review_end_year.setProperty("value", max(year_list))


    def cmb_select_cross_section_analysis_scenario_onchange(self):
        # Refresh the stat_table cursor
        stat_table = DataAccess.get_table(db, stat_table_name) 

        # Clear current select cross section analysis variable combo box
        self.cmb_select_cross_section_analysis_variable.clear()
            
        # Get the variable list and simulation length for the selected scenario        
        variable_list = list()
        year_list = list()
    
        for record in stat_table:
            if record.ScenarioVersion == self.cmb_select_cross_section_analysis_scenario.currentText():
                if record.StatDate not in year_list:
                    year_list.append(record.StatDate)
                if record.Variable not in variable_list and record.CompositeIndicator == 0:
                    # Exclude the composite indicators
                    variable_list.append(record.Variable)

        # Sort the variables list
        variable_list.sort()        
                    
        # add the items to variable combo box
        self.cmb_select_cross_section_analysis_variable.addItems(variable_list)
        
        # Reset the cross section year display according to the respective scenario's settings.
        self.sbx_select_cross_section_analysis_year.setProperty("value", min(year_list))       
    

    def cmb_select_time_series_analysis_scenario_onchange(self):
        # Refresh the stat_table cursor
        stat_table = DataAccess.get_table(db, stat_table_name) 

        # Clear current select time series analysis variable combo box
        self.cmb_select_time_series_analysis_variable.clear()
            
        # Get the variable list and simulation length for the selected scenario        
        variable_list = list()
        year_list = list()
    
        for record in stat_table:
            if record.ScenarioVersion == self.cmb_select_time_series_analysis_scenario.currentText():
                if record.StatDate not in year_list:
                    year_list.append(record.StatDate)
                if record.Variable not in variable_list and record.CompositeIndicator == 1:
                    # Include only the composite indicators
                    variable_list.append(record.Variable)

        # Sort the variables list
        variable_list.sort()        
                    
        # add the items to variable combo box
        self.cmb_select_time_series_analysis_variable.addItems(variable_list)
        
        # Reset the analysis start and end years display according to the respective scenario's settings.
        self.sbx_select_time_series_analysis_start_year.setProperty("value", min(year_list))
        self.sbx_select_time_series_analysis_end_year.setProperty("value", max(year_list))        



    def btn_review_plot_onclick(self):
        '''
        The Plot button in the 'Results Review' Tag of the Control Panel
        '''

        # Note that data must be read from the database, rather than lists and dictionaries in the program, 
        # for users may need to make plots after the iteration (running of main simulation program).
        
        # Read the statistics table.        
        stat_table = DataAccess.get_table(db, stat_table_name)
        
        # Get the plot title
        plot_title = str(self.cmb_select_review_variable.currentText())        
        
        # Define x and y axes units
        x_unit = 'Year'
        y_unit = ''

        # Define the plot series list       
        plot_series_list = list()
        
        # Assign values for the variable lists        
        # Define a list containing the (x, y) data points (in the form of tuples)
        plot_xy_tuple_list = list()                

        for st in stat_table:            
            # Look only the records for the current scenario version
            if st.ScenarioVersion == self.cmb_select_review_scenario.currentText():
                # Find the variable
                if st.Variable == str(self.cmb_select_review_variable.currentText()):    
                    series_name = st.Variable
                    y_unit = st.StatUnit
                    
                    # Determine the plot time range according to the plot type
                    # For line plots, skip the first year (the starting point).
                    if self.rdbtn_line_chart.isChecked() and self.tab_controlpanel.currentIndex() == 1:
                        plot_start_year = self.sbx_select_review_start_year.value() + 1
                    else:
                        plot_start_year = self.sbx_select_review_start_year.value()
                    
                    # Assign values for the variable
                    if st.StatDate >= plot_start_year and st.StatDate <= self.sbx_select_review_end_year.value():                
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

        # Draw the plot
        # First, remove any existing canvas contents
        self.lyt.removeWidget(self.mc)
        self.lyt.removeWidget(self.mpl_toolbar)
        
        # Then create a new canvas instance
        self.mc = MplCanvas(self.canvaswidget)
        self.mc.plot('timeseries', plot_title, x_data, plot_series_list, x_unit, y_unit, self)






    def btn_time_series_plot_onclick(self):
        '''
        The Plot button in the 'Data Analysis' Tag of the Control Panel
        '''
        
        # Read the statistics table.   
        stat_table = DataAccess.get_table(db, stat_table_name)

        # Get the plot title
        plot_title = str(self.cmb_select_time_series_analysis_variable.currentText())
        
        # Define the x and y axes unit
        x_unit = 'Year'
        y_unit = ''
        
        # Define the plot series list       
        plot_series_list = list()

        # Determine the plot time range according to the plot type
        # For line plots, skip the first year (the starting point).
        if self.rdbtn_multiple_line_chart.isChecked() and self.tab_controlpanel.currentIndex() == 2:
            analysis_start_year = self.sbx_select_time_series_analysis_start_year.value() + 1 # Do not plot "the current year" in a multiple line chart.
        else:
            analysis_start_year = self.sbx_select_time_series_analysis_start_year.value()

        
        
        # Make the plot series list
        for indicator in composite_indicators_dict:
            if self.cmb_select_time_series_analysis_variable.currentText() == indicator: 
                if self.cmb_select_time_series_analysis_variable.currentText() == indicator:
                    for variable in composite_indicators_dict[indicator]:     
                        plot_xy_tuple_list = list()
                        
                        for st in stat_table:
                            # Find the currently selected scenario
                            if st.Variable == variable \
                            and st.ScenarioVersion == self.cmb_select_time_series_analysis_scenario.currentText() \
                            and st.StatDate >= analysis_start_year \
                            and st.StatDate <= self.sbx_select_time_series_analysis_end_year.value():                          
                                
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

        # Draw the plot
        # First, remove any existing canvas contents
        self.lyt.removeWidget(self.mc)
        self.lyt.removeWidget(self.mpl_toolbar)
        
        # Then create a new canvas instance
        self.mc = MplCanvas(self.canvaswidget)
        self.mc.plot('timeseries', plot_title, x_data, plot_series_list, x_unit, y_unit, self)
        


    def refresh_review_panel(self):
        '''
        Only refresh the select scenario combo boxes here;
        Will refresh the select variable combo boxes later when a specific scenario is selected.
        '''
            
        # Refresh the version_table cursor
        version_table = DataAccess.get_table(db, version_table_name)
            
        # Get the scenario list for the select scenario combo boxes in the GUI/Results Review tab to display
        scenario_list = list()
        
        # Get the current scenario list in the select review scenario combo box
        existing_scenarios = [self.cmb_select_review_scenario.itemText(i) for i in range(self.cmb_select_review_scenario.count())]
        
        # Add the newly created scenario version to scenario_list
        for version in version_table:
            if version[0] not in existing_scenarios:
                scenario_list.append(str(version[0]))        
                    
        # add the new scenario list to the respective combo box
        if len(scenario_list) != 0:
            self.cmb_select_review_scenario.addItems(scenario_list)
            # The addItems action will automatically trigger the 'onChange' event of the combo box 
            # and call the respective event handling submodule to refresh the select variable combo box
    
    
    
    def refresh_analysis_panel(self):    
        '''
        Only refresh the select scenario combo boxes here;
        Will refresh the select variable combo boxes later when a specific scenario is selected.
        '''
        
        # Refresh the version_table cursor
        version_table = DataAccess.get_table(db, version_table_name)
            
        # Get the scenario list for the combo boxes in GUI to display
        scenario_list = list()
        
        # Get the current scenario list in the combo box
        existing_scenarios = [self.cmb_select_time_series_analysis_scenario.itemText(i) for i in range(self.cmb_select_time_series_analysis_scenario.count())]
        
        # Add the newly created scenario version to scenario_list
        for version in version_table:
            if version[0] not in existing_scenarios:
                scenario_list.append(str(version[0]))
                    
        # add the scenario_list to the respective combo box
        if len(scenario_list) != 0:
            self.cmb_select_cross_section_analysis_scenario.addItems(scenario_list)
            self.cmb_select_time_series_analysis_scenario.addItems(scenario_list)



    def action_menu_help_about(self):
        help_about_dialog = QtGui.QDialog()
        help_about_dialog_ui = Ui_SEEMS_help_about()
        help_about_dialog_ui.setupUi(help_about_dialog)
        help_about_dialog.show()
        help_about_dialog.exec_()




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
        
        x_data: a simple list of numbers
        y_data: a list of tuples; each tuple is in the form of (series_name, [series_data_list]).

        x_unit - unit of the x axis
        y_unit - unit of the y axis       
        '''
        


        if data_type == 'timeseries':

            # Determine the chart type
            if gui.rdbtn_bar_chart.isChecked() and gui.tab_controlpanel.currentIndex() == 1 \
            or gui.rdbtn_stacked_bars_chart.isChecked() and gui.tab_controlpanel.currentIndex() == 2:                

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
                
                
            elif gui.rdbtn_line_chart.isChecked() and gui.tab_controlpanel.currentIndex() == 1 \
            or gui.rdbtn_multiple_line_chart.isChecked() and gui.tab_controlpanel.currentIndex() == 2:
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
        gui.mpl_toolbar = NavigationToolbar(gui.mc, gui.canvaswidget)

        # Add the widegts to the vbox
        gui.lyt.addWidget(gui.mc)
        gui.lyt.addWidget(gui.mpl_toolbar)


