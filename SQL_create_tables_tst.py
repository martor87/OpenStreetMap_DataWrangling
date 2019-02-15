# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 11:49:14 2018

@author: marce
"""
#%%
import pandas as pd
import os
import csv
os.chdir('C:/Users/marce/Documents/6_DS_Projects/projects/2_Udacity_P1_Data_Wrangling')

df = pd.read_csv('5_db/ways_tags.csv', sep=',')
#i = 0
#
#with open(, encoding="utf8") as csvfile:
#    csvReader = csv.reader(csvfile, delimiter=',', quotechar='"' )        
#    next(csvReader, None)
#    for row in csvReader:
#        df.append(row)
       
print(df)

        