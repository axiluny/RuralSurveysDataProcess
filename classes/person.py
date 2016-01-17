'''
Created on Apr 5, 2015

@author: Liyan Xu; Hongmou Zhang
'''
import random
from __builtin__ import False
# import copy
# from enum import Enum

class Person(object):
    
#     edu_type = Enum('edu_type','uneducated primary secondary high_school college graduate' )
    
    def __init__(self, record, VarList, current_year):
        '''
        Construct the person class from the person table in the DB, and then add some other user-defined attributes.

        record - a record in the person table in the DB.        
        VarList - the variable (or field) list of the person table in the DB   
        VarList = {paramName1: paramOrder1, paramName2: paramOrder2, ...}   
        '''       

        # Set the attributes (var) and their values (record) from the person table in the DB.                
        for var in VarList:
            setattr(self, var[0], record[var[1]])
    
        # Set the person variables (attributes) lists
        self.pp_var_list = VarList

        # Set the current time stamp
        self.StatDate = current_year
        
        # Define some other attributes of the person class
        self.is_college = False
        self.moved_out = False
        self.marriage_length = 0 #This value should have been given in the original database!
        
        # Define a variable indicating if the person is a current student
        self.is_student = False
        
        # Define some switch variables indicating whether the person is getting married, giving birth, or die in the current year
        self.is_married_this_year = False
        self.is_giving_birth_this_year = False
        self.is_died_this_year = False
            
        
    def personal_demographic_update(self, current_year, model_parameters):
        '''
        Annual demographic updates of the person.
        '''

        # Update the current time stamp
        self.StatDate = current_year
        
        # Reset the switches
        # Note this is before the "is_alive" bifurcation. 
        # So all person in hh_dict.own_pp_dict get this switch reset (every year).        
        self.is_married_this_year = False
        self.is_giving_birth_this_year = False
        self.is_died_this_year = False


        # Only the alive persons proceed into the personal demographic dynamics
        if self.is_alive == 1:
            self.grow()
            
            if self.decease(model_parameters) == True: # If the person dies this year
                return self
            
            else: # If the person lives
                self.educate(model_parameters)
                
                if self.moved_out == False:  # Persons who moved out (through colleges) are removed from the system's active person list
                    if self.IsMarry == 1:
                        if self.divorce() == False: # Temporarily not allow anyone to divorce
                            self.marriage_length += 1
                            self.childbirth(model_parameters)
                    else:
                        self.marry(model_parameters)

        return self
                        
    
    def grow(self):
        self.Age += 1        
    
    
    def decease(self, model_parameters):
        
        # Get the mortality rate according to one's age
        if self.Age <= 5:
            mortality = float(model_parameters['MortalityBelow5'])
        elif self.Age >= 6 and self.Age <= 12:
            mortality = float(model_parameters['Mortality6To12'])
        elif self.Age >= 13 and self.Age <= 15:
            mortality = float(model_parameters['Mortality13To15'])
        elif self.Age >= 16 and self.Age <= 20:
            mortality = float(model_parameters['Mortality16To20'])
        elif self.Age >= 21 and self.Age <= 60:
            mortality = float(model_parameters['Mortality21To60'])
        elif self.Age >= 61:
            mortality = float(model_parameters['MortalityAbove61'])
        
        # Make the judgment
        if mortality > random.random():
            self.is_alive = 0 # Mark the one as not alive
            self.is_died_this_year = True # And turn on this switch
            return True
        else:
            return False
        
    
    def educate(self, model_parameters):
        if self.Age >= 23:
            self.is_student = False
        else:
            if self.Education == 'uneducated':
                if self.Age >= 3 and self.Age <=6:
                    self.Education = 'preschool'
                    self.is_student = True

            elif self.Education == 'preschool':
                if self.Age >= 7 and self.Age <=12:
                    self.Education = 'primary'
                    self.is_student = True
            
            elif self.Education == 'primary':
                if self.Age >= 13 and self.Age <= 15:
                    self.Education = 'secondary'
                    self.is_student = True
            
            elif self.Education == 'secondary':
                if self.Age >= 16 and self.Age <= 18:
                    if float(model_parameters['HighSchoolEnrollmentRate']) > random.random():
                        self.Education = 'high_school'
                        self.is_student = True                         
                    else:
                        self.is_student = False                                                            

            elif self.Education == 'high_school':
                if self.Age >= 19 and self.Age <= 22: # Four chances to enter colleges           
                    if float(model_parameters['CollegeEnrollmentRate']) > random.random():
                        self.Education = 'college'
                        self.is_college = True
                        self.moved_out = True
                        self.is_student = True                         
                    else:
                        self.is_student = False




    def marry(self,model_parameters):
        '''
        Determine if the person get married this year; if yes, mark self.is_married_this_year as True
        The actions of getting married are realized in the Society Class in the next step,
        When all persons who get married this year have been marked
        '''
        
        if self.Gender == 0: # Female
            if self.Age >= 20:
                if self.marriage_rate(model_parameters) > random.random():
#                     self.IsMarry = 1
                    self.is_married_this_year = True
                    self.marriage_length = 1
        else: # Male
            if self.Age >= 22:
                if self.marriage_rate(model_parameters) > random.random():
#                     self.IsMarry = 1
                    self.is_married_this_year = True
                    self.marriage_length = 1


    
    def divorce(self):
        if 1 > 2:#Never let anyone to divorce for now/20150407
            return True
        
        else:
            self.marriage_length += 1 
            return False


    
    def childbirth(self, model_parameters):
        
        if self.Gender == 0 and self.Age < float(model_parameters['UpperBirthAge']):
        # Only women under a predetermined age can give birth.       
            if self.Age >= 15 and self.Age <= 19:
                if random.random() < float(model_parameters['FertilityRate15To19']):
                    self.is_giving_birth_this_year = True
            elif self.Age >= 20 and self.Age <= 24:
                if random.random() < float(model_parameters['FertilityRate20To24']):
                    self.is_giving_birth_this_year = True
            elif self.Age >= 25 and self.Age <= 29:
                if random.random() < float(model_parameters['FertilityRate25To29']):
                    self.is_giving_birth_this_year = True            
            elif self.Age >= 30 and self.Age <= 34:
                if random.random() < float(model_parameters['FertilityRate30To34']):
                    self.is_giving_birth_this_year = True            
            elif self.Age >= 35 and self.Age <= 39:
                if random.random() < float(model_parameters['FertilityRate35To39']):
                    self.is_giving_birth_this_year = True
            elif self.Age >= 40 and self.Age <= 44:
                if random.random() < float(model_parameters['FertilityRate40To44']):
                    self.is_giving_birth_this_year = True
            elif self.Age >= 45 and self.Age <= 49:
                if random.random() < float(model_parameters['FertilityRate45To49']):
                    self.is_giving_birth_this_year = True
                    
             
    def marriage_rate(self,model_parameters):
        max_rate = float(model_parameters['MaxMaritalRate'])
        
        if self.Age < 30:
            res = max_rate
            return res
        else:
            res = max_rate/(self.Age - 29)**0.4
            return res

    