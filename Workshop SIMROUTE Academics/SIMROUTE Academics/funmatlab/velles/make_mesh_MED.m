clear all
close all

%%%%%%%% CREATES MESH:

%Mesh Dimension (degrees)
% DCorrespon a tot el mediterrani
LonMin=-5.5;LonMax=37.0;LatMin=30.0;LatMax=46.6;

%Resolution
inc=1.5;%en milles   (minuts de arcmax)

%%%%%%%%%%%%% END OF INPUTS %%%%

axis([LonMin LonMax LatMin LatMax]);
%Fem la malla amb aquests dos limits i amb el increment inc
%Calculem Nx i Ny
inc=inc/60.0;
Nx=floor((LonMax-LonMin)/inc)+1;
Ny=floor((LatMax-LatMin)/inc)+1;
nodes=zeros(Nx*Ny,2);
nodes(:,1)=[1:1:Nx*Ny]; 

tira_lon=[LonMin:inc:LonMin+inc*(Nx-1)];
tira_lat=[LatMin:inc:LatMin+inc*(Ny-1)];
% Construim nodes: 
for j=1:Ny
  nodes(Nx*(j-1)+1:Nx*j,1)=tira_lon;
  nodes(Nx*(j-1)+1:Nx*j,2)=tira_lat(j);
end
figure(1)
hold on
plot(nodes(:,1),nodes(:,2),'.k')

plot(nodes(Nx,1),nodes(Nx,2),'*r')
plot(nodes(1,1),nodes(1,2),'*r')
plot(nodes(Nx+1,1),nodes(Nx+1,2),'*g')
load in/ldc_euro_i_mask.mat;
plot(lon,lat,'r-')
inc=inc*60; % per tornarla en minuts
save('in/nods','nodes','Nx','Ny','inc','LonMin','LonMax','LatMin','LatMax')
disp('Feta la malla')