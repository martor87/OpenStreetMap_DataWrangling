# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 13:44:04 2018
@author: marcel torretta
"""
import sqlite3
import pandas as pd 
import os
import csv
os.chdir('C:/Users/marce/Documents/6_DS_Projects/projects/2_Udacity_P1_Data_Wrangling')


#%%
with sqlite3.connect("C:/sqlite-windows/sqlite_windows/Udacity_P1/Udacity_P1.sqlite") as db:
    c = db.cursor() 
    
#    c.execute(" ")
    
    QUERY = '''
    select * from nodes_tags where key == 'address'
    
    '''  
    table = pd.read_sql_query(QUERY, db)      
    pd.set_option('display.max_colwidth', -1)
    print(table)
#
#    Table Names
#    table = pd.read_sql_query("SELECT * from sqlite_master", db)
#    print(table)
#%%     
# Get first word of street name    
table0 = table['value'].str.split().str.get(0)

tableset = []
for i in table0:
    if i not in tableset:
        tableset.append(i)
        
pd.DataFrame(tableset)

#%%

with sqlite3.connect("C:/sqlite-windows/sqlite_windows/Udacity_P1/Udacity_P1.sqlite") as db:
    c = db.cursor() 

    QUERY1 = '''
    select id, key, value, type from nodes_tags
    where key == 'suburb' and value LIKE '%vea%'
    order by id, key    
    '''

    table = pd.read_sql_query(QUERY1, db)      
    pd.set_option('display.max_colwidth', -1)
    print(table)
    
zonasul  = [ 
            'Botafogo',
            'Catete',
            'Copacabana',
            'Cosme Velho',
            'Flamengo',
            'Gávea',
            'Glória',
            'Humaitá',
            'Ipanema',
            'Jardim Botânico',
            'Laranjeiras',
            'Largo do Machado',
            'Leme',
            'Rocinha',
            'São Conrado',
            'Silvestre',
            'Urca']

#%%


#with sqlite3.connect("C:/sqlite-windows/sqlite_windows/Udacity_P1/Udacity_P1.sqlite") as db:
#    c = db.cursor() 
#
#    QUERY1 = '''
#    select id, key, value, type from nodes_tags
#    where key == 'street' or key == 'housenumber' or key = 'address'
#    order by id, key    
#    '''
#
#    table = pd.read_sql_query(QUERY1, db)      
#    pd.set_option('display.max_colwidth', -1)
#    print(table[100:200])


#%%
#    #get street type from nodes_tags and ways_tags
#    QUERY1 = '''
#    select value from nodes_tags
#    where key like '%street%' or key like '%Endereco%' or lower(key) like '%endereco%' 
#    union     
#    select value from ways_tags
#    where key like '%street%' 
#    union
#    select value from ways_tags
#    where key like '%name%' and 
#    id == (select id from ways_tags where key = 'highway')


