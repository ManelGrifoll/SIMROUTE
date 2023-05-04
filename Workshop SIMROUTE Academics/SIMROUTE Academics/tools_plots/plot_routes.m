close all,clc,clear all

%files:
q_fix=load('out/BCN_GEN_fix');
q=load('out/BCN_GEN');


disp(['Time total optimization ' num2str(q.costt(end)) ' hours'])
disp(['Time total without optimization (with wave effect)' num2str(q_fix.cost_fix(end)) ' hours']) 
Time_base=q_fix.length_fix/q.v0;

disp(['Time total without optimization (without wave effects)' num2str(Time_base) ' hours']) 
disp(['Distance optimizatation: ' num2str(q.length_opt) ' milles'])
disp(['Distance minimum: ' num2str(q_fix.length_fix) ' milles']) 

figure(1)
load in/ldc_euro_i_mask;
load in/nods;
lon(lon<LonMin)=NaN;
lon(lon>LonMax)=NaN;
lat(lat<LatMin)=NaN;
lat(lat>LatMax)=NaN;
plot(q.nodes(q.nods_trip,1),q.nodes(q.nods_trip,2),'r','linewidth',2)
hold on
plot(q_fix.nodes(q_fix.nods_trip_fix,1),q_fix.nodes(q_fix.nods_trip_fix,2),'g','linewidth',2)
plot(lon,lat,'k-')
leg=legend('Optimized route','Minimum Distance route','Coastline')
set(leg,'Position',[0.144047626923947 0.780158733351836 0.355357134980815 0.119047615854513]);
xlabel('Longitude (º)')
ylabel('Latitude (º)')
title('SIMROUTE\copyright')
