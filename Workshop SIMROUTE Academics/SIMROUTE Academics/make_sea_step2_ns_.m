

% first run de previous and zoom the zone desired to make sea
% afterwards, run this program.

% The sequence is from bottom left to top right
% the result is the start with sifix _m


%%%%%%%%%%%%%%%%%%%% start user zone
arx_in='in/waves_20200825';

%%%% end user

arx_mod=[arx_in '_m']

a=ginput(2);
%a=[15.421401639992617 37.809438517863900;15.633387823977640 38.377217207423310];


hh=hs(:,1); %used to find where the NaNs start
N1=search_nods(a(1,1),a(1,2));
N2=search_nods(a(2,1),a(2,2));
[x1,y1]=nod2xy(N1,Nx);
[x2,y2]=nod2xy(N2,Nx);
% make it vertically, it is where data is.
% For each vertical column, start from bottom to top
% downn and its downvalue check where the NanNs start
% the upn and the upvalue check where the NaNs end

for i=0:x2-x1
    
  n=N1+i;
  downvalue=hh(n); 
  if isnan(downvalue)
    disp('Error the limits of the new sea must be at N and S')
    return
  end
  for k=0:y2-y1
      if ~isnan(hh(n+k*Nx))
          downvalue=hh(n+k*Nx);
          downn=n+k*Nx;
      else
         break
      end
  end
  if isnan(hh(n+Nx*(y2-y1)))
    disp('Error the limits of the new sea must be at N and S')
    return
  end  
  for k=y2-y1:-1:0
      if ~isnan(hh(n+k*Nx))
          %upvalue=hh(n+k*Nx);
          upn=n+k*Nx;
      else
         break
      end
  end
   
 clear downvalue upvalue
  %make hs
  downvalue=hs(downn,:);
  upvalue=hs(upn,:);
  nn=(upn-downn)/Nx;
  xx=(upvalue-downvalue)/nn;
  for t=1:n_time
    for i=downn+Nx:Nx:upn-Nx
      hs(i,t)=hs(i-Nx,t)+xx(t);
    end
  end
%     %make dir

  clear downvalue upvalue
  downvalue=dir(downn,:);
 downvalue=compass2cart(downvalue);
  upvalue=dir(upn,:);
 upvalue=compass2cart(upvalue);
  nn=(upn-downn)/Nx;
  xx=(upvalue-downvalue)/nn;
  for t=1:n_time
    for i=downn+Nx:Nx:upn-Nx
      dir(i,t)=cart2compass(cart2compass(dir(i-Nx,t))+xx(t));
    end
  end
%  %make fp
  clear downvalue upvalue
  downvalue=fp(downn,:);
  upvalue=fp(upn,:);
  nn=(upn-downn)/Nx;
  xx=(upvalue-downvalue)/nn;
  for t=1:n_time
    for i=downn+Nx:Nx:upn-Nx
      fp(i,t)=fp(i-Nx,t)+xx(t);
    end
  end


  
end

save (arx_mod,'hs','dir','fp','ARX','Tini_trip')
disp('Fet')