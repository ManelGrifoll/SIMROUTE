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
name_Simu='HV_NAIN'
prod='GLOBAL'   #  producte de onatge   

'''  ATENCIÖ  aqui posen la data de inici i final del onatge
'''
date_Ini = [2022, 12, 19]  # [year,month,day]
date_End = [2022, 12, 21]
#Mesh boundaries
LonMin=-61.5
LonMax=-56
LatMin=53
LatMax=57

#Grid-step in Miles
inc=1.5    #in nautical miles   
# Initial node in mesh:
nodIni=11502

# Final node in mesh:
nodEnd=31100
   
#Time resolution of CMEMS product:
time_res=3 # In hours: 1 for all regions except o 3 for the GLOBAL

#Extension added at boundaries (in degrees)
dx= 0.5
#Wave 

dir_arx='storeWaves/'  

#Initial start time of sailing from 00:00 (from 0 to 23 hours)
t_ini=9 

#Sailing velocity (in knots)
v0=16.1  # Cruising speed in nautical milles per hour (in knots)

#Formulation WEN (Wave Effect on Navigation)
    #Bowditch = 1; Aertessen = 2; Khokhlov = 3; no reduction = 4
WEN_form=1;

#Ship parameteres for WEN options 2 and 3. 
Lbp = 225; # ship's length between perpendiculars (in meters)
DWT = 8000; # ship's deadweight (in tons)

#Additional plot flags:
plot_nodes=1 #Yes=1 ; No=0
plot_waves=1 #Yes=1 ; No=0
plot_routes=1 #Yes=1 ; No=0

# END OF USER INPUTS   #######################