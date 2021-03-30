#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 23:10:59 2020

@author: manel grifoll (UPC-BarcelonaTech)
"""
import matplotlib.gridspec as gridspec
import numpy as np
import matplotlib.pyplot as plt
import math as math
import os
import cartopy.crs as ccrs
import cartopy.feature as cfeature
#Simulation name:
import cartopy.mpl.ticker as cticker    
name_Simu='LivEbo'

# END OF USER INPUTS   #######################

####Coses a fer pel pare:
    #i) un if per si no hi ha la simulacio
    #ii) unltim frame amb l'hora ben posada

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
ldc=dat['arr_6']
L_CostTrip=dat['arr_7']
L_ConsCostTrip=dat['arr_8']
L_CostFix=dat['arr_9']
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
vmax=np.nanmax(hs)  # maxix valor de hs posible en la simu (pel colorbar)
######################################################33
Xnod, Ynod = np.meshgrid(tira_lon,tira_lat)
x=nodes[L_Trip[:],0]
y=nodes[L_Trip[:],1]
xc=nodes[L_TripFix[:],0]
yc=nodes[L_TripFix[:],1]

loni, lati = nodes[nodIni,0], nodes[nodIni,1]
lone, late = nodes[nodEnd,0], nodes[nodEnd,1]

"""
plt.figure(1)
plt.title('SIMROUTE results')
plt.plot(xc,yc,'-m',label='Optimized route')  
plt.plot(x,y,'-k',label='Minimum distance route') 
plt.plot(xc[0],yc[0],'*',label='Departure')
plt.plot(xc[-1],yc[-1],'*r',label='Arrival') 
plt.legend()          
plt.plot(ldc[:,0],ldc[:,1],'-')   
name_fig='../out/SIMROUTE_'+name_Simu+'.png'
plt.savefig(name_fig) #, bbox_inches='tight')
plt.show()
print('Figure '+name_fig+' plotted')
"""

extend=[LonMin-3,LonMax+3, LatMin-10, LatMax]
central_lon, central_lat = -35, 50
rows, cols = 2,1
gs = gridspec.GridSpec(rows, cols)

fig = plt.figure(figsize=(20,10))

for k in range(rows):
    
    if k==0 :   # ortographic
        ax=plt.subplot(gs[k,0], projection=ccrs.Orthographic(central_lon, central_lat))
        ax.set_title('SIMROUTE results (trasform OrtographicCentral)')
 #       ax = plt.axes(projection=ccrs.Orthographic(central_lon, central_lat))
        ax.plot([loni],[lati],'*r',transform=ccrs.Geodetic(),label='Departure')
        ax.plot([lone],[late],'*g',transform=ccrs.Geodetic(),label='Arrival')     
    elif k==1 :
  #      ax= plt.subplot(gs[k,0],  projection=ccrs.Mercator())
        ax= plt.subplot(gs[k,0],  projection=ccrs.PlateCarree())
        ax.set_title('SIMROUTE results  (trasform PlateCarre)')       
        ax.plot(loni,lati,'*r',label='Departure')
        ax.plot(lone,late,'*g',label='Arrival')
        ax.set_yticks(np.arange(30,60,2))
        ax.set_xticks(np.arange(-70,-4,10))

   
    ax.plot(xc,yc,'-m',label='Optimized route',transform=ccrs.Geodetic())  
    ax.plot(x,y,'-k',label='Minimum distance route',transform=ccrs.Geodetic()) 
    ax.plot([loni,lone],[lati,late],'-',color="blue",label="Grat Circle", transform=ccrs.Geodetic())
    ax.set_extent(extend)
    ax.gridlines()
    ax.add_feature(cfeature.LAND)
    ax.add_feature(cfeature.COASTLINE)
    ax.coastlines(resolution='50m')
    ax.legend() 
##############################
plt.suptitle(name_Simu)

plt.savefig('../out/'+name_Simu+'.png')
plt.show()
#plt.figure(1)
#plt.title( name_Simu) #+ ' make_plot temps = {}'.format(i))
#plt.xlim([LonMin, LonMax])
#plt.ylim([LatMin, LatMax])
#   
#lont=nodes[L_Trip[:],0]
#latt=nodes[L_Trip[:],1]
#
#plt.plot(lont,latt,'m-')
#lonc=nodes[L_TripFix[:],0]
#latc=nodes[L_TripFix[:],1]
#
#plt.plot(lonc,latc,linewidth=1.5,color='k')
#plt.plot([nodes[nodIni,0],nodes[nodEnd,0]],[nodes[nodIni,1],nodes[nodEnd,1]],'-g')
#plt.legend(('Optimized','Minimum Distance','direct'),loc='best')
##Re-build Mesh:
#inc=inc/60    
#Nx=int(np.floor((LonMax-LonMin)/inc)+2)
#Ny=int(np.floor((LatMax-LatMin)/inc)+2)
#tira_lon=[]
#for i in range(Nx):
#    tira_lon.append(LonMin+i*inc)
#tira_lat=[]
#for j in range(Ny):  
#    tira_lat.append(LatMin+j*inc)
#nodes=np.zeros((Nx*Ny,2))
#for j in range(Ny):   
#    for i in range(Nx):
#        nodes[Nx*j +i,0]=tira_lon[i]
#        nodes[Nx*j +i,1]=tira_lat[j]
#inc=inc*60
#Xnod, Ynod = np.meshgrid(tira_lon,tira_lat)
#hs_rec=np.zeros(shape=Xnod.shape)
#dir_rec=np.copy(hs_rec)
#t=6
#for j in range(Ny):
#    for i in range(Nx):
#          hs_rec[j,i]=hs[:,t][i+Nx*j]
#          dir_rec[j,i]=dir[:,t][i+Nx*j]
#plt.pcolor(Xnod,Ynod,hs_rec)
#vmax=np.nanmax(hs)
#plt.clim(0,vmax)
#plt.colorbar()
#plt.plot(ldc[:,0],ldc[:,1],'-')
##plt.savefig('out/'+name_Simu+'fig.png')
#plt.show()
