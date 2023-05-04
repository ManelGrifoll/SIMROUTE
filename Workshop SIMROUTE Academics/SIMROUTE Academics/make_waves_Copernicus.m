clear all
close all
tic

%%%%%% CREATE WAVE FILES FROM NETCDF FORECASTS %%%%%%
Tini_trip=10;%Time ini trip from 00:00 respect to waves file (e.g. 0 means that begin at 00:00);

%FILES WITH WAVE INFORMATION

ARX={'MED-20200421.nc','MED-20200422.nc'};

%NAME AND FOLDER FOR INTERPOLATED WAVES (output)
arxiu_out='waves_20200422';
dir_arx='in/';

%Mesh to be interpolated:
load in/nods.mat;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% END OF INPUTS %%%%%%

Na=length(ARX); 

last_lon_hight=21; %        longitude from which it is low res
hs_t=NaN*zeros(Nx*Ny,24*Na);   %sea_surface_wave_significant_height
hsf=zeros(Nx,Ny) ;    % interpolated swell within the loop time
fpf=zeros(Nx,Ny) ; 
dirfx=zeros(Nx,Ny) ; 
dirfy=zeros(Nx,Ny) ; 
dir_t=NaN*zeros(Nx*Ny,24*Na);  %sea_surface_wave_from_direction
fp_t=NaN*zeros(Nx*Ny,24*Na);   %sea_surface_wave_peak_frequency
onatge=zeros(Nx*Ny,3);
disp('big matrix have just been created')
arx=[dir_arx ARX{1}];
lon_w=ncread(arx,'longitude');
lat_w=ncread(arx,'latitude');   %     h= hight resolution
%lon_w=ncread(arx,'lon');
%lat_w=ncread(arx,'lat');
[X,Y]=ndgrid(lon_w,lat_w);
Nwx=length(lon_w);              %      w= wave  
Nwy=length(lat_w);              %      l=low
lon_h=lon_w(1:last_lon_hight);
lon_l=lon_w(last_lon_hight:2:end);
lat_l=lat_w(1:2:end);                        %  h hight ses  l  low res
%per hight res                               %XF YF  coor 2x2 nod mesh
[X_h,Y_h]=ndgrid(lon_h,lat_w);               % X  Y  coord 2x2  med mesh
[X_l,Y_l]=ndgrid(lon_l,lat_l);               %minuscule coordnaded 1 dim
%%%%%%%%%%%%%%%%%
% Make interpolable the part of the nodes which are high resolution
Nx_h=Nx;
for i =1 :Nx
 if nodes(i,1)>lon_w(last_lon_hight)
     Nx_h=i-1;
     break   
 end
end
zona='TOT';
if Nx_h==Nx
    disp('everything to hres')
    zona='HIGTH';
 elseif Nx_h==0
    disp('everything to lowres')
    zona='LOW';
end

   xf_h=nodes(1:Nx_h,1);
   yf_h=zeros(Ny,1);
   for k=1:Ny
      yf_h(k)=nodes(1+(k-1)*Nx,2);
   end

   [XF_h,YF_h]=ndgrid(xf_h,yf_h);

   %%%%%%%%%%      %Make low resolution
   xf_l=nodes(Nx_h+1:Nx,1);
   [XF_l,YF_l]=ndgrid(xf_l,yf_h);     % it is the same latitude
   %[XF,YF]=ndgrid(nodes(1:Nx,1),yf_h);

for n=1:Na
    
  arx=[dir_arx ARX{n}]   ;
  hsot=ncread(arx,'VHM0');    %wave height
  dirot=ncread(arx,'VMDR');   %Direction 
  fpot=ncread(arx,'VTM01_SW1');    %Wave period (in seconds)

  for  t=1:24
      disp(['arx n. =' num2str(n) '         t = ' num2str(t)])
     hso=squeeze(hsot(:,:,t));
     diro=squeeze(dirot(:,:,t)); %diro is in degN   (north degrees or compass)
     fpo=squeeze(fpot(:,:,t)); 
     
%interpolations in hres and lowres
 %hs  wave height
     F_h=griddedInterpolant(double(X_h),double(Y_h),hso(1:last_lon_hight,:));
     hsf_h=F_h(XF_h,YF_h);
     hso_l=hso(last_lon_hight:2:end,1:2:end);
     F_l=griddedInterpolant(double(X_l),double(Y_l),hso_l);
     hsf_l=F_l(XF_l,YF_l);
  %fp  Frequency
     H_h=griddedInterpolant(double(X_h),double(Y_h),fpo(1:last_lon_hight,:));
     fpf_h=H_h(XF_h,YF_h);

     fpo_l=fpo(last_lon_hight:2:end,1:2:end);
     H_l=griddedInterpolant(double(X_l),double(Y_l),fpo_l);
     fpf_l=H_l(XF_l,YF_l);

  % dir wave convert the diro from N degrees to cartesian    
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
  
     %put together both res in dir
      dirfx(1:Nx_h,:)=dirxf_h;
      dirfx(Nx_h+1:end,:)=dirxf_l;
      dirfy(1:Nx_h,:)=diryf_h;
      dirfy(Nx_h+1:end,:)=dirfy_l;
     
      zet=complex(dirfx,dirfy);
     dirof=angle(zet)*180/pi;  %cartesian
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
           hs_t(i+Nx*(j-1),24*(n-1)+t)=hsf(i,j);
           dir_t(i+Nx*(j-1),24*(n-1)+t)=dirof(i,j); 
           fp_t(i+Nx*(j-1),24*(n-1)+t)=fpf(i,j);
        end
     end
  
  end 
end
%%%%%%%%%%%%  Modifications to carry out %%%%%%%%%%%%%%%%%%
% Definitive variables to save according to Tini_trip 
    dir=dir_t(:,Tini_trip+1:end);
    hs=hs_t(:,Tini_trip+1:end);
    fp=fp_t(:,Tini_trip+1:end);
    
    
    M=max(hs);
    N=min(hs);
    AVE_hs=mean(isnan(hs));
    
    %D=mean(dir);
    %Mitjana=mean(isnan(dir));
    %disp(['Mean wave direction: ' num2str(Mitjana) 'm'])
    
    disp(['Max. significant wave height: ' num2str(M(1,end)) 'm'])
    %disp(['Min. significant wave height: ' num2str(N(1,end)) 'm'])
    disp(['Average wave height for the trip: ' num2str(AVE_hs(1,end)) 'm'])
  
    
%%%%%%%%%%%%%%%%%%%%%%%%%clear hsf fpf dirfx dirfy
disp( 'Saving the swell')
save([dir_arx arxiu_out],'hs','fp','dir','ARX','Tini_trip')
toc