# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 18:55:12 2018
@author: marcel torretta
"""
'''
This function modifies the database in the following way:
Creates a new 'address' key which has an associated 'value' = 'StreetName, Housenumber'
which are taken from keys = 'street' and key = 'housenumber'
This is performed once for each ID.
IDs which did not contain street nor housenumber keys won't have their new 'address'
key saved.

Then, a few keys in Portuguese are translated back to their common English tags.

The aim is to improve consistency among different types of address sources in the dataset.
'''
import sqlite3
import pandas as pd     

#%%
def fix_address(db_table):
    'To be applied on nodes_tags and ways_tags'
    
    # Grab all instances of relevant rows
    with sqlite3.connect("C:/sqlite-windows/sqlite_windows/Udacity_P1/Udacity_P1.sqlite") as db:
        c = db.cursor() 
        QUERY1 = '''
        select id, key, value, type from {}
        where key == 'street' or key == 'housenumber'  
        order by id, key    
        '''.format(db_table)  
        table = pd.read_sql_query(QUERY1, db) 
        
    #For each id in the table, creates a new row combining street and housenumber information 
    rows_list = []
    for i in list(set(table['id'])):
        ap = {}    
        ap['id'] = i
        ap['key'] = 'address'
        try:
            st = table[(table.id == i) & (table.key == 'street')]['value'].item()
        except:
            st = 'no_streetname_info'
        try:
            hn = table[(table.id == i) & (table.key == 'housenumber')]['value'].item()
        except:
            hn = 'no_housenumber_info'
        val = st + ', ' + hn
        ap['value'] = val
        ap['type'] = 'addr'
        rows_list.append(ap)
        
    table_app = pd.DataFrame(rows_list)
    table_app = table_app[['id','key','value','type']]
    
    # Insert newly created address rows into database and delete the old onesm as well as NULL 'value' ones.
    with sqlite3.connect("C:/sqlite-windows/sqlite_windows/Udacity_P1/Udacity_P1.sqlite") as db:
        c = db.cursor() 
        for index, row in table_app.iterrows():    
            c.execute('insert into ' + db_table + ' values (?, ?, ?, ?);', [row[0],row[1],row[2],row[3]])
    
        c.execute('delete from '+db_table+' where key == \"street\" or key == \"housenumber\";')
        c.execute('delete from '+db_table+' where key == \"address\" and \"value\" is NULL')
    
    # Translate a few keys in portuguese to their common English keys.
    # Changes type to 'addr' if related to address.
    with sqlite3.connect("C:/sqlite-windows/sqlite_windows/Udacity_P1/Udacity_P1.sqlite") as db:
        c = db.cursor() 
        c.execute('update '+ db_table +' set key = \"address\", type = \"addr\" where upper(key) LIKE \"%ENDERE%\";')
        c.execute('update '+ db_table +' set key = \"suburb\", type = \"addr\" where upper(key) LIKE \"BAIRRO%\";')
        c.execute('update '+ db_table +' set key = \"phone\", type = \"regular\" where upper(key) LIKE \"%TELEFONE%\";')   
        
        
#%%
fix_address('nodes_tags')
fix_address('ways_tags')
        

#%%
# Checking results - not part of processing.
#with sqlite3.connect("C:/sqlite-windows/sqlite_windows/Udacity_P1/Udacity_P1.sqlite") as db:
#        c = db.cursor() 
#        QUERY1 = '''
#        select * from nodes_tags
#        where id == 2091671631
#        '''
#        table = pd.read_sql_query(QUERY1, db) 
#        print(table)
        
#%%
    

