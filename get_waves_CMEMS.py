#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 23:10:59 2020
Code part of SIMROUTE (UPC-BarcelonaTech)
Version: 02 / 03 / 21
@author: manel grifoll (UPC-BarcelonaTech)
"""
from simroute import *      #Aquest modul ja carrega el parms_PROD
import os
import datetime
import copernicusmarine



# END OF USER INPUTS   #######################

if prod=='GLOBAL':
    ### GLOBAL OCEAN
   # CMEMS_service = ' --service-id GLOBAL_ANALYSIS_FORECAST_WAV_001_027-TDS'
   # CMEMS_product=' --product-id global-analysis-forecast-wav-001-027 '
    varfll   = '--variable VHM0 --variable VMDR --variable VTPK'
    retall='--longitude-min ' + str(LonMin-dx)  +' --longitude-max '+ str(LonMax+dx) +' --latitude-min ' + str(LatMin-dx) + ' --latitude-max '+str(LatMax+dx)+' ' # Coordenades Limit.Cada cas especial
    ID_DTSET='cmems_mod_glo_wav_anfc_0.083deg_PT3H-i'
    DT_VER="202411"
    # a partir del   1/11/2022 03:00
if prod=='MEDSEA':
    ### Service MEDSEA
    ID_DTSET="cmems_mod_med_wav_anfc_4.2km_PT1H-i"
    #ID_DTSET='MEDSEA_MULTIYEAR_WAV_006_012'  
    #ID_DTSET='omi_var_extreme_wmf_medsea_area_averaged_mean'
    DT_VER=''
if prod=='IBI':
    ### Service IBI
    ID_DTSET = 'cmems_mod_ibi_wav_anfc_0.027deg_PT1H-i'
    DT_VER=''
if prod=='AENWS':
    ### ATLANTIC - EUROPEAN NORTH WEST SHELF
    ID_DTSET='MetO-NWS-WAV-RAN'
    DT_VER=''
if prod=='BLKSEA':
    ### BLKSEA_ANALYSIS_FORECAST_WAV_007_003
    ID_DTSET='cmems_mod_blk_wav_anfc_2.5km_PT1H-i'   
    DT_VER=''
if prod=='BALTIC':
    ### BALTIC SEA                                                                 
    ID_DTSET ='cmems_mod_bal_wav_anfc_PT1H-i'
    DT_VER=''
# if prod=='ARTIC':    NO Existeix
#     ### ARTIC SEA
#      DT_VER=''
#     ID_DTSET='ARCTIC_MULTIYEAR_WAV_002_013'
    
   # ID_DTSET='ARCTIC_MULTIYEAR_WAV_002_013'

####################
d1 = datetime.date(date_Ini[0],date_Ini[1],date_Ini[2])
d2 = datetime.date(date_End[0],date_End[1],date_End[2])
nomw1=d1.strftime('%Y-%m-%d')
dt_min= nomw1+'T00:00:00' 
nomw2=d2.strftime('%Y-%m-%d')
dt_max= nomw2+'T23:59:59' 
nomarx='Waves_'+name_Simu+'_'+nomw1+'%'+nomw2+'.nc'
print(dt_min,dt_max)
print(nomarx)

####################

copernicusmarine.subset(
        dataset_id=ID_DTSET,
        dataset_version=DT_VER,
        dataset_part='',
        variables=["VHM0", "VMDR"],
        minimum_longitude=LonMin-dx,
        maximum_longitude=LonMax+dx,
        minimum_latitude=LatMin-dx,
        maximum_latitude=LatMax+dx,
        start_datetime=dt_min,
        end_datetime=dt_max,
        overwrite = True,
        coordinates_selection_method="strict-inside",
        output_filename=nomarx ,
        disable_progress_bar=False,
        output_directory=dir_arx 
        
    )
 

        
    