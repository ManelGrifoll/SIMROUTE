function temps_edge= time_edge(v0,n_o,n_e,cost,reduc_id, Lbp, DWT)

% With a edge length given and knowing the cost (time from start point)
% and figuring that height and direction are known, acumulated time is 
% found. It finishes travelling the edge, knowing that
% THERE IS AN HOURLY SWELL RESOLUTION
%global Nx Ny nodes
global nodes hs dir 
L=dist_nods(n_o,n_e);
q=1;  % It will inform whether the edge is done or not
tau=1-(cost-floor(cost)) ; % remaining time for travelling at current speed, swell changes hourly 

while q==1
   if veloc(v0,n_o,n_e,cost,reduc_id,Lbp,DWT)*tau>L      % with tau, remaining time for travelling the edge, it makes it and leaves (q==0)
    %gg=cost%veloc(v0,n_o,n_e,cost,reduc_id)
    cost=cost+L/veloc(v0,n_o,n_e,cost,reduc_id, Lbp, DWT);
   %cost=cost+L/v0; %veloc(v0,n_o,n_e,cost,reduc_id, Lbp, DWT);
    %disp('warning1')
   q=0;
   else
       L=L-veloc(v0,n_o,n_e,cost,reduc_id,Lbp,DWT)*tau;  %now the edge is shorter
       cost=cost+tau; %cost is actualized
       %disp('warning2')
       tau=1; %remaining time is 1 hour      
   end    
end
temps_edge=cost;

return
