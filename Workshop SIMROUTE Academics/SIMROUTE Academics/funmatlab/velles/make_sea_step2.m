

% correm primer el previ i Fem un zoom de la zona que vulguem
% fer mar i despres corren aquest programa.

%El sentit es de baix a l'esquerra a dalt a la dreta.
% el resultat es l inici amb sifix _m


%%%%%%%%%%%%%%%%%%%% inici zona usuari
arx_in='in/waves_20161120_20161122';

%%%% end user

arx_mod=[arx_in '_m']

a=ginput(2)

hh=hs(:,1);
N1=search_nods(a(1,1),a(1,2));
N2=search_nods(a(2,1),a(2,2));
[x1,y1]=nod2xy(N1,Nx);
[x2,y2]=nod2xy(N2,Nx);
for j=0:y2-y1
    
  n=N1+j*Nx;
  leftvalue=hh(n); 
  if isnan(leftvalue)
    disp('Error els limits del nou sea han de ser sea')
    return
  end
  n=n+1;
  leftn=n;
  while ~isnan(hh(n))     
    leftvalue=hh(n);
    leftn=n;
    n=n+1;
  end
  while isnan(hh(n)) 
    n=n+1;
  end
 
  rightn=n;
  %%%%%%%% per cada variable:
  clear rightvalue leftvalue
  %fem hs
  rightvalue=hs(rightn,:);
  leftvalue=hs(leftn,:);
  xx=(rightvalue-leftvalue)/(rightn-leftn);
  for t=1:n_time
    for i=leftn+1:rightn-1
      hs(i,t)=hs(i-1,t)+xx(t);
    end
  end
    %fem dir
  rightvalue=dir(rightn,:);
  leftvalue=dir(leftn,:);
  xx=(rightvalue-leftvalue)/(rightn-leftn);
  for t=1:n_time
    for i=leftn+1:rightn-1
      dir(i,t)=dir(i-1,t)+xx(t);
    end
  end
 %fem fp
  rightvalue=fp(rightn,:);
  leftvalue=fp(leftn,:);
  xx=(rightvalue-leftvalue)/(rightn-leftn);
  for t=1:n_time
    for i=leftn+1:rightn-1
      fp(i,t)=fp(i-1,t)+xx(t);
    end
  end  
  
end

save (arx_mod,'hs','dir','fp','ARX','Tini_trip')
disp('Fet')