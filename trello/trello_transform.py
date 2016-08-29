# -*- coding: utf-8 -*-
"""
Created on Fri Aug 19 10:38:14 2016

@author: Cloud User
"""

import trello_pull
import os
import re
import pandas as pd
import numpy as np

###############################################################################
# TODO
#
# 1. Utilize weeks
#       1. Specify a date range for the function to pull the proper week
#       2. Make sure we are flexible to pull out various data
#
#   Not all departments will be filled out, all operations should be filled out
#
#
# 2. Update report with Titles and Text amendments
# 3. Find an interesting way to update weekly text pieces
#
#


def generateData():
    data = trello_pull.generateTrelloData()
    return data


def processData(data):
    
        # Pull out the work object and normalize for merging with the card object
        # I am being really lazy here and will need to rework all of this code
        # Quick and Dirty to get stats on work
        
        
    operations = ['Ad Hoc Requests', 'Research', 'Operations']
    departments = ['Communications',
                       'Marketing',
                       'Group Sales',
                       'Visitor Information Center',
                       'International & Leisure Sales']
    
    
    wk = pd.DataFrame(data)
    
    
    
    # Go to work on the hours field, format for summation
    wk['hrs'] = wk['hrs'].str.replace(' hrs','')
    wk['hrs'][wk['hrs'] == ''] = '0'
    wk.hrs = wk.hrs.apply(str)
    wk.hrs = wk.hrs.apply(lambda x: x.split(','))
    
    # Go to work on the date field, format for inclusion on general Timing
    
    
    # Sum via loop for lack of a better way. Can't imagine performance is going to 
    # Matter for just me. However, this is a shitty way
    for index, row in wk.iterrows():
        hrs = row['hrs']
        hrs = map(float, hrs)       
        hrs_sum = sum(hrs)
        wk.loc[index, 'hrs'] = hrs_sum
    
    
    spacen = lambda x: pd.Series([i for i in reversed(x.split(','))])
    wk_new_labels = wk['labels'].apply(spacen)
    wk_new_labels['task_name'] = wk['task_name']
    
    wk_v1 = pd.merge(wk, wk_new_labels, on = 'task_name')
    
    for index, row in wk_v1.iterrows():
        row0 = str(row[0])
        row1 = str(row[1])
        
        if row0 in operations:
            wk_v1.loc[index, 'operations'] = row0
        if row0 in departments:
            wk_v1.loc[index, 'departments'] = row0        
    
        if row1 in operations:
            wk_v1.loc[index, 'operations'] = row1
        if row1 in departments:
            wk_v1.loc[index, 'departments'] = row1
            
    
    wk_v2 = wk_v1[['ids','hrs','labels','task_name','departments','operations']]


    return wk_v2

def outputData(data):
    
    #     Pull out the work object and normalize for merging with the card object
    #     I am being really lazy here and will need to rework all of this code
    #     Quick and Dirty to get stats on work
    
    operations = ['Ad Hoc Requests', 'Research', 'Operations']
    departments = ['Communications',
                       'Marketing',
                       'Group Sales',
                       'Visitor Information Center',
                       'International & Leisure Sales',
                       'Personal Development']        



    wk = pd.DataFrame(data)
    
    wk['hrs'] = wk['hrs'].str.replace(' hrs','')
    wk['hrs'][wk['hrs'] == ''] = '0'
    wk.hrs = wk.hrs.apply(lambda x: x.split(','))
    wk.date = wk.date.apply(str)
    wk.date = wk.date.apply(lambda x: x.split(','))
    wk.date = wk.date.apply(lambda x: pd.to_datetime(x, utc = True))
    wk['date_hrs'] = zip(wk.date,wk.hrs)
    
    wk_v1 = wk[['task_name','date_hrs','labels']]
    
    cust_data_set = []
    for index, row in wk_v1.iterrows():
        datelist = row[1][0]
        timelist = row[1][1]    
        type_dep_list = row[2]   

        
        for i in range(0, len(datelist)):
            line = []                    
            line.append(row[0]) # append task_name for ease        
            line.append(datelist[i])
            line.append(timelist[i])     
            line.append(type_dep_list)
            cust_data_set.append(line)
            
        wk_v2 = pd.DataFrame(cust_data_set, columns = ['task_name','date','hrs','labels'])
    
    
        for index, row in wk_v2.iterrows():
            row0 = row[3].split(',')
            num_labels = len(row0)

            if num_labels == 0:
                break
            
            if num_labels == 1:
                if row0[0] in operations:
                    wk_v2.loc[index, 'operations'] = row0[0]
                if row0[0] in departments:
                    wk_v2.loc[index, 'departments'] = row0[0]
                    
            if num_labels == 2:
                if row0[0] in operations:    
                    wk_v2.loc[index, 'operations'] = row0[0]
                if row0[0] in departments:
                    wk_v2.loc[index,'departments'] = row0[0]
            
                if row0[1] in operations:    
                    wk_v2.loc[index, 'operations'] = row0[1]
                if row0[1] in departments:
                    wk_v2.loc[index,'departments'] = row0[1]
                    
                    
                    
                    
                    
    wk_v2['hrs'] = wk_v2['hrs'].apply(float)
    del wk_v2['labels']
    return wk_v2