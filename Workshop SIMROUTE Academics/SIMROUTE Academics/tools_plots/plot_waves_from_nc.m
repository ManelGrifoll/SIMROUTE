close all,clear all,clc
%%% TOOL TO PLOT WAVE FIELD FROM .nc (X.Calvo, C.Boren, Ma.grifoll)

%netcdf file
nc=('in/COP-20200928.nc');
time=8;

%%%%%%%%%%% End of User Input %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%



Hs=ncread(nc,'VHM0');
Dir=ncread(nc,'VMDR');
lon_w=ncread(nc,'longitude');
lat_w=ncread(nc,'latitude'); 
Hs=Hs(:,:,time);Hs=Hs';
Dir=Dir(:,:,time);Dir=Dir';
[LON,LAT] = meshgrid(lon_w,lat_w);
Hy=-(Hs.*cosd(Dir));
Hx=-(Hs.*sind(Dir));

figure('position',[150 150 1000 500])

pcolor(LON,LAT,Hs);
shading flat
colorbar
xlabel('Longitude'),ylabel('Latitude')
title('Wave Field')
hold on
load in/ldc_euro_i_mask;
plot(lon,lat,'r-')
nred=4
quiver(LON(1:nred:end,1:nred:end),LAT(1:nred:end,1:nred:end),Hx(1:nred:end,1:nred:end),Hy(1:nred:end,1:nred:end),4,'k')