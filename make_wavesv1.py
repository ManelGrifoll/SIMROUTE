import numpy  as np
from modsim import * 
from netCDF4 import Dataset 
import scipy.interpolate
import matplotlib.pyplot as plt
tic()
Tini_trip=11   #Time ini trip from 00:00 respect to waves file (e.g. 0 means that begin at 00:00);
#FILES WITH WAVE INFORMATION
ARX=['HW-20180228-HC.nc','HW-20180301-HC.nc']

#NAME AND FOLDER FOR INTERPOLATED WAVES (output)
Na=len(ARX)
arxiu_out='in/waves_xxxx'
dir_arx='in/'
dat = np.load('nodes.npz')
nodes=dat['arr_0']
#inc=dat['arr_1']
Nx=dat['arr_2']
Ny=dat['arr_3']
LonMin=dat['arr_4']
LonMax=dat['arr_5']
LatMin=dat['arr_6']
LatMax=dat['arr_7']
tira_lon=dat['arr_8']

tira_lat=dat['arr_9']

nc=Dataset(dir_arx+ARX[0],'r')

lon=nc.variables['longitude'][:]
nx=len(lon)
lat=nc.variables['latitude'][:]
ny=len(lat)

x0=np.where((lon>=LonMin) & (lon<=LonMax)) # marge de seguretat restem 1 i sumen 
y0=np.where((lat>=LatMin) & (lat<=LatMax)) # marge de seguretat restem 1 i sumen 2
a1=x0[0][0]-1
a2=x0[0][-1]+2
b1=y0[0][0]-1
b2=y0[0][-1]+2

x=lon[a1 : a2]
y=lat[b1 : b2]

X,Y=np.meshgrid(x,y)
Xnod, Ynod = np.meshgrid(tira_lon,tira_lat)

hsa=nc.variables['VHM0'][10,b1:b2,a1:a2] 
f_v=np.ma.MaskedArray.get_fill_value(hsa)  # si el fillvalue es diferent de nan
di=hsa.shape
maski=hsa.mask
vari=np.ma.MaskedArray (np.ones(shape=di), mask = maski, fill_value = np.nan) # matriu de entrada amb mascara nan i tot uns

hsg=scipy.interpolate.griddata((X.flatten(),Y.flatten()),(hsa*maski).flatten() , (Xnod,Ynod),method='linear')
hsg[hsg<0.0]=np.nan
hsg[hsg>=0.0]=1.0

#Per no interpolar amb fillValues utilizem la vari  com a mascara per tenir nans
maskin=np.copy(vari)
maskw=np.copy(hsg)   # mascara per la sortida posarem nans a la terra o a on no tinguem dades
# Ara coemncarem a construir la matriu de ones
hs_rec=np.zeros(shape=(Ny,Nx,Na*24))
fp_rec=np.zeros(shape=(Ny,Nx,Na*24))
dir_rec=np.zeros(shape=(Ny,Nx,Na*24))
for n in range(Na):
    nc=Dataset(dir_arx+ARX[n],'r')
    print(dir_arx+ARX[n])
    for t in range(24):
        hw=np.copy(vari)
        hw[:,:]=nc.variables['VHM0'][t,b1:b2,a1:a2][:,:]
        hs=scipy.interpolate.griddata((X.flatten(),Y.flatten()),(hw*maskin).flatten() , (Xnod,Ynod),method='linear')*maskw
        hs_rec[:,:,t+24*n]=hs[:,:] 
        
        fw=np.copy(vari)
        fw[:,:]=nc.variables['VSMC'][t,b1:b2,a1:a2][:,:]
        fs=scipy.interpolate.griddata((X.flatten(),Y.flatten()),(fw*maskin).flatten() , (Xnod,Ynod),method='linear')*maskw
        fp_rec[:,:,t+24*n]=fs[:,:]
        
        dirw=np.copy(vari)
        dir_x=np.copy(vari)
        dir_y=np.copy(vari)
        a=np.copy(vari)
        dirw[:,:]=nc.variables['VMDR'][t,b1:b2,a1:a2][:,:]
        for i in range(di[0]):
            for j in range(di[1]):
                a[i,j]=compass2cart(dirw[i,j])
                
        dir_x=np.cos(np.deg2rad(a))*maskin
        dir_y=np.sin(np.deg2rad(a))*maskin
        dir_xi=scipy.interpolate.griddata((X.flatten(),Y.flatten()),dir_x.flatten() , (Xnod,Ynod),method='linear')*maskw
        dir_yi=scipy.interpolate.griddata((X.flatten(),Y.flatten()),dir_y.flatten() , (Xnod,Ynod),method='linear')*maskw
        for i in range(Nx):
            for j in range(Ny):
                zeta=np.complex(dir_xi[j,i],dir_yi[j,i])
                an=cart2compass(np.angle(zeta,deg=True))
                dir_rec[j,i,t+24*n]=an
                
hs=np.zeros(shape=(Nx*Ny,Na*24))
hs.fill(np.nan)
fp=np.copy(hs)
dir=np.copy(hs)

for t in  range(24*Na):
    for j in range(Ny):
        for i in range(Nx):
            hs[i+j*Nx,t]=hs_rec[j,i,t];
            fp[i+j*Nx,t]=fp_rec[j,i,t];
            dir[i+j*Nx,t]=dir_rec[j,i,t];
            
np.savez_compressed(arxiu_out, hs,fp,dir)

toc()

#t=12
#plt.title('temps = {}'.format(t))
#plt.pcolor(Xnod,Ynod,hs_rec[:,:,t])
#plt.clim(0,1.4)
#plt.colorbar()

#plt.show()
 