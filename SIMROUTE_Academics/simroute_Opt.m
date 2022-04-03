clear all
close all
tic
global Nx Ny nodes hs dir
load in/nods %Mesh information
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%% USER PARAMETER INPUTS: 

%%%%Load wave conditions (with or without modifications).
load in/waves_20200422;%wave infromation

nod_ini=71574;%start point
nod_end=29871;%end point

nom_resul='TESTCASE_LIV_ALI';%Output File Name
plot_onatge=0;  % draw
plot_nods=0; % draw the open ones
astar=1;     % astar=1  algorithm astar; astar=0 algorithm dijstra

reduc_id=1; % select the speed reduction formula. Bowditch = 1; Aertssen = 2; Khokhlov = 3; no reduction = 4
v0=25; % SERVICE SPEED TRETA DE IHS Markit (cruising speed in nautical milles per hour (knots))
Lbp=231.56; % ship's length between perpendiculars (meters)
DWT=7500; % ship's deadweight (tons)


%%%%%%%%%%%%%%%%%%%%%%%%%%% END of USER
disp('swell loaded')
disp('Mesh data loaded')
disp(['Nx=' num2str(Nx) '--------- Ny=' num2str(Ny)]) 
disp([ 'Resolution in minutes  (milles in G.C.)  of the mesh =' num2str(inc)])


if isnan(hs(nod_ini,1))
    disp('The nod_ini is land')
    return
end
if isnan(hs(nod_end,1))
    disp('The nod_end is land')
    return
end

frontier_nods = [1:Nx]; %nods that belong to the bottom frontier of the map
for k = 1:(Ny-2)
    frontier_nods = [frontier_nods, k*Nx+1]; %nods that belong to the left frontier of the map
end
for k = 2:(Ny-1)
    frontier_nods = [frontier_nods, k*Nx]; %nods that belong to the right frontier of the map
end
for k = 1:Nx
    frontier_nods = [frontier_nods, Nx*(Ny-1)+k]; %nods that belong to the upper frontier of the map
end

if ismember(nod_ini,frontier_nods)
    disp('The nod_ini is on the frontier of the map')
    return
end
if ismember(nod_end,frontier_nods)
    disp('The nod_end is on the frontier of the map')
    return
end

if reduc_id == 1
    disp('Bowditch formula used for wave effects on navigation')%= 1;  = 2; Khokhlov = 3; no reduction = 4')
elseif reduc_id == 2
    disp('Aertssen formula used for wave effects on navigation')
elseif reduc_id == 3    
    disp('Khokhlov formula used for wave effects on navigation')
else
    disp('No reduction for wave effects on navigation for wave effects on navigation ')
end
    
disp(['The lon of ini is ' num2str(nodes(nod_ini,1))])
disp(['The lat of ini is ' num2str(nodes(nod_ini,2))])  
%%%%%%%% initializing
%%%    settled each row gives info about the node corresponding the the n. of the row
%     the variable is initialized at zero
%     the first column -> if there is a 1, it means the node is closed
%     the second column gives the cost at which the node has been closed to 
%     the third column the father node, if there is a 4th column, it is for the evaluation function
if astar==1
    settled=zeros(Nx*Ny,4);
else
    settled=zeros(Nx*Ny,3);
end  
%     min_c each row keeps the nodes information, initialized at Inf
%     the first column indicates the cost of the open node, because when the node is closed the info goes to inf, 
%     the second one the father node (when we close the node, we leave inf),the third one of it is
%     astar for the evaluation function 
%
if astar==1
   min_c=Inf(Nx*Ny,3);
else
   min_c=Inf(Nx*Ny,2);
end

pidx=nod_ini;
min_c(pidx,1)=0; %the cost of the start node is 0
min_c(pidx,2)=NaN; %the start node doesn't have a father node
if astar==1
   min_c(pidx,3)=NaN;
end
while pidx~=nod_end;   %pidx of the node to close the first time it is the initial it will finish when it closes the end
  settled(pidx,1)=1;   % it closes the node we are about to expand
  settled(pidx,2)=min_c(pidx,1); %cost node
  settled(pidx,3)=min_c(pidx,2); %father node
 %  disp(['pidx = ' num2str(pidx)])
  if astar==1
     min_c(pidx,3)=Inf;   % we utilize it to Inf
     min_c(pidx,1)=Inf;   % it closes the node
  else
     min_c(pidx,1)=Inf;   % it closes the node
  end
  %disp([num2str(pidx)])    % to check it works 
  neighbor_ids=veins(pidx);   % we expand
  for k=1: length(neighbor_ids);
      cidx=neighbor_ids(k);
      if settled(cidx,1)==0 ; %if node open it works, if closed we do nothing, because there is no else 
          %a=find(mask==cidx); % check if the neighbour is on the barrier
            if ~(isnan(hs(cidx,1)) || (ismember(cidx,frontier_nods)));  
              %if cidx is onshore or on the frontier, we don't evaluate them.
              %hs behaves as mask, because if hs is a NaN, the corresponding node is on the land
              g=time_edge(v0,pidx,cidx,settled(pidx,2),reduc_id,Lbp,DWT); % accumulated time to pass the edge
              if astar==1;
                  heu=dist_nods(cidx,nod_end)/v0;   % heuristic time from the node to the end node
                  if (heu+g)<min_c(cidx,3);  %astar
                      min_c(cidx,1)=g;
                      min_c(cidx,2)=pidx;
                      min_c(cidx,3)=heu+g;
                  end
              else %dijsktra
                  if (g<min_c(cidx,1));
                      min_c(cidx,1)=g;
                      min_c(cidx,2)=pidx;  % father node
                  end
              end
          end
      end
  end
  %the candidate to expand and close is chosen
  if astar==1
     [a pidx]=min(min_c(:,3));  % node of smallest evaluation a
     if pidx==nod_end;
        settled(pidx,1)=1;
        settled(pidx,2)=min_c(pidx,1);
        settled(pidx,3)=min_c(pidx,2);
     end
  else
     [a ,pidx]=min(min_c(:,1));   %node of smallest cost
     if pidx==nod_end;
        settled(pidx,1)=1;
        settled(pidx,2)=min_c(pidx,1);
        settled(pidx,3)=min_c(pidx,2);
     end
  end     
end 
disp(['Finished, reconstructs the path from settled']) 

disp([ 'Total Cost: '   num2str(settled(pidx,2)) ' hours'])
disp([ 'final node ' num2str(pidx)]) 
disp(['The final lon is ' num2str(nodes(nod_end,1))])
disp(['The final lat is ' num2str(nodes(nod_end,2))])  
cost_opt=settled(pidx,2);
% We make the nodes of the trip looking at father starting form nod_end
nod_p=nod_end;
i=1;
nods_trip(1)=nod_end;    %nods_trips the route following the nodes
while nod_p ~=nod_ini
   nod=settled(nod_p,3);
   nods_trip(i+1)=nod;
   nod_p=nod;
   i=i+1;
end
nods_trip=flip(nods_trip);
Ntrip=length(nods_trip); 
vt=zeros(Ntrip,1);    %vt average speed between nodes
for i=Ntrip:-1:2
    vt(i)=dist_nods(nods_trip(i),nods_trip(i-1))/(settled(nods_trip(i),2)-settled(nods_trip(i-1),2));
end
hst=zeros(Ntrip,1);
dirt=zeros(Ntrip,1);
fpt=zeros(Ntrip,1);
costt=zeros(Ntrip,1);
for i=1:Ntrip
    hst(i)=hs(nods_trip(i),1+round(settled(nods_trip(i),2)));
    fpt(i)=fp(nods_trip(i),1+round(settled(nods_trip(i),2)));
    dirt(i)=dir(nods_trip(i),1+round(settled(nods_trip(i),2)));
    costt(i)=settled(nods_trip(i),2);
end
length_opt=dist_trip(nods_trip);   % distance of the trip in milles

disp( ['going through the optimum route of ' num2str(length_opt) ' milles'])
disp( ['the trip time is ' num2str(cost_opt) ' hores']);
AVE_Hs=mean(hst);
save(['out/' nom_resul],'nodes','costt','nods_trip','v0','nod_ini','nod_end','vt',...
    'hst','dirt','fpt','LonMin','LonMax','LatMin','LatMax','ARX','cost_opt','length_opt','Tini_trip',...
    'reduc_id','Lbp','DWT','frontier_nods') 

cost_f=0;

for i=2:Ntrip
    cost_f=time_edge(v0,nods_trip(i-1),nods_trip(i),cost_f,reduc_id, Lbp, DWT);
end
disp(['With a calculation similar to fix the cost is ' num2str(cost_f) ' hours']) 
if plot_nods ==1
    figure(1)
   hold on 
   axis([LonMin LonMax LatMin LatMax]);
   load in/ldc_euro_i_mask.mat
% lon(lon<LonMin)=NaN;
% lon(lon>LonMax)=NaN;
% lat(lat<LatMin)=NaN;
% lat(lat>LatMax)=NaN;
   plot(lon,lat,'r-')
   a=find(min_c(:,2)~=Inf);
   plot(nodes(a,1),nodes(a,2),'b*')
   b=find(min_c(a,1)~=Inf);
   plot(nodes(a(b),1),nodes(a(b),2),'r*')
end
toc
