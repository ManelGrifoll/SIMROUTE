%%% This script plot route and waves in an interval of 1 hour.

close all,clc,clear all

qfix=load('out/TESTCASE_LIV_ALI_fix');%Minimum Distance Route
q=load('out/TESTCASE_LIV_ALI');%Optimized route
load in/waves_20200422;%wave file
load in/nods;%mesh file

%%%%%%%%%%%%%%%%% End Inputs 
[LON,LAT]=meshgrid(tira_lon,tira_lat);
%nt=size(hs);nt=nt(2);
nt=ceil(qfix.cost_fix(end));
Hmax=max(max(max(hs)));

k=0;
for t=1:nt
Hs=squeeze(hs(:,t));%
Dir=squeeze(dir(:,t));
Hs_r=reshape(Hs,Nx,Ny);
Dir_r=reshape(Dir,Nx,Ny);
pcolorjw(LON,LAT,Hs_r');
caxis([0 Hmax])
colorbar,shading flat,hold on,colormap('jet')
Hy=squeeze(Hs_r.*cosd(Dir_r));
Hx=squeeze(Hs_r.*sind(Dir_r));
nred=8;
quiver(LON(1:nred:end,1:nred:end),LAT(1:nred:end,1:nred:end),-Hx(1:nred:end,1:nred:end)',-Hy(1:nred:end,1:nred:end)',2,'k');
% caxis([0.5,5.5]);
load in/ldc_euro_i_mask;
lon(lon<LonMin)=NaN;
lon(lon>LonMax)=NaN;
lat(lat<LatMin)=NaN;
lat(lat>LatMax)=NaN;
plot(lon,lat,'r-')

%We look for the position where there the change occurs
pos=find(q.costt<t);pos_ok=pos(end);
pos2=find(qfix.cost_fix<t);pos2_ok=pos2(end);

%%% We load the algorithm results
plot(qfix.nodes(qfix.nods_trip_fix(pos2_ok),1),qfix.nodes(qfix.nods_trip_fix(pos2_ok),2),'*k')%fix
plot(qfix.nodes(qfix.nods_trip_fix(1:pos2_ok),1),qfix.nodes(qfix.nods_trip_fix(1:pos2_ok),2),'k','linewidth',2)

plot(q.nodes(q.nods_trip(pos_ok),1),q.nodes(q.nods_trip(pos_ok),2),'*m')
plot(q.nodes(q.nods_trip(1:pos_ok),1),q.nodes(q.nods_trip(1:pos_ok),2),'m','linewidth',2)

ttt=num2str(t);
 tit=strcat('Hours since departure time:      ',ttt,' hr'),box on
 title(tit,'fontsize',12,'fontweight','bold')
%saveas(gcf,'SynopticSituation.ai')
     k=k+1
      if k<10  
          nom=strcat('00',num2str(k));
      elseif k <100
          nom=strcat('0',num2str(k));
      else
          nom=strcat(num2str(k));
      end
    set(gcf,'PaperPositionMode','Auto') 
    nom2=['out/plots/' nom]
    print ('-dpng','-zbuffer','-r300',nom2) 
    %pause
    close all


end

display(['The time of OPTIM trip is ' num2str(q.cost_opt) ' hours']);
display(['The time of DIST.MINIMA trip is ' num2str(qfix.cost_fix(end)) ' hores']);
mitja=(q.cost_opt+qfix.cost_fix(end))/2;
display(['Savings percentage ' num2str(100*abs(qfix.cost_fix(end)-q.cost_opt)/mitja) '%']);
return


%arx2=q.ARX;narx=length(arx2);
%arx='in/';






%%% load wave infromation
%hs=zeros(265,24,97);dir=zeros(265,24,97);
hs=zeros(265,97,narx*24);dir=zeros(265,97,narx*24);
for n=1:narx
arx3=strcat(arx,arx2(n));
arx4=num2str(cell2mat(arx3));
hs1=ncread(arx4,'hs');
hs(:,:,24*n-23:24*n)=hs1(:,:,:);
%hs1=permute(hs1,[1 3 2]);
%hs=[hs1 hs];

dir1=ncread(arx4,'dir');
dir(:,:,24*n-23:24*n)=dir1(:,:,:);

end

lon=ncread(arx4,'longitude');
lat=ncread(arx4,'latitude');
[X,Y]=ndgrid(lon,lat);

k=0;
%nt=length(q.nods_trip);
nt=ceil(qfix.cost_fix(end));

for t=1:nt

hsot=squeeze(hs(:,:,t));
dirot=squeeze(dir(:,:,t));
 

figure('position',[ 263   50   519   358])
title('Wave')
%pcolor(X,Y,hsot),
pcolorjw(X,Y,hsot);
colorbar,shading flat,hold on
Hy=squeeze(hsot.*cosd(dirot));
Hx=squeeze(hsot.*sind(dirot));
nred=4;
quiver(X(1:nred:end,1:nred:end),Y(1:nred:end,1:nred:end),Hx(1:nred:end,1:nred:end),Hy(1:nred:end,1:nred:end),0.6,'k');
caxis([0.5,5.5]);

xdata=get(gca,'XTick'),set(gca,'XTick',xdata,'fontsize',12,'fontweight','bold')
tit=title('21 May 2012, 06:00')
set(tit,'fontsize',12,'fontweight','bold');
ylabel('Lat (º)','fontsize',12,'fontweight','bold');xlabel('Lon (º)','fontsize',12,'fontweight','bold')

%ldc
ldc=load('ldc_eur.mat');
plot(ldc.lon,ldc.lat,'k');

% We look for te position where the change occurs
pos=find(q.costt<t);pos_ok=pos(end);
pos2=find(qfix.cost_fix<t);pos2_ok=pos2(end);

%%% We load the algorithm results:
plot(qfix.nodes(qfix.nods_trip_fix(pos2_ok),1),qfix.nodes(qfix.nods_trip_fix(pos2_ok),2),'*k')%fix
plot(qfix.nodes(qfix.nods_trip_fix(1:pos2_ok),1),qfix.nodes(qfix.nods_trip_fix(1:pos2_ok),2),'k','linewidth',2)

plot(q.nodes(q.nods_trip(pos_ok),1),q.nodes(q.nods_trip(pos_ok),2),'*m')
plot(q.nodes(q.nods_trip(1:pos_ok),1),q.nodes(q.nods_trip(1:pos_ok),2),'m','linewidth',2)

axis([-3 15 32 46])

 ttt=num2str(t);
 tit=strcat('Hours since departure time:      ',ttt,' hr'),box on
 title(tit,'fontsize',12,'fontweight','bold')
%saveas(gcf,'SynopticSituation.ai')
     k=k+1
      if k<10  
          nom=strcat('00',num2str(k));
      elseif k <100
          nom=strcat('0',num2str(k));
      else
          nom=strcat(num2str(k));
      end
    set(gcf,'PaperPositionMode','Auto') 
  %  print ('-dpng','-zbuffer','-r300',nom) 
    
    close all
t
end
close all
