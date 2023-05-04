
close all;
clear all;
clc;
 
%%% LOADING OF FILES 
 
%[t(yyyy-MM-dd HH:mm:SS) Source Speed Course LAT LONG] (CSV)
 
formatspec='%{yyyy-MM-dd HH:mm:SS}D%f%f%f%f%f';
filename='Cruise_Roma_10_jan_2021.csv'; %AIS route
nom_ruta_AIS='Cruise_Roma_10_jan_2021_PREP.mat';% Name of the output file


%%% END OF LOADING %%%%%%%%%%%%%%%%%%%%%%%
 
FILE=readtable(filename);
 
departure=FILE.x_Timestamp(1);
arrival=FILE.x_Timestamp(end);

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
 
disp(['Total time in reality, obtained from AIS data  ' num2str(route(end,1)) '   hours'])
        
disp(['Distance obtained from AIS data                ' num2str(dTOTAL) ' miles'])
 
disp(['Average speed of                               ' num2str(averageSpeed) '  kn'])
 
disp(['Port of origin                                 ' num2str(route(1,4)) 'º ' num2str(route(1,5)) 'º'])
 
disp(['Port of destination                            ' num2str(route(end,4)) 'º ' num2str(route(end,5)) 'º'])

save(['out/' nom_ruta_AIS],'route','dTOTAL','averageSpeed') 

return

