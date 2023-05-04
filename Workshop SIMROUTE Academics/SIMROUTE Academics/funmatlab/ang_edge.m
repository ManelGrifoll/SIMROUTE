function alfa=ang_edge(n_desti,n_ori)
%This function gives the angle between two nodes
global nodes
x=nodes(n_desti,1)-nodes(n_ori,1);
y=nodes(n_desti,2)-nodes(n_ori,2);
at=atan2d(y,x);
alfa =cart2compass(at);
return
