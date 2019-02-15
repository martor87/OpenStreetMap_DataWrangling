# -*- coding: utf-8 -*-
"""
Created on Tue Feb 06 14:45:47 2018

@author: marcel torretta

This script extracts a sample of some OSM data (OpenStreetMap)
In this project, samples are used to test audit procedures before applying them to 
the whole dataset.
"""
import xml.etree.ElementTree as ET
import os
os.chdir('C:/Users/marce/Documents/6_DS_Projects/projects/2_Udacity_P1_Data_Wrangling')

OSM_FILE = "1_input_data/rio-de-janeiro_brazil.osm/rio-de-janeiro_brazil.osm"
SAMPLE_FILE = '1.1_input_sample/rio_sample_k20.osm'

#Change k to lower/higher values to get larger/smaller samples
k = 20

def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag

    Reference:
    http://stackoverflow.com/questions/3095434/inserting-newlines-in-xml-file-generated-via-xml-etree-elementtree-in-python
    """
    context = iter(ET.iterparse(osm_file, events=('start', 'end')))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


with open(SAMPLE_FILE, 'wb') as output:
    output.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    output.write('<osm>\n  ')

    # Write every kth top level element
    for i, element in enumerate(get_element(OSM_FILE)):
        if i % k == 0:
            output.write(ET.tostring(element, encoding='utf-8'))

    output.write('</osm>')