function delta_v = reduc_v_aertssen(ang_ship,ang_wave,Lbp,v0,Hs)
%Aertssen speed penalty
%   Hs: wave significant height, in meters. This is a scalar
%   Lbp: Ship's length between perpendiculars, in meters

if(ang_wave>ang_ship) %/!\ Angles in degrees
 theta=-ang_ship+ang_wave; % Wave encounter angle
else
  theta=ang_ship-ang_wave;  
end
% /!\ for Aertssen, theta must be in [0,180] deg
if 180 < theta && theta <= 360
    theta = 360 - theta;
end

%definition of coefficients m and n:
if Hs < 0
    disp('error, Hs < 0')
    return
end
if (0 <= Hs && Hs < 2.5) % /!\ Hs_m in meters
    m = 0;
    n = 0;
end

if (2.5 <= Hs && Hs < 4.0)
    if 0 <= theta && theta <= 30
        m = 100;
        n = 0;
    end
    if 30 < theta && theta <= 120
        m = 350;
        n = 1;
    end
    if 120 < theta && theta <= 150
        m = 700;
        n = 2;
    end
    if 150 < theta && theta <= 180
        m = 900;
        n = 2;
    end
end

if (4.0 <= Hs && Hs < 5.5)
    if 0 <= theta && theta <= 30
        m = 200;
        n = 1;
    end
    if 30 < theta && theta <= 120
        m = 500;
        n = 3;
    end
    if 120 < theta && theta <= 150
        m = 1000;
        n = 5;
    end
    if 150 < theta && theta <= 180
        m = 1300;
        n = 6;
    end
end

if (5.5 <= Hs && Hs < 7.5)
    if 0 <= theta && theta <= 30
        m = 400;
        n = 2;
    end
    if 30 < theta && theta <= 120
        m = 700;
        n = 5;
    end
    if 120 < theta && theta <= 150
        m = 1400;
        n = 8;
    end
    if 150 < theta && theta <= 180
        m = 2100;
        n = 11;
    end

end

if (7.5 <= Hs)
    if 0 <= theta && theta <= 30
        m = 700;
        n = 3;
    end
    if 30 < theta && theta <= 120
        m = 1000;
        n = 7;
    end
    if 120 < theta && theta <= 150
        m = 2300;
        n = 12;
    end
    if 150 < theta && theta <= 180
        m = 3600;
        n = 18;
    end
end

delta_v = v0*(m/Lbp + n)/100;

end

