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
from simroute import * #   Aquest modul carrega el paramS_PROD
from netCDF4 import Dataset 
import scipy.interpolate
import matplotlib.pyplot as plt


# Plot waves after interpolation
plot_waves = True

# Time frame if plotting waves.
t=0

# END OF USER INPUTS   #######################
#creem els arxius diaris aparir del params
 
tic()
d1 = datetime.date(date_Ini[0],date_Ini[1],date_Ini[2])
d2 = datetime.date(date_End[0],date_End[1],date_End[2])
nomw1=d1.strftime('%Y-%m-%d')
nomw2=d2.strftime('%Y-%m-%d')
nomarx='Waves_'+name_Simu+'_'+nomw1+'%'+nomw2+'.nc'

nc=Dataset(dir_arx+nomarx,'r')

if  prod=='XBLKSEA'  :   # ja no , BLKSEA es normal
    lon=nc.variables['lon'][:]
    lat=nc.variables['lat'][:]
    X,Y=np.meshgrid(lon,lat)
    nx=len(lon)
    ny=len(lat)
elif prod=='XARTIC':
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
    ntim=nc.dimensions['time'].size
Xnod, Ynod = np.meshgrid(tira_lon,tira_lat)
#sys.exit()

# Ara coemncarem a construir la matriu de ones
hsi=np.zeros(shape=(ny,nx))
diri=np.zeros(shape=(ny,nx))
#fpi=np.zeros(shape=(ny,nx))
hs_rec=np.zeros(shape=(Ny,Nx,ntim))
#fp_rec=np.zeros(shape=(Ny,Nx,ntim))
dir_rec=np.zeros(shape=(Ny,Nx,ntim))
'''
    Degut a que les variebles extretates dels nc tenen un compotament diferent
    En el cas que  hagin punts "land" o que no hi hagi cap punt land hem de fer
    un procediment diferent en cada cas:
'''

#mnc=Dataset(dir_arx+ARX[0],'r')
mhw=nc.variables['VHM0'][0,:,:]
if isinstance(mhw.mask,np.ndarray) is False:
    print("No hi ha lands")
    msk = False
else:
    print('Hi ha ha lands')
    msk = True    
    
#for n in range(Na):
#    nc=Dataset(dir_arx+ARX[n],'r')
#    print(dir_arx+ARX[n])
toc()
print(' unitat de temps')
print(ntim)
for t in range(ntim):
    print(t)
    hw=nc.variables['VHM0'][t,:,:]
    for i in range(nx):
        for j in range(ny):
            if msk is True:                        
                if   hw.mask[j,i]==False:
                     hsi[j,i]=hw[j,i]     
                else:
                    hsi[j,i]=np.nan
            else:
                hsi[j,i]=hw[j,i]                         
    hsg=scipy.interpolate.griddata((X.flatten(), Y.flatten()), 
                      (hsi.flatten()) ,(Xnod,Ynod), method='linear')
    hs_rec[:,:,t]=hsg[:,:] 

            
    dirw=nc.variables['VMDR'][t,:,:]
        
    for i in range(nx):
        for j in range(ny):
            if msk is True:  
                if dirw.mask[j,i]==False:
                    diri[j,i]=dirw[j,i]
                else:
                   diri[j,i]=np.nan #problema el fill_value es negatiu gran, volem nan
            else:
                diri[j,i]=dirw[j,i]
    dirc=arrayComp2Cart(diri)                   
    dir_x=np.cos(np.deg2rad(dirc))
    dir_y=np.sin(np.deg2rad(dirc))
    
    dir_xi=scipy.interpolate.griddata((X.flatten(),Y.flatten()),
                    (dir_x.flatten()) , (Xnod,Ynod),method='linear')
    dir_yi=scipy.interpolate.griddata((X.flatten(),Y.flatten()),
                                       (dir_y.flatten()) , 
                                       (Xnod,Ynod),method='linear')
    
    dir_rec[:,:,t]=arrayRect2Comp(dir_xi,dir_yi)

print('Interpolation done! Assigning waves at nodes')             
hs=np.zeros(shape=(Nx*Ny,ntim))
hs.fill(np.nan)
#fp=np.copy(hs)
dir=np.copy(hs)

for t in  range(ntim):
    for j in range(Ny):
        for i in range(Nx):
            hs[i+j*Nx,t]=hs_rec[j,i,t];
 #           fp[i+j*Nx,t]=fp_rec[j,i,t];
            dir[i+j*Nx,t]=dir_rec[j,i,t];

#Nan extraction in Dir due to interpolation 
for i in  range(Nx*Ny):
    if  np.isnan(hs[i,0])==False and np.isnan(dir[i,0])==True:
                hs[i,:]=np.nan
                print('algun nan fa la punyeta ',i,j)

if plot_waves is False:
    print("Delete intermediate variables.")       
    del dir_xi
    del dir_yi
    del dir_rec
#    del fp_rec
    del hs_rec
print ("Checking nans in waves fields.")
[nn,tt]=hs.shape
n=0
for i in range(nn):
    val_ini=np.isnan(hs[i,0])
    for t in range(tt):
        if val_ini !=np.isnan(hs[i,t]):
            hs[i,:]=np.nan
            dir[i,:]=np.nan
#            fp[i,:]=np.nan 
            n=n+1
            print(i,t,n)
            break
if n !=0:
    print('Find nans and eliminated :',n )



                
print("Done. Saving...")
arxi='in/'+name_Simu+'_wInt.npz'            
np.savez_compressed(arxi,hs,dir)


toc()

if plot_waves is True:
    fig=plt.figure()
    t=10
    axes=fig.add_axes([0.1,0.1,0.8,0.8])
    axes.set_ylabel('Lat (º)')
    axes.set_xlabel('Lon (º)')
    axes.set_title('Significant wave hight (in m) in time : '.format(t))
    ima=axes.pcolor(Xnod,Ynod,hs_rec[:,:,t],vmin=0,vmax=np.nanmax(hs_rec))
    plt.colorbar(ima)    
    plt.show()

