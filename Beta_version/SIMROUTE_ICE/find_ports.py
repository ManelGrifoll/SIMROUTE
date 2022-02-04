#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 23:10:59 2020
Code part of SIMROUTE (UPC-BarcelonaTech)
Version: 02 / 02 / 21
@author: manel grifoll (UPC-BarcelonaTech)
find_ports.py: convert port coordinates (input) in mesh node (output). 
    
"""

import numpy  as np
from netCDF4 import Dataset 
import scipy.interpolate
import matplotlib.pyplot as plt
from params import * 
from func_simroute_ice import *

#Introduce [Lon, Lat] to find the node at mesh:
#P1=[-22.4,63.9] #Reykjavik 
#P1=[-92.9,59.3] #Churchill
P1=[-51.9,64.1] #Nuuk

# END OF USER INPUTS   #######################

# Descaarta el P1 si esta fora del domini.
d=1
if (P1[0]<LonMin or P1[0]>LonMax) :
  d=0       
if (P1[1]<LatMin or P1[1]>LatMax) :
    d=0
if d==0:
    print ('Coordinates out of the domain')
    raise SystemExit
# END OF USER INPUTS   #######################

#Variable to plot: var=1 -> hs // var=2 -> fp // var=3   ->   dir
var=1  
# Time to plot:
t=1                   

Xnod, Ynod = np.meshgrid(tira_lon,tira_lat)
sh=Xnod.shape
if var == 1 :
    vari=np.copy(hs)
elif var==2:
    vari=np.copy(fp)
else:
    vari=np.copy(dir)
hh=vari[:,t].reshape(sh)
inc=inc/60;
xnod=np.floor((P1[0]-LonMin)/inc)
ynod=np.floor((P1[1]-LatMin)/inc)
nnod=int(xnod+Nx*(ynod))


print('            Nodes Tests   \n')
print(' ================================================================ \n')
print('  {} -------------------- {}          {:8.5f}  \n'.format(nnod+Nx,nnod+Nx+1,nodes[nnod+Nx+1,1]) )  
print('         {:8.5f}  , {:8.5f}     \n'.format(P1[0],P1[1]))
print('  {} -------------------- {}          {:8.5f}  \n'.format(nnod,nnod+1,nodes[nnod,1])   )

print(' {:8.5f}          {:8.5f}  \n'.format(nodes[nnod,0],nodes[nnod+1,0]))
kk=hs[nnod,0]
if np.isnan(kk):
    print('Node {} is land (not valid) \n'.format(nnod))
else:
    print('Node {} is sea \n'.format(nnod))
 
fig = plt.figure(figsize=(10,5))

ax=plt.subplot(1,2,1)
imat= ax.pcolor(Xnod,Ynod,hh)
plt.colorbar(imat)
ax.plot(P1[0],P1[1],'*m',label='Lan/Lot input')
ax.legend()
ax.set_title('node selected in SIMROUTE mesh')

ax1=plt.subplot(1,2,2)
Lon_vicinity=[nodes[nnod+Nx-1,0],nodes[nnod-1,0],nodes[nnod,0],nodes[nnod+1,0],nodes[nnod+Nx,0],nodes[nnod+Nx+1,0],nodes[nnod+2,0],nodes[nnod+Nx+2,0]]
Lat_vicinity=[nodes[nnod+Nx-1,1],nodes[nnod-1,1],nodes[nnod,1],nodes[nnod+1,1],nodes[nnod+Nx,1],nodes[nnod+Nx+1,1],nodes[nnod+2,1],nodes[nnod+Nx+2,1]]
#nodes_v=int([[nnod+Nx-1],[nnod-1],[nnod],[nnod+1],[nnod+Nx],[nnod+Nx+1],[nnod+2],[nnod+Nx+2]])
nodes_v=[nnod+Nx-1,nnod-1,nnod,nnod+1,nnod+Nx,nnod+Nx+1,nnod+2,nnod+Nx+2]

n_p=8
Lon_vicinity_l=[]
Lon_vicinity_s=[]
Lat_vicinity_l=[]
Lat_vicinity_s=[]
nodL=[]
nodS=[]
for i in range(n_p):
    kkkk=hs[nodes_v[i],0]
    if np.isnan(float(kkkk)):
        Lon1=Lon_vicinity[i]
        Lon_vicinity_l.append(Lon1)
        Lat1=Lat_vicinity[i]
        Lat_vicinity_l.append(Lat1)
        nodL.append(nodes_v[i])    
    else:
        Lon2=Lon_vicinity[i]
        Lon_vicinity_s.append(Lon2)      
        Lat2=Lat_vicinity[i]
        Lat_vicinity_s.append(Lat2)
        nodS.append(nodes_v[i])
ax1.scatter(Lon_vicinity_s,Lat_vicinity_s, color='blue',marker='_',label='Node sea') #,'o',label='Node Sea')
for i, txt in enumerate(nodS):    
    ax1.annotate(txt,( Lon_vicinity_s[i],Lat_vicinity_s[i]))
ax1.scatter(Lon_vicinity_l,Lat_vicinity_l,color='red',marker='^',label='Node Land')
for i, txt in enumerate(nodL):    
    ax1.annotate(txt,( Lon_vicinity_l[i],Lat_vicinity_l[i]))

ax1.plot(P1[0],P1[1],'*m',label='Lan/Lot selected')
ax1.legend()
#plt.savefig('find_ports.png',dpi=300) 
plt.show()