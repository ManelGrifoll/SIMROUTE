#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 23:10:59 2020
Code part of SIMROUTE (UPC-BarcelonaTech)
Version: 02 / 02 / 21
@author: manel grifoll (UPC-BarcelonaTech)
"""
import sys
import numpy  as np
from func_simroute_ice import * 
# from driver_v1 import *
from netCDF4 import Dataset 
import scipy.interpolate
import matplotlib.pyplot as plt
from params import *

# Plot ice after interpolation
plot_ice = False

# Time frame if plotting waves.
t=0

# END OF USER INPUTS   #######################
tic()

storeddatapath = 'C:/Users/polbl/OneDrive/Documents/SIMROUTE/storeWaves/'
ARX = os.listdir(storeddatapath)

Na=len(ARX)
nc=Dataset(dir_arx+ARX[0],'r')
if ARX[0].find('BALTIC')==6 or ARX[0].find('BLKSEA')==6:
    lon=nc.variables['lon'][:]
    lat=nc.variables['lat'][:]
    X,Y=np.meshgrid(lon,lat)
    nx=len(lon)
    ny=len(lat)
elif(ARX[0].find('ARTIC')==6):
    lon=nc.variables['lon'][:]
    lat=nc.variables['lat'][:]
    X=lon
    Y=lat
    ny,nx=lon.shape[:]
else:
    lon=nc.variables['longitude'][:]
    lat=nc.variables['latitude'][:]
    X,Y=np.meshgrid(lon,lat)
    nx=len(lon)
    ny=len(lat)

Xnod, Ynod = np.meshgrid(tira_lon,tira_lat)
#sys.exit()

# Ara coemncarem a construir la matriu de gel
afi=np.zeros(shape=(ny,nx))
thi=np.zeros(shape=(ny,nx))

af_rec=np.zeros(shape=(Ny,Nx,Na*int(24/time_res)))
th_rec=np.zeros(shape=(Ny,Nx,Na*int(24/time_res)))

'''
    Degut a que les variables extretes dels nc tenen un compotament diferent
    En el cas que  hagin punts "land" o que no hi hagi cap punt land hem de fer
    un procediment diferent en cada cas:
'''

mnc=Dataset(dir_arx+ARX[0],'r')
siaf=nc.variables['SIC'][0,:,:]
if isinstance(siaf.mask,np.ndarray) is False:
    print("No hi ha lands")
    msk = False
else:
    print('Hi ha ha lands')
    msk = True    
    
for n in range(Na):
    nc=Dataset(dir_arx+ARX[n],'r')
    print(dir_arx+ARX[n])
    toc()
    print('Day / Hour')
    for t in range(int(24/time_res)):
        print(n,t)
        maf=nc.variables['SIC'][t,:,:]
        for i in range(nx):
            for j in range(ny):
                if msk is True:                        
                    if   maf.mask[j,i]==False:
                         afi[j,i]=maf[j,i]     
                    else:
                        afi[j,i]=np.nan
                else:
                    afi[j,i]=maf[j,i]                         
        afg=scipy.interpolate.griddata((X.flatten(), Y.flatten()), 
                          (afi.flatten()) ,(Xnod,Ynod), method='linear')
        af_rec[:,:,t+int(24/time_res)*n]=afg[:,:]
        
        mth=nc.variables['SIT'][t,:,:]
        for i in range(nx):
            for j in range(ny):
                if msk is True:    
                    if   mth.mask[j,i]==False:
                         thi[j,i]=mth[j,i]     
                    else:        
                        thi[j,i]=np.nan
                else:
                    thi[j,i]=mth[j,i] 
        
        thg=scipy.interpolate.griddata((X.flatten(),Y.flatten()),
                         (thi.flatten()) , (Xnod,Ynod),method='linear')
        th_rec[:,:,t+int(24/time_res)*n]=thg[:,:]  
                
        
print('Interpolation done! Assigning ice at nodes')             
af=np.zeros(shape=(Nx*Ny,Na*int(24/time_res)))
af.fill(np.nan)
th=np.copy(af)


for t in  range(int(24/time_res)*Na):
    for j in range(Ny):
        for i in range(Nx):
            af[i+j*Nx,t]=af_rec[j,i,t];
            th[i+j*Nx,t]=th_rec[j,i,t];

#Nan extraction in Dir due to interpolation 
for i in  range(Nx*Ny):
    if  np.isnan(af[i,0])==False and np.isnan(th[i,0])==True:
                af[i,:]=np.nan
                print('algun nan fa la punyeta ',i,j)

if plot_ice is False:
    print("Delete intermediate variables.")       
    del th_rec
    del af_rec
print ("Checking nans in ice area fraction fields.")
[nn,tt]=af.shape
n=0
for i in range(nn):
    val_ini=np.isnan(af[i,0])
    for t in range(tt):
        if val_ini !=np.isnan(af[i,t]):
            af[i,:]=np.nan
            th[i,:]=np.nan
            n=n+1
            print(i,t,n)
            break
if n !=0:
    print('Find nans and eliminated :',n )


print("Done. Saving...")
            
np.savez_compressed(arx_ice,af,th)

toc()