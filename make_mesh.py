import numpy  as np

LonMin=2.0
LonMax=10.0
LatMin=41.0
LatMax=45.0
inc=1.5;    #in milles   (minutes of arcmax)
arx='in/nodes.npz'
#########################################3
#LonMin=14.66
#LonMax=17.83
#LatMin=36.08
#LatMax=39
#inc=1.5;    #in milles   (minutes of arcmax)
#arx='in/nodes_sn.npz'
####################################### Fi de usuari

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
print('longituds    {:8.3f}    -----   {:8.3f} \n'.format(tira_lon[0],tira_lon[-1]))
print('latituds     {:8.3f}    -----   {:8.3f} \n'.format(tira_lat[0],tira_lat[-1]))
for j in range(Ny):   
    for i in range(Nx):
        nodes[Nx*j +i,0]=tira_lon[i]
        nodes[Nx*j +i,1]=tira_lat[j]
inc=inc*60
np.savez_compressed(arx, nodes,inc, Nx,Ny,LonMin,LonMax,LatMin,LatMax,tira_lon,tira_lat)


