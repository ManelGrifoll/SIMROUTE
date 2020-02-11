import numpy  as np
from pathlib import Path
nomSim='BcnGenA1'
LonMin=2
LonMax=10.0
LatMin=41.0
LatMax=45.0
inc=1.5;    #in milles   (minutes of arcmax)
nodIni=43418
nodEnd=5491
# ###################################### Si poses un valor a arxiu ones el carregara si existeix, 
# la linea de costa pasara el nom que hi posis
arx_ones= 'in/waves_A1.npz'
arx_ldc= 'in/ldcA1.npz'
v0=16.1  # cruising speed in nautical milles per hour (knots)
# #######################
if  Path(arx_ones).is_file():
    dat = np.load(arx_ones)
    hs=dat['arr_0']
    fp=dat['arr_1']
    dir=dat['arr_2']   
# posar un ldc per
# ##############
inc=inc/60.0    # in deg


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


