clear all, close all

% plot swell  take the first day at hour 1
% Draw it
dia= 1;
hora=1; 
var=  1                     ; %hs=1 ;   %fp=2,   dir=3
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

load in/nods
%output (modified)
arx_in='in/waves_20200422'

%%end user

arx_mod=[arx_in '_m']

load(arx_in)
hsm=hs;
dirm=dir;
fpm=fp;
clear hs dir fp
load(arx_mod)


t=(dia-1)*24+hora;
lon_n=nodes(1:Nx,1);
lat_n=zeros(Ny,1);
for k=1:Ny
      lat_n(k)=nodes(1+(k-1)*Nx,2);
end
[lon_p,lat_p]=ndgrid(lon_n,lat_n);

vari=zeros(Nx,Ny);
varim=zeros(Nx,Ny);
figure(1)
hold on
for j=1:Ny
   for i=1:Nx
       if var == 1
            vari(i,j)=hs(Nx*(j-1)+i,t);
            varim(i,j)=hsm(Nx*(j-1)+i,t);
         %    caxis([0,2.5]); 
       end
       if var == 2
            vari(i,j)=fp(Nx*(j-1)+i,t);
             varim(i,j)=fpm(Nx*(j-1)+i,t);
         %     caxis([1,6]); 
       end
       if var == 3
            vari(i,j)=dir(Nx*(j-1)+i,t);
            varim(i,j)=dirm(Nx*(j-1)+i,t);
          % caxis([0,360]); 
       end 
  
   end    
end

load in/ldc_euro_i_mask.mat;
lon(lon<LonMin)=NaN;
lon(lon>LonMax)=NaN;
lat(lat<LatMin)=NaN;
lat(lat>LatMax)=NaN;
plot(lon,lat,'r-')


pcolor(double(lon_p),double(lat_p),vari) ,colorbar ,shading flat
title('sea created')
figure(2)
hold on
pcolor(double(lon_p),double(lat_p),varim) ,colorbar ,shading flat
title('sea not created')


plot(lon,lat,'r-')

