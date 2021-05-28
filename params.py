#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 23:10:59 2020
This code is part of SIMROUTE
@author: manel grifoll (UPC-BarcelonaTech)

params.py: parameters file for the case Palma Mallorca - Barcelona
"""
import numpy  as np
from pathlib import Path
import matplotlib.pyplot as plt

#Simulation name
name_Simu='Palma_Barna'

#Mesh boundaries
LonMin=2.0
LonMax=5.1
LatMin=38.95
LatMax=41.65

#Grid-step in Miles
inc=1.5    #in nautical miles   

# Initial node in mesh:
nodIni=1411

# Final node in mesh:
nodEnd=12781
   
ARX=['Waves_MEDSEA_20200120.nc','Waves_MEDSEA_20200121.nc'] 
dir_arx='storeWaves/'    

#Time resolution of CMEMS product:
time_res=1 # In hours: 1 for all regions except o 3 for the GLOBAL

#Wave interpolated file (output): 
arx_waves= 'in/waves.npz'

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