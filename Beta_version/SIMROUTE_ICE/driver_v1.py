# -*- coding: utf-8 -*-
"""
Created on Tue Sep  7 17:29:26 2021

@author: polbl
"""


"""Data download"""
# import os
# exec(open("get_waves_CMEMS.py").read());
    
# """Data interpolation"""    
# from params import *
# if wave_prod==7:   
#     print('Executing make_waves:')
#     exec(open("make_waves.py").read()) 
#     print('make_waves executed!')
    
#     import os
    
#     print('Executing make_ice:')
#     exec(open("make_ice.py").read())
#     print('make_ice executed!')
# else:
#     import os
#     exec(open("get_waves_CMEMS.py").read());
    
#     print('Executing make_waves:')
#     exec(open("make_waves.py").read()) 
#     print('make_waves executed!')
        


"""Simulation 1"""
import os
from params import *
import datetime

nodIni=nod1_n
origin=nod1_name
nodEnd=nod2_n
destination=nod2_name

d1 = datetime.date(date_Ini[0],date_Ini[1],date_Ini[2])

name_Simu=origin+'_'+destination+'_'+'v'+d1.strftime('%m%d')+'_'+d1.strftime('%Y')+"WEN{}".format(WEN_form)+"inc{}".format(inc)



exec(open("main.py").read())

# # exec(open("PostProcesing_tools/Plot_routes.py").read())
# # exec(open("PostProcesing_tools/Plot_routes_and_waves_projected.py").read())

""""Simulation 2"""
import os
from params import *
import datetime

nodIni=nod2_n
origin=nod2_name
nodEnd=nod1_n
destination=nod1_name

d1 = datetime.date(date_Ini[0],date_Ini[1],date_Ini[2])

name_Simu=origin+'_'+destination+'_'+'v'+d1.strftime('%m%d')+'_'+d1.strftime('%Y')+"WEN{}".format(WEN_form)+"inc{}".format(inc)

exec(open("main.py").read())

# exec(open("PostProcesing_tools/Plot_routes.py").read())
# exec(open("PostProcesing_tools/Plot_routes_and_waves_projected.py").read())

# del(ARX)





