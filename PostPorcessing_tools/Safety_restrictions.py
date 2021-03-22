#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 20:02:41 2021

@author: xarx
"""

name_Simu='Tunis_Nice'
offset=0.2


# END OF USER INPUTS   #######################

import numpy as np
from func_postprocess import *
import matplotlib.pyplot as plt
import math as math
import os
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.mpl.ticker as cticker 

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
L_CostTrip=dat['arr_6']
L_ConsCostTrip=dat['arr_7']
L_CostFix=dat['arr_8']
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
vmax=np.nanmax(hs)  # maxix valor de hs posible en la simu (pel colorbar)
''' Angle ship es el rumb del vaixell que es treu amb les funcions rumIni
rumEnd , donats els punts ini i end i el angle encountere es troba mab la funcio
ang_encounter (alfa) donant el rumb i la dir de la onada
Tw =  periode de wave (es fp segons l'arxiu d'ones)
L = length of ship (Lbp)
λ = 1.56 * Tw
Tw = 0.8 * λ        Longitud de ona en funcio del periode d'ona 

El Te Periode de encounter es aprox=

Te=(3Tw^2)/(3*Tw+V*cos(alfa))

Tr= Periode rooling del ship concret per exemple 20 (Marinnari)
Tolerancia epsi= 10%   

Si hi ha "coincidencia" entre Te i Tr  que mesurarem :
    |Te-Tr|<epsi*Tr           es perillos
    tambe ho es un "semicoincidencia"
    |2Te-Tr|<epsi*Tr           es perillos
    


Surf-riding and broaching-to les dues conduicions de perill  pel 
son: 135<alfa<225   (mar de popa) i v> 1.8sqrt(L)/ cos(180-alfa)
cos(180-135)=sqrt(2)/2   i cos(180-225)=sqrt(2)/2  cos(180-180)=1
Per haver sf-bt el la velocitat del vaixell ha de ser mes gran que:
1.8sqrt(L) amn followsea (180)    
For successive high-wave attack, 2 conditions:
λ >0.8*L      and    hs > 0.04*L

units :  λ  , L    meters
           
   + 

'''
Tr=20
epsi=0.1
L_sr_bt=[]
L_pr=[]

#for i in range(4):
for i in range(len(L_Trip)-1):    
    Ni=L_Trip[i]
    Ne=L_Trip[i+1]
    loni,lati = nodes[Ni,0], nodes[Ni,1]
    lone,late = nodes[Ne,0], nodes[Ne,1]
 #   print(i,Ni,Ne)
    for k in range(2):
        if time_res==1:
            ti=np.rint(L_CostTrip[i+k])
        else:
           (a,b)=np.divmod(L_CostTrip[i+k],time_res) 
           if b>time_res/2:
               ti=a+1
           else:
               ti=a
        ti=int(ti)
        if k==0:
            hi=hs[Ni,ti]
            diri=dir[Ni,ti]
            fpi=fp[Ni,ti]
            rumb=rumIni(loni,lati,lone,late)
        else:
            hi=hs[Ne,ti]
            diri=dir[Ne,ti]
            fpi=fp[Ne,ti]
            rumb=rumEnd(loni,lati,lone,late)
        angEnc=ang_encounter(rumb,diri)
        v=1.8*np.sqrt(Lbp)/ np.cos(np.deg2rad(180-angEnc))
        if angEnc > 145 and angEnc<225 and v0>v:
            if k==0:
                print("Unstable sr-bt in  node ini  ", Ni)
                L_sr_bt.append(Ni)
            else:
                print("Unstable sr-bt in  node end  ", Ne)
                L_sr_bt.append(Ne)                
        Tw=fpi
        Te=3*Tw*Tw/(3*Tw+v0*np.cos(np.deg2rad(angEnc)))
#        print(Te,Tw,angEnc)       
        if (np.abs(Te-Tr)<epsi*Tr ) or (np.abs(2*Te-Tr)<epsi*Tr ):
            if k==0:
                print("Unstable parametric rolling in node ini ", Ni)
                L_pr.append(Ni)
            else:
                print("Unstable parametric rolling in node end", Ne)
                L_pr.append(Ne)      

pc=ccrs.PlateCarree()
res_ldc='10m'
extent=[LonMin-offset,LonMax+offset, LatMin-offset, LatMax+offset]
fig = plt.figure(figsize=(20,10))    
ax=plt.subplot(1,1,1, projection=pc)
ax.set_title( name_Simu) #+ ' make_plot temps = {}'.format(i))
x=nodes[L_Trip[:],0]
y=nodes[L_Trip[:],1]
xc=nodes[L_TripFix[:],0]
yc=nodes[L_TripFix[:],1]
ax.plot(xc,yc,'m',label='Optimized route')  
ax.plot(x,y,'orange',label='Minimum distance route') 
ax.set_extent(extent)
ax.plot([nodes[nodIni,0]],[nodes[nodIni,1]],'^b',label='Departure')
ax.plot([nodes[nodEnd,0]],[nodes[nodEnd,1]],'^r',label='Arrival') 
ax.gridlines()
ax.coastlines(resolution=res_ldc)
ax.add_feature(cfeature.LAND)
ax.set_yticks(np.arange(LatMin-offset,LatMax+offset,(LatMax+offset-(LatMin-offset))/5))
ax.set_xticks(np.arange(LonMin-offset,LonMax+offset,(LonMax+offset-(LonMin-offset))/5))
lprx=nodes[L_pr[:],0]
lpry=nodes[L_pr[:],1]
lsrx=nodes[L_sr_bt[:],0]
ldry=nodes[L_sr_bt[:],1]

ax.scatter(lprx,lpry,marker ='o',label='Param rolling')
ax.legend(loc='best') 


name_fig='../out/plots/'+name_Simu+'-sr_pr.png'
plt.savefig(name_fig) #, bbox_inches='tight')
plt.show()
