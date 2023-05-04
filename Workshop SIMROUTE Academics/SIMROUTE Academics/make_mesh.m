clear all
close all

%%%%%%%% CREATES MESH:

%Mesh Dimension (degrees)

%CASE TESTS
%MED
LonMin=-5.5;LonMax=17;LatMin=35;LatMax=45; 
%BAL
%LonMin=-5;LonMax=12.9;LatMin=51;LatMax=60; 

%Resolution:
inc=3;% ALPHA; in milles   (minutes of arcmax)

%%%%%%%%%%%%% END OF INPUTS %%%%

axis([LonMin LonMax LatMin LatMax]);
%Make the mesh within these two limits and with the inc increase
%Calculate Nx i Ny
inc=inc/60.0;
Nx=floor((LonMax-LonMin)/inc)+1;
Ny=floor((LatMax-LatMin)/inc)+1;
nodes=zeros(Nx*Ny,2);
nodes(:,1)=[1:1:Nx*Ny]; 

tira_lon=[LonMin:inc:LonMin+inc*(Nx-1)];
tira_lat=[LatMin:inc:LatMin+inc*(Ny-1)];
% Build nodes: 
for j=1:Ny
  nodes(Nx*(j-1)+1:Nx*j,1)=tira_lon;
  nodes(Nx*(j-1)+1:Nx*j,2)=tira_lat(j);
end
figure(1)
hold on
plot(nodes(:,1),nodes(:,2),'.')

plot(nodes(Nx,1),nodes(Nx,2),'*r')
plot(nodes(1,1),nodes(1,2),'*r')
plot(nodes(Nx+1,1),nodes(Nx+1,2),'*g')
load in/ldc_euro_i_mask.mat;

plot(lon,lat,'r-')
inc=inc*60; % to change it into minutes
save('in/nods','nodes','Nx','Ny','inc','LonMin','LonMax','LatMin','LatMax','tira_lat','tira_lon')
disp('Mesh done')