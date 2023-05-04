%%%%plot_onatge
%%% Plot the wave conditions of the interpolated file: 

close all, clear all, clc,

%wave file 
load in/waves_20200923CP%([dir arx arxiu_out])% in/onatge

%Time plot from wave file 
Time_plot=24;%Hours since 00:00.

%Variable: Define de variable that you want to plot: :%hs=1 ;   %fp=2,   dir=3
var= 2;
%%%%%%%%%%% End of User Input %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

Hs=squeeze(hs(:,Time_plot));
Hmax=max(max(max(hs)));
Dir=squeeze(dir(:,Time_plot));
load in/nods;
[LON,LAT]=meshgrid(tira_lon,tira_lat);
Hs_r=reshape(Hs,Nx,Ny);
Dir_r=reshape(Dir,Nx,Ny);
pcolorjw(LON,LAT,Hs_r');
caxis([0 Hmax])
colorbar,shading flat,hold on
Hy=squeeze(Hs_r.*cosd(Dir_r));
Hx=squeeze(Hs_r.*sind(Dir_r));
nred=4;
quiver(LON(1:nred:end,1:nred:end),LAT(1:nred:end,1:nred:end),-Hx(1:nred:end,1:nred:end)',-Hy(1:nred:end,1:nred:end)',2.6,'k');
% caxis([0.5,5.5]);
load in/ldc_euro_i_mask;
lon(lon<LonMin)=NaN;
lon(lon>LonMax)=NaN;
lat(lat<LatMin)=NaN;
lat(lat>LatMax)=NaN;
plot(lon,lat,'r-')

load in/ldc_euro_i_mask;
lon(lon<LonMin)=NaN;
lon(lon>LonMax)=NaN;
lat(lat<LatMin)=NaN;
lat(lat>LatMax)=NaN;
plot(lon,lat,'r-')

return


%Example for intermidate plot
%day:
dia= 1;
%hour:
hora=1;








load in/nods;
dir_arx='../in/'
t=(dia-1)*24+hora;
arx=[dir_arx ARX{dia}];   % pels meds
lon_n=nodes(1:Nx,1);
lat_n=zeros(Ny,1);
for k=1:Ny
      lat_n(k)=nodes(1+(k-1)*Nx,2);
end
[lon_p,lat_p]=ndgrid(lon_n,lat_n);
vari=zeros(Nx,Ny);
varih=zeros(Nx,Ny);
for j=1:Ny
   for i=1:Nx
       if var == 1
            vari(i,j)=hs(Nx*(j-1)+i,t);
            
       end
       if var == 2
            vari(i,j)=fp(Nx*(j-1)+i,t);
       end
       if var == 3
            vari(i,j)=dir(Nx*(j-1)+i,t);
       end 
   %varih(i,j)=hh(Nx*(j-1)+i,t);
   end    
end
figure(1)
hold on
pcolor(double(lon_p),double(lat_p),vari) ,colorbar ,shading flat

if var == 1
   caxis([0.2,4]);
   nom='hs';
end
 if var == 2
   caxis([1,6]);
   nom='fp';
end
if var == 3
   caxis([0,360])
   nom='dir';
end
load in/ldc_euro_i_mask;
lon(lon<LonMin)=NaN;
lon(lon>LonMax)=NaN;
lat(lat<LatMin)=NaN;
lat(lat>LatMax)=NaN;
plot(lon,lat,'r-')
box on
title(['Variable ' nom '  dia = ' num2str(dia) '  hora = ' num2str(hora)])

% figure(10)
% hold on
% pcolor(double(lon_p),double(lat_p),varih) ,colorbar ,shading flat
% 
% 
%    caxis([0.2,4]);
%    nom='hh';





%load ldc_euro_i_mask.mat;
lon(lon<LonMin)=NaN;
lon(lon>LonMax)=NaN;
lat(lat<LatMin)=NaN;
lat(lat>LatMax)=NaN;
plot(lon,lat,'r-')
 
  
return
last_lon_hight=193;

lon_w=ncread(arx,'longitude');
lat_w=ncread(arx,'latitude');   %     h= hight resolution
[X,Y]=ndgrid(lon_w,lat_w);
Nwx=length(lon_w);              %      w= wave  
Nwy=length(lat_w);              %      l=low
lon_h=lon_w(1:last_lon_hight);
lon_l=lon_w(last_lon_hight:2:end);
lat_l=lat_w(1:2:end);                        %  h hight ses  l  low res
%per hight res                               
[X_h,Y_h]=ndgrid(lon_h,lat_w);               % X  Y  coord 2x2  malla med
[X_l,Y_l]=ndgrid(lon_l,lat_l);
disp('ara arem la lectura')


if var==1
    varim=ncread(arx,'VHM0');
end
if var==3
    varim = ncread(arx,'VMDR');
end
if var==2
    varim=ncread(arx,'VSMC');    %frequencia de l'ona
end

disp ('arabe el grafic')
figure(2)
hold on
pcolor(X_h,Y_h,varim(1:last_lon_hight,:,hora)), colorbar,shading flat
title(['Variable Med hightres ' nom '  dia = ' num2str(dia) '  hora = ' num2str(hora)])

if var == 1
   caxis([0.2,4])
end
 if var == 2
   caxis([1,6])
end
if var == 3
   caxis([0,360])
end
%%%%%%% representacio lowres
lon_l=lon_w(last_lon_hight:2:end);
lat_l=lat_w(1:2:end);    
[X_l,Y_l]=ndgrid(lon_l,lat_l);
figure(3)
       
pcolor(X_l,Y_l,squeeze(varim(last_lon_hight:2:end,1:2:end,hora))) ,colorbar,shading flat,hold on
title(['Variable Med low res ' nom '  dia = ' num2str(dia) '  hora = ' num2str(hora)])          
if var == 1
   caxis([0.2,4])
end
 if var == 2
   caxis([1,6])
end
if var == 3
   caxis([0,360])
end


%load ldc_euro_i_mask.mat;
% lon(lon<LonMin)=NaN;
% lon(lon>LonMax)=NaN;
% lat(lat<LatMin)=NaN;
% lat(lat>LatMax)=NaN;
% plot(lon,lat,'r-')
%  
    
 