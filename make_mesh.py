import numpy  as np

LonMin=2.0
LonMax=10.0
LatMin=41.0
LatMax=45.0
inc=1.5;    #in milles   (minutes of arcmax)
inc=inc/60.0    # in deg
Nx=int(np.floor((LonMax-LonMin)/inc)+1)
Ny=int(np.floor((LatMax-LatMin)/inc)+1)

nodes=np.zeros((Nx*Ny,2))
tira_lon=np.arange(LonMin,LonMin+inc*Nx,inc)
tira_lat=np.arange(LatMin,LatMin+inc*Ny,inc)
print( ' Nx = {:6d} ---   Ny = {:4d}\n'.format(Nx,Ny))
print(tira_lon[0])
print(tira_lon[Nx-1])
print(tira_lat[0])
print(tira_lat[Ny-1])
for j in range(Ny):   
    for i in range(Nx):
        nodes[Nx*j +i,0]=tira_lon[i]
        nodes[Nx*j +i,1]=tira_lat[j]
inc=inc*60
np.savez_compressed('nodes.npz', nodes,inc, Nx,Ny,LonMin,LonMax,LatMin,LatMax,tira_lon,tira_lat)
