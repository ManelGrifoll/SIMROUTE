%avaloacio test3 per detectar diferencues amb el python

clear all,close all
tic
global Nx Ny nodes hs dir
load in/nods %Mesh information
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%% USUR PARAMETRE INPUTS: 

%%%%Load wave conditions (with or without modifications).
%load in/waves_20161120_20161122_m   % onatge
load in/waves_20170121 %wave infromation

%nod_ini=770861;%bcn
%nod_end=920868;%livorno
nod_ini=25477;%start point
nod_end=10764;%end point+-
%%%%%%%%%%%%%%%  treure  es de prova1  ni ha 3
file66 = fopen('out/test3.txt','w');
%%%%%%%%%%%%%   acaba prova1



nom_resul='BCN_PM';%Nom Arxiu Sortida
v0=16.1 ;% velocitat de creuer en milles nautiques per hora (nusos)
plot_onatge=1;  % graficar
plot_nods=0; % grafica els oberts
astar=1;     % astar=1  algorotme astar; astar=0 algorithm dijstra

%%%%%%%%%%%%%%%%%%%%%%%%%%% END of USER
disp('carregat onatge')
disp('Dades de la malla carregada')
disp(['Nx=' num2str(Nx) '--------- Ny=' num2str(Ny)]) 
disp([ 'Resolucio en minuts  (milles nautiques en G.C.)  de la malla =' num2str(inc)])


if isnan(hs(nod_ini,1))
    disp('El nod_ini is land')
    return
end
if isnan(hs(nod_end,1))
    disp('El nod_end is land')
    return
end

    
disp(['La lon del ini es ' num2str(nodes(nod_ini,1))])
disp(['La lat del ini es ' num2str(nodes(nod_ini,2))])  
%%%%%%%% inicialitzem
%%    settled cada  fila dona informacio sobre el node correpoment al n. de fila
%     la variables esta inicialitzada a zero
%     la primerta columna -> si te un 1 vols dir que el node esta tencat
%     la segona columna dona el cost a que s'ha tencat
%     la tercera columna el node pare, la 4 si hi es perla funcio avaluacio
if astar==1
  settled=zeros(Nx*Ny,4);
else
    settled=zeros(Nx*Ny,3);
end  
%     min_c cada fila guarda infirmacio dels nodes, inicialitzada a Inf
%     la primera columna indica el cost del node obret, ja que quan tanquem un node la posem a inf 
%     la segona el node pare (quan tanquem el node deixem inf,la tercer si
%     es astar per la funcio de avaluacio
%
if astar==1
   min_c=Inf(Nx*Ny,3);
else
   min_c=Inf(Nx*Ny,2);
end

pidx=nod_ini;
min_c(pidx,1)=0;
min_c(pidx,2)=NaN;
if astar==1
   min_c(pidx,3)=NaN;
end
total=0;
%while pidx~=nod_end;   %pidx del node a tancar la primera vegada es el inicial acabara quant tenqui el final
while pidx~=nod_end;   
  total=total+1;
  settled(pidx,1)=1;   % tenca el noda que anem  a expandir
  settled(pidx,2)=min_c(pidx,1); %cost node
  settled(pidx,3)=min_c(pidx,2); %node pare
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%   prova2
  fprintf(file66, '===========================\n');
  fprintf(file66,' %5d  %10.5f   %10.5f     ***  pare***\n', pidx,   settled(pidx,2), min_c(pidx,3));
 
        
   %disp(['pidx = ' num2str(pidx)])
  if astar==1
     min_c(pidx,3)=Inf;   % el inutilitzem a Infinit
     min_c(pidx,1)=Inf; 
  else
     min_c(pidx,1)=Inf; 
  end
  %disp([num2str(pidx)])    % per veure si treballa
  neighbor_ids=veins(pidx);   %expandim
  for k=1: length(neighbor_ids);
      cidx=neighbor_ids(k);
      if settled(cidx,1)==0 ; %si el node obert trbeallen, si  tancat no fem  res
        
        %a=find(mask==cidx); %veure si vei esta a la barrera de moment la barrera es els nans del onatge
        if ~isnan(hs(cidx,1)) ;  %hs fa el paper de mask
           g=time_edge(v0,pidx,cidx,settled(pidx,2)); % temps acumulat per pssar la aresta
           if astar==1;
               heu=dist_nods(cidx,nod_end)/v0;   % heristic  temps  del node al node final
              if (heu+g)<min_c(cidx,3);  %astar
                min_c(cidx,1)=g;
                min_c(cidx,2)=pidx;
                min_c(cidx,3)=heu+g;
                if isinf(min_c(cidx,1))== 1
                      fprintf(file66,' %5d  %10.5f   %10.5f   nova evalu \n', cidx,   g, heu+g);
                end 
             end              
              
           else 
            if (g<min_c(cidx,1));
             min_c(cidx,1)=g;    %djsktra
             min_c(cidx,2)=pidx;  % nod pare
            end
           end
        end   
      end
  end
  %Escollim candidat per expandir i tancar
  if astar==1
     [a pidx]=min(min_c(:,3));  % el nod d avaluacio mes petita
     if pidx==nod_end;
        settled(pidx,1)=1;
        settled(pidx,2)=min_c(pidx,1);
        settled(pidx,3)=min_c(pidx,2);   
        
        
        
     end
  else
     [a ,pidx]=min(min_c(:,1));   %el nod que te cost mes petit
     if pidx==nod_end
        settled(pidx,1)=1;
        settled(pidx,2)=min_c(pidx,1);
        settled(pidx,3)=min_c(pidx,2);
     end
  end     
end 
disp(['Acabat, reconstrueix el cami a partir del settled']) 

disp([ 'Cost total: '   num2str(settled(pidx,2)) ' hores'])
disp([ 'node final el ' num2str(pidx)]) 
disp(['La lon del final es ' num2str(nodes(nod_end,1))])
disp(['La lat del final es ' num2str(nodes(nod_end,2))])  
cost_opt=settled(pidx,2);
%Fem els nodes del trip  mirant els pares començant pel nod_end
% nod_p=nod_end;
% i=1;
% nods_trip(1)=nod_end;    %nods_trips la routa seguint els nodes
% while nod_p ~=nod_ini
%    nod=settled(nod_p,3);
%    nods_trip(i+1)=nod;
%    nod_p=nod;
%    i=i+1;
% end
% nods_trip=flip(nods_trip);
% Ntrip=length(nods_trip); 
% vt=zeros(Ntrip,1);    %vt velocitat mitjana entre nodes
% for i=Ntrip:-1:2
%     vt(i)=dist_nods(nods_trip(i),nods_trip(i-1))/(settled(nods_trip(i),2)-settled(nods_trip(i-1),2));
% end
% hst=zeros(Ntrip,1);
% dirt=zeros(Ntrip,1);
% fpt=zeros(Ntrip,1);
% costt=zeros(Ntrip,1);
% for i=1:Ntrip
%     hst(i)=hs(nods_trip(i),1+round(settled(nods_trip(i),2)));
%     fpt(i)=fp(nods_trip(i),1+round(settled(nods_trip(i),2)));
%     dirt(i)=dir(nods_trip(i),1+round(settled(nods_trip(i),2)));
%     costt(i)=settled(nods_trip(i),2);
% end
% length_opt=dist_trip(nods_trip);   % distancia en milles del trip
% 
% disp( ['Anant pel la ruta optima  de ' num2str(length_opt) ' milles'])
% disp( ['El temps del trip es de ' num2str(cost_opt) ' hores']);
% save(['out/' nom_resul],'nodes','costt','nods_trip','v0','nod_ini','nod_end','vt',...
%     'hst','dirt','fpt','LonMin','LonMax','LatMin','LatMax','ARX','cost_opt','length_opt','Tini_trip') 
% 
% cost_f=0;
% 
% for i=2:Ntrip
%     cost_f=time_edge(v0,nods_trip(i-1),nods_trip(i),cost_f);
% end
% disp(['Amb calcul similar al fix el cost surt ' num2str(cost_f) ' hores']) 
% if plot_nods ==1
%     figure(1)
%    hold on 
%    axis([LonMin LonMax LatMin LatMax]);
%    load in/ldc_euro_i_mask.mat
% % lon(lon<LonMin)=NaN;
% % lon(lon>LonMax)=NaN;
% % lat(lat<LatMin)=NaN;
% % lat(lat>LatMax)=NaN;
%    plot(lon,lat,'r-')
%    a=find(min_c(:,2)~=Inf);
%    plot(nodes(a,1),nodes(a,2),'b*')
%    b=find(min_c(a,1)~=Inf);
%    plot(nodes(a(b),1),nodes(a(b),2),'r*')
% end


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%prova3
fclose(file66);
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
toc
