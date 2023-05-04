function nnod=search_nods(xlon,xlat,p)
% It gives the closest node on the bottom left side for a given position
% When a third argument is given, it outputs and scheme of the nodes that
% close the argument and their coord
if nargin >2
    p=1;
else
    p=0;
end
load in/nods
inc=inc/60;
xnod=floor((xlon-LonMin)/inc)+1;
xnod+1;
ynod=floor((xlat-LatMin)/inc);
nnod=xnod+Nx*(ynod);
if p==1
disp(' ')
disp('         Nodes Tests')
disp( [num2str(nnod+Nx) '------------' num2str(nnod+Nx+1) '    ' num2str(nodes(nnod+Nx+1,2)) ]   )
disp( ['       (' num2str(xlon) ' ,' num2str(xlat) ')'])
disp( [num2str(nnod) '------------' num2str(nnod+1) '    ' num2str(nodes(nnod+1,2))])
disp( [num2str(nodes(nnod,1)) '            ' num2str(nodes(nnod+1,1))])
end
return