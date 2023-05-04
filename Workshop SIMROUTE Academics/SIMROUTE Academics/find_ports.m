% Tool to find final/end nodes from the mesh accordingly lon/lat from a
% Port. Allows to see the limits of the wave map and be
% able to choose a correct node for your port.
close all;
clc;
clear all;

%Introduce mesh information file
load('in/nods.mat')
%Introduce wave field file
load in/waves_20200422 %wave information

%%%%Load wave conditions (with or without modifications).
%Would you like to display the wave field? Y=1 N=0
WF=1;

%Introduce coordinates of a Port:
%LIV_ALI
Lat_port1=42.92;
Lon_port1=10.27;

Lat_port2=38.32;
Lon_port2=-0.27;


%CHI_BCN
%Lat_port1=42.0991;
%Lon_port1=11.6514;

%Lat_port2=41.325;
%Lon_port2=2.325;

%Would you like to display the AIS route? Y=1 N=0
AISR=0;

%Load the AIS rout
if AISR==1
filename='Tenere_13_15_octubre_2021.csv';
end

%Göteborg - Edimburg
%Lat_port1=57.70;
%Lon_port1=11.96;

%Lat_port2=55.95;
%Lon_port2=-3.18;

%Port Said - Malta
%Lat_port1=31.88638;
%Lon_port1=31.78526;

%Lat_port2=35.82303;
%Lon_port2=14.54762;

%PMI_BCN
%Lat_port1=39.48;
%Lon_port1=2.61;

%Lat_port2=41.2728;
%Lon_port2=2.21468;

%%% End of User Inputs
if WF==1;
[LON,LAT]=meshgrid(tira_lon,tira_lat);
%nt=size(hs);nt=nt(2);
%nt=ceil(qfix.cost_fix(end));
Hmax=max(max(max(hs)));
Hs=squeeze(hs(:,1));
Dir=squeeze(dir(:,1));
Hs_r=reshape(Hs,Nx,Ny);
Dir_r=reshape(Dir,Nx,Ny);
pcolorjw(LON,LAT,Hs_r');
caxis([0 Hmax])
colorbar,shading flat,hold on,colormap('jet')
Hy=squeeze(Hs_r.*cosd(Dir_r));
Hx=squeeze(Hs_r.*sind(Dir_r));
end
%Node of origin
Node_port1=search_nods(Lon_port1,Lat_port1,4);
hold on
%el plot següent et pinta la línia vermella de la costa
load in/ldc_euro_i_mask;
plot(lon,lat,'r-','linewidth',1)
h1=plot(nodes(Node_port1,1),nodes(Node_port1,2),'+k','MarkerSize',20);
xlim([LonMin LonMax]);
ylim([LatMin LatMax]);
%Node of destination
Node_port2=search_nods(Lon_port2,Lat_port2,4);
h2=plot(nodes(Node_port2,1),nodes(Node_port2,2),'+g','MarkerSize',20);
xlim([LonMin LonMax]);
ylim([LatMin LatMax]);
if AISR==1;
FILE=readtable(filename);
t=datenum(FILE.x_Timestamp(end)-FILE.x_Timestamp(1)).*24; %Calculate time of the trip in hours
t=fix(t);
FILE.x_Timestamp=datenum((FILE.x_Timestamp(:)-FILE.x_Timestamp(1)).*24);
route=[FILE.x_Timestamp,FILE.Speed,FILE.Course,FILE.Latitude,FILE.Longitude];
%ploteja les coordenades d'inici (punt1) amb un cercle magenta (5=longitud, 4=latitud)
plot(route(1,5),route(1,4),'om')
hold on
%ploteja les coordenades de fi (punt end) amb un cercle magenta (5=longitud, 4=latitud)
plot(route(end,5),route(end,4),'om')
%ploteja la ruta d'origen a fi en magenta (5=longitud, 4=latitud) gruix de
%la linia 2
plot(route(:,5),route(:,4),'-m','linewidth',2)
end
legend([h1 h2],'Origin','Destination');
if isnan(hs(Node_port1,1))
disp('The node of ORIGIN is land')
return
end
if isnan(hs(Node_port2,1))
disp('The node of DESTINATION is land')
return
end
disp(['The port of ORIGIN coordinates are ' num2str(Lat_port1) 'º ' num2str(Lon_port1) 'º']);
disp([' node is ' num2str(Node_port1)])
disp(['The port of DESTINATION coordinates are ' num2str(Lat_port2) 'º ' num2str(Lon_port2) 'º']);
disp([' node is ' num2str(Node_port2)])