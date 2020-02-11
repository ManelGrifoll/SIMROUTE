# plot nodes

import numpy  as np
from modsim import * 
from netCDF4 import Dataset 
import scipy.interpolate
import matplotlib.pyplot as plt
from params import * 
dat = np.load(arx_ones)
hs=dat['arr_0']
fp=dat['arr_1']
dir=dat['arr_2']

dat=np.load(arx_ldc)
ldc=dat['arr_0']
##############
Xnod, Ynod = np.meshgrid(tira_lon,tira_lat)
sh=Xnod.shape
var=1
t=12
if var == 1 :
    vari=np.copy(hs)
elif var==2:
    vari=np.copy(fp)
else:
    vari=np.copy(dir)


hh=vari[:,t].reshape(sh)
###############
plt.figure(1)
#plt.
plt.plot(ldc[:,0],ldc[:,1],'-')

plt.title(' make_plot temps = {}'.format(t))

plt.pcolor(Xnod,Ynod,hh)
plt.colorbar()


P1=[2.425,41.45]
P2=[8.75,44.35]

plt.plot(P1[0],P1[1],'*')
plt.plot(P2[0],P2[1],'o')

N1=43095+1+Nx
plt.plot(nodes[N1,0],nodes[N1,1],'k*')

N2=5813-Nx
plt.plot(nodes[N2,0],nodes[N2,1],'k*')