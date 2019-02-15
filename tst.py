# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 17:29:15 2018

@author: marce
"""
#%%
import string 

st = 'Tv.'
street_ids = ['rua','avenida','estrada','travessa','praça', 'praia']


def street_type(st, street_ids):
    '''
    Takes a string with the possibly abbreviated street type and a list of 
    common non abbreviated versions  
    ''' 
    s = st.lower()
    s = s.translate(None, string.punctuation) 
    s_list = list(s.decode("utf-8"))
    for si in street_ids:
        si_list = list(si.decode("utf-8"))
        for pos, s_let in enumerate(s_list):     
            m = s_let in si_list[pos:]
            if m == False:
                break
            elif pos == len(s_list) -1:
                return(si) 
    return(st)
    
a = street_type(st,street_ids)
print(a)
#%%




        
