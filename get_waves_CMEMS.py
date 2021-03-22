#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 23:10:59 2020
Code part of SIMROUTE (UPC-BarcelonaTech)
Version: 02 / 03 / 21
@author: manel grifoll (UPC-BarcelonaTech)
"""

from  params import *
import os
import datetime

#Data to donwnload wave files from CMEMS server:
date_Ini = [2020,6,20]#[year,month,day]
date_End = [2020,6,23] 

dir_waveDATA='storeWaves/'

#wave product (=1  GLOBAL OCEAN; = 2 MEDSEA; = 3 IBI; = 4 AENWS; = 5 BLKSEA; = 6 BAL; = 7 ARTIC )
wave_prod= 1

#Extension added at boundaries (in degrees)
dx= 0.5

#motu_path = ' /home/xarx/Downloads/motuclient-python/motuclient.py'
motu_path = '/home/manel/MANEL_POWER/motuclient-python/motuclient.py'
user     = ' -u mgrifoll2'
passwd   = ' -p Estufa@1714'
motu_web = ' --motu http://nrt.cmems-du.eu/motu-web/Motu'

# END OF USER INPUTS   #######################

if wave_prod==1:
    ### GLOBAL OCEAN
    CMEMS_service = ' --service-id GLOBAL_ANALYSIS_FORECAST_WAV_001_027-TDS'
    CMEMS_product=' --product-id global-analysis-forecast-wav-001-027 '
    varfll   = '--variable VHM0 --variable VMDR --variable VTPK'
    retall='--longitude-min ' + str(LonMin-dx)  +' --longitude-max '+ str(LonMax+dx) +' --latitude-min ' + str(LatMin-dx) + ' --latitude-max '+str(LatMax+dx)+' ' # Coordenades Limit.Cada cas especial
    prod='GLOBAL_'

if wave_prod==2:
    ### Service MEDSEA
    CMEMS_service = ' --service-id MEDSEA_ANALYSIS_FORECAST_WAV_006_017-TDS'
    CMEMS_product=' --product-id med00-hcmr-wav-an-fc-h '
    varfll   = '--variable VHM0 --variable VMDR --variable VTPK'
    retall='--longitude-min ' + str(LonMin-dx)  +' --longitude-max '+ str(LonMax+dx) +' --latitude-min ' + str(LatMin-dx) + ' --latitude-max '+str(LatMax+dx)+' ' # Coordenades Limit.Cada cas especial
    prod='MEDSEA_'
 
if wave_prod==3:
    ### Service IBI
    CMEMS_service = ' --service-id IBI_ANALYSIS_FORECAST_WAV_005_005-TDS'
    CMEMS_product=' --product-id dataset-ibi-analysis-forecast-wav-005-005-hourly '
    varfll   = '--variable VHM0 --variable VMDR --variable VTPK'
    retall='--longitude-min ' + str(LonMin-dx)  +' --longitude-max '+ str(LonMax+dx) +' --latitude-min ' + str(LatMin-dx) + ' --latitude-max '+str(LatMax+dx)+' ' # Coordenades Limit.Cada cas especial
    prod='IBI_'
    
if wave_prod==4:
    ### ATLANTIC - EUROPEAN NORTH WEST SHELF
    CMEMS_service = ' --service-id	NORTHWESTSHELF_ANALYSIS_FORECAST_WAV_004_014-TDS'
    CMEMS_product=' --product-id MetO-NWS-WAV-hi '
    varfll   = '--variable VHM0 --variable VMDR --variable VTPK'
    retall='--longitude-min ' + str(LonMin-dx)  +' --longitude-max '+ str(LonMax+dx) +' --latitude-min ' + str(LatMin-dx) + ' --latitude-max '+str(LatMax+dx)+' ' # Coordenades Limit.Cada cas especial
    prod='AENWS_'    

if wave_prod==5:
    ### BLKSEA_ANALYSIS_FORECAST_WAV_007_003
    CMEMS_service = ' --service-id	BLKSEA_ANALYSISFORECAST_WAV_007_003-TDS'
    CMEMS_product=' --product-id bs-hzg-wav-an-fc-h '
    varfll   = '--variable VHM0 --variable VMDR --variable VTPK'
    retall='--longitude-min ' + str(LonMin-dx)  +' --longitude-max '+ str(LonMax+dx) +' --latitude-min ' + str(LatMin-dx) + ' --latitude-max '+str(LatMax+dx)+' ' # Coordenades Limit.Cada cas especial
    prod='BLKSEA_'    

if wave_prod==6:
    ### BALTIC SEA
    CMEMS_service = ' --service-id	BALTICSEA_ANALYSISFORECAST_WAV_003_010-TDS'
    CMEMS_product=' --product-id dataset-bal-analysis-forecast-wav-hourly '
    varfll   = '--variable VHM0 --variable VMDR --variable VTPK'
    retall='--longitude-min ' + str(LonMin-dx)  +' --longitude-max '+ str(LonMax+dx) +' --latitude-min ' + str(LatMin-dx) + ' --latitude-max '+str(LatMax+dx)+' ' # Coordenades Limit.Cada cas especial
    prod='BALTIC_'    

if wave_prod==7:
    ### ARTIC SEA
    CMEMS_service = ' --service-id	ARCTIC_ANALYSIS_FORECAST_WAV_002_014-TDS'
    CMEMS_product=' --product-id dataset-wam-arctic-1hr3km-be '
    varfll   = '--variable VHM0 --variable VMDR --variable VTPK --variable SIC --variable SIT'
    retall='--longitude-min ' + str(LonMin-dx)  +' --longitude-max '+ str(LonMax+dx) +' --latitude-min ' + str(LatMin-dx) + ' --latitude-max '+str(LatMax+dx)+' ' # Coordenades Limit.Cada cas especial
    prod='ARTIC_' 

###################################################
# 	Baixa les dades
###################################################
###################################################
d1 = datetime.date(date_Ini[0],date_Ini[1],date_Ini[2])
d2 = datetime.date(date_End[0],date_End[1],date_End[2])

incDies=datetime.timedelta(days=1)
files = []
for i in range((d2-d1).days+1):
    d=d1+incDies*i
    datelim  = ' --date-min "'+ d.strftime('%Y-%m-%d')+' 00:00:00" --date-max "'+d.strftime('%Y-%m-%d')+' 23:00:00" '    
    filename= dir_waveDATA+'Waves_'+prod+d.strftime('%Y%m%d')+'.nc'
    print ('Downloading ' + filename )
    options = motu_path+user+passwd+motu_web+CMEMS_service+ CMEMS_product+ retall +datelim + varfll +' --out-name '+filename
    print(options)
    os.system(options)
    files.append(filename)
print ('==================================================')
stf=''
for file in files:
    if os.path.exists(file):
        st='File '+file+ '   Downloaded file\n'
    else:
        st='File '+file+ '  No downloaded!\n'
        stf='  With problems'
    print(st)

    
print (' ++++++++++++++++++++++++++++++++++ ')
print (' get_waves_CMEMS.py executed'+ stf)
print ('+++++++++++++++++++++++++++++++++++++')



