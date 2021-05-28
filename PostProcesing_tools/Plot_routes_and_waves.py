#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 23:10:59 2020
Code part of SIMROUTE (UPC-BarcelonaTech)
version 5/02/2021
@author: manel grifoll (UPC-BarcelonaTech)

Plot_routes_and_waves.py creates a plots sequence of routes and waves 
"""

#Simulation name:   
name_Simu='Palma_Barna'

#Offset at boundary plots (in degrees):
offset=0.2

#Quiver plot sub-sampling (nred=sub-sampling factor; sc= arrow scale; wd_quiver=width quiver) 
nred=7
sc=75#175
wd_quiver=0.002

#Interval of plotting frames (in hours)
inc_frame=1

# END OF USER INPUTS   #######################
import numpy as np
import matplotlib.pyplot as plt
import math as math
import os
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
    
L_Trip=dat['arr_4']
L_TripFix=dat['arr_5']
Cost_Opt=dat['arr_6']
L_ConsCostTrip=dat['arr_7']
Cost_Min=dat['arr_8']
ARX=dat['arr_9']

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
k=0
for t in  infotos:
    print(t)
    if time_res==1:        
        hs_rec=hs[:,t].reshape((Ny,Nx))
        dir_rec=dir[:,t].reshape((Ny,Nx))+180
    else:
        hs_rec=hs[:,np.int(np.round(t/3))].reshape((Ny,Nx))
        dir_rec=dir[:,np.int(np.round(t/3))].reshape((Ny,Nx))+180                                             
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
    
    fig = plt.figure(figsize=(7,7))    
    ax=plt.subplot(1,1,1)
    imat= ax.pcolor(Xnod,Ynod,hs_rec,vmin=0,vmax=hsmax) 
    strtim=name_Simu+' time = {:.2f} hours'.format(t) 
    ax.set_title(strtim)
    ax.plot(lonc,latc,'orange',label='Minimum distance route') 
    ax.plot(lon,lat,'m',label='Optimized route') 
    ax.plot([nodes[nodIni,0]],[nodes[nodIni,1]],'^b',label='Departure')
    ax.plot([nodes[nodEnd,0]],[nodes[nodEnd,1]],'*r',label='Arrival') 
    ax.legend(loc='best') 
    ax.quiver(Xnod[::nred, ::nred], Ynod[::nred, ::nred],U[::nred, ::nred], V[::nred, ::nred],
              scale=sc,width = wd_quiver)
    plt.colorbar(imat)
    
    pref='-'
    if k<10:
        pref='-0'
    name_fig='../out/plots/'+name_Simu+pref+str(k)+'.png'
    k=k+1
    plt.savefig(name_fig) #, bbox_inches='tight')
    plt.close()
    print('Figure '+name_fig+' plotted')

#Final frame:
    
name_fig='../out/plots/'+name_Simu+pref+str(k+1)+'.png'
print('Figure '+name_fig+' plotted')
    