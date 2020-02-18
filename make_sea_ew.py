# first run de previous and zoom the zone desired to make sea
# afterwards, run this program.
#The sequence is from bottom left to top right
#the result is the start with sufix _ew  (dins de in)
import numpy  as np
import sys
import matplotlib.pyplot as plt
from modsim import *
from params import *
N1=4971
N2=5447

#arx_ones='in/waves_xxx.npz'
gravar=1       # Si voleu fer proves sense grabar poseu 0
###########
# representacio
plotejar=1        #1 es plotejar primer a 0 quan vulguis veure resultats a 1
vari=3             # 1->hs    2->fp  3-> dir
t=0             # hora  que caugui dins del domini
###############

dat = np.load(arx_ones)
hs=dat['arr_0']
hOld=np.copy(dir)
fp=dat['arr_1']
dir=dat['arr_2']
if plotejar==1: 
    if vari==1:
        old=np.copy(hs)
    if vari==2:
        old=np.copy(fp)
    if vari==3:
        old=np.copy(dir)
    Xnod, Ynod = np.meshgrid(tira_lon,tira_lat) 
    sh=Xnod.shape         


inc=inc/60.
incX=int(round((nodes[N2,0]-nodes[N1,0])/inc,5))
incY=int(round((nodes[N2,1]-nodes[N1,1])/inc,5))
hh=hs[:,1]
n_time=hs.shape[1]

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
print('Per la dreta be \n')
for j in range(incY+1):
    for i in range(incX+1):           # busca el ultim node i que te valor per l'esquerra 
        n=N1+i+Nx*j
        if not np.isnan(hh[n]):
            leftn=n
        else:
            break
    for i in range(incX+1):
            n=N1+incX-i+Nx*j
            if  not np.isnan(hh[n]):
                rightn=n
                break
            
        
    ###make hs
    leftvalue=hs[leftn,:]
    rigthvalue=hs[rightn,:]
    nn=(rightn-leftn);
    xx=(rigthvalue-leftvalue)/nn;
    ###for t in range(t_time):
    for t in range(n_time):
        for i in range(leftn+1,rightn,1):
            hs[i,t]=hs[i-1,t]+xx[t]
     ###make fp       
    leftvalue=fp[leftn,:]
    rigthvalue=fp[rightn,:]
    nn=(rightn-leftn);
    xx=(rigthvalue-leftvalue)/nn;
    ###for t in range(t_time):
    for t in range(n_time):
        for i in range(leftn+1,rightn,1):
            fp[i,t]=fp[i-1,t]+xx[t]      
            
       ###make dir
    leftvalue=dir[leftn,:]
    rigthvalue=dir[rightn,:]
    
    for t in  range(n_time):     
        dir[leftn+1:rightn,t]=dir2dir(leftvalue[t],rigthvalue[t],rightn-leftn-1)
        #aquesta funcio esta comentada as modsim.py
#ara gravarem treiem el 4 ultims caracters i hi posem '_ew'
if gravar==1:
    ar=arx_ones[:-4]+'_ew'
    np.savez_compressed(ar, hs,fp,dir)
    print('He gravat')
if plotejar==1:    #la x,y son els valors limits cel colorbar
    
    if vari==1:
        new=hs[:,t].reshape(sh)
        tit='HS'
        x=0
        y=10
    if vari==2:
        new=fp[:,t].reshape(sh)
        tit='FP'
        x=0
        y=14
    if vari==3:
        new=dir[:,t].reshape(sh)
        tit='DIR'
        x=0
        y=360
    dat=np.load(arx_ldc)
    ldc=dat['arr_0']
    plt.figure(1)
#plt.
    plt.plot(ldc[:,0],ldc[:,1],'-')

    oo=old[:,t].reshape(sh)
    
    plt.subplot(1,2,1)
    plt.plot(ldc[:,0],ldc[:,1],'-')            
    plt.title('{}  Old temps = {}'.format(tit,t))           
    plt.pcolor(Xnod,Ynod,oo)
    plt.clim(x,y)
    plt.colorbar()  
    plt.subplot(1,2,2)

    plt.plot(ldc[:,0],ldc[:,1],'-')            
    plt.title('{} New temps = {}'.format(tit,t))           
    plt.pcolor(Xnod,Ynod,new)
    plt.clim(x,y)
    plt.colorbar()  
    
    plt.figure(2)
    plt.plot(ldc[:,0],ldc[:,1],'-')            
    plt.title('{} diff temps = {}'.format(tit,t))           
    plt.pcolor(Xnod,Ynod,new-oo)
    plt.clim(x,y)
    plt.colorbar()  
    
    plt.show()