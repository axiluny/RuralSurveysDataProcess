'''
Created on Mar 28, 2016

@author: Liyan Xu;
'''
from data_access import DataAccess
from person import Person

db_file_name = 'C:\Users\liyanxu\Dropbox (MIT)\Projects\RuralSurveys\_python_processing\RuralSurvey2014_kinships.mdb'
dbdriver = '{Microsoft Access Driver (*.mdb)}'

input_db = DataAccess(db_file_name, dbdriver)

input_table_name = 'A_Persons'
# output_table_name = 'Persons_offsprings'

input_table = DataAccess.get_table(input_db, input_table_name)


'''
Make a person dictionary, filled with person class instances
''' 
pp_dict = dict()
  
for pp in input_table:
    pp_dict[pp[1]] = Person(pp) # Indexed by PID
     
 
# # find sons(daughters) and grandsons(granddaughters) of the household head and his/her spouse
# for PID in pp_dict:
#     if pp_dict[PID].R2HH == '1' or pp_dict[PID].R2HH == '2':
#         for PID_member in pp_dict:
#             if pp_dict[PID_member].HID == pp_dict[PID].HID:
#                 if pp_dict[PID_member].R2HH == '3':
#                     pp_dict[PID].sonlist.append(pp_dict[PID_member])
#                 elif pp_dict[PID_member].R2HH == '5':
#                     pp_dict[PID].grandsonlist.append(pp_dict[PID_member])
#                       
#  
# # find sons(daughters) of the second-generation people (son/daughter of the household head and his/her spouse) in a household
# for PID in pp_dict:
#     if pp_dict[PID].R2HH == '3' or pp_dict[PID].R2HH == '4':
#         for PID_member in pp_dict:
#             if pp_dict[PID_member].HID == pp_dict[PID].HID:
#                 if pp_dict[PID_member].R2HH == '5':
#                     if pp_dict[PID_member].YOB - pp_dict[PID].YOB >= 18:
#                         pp_dict[PID].sonlist.append(pp_dict[PID_member])
 
                      
'''
Find parents, kids, and spouse IDs
'''

# find spouse
for PID in pp_dict:
    if pp_dict[PID].R2HH == '1':
        for PID_spouse in pp_dict:
            if pp_dict[PID_spouse].HID == pp_dict[PID].HID and pp_dict[PID_spouse].R2HH == '2':
                pp_dict[PID].spouse.append(pp_dict[PID_spouse])
                pp_dict[PID_spouse].spouse.append(pp_dict[PID])


    elif pp_dict[PID].R2HH == '3':
        
        # search only those married
        if pp_dict[PID].maritalstatus == '1':
        
            ct_siblings = 0
            
            # find all siblings in household
            for PID_sibling in pp_dict:
                if pp_dict[PID_sibling].HID == pp_dict[PID].HID and pp_dict[PID_sibling].R2HH == '3' and pp_dict[PID_sibling].PID <> PID:
                    ct_siblings += 1
            
            # if no siblings
            if ct_siblings == 0:
            
                # then         
                for PID_spouse in pp_dict:
                    if pp_dict[PID_spouse].HID == pp_dict[PID].HID and pp_dict[PID_spouse].R2HH == '4':
                        pp_dict[PID].spouse.append(pp_dict[PID_spouse])
                        pp_dict[PID_spouse].spouse.append(pp_dict[PID])
    
    elif pp_dict[PID].R2HH == '6':
        for PID_spouse in pp_dict:
            if pp_dict[PID_spouse].HID == pp_dict[PID].HID and pp_dict[PID_spouse].R2HH == '6' and pp_dict[PID_spouse].PID <> PID:
                pp_dict[PID].spouse.append(pp_dict[PID_spouse])
                pp_dict[PID_spouse].spouse.append(pp_dict[PID])



# find parents and kids
for PID in pp_dict:
    if pp_dict[PID].R2HH == '1':
        for PID_parent in pp_dict:
            if pp_dict[PID_parent].HID == pp_dict[PID].HID and pp_dict[PID_parent].R2HH == '6' and pp_dict[PID_parent].sex == '1':
                pp_dict[PID].father.append(pp_dict[PID_parent])
                pp_dict[PID_parent].kidslist.append(pp_dict[PID])
            if pp_dict[PID_parent].HID == pp_dict[PID].HID and pp_dict[PID_parent].R2HH == '6' and pp_dict[PID_parent].sex == '0':
                pp_dict[PID].mother.append(pp_dict[PID_parent])                
                pp_dict[PID_parent].kidslist.append(pp_dict[PID])


    elif pp_dict[PID].R2HH == '3':
        for PID_parent in pp_dict:
            if pp_dict[PID_parent].HID == pp_dict[PID].HID and (pp_dict[PID_parent].R2HH == '1' or pp_dict[PID_parent].R2HH == '2') and pp_dict[PID_parent].sex == '1':
                pp_dict[PID].father.append(pp_dict[PID_parent])
                pp_dict[PID_parent].kidslist.append(pp_dict[PID])
            if pp_dict[PID_parent].HID == pp_dict[PID].HID and (pp_dict[PID_parent].R2HH == '1' or pp_dict[PID_parent].R2HH == '2') and pp_dict[PID_parent].sex == '0':
                pp_dict[PID].mother.append(pp_dict[PID_parent])                
                pp_dict[PID_parent].kidslist.append(pp_dict[PID])        
        

    elif pp_dict[PID].R2HH == '5':
        # find and count potential parents in the household
        
        ct_ptl_prnts = 0
        ptl_prnts_list = list()
        
        for PID_ptl_prnt in pp_dict:
            if pp_dict[PID_ptl_prnt].HID == pp_dict[PID].HID and (pp_dict[PID_ptl_prnt].R2HH == '3' or pp_dict[PID_ptl_prnt].R2HH == '4') and pp_dict[PID_ptl_prnt].maritalstatus == '1':
                ct_ptl_prnts += 1
                ptl_prnts_list.append(pp_dict[PID_ptl_prnt])
        
        if ct_ptl_prnts == 2: # proceed
            if ptl_prnts_list[0].sex == 1:
                pp_dict[PID].father.append(ptl_prnts_list[0])
                pp_dict[PID].mother.append(ptl_prnts_list[1])
                pp_dict[ptl_prnts_list[0].PID].kidslist.append(pp_dict[PID])
                pp_dict[ptl_prnts_list[1].PID].kidslist.append(pp_dict[PID])

            else:
                pp_dict[PID].father.append(ptl_prnts_list[1])
                pp_dict[PID].mother.append(ptl_prnts_list[0])                
                pp_dict[ptl_prnts_list[0].PID].kidslist.append(pp_dict[PID])
                pp_dict[ptl_prnts_list[1].PID].kidslist.append(pp_dict[PID])     



'''
Create a new table in the database and store the results
'''
                
# name of the new table: offsprings
# create_table_order = '''create table offsprings (HID VARCHAR,PID VARCHAR,R2HH VARCHAR, sex VARCHAR, YOB VARCHAR, maritalstatus VARCHAR, 
#         son1 VARCHAR, son1_YOB VARCHAR, son2 VARCHAR, son2_YOB VARCHAR, son3 VARCHAR, son3_YOB VARCHAR, 
#         son4 VARCHAR, son4_YOB VARCHAR, son5 VARCHAR, son5_YOB VARCHAR, 
#         grandson1 VARCHAR, grandson1_YOB VARCHAR, grandson2 VARCHAR, grandson2_YOB VARCHAR, grandson3 VARCHAR, grandson3_YOB VARCHAR, 
#         grandson4 VARCHAR, grandson4_YOB VARCHAR, grandson5 VARCHAR, grandson5_YOB VARCHAR)'''


# name of the new table: kinships
create_table_order = '''create table kinships (HID VARCHAR,PID VARCHAR,R2HH VARCHAR, sex VARCHAR, YOB VARCHAR, maritalstatus VARCHAR, 
        FatherID VARCHAR, MotherID VARCHAR, SpouseID VARCHAR, KidID_1 VARCHAR, KidID_2 VARCHAR, KidID_3 VARCHAR, KidID_4 VARCHAR, KidID_5 VARCHAR)'''

DataAccess.create_table(input_db, create_table_order)
DataAccess.db_commit(input_db)


# insert the records into the new table
# information to be inserted: PID, YOB
for PID in pp_dict:
    content_list = list()
    
    content_list.append(pp_dict[PID].HID)
    content_list.append(pp_dict[PID].PID)
    content_list.append(pp_dict[PID].R2HH)
    content_list.append(pp_dict[PID].sex)    
    content_list.append(pp_dict[PID].YOB)
    content_list.append(pp_dict[PID].maritalstatus)
    
    if len(pp_dict[PID].father) <> 0:
        content_list.append(pp_dict[PID].father[0].PID)
    else:
        content_list.append('')
    
    if len(pp_dict[PID].mother) <> 0:        
        content_list.append(pp_dict[PID].mother[0].PID)
    else:
        content_list.append('')

    if len(pp_dict[PID].spouse) <> 0:
        content_list.append(pp_dict[PID].spouse[0].PID)
    else:
        content_list.append('')
    
    for i in range(5):
        if i < (len(pp_dict[PID].kidslist)):
            content_list.append(pp_dict[PID].kidslist[i].PID)
        else:
            content_list.append('')
    
    
#     for i in range(5):
#         if i < (len(pp_dict[PID].sonlist)):
#             content_list.append(pp_dict[PID].sonlist[i].PID)
#             content_list.append(pp_dict[PID].sonlist[i].YOB)
#         else:
#             content_list.append('')
#             content_list.append('')
#     
#     for j in range(5):
#         if j < (len(pp_dict[PID].grandsonlist)):
#             content_list.append(pp_dict[PID].grandsonlist[j].PID)
#             content_list.append(pp_dict[PID].grandsonlist[j].YOB)
#         else:
#             content_list.append('')
#             content_list.append('')



    
    new_record_content = '('
    for k in range(len(content_list)):
        new_record_content += '\''+ unicode(content_list[k])+ '\','        

    # Change the ending comma to a closing parenthesis
    new_record_content = new_record_content[0:len(new_record_content)-1] + ')'    
    
    insert_table_order = "insert into kinships values " + new_record_content.replace('None','Null') +';'
    
    DataAccess.insert_record_to_table(input_db, insert_table_order)
DataAccess.db_commit(input_db)  

print "Success!"






