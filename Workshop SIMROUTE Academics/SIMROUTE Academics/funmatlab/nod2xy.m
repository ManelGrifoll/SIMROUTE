function [x ,y]=nod2xy(N,Ax)
% N nod to decompose; Ax=Nx nod number on mesh row
x=mod(N,Ax);
y=floor(N/Ax)+1;