import math as math
from  params import *

def veins(N):
  y=math.floor(N/Nx) #+1
  x=N%Nx  # numero de fila començant per zero  (hi ha Nx-1 files i Ny-1 columnes)
  
  if((x>2 and x<Nx-3) and (y>2 and y<Ny-3)):
        A=[N+3,N+3+Nx,N+3+2*Nx,N+3+3*Nx,N+3*Nx+2,N+3*Nx+1,N+3*Nx,N+3*Nx-1,N+3*Nx-2,N+3*Nx-3,N+2*Nx-3,N+Nx-3,N-3,N-3-Nx, N-3-2*Nx,N-3-3*Nx,N-2-3*Nx,N-1-3*Nx,N-3*Nx,N-3*Nx+1,N-3*Nx+2,N-3*Nx+3,N-2*Nx+3,N-Nx+3]
        return A
  if((x==0) and (y==Ny-1)):   #vertex N-W
        propers=[N+3,N+3-Nx,N+3-2*Nx,N+3-3*Nx,N+2-3*Nx,  N+1-3*Nx,N-3*Nx ]
        return propers

  if((x==1) and (y==Ny-1)): #un a la dreta 
        propers=[N+3,N+3-Nx,N+3-2*Nx,N+3-3*Nx,N+2-3*Nx,  N+1-3*Nx,N-3*Nx,N-3*Nx-1 ]
        return propers
    

  if((x==2) and (y==Ny-1)): #un altre a la dreta
            propers=[N+3,N+3-Nx,N+3-2*Nx,N+3-3*Nx,N+2-3*Nx,  N+1-3*Nx,N-3*Nx,N-3*Nx-1,N-3*Nx-2 ]
            return propers

  if (x>2 and x<(Nx-3)) and (y==Ny-1):  # el marc de dalt sense recons
            propers=[N+3,N+3-Nx,N+3-2*Nx,N+3-3*Nx,N+2-3*Nx,  N+1-3*Nx,N-3*Nx,N-3*Nx-1,N-3*Nx-2, N-3*Nx-3,  N-2*Nx-3,N-Nx-3,  N-3 ]
            return propers

  if (x==Nx-3) and (y==Ny-1): #  primer acostatse al raco
            propers=[N+2-3*Nx,N+1-3*Nx,N-3*Nx,N-3*Nx-1,N-3*Nx-2, N-3*Nx-3,  N-2*Nx-3,N-Nx-3,  N-3 ]
            return propers

  if (x==Nx-2) and (y==Ny-1): #segon
            propers=[ N+1-3*Nx,N-3*Nx,N-3*Nx-1,N-3*Nx-2, N-3*Nx-3, N-2*Nx-3,N-Nx-3,  N-3 ]
            return propers
  if (x==Nx-1) and (y==Ny-1): # ultim nod del mar de dalt
            propers=[ N-3*Nx,N-3*Nx-1,N-3*Nx-2, N-3*Nx-3, N-2*Nx-3,N-Nx-3,  N-3 ]
            return propers

  if((x==0) and (y==Ny-2)): #  Marc 2n de sota
            propers=[N+3+Nx,N+3,N+3-Nx,N+3-2*Nx,N+3-3*Nx,N+2-3*Nx,  N+1-3*Nx,N-3*Nx ]
            return propers

  if((x==1) and (y==Ny-2)):  # segon del raco
            propers=[N+3+Nx,N+3,N+3-Nx,N+3-2*Nx,N+3-3*Nx,N+2-3*Nx,  N+1-3*Nx,N-3*Nx,N-3*Nx-1 ]
            return propers

  if((x==2) and (y==Ny-2)):  # tercer del reco
            propers=[N+3+Nx,N+3,N+3-Nx,N+3-2*Nx,N+3-3*Nx,N+2-3*Nx,  N+1-3*Nx,N-3*Nx,N-3*Nx-1,N-3*Nx-2 ]
            return propers

  if (x>2 and x<(Nx-3)) and (y==Ny-2):  #sota marc fins arribar al raco
            propers=[N+3+Nx,N+3,N+3-Nx,N+3-2*Nx,N+3-3*Nx,N+2-3*Nx,  N+1-3*Nx,N-3*Nx,N-3*Nx-1,N-3*Nx-2, N-3*Nx-3,  N-2*Nx-3,N-Nx-3,  N-3,N-3+Nx ]
            return propers


  if (x==Nx-3 and y==Ny-2): #son raco
            propers=[N+2-3*Nx,  N+1-3*Nx,N-3*Nx,N-3*Nx-1,N-3*Nx-2, N-3*Nx-3,  N-2*Nx-3,N-Nx-3,  N-3,N-3+Nx ]
            return propers

  if (x==Nx-2 and y==Ny-2):#son raco
            propers=[ N+1-3*Nx,N-3*Nx,N-3*Nx-1,N-3*Nx-2, N-3*Nx-3, N-2*Nx-3,N-Nx-3,  N-3,N-3+Nx ]
            return propers

  if (x==Nx-1 and y==Ny-2):#son raco
            propers=[ N-3*Nx,N-3*Nx-1,N-3*Nx-2, N-3*Nx-3, N-2*Nx-3,N-Nx-3,  N-3,N-3+Nx ]
            return propers
          
  if (x>2 and x<(Nx-3)) and (y==Ny-3): # ultim tram llarg de dalt despres fara els recons
            propers=[N+3+2*Nx,N+3+Nx,N+3,N+3-Nx,N+3-2*Nx,N+3-3*Nx,N+2-3*Nx,  N+1-3*Nx,N-3*Nx,N-3*Nx-1,N-3*Nx-2, N-3*Nx-3, N-2*Nx-3,N-Nx-3,  N-3,N-3+Nx,N-3+2*Nx ]
            return propers

  if (x==2) and (y==Ny-3):   #raco esquerra tercer tram
            propers=[N+3+2*Nx,N+3+Nx,N+3,N+3-Nx,N+3-2*Nx,N+3-3*Nx,N+2-3*Nx,  N+1-3*Nx,N-3*Nx,N-3*Nx-1,N-3*Nx-2]
            return propers
    
  if (x==1) and (y==Ny-3):#raco esqtercer tram
            propers=[N+3+2*Nx,N+3+Nx,N+3,N+3-Nx,N+3-2*Nx,N+3-3*Nx,N+2-3*Nx,  N+1-3*Nx,N-3*Nx,N-3*Nx-1]
            return propers

  if (x==0) and (y==Ny-3):#raco esq tercer tram
            propers=[N+3+2*Nx,N+3+Nx,N+3,N+3-Nx,N+3-2*Nx,N+3-3*Nx,N+2-3*Nx,  N+1-3*Nx,N-3*Nx]
            return propers

  if (x==Nx-3) and (y==Ny-3):  #raco dret del tram tercer
            propers=[N+2-3*Nx,  N+1-3*Nx,N-3*Nx,N-3*Nx-1,N-3*Nx-2, N-3*Nx-3,  N-2*Nx-3,N-Nx-3,  N-3,N-3+Nx,N-3+2*Nx ]
            return propers
 
  if (x==Nx-2) and (y==Ny-3): #raco dret del tram tercer
            propers=[  N+1-3*Nx,N-3*Nx,N-3*Nx-1,N-3*Nx-2, N-3*Nx-3,   N-2*Nx-3,N-Nx-3,  N-3,N-3+Nx,N-3+2*Nx ]
            return propers
 
  if (x==Nx-1) and (y==Ny-3): #raco dret del tram tercer
            propers=[N-3*Nx,N-3*Nx-1,N-3*Nx-2, N-3*Nx-3, N-2*Nx-3,N-Nx-3,  N-3,N-3+Nx,N-3+2*Nx ]
            return propers
        

 
  if (x==0 and y==0): #tramsota  raco dret
            propers=[N+3*Nx,N+3*Nx+1,N+3*Nx+2,N+3*Nx+3,N+2*Nx+3,N+Nx+3,N+3 ];
            return propers

  if (x==1 and y==0): #segon
            propers=[N+3*Nx-1,N+3*Nx,N+3*Nx+1,N+3*Nx+2,N+3*Nx+3,N+2*Nx+3,N+Nx+3,N+3 ]
            return propers

  if (x==2 and y==0): # tercer
            propers=[N+3*Nx-2,N+3*Nx-1,N+3*Nx,N+3*Nx+1,N+3*Nx+2,N+3*Nx+3,N+2*Nx+3,N+Nx+3,N+3 ]
            return propers

  if (x>2 and x<Nx-3) and (y==0):
            propers=[N-3,N+Nx-3,N+2*Nx-3,N+3*Nx-3,N+3*Nx-2,N+3*Nx-1,N+3*Nx,N+3*Nx+1,N+3*Nx+2,N+3*Nx+3,N+2*Nx+3,N+Nx+3,N+3 ]
            return  propers

  if (x==Nx-3 and y==0):
            propers=[N-3,N+Nx-3,N+2*Nx-3,N+3*Nx-3,N+3*Nx-2,N+3*Nx-1,N+3*Nx,N+3*Nx+1,N+3*Nx+2]
            return propers

  if (x==Nx-2 and y==0):
            propers=[N-3,N+Nx-3,N+2*Nx-3,N+3*Nx-3,N+3*Nx-2,N+3*Nx-1,N+3*Nx,N+3*Nx+1]
            return propers
