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

#Data to donwnload wave files from CMEMS server:
#CMEMS only has data from 2017-present
date_Ini = [2001,2,2]#[year,month,day]
date_End = [2088,2,10] 

#wave product (=1  GLOBAL OCEAN; = 2 MEDSEA; = 3 IBI; = 4 AENWS; = 5 BLKSEA; = 6 BAL; = 7 ARTIC )
wave_prod=7

#Mesh boundaries
LonMin=-93
LonMax=16
LatMin=56
LatMax=70

#Grid-step in Miles
inc=25   #in nautical miles   

# Initial node in mesh:
nod1_n=31734
nod1_name='Nuuk'

# Final node in mesh:

nod2_n=48536
nod2_name="Narvik"

   
dir_arx='storeWaves/' 

#Time resolution of CMEMS product:
time_res=1 # In hours: 1 for all regions except o 3 for the GLOBAL

#Wave interpolated file (output): 
arx_waves= 'in/waves.npz'
arx_ice= 'in/ice.npz'

#Initial start time of sailing from 00:00 (from 0 to 23 hours)
t_ini=28

#Sailing velocity (in knots)
v0=16  # Cruising speed in nautical milles per hour (in knots)

#Formulation WEN (Wave Effect on Navigation)
    #Bowditch = 1; Aertessen = 2; Khokhlov = 3; 
    #Bowditch w/ Ice = 4; Aertessen w/ Ice = 5; Khokhlov w/ Ice = 6;
    #only ice = 7
WEN_form=4;

Vessel_type='OW'

#Ship parameteres for WEN options 2 and 3. 
Lbp = 225; # ship's length between perpendiculars (in meters)
DWT = 8000; # ship's deadweight (in tons)

#Additional plot flags:
plot_nodes=1 #Yes=1 ; No=0
plot_waves=1 #Yes=1 ; No=0
plot_routes=1 #Yes=1 ; No=0

# END OF USER INPUTS   #######################