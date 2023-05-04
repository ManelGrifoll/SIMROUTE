close all
tic
global Nx Ny nodes hs dir
%Simulation file or take out the clim

arx_base='out/TESTCASE_CHI_BCN'
load in/nods
load in/waves_20210110
load (arx_base)
disp('Data of loaded mesh')
disp(['Nx=' num2str(Nx) '--------- Ny=' num2str(Ny)]) 
disp([ 'Resolution in minutes  (nautical milles in G.C.)  of the mesh =' num2str(inc)])
%disp('without climatology')
nom_resul=[arx_base '_fix'];

%%%%%%%%%%%
disp(['ini longitude is ' num2str(nodes(nod_ini,1))])
disp(['ini latitude is ' num2str(nodes(nod_ini,2))])  
%%%%%%%% initializing
astar=1;
%%%    settled each row gives information about the node corresponding to
%%%    n. of row
%     the variable is initialized to zero
%     firts column -> if there is a 1, it means that the node is closed
%     the second column gives the cost at which it has closed
%     the third column is the father node, if there is a 4th column, it is
%     for the evaluation function
if astar==0
  settled=zeros(Nx*Ny,4);
else
    settled=zeros(Nx*Ny,3);
end  
%     min_c each row keeps information about the nodes, initialized at Inf
%     the first column indicates the cost of the open node, because when a node is closed, it is put at inf 
%     the second row is the father (when the node is closed, it is left at inf,the third is
%     astar for the evaluation function
%
if astar==1
   min_c=Inf(Nx*Ny,3);
else
   min_c=Inf(Nx*Ny,2);
end
% here the algorithm searches the optimum route at constant speed (it doesn't depend on it)
pidx=nod_ini;
min_c(pidx,1)=0;
min_c(pidx,2)=NaN;
if astar==1
   min_c(pidx,3)=NaN;
end

while pidx~=nod_end;   %pidx node to close, the first time it is the initial one, it will finish when it closes the end
  settled(pidx,1)=1;   % it closes the node to expland 
  settled(pidx,2)=min_c(pidx,1);
  settled(pidx,3)=min_c(pidx,2); 
  %disp(['pidx = ' num2str(pidx)])
  if astar==1
     min_c(pidx,3)=Inf;   % it is inutilized to min
     min_c(pidx,1)=Inf; 
  else
     min_c(pidx,1)=Inf; 
  end
  %disp([num2str(pidx)])    % to check it is working
  neighbor_ids=veins(pidx);   % expanding 
  for k=1: length(neighbor_ids);
      cidx=neighbor_ids(k);
      if settled(cidx,1)==0 ; % if node is open, it works; if it is closed, nothing is done
        if (~isnan(hs(cidx,1))) ;
           g=dist_nods(cidx,pidx)+settled(pidx,2);   % here the cost is the distance
           if astar==1;                     
              heu=dist_nods(cidx,nod_end);
              if (heu+g)<min_c(cidx,3);
                min_c(cidx,1)=g;
                min_c(cidx,2)=pidx;
                min_c(cidx,3)=heu+g;
             end              
              
           else 
            if (g<min_c(cidx,1));
             min_c(cidx,1)=g; 
             min_c(cidx,2)=pidx;
            end
           end
        end   
      end
  end
  %the candidate to expand and close is chosen
  if astar==1;
     [a pidx]=min(min_c(:,3));
     if pidx==nod_end;
        settled(pidx,1)=1;
        settled(pidx,2)=min_c(pidx,1);
        settled(pidx,3)=min_c(pidx,2);
     end
  else
     [a pidx]=min(min_c(:,1));
     if pidx==nod_end;
        settled(pidx,1)=1;
        settled(pidx,2)=min_c(pidx,1);
        settled(pidx,3)=min_c(pidx,2);
     end
  end     
end 
% disp(['Finished, reconstruct the path from the settled one']) 
 disp([ 'theoretical total distance fixed path: '   num2str(settled(pidx,2)) ' milles'])
 disp( ['if we have a constant v0 = ' num2str(v0) ' kn/h'])
 
 disp([ 'Theoretical cost at v0 ' num2str( settled(pidx,2)/v0) ' hours'])
% disp([ 'final node ' num2str(pidx)]) 
% disp(['The final lon is ' num2str(nodes(nod_end,1))])
% disp(['The finakl lat is ' num2str(nodes(nod_end,2))])  

% Trip nodes are made
nod_p=nod_end;
i=1;
nods_trip_fix(1)=nod_end;
while nod_p ~=nod_ini
   nod=settled(nod_p,3);
   nods_trip_fix(i+1)=nod;
   nod_p=nod;
   i=i+1;
end
nods_trip_fix=flip(nods_trip_fix);
Ntrip=length(nods_trip_fix);
cost_fix(1)=0;

for i=2:Ntrip
    cost_fix(i)=time_edge(v0,nods_trip_fix(i-1),nods_trip_fix(i),cost_fix(i-1),reduc_id,Lbp,DWT);
end
cost_fix=cost_fix';
length_fix=dist_trip(nods_trip_fix);

vt_fix=zeros(Ntrip,1);
for i=Ntrip:-1:2
    vt_fix(i)=dist_nods(nods_trip_fix(i),nods_trip_fix(i-1))/(cost_fix(i)-cost_fix(i-1));%settled(nods_trip_fix(i),2)-settled(nods_trip_fix(i-1),2));
end

% costt=zeros(Ntrip,1);
% for i=1:Ntrip  
%     costt(i)=settled(nods_trip_fix(i),2)/v0;
% end


save(nom_resul,'nodes','cost_fix','length_fix','nods_trip_fix','vt_fix','LonMin','LonMax','LatMin','LatMax','Tini_trip') 

%disp( ['Going through the fixed route of'])% num2str(length_fix) ' milles'])

disp( ['The time of the trip is ' num2str(cost_fix(end)) ' hours  if we have swell at the route fix']);
  
toc