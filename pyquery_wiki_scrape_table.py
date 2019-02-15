# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 14:34:39 2018
By Marcel Torretta

The script below attempts to scrape all tables from the wikipedia page containing
a large set of possible Map_Features usually added to OpenStreetMap 

As of 09Feb, the script is unsuccessful, not being able to fetch all tables
"""


import os
os.chdir('C:/Users/marce/Documents/6_DS_Projects/projects/2_Udacity_P1_Data_Wrangling')
import pandas as pd

url = 'https://wiki.openstreetmap.org/wiki/Map_Features'

#%% Urllib + BeautifulSoup
import urllib3
from bs4 import BeautifulSoup
import lxml

http = urllib3.PoolManager()
response = http.request('GET', url)
bs_obj = BeautifulSoup(response.data.decode('utf-8'))

#dfs is a list of fetched tables
tables = bs_obj.findAll('table')
dfs = list()
for table in tables:
    df = pd.read_html(str(table))[0]
    dfs.append(df)

#Get list of keys - strings that appear in the 'key' column of all fetched tables
keys = []
for i in range(0,len(dfs)):
    for ii in dfs[i].iloc[:,0]:
        keys.append(ii)
print(keys)

#set of keys
keys_std = pd.Series(sorted(set(keys)))

#%%
        
# After some examination, I noticed that some keys from the wiki page were not present 
# in keys_std. Actually, whole tables seemed to be missing.
# In order to make sure this information was actually missing, and not only
# stored in unexpected ways, I searched for a few strings in any position of 
# the fetched tables, and they are indeed missing.

string = 'aeroway'        
sss = []
for i in range(0,len(dfs)):
    ss = []
    for ii in dfs[i]:
        s = sum(dfs[i][ii] == string)
        ss.append(s)
    sss.append(sum(ss))        
print(sum(sss))

# I tried quite a few different approaches suggested on blogs and StackOverflow (such
# as PyQuery, below ) but always got 17 tables from the wikipedia page, which is short
# of the actual number of tables

#%% PyQuery option to scrape tables from wikipedia
pq = PyQuery(url)
all_tables = pq(".wikitable")
print(len(all_tables))
            
