#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 16:48:55 2025

@author: dolors
"""

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

prod='GLOBAL' 
#Simulation name
name_Simu='NINGBO_SINGPR'

date_Ini = [2023, 2, 23]  # [year,month,day]
date_End = [2023 , 2, 28]

#Mesh boundaries
LonMin=104.50
LonMax=123.5
LatMin=1.3
LatMax=30.5


#Grid-step in Miles
inc=1.5    #in nautical miles   

# Initial node in mesh:
nodEnd=888472

# Final node in mesh:
nodIni=6867

#Extension added at boundaries (in degrees)
dx= 0.5

dir_arx='storeWaves/'    

#Time resolution of CMEMS product:
time_res=3 # In hours: 1 for all regions except o 3 for the GLOBAL



#Initial start time of sailing from 00:00 (from 0 to 23 hours)
t_ini= 4

#Sailing velocity (in knots)
v0=16.1  # Cruising speed in nautical milles per hour (in knots)

#Formulation WEN (Wave Effect on Navigation)
    #Bowditch = 1; Aertessen = 2; Khokhlov = 3; no reduction = 4
WEN_form=2;

#Ship parameteres for WEN options 2 and 3. 
Lbp = 225; # ship's length between perpendiculars (in meters)
DWT = 8000; # ship's deadweight (in tons)

#Additional plot flags:
plot_nodes=1 #Yes=1 ; No=0
plot_waves=1 #Yes=1 ; No=0
plot_routes=1 #Yes=1 ; No=0

# END OF USER INPUTS   #######################