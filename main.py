from  params import *
#from  func_namoa import *
from  mod_veins import *
from modsim import *
#from load_waves import *
import matplotlib.pyplot as plt
import numpy as np
import sys
if np.isnan(hs[nodIni,0]):
    print('The nodIni is land')
    sys.exit()
if np.isnan(hs[nodEnd,1]):
    print('The nodEnd is land')
    sys.exit()
 #       settled each row gives information about the node corresponding to
 #       n. of row
 #       the variable is initialized to zero
 #       col 0  =  if there is a 1, it means that the node is closed
 #       col 1 the second column gives the cost at which it has closed
 #       col 2   the third column is the father node, 
 #       col 3  for the evaluation function

setled=np.zeros(shape=(Ny*Nx,4))

#     min_c each row keeps information about the nodes, initialized at Inf
#     col 0   the cost of the open node, because when a node is closed, it is put at inf 
#     col 1   is the father (when the node is closed, it is left at inf)
#     col 2   for the evaluation function

min_c=np.ones(shape=(Nx*Ny,3))*np.inf

 # here the algorithm searches the optimum route at constant speed (it doesn't depend on it)
pidx=nodIni
min_c[pidx,0]=0;
min_c[pidx,2]=np.nan

while (pidx != nodEnd) :   #pidx node to close, the first time it is the initial one, it will finish when it closes the end
    setled[pidx,0]=1   # it closes the node to expland 
    setled[pidx,1]=min_c[pidx,0];
    setled[pidx,2]=min_c[pidx,1]; 
  #  print('pidx =  {} \n'.format( pidx))
    min_c[pidx,2]=np.inf   # it is inutilized to min
    min_c[pidx,0]=np.inf 
    neighbor_ids=veins(pidx)   # expanding list of neighbors
    for cidx in neighbor_ids:
        if setled[cidx,0]==0:   # if node is open, it works; if it is closed, nothing is done 
            if (not np.isnan(hs[cidx,1])):
                g=time_edge(v0,pidx,cidx,setled[pidx,1])    # accumulated time to pass the edge
                heu=dist_nods(cidx,nodEnd)/v0   # heuristic time from the node to the end node
                if (heu+g)<min_c[cidx,2]:
                        min_c[cidx,0]=g
                        min_c[cidx,1]=pidx
                        min_c[cidx,2]=heu+g
    pidx=int(np.where(min_c[:,2]==np.nanmin(min_c[:,2]))[0])
    if pidx==nodEnd:
        setled[pidx,0]=1
        setled[pidx,1]=min_c[pidx,0]
        setled[pidx,2]=min_c[pidx,1]

#'Finished, reconstructs the path from settled'while nod_p ~=nod_ini
L_trip=[]
L_t=[]
nod_p =nodEnd  # comencem pel ultim node i anem mirant els pares de cada node fins anar al nosIni
print(' nodIni = {}     nodEnd= {} \n'.format(nodIni,nodEnd))
L_t.append(nodEnd)
while (nod_p != nodIni) :
    nod=int(setled[int(nod_p),2])
    L_t.append(nod)
    nod_p=nod
L_trip=L_t[::-1]