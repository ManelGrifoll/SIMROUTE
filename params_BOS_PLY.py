#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 23:10:59 2020
This code is part of SIMROUTE
@author: manel grifoll (UPC-BarcelonaTech)
"""
import numpy  as np
from pathlib import Path
import matplotlib.pyplot as plt
#Simulation name
name_Simu='BOS_PLY'
prod='GLOBAL'   #  producte de onatge   

'''  ATENCIÖ  aqui posen la data de inici i final del onatge
'''
date_Ini = [2023, 2, 23]  # [year,month,day]
date_End = [2023 , 3, 2]
#date_End = [2023 , 2, 27]
#Mesh boundaries
LonMin=-70.720
LonMax=-4.290
LatMin=42.0
LatMax=52.2

#Grid-step in Miles
inc=1.5    #in nautical miles   
# Initial node in mesh:
nodIni=106388

# Final node in mesh:
nodEnd=853524
   
#Time resolution of CMEMS product:
time_res=3 # In hours: 1 for all regions except o 3 for the GLOBAL i altres...

#Extension added at boundaries (in degrees)
dx= 0.5
#Wave 

dir_arx='storeWaves/'  

#Initial start time of sailing from 00:00 (from 0 to 23 hours)
t_ini=0 

#Sailing velocity (in knots)
v0=16.1  # Cruising speed in nautical milles per hour (in knots)

#Formulation WEN (Wave Effect on Navigation)
    #Bowditch = 1; Aertessen = 2; Khokhlov = 3; no reduction = 4
WEN_form=2;   # la 1 treu velocitat negativa Investigar

#Ship parameteres for WEN options 2 and 3. 
Lbp = 225; # ship's length between perpendiculars (in meters)
DWT = 8000; # ship's deadweight (in tons)

#Additional plot flags:
plot_nodes=1 #Yes=1 ; No=0
plot_waves=1 #Yes=1 ; No=0
plot_routes=1 #Yes=1 ; No=0

# END OF USER INPUTS   #######################
