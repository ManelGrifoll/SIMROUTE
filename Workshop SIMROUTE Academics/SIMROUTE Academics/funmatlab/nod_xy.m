function nnod=nod_xy(x,y,Nx,Ny)
%Given x,y this function gives the node number of the mesh 
%It will load nods.mat
nnod=Nx*(y-1)+x;