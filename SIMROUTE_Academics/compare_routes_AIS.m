close all;
clear all;
clc;

%%% LOADING OF FILES 

%ROUTES MUST BE INTRODUCED IN THE FOLLOWING FORMAT: 
%[t(yyyy-MM-dd HH:mm:SS) Speed Course Heading LAT LONG] (CSV)
%[t(yyyy-MM-dd HH:mm:SS) Source Speed Course LAT LONG] (CSV)

%                                         (INPUT)

nom_resul3='Cruise_Roma_10_jan_2021_ROUTES_COMP';
formatspec='%{yyyy-MM-dd HH:mm:SS}D%f%f%f%f%f';
filename='Cruise_Roma_10_jan_2021.csv'; %AIS route (Preferably files of the type .csv)
q=load('TESTCASE_CHI_BCN.mat'); %Optimized SIMROUTE route
qfix=load('out/TESTCASE_CHI_BCN_fix');%Minimum Distance Route


%LonMin=-6;LonMax=24;LatMin=35;LatMax=46; %Spain to Greece
%LonMin=-5.5;LonMax=37.0;LatMin=30;LatMax=46; %Eastern Mediterranean
%LonMin=-11;LonMax=17.0;LatMin=34;LatMax=51; %Western Mediterranean
LonMin=-6;LonMax=18.0;LatMin=34;LatMax=44.6; %Spain to Italy
%LonMin=-2;LonMax=5.0;LatMin=37;LatMax=43;%Catalan countries
%LonMin=-6;LonMax=10;LatMin=34;LatMax=44.6; %Eastern Spain

%Introduce mesh information file
load('in/nods.mat')

%Introduce wave field file
load in/waves_20210110 %wave information

%%%%Load wave conditions (with or without modifications).
%Would you like to display the wave field? Y=1 N=0
WF=1;

%Would you like to display the AIS route? Y=1 N=0
AISR=1;

%Load the AIS rout
if AISR==1
filename='Cruise_Roma_10_jan_2021.csv';
end

%Introduce coordinates of a Port:

%CHI_BCN
Lat_port1=42.0991;
Lon_port1=11.6514;

Lat_port2=41.325;
Lon_port2=2.325;

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

%%EUROPE MASK
%load in/ldc2;
load in/ldc_euro_h_mask;
%load in/ldc_euro_mask;
%load in/ldc_euro_i_mask;

%%% END OF LOADING %%%%%%%%%%%%%%%%%%%%%%%%

[fPath, fName, fExt] = fileparts(filename);

%Start of operations


FILE=readtable(filename);

t=datenum(FILE.x_Timestamp(end)-FILE.x_Timestamp(1)).*24; %Calculate time of the trip in hours
t=fix(t);
FILE.x_Timestamp=datenum((FILE.x_Timestamp(:)-FILE.x_Timestamp(1)).*24);

route=[FILE.x_Timestamp,FILE.Speed,FILE.Course,FILE.Latitude,FILE.Longitude];

xx=(0:0.083:t)';
finish=route(end,:);

route=[xx,interp1(FILE.x_Timestamp,FILE.Speed,xx,'linear','extrap'),interp1(FILE.x_Timestamp,FILE.Course,xx,'linear','extrap'),interp1(FILE.x_Timestamp,FILE.Latitude,xx,'linear','extrap'),interp1(FILE.x_Timestamp,FILE.Longitude,xx,'linear','extrap');finish];

LatRad=deg2rad(FILE.Latitude);
LongRad=deg2rad(FILE.Longitude);

h=numel(LatRad)-1;        
for k=1:1:h
    A(k,1)=sin(LatRad(k)).*sin(LatRad(k+1));
    B(k,1)=cos(LatRad(k)).*cos(LatRad(k+1)).*cos(LongRad(k+1)-LongRad(k));
end

Cosd=A+B;
d=rad2deg(acos(Cosd))*60;
dTOTAL=sum(d);
averageSpeed=mean(FILE.Speed);
%averageSpeed=mean_weighted(FILE.Speed);
savingshour=route(end,1)-q.cost_opt;
savingsdistance=dTOTAL-q.length_opt;
savingspercentagedist=savingsdistance*100/dTOTAL;
savingspercentage=savingshour*100/route(end,1);

plot(route(1,5),route(1,4),'om')
hold on
plot(route(end,5),route(end,4),'om')
h1=plot(route(:,5),route(:,4),'-g','linewidth',2);

xlabel('Longitude'),ylabel('Latitude')
plot(lon,lat,'k-')
nred=2;
axis([LonMin LonMax LatMin LatMax]);

set(gcf,'PaperPositionMode','Auto')

pos=find(q.costt<t);pos_ok=pos(end);

plot(q.nodes(q.nods_trip(end),1),q.nodes(q.nods_trip(end),2),'ok')
plot(q.nodes(q.nods_trip(1),1),q.nodes(q.nods_trip(1),2),'ok')
h2=plot(q.nodes(q.nods_trip(1:end),1),q.nodes(q.nods_trip(1:end),2),'-m','linewidth',2);

plot(qfix.nodes(qfix.nods_trip_fix(end),1),qfix.nodes(qfix.nods_trip_fix(end),2),'ok')
plot(qfix.nodes(qfix.nods_trip_fix(1),1),qfix.nodes(qfix.nods_trip_fix(1),2),'ok')
h3=plot(qfix.nodes(qfix.nods_trip_fix(1:end),1),qfix.nodes(qfix.nods_trip_fix(1:end),2),'-k','linewidth',2);

legend([h1 h2 h3],'AIS obtained route','Optimized route','Minimum distance rute')
tit=nom_resul3;box on
title(tit,'fontsize',12,'fontweight','bold')

disp(['Total time with optimization                   ' num2str(q.costt(end)) '   hours'])

disp(['Distance with optimization                     ' num2str(q.length_opt) ' miles'])

disp(['Total time in reality, obtained from AIS data  ' num2str(route(end,1)) '  hours'])

disp(['Distance obtained from AIS data                ' num2str(dTOTAL) ' miles'])

disp(['Average speed of                               ' num2str(averageSpeed) '   kn'])

disp(['Time saved                                     ' num2str(savingshour) '   hours'])

disp(['Percentage of saved time                       ' num2str(savingspercentage) '  % (h)'])

disp(['Distance saved                                 ' num2str(savingsdistance) '  miles'])

disp(['Percentage of saved distance                   ' num2str(savingspercentagedist) '  % (miles)'])

disp(['Port of origin                                 ' num2str(route(1,4)) 'º ' num2str(route(1,5)) 'º'])

disp(['Port of destination                            ' num2str(route(end,4)) 'º ' num2str(route(end,5)) 'º'])

Time_opt_route=q.costt(end);
Dist_opt_route=q.length_opt;
Time_AIS_route=route(end,1);
Lat_ini=route(1,4);
Lon_ini=route(1,5);
Lat_end=route(end,4);
Lon_end=route(end,5);

save(['out/' nom_resul3],'Time_opt_route','Dist_opt_route','Time_AIS_route','dTOTAL','averageSpeed',...
    'savingshour','savingspercentage','savingsdistance','savingspercentagedist','Lat_ini','Lon_ini',...
    'Lat_end','Lon_end');


set(gcf,'PaperPositionMode','Auto') 
nom_resul3_2=['out/compare_routes_figures/' nom_resul3];
print ('-dpng','-r300',nom_resul3_2)

