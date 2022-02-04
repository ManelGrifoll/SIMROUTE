#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 23:10:59 2020
Code part of SIMROUTE (UPC-BarcelonaTech)
version 31/01/2021
@author: manel grifoll (UPC-BarcelonaTech)

Plot_routes.py creates a plot with the minimu distance and optimized routes

"""
#Offset at boundary plots:
offset=0.5

#Coastline reoslution (in m)
res_ldc='10m'

name_Simu='Nuuk_Narvik_v1103_2088WEN4'

# END OF USER INPUTS   #######################

import numpy as np
import matplotlib.pyplot as plt
import math as math
import os
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.mpl.ticker as cticker 
# from driver_v1 import name_Simu

arx = '../out/'+name_Simu+'.npz'
if os.path.exists(arx) == False:
    print('Simulation '+arx+' not exist')
    raise SystemExit
    
dat = np.load(arx)
LonMin=dat['arr_0'][0]
LonMax=dat['arr_0'][1]
LatMin=dat['arr_0'][2]
LatMax=dat['arr_0'][3]
v0=dat['arr_0'][4]
inc=dat['arr_0'][5] 
nodIni=int(dat['arr_0'][6])
nodEnd=int(dat['arr_0'][7])
t_ini=int(dat['arr_0'][8])
time_res=int(dat['arr_0'][9])
WEN_form=int(dat['arr_0'][10])
Lbp=dat['arr_0'][11]
DWT=dat['arr_0'][12]

extend=[LonMin-offset,LonMax+offset, LatMin-offset, LatMax+offset]

hs=dat['arr_1']
fp=dat['arr_2']
dir=dat['arr_3']
L_Trip=dat['arr_6']
L_TripFix=dat['arr_7']
L_CostTrip=dat['arr_8']
L_ConsCostTrip=dat['arr_9']
L_CostFix=dat['arr_10']
ARX=dat['arr_11']

inc=inc/60.0    
#Re-build Mesh:
Nx=int(np.floor((LonMax-LonMin)/inc)+2)
Ny=int(np.floor((LatMax-LatMin)/inc)+2)
tira_lon=[]
for i in range(Nx):
    tira_lon.append(LonMin+i*inc)
tira_lat=[]
for j in range(Ny):  
    tira_lat.append(LatMin+j*inc)
nodes=np.zeros((Nx*Ny,2))
#print( ' Nx = {:6d} ---   Ny = {:4d}\n'.format(Nx,Ny))
#print('longituds    {:8.3f}    -----   {:8.3f} \n'.format(tira_lon[0],tira_lon[-1]))
#print('latituds     {:8.3f}    -----   {:8.3f} \n'.format(tira_lat[0],tira_lat[-1]))
for j in range(Ny):   
    for i in range(Nx):
        nodes[Nx*j +i,0]=tira_lon[i]
        nodes[Nx*j +i,1]=tira_lat[j]
inc=inc*60
print('Mesh Re-built')
vmax=np.nanmax(hs)  # maxix valor de hs posible en la simu (pel colorbar)
######################################################33
Xnod, Ynod = np.meshgrid(tira_lon,tira_lat)
lon=nodes[L_Trip[:],0]
lat=nodes[L_Trip[:],1]
lonc=nodes[L_TripFix[:],0]
latc=nodes[L_TripFix[:],1]

fig = plt.figure(figsize=(20,10))




LamC=ccrs.LambertConformal(central_longitude=(LonMin+LonMax)/2,central_latitude=(LatMin+LatMax)/2)
geo=ccrs.Geodetic()
ax1=plt.subplot(1,1,1, projection=LamC)
ax1.set_title(name_Simu+'SIMROUTE results (Lambert)')
ax1.plot(lonc,latc,'orange',transform=geo,label='Minimum distance route') 
ax1.plot(lon,lat,'m',transform=geo,label='Optimized route')  
ax1.plot(lonc[0],latc[0],'*',transform=geo,label='Departure')
ax1.plot(lonc[-1],latc[-1],'*r',transform=geo,label='Arrival') 
ax1.set_ylim(LatMin-offset,LatMax+offset)
ax1.set_xlim(LonMin-offset,LonMax+offset)
ax1.legend(loc='best') 

ax1.set_extent(extend,crs=ccrs.PlateCarree())
ax1.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False)
ax1.coastlines(resolution=res_ldc)
ax1.add_feature(cfeature.LAND)

name_fig='../out/SIMROUTE_'+name_Simu+'.png'
plt.savefig(name_fig) #, bbox_inches='tight')
plt.show()
print('Figure '+name_fig+' plotted')
    