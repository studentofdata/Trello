# -*- coding: utf-8 -*-
"""
Created on Fri Aug 19 10:38:14 2016

@author: Cloud User
"""

import trello_pull
import os
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



def processData():
    
    data = trello_pull.generateTrelloData()
    
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
    wk['hrs'] = wk['hrs'].str.replace(' hrs','')
    wk['hrs'][wk['hrs'] == ''] = '0'
    wk.hrs = wk.hrs.apply(str)
    wk.hrs = wk.hrs.apply(lambda x: x.split(','))
    
    for index, row in wk.iterrows():
        hrs = row['hrs']
        hrs = map(int, hrs)       
        hrs_sum = sum(hrs)
        wk.loc[index, 'hrs'] = hrs_sum
    
    
    spacen = lambda x: pd.Series([i for i in reversed(x.split(','))])
    wk_new_labels = wk['labels'].apply(spacen)
    wk_new_labels['name'] = wk['name']
    
    wk_v1 = pd.merge(wk, wk_new_labels, on = 'name')
    
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
            
    
    wk_v2 = wk_v1[['ids','hrs','labels','name','departments','operations']]


    return wk_v2
