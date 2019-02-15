# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 17:29:15 2018

@author: marce
"""
#%%
import string 
#%%

st = 'Avá Adalbérto Ferreira'
street_ids = ['via', 'rua','avenida', 'ladeira', 'alameda', 'estrada', 
              'travessa', 'praça', 'praia', 'caminho', 'largo', 'rodovia']

def street_type(st, street_ids):
    '''
    Takes a string with the possibly abbreviated street type and a list of 
    common non abbreviated versions, returns the non abbreviated version.
    ''' 
    st0 = st.split()[0]
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
                ans = si + " "+" ".join(st.split()[1:]) # Join processed street type with rest of street name               
                ans = " ".join(w.capitalize() for w in ans.split())  #Capitalizes first letter of each word. title() method doesn't work well with 'ç' and special characters.  
                return(ans.title()) 
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
    This method is not fool-proof but considerably more robust than a dictionary  
    {refecence-version: possibly-abbreviated-versions}, since abbreviations
    are quite loose when human-entered.
    '''
a = street_type(st,street_ids)
print(a)
#%%




        
