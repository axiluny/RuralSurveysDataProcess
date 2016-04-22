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
    
    def __init__(self, record):
        
        self.HID = record[0]
        self.PID = record[1]
        self.R2HH = record[2]
        self.sex = record[3]
        self.YOB = record[4]
        self.maritalstatus = record[5]
        
        self.father = list()
        self.mother = list()

        self.spouse = list()

        self.childrenlist = list()
        
        self.grandchildrenlist=list()
                  
        
        
        
        
        
        
        
          