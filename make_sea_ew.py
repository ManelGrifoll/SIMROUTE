# first run de previous and zoom the zone desired to make sea
# afterwards, run this program.
#The sequence is from bottom left to top right
#the result is the start with sifix _m
import numpy  as np
import sys
import matplotlib.pyplot as plt
from modsim import *

N1=4137
N2=4792
dat = np.load('nodes.npz')
nodes=dat['arr_0']
inc=dat['arr_1']
Nx=dat['arr_2']
Ny=dat['arr_3']
LonMin=dat['arr_4']
LonMax=dat['arr_5']
LatMin=dat['arr_6']
LatMax=dat['arr_7']
tira_lon=dat['arr_8']
tira_lat=dat['arr_9']

dat = np.load('in/waves_xxxx.npz')
hs=dat['arr_0']
hOld=np.copy(hs)
fp=dat['arr_1']
dir=dat['arr_2']

dat=np.load('in/ldcTrim.npz')
ldc=dat['arr_0']

inc=inc/60.
incX=int(round((nodes[N2,0]-nodes[N1,0])/inc,5))
incY=int(round((nodes[N2,1]-nodes[N1,1])/inc,5))
hh=hs[:,1]
n_time=hs.shape[1]
# ######  test
for i in range(N1,N1+incX+1,1):
    print(' N = {}   lon= {:8.5f}   hs= {:8.3f}\n'.format(i,nodes[i,0],hs[i,1]))
print("========================================================================")
for i in range(N1+Nx,N1+Nx+incX+1,1):
    print(' N = {}   lon= {:8.5f}   hs= {:8.3f}\n'.format(i,nodes[i,0],hs[i,1]))
print("========================================================================")
for i in range(N1+2*Nx,N1+2*Nx+incX+1,1):
    print(' N = {}   lon= {:8.5f}   hs= {:8.3f}\n'.format(i,nodes[i,0],hs[i,1]))    
# ############
# primer mirem si els N1 i N2 son sea-sea en tot el rectanngle
for j in range(incY+1):
    n=N1+j*Nx
    
    if np.isnan(hh[n]):
        print('Mira be els punts de l\'esquerra han de ser tots sea, prova de baixar N1 una unitat')
        sys.exit()
print('Per l\'esquerra be \n')
for j in range(incY+1):
    n=N1+incX+j*Nx
    if np.isnan(hh[n]):
        print('Mira be els punts de la dreta han de ser tots sea, prova de pujar N2 una unitat')
        sys.exit()        
print('Per la dreat be \n')




for j in range(incY+1):
    for i in range(incX+1):           # busca el ultim node i que te valor per l'esquerra 
        n=N1+i+Nx*j
        if not np.isnan(hh[n]):
            leftn=n
        else:
            print('ja ha trobat el primer nan ara surt i buscarà per la dreta')
            break
        print('leftn ={} \n'.format(leftn))
        for i in range(incX+1):
            n=N1+incX-i+Nx*j
            if  not np.isnan(hh[n]):
                rightn=n
               # print('rightn = {} '.format(rightn))
            else:
                break
            print('rightn = {} '.format(rightn))
    
    ####clear downvalue upvalue
    ###make hs
    leftvalue=hs[leftn,:]
    rigthvalue=hs[rightn,:]
    nn=(rightn-leftn);
    xx=(rigthvalue-leftvalue)/nn;
    ###for t in range(t_time):
    for t in range(n_time):
        for i in range(leftn+1,rightn,1):
         #   print(i)
            hs[i,t]=hs[i-1,t]+xx[t]
     ###make fp       
    leftvalue=fp[leftn,:]
    rigthvalue=fp[rightn,:]
    nn=(rightn-leftn);
    xx=(rigthvalue-leftvalue)/nn;
    ###for t in range(t_time):
    for t in range(n_time):
        for i in range(leftn+1,rightn,1):
          #  print(i)
            fp[i,t]=fp[i-1,t]+xx[t]      
            
       ###make dir
    leftvalue=dir[leftn,:]
    rigthvalue=dir[rightn,:]
    rcart=np.copy(rigthvalue)
    lcart=np.copy(leftvalue)
    for i in range(47):
        rcart[i]=np.cos(np.deg2rad(compass2cart(rigthvalue[i])))
        lcart[i]=np.cos(np.deg2rad(compass2cart(rigthvalue[i])))
        Xrcart[i]=np.cos(np.deg2rad(dirc))        
            
            
print('Acabat ara venen els grafics')            
            
t=12
x=0
y=8


Xnod, Ynod = np.meshgrid(tira_lon,tira_lat) 
sh=Xnod.shape 
hh=hOld[:,t].reshape(sh)
plt.figure(1)
plt.subplot(1,2,1)
plt.plot(ldc[:,0],ldc[:,1],'-')            
plt.title('  Old temps = {}'.format(t))           
plt.pcolor(Xnod,Ynod,hh)
plt.clim(x,y)
plt.colorbar()  
plt.subplot(1,2,2)
hh=hs[:,t].reshape(sh)
plt.plot(ldc[:,0],ldc[:,1],'-')            
plt.title(' New temps = {}'.format(t))           
plt.pcolor(Xnod,Ynod,hh)
plt.clim(x,y)
plt.colorbar()  
plt.show()