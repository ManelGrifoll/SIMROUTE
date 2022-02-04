#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 23:10:59 2020
Code part of SIMROUTE (UPC-BarcelonaTech)
version 31/01/2021
@author: manel grifoll (UPC-BarcelonaTech)
"""

from  params import *
from func_simroute_ice import *
import matplotlib.pyplot as plt
import numpy as np
import sys
#from mpl_toolkits.basemap import Basemap

storeddatapath = 'C:/Users/polbl/OneDrive/Documents/SIMROUTE/storeWaves/'
ARX = os.listdir(storeddatapath)

tic()
mxcost=0  
mxdks=0  
if np.isnan(hs[nodIni,0]):
    print('The nodIni is land')
    sys.exit()

if np.isnan(hs[nodEnd,1]):
    print('The nodEnd is land')
    sys.exit()

flag= testVrtx(nodIni)   
if flag is  False:
    print('The nodIni is in vertex move!')
    sys.exit()

flag= testVrtx(nodEnd)   
if flag is  False:
    print('The nodEnd is in vertex move!')
    sys.exit()   

    
'''   setled=np.zeros(shape=(Ny*Nx,4))
       settled each row gives information about the node corresponding to
       n. of row
       the variable is initialized to zero
       col 0  =  if there is a 1, it means that the node is closed
       col 1 the second column gives the cost at which it has closed
       col 2   the third column is the father node, 
       col 3  for the evaluation function
       min_c=np.ones(shape=(Nx*Ny,3))*np.inf
       min_c each row keeps information about the nodes, initialized at Inf
       col 0   the cost of the open node, because when a node is closed, it is 
           put at inf 
       col 1   is the father (when the node is closed, it is left at inf)
       col 2   for the evaluation function
       here the algorithm searches the optimum route at constant speed V0 , 
       en dos casos,1 ,sense  tenin present el onatge 
       i 0 , tenin present onatge
             
 ''' 
 ##
''' 
     Fem primer 
     dos casos diferents i=0 ,i=1
     i=0  Cas que la velocitat del vaixell es veu alterada per 
     la longitud i direccio d'ona  i=1  La velocitat del vaixell es v0 constant
'''
Ldebug=[]
print('Working very hard....!')
for i in range(2):           
    setled=np.zeros(shape=(Ny*Nx,4))
    min_c=np.ones(shape=(Nx*Ny,3))*np.inf
    pidx=nodIni
    min_c[pidx,0]=0
    min_c[pidx,2]=np.nan
    if i==0:
        print('Init trip with waves')
    else:
        print('Init trip without waves')
    '''
        pidx node to close, the first time it is the initial one, 
        it will finish when it closes the end
    '''    
    while (pidx != nodEnd) :   
        setled[pidx,0]=1   # it closes the node to expland 
        setled[pidx,1]=min_c[pidx,0];
        setled[pidx,2]=min_c[pidx,1]; 
#        print('pidx =  {}  {} {}\n'.format( pidx,i,i))
        min_c[pidx,2]=np.inf   # it is inutilized to min
        min_c[pidx,0]=np.inf 
        neighbor_ids=veins(pidx)   # expanding list of neighbors
        for cidx in neighbor_ids:
            if setled[cidx,0]==0:   # if node is open, it works; if it is closed, nothing is done 
                if (not np.isnan(hs[cidx,1])):
                    if i==0:
                        g=time_edge(v0,pidx,cidx,setled[pidx,1])    # accumulated time to pass the edge
                        if mxcost<setled[pidx,1] :
                            mxcost=setled[pidx,1]
                            print("Max. sailing time (in hours) = ",mxcost)
                    else:
                        g=dist_nods(pidx,cidx)/v0+setled[pidx,1]
                        if mxdks<setled[pidx,1] :
                            mxdks=setled[pidx,1]
                            print("Max. sailing time without waves (in hours) = ",mxdks) 
                        
                    heu=dist_nods(cidx,nodEnd)/v0   # heuristic time from the node to the end node
                    if (heu+g)<min_c[cidx,2]:
                            min_c[cidx,0]=g
                            min_c[cidx,1]=pidx
                            min_c[cidx,2]=heu+g
                            
        pidx=int(np.where(min_c[:,2]==np.nanmin(min_c[:,2]))[0][0])
        
        if pidx==nodEnd:
            setled[pidx,0]=1
            setled[pidx,1]=min_c[pidx,0]
            setled[pidx,2]=min_c[pidx,1]
            
        #print('node: ',pidx)

    #'Finished, reconstructs the path from settled'while nod_p ~=nod_ini
    L_t=[]
    L_c=[]   # LLista amb els costos columna 1 del setled
    nod_p =nodEnd   
    ''' comencem pel ultim node i anem mirant els pares de cada node fins 
        anar al nodIni
    '''
    L_t.append(nodEnd)
    L_c.append(setled[nodEnd,1])
    while (nod_p != nodIni) :
        nod=int(setled[int(nod_p),2])
        cos=setled[int(nod),1]
        L_t.append(nod)
        L_c.append(cos)
        nod_p=nod
    if i==0:  
        L_Trip=L_t[::-1]
        Cost_Opt=L_c[::-1]
        CostWave=setled[nodEnd,1]
    else:
        L_TripFix=L_t[::-1]
        CostConst=setled[nodEnd,1]
        L_ConsCostTrip=L_c[::-1]
        
#Calcul de les milles fetes
n=len(L_Trip)
distWave=0
for i in range(n-1):
    distWave=distWave+dist_nods(L_Trip[i],L_Trip[i+1])
n=len(L_TripFix)
distConst=0
for i in range(n-1):
    distConst=distConst+dist_nods(L_TripFix[i],L_TripFix[i+1])
''' Tercera part de la simulacio:
    Considerem que un vaixell va per la ruta que hem dit constant
    pero tenin en compte la velocitat si es afectada pel onatge
    En direm ruta ctw
'''   
CostCtw=0
Cost_Min=[]
Cost_Min.append(CostCtw)
for i in range(len(L_TripFix)-1):   
    CostCtw=time_edge(v0,L_TripFix[i],L_TripFix[i+1],CostCtw)
    Cost_Min.append(CostCtw)

#dat=np.load(lcd_out)
#ldc=dat['arr_0']
#grabarem les sortides
report='out/'+name_Simu+'_Res.txt'
frep=open(report,'w')
st='              SIMROUTE report:     '+name_Simu+'\n'
frep.write(st)
st='=========================================================================\n\n'
frep.write(st)
st= 'Initial Velocity in knots = {} \n'.format(v0)
frep.write(st)
print(st)
st='WEN_form = {:d} \n'.format(WEN_form)
print(st)
frep.write(st)

st='Departure:  Node = {:6d}  --  coordinates  ({:6.4f},{:6.4f})\n'
frep.write(st.format(nodIni,nodes[nodIni,0],nodes[nodIni,1]))
print(st.format(nodIni,nodes[nodIni,0],nodes[nodIni,1]))
s=ARX[0]
k=s.find('_',s.find('_')+1)
Syear=s[k+1:k+5]
Smon=s[k+5:k+7]
Sdia=s[k+7:k+9]
Shora=str(t_ini)
dat=Sdia+'-'+Smon+'-'+Syear+' '+Shora+':00'
st='Departure time (day-month-year hour:min): '+dat+'\n'
del k , s , Syear, Sdia, Shora, Smon
frep.write(st)
print(st)
st='Arrival:     Node = {:6d}  --  coordinates  ({:6.4f},{:6.4f})\n'
frep.write(st.format(nodEnd,nodes[nodEnd,0],nodes[nodEnd,1]))
print(st.format(nodEnd,nodes[nodEnd,0],nodes[nodEnd,1]))
st='Number of nodes: Nx={:6d}   Ny={:6d}   Nx*Ny={:6d}   \n'
print(st.format(Nx,Ny,Nx*Ny))
frep.write(st.format(Nx,Ny,Nx*Ny))
st='Geodetic Distance (in milles): {:6.2f}\n '
frep.write(st.format(dist_nods(nodIni,nodEnd)))
st='\n========================================================================\n'
frep.write(st)
print(st)
st='                                        Sailed hours    Sailed milles\n'
frep.write(st)
print(st)
st='Route Optimized:                          {:6.2f}            {:6.2f}    \n'
frep.write(st.format(Cost_Opt[-1],distWave))
print(st.format(Cost_Opt[-1],distWave))
st='Route Minimum Distance:                  {:6.2f}            {:6.2f}    \n'
print(st.format(Cost_Min[-1],distConst))
frep.write(st.format(Cost_Min[-1],distConst))
st='Route Minimum Distance (without waves):   {:6.2f}            {:6.2f}    \n'
print(st.format(CostConst,distConst))
frep.write(st.format(CostConst,distConst))
st='\n========================================================================\n\n'
'''  ara gravem resultats posem com nom
'''
print('-------------- SIMROUTE DONE ---------------------')
print('-------------- Saving results in 3 files...')
print ('File simulation results created: ' + report )

prs = np.array([LonMin,LonMax,LatMin,LatMax,v0,inc,nodIni,nodEnd,t_ini,
                time_res,WEN_form,Lbp,DWT])
np.savez_compressed('out/'+name_Simu,prs,hs,fp,dir,th,af,L_Trip,L_TripFix,
                    Cost_Opt,L_ConsCostTrip,Cost_Min,ARX)
######################
frep.write(st)
frep.close()
print ('File .npz results created: ' + 'out/'+name_Simu+'.npz')


nom_reco=name_Simu+'_MetaData.txt'
reco=open('out/'+nom_reco,'w')
st='name_Simu = \''+name_Simu+'\'\n'
reco.write(st)
st='LonMin = {:6.3f} \n'
reco.write(st.format(LonMin))
st='LonMax = {:6.3f} \n'
reco.write(st.format(LonMax))
st='LatMin = {:6.3f} \n'
reco.write(st.format(LatMin))
st='LatMax = {:6.3f} \n'
reco.write(st.format(LatMax))
st='inc = {:6.3f} \n'
reco.write(st.format(inc))
st='nodIni = {:d} \n'
reco.write(st.format(nodIni))
st='nodEnd = {:d} \n'
reco.write(st.format(nodEnd))
reco.write('ARX = [')
for a in ARX:
    reco.write('\''+str(a)+'\' , ')
reco.write(' ] \n')
reco.write('dir_arx = \'storeWaves/\'\n')
st='time_res = {:d} \n'
reco.write(st.format(time_res))
st='t_ini = {:d} \n'
reco.write(st.format(t_ini))
st='v0 = {:6.3f} \n'
reco.write(st.format(v0))
st='WEN_form = {:d} \n'
reco.write(st.format(WEN_form))
st='Lbp = {:d} \n'
reco.write(st.format(int(Lbp)))
st='DWT = {:d} \n'
reco.write(st.format(int(DWT)))
reco.close()
print ('File simulation metadata created: ' + nom_reco)

report='out/'+name_Simu+'_Route.txt'
frout=open(report,'w')
st='  nnod     Lon    Lat      Cost    hs      dir    SIT      SIC   \n'
frout.write(st)
for i in range(len(L_Trip)):
    n=L_Trip[i]
    lonn=nodes[n,0]
    latt=nodes[n,1]
    if time_res==3:
        ccost= Cost_Opt[i]/3  
    else:    
        ccost=Cost_Opt[i]    
    hh=hs[n,int(np.round(ccost))]
    dirr=dir[n,int(np.round(ccost))]
    thhh=th[n,int(np.round(ccost))]
    afff=af[n,int(np.round(ccost))]
    st='{:7d} {:8.3f} {:7.3f} {:7.3f} {:5.2f} {:6.2f} {:6.2f} {:6.2f} \n'.format(n,lonn,latt,ccost,hh,dirr,thhh,afff)
    frout.write(st)
frout.close()


print ('File simulation route created')
toc()
if plot_routes==1:
    plt.figure(1)
    plt.title( name_Simu) #+ ' make_plot temps = {}'.format(i))
    plt.xlim([LonMin, LonMax])
    plt.ylim([LatMin, LatMax])
   
    lont=nodes[L_Trip[:],0]
    latt=nodes[L_Trip[:],1] 
    
    lonc=nodes[L_TripFix[:],0]
    latc=nodes[L_TripFix[:],1]
    
    plt.plot(lonc,latc,linewidth=1.5,color='orange')
    plt.plot(lont,latt,'m-')
    plt.legend(('Minimum Distance','Optimized'),loc='best')
    #Re-build Mesh:
    inc=inc/60    
    Nx=int(np.floor((LonMax-LonMin)/inc)+2)
    Ny=int(np.floor((LatMax-LatMin)/inc)+2)
    tira_lon=[]
    for i in range(Nx):
        tira_lon.append(LonMin+i*inc)
    tira_lat=[]
    for j in range(Ny):  
        tira_lat.append(LatMin+j*inc)
    nodes=np.zeros((Nx*Ny,2))
    for j in range(Ny):   
        for i in range(Nx):
            nodes[Nx*j +i,0]=tira_lon[i]
            nodes[Nx*j +i,1]=tira_lat[j]
    inc=inc*60
    Xnod, Ynod = np.meshgrid(tira_lon,tira_lat)
    hs_rec=np.zeros(shape=Xnod.shape)
    dir_rec=np.copy(hs_rec)
    t=6
    for j in range(Ny):
        for i in range(Nx):
              hs_rec[j,i]=hs[:,t][i+Nx*j]
              dir_rec[j,i]=dir[:,t][i+Nx*j]
    plt.pcolor(Xnod,Ynod,hs_rec)
    vmax=np.nanmax(hs)
    plt.clim(0,vmax)
    plt.colorbar()
    plt.show()
