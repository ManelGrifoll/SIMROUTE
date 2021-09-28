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

ARX=['Waves_GLOBAL_20200118.nc' , 'Waves_GLOBAL_20200119.nc' , 'Waves_GLOBAL_20200120.nc' , 'Waves_GLOBAL_20200121.nc' , 'Waves_GLOBAL_20200122.nc' , 'Waves_GLOBAL_20200123.nc' , 'Waves_GLOBAL_20200124.nc' , 'Waves_GLOBAL_20200125.nc'] 
dir_arx='storeWaves/'    

#Time resolution of CMEMS product:
time_res=3 # In hours: 1 for all regions except o 3 for the GLOBAL

#Wave interpolated file (output): 
arx_waves= 'in/waves.npz'

#Initial start time of sailing from 00:00 (from 0 to 23 hours)
t_ini= 0

#coastline source file:
arx_ldc= 'in/lcd_eu_h.dat'

#coastline name output: 
#    lcd_out= 'in/ldcK1.npz'

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
