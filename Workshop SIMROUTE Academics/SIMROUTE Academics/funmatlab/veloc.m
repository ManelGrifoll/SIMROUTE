function vel = veloc(v0,nod_i,nod_f,cost,reduc_id,Lbp,DWT)
% inputs :
%        v0  cruising speed
%        nod_ini edge initial node
%        nod_f  section final node
%        cost to choose swell time
global Nx Ny nodes hs dir
iv=floor(cost)+1;
tau=1-(cost-floor(cost)) ;
hm=0.5*(hs(nod_i,iv)+hs(nod_f,iv));
ang_ship=ang_edge(nod_f,nod_i);

%Speed reduction formulas. Bowditch = 1; Aertssen = 2; Khokhlov = 3; no reduction = 4
if reduc_id == 1
    h_feet=hm*3.28084;  %hm is converted from meters to feets
    %hm=convlength(hm,'m','ft');
    vel=v0-reduc_v_bowditch(ang_ship,dir(nod_f,iv))*h_feet^2;
end
if reduc_id == 2
    vel = v0 - reduc_v_aertssen(ang_ship,dir(nod_f,iv),Lbp,v0,hm);
end
if reduc_id == 3
    vel = v0 - reduc_v_khokhlov(ang_ship,dir(nod_f,iv),hm)*(1 - 1.35e-6*DWT*v0) ;
end
if reduc_id == 4
    vel = v0;
end

if vel<0;
    for i=1:100
        disp('Stop engines, we are going astern')
    end
end
return 
