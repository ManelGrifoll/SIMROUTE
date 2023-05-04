function degN=cart2compass(deg)
%Function that converts cartesian angles to compass angles
degN = 90 - deg;
idx = find(degN < 0);
degN(idx) = degN(idx) + 360; 
return