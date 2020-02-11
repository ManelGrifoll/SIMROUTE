from  params import *
from  mod_veins import *
from modsim import *
import matplotlib.pyplot as plt
import numpy as np
import sys
if np.isnan(hs[nodIni,0]):
    print('The nodIni is land')
    sys.exit()
if np.isnan(hs[nodEnd,1]):
    print('The nodEnd is land')
    sys.exit()
 #   setled=np.zeros(shape=(Ny*Nx,4))
 #       settled each row gives information about the node corresponding to
 #       n. of row
 #       the variable is initialized to zero
 #       col 0  =  if there is a 1, it means that the node is closed
 #       col 1 the second column gives the cost at which it has closed
 #       col 2   the third column is the father node, 
 #       col 3  for the evaluation function
#   min_c=np.ones(shape=(Nx*Ny,3))*np.inf
#        min_c each row keeps information about the nodes, initialized at Inf
#        col 0   the cost of the open node, because when a node is closed, it is put at inf 
#        col 1   is the father (when the node is closed, it is left at inf)
#        col 2   for the evaluation function
 # here the algorithm searches the optimum route at constant speed V0 , en dos casos,1 ,sense  tenin present el onatge 
  # i 0 , tenin present onatge 
  
for i in range(2): 
    setled=np.zeros(shape=(Ny*Nx,4))
    min_c=np.ones(shape=(Nx*Ny,3))*np.inf
    pidx=nodIni
    min_c[pidx,0]=0;
    min_c[pidx,2]=np.nan
        
    while (pidx != nodEnd) :   #pidx node to close, the first time it is the initial one, it will finish when it closes the end
        setled[pidx,0]=1   # it closes the node to expland 
        setled[pidx,1]=min_c[pidx,0];
        setled[pidx,2]=min_c[pidx,1]; 
        #print('pidx =  {}  {} {}\n'.format( pidx,i,i))
        min_c[pidx,2]=np.inf   # it is inutilized to min
        min_c[pidx,0]=np.inf 
        neighbor_ids=veins(pidx)   # expanding list of neighbors
        for cidx in neighbor_ids:
            if setled[cidx,0]==0:   # if node is open, it works; if it is closed, nothing is done 
                if (not np.isnan(hs[cidx,1])):
                    if i==0:
                        g=time_edge(v0,pidx,cidx,setled[pidx,1])    # accumulated time to pass the edge
                    else:
                        g=dist_nods(pidx,cidx)/v0+setled[pidx,1]
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
    L_t=[]
    
    nod_p =nodEnd  # comencem pel ultim node i anem mirant els pares de cada node fins anar al nosIni
    #print(' nodIni = {}     nodEnd= {} \n'.format(nodIni,nodEnd))
    
    L_t.append(nodEnd)
    while (nod_p != nodIni) :
        nod=int(setled[int(nod_p),2])
        L_t.append(nod)
        nod_p=nod
    if i==0:  
        L_trip=L_t[::-1]
        CostWave=setled[nodEnd,1]
    else:
        L_tripConst=L_t[::-1]
        CostConst=setled[nodEnd,1]
#Calcul de les milles fetes
n=len(L_trip)
distWave=0
for i in range(n-1):
    distWave=distWave+dist_nods(L_trip[i],L_trip[i+1])
n=len(L_tripConst)
distConst=0
for i in range(n-1):
    distConst=distConst+dist_nods(L_tripConst[i],L_tripConst[i+1])
    
#grabarem les sortides
report='out/report_'+nomSim+'.txt'
frep=open(report,'w')
st='                     '+nomSim+'\n'
frep.write(st)
st='===========================================================================\n'
frep.write(st)
st= 'Velociat en m/h = {} \n'.format(v0)
frep.write(st)
st='Punt de Inici:  Node = {:6d}  --  coordenades  ({:6.4f},{:6.4f})\n'.format(nodIni,nodes[nodIni,0],nodes[nodIni,1])
frep.write(st)
st='Punt Final:     Node = {:6d}  --  coordenades  ({:6.4f},{:6.4f})\n'.format(nodEnd,nodes[nodEnd,0],nodes[nodEnd,1])
frep.write(st)
st='===========================================================================\n'
frep.write(st)
st='                          hores  invertides                  milles navegades\n'
frep.write(st)
st='Condiderant onatge:             {:6.2f}                            {:6.2f}    \n'.format(CostWave,distWave)
frep.write(st)
st='Velocitat constant:             {:6.2f}                            {:6.2f}    \n'.format(CostConst,distConst)
frep.write(st)
st='\n\n===========================================================================\n\n'
frep.write(st)
frep.close()
dat=np.load(arx_ldc)
ldc=dat['arr_0']
plt.figure(1)
#plt.
plt.plot(ldc[:,0],ldc[:,1],'-')

plt.title(' make_plot temps = {}'.format(i))
lont=nodes[L_trip[:],0]
latt=nodes[L_trip[:],1]
plt.plot(lont,latt,'r*')
lonc=nodes[L_tripConst[:],0]
latc=nodes[L_tripConst[:],1]
plt.plot(lonc,latc,'k-')