function khokhlov_factor = reduc_v_khokhlov(ang_ship,ang_wave,Hs)
%Khokhlov speed penalty
%   Hs: wave significant height, in meters
if(ang_wave>ang_ship)
 theta=-ang_ship+ang_wave; %Wave encounter angle
else
  theta=ang_ship-ang_wave;  
end
% /!\ for Khokhlov, theta must be in [0,180] deg
if 180 < theta && theta <= 360
    theta = 360 - theta;
end

% /!\ Angle in degrees, we need to convert it to radians:
theta_rad = pi/180*theta;

khokhlov_factor = (0.745 - 0.245*(pi-theta_rad))*Hs;
return

