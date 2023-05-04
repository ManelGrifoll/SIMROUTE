  function alfa=compass2cart(degN)
idx=find(degN>=0 & degN<90);
alfa(idx,1) = abs(degN(idx) - 90);
idx = find(degN>=90&degN<=360);
alfa(idx,1) = abs(450 - degN(idx));
return