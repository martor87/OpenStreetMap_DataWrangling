# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 13:44:04 2018

@author: marcel torretta
"""
import sqlite3
# import pandas as pd 
import os
import csv
os.chdir('C:/Users/marce/Documents/6_DS_Projects/projects/2_Udacity_P1_Data_Wrangling')

create = [
'''CREATE TABLE raw_nodes (
    id INTEGER PRIMARY KEY NOT NULL,
    lat REAL,
    lon REAL,
    user TEXT,
    uid INTEGER,
    version INTEGER,
    changeset INTEGER,
    timestamp TEXT
);
''',
'''CREATE TABLE raw_nodes_tags (
    id INTEGER,
    key TEXT,
    value TEXT,
    type TEXT,
    FOREIGN KEY (id) REFERENCES raw_nodes(id)
);
''',
'''CREATE TABLE raw_ways (
    id INTEGER PRIMARY KEY NOT NULL,
    user TEXT,
    uid INTEGER,
    version TEXT,
    changeset INTEGER,
    timestamp TEXT
);
''',
'''CREATE TABLE raw_ways_tags (
    id INTEGER NOT NULL,
    key TEXT NOT NULL,
    value TEXT NOT NULL,
    type TEXT,
    FOREIGN KEY (id) REFERENCES raw_ways(id)
);
''',
'''CREATE TABLE raw_ways_nodes (
    id INTEGER NOT NULL,
    node_id INTEGER NOT NULL,
    position INTEGER NOT NULL,
    FOREIGN KEY (id) REFERENCES raw_ways(id),
    FOREIGN KEY (node_id) REFERENCES raw_nodes(id)
);
'''
]

csvs = ['raw_nodes','raw_ways','raw_nodes_tags','raw_ways_tags','raw_nodes_ways']
#%%

with sqlite3.connect("C:/sqlite-windows/sqlite_windows/Udacity_P1/raw_Udacity_P1.sqlite") as db:
    c = db.cursor() 
    
    c.execute('drop table raw_nodes;')
    c.execute('drop table raw_nodes_tags;')
    c.execute('drop table raw_ways;')
    c.execute('drop table raw_ways_tags;')
    c.execute('drop table raw_ways_nodes;')
    
    for i in create:
        command = i
        try:
            c.execute(command)
        except:
            print('Command not executed for', i)
    # if running in Python 3, the encoding argument is necessary
    with open('5_db/raw_nodes.csv', encoding="utf8") as csvfile:
        csvReader = csv.reader(csvfile, delimiter=',', quotechar='"' )        
        next(csvReader, None)
        for row in csvReader:
            if row:
                c.execute('insert into raw_nodes values (?, ?, ?, ?, ?, ?, ?, ?)', row)

    with open('5_db/raw_nodes_tags.csv', encoding="utf8") as csvfile:
        csvReader = csv.reader(csvfile, delimiter=',', quotechar='"' )        
        next(csvReader, None)
        for row in csvReader:
            if row:
                c.execute('insert into raw_nodes_tags values (?, ?, ?, ?)', row)

                    
    with open('5_db/raw_ways.csv', encoding="utf8") as csvfile:
        csvReader = csv.reader(csvfile, delimiter=',', quotechar='"' )        
        next(csvReader, None)
        for row in csvReader:
            if row:
                c.execute('insert into raw_ways values (?, ?, ?, ?, ?, ?)', row)

                
    with open('5_db/raw_ways_tags.csv', encoding="utf8") as csvfile:
        csvReader = csv.reader(csvfile, delimiter=',', quotechar='"' )        
        next(csvReader, None)
        for row in csvReader:
            if row:
                c.execute('insert into raw_ways_tags values (?, ?, ?, ?)', row)
               
    with open('5_db/raw_ways_nodes.csv', encoding="utf8") as csvfile:
        csvReader = csv.reader(csvfile, delimiter=',', quotechar='"' )        
        next(csvReader, None)
        for row in csvReader:
            if row:
                c.execute('insert into raw_ways_nodes values (?, ?, ?)', row)        
        




