

% first run de previous and zoom the zone desired to make sea
% afterwards, run this program.

%The sequence is from bottom left to top right
% the result is the start with sifix _m


%%%%%%%%%%%%%%%%%%%% start user zone
arx_in='in/waves_20200825';

%%%% end user

arx_mod=[arx_in '_m']

a=ginput(2)
%a=[8.907067305838655 41.209151306653204;9.624207996504260 41.333330703194044];

hh=hs(:,1);
N1=search_nods(a(1,1),a(1,2));
N2=search_nods(a(2,1),a(2,2));
[x1,y1]=nod2xy(N1,Nx);
[x2,y2]=nod2xy(N2,Nx);
for j=0:y2-y1
    
  n=N1+j*Nx;
  leftvalue=hh(n); 
  if isnan(leftvalue)
    disp('Error the limits of the new sea must be sea')
    return
  end
  for i=0:x2-x1
      if ~isnan(hh(n+i))
          leftvalue=hh(n+i);
          leftn=n+i;
      else
         break
      end
  end
  if isnan(hh(n+(x2-x1)))
    disp('Error the limits of the new sea must be sea to E and W')
    return
  end  
  for i=x2-x1:-1:0
      if ~isnan(hh(n+i))
          rigthn=n+i;
      else
         break
      end
  end
  %make hs
  clear downvalue upvalue
  %make hs
  leftvalue=hs(leftn,:);
  rigthvalue=hs(rigthn,:);
  nn=(rigthn-leftn);
  xx=(rigthvalue-leftvalue)/nn;
  for t=1:n_time
    for i=leftn+1:rigthn-1
      hs(i,t)=hs(i-1,t)+xx(t);
    end
  end
  
   %make dir
  leftvalue=dir(leftn,:);
  leftvalue=compass2cart(leftvalue);
  rigthvalue=dir(rigthn,:);
  rigthvalue=compass2cart(rigthvalue);
  nn=(rigthn-leftn);
  xx=(rigthvalue-leftvalue)/nn;
  for t=1:n_time
    for i=leftn+1:rigthn-1
      dir(i,t)=cart2compass(cart2compass(dir(i-1,t))+xx(t));
    end
  end
  %make fp
  clear downvalue upvalue
  %make hs
  leftvalue=fp(leftn,:);
  rigthvalue=fp(rigthn,:);
  nn=(rigthn-leftn);
  xx=(rigthvalue-leftvalue)/nn;
  for t=1:n_time
    for i=leftn+1:rigthn-1
      fp(i,t)=fp(i-1,t)+xx(t);
    end
  end
  
  
 
  
end

save (arx_mod,'hs','dir','fp','ARX','Tini_trip')
disp('Done make_sea_step2_ew')