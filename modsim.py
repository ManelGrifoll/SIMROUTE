import numpy  as np
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

