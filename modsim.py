import numpy  as np
from  params import *
import math as math

global nodes
def cart2compass(deg):
   #Function that converts cartesian angles to compass angles arg <=360
   degN=90 - deg
   if ( degN) <0:
      return degN+360
   else:
      return degN
 
def compass2cart(degN):
    #Function that converts compass angles to cartesian angles arg <=360
   if (degN>=0) & (degN<=90):
      return abs(degN-90)
   else:
      return abs(450-degN)
   
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
   return out
   
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
       cost_i  per escollir el time del onatage """
   iv=math.floor(cost_i)+1
   tau=1-(cost_i-math.floor(cost_i))
   hm=0.5*(hs[nod_i,iv]+hs[nod_f,iv])
   ang_ship=ang_edge(nod_f,nod_i)
   hm=hm*3.28084
   vel=v0-reduc_v(ang_ship,dir[nod_f,iv])*hm*hm;
   if vel<0:
      for i in range(100):
         print('Pareu maquines anem enradera')

   return vel

def ang_edge(n_desti,n_ori):
   x=nodes[n_desti,0]-nodes[n_ori,0];
   y=nodes[n_desti,1]-nodes[n_ori,1];
   at=math.atan2(y,x);
   alfa =cart2compass(np.rad2deg(at));
   return alfa

def reduc_v(ang_ship,ang_wave):
   #%Bowditch speed penalty
   if(ang_wave>ang_ship):
      a=-ang_ship+ang_wave;
   else:
      a=ang_ship-ang_wave;  
   if ((a>=45 and a<=135) or (a>=225 and a<=315)):
      f_theta=0.0165
      return f_theta
   if (a>135 and a<225):
      f_theta=0.0248;
      return f_theta

   if ((a>=0 and a<45) or(a>315 and a<=360)):
      f_theta=0.0083
      return f_theta

   f_theta=0  
   return f_theta

def time_edge(v0,n_o,n_e,cost):
   #With a edge length given and knowing the cost (time from start point)
   # and figuring that height and direction are known, acumulated time is 
   # found. It finishes travelling the edge, knowing that
   # THERE IS AN HOURLY SWELL RESOLUTION
   L=dist_nods(n_o,n_e)
   q=1                        # It will inform whether the edge is done or not
   tau=1-(cost-math.floor(cost))    #remaining time for travelling at current speed, swell changes hourly 
   while q==1:
      if veloc(v0,n_o,n_e,cost)*tau>L:   # with tau, remaining time for travelling the edge, it makes it and leaves (q==0)
         cost=cost+L/veloc(v0,n_o,n_e,cost)
         q=0
      else:
         L=L-veloc(v0,n_o,n_e,cost)*tau  #now the edge is shorter
         cost=cost+tau   #cost is actualized
         tau=1  #remaining time is 1 hour      
   
   return  cost
