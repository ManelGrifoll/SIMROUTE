function f_theta=reduc_v_bowditch(ang_ship,ang_wave)
%Bowditch speed penalty
if(ang_wave>ang_ship) %% /!\ Angles in degrees
 theta=-ang_ship+ang_wave; %Wave encounter angle: angle between the ship motion direction and the waves direction
else
  theta=ang_ship-ang_wave;  
end
if ((theta>=45 && theta<=135)||(theta>=225 && theta<=315))
    f_theta=0.0165;
    return
end
if (theta>135 && theta<225)
    f_theta=0.0248;
    return
end
if ((theta>=0 && theta<45)||(theta>315 && theta<=360))
    f_theta=0.0083;
    return
end
disp([num2str(ang_ship) 'kkkk ' num2str(ang_wave)])
f_theta=0   % if value = -1000, there is something wrong
return
