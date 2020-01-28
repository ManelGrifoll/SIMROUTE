# first run de previous and zoom the zone desired to make sea
# afterwards, run this program.
#The sequence is from bottom left to top right
#the result is the start with sufix _ew  
import numpy  as np
import sys
import matplotlib.pyplot as plt
from modsim import *
gravar=1       # Si voleu fer proves sense grabar poseu 0
N1=9251
N2=11945
arx_in='in/nodes_sn.npz'
arx_ones='in/waves_xsn.npz'
ldct='in/ldcTrim_sn.npz'
###########
# representacio
plotejar=1        #1 es plotejar
vari=3            # 1->hs    2->fp  3-> dir
t=48            # hora  que caugui dins del domini
###############
dat = np.load(arx_in)
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

dat = np.load(arx_ones)
hs=dat['arr_0']
hOld=np.copy(dir)
fp=dat['arr_1']
dir=dat['arr_2']

dat=np.load(ldct)
ldc=dat['arr_0']
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

#Comprobacio qie els N1 i N2 escollits son factibles (sea-sea) 
for i in range(incX+1):
    n=N1+i
    
    if np.isnan(hh[n]):
        print('Mira be els punts de l\'sota han de ser tots sea, prova de baixar N1 una unitat')
        sys.exit()
print('Per sota be \n')
for j in range(incX+1):
    n=N2-j
    if np.isnan(hh[n]):
        print('Mira be els punts de dalt han  ser tots sea, prova de pujar N2 una unitat')
        sys.exit()        
print('Per la dreat be \n')

# mira a cada tira vertical els nodes extrem q no son nans a mida que els trobi fara els canvis a valors interpolats
print("Ara mirem de trobar els ultims nodes no nan")
for i in range(incX+1):
    for j in range(incY+1):           # busca el ultim node que te valor per sota(no es NaN) 
        n=N1+i+Nx*j
        if not np.isnan(hh[n]):
            downn=n
        else:
            break
        
    for j in range(incY+1):
            n=N1+i+(incY-j)*Nx
            if  not np.isnan(hh[n]):
                upn=n
            else:
                break
        
    ####make hs
    
    downvalue=hs[downn,:]
    upvalue=hs[upn,:]
    nn=(upn-downn)/Nx;
    xx=(upvalue-downvalue)/nn;

    for t in range(n_time):
        for k in range(downn+Nx,upn,Nx):
            hs[k,t]=hs[k-Nx,t]+xx[t]
     # ###make fp    
    downvalue=fp[downn,:]
    upvalue=fp[upn,:]
    nn=(upn-downn)/Nx;
    xx=(upvalue-downvalue)/nn;
    for t in range(n_time):
        for k in range(downn+Nx,upn,Nx):
            fp[k,t]=fp[k-Nx,t]+xx[t] 
   # make dir
    downvalue=dir[downn,:]
    upvalue=dir[upn,:]
    for t in  range(n_time):  
       # Lafuncio dir2dir opera amb horitzontal , volem els resultats colocats en vertical
        out=dir2dir(downvalue[t],upvalue[t],int((upn-downn)/Nx)-1) 
        i=0
        for k in range(downn+Nx,upn,Nx):
            dir[k,t]=out[i]
            i=i+1
 #ara gravarem treiem el 4 ultims caracters i hi posem '_ew'
if gravar==1:
    ar=arx_ones[:-4]+'_sn'
    np.savez_compressed(ar, hs,fp,dir)
    print('He gravat')            
            
    
if plotejar==1:
    if vari==1:
        new=hs[:,t].reshape(sh)
        tit='HS'
        x=0
        y=10
    if vari==2:
        new=fp[:,t].reshape(sh)
        tit='FP'
        x=0
        y=6
    if vari==3:
        new=dir[:,t].reshape(sh)
        tit='DIR'
        x=0
        y=360
    
    
    



    oo=old[:,t].reshape(sh)
    plt.figure(1)
    plt.subplot(1,2,1)
    plt.plot(ldc[:,0],ldc[:,1],'-')            
    plt.title('{}  Old temps = {}'.format(tit,t))           
    plt.pcolor(Xnod,Ynod,oo)
#    plt.colorbar()  
    plt.subplot(1,2,2)

    plt.plot(ldc[:,0],ldc[:,1],'-')            
    plt.title('{} New temps = {}'.format(tit,t))           
    plt.pcolor(Xnod,Ynod,new)
  #  plt.clim(x,y)
    plt.colorbar()  
    plt.plot(nodes[N1,0],nodes[N1,1],'*')
    plt.plot(nodes[N2,0],nodes[N2,1],'o')
    plt.figure(2)
    plt.plot(ldc[:,0],ldc[:,1],'-')            
    plt.title('{} diff temps = {}'.format(tit,t))           
    plt.pcolor(Xnod,Ynod,new-oo)
  #  plt.clim(x,y)
    plt.colorbar()  
    
    plt.show()