'''
Created on Mar 26, 2015

@author: Liyan Xu; Hongmou Zhang
'''
import sys
from PyQt4 import QtCore, QtGui

from data_access import DataAccess
from society import Society
import statistics
from plot_test import Window
from PyQt4.Qt import QMessageBox

# Define scenario name temporarily
scenario_name = ''

 
 
# dbname = 'C:/WolongRun/test_db/SimplifiedDB.mdb'
dbname = 'C:/WolongRun/WolongDB'
dbdriver = '{Microsoft Access Driver (*.mdb)}'
 
model_table_name = 'ModelTable'
household_table_name = 'HouseholdTable'
person_table_name = 'PersonTable'
 
stat_table_name = 'StatTable'
 
# Rounds of iteration (years)
simulation_depth = 2
 
# Starting and ending year of simulation
start_year = 2015
end_year = 2030
 
 
'''
 When the database is loaded in the app, do the following.
'''
 
# Get the working database
db = DataAccess(dbname, dbdriver)
 
# Get the table pointers
model_table = DataAccess.get_table(db, model_table_name)
household_table = DataAccess.get_table(db, household_table_name)
person_table = DataAccess.get_table(db, person_table_name)
stat_table = DataAccess.get_table(db, stat_table_name)







def CreateScenario(db, model_table_name, model_table, hh_table_name, hh_table, pp_table_name, pp_table, stat_table_name, stat_table, simulation_depth, start_year, end_year, gui):
    
    # Set up a scenario name
    set_up_scenario_name()
    
    # Initialize society: create society, household, person, etc instances
    soc = Society(db, model_table_name, model_table, hh_table_name, hh_table, pp_table_name, pp_table, stat_table_name, stat_table, start_year, end_year)

    # Add statistics for the starting point
    add_stat_results(soc)
    
    # Then save updated tables in database
    save_results_to_db(db, soc)
    
    # Set the progress bar in the GUI
    gui.prb_progressBar.setMinimum(0)
    gui.prb_progressBar.setMaximum(simulation_depth)    
    
    #Start simulation
    for simulation_count in range(simulation_depth):
        step_go(db, soc, start_year, end_year, simulation_count)

        # Set value for the progress bar
        gui.prb_progressBar.setValue(simulation_count + 1)

            
        
#     # Make plots of results
#     make_plots(soc, db, stat_table_name)


#     # Temporarily adding this - signaling end of the run.
#     print 'Success!'


# Set up scenario name from UI inputs
# Should check for already existing names, otherwise later results will be added to the existing table, causing troubles
def set_up_scenario_name():
    name = 'test_scenario'
    return name

scenario_name = set_up_scenario_name()



def step_go(database, society_instance, start_year, end_year, simulation_count):

    
    # Do the simulation
    Society.step_go(society_instance, start_year, end_year, simulation_count)

    # Do statistics and add records to statistics table in database
    add_stat_results(society_instance)
    
    # Then save updated tables in database
    save_results_to_db(database, society_instance)




def add_stat_results(society_instance):
    
    society_instance.stat_dict = dict()

    # Total population
    pp = statistics.StatClass()
    statistics.StatClass.get_population_count(pp, society_instance, scenario_name)
    
    # Household count
    hh = statistics.StatClass()
    statistics.StatClass.get_household_count(hh, society_instance, scenario_name)
   
    
    
    
def save_results_to_db(database, society_instance):
    
    # Determine household, people,and land table names
    # Format: Scenario_name + household/people/land
    new_hh_table_name = scenario_name + '_household'
    new_pp_table_name = scenario_name + '_persons'
#     new_land_table_name = scenario_name + '_land'
    
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





    # Saving the Statistics table in the database
  
      
    # If the table with that name does not exist in the database
    # i.e. in the first round of iteration,
    # Then first create a new table, then insert the records.
    # Otherwise, just find the right table, and then insert the records.
    if DataAccess.get_table(database, stat_table_name) == None: 
        pass
      
#         # Create a new Household table from the variable list of Household Class
#         new_household_table_formatter = '('
#         for var in society_instance.hh_var_list:
#             # Add household variables to the formatter
#             new_household_table_formatter += var[0] + ' ' + var[2] + ','  
#         new_household_table_formatter = new_household_table_formatter[0: len(new_household_table_formatter) - 1] + ')'
#       
#         create_table_order = "create table " + new_hh_table_name +''+ new_household_table_formatter
#         DataAccess.create_table(database, create_table_order)
#         DataAccess.db_commit(database)
#   
#         # Then insert all households into the new table
#         # InsertContent = ''
#         for HID in society_instance.hh_dict:
#             # Make the insert values for this household
#             new_household_record_content = '('
#             for var in society_instance.hh_var_list:
#                 # If the value is string, add quotes
#                 if var[2] == 'VARCHAR' and getattr(society_instance.hh_dict[HID], var[0]) != None: 
#                     new_household_record_content += '\''+ unicode(getattr(society_instance.hh_dict[HID], var[0]))+ '\','
#                 else:
#                     new_household_record_content += unicode(getattr(society_instance.hh_dict[HID], var[0]))+ ','
#             # Change the ending comma to a closing parenthesis
#             new_household_record_content = new_household_record_content[0:len(new_household_record_content)-1] + ')'
#             # Insert one household record
#             insert_table_order = "insert into " + new_hh_table_name + ' values ' + new_household_record_content.replace('None','Null') +';'
#             DataAccess.insert_table(database, insert_table_order)
#         DataAccess.db_commit(database)  
  
      
    else:
        # Just insert all records into the existing table
        # InsertContent = ''
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
            DataAccess.insert_table(database, insert_table_order)
        DataAccess.db_commit(database)        
   




def make_plots(society_instance, db, stat_table_name):
    
    # For tech demo, just add one plot without the event driver.
    
    # Data must be read from the database, rather than lists and dictionaries in the program, 
    # for users may need to make plots after the iteration (running of main simulation program).
    
    # Read the statistics table and make the lists for plotting charts
    stat_table = DataAccess.get_table(db, stat_table_name)
    
    time_stamps = list()
    population = list()
    household_count = list()
    
    for st in stat_table:
                            
        if st.Variable == 'Total_Population':
            time_stamps.append(st.StatDate)
            population.append(st.StatValue)
        
        elif st.Variable == 'Household_Count':
            household_count.append(st.StatValue)
            

    # Show plot in a GUI window
    app = QtGui.QApplication(sys.argv)
    
    # population
    gui = Window(time_stamps, population)
    gui.show()
    
    # household count
    gui1 = Window(time_stamps, household_count)
    gui1.show()
    
    sys.exit(app.exec_())
    



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
        frm_SEEMS_main.setObjectName(_fromUtf8("frm_SEEMS_main"))
        frm_SEEMS_main.resize(1070, 734)
        self.centralwidget = QtGui.QWidget(frm_SEEMS_main)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.tab_controlpanel = QtGui.QTabWidget(self.centralwidget)
        self.tab_controlpanel.setGeometry(QtCore.QRect(10, 10, 351, 661))
        self.tab_controlpanel.setObjectName(_fromUtf8("tab_controlpanel"))
        self.scenarios_setup = QtGui.QWidget()
        self.scenarios_setup.setObjectName(_fromUtf8("scenarios_setup"))
        self.prb_progressBar = QtGui.QProgressBar(self.scenarios_setup)
        self.prb_progressBar.setGeometry(QtCore.QRect(10, 590, 321, 23))
        self.prb_progressBar.setProperty("value", 0)
        self.prb_progressBar.setObjectName(_fromUtf8("prb_progressBar"))
        self.btn_start_simulation = QtGui.QPushButton(self.scenarios_setup)
        self.btn_start_simulation.setGeometry(QtCore.QRect(90, 540, 151, 34))
        self.btn_start_simulation.setObjectName(_fromUtf8("btn_start_simulation"))

        
        self.btn_start_simulation.clicked.connect(self.on_btn_start_simulation_clicked)


        
        self.lbl_input_scenario_name_label = QtGui.QLabel(self.scenarios_setup)
        self.lbl_input_scenario_name_label.setGeometry(QtCore.QRect(10, 490, 121, 19))
        self.lbl_input_scenario_name_label.setObjectName(_fromUtf8("lbl_input_scenario_name_label"))
        self.txt_input_scenario_name = QtGui.QLineEdit(self.scenarios_setup)
        self.txt_input_scenario_name.setGeometry(QtCore.QRect(140, 490, 191, 25))
        self.txt_input_scenario_name.setObjectName(_fromUtf8("txt_input_scenario_name"))
        self.tab_controlpanel.addTab(self.scenarios_setup, _fromUtf8(""))
        self.result_review = QtGui.QWidget()
        self.result_review.setObjectName(_fromUtf8("result_review"))
        self.cmb_select_variable = QtGui.QComboBox(self.result_review)
        self.cmb_select_variable.setGeometry(QtCore.QRect(130, 20, 201, 25))
        self.cmb_select_variable.setObjectName(_fromUtf8("cmb_select_variable"))
        self.cmb_select_variable.addItem(_fromUtf8(""))
        self.cmb_select_variable.addItem(_fromUtf8(""))
        self.lbl_select_variable_label = QtGui.QLabel(self.result_review)
        self.lbl_select_variable_label.setGeometry(QtCore.QRect(10, 20, 121, 19))
        self.lbl_select_variable_label.setObjectName(_fromUtf8("lbl_select_variable_label"))
        self.btn_plot = QtGui.QPushButton(self.result_review)
        self.btn_plot.setGeometry(QtCore.QRect(110, 550, 112, 34))
        self.btn_plot.setObjectName(_fromUtf8("btn_plot"))
        self.tab_controlpanel.addTab(self.result_review, _fromUtf8(""))
        self.graphicsView = QtGui.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(390, 10, 661, 661))
        self.graphicsView.setObjectName(_fromUtf8("graphicsView"))
        frm_SEEMS_main.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(frm_SEEMS_main)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1070, 31))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        frm_SEEMS_main.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(frm_SEEMS_main)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        frm_SEEMS_main.setStatusBar(self.statusbar)
        self.actionAbout = QtGui.QAction(frm_SEEMS_main)
        self.actionAbout.setObjectName(_fromUtf8("actionAbout"))
        self.actionAbout_2 = QtGui.QAction(frm_SEEMS_main)
        self.actionAbout_2.setObjectName(_fromUtf8("actionAbout_2"))
        self.menuFile.addAction(self.actionAbout_2)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(frm_SEEMS_main)
        self.tab_controlpanel.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(frm_SEEMS_main)

    def retranslateUi(self, frm_SEEMS_main):
        frm_SEEMS_main.setWindowTitle(_translate("frm_SEEMS_main", "SEEMS  -  Socio-Economical-Ecological Multipurpose Simulator", None))
        self.btn_start_simulation.setText(_translate("frm_SEEMS_main", "Start Simulation", None))
        self.lbl_input_scenario_name_label.setText(_translate("frm_SEEMS_main", "Scenario Name:", None))
        self.tab_controlpanel.setTabText(self.tab_controlpanel.indexOf(self.scenarios_setup), _translate("frm_SEEMS_main", "Scenarios Setup", None))
        self.cmb_select_variable.setItemText(0, _translate("frm_SEEMS_main", "Total Population", None))
        self.cmb_select_variable.setItemText(1, _translate("frm_SEEMS_main", "Total Household Count", None))
        self.lbl_select_variable_label.setText(_translate("frm_SEEMS_main", "Select Variable:", None))
        self.btn_plot.setText(_translate("frm_SEEMS_main", "Plot", None))
        self.tab_controlpanel.setTabText(self.tab_controlpanel.indexOf(self.result_review), _translate("frm_SEEMS_main", "Result Review", None))
        self.menuFile.setTitle(_translate("frm_SEEMS_main", "Help", None))
        self.actionAbout.setText(_translate("frm_SEEMS_main", "About", None))
        self.actionAbout_2.setText(_translate("frm_SEEMS_main", "About", None))




    def on_btn_start_simulation_clicked(self):
        
        # Run the simulation
        CreateScenario(db, model_table_name, model_table, household_table_name, household_table, person_table_name, person_table, stat_table_name, stat_table, simulation_depth, start_year, end_year, self)
    

        # Show a message box indicating the completion of run.
        msb = QMessageBox()
        msb.setText('The Simulation is Complete!        ')
        msb.setWindowTitle('SEEMS Run')
        msb.exec_()

#         mb = MessageBox()
#         mb.exec_()



class MessageBox(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('message box')    
    
#     def closeEvent(self, event):
#         reply = QtGui.QMessageBox.question(self, 'Message', 'Are you sure to quit?', QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
#         if reply == QtGui.QMessageBox.Yes:
#             event.accept()
#         else:
#             event.ignore()



