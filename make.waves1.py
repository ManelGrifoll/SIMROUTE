import numpy  as np
from netCDF4 import Dataset 
import scipy.interpolate
import matplotlib.pyplot as plt
Tini_trip=11   #Time ini trip from 00:00 respect to waves file (e.g. 0 means that begin at 00:00);
#FILES WITH WAVE INFORMATION
ARX=['HW-20180228-HC.nc','HW-20180301-HC.nc']

#NAME AND FOLDER FOR INTERPOLATED WAVES (output)
arxiu_out='waves_20180228'
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
vari=np.ma.MaskedArray (np.ones(shape=di), mask = maski, fill_value = np.nan) # matriu de entrada
hsi=np.copy(vari)
hsi[:,:]=hsa[:,:]   # amb nans al f-v
hsg=scipy.interpolate.griddata((X.flatten(),Y.flatten()),hsi.flatten() , (Xnod,Ynod),method='linear')
hsg[hsg<0.0]=np.nan
hsg[hsg>0.0]=1.0
#Per no interpolar amb fillValues utilizem la vari 
maskw=np.copy(hsg)   # mascara per la sortida posarem nans a la terra o a on no tinguem dades
# Ara coemncarem a construir la matriu de ones
for t in range(1):
    print(t)

hw=vari
#hw=nc.variables['VHM0'][t,b1:b2,a1:a2] 


#hsgn=scipy.interpolate.griddata((X.flatten(),Y.flatten()),vari.flatten() , (Xnod,Ynod),method='linear')


#plt.figure(1)
#plt.subplot(2,1,1)
#plt.pcolor(Xnod,Ynod,hsgn)
#plt.clim(0,1.4)
#plt.colorbar()
#plt.show()


plt.subplot(2,1,2)
plt.title('fen nan a ma')
plt.pcolor(Xnod,Ynod,hsg)
plt.clim(0,1.4)
plt.colorbar()

plt.show()
 