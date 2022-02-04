#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 23:10:59 2020
Code part of SIMROUTE (UPC-BarcelonaTech)
version 5/02/2021
@author: manel grifoll (UPC-BarcelonaTech)
Plot_routes_and_waves_projected.py: creates a plots sequence of routes and waves in Lambert and Plate-Carre Projections
"""

#Simulation name:  
name_Simu='Narvik_Nuuk_v1101_2088WEN4'

#Offset at boundary plots (in degrees):
offset=0.2

#Interval of plotting frames (in hours)
inc_frame=20

#Coastline resolution (in m)
res_ldc='10m'

#Quiver lplot paramerters Plate-Carre:
sc_pc=100
regrid_shape_pc=20
width_pc = 0.002   

#Quiver plot paramerters Lambert:
sc_lam=140
regrid_shape_lam=20
width_lam = 0.002

# END OF USER INPUTS   #######################

import numpy as np
import matplotlib.pyplot as plt
import math as math
import os
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.mpl.ticker as cticker 
from func_postprocess import * 
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



hs=dat['arr_1']
fp=dat['arr_2']
dir=dat['arr_3']
th=dat['arr_4']
af=dat['arr_5']
L_Trip=dat['arr_6']
L_TripFix=dat['arr_7']
Cost_Opt=dat['arr_8']
L_ConsCostTrip=dat['arr_9']
Cost_Min=dat['arr_10']
ARX=dat['arr_10']

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
print('Mesh Re-built')
hsmax=np.nanmax(hs)

Xnod, Ynod = np.meshgrid(tira_lon,tira_lat)
Xnod, Ynod = np.meshgrid(tira_lon,tira_lat)
lon=nodes[L_Trip[:],0]
lat=nodes[L_Trip[:],1]
lonc=nodes[L_TripFix[:],0]
latc=nodes[L_TripFix[:],1]
nmax=Cost_Min[-1]
n=np.int_(np.arange(0,nmax,inc_frame))
#a=np.int_(n)
infotos=n.tolist() #passem a llista
infotos.append(int(np.ceil(nmax)))
#volem la ultima foto segur
print ('Plotting frames:',len(infotos))

######3
extent=[LonMin-offset,LonMax+offset, LatMin-offset, LatMax+offset]
pc=ccrs.PlateCarree()
LamC=ccrs.LambertConformal(central_longitude=(LonMin+LonMax)/2,central_latitude=(LatMin+LatMax)/2)
geo=ccrs.Geodetic()
####    
k=0   # numering files graphics
for t in infotos:
    if time_res==1:        
        hs_rec=hs[:,t].reshape((Ny,Nx))
        dir_rec=dir[:,t].reshape((Ny,Nx))+180
        th_rec=th[:,t].reshape((Ny,Nx))
    else:
        hs_rec=hs[:,np.int(np.round(t/3))].reshape((Ny,Nx))
        dir_rec=dir[:,np.int(np.round(t/3))].reshape((Ny,Nx))+180 
        th_rec=th[:,np.int(np.round(t/3))].reshape((Ny,Nx))
    
    U=hs_rec[:,:]*np.sin(np.deg2rad(dir_rec[:,:]))
    V=hs_rec[:,:]*np.cos(np.deg2rad(dir_rec[:,:]))    
    if t <Cost_Opt[-1]:
        tl=distL(Cost_Opt,t)   
    else:
        tl=len(Cost_Opt)
    if t <Cost_Min[-1]:
        tc=distL(Cost_Min,t)  
    else:
        tc=len(Cost_Min)
    lon=nodes[L_Trip[0:tl],0]
    lat=nodes[L_Trip[0:tl],1]
    lonc=nodes[L_TripFix[0:tc],0]
    latc=nodes[L_TripFix[0:tc],1]
    fig = plt.figure(figsize=(20,10))    
    
    ax1=plt.subplot(1,2,1, projection=LamC)
    strtim=name_Simu+' (LamberConf) time = {:.2f} hours'.format(t) 
    ax1.set_title(strtim)
    ax1.plot(lonc,latc,'orange',transform=geo,label='Minimum distance route') 
    ax1.plot(lon,lat,'m',transform=geo,label='Optimized route')  
    ax1.plot([nodes[nodIni,0]],[nodes[nodIni,1]],'^b',transform=geo,label='Departure')
    ax1.plot([nodes[nodEnd,0]],[nodes[nodEnd,1]],'*r',transform=geo,label='Arrival') 
    imat1= ax1.pcolor(Xnod,Ynod,hs_rec,vmin=0,vmax=hsmax,transform=pc)
    ax1.legend(loc='best') 
    ax1.quiver(Xnod, Ynod,U, V, regrid_shape=regrid_shape_lam,scale=sc_lam, width = width_lam,pivot='middle',transform=pc)
    ax1.set_extent(extent,crs=ccrs.PlateCarree())
    ax1.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False)
    ax1.coastlines(resolution=res_ldc)
    ax1.add_feature(cfeature.LAND)
    plt.colorbar(imat1)

    ax2=plt.subplot(1,2,2, projection=LamC)
    strtim=name_Simu+' (LamberConf) time = {:.2f} hours'.format(t) 
    ax2.set_title(strtim)
    ax2.plot(lonc,latc,'orange',transform=geo,label='Minimum distance route') 
    ax2.plot(lon,lat,'m',transform=geo,label='Optimized route')  
    ax2.plot([nodes[nodIni,0]],[nodes[nodIni,1]],'^b',transform=geo,label='Departure')
    ax2.plot([nodes[nodEnd,0]],[nodes[nodEnd,1]],'*r',transform=geo,label='Arrival') 
    imat2= ax2.pcolor(Xnod,Ynod,th_rec,vmin=0,vmax=np.nanmax(th),transform=pc)
    ax2.legend(loc='best') 
    ax2.set_extent(extent,crs=ccrs.PlateCarree())
    ax2.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False)
    ax2.coastlines(resolution=res_ldc)
    ax2.add_feature(cfeature.LAND)
    plt.colorbar(imat2)
    ##########################
    pref='-'
    if k<10:
        pref='-0'
  
    name_fig='../out/plots/SIMROUTE_'+name_Simu+pref+str(k)+'.png'
    plt.savefig(name_fig) #, bbox_inches='tight')
    plt.close()
    k=k+1
    print('Figure '+name_fig+' plotted')