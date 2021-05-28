#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 23:10:59 2020
Versio 31-01-2921  # afegida funcio testVrtx
Versió 29-01-2021
@author: manel grifoll (UPC-BarcelonaTech)
"""


import numpy  as np
from  params import *
import math as math
import re
import os
# treure ldc 
################### Fem el mesh primer de tot
inc=inc/60.0    # in deg
Nx=int(np.floor((LonMax-LonMin)/inc)+2)
Ny=int(np.floor((LatMax-LatMin)/inc)+2)
tira_lon=[]
for i in range(Nx):
    tira_lon.append(LonMin+i*inc)
tira_lat=[]
for j in range(Ny):  
    tira_lat.append(LatMin+j*inc)

nodes=np.zeros((Nx*Ny,2))
#print( ' Nx = {:6d} ---   Ny = {:4d}\n'.format(Nx,Ny))
#print('longituds    {:8.3f}    -----   {:8.3f} \n'.format(tira_lon[0],tira_lon[-1]))
#print('latituds     {:8.3f}    -----   {:8.3f} \n'.format(tira_lat[0],tira_lat[-1]))
for j in range(Ny):   
    for i in range(Nx):
        nodes[Nx*j +i,0]=tira_lon[i]
        nodes[Nx*j +i,1]=tira_lat[j]
inc=inc*60
LatMaxEfec=nodes[Nx*Ny-1,1]
LonMaxEfec=nodes[Nx-1,0]

# si tenim el onatge el posem, si no, no el carreguem                        
if os.path.exists(arx_waves):                        
    if t_ini==0:
        dat=np.load(arx_waves)
        hs=dat['arr_0']
        fp=dat['arr_1']
       
        dir=dat['arr_2']      
    else:
        dat=np.load(arx_waves)
        hs1=dat['arr_0']
        fp1=dat['arr_1']
        dir1=dat['arr_2']
        if time_res==1:   
            tt=range(0,t_ini)
        else:
            tt=range(0,int(t_ini/3))
            
        hs=np.delete(hs1,tt,axis=1)
        del hs1
        fp=np.delete(fp1,tt,axis=1)
        del fp1
        dir=np.delete(dir1,tt,axis=1)
        del dir1



################################3
def cart2compass(deg):
   #Function that converts cartesian angles to compass angles arg <=360
   if np.isnan(deg):
       return np.nan
   degN=90 - deg
   if ( degN) <0:
      return degN+360
   else:
      return degN
 
def compass2cart(degN):
  if np.isnan(degN):
      return np.nan
  if degN>=0 and degN<=90:
      return np.abs(degN - 90)
  if degN>90 and degN<=360:
     return  np.abs(450 - degN)

   
def arrayRect2Comp(Ax,Ay):
   d=Ax.shape
   Az=np.zeros(shape=d)
   for i in range(d[1]):
      for j in range(d[0]):
         zeta=np.complex(Ax[j,i],Ay[j,i])
         an=cart2compass(np.angle(zeta,deg=True))
         Az[j,i]=an              
   return Az     

def arrayComp2Cart(Ax):
   d=Ax.shape
   Az=np.zeros(shape=d)
   for i in range(d[0]):
      for j in range(d[1]):
         Az[i,j]=compass2cart(Ax[i,j])
   return Az
  
def tic():
   #Homemade version of matlab tic and toc functions
   import time
   global startTime_for_tictoc
   startTime_for_tictoc = time.time()

def toc():
   import time
   if 'startTime_for_tictoc' in globals():
      print ('Elapsed time is  {}  seconds.'.format( (time.time() - startTime_for_tictoc)))
   else:
      print ("Toc: start time not set")
# diuen que es un invent https://gist.github.com/jeromer/2005586

def dir2dir(dir1,dir2,n):
   # passar de dir 1 a dir2 amb npassos compass a commpass
   #N son els nds interiors, o sigui:  rightn-leftn -1
   # el leftn i rihtn no surtiran al resultat
   #Tambe s'utilitza per fer el sud nort
   x1=np.cos(np.deg2rad(compass2cart(dir1)))
   y1=np.sin(np.deg2rad(compass2cart(dir1)))
   x2=np.cos(np.deg2rad(compass2cart(dir2)))
   y2=np.sin(np.deg2rad(compass2cart(dir2))) 
   dx=(x2-x1)/(n+1)
   dy=(y2-y1)/(n+1)
   out=np.zeros(n)
   for i in range(1,n+1):
      zeta=np.complex(x1+dx*i,y1+dy*i)
      out[i-1]=cart2compass(np.angle(zeta,deg=True))
   return
def dist_nods(N1,N2):
  
   lon1=nodes[N1,0]
   lat1=nodes[N1,1]
   lon2=nodes[N2,0]
   lat2=nodes[N2,1]
   d=60*np.rad2deg((np.arccos(np.sin(np.deg2rad(lat1))*np.sin(np.deg2rad(lat2))+np.cos(np.deg2rad(lat1))*np.cos(np.deg2rad(lat2))*np.cos(np.deg2rad(lon1-lon2)))));
   return d

def veloc(v0,nod_i,nod_f,cost_i):
   """
       v0  velocitat de creuer
       nod_ini node inicial del edge
       nod_f  node final del tram 
       cost_i  per escollir el time del onatage 
       Consulteu np.divmod(cost,time_res)
       dona la i del onatge que actuara i el temps que queda
       per entrar una nova dade de ona       """
   ang_ship=ang_edge(nod_f,nod_i)
   if time_res==1: 
       iv=math.floor(cost_i)+1
       hm=0.5*(hs[nod_i,iv]+hs[nod_f,iv])
       angEnc=ang_encounter(ang_ship,dir[nod_f,iv])
   elif time_res==3:
#       print(nod_i,nod_f,cost_i)
       iv,a=np.divmod(cost_i,time_res)
       iv=int(iv)
  #     print(nod_i)
       hm=0.5*(hs[nod_i,iv]+hs[nod_f,iv])
       angEnc=ang_encounter(ang_ship,dir[nod_f,iv])
#       print("veloc  ", hm   )
     #  hm=hs[nod_i,iv]+(hs[nod_i,iv+1]-hs[nod_i,iv])*a/time_res
       # sembla que no cal fer la mitjana entre nodes 
 #      hm2=hs[nod_f,iv]+(hs[nod_f,iv+1]-hs[nod_f,iv])*a/time_res
 #      hm=0.5*(hm1+hm2)
       
   
   
   if WEN_form==1:
       vel=v0-reduc_v_bow(angEnc)*hm*hm*3.2808*3.2808 #transform meters to feets
   elif WEN_form==2:
       vel=v0-reduc_v_arte(angEnc,hm,Lbp,v0)
   elif WEN_form==3:
       vel=v0-reduc_v_khok(angEnc,hm)*(1 - 1.35e-6*DWT*v0)
#
   else:
       vel=v0
   if vel<0:
      print('Negative Ship speed. Use other Wave Effect on Navigation formulation.') 
      print(vel,angEnc,ang_ship,nod_i,nod_f,hm,cost_i )
      raise SystemExit

   return vel

def ang_edge(n_desti,n_ori):
#   x=nodes[n_desti,0]-nodes[n_ori,0];
#   y=nodes[n_desti,1]-nodes[n_ori,1];
#   at=math.atan2(y,x);
#   alfa =cart2compass(np.rad2deg(at));
#   return alfa
    loni , lati = nodes[n_ori,0],nodes[n_ori,1]
    lone , late = nodes[n_desti,0],nodes[n_desti,1]    
    if lati==late:
        if loni >lone:
            return 270
        else:
            return 90     
#    lati=lati+0.00001    
    k=dist_arc(loni,lati,lone,late)
    cosI=(np.cos(np.deg2rad(90-late))- np.cos(k)*
          np.cos(np.deg2rad(90-lati))) /((np.sin(k)) *
          np.sin(np.deg2rad(90-lati)) ) 
    if cosI>1:   # millor if cosI>1 and cosI<1.001:
#        print('cosi 1 ',cosI)
        I=0
    elif cosI<-1:   # cosI<-1 ans cosI>-1.0001
#        print('cosi -1 ', cosI)
        I=np.pi
    else:
        I=np.arccos(cosI)
        
    I=I*180/np.pi
    if loni>lone:
        return  360-I
    else:
        return I
    
    
def dist_arc(loni,lati,lone,late):   #resultat en radiants !!Funcio no utilitzada     
    cosp=(np.cos(np.deg2rad(90-lati))*np.cos(np.deg2rad(90-late)) +
        np.sin(np.deg2rad(90-lati))*np.sin(np.deg2rad(90-late)) * 
        np.cos(np.deg2rad(lone-loni)))    
    return np.arccos(cosp)   #np.arccos(cosp)



def ang_encounter(ang_ship,ang_wave):
    if(ang_wave>ang_ship):
        theta=ang_wave-ang_ship
        return theta
    else:
        theta=360-(ang_ship-ang_wave)
#        print('kkkk',theta)
        return theta

def reduc_v_bow(theta):
   #Bowditch speed penalty (theta angle of encounter)             
   if ((theta>=45 and theta<=135) or (theta>=225 and theta<=315)):
      f_theta=0.0165 # BEAM SEA
      return f_theta
   if (theta>135 and theta<225):
      f_theta=0.0083#FOLLOWING SEA 
      return f_theta

   if ((theta>=0 and theta<45) or(theta>315 and theta<=360)):
      f_theta=0.0248 #HEAD SEA
      return f_theta

   f_theta=0  
   return f_theta

def reduc_v_arte(theta,h,Lb,v):
    #Aertssen speed penalty (theta angle of encounter)
    # theta must be in [0,180] deg
    if (theta > 180 and theta <= 360):
        theta = 360 - theta    
    m=0
    n=0    
    
    if (0 <= h and h < 2.5): 
        m = 0
        n = 0
        
    if (2.5 <= h and h < 4.0):         #referencia aertssen
        if (0 <= theta and theta <= 30): #  head sea 
            m = 900
            n = 2
        if (30 < theta and theta <= 60): #bow sea  (mar de proa)
            m = 700
            n = 2
        if (60 < theta and theta <= 150):  #beam sea  (mar de traves)
            m = 350
            n = 1
        if (150 < theta and theta <= 180): #following sea  (mar de popa)
            m = 100
            n = 0

    if (4.0 <= h and h < 5.5):
        if (0 <= theta and theta <= 30): #  head sea 
            m = 1300
            n = 6
        if (30 < theta and theta <= 60): #bow sea  (mar de proa)
            m = 1000
            n = 5
        if (60 < theta and theta <= 150):  #beam sea  (mar de traves)
            m = 500
            n = 3
        if (150 < theta and theta <= 180): #following sea  (mar de popa)
            m = 200
            n = 1

    if (5.5 <= h and h < 7.5):
        if (0 <= theta and theta <= 30): #  head sea 
            m = 2100
            n = 11
        if (30 < theta and theta <= 60): #bow sea  (mar de proa)
            m = 1400
            n = 8
        if (60 < theta and theta <= 150):  #beam sea  (mar de traves)
            m = 700
            n = 5
        if (150 < theta and theta <= 180): #following sea  (mar de popa)
            m = 400
            n = 2

    if (7.5 <= h):
        if (0 <= theta and theta <= 30): #  head sea 
            m = 3600
            n = 18
        if (30 < theta and theta <= 60): #bow sea  (mar de proa)
            m = 2300
            n = 12
        if (60 < theta and theta <= 150):  #beam sea  (mar de traves)
            m = 1000
            n = 7
        if (150 < theta and theta <= 180): #following sea  (mar de popa)
            m = 700
            n = 3        
    
    
    delta_v = v * (m / Lb + n) / 100
    
    
    return delta_v    

def reduc_v_khok(theta,h):
    #Khoklov speed penalty (theta angle of encounter)
    # theta must be in [0,180] deg
    if (theta > 180 and theta <= 360):
        theta = 360 - theta    
    # 

    #% /!\ Angle in degrees, we need to convert it to radians:
    theta_rad = np.pi/180*theta;
    #print('theta?',theta_rad)
    khokhlov_factor = (0.745 - 0.245*theta_rad)*h;
    
    return khokhlov_factor

def time_edge(v0,n_o,n_e,cost):
   #With a edge length given and knowing the cost (time from start point)
   # and figuring that height and direction are known, acumulated time is 
   # found. It finishes travelling the edge, knowing that
   # THERE IS AN HOURLY SWELL RESOLUTION!!!!!!!!Nonhourly, time_res
   L=dist_nods(n_o,n_e)
   q=1   
   costi=cost
   tau=time_res-np.divmod(costi,time_res)[1]
   while q==1:
      if veloc(v0,n_o,n_e,costi)*tau>=L:   # with tau, remaining time for travelling the edge, it makes it and leaves (q==0)
         costi=costi+L/veloc(v0,n_o,n_e,costi)
 #        print( "Ldirect, veloc = ",L,veloc(v0,n_o,n_e,costi))
 #        print("veloc L ", veloc(v0,n_o,n_e,costi) ) 
         q=0
      else:
  #       print("tau icost L=",tau,costi,L)
         L=L-veloc(v0,n_o,n_e,costi)*tau  #now the edge is shorter
         costi=costi+tau   #cost is actualized
#         print("veloc Lindi ", veloc(v0,n_o,n_e,costi) ) 
         tau=time_res-np.divmod(costi,time_res)[1]           
#         print("tau,icost,L,v=",tau,costi,L,veloc(v0,n_o,n_e,costi))
   return  costi


def veins(N):
  if N >Nx*Ny-1:
      print("error valor  ha de ser mes petita que  ",N)
      
      return False
  y=math.floor(N/Nx) #+1
  x=N%Nx  # numero de fila començant per zero  (hi ha Nx-1 files i Ny-1 columnes)
  #print(x,y)
  if((x>3 and x<Nx-4) and (y>3 and y<Ny-4)):
 
        A =[N+1+Nx, N+1+2*Nx, N+1+3*Nx, N+1+4*Nx, N+2+3*Nx, N+2+Nx, N+3+Nx, N+3+2*Nx, N+3+4*Nx, N+4+Nx, N+4+3*Nx,
            N+1-Nx, N+1-2*Nx, N+1-3*Nx, N+1-4*Nx, N+2-3*Nx, N+2-Nx, N+3-Nx, N+3-2*Nx, N+3-4*Nx, N+4-Nx, N+4-3*Nx,
            N-1+Nx, N-1+2*Nx, N-1+3*Nx, N-1+4*Nx, N-2+3*Nx, N-2+Nx, N-3+Nx, N-3+2*Nx, N-3+4*Nx, N-4+Nx, N-4+3*Nx,
            N-1-Nx, N-1-2*Nx, N-1-3*Nx, N-1-4*Nx, N-2-3*Nx, N-2-Nx, N-3-Nx, N-3-2*Nx, N-3-4*Nx, N-4-Nx, N-4-3*Nx,
            N+1, N-1, N+Nx, N-Nx]

        return A
    
  if (x==0) and (y>3) and (y<Ny-4) :    # marc esquerra pur
        A =[N+1+Nx, N+1+2*Nx,N+1+3*Nx,N+1+4*Nx, N+2+3*Nx, N+2+Nx, N+3+Nx, N+3+2*Nx, N+3+4*Nx, N+4+Nx, N+4+3*Nx,
            N+1-Nx, N+1-2*Nx,N+1-3*Nx,N+1-4*Nx, N+2-3*Nx, N+2-Nx, N+3-Nx, N+3-2*Nx, N+3-4*Nx, N+4-Nx, N+4-3*Nx,
            N+1,  N+Nx, N-Nx]
        return A      
      
  if (x==1) and (y>3) and (y<Ny-4) :
        A =[N+1+Nx, N+1+2*Nx,N+1+3*Nx,N+1+4*Nx, N+2+3*Nx, N+2+Nx, N+3+Nx, N+3+2*Nx, N+3+4*Nx, N+4+Nx, N+4+3*Nx,
            N+1-Nx, N+1-2*Nx,N+1-3*Nx,N+1-4*Nx, N+2-3*Nx, N+2-Nx, N+3-Nx, N+3-2*Nx, N+3-4*Nx, N+4-Nx, N+4-3*Nx,
            N-1+Nx, N-1+2*Nx,N-1+3*Nx,N-1+4*Nx, 
            N-1-Nx, N-1-2*Nx,N-1-3*Nx,N-1-4*Nx, 
            N+1, N-1, N+Nx, N-Nx]
        return A      
      
  if (x==2) and (y>3) and (y<Ny-4) :  
        A =[N+1+Nx, N+1+2*Nx, N+1+3*Nx, N+1+4*Nx, N+2+3*Nx, N+2+Nx, N+3+Nx, N+3+2*Nx, N+3+4*Nx, N+4+Nx, N+4+3*Nx,
            N+1-Nx, N+1-2*Nx, N+1-3*Nx, N+1-4*Nx, N+2-3*Nx, N+2-Nx, N+3-Nx, N+3-2*Nx, N+3-4*Nx, N+4-Nx, N+4-3*Nx,
            N-1+Nx, N-1+2*Nx, N-1+3*Nx, N-1+4*Nx, N-2+3*Nx, N-2+Nx,
            N-1-Nx, N-1-2*Nx, N-1-3*Nx, N-1-4*Nx, N-2-3*Nx, N-2-Nx, 
            N+1, N-1, N+Nx, N-Nx]
        return A
  if (x==3) and (y>3) and (y<Ny-4) : 
         A =[N+1+Nx, N+1+2*Nx, N+1+3*Nx, N+1+4*Nx, N+2+3*Nx, N+2+Nx, N+3+Nx, N+3+2*Nx, N+3+4*Nx, N+4+Nx, N+4+3*Nx,
            N+1-Nx, N+1-2*Nx, N+1-3*Nx, N+1-4*Nx, N+2-3*Nx, N+2-Nx, N+3-Nx, N+3-2*Nx, N+3-4*Nx, N+4-Nx, N+4-3*Nx,
            N-1+Nx, N-1+2*Nx, N-1+3*Nx, N-1+4*Nx, N-2+3*Nx, N-2+Nx, N-3+Nx, N-3+2*Nx, N-3+4*Nx,
            N-1-Nx, N-1-2*Nx, N-1-3*Nx, N-1-4*Nx, N-2-3*Nx, N-2-Nx, N-3-Nx, N-3-2*Nx, N-3-4*Nx, 
            N+1, N-1, N+Nx, N-Nx]   
         return A
  if (x==Nx-1) and  (y>3) and (y<Ny-4) : 
        A =[N-1+Nx, N-1+2*Nx, N-1+3*Nx, N-1+4*Nx, N-2+3*Nx, N-2+Nx, N-3+Nx, N-3+2*Nx, N-3+4*Nx, N-4+Nx, N-4+3*Nx,
            N-1-Nx, N-1-2*Nx, N-1-3*Nx, N-1-4*Nx, N-2-3*Nx, N-2-Nx, N-3-Nx, N-3-2*Nx, N-3-4*Nx, N-4-Nx, N-4-3*Nx,
            N-1, N+Nx, N-Nx]      
        return A
      
  if (x==Nx-2) and  (y>3) and (y<Ny-4) :
         A =[N+1+Nx, N+1+2*Nx, N+1+3*Nx, N+1+4*Nx,
            N+1-Nx, N+1-2*Nx, N+1-3*Nx, N+1-4*Nx,
            N-1+Nx, N-1+2*Nx, N-1+3*Nx, N-1+4*Nx, N-2+3*Nx, N-2+Nx, N-3+Nx, N-3+2*Nx, N-3+4*Nx, N-4+Nx, N-4+3*Nx,
            N-1-Nx, N-1-2*Nx, N-1-3*Nx, N-1-4*Nx, N-2-3*Nx, N-2-Nx, N-3-Nx, N-3-2*Nx, N-3-4*Nx, N-4-Nx, N-4-3*Nx,
            N+1, N-1, N+Nx, N-Nx]

         return A   
    
  if (x==Nx-3) and  (y>3) and (y<Ny-4) :   
         A =[N+1+Nx, N+1+2*Nx, N+1+3*Nx, N+1+4*Nx, N+2+3*Nx, N+2+Nx, 
            N+1-Nx, N+1-2*Nx, N+1-3*Nx, N+1-4*Nx, N+2-3*Nx, N+2-Nx,
            N-1+Nx, N-1+2*Nx, N-1+3*Nx, N-1+4*Nx, N-2+3*Nx, N-2+Nx, N-3+Nx, N-3+2*Nx, N-3+4*Nx, N-4+Nx, N-4+3*Nx,
            N-1-Nx, N-1-2*Nx, N-1-3*Nx, N-1-4*Nx, N-2-3*Nx, N-2-Nx, N-3-Nx, N-3-2*Nx, N-3-4*Nx, N-4-Nx, N-4-3*Nx,
            N+1, N-1, N+Nx, N-Nx]

         return A   
    
  if (x==Nx-4) and  (y>3) and (y<Ny-4) :       
         A =[N+1+Nx, N+1+2*Nx, N+1+3*Nx, N+1+4*Nx, N+2+3*Nx, N+2+Nx, N+3+Nx, N+3+2*Nx, N+3+4*Nx,
            N+1-Nx, N+1-2*Nx, N+1-3*Nx, N+1-4*Nx, N+2-3*Nx, N+2-Nx, N+3-Nx, N+3-2*Nx, N+3-4*Nx, 
            N-1+Nx, N-1+2*Nx, N-1+3*Nx, N-1+4*Nx, N-2+3*Nx, N-2+Nx, N-3+Nx, N-3+2*Nx, N-3+4*Nx, N-4+Nx, N-4+3*Nx,
            N-1-Nx, N-1-2*Nx, N-1-3*Nx, N-1-4*Nx, N-2-3*Nx, N-2-Nx, N-3-Nx, N-3-2*Nx, N-3-4*Nx, N-4-Nx, N-4-3*Nx,
            N+1, N-1, N+Nx, N-Nx]

         return A   
  if (y==0) and (x>3) and (x<Nx-4):   # marc inferior
        A =[N+1+Nx, N+1+2*Nx, N+1+3*Nx, N+1+4*Nx, N+2+3*Nx, N+2+Nx, N+3+Nx, N+3+2*Nx, N+3+4*Nx, N+4+Nx, N+4+3*Nx,
            N-1+Nx, N-1+2*Nx, N-1+3*Nx, N-1+4*Nx, N-2+3*Nx, N-2+Nx, N-3+Nx, N-3+2*Nx, N-3+4*Nx, N-4+Nx, N-4+3*Nx,
            N+1, N-1, N+Nx]
        return A
      
  if (y==1) and (x>3) and (x<Nx-4):    
        A =[N+1+Nx, N+1+2*Nx, N+1+3*Nx, N+1+4*Nx, N+2+3*Nx, N+2+Nx, N+3+Nx, N+3+2*Nx, N+3+4*Nx, N+4+Nx, N+4+3*Nx,
            N+1-Nx, N+2-Nx, N+3-Nx,  N+4-Nx, 
            N-1+Nx, N-1+2*Nx, N-1+3*Nx, N-1+4*Nx, N-2+3*Nx, N-2+Nx, N-3+Nx, N-3+2*Nx, N-3+4*Nx, N-4+Nx, N-4+3*Nx,
            N-1-Nx, N-2-Nx, N-3-Nx, N-4-Nx,
            N+1, N-1, N+Nx, N-Nx]    
        return A
    
  if (y==2) and (x>3) and (x<Nx-4):
        A =[N+1+Nx, N+1+2*Nx, N+1+3*Nx, N+1+4*Nx, N+2+3*Nx, N+2+Nx, N+3+Nx, N+3+2*Nx, N+3+4*Nx, N+4+Nx, N+4+3*Nx,
            N+1-Nx, N+1-2*Nx, N+2-Nx, N+3-Nx, N+3-2*Nx, N+4-Nx,
            N-1+Nx, N-1+2*Nx, N-1+3*Nx, N-1+4*Nx, N-2+3*Nx, N-2+Nx, N-3+Nx, N-3+2*Nx, N-3+4*Nx, N-4+Nx, N-4+3*Nx,
            N-1-Nx, N-1-2*Nx, N-2-Nx, N-3-Nx, N-3-2*Nx, N-4-Nx,
            N+1, N-1, N+Nx, N-Nx]
        return A
    
  if (y==3) and (x>3) and (x<Nx-4):
        A =[N+1+Nx, N+1+2*Nx, N+1+3*Nx, N+1+4*Nx, N+2+3*Nx, N+2+Nx, N+3+Nx, N+3+2*Nx, N+3+4*Nx, N+4+Nx, N+4+3*Nx,
            N+1-Nx, N+1-2*Nx, N+1-3*Nx, N+2-3*Nx, N+2-Nx, N+3-Nx, N+3-2*Nx, N+4-Nx, N+4-3*Nx,
            N-1+Nx, N-1+2*Nx, N-1+3*Nx, N-1+4*Nx, N-2+3*Nx, N-2+Nx, N-3+Nx, N-3+2*Nx, N-3+4*Nx, N-4+Nx, N-4+3*Nx,
            N-1-Nx, N-1-2*Nx, N-1-3*Nx, N-2-3*Nx, N-2-Nx, N-3-Nx, N-3-2*Nx, N-4-Nx, N-4-3*Nx,
            N+1, N-1, N+Nx, N-Nx]
        return A    
      
  if (y==Ny-1) and (x>3) and (x<Nx-4):     
        A =[N+1-Nx, N+1-2*Nx, N+1-3*Nx, N+1-4*Nx, N+2-3*Nx, N+2-Nx, N+3-Nx, N+3-2*Nx, N+3-4*Nx, N+4-Nx, N+4-3*Nx,
            N-1-Nx, N-1-2*Nx, N-1-3*Nx, N-1-4*Nx, N-2-3*Nx, N-2-Nx, N-3-Nx, N-3-2*Nx, N-3-4*Nx, N-4-Nx, N-4-3*Nx,
            N+1, N-1, N-Nx]
    
        return A
  if (y==Ny-2) and (x>3) and (x<Nx-4):  
          A =[N+1+Nx, N+2+Nx, N+3+Nx,  N+4+Nx, 
            N+1-Nx, N+1-2*Nx, N+1-3*Nx, N+1-4*Nx, N+2-3*Nx, N+2-Nx, N+3-Nx, N+3-2*Nx, N+3-4*Nx, N+4-Nx, N+4-3*Nx,
            N-1+Nx,  N-2+Nx, N-3+Nx,  N-4+Nx,
            N-1-Nx, N-1-2*Nx, N-1-3*Nx, N-1-4*Nx, N-2-3*Nx, N-2-Nx, N-3-Nx, N-3-2*Nx, N-3-4*Nx, N-4-Nx, N-4-3*Nx,
            N+1, N-1, N+Nx, N-Nx]
          return A
      
  if (y==Ny-3) and (x>3) and (x<Nx-4):      
#        A =[N+1+Nx, N+1+2*Nx, N+2+Nx, N+3+Nx, N+3+2*Nx,  N+4+Nx,
#            N+1-Nx, N+1-2*Nx, N+1-3*Nx, N+1-4*Nx, N+2-3*Nx, N+2-Nx, N+3-Nx, N+3-2*Nx, N+3-4*Nx, N+4-Nx, N+4-3*Nx,
#            N-1+Nx, N-1+2*Nx, N-1+3*Nx, N-1+4*Nx, N-2+3*Nx, N-2+Nx, N-3+Nx, N-3+2*Nx, N-3+4*Nx, N-4+Nx, N-4+3*Nx,
#            N-1-Nx, N-1-2*Nx, N-2-Nx, N-3-Nx, N-3-2*Nx, N-4-Nx,
#            N+1, N-1, N+Nx, N-Nx]    
        A =[N+1+Nx, N+1+2*Nx,    N+2+Nx, N+3+Nx, N+3+2*Nx,  N+4+Nx, 
            N+1-Nx, N+1-2*Nx, N+1-3*Nx, N+1-4*Nx, N+2-3*Nx, N+2-Nx, N+3-Nx, N+3-2*Nx, N+3-4*Nx, N+4-Nx, N+4-3*Nx,
            N-1+Nx, N-1+2*Nx,  N-2+Nx, N-3+Nx, N-3+2*Nx,  N-4+Nx, 
            N-1-Nx, N-1-2*Nx, N-1-3*Nx, N-1-4*Nx, N-2-3*Nx, N-2-Nx, N-3-Nx, N-3-2*Nx, N-3-4*Nx, N-4-Nx, N-4-3*Nx,
            N+1, N-1, N+Nx, N-Nx]
        
        return A
    
  if (y==Ny-4) and (x>3) and (x<Nx-4):  
        A =[N+1+Nx, N+1+2*Nx, N+1+3*Nx, N+2+3*Nx, N+2+Nx, N+3+Nx, N+3+2*Nx, N+4+Nx, N+4+3*Nx,
            N+1-Nx, N+1-2*Nx, N+1-3*Nx, N+1-4*Nx, N+2-3*Nx, N+2-Nx, N+3-Nx, N+3-2*Nx, N+3-4*Nx, N+4-Nx, N+4-3*Nx,
            N-1+Nx, N-1+2*Nx, N-1+3*Nx, N-1+4*Nx, N-2+3*Nx, N-2+Nx, N-3+Nx, N-3+2*Nx, N-3+4*Nx, N-4+Nx, N-4+3*Nx,
            N-1-Nx, N-1-2*Nx, N-1-3*Nx, N-2-3*Nx, N-2-Nx, N-3-Nx, N-3-2*Nx, N-3-4*Nx, N-4-3*Nx,
            N+1, N-1, N+Nx, N-Nx]         
         
  # Si arriba aqui es que el node es un dels 64 dels quatre vertex, el rebotem al seu pare i que dara tencat.
  return [N]    
       
def testVrtx(N):
    y=math.floor(N/Nx) #  Miren si un dode esta en un vertex amb un unic vei,no valis per nodEnd o nodIni
    x=N%Nx
    if x<4 and y<4:
        return False
    if x>Nx-5  and y<4:
        return False
    if x<4 and y>Ny-5 :
        return False
    if x>Nx-5 and y>Ny-5:
        return False
    return True     
         
def nod2cart(N):  # dona llista [y,x]    
    y=math.floor(N/Nx)      
    x=N%Nx
    return [y,x]
       