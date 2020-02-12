# per fer plots dels valors d'omnatge i per trobar donats les lons i lasts d'un punt
#el node inferior esquerra de la malla de nodes, s'ha de fer dues vegades per fer mes mar
#en el cas de estrets que no tinguin valors d'onatge En el grafic del onatge espoden veures
#els valors de lon i lar adequats
import numpy  as np
from modsim import * 
from netCDF4 import Dataset 
import scipy.interpolate
import matplotlib.pyplot as plt
from params import * 

# trobar donant un punt en coords trobar els nods  util per fers sea_ew o sea_sn  o el nodIni i el nodEnd
# Donem valors qualsevols 


P1=[9.089,41.351]


# Donem valors qualsevols 


t=2   #  var=1 -> hs
       #var=2   -< fp
       #var=3   ->   dir
var=3                  
x= 0         # del plt.clim(x,y)         [0,360] es pel dir
y=360         # es el caxis del matlab   [[0,12]  per la hs
#########################
# Acabat aqui per usuari
#######################
dat = np.load(arx_ones)
hs=dat['arr_0']
fp=dat['arr_1']
dir=dat['arr_2']

dat=np.load(arx_ldc)
ldc=dat['arr_0']
##############
Xnod, Ynod = np.meshgrid(tira_lon,tira_lat)
sh=Xnod.shape
if var == 1 :
    vari=np.copy(hs)
elif var==2:
    vari=np.copy(fp)
else:
    vari=np.copy(dir)


hh=vari[:,t].reshape(sh)
plt.figure(1)

plt.plot(ldc[:,0],ldc[:,1],'-')
plt.title(' make_plot temps = {}'.format(t))

plt.pcolor(Xnod,Ynod,hh)
plt.clim(x,y)
plt.colorbar()
plt.plot(P1[0],P1[1],'*')

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

if np.isnan(fp[nnod,0]) :
    print('El node buscat {} es terra \n'.format(nnod))
else:
    print('El node buscat {} es valid \n'.format(nnod))
    
 
plt.show()