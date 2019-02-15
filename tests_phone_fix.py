# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 09:52:51 2018

@author: marce
"""
phone = '55(55)911111111;5-555-22-2222-22'
postalcode = '22260090'
def phone_fix(phone):
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
        if ph[-9] == '9':
            pho = '+55-21-'+''.join(ph[-9:])
        else:
            pho = '+55-21-'+''.join(ph[-8:])

        pho_list.append(pho)
    return '; '.join(pho_list)

def postalcode_fix(postalcode):
    pc = []
    for p in postalcode:
        try:
            int(p)
            pc.append(p)
        except:
            pass    
    pcode = ''.join(pc[-8:-3])+'-'+''.join(pc[-3:])
    return pcode

print(phone_fix(phone))
#print(postalcode_fix(postalcode))
#%%
a = 'telefones'
a.startswith('telefone')

#%%





