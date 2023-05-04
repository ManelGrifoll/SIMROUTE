clear all
close all
tic

%%%%%% CREATE WAVE FILES FROM NETCDF FORECASTS %%%%%%

%FILES WITH WAVE INFORMATION
ARX={'HW-20161120-HC.nc','HW-20161121-HC.nc','HW-20161122-HC.nc'}%,'HW-20161123-HC.nc','HW-20161124-HC.nc','HW-20161125-HC.nc','HW-20161126-HC.nc','HW-20161127-HC.nc','HW-20161128-HC.nc'};%

%NAME AND FOLDER FOR INTERPOLATED WAVES (output)
arxiu_out='waves_20161120_20161122';
dir_arx='in/';
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% END OF INPUTS %%%%%%

Na=length(ARX); 
load in/nods.mat;
last_lon_hight=193; %        longitud a partir de la qual es low res
hs=NaN*zeros(Nx*Ny,24*Na);   %sea_surface_wave_significant_height
hsf=zeros(Nx,Ny) ;    % onatge interpolat en el temps del bucle
fpf=zeros(Nx,Ny) ; 
dirfx=zeros(Nx,Ny) ; 
dirfy=zeros(Nx,Ny) ; 
dir=NaN*zeros(Nx*Ny,24*Na);  %sea_surface_wave_from_direction
fp=NaN*zeros(Nx*Ny,24*Na);   %sea_surface_wave_peak_frequency
onatge=zeros(Nx*Ny,3);
disp('acabo de crear matrius grans')
arx=[dir_arx ARX{1}];
lon_w=ncread(arx,'longitude');
lat_w=ncread(arx,'latitude');   %     h= hight resolution
[X,Y]=ndgrid(lon_w,lat_w);
Nwx=length(lon_w);              %      w= wave  
Nwy=length(lat_w);              %      l=low
lon_h=lon_w(1:last_lon_hight);
lon_l=lon_w(last_lon_hight:2:end);
lat_l=lat_w(1:2:end);                        %  h hight ses  l  low res
%per hight res                               %XF YF  coor 2x2 malla nod
[X_h,Y_h]=ndgrid(lon_h,lat_w);               % X  Y  coord 2x2  malla med
[X_l,Y_l]=ndgrid(lon_l,lat_l);               %minuscula coordnaded 1 dim
Nx_h=search_nods(lon_w(last_lon_hight),lat_w(1));
xf_h=nodes(1:Nx_h,1);
yf_h=zeros(Ny,1);
for k=1:Ny
      yf_h(k)=nodes(1+(k-1)*Nx,2);
end
[XF_h,YF_h]=ndgrid(xf_h,yf_h);
%Llegim el primer arxiu
% problemes al fer la alta resolucio
xf_l=nodes(Nx_h+1:Nx,1);
[XF_l,YF_l]=ndgrid(xf_l,yf_h);     % es la mateixa latitud
[XF,YF]=ndgrid(nodes(1:Nx,1),yf_h);


for n=1:Na
    
  arx=[dir_arx ARX{n}]   ;
  hsot=ncread(arx,'VHM0');    %Alçada d'ona
  dirot=ncread(arx,'VMDR');   %Direccio 
  fpot=ncread(arx,'VSMC');    %Periode de l'ona (en segons)

  for  t=1:24
      disp(['arx n. =' num2str(n) '         t = ' num2str(t)])
     hso=squeeze(hsot(:,:,t));
     diro=squeeze(dirot(:,:,t)); %diro esta en degN   (graus north o compass)
     fpo=squeeze(fpot(:,:,t)); 
     
%interpolations en hres i lowres
 %hs  altura  ona
     F_h=griddedInterpolant(double(X_h),double(Y_h),hso(1:last_lon_hight,:));
     hsf_h=F_h(XF_h,YF_h);
     clear F_h 
     hso_l=hso(last_lon_hight:2:end,1:2:end);
     F_l=griddedInterpolant(double(X_l),double(Y_l),hso_l);
     hsf_l=F_l(XF_l,YF_l);
  %fp  Frequebcia
     H_h=griddedInterpolant(double(X_h),double(Y_h),fpo(1:last_lon_hight,:));
     fpf_h=H_h(XF_h,YF_h);

     fpo_l=fpo(last_lon_hight:2:end,1:2:end);
     H_l=griddedInterpolant(double(X_l),double(Y_l),fpo_l);
     fpf_l=H_l(XF_l,YF_l);

  % dir de ona passem el diro de grausN a cartesia    
     for i=1:Nwx
       for j=1:Nwy
            a=compass2cart(diro(i,j));
            if length(a)==1
             diro(i,j)=a;
            end
        end
     end
     dirx=cosd(diro(:,:));
     diry=sind(diro(:,:));
   
     G_h=griddedInterpolant(double(X_h),double(Y_h),dirx(1:last_lon_hight,:));
     dirxf_h=G_h(XF_h,YF_h);

     dirx_l=dirx(last_lon_hight:2:end,1:2:end);
     G_l=griddedInterpolant(double(X_l),double(Y_l),dirx_l);
     dirxf_l=G_l(XF_l,YF_l);

    
     G_h=griddedInterpolant(double(X_h),double(Y_h),diry(1:last_lon_hight,:));
     diryf_h=G_h(XF_h,YF_h);

     diry_l=diry(last_lon_hight:2:end,1:2:end);
     G_l=griddedInterpolant(double(X_l),double(Y_l),diry_l);
     dirfy_l=G_l(XF_l,YF_l);
  
     %ajuntemles dues res a dir
      dirfx(1:Nx_h,:)=dirxf_h;
      dirfx(Nx_h+1:end,:)=dirxf_l;
      dirfy(1:Nx_h,:)=diryf_h;
      dirfy(Nx_h+1:end,:)=dirfy_l;
     
      zet=complex(dirfx,dirfy);
     dirof=angle(zet)*180/pi;  %cartesia
      for i=1:Nx
        for j=1:Ny
            dirof(i,j)=cart2compass(dirof(i,j));
         end
      end    
%%%%%%%%%%%%%      
 
      hsf(1:Nx_h,:)=hsf_h;
      hsf(Nx_h+1:end,:)=hsf_l;
      clear hsf_l hfs_h
      fpf(1:Nx_h,:)=fpf_h;
      fpf(Nx_h+1:end,:)=fpf_l;

     for j=1:Ny
        for i=1:Nx  
           hs(i+Nx*(j-1),24*(n-1)+t)=hsf(i,j);
           dir(i+Nx*(j-1),24*(n-1)+t)=dirof(i,j); 
            fp(i+Nx*(j-1),24*(n-1)+t)=fpf(i,j);
        end
     end
  
  end 
end
%%%%%%%%%%%%%%%%%%%%%%%%%clear hsf fpf dirfx dirfy
disp( 'Gravant el onatge')
save([dir_arx arxiu_out],'hs','fp','dir','ARX')
toc