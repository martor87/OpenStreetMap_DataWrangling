# -*- coding: utf-8 -*-
"""
Created on Sun Feb 11 19:23:52 2018

@author: marce
"""

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
os.chdir('C:/Users/marce/Documents/6_DS_Projects/projects/2_Udacity_P1_Data_Wrangling/2_scripts')
os.getcwd()
import schema2
SCHEMA = schema2.schema
import cerberus
import string

#%%
import os
os.chdir('C:/Users/marce/Documents/6_DS_Projects/projects/2_Udacity_P1_Data_Wrangling')
import csv
import codecs
import pprint
import re
import xml.etree.cElementTree as ET

OSM_PATH = "1.1_input_sample/rio_sample_k20.osm"
#OSM_PATH = "1_input_data/rio-de-janeiro_brazil.osm/rio-de-janeiro_brazil.osm"
#OSM_PATH = "1_input_data/map"

NODES_PATH = "5_db/nodes.csv"
NODE_TAGS_PATH = "5_db/nodes_tags.csv"
WAYS_PATH = "5_db/ways.csv"
WAY_NODES_PATH = "5_db/ways_nodes.csv"
WAY_TAGS_PATH = "5_db/ways_tags.csv"


COLON = re.compile(r'^([A-Za-z]|_)+:([A-Za-z]|_)+') #Rio de Janeiro's OSM data contains 'IPP:key' keys, therefore the regex has to account for upper case as well.
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

# Make sure the fields order in the csvs matches the column order in the sql table schema
NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']

# List of common street types full names in Portuguese, used as searching reference
# to fix abbreviations. Can be updated.
# Obs.: 'praça' was substituted by 'pracça' allowing match for abreviations such as 'pca'
street_ids = ['via', 'rua','avenida', 'ladeira', 'alameda', 'estrada', 
              'travessa', 'pracça', 'praia', 'caminho', 'largo', 'rodovia']
            

# ================================================== #
#               Helper Functions                     #
# ================================================== #

def street_type_fix(st, street_ids = street_ids):
    '''
    Takes a string 'st' with the possibly abbreviated street type and a list
    'street ids' of common non-abbreviated versions. 
    Compares the string to each item in the list and returns the non abbreviated version.
    ''' 
    st0 = st.split()[0] #Gets first word of street, the street 'type'
    s = st0.lower()
    s = s.translate(None, string.punctuation) 
    s_list = list(s.decode("utf-8"))
    for si in street_ids:  
        si_list = list(si.decode("utf-8"))
        for pos, s_let in enumerate(s_list):     
            m = s_let in si_list[pos:]
            if m == False:
                break
            elif pos == len(s_list) -1:
                if si == 'pracça': # correct word is 'praça', see note on street_ids comment.
                    si = 'praça' 
                ans = si + " "+" ".join(st.split()[1:]) # Join processed street type with rest of street name               
                ans = " ".join(w.capitalize() for w in ans.split())  #Capitalizes first letter of each word. title() method doesn't work well with 'ç' and special characters.  
                return(ans) 
    return(st)    
    '''
    Function explanation:
    The nested for loop compares the given string with each item in the list 
    in the following fashion:     
        string: 'Av.'     
        # Note that the position of the letter being searched 
        limits the street_id string accordingly.
        Is 'a' in via ? Yes
        Is 'v' in 'ia' ? No, next item
        Is 'a' in 'rua'? Yes
        Is 'v' in 'ua' ? No, next
        Is 'a' in 'avenida' ? Yes
        Is 'v' in 'venida' ? Yes
        Returns 'Avenida'. 
        If no match is found, returns the original string.
    This method may not be completely fool-proof but is considerably more 
    robust than a dictionary {refecence-version: possibly-abbreviated-versions},
    since abbreviations of the kind are quite loose when human-entered.
    '''   
    
def phone_fix(phone):
    '''
    Standardizes phone numbers on the dataset
    Joins country and area code to 8 last numbers of phone string (9 if mobile number)
    It handles well multiple phone numbers, if separated by ';'
    '''    
    phone_list = phone.split(';')
    pho_list = []
    for p in phone_list:
        ph = []
        for digit in p:
            try:
                int(digit)
                ph.append(digit)
            except:
                pass    
        if (len(ph) > 8 and ph[-9] in [8,9]):
            pho = '+55-21-'+''.join(ph[-9:])
        else:
            pho = '+55-21-'+''.join(ph[-8:])
        pho_list.append(pho)
    return '; '.join(pho_list)

def postalcode_fix(postalcode):
    'Standardizes postal codes on the dataset'
    pc = []
    for p in postalcode:
        try:
            int(p)
            pc.append(p)
        except:
            pass    
    pcode = ''.join(pc[-8:-3])+'-'+''.join(pc[-3:])
    return pcode

def shape_element(element, node_attr_fields=NODE_FIELDS, way_attr_fields=WAY_FIELDS,
                  problem_chars=PROBLEMCHARS, default_tag_type='regular'):
    """Clean and shape node or way XML element to Python dict"""
    

    node_attribs = {}
    way_attribs = {}
    way_nodes = []
    tags = []  
    if element.tag == 'node':        
        for i in NODE_FIELDS:
            node_attribs.update({i: element.attrib[i]})
        for child in element:
            if child.tag == 'tag':
                m = re.match(PROBLEMCHARS, child.attrib['k'])
                if m:
                    continue
                else:
                    dic = {}
                    dic['id'] = element.attrib['id']
                    dic['value'] = child.attrib['v']
                    m = re.match(COLON, child.attrib['k']) 
                    if m:
                        dic['key'] = ':'.join(m.string.split(':')[1:])
                        dic['type'] = m.string.split(':')[0]
                    else:
                        dic['key'] = child.attrib['k']
                        dic['type'] = 'regular' 
                        
                ''' The following 'ifs' apply the _fix functions on parsed street names, 
                phone numbers and postal codes as a mean of standardizing the dataset'''   
                if(dic['key'].lower() == 'street' or 
                   dic['key'].lower() == 'endereco'):             
                    st = child.attrib['v'].encode('utf-8')
                    try:                         
                        dic['value'] = street_type_fix(st)                                           
                    except:
                        pass
                
                if(dic['key'].lower().startswith('phone') or  
                   dic['key'].lower().startswith('telefone')):
                    phone = dic['value']
                    dic['value'] = phone_fix(phone)

                if(dic['key'].lower() == 'postcode'):
                    postcode = dic['value']
                    dic['value'] = postalcode_fix(postcode)                    
                    
                tags.append(dic)

        return {'node': node_attribs, 'node_tags': tags}    
    
    elif element.tag == 'way':
        pos = 0
        for i in WAY_FIELDS:
            way_attribs.update({i: element.attrib[i]})
        for child in element:
            if child.tag == 'tag':
                m = re.match(PROBLEMCHARS, child.attrib['k'])
                if m:
                    continue
                else:
                    dic = {}
                    dic['id'] = element.attrib['id']
                    dic['value'] = child.attrib['v']
                    m = re.match(COLON, child.attrib['k']) 
                    if m:
                        dic['key'] = ':'.join(m.string.split(':')[1:])
                        dic['type'] = m.string.split(':')[0]
                    else:
                        dic['key'] = child.attrib['k']
                        dic['type'] = 'regular'        
                                   
                if(dic['key'].lower() == 'street' or 
                   dic['key'].lower() == 'endereco'):                    
                    st = child.attrib['v'].encode('utf-8')
                    try:                         
                        dic['value'] = street_type(st)                                           
                    except:
                        pass
                
                if(dic['key'].lower().startswith('phone') or  
                   dic['key'].lower().startswith('telefone')):
                    phone = dic['value']
                    dic['value'] = phone_fix(phone)

                if(dic['key'].lower() == 'postcode'):
                    postcode = dic['value']
                    dic['value'] = postalcode_fix(postcode)                    
                    
                    
                tags.append(dic)
                
            if child.tag == 'nd':
                dic = {}
                i = 0
                dic = {}
                dic['id'] = element.attrib['id']
                dic['node_id'] = child.attrib['ref']
                dic['position'] = pos
                pos += 1
                
                way_nodes.append(dic)

        return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}

     

def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag"""

    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


def validate_element(element, validator, schema=SCHEMA):
    """Raise ValidationError if element does not match schema"""
    if validator.validate(element, schema) is not True:
        field, errors = next(validator.errors.iteritems())
        message_string = "\nElement of type '{0}' has the following errors:\n{1}"
        error_string = pprint.pformat(errors)
        
        raise Exception(message_string.format(field, error_string))


class UnicodeDictWriter(csv.DictWriter, object):
    """Extend csv.DictWriter to handle Unicode input"""

    def writerow(self, row):
        super(UnicodeDictWriter, self).writerow({
            k: (v.encode('utf-8') if isinstance(v, unicode) else v) for k, v in row.iteritems()
        })

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


# ================================================== #
#               Main Function                        #
# ================================================== #
def process_map(file_in, validate):
    """Iteratively process each XML element and write to csv(s)"""

    with codecs.open(NODES_PATH, 'w') as nodes_file, \
         codecs.open(NODE_TAGS_PATH, 'w') as nodes_tags_file, \
         codecs.open(WAYS_PATH, 'w') as ways_file, \
         codecs.open(WAY_NODES_PATH, 'w') as way_nodes_file, \
         codecs.open(WAY_TAGS_PATH, 'w') as way_tags_file:

        nodes_writer = UnicodeDictWriter(nodes_file, NODE_FIELDS)
        node_tags_writer = UnicodeDictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
        ways_writer = UnicodeDictWriter(ways_file, WAY_FIELDS)
        way_nodes_writer = UnicodeDictWriter(way_nodes_file, WAY_NODES_FIELDS)
        way_tags_writer = UnicodeDictWriter(way_tags_file, WAY_TAGS_FIELDS)

        nodes_writer.writeheader()
        node_tags_writer.writeheader()
        ways_writer.writeheader()
        way_nodes_writer.writeheader()
        way_tags_writer.writeheader()

        validator = cerberus.Validator()

        for element in get_element(file_in, tags=('node', 'way')):
            el = shape_element(element)
            if el:
                if validate is True:
                    validate_element(el, validator)

                if element.tag == 'node':
                    nodes_writer.writerow(el['node'])
                    node_tags_writer.writerows(el['node_tags'])
                elif element.tag == 'way':
                    ways_writer.writerow(el['way'])
                    way_nodes_writer.writerows(el['way_nodes'])
                    way_tags_writer.writerows(el['way_tags'])


if __name__ == '__main__':
    # Note: Validation is ~ 10X slower. For the project consider using a small
    # sample of the map when validating.
    process_map(OSM_PATH, validate=False)
    
    
    
    
    
    
    
    
    
    

