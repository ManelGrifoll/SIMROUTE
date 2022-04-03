clear all,close all

%%%%% 
% plot swell, take the first day hour 1
% Draw it
load in/nods
%%%%%%%%%%   start user zone inici wave file to modify
load in/waves_20200825

%%%%%%%%%%%%%%%%%%%%% End user zone


[kk ,n_time]=size(hs);
dir_arx='in/';
dia= 1;
hora=1; 
lon_n=nodes(1:Nx,1);
lat_n=zeros(Ny,1);
for k=1:Ny
      lat_n(k)=nodes(1+(k-1)*Nx,2);
end
[lon_p,lat_p]=ndgrid(lon_n,lat_n);
vari=zeros(Nx,Ny);
for j=1:Ny
   for i=1:Nx
       vari(i,j)=hs(Nx*(j-1)+i,1);
   end
end
figure(1)
hold on
pcolor(double(lon_p),double(lat_p),vari) ,colorbar ,shading flat
caxis([0.2,4]);
title('Select the area with the zoom.')
load in/ldc_euro_i_mask.mat;
lon(lon<LonMin)=NaN;
lon(lon>LonMax)=NaN;
lat(lat<LatMin)=NaN;
lat(lat>LatMax)=NaN;
plot(lon,lat,'r-')