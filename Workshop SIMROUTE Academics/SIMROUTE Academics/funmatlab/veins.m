function propers=veins(N)
%neighbours' function 
global Nx Ny

y=floor(N/Nx)+1;
x=mod(N,Nx);
if x==0
    x=Nx;y=y-1;
end
%disp(['x=' num2str(x)])
%disp(['y=' num2str(y)])
if((x>3 && x<Nx-2) && (y>3 && y<Ny-2))
    A=[N+3,N+3+Nx,N+3+2*Nx,N+3+3*Nx,N+3*Nx+2,N+3*Nx+1,N+3*Nx,N+3*Nx-1,N+3*Nx-2,N+3*Nx-3,N+2*Nx-3,N+Nx-3,N-3,N-3-Nx,...
        N-3-2*Nx,N-3-3*Nx,N-2-3*Nx,N-1-3*Nx,N-3*Nx,N-3*Nx+1,N-3*Nx+2,N-3*Nx+3,N-2*Nx+3,N-Nx+3];
    propers = A;
    return
end
if((x==1) && (y==Ny))
    propers=[N+3,N+3-Nx,N+3-2*Nx,N+3-3*Nx,N+2-3*Nx,  N+1-3*Nx,N-3*Nx ];
    return
end
if((x==2) && (y==Ny))
    propers=[N+3,N+3-Nx,N+3-2*Nx,N+3-3*Nx,N+2-3*Nx,  N+1-3*Nx,N-3*Nx,N-3*Nx-1 ];
    return
    
end
if((x==3) && (y==Ny))
    propers=[N+3,N+3-Nx,N+3-2*Nx,N+3-3*Nx,N+2-3*Nx,  N+1-3*Nx,N-3*Nx,N-3*Nx-1,N-3*Nx-2 ];
    return
end
if (x>3 && x<(Nx-2)) && (y==Ny)
  propers=[N+3,N+3-Nx,N+3-2*Nx,N+3-3*Nx,N+2-3*Nx,  N+1-3*Nx,N-3*Nx,N-3*Nx-1,N-3*Nx-2, N-3*Nx-3,...
   N-2*Nx-3,N-Nx-3,  N-3 ];
  return
end
if (x==Nx-2) && (y==Ny)
  propers=[N+2-3*Nx,  N+1-3*Nx,N-3*Nx,N-3*Nx-1,N-3*Nx-2, N-3*Nx-3,...
   N-2*Nx-3,N-Nx-3,  N-3 ];
  return
end
if (x==Nx-1) && (y==Ny)
  propers=[ N+1-3*Nx,N-3*Nx,N-3*Nx-1,N-3*Nx-2, N-3*Nx-3,...
   N-2*Nx-3,N-Nx-3,  N-3 ];
  return
end
if (x==Nx) && (y==Ny)
  propers=[ N-3*Nx,N-3*Nx-1,N-3*Nx-2, N-3*Nx-3,...
   N-2*Nx-3,N-Nx-3,  N-3 ];
  return
end
if((x==1) && (y==Ny-1))
    propers=[N+3+Nx,N+3,N+3-Nx,N+3-2*Nx,N+3-3*Nx,N+2-3*Nx,  N+1-3*Nx,N-3*Nx ];
    return
end
if((x==2) && (y==Ny-1))
    propers=[N+3+Nx,N+3,N+3-Nx,N+3-2*Nx,N+3-3*Nx,N+2-3*Nx,  N+1-3*Nx,N-3*Nx,N-3*Nx-1 ];
    return
end
if((x==3) && (y==Ny-1))
    propers=[N+3+Nx,N+3,N+3-Nx,N+3-2*Nx,N+3-3*Nx,N+2-3*Nx,  N+1-3*Nx,N-3*Nx,N-3*Nx-1,N-3*Nx-2 ];
    return
end
if (x>3 && x<(Nx-2)) && (y==Ny-1)
  propers=[N+3+Nx,N+3,N+3-Nx,N+3-2*Nx,N+3-3*Nx,N+2-3*Nx,  N+1-3*Nx,N-3*Nx,N-3*Nx-1,N-3*Nx-2, N-3*Nx-3,...
   N-2*Nx-3,N-Nx-3,  N-3,N-3+Nx ];
  return
end

if (x==Nx-2 && y==Ny-1)
    propers=[N+2-3*Nx,  N+1-3*Nx,N-3*Nx,N-3*Nx-1,N-3*Nx-2, N-3*Nx-3,...
   N-2*Nx-3,N-Nx-3,  N-3,N-3+Nx ];
  return
end
if (x==Nx-1 && y==Ny-1)
    propers=[ N+1-3*Nx,N-3*Nx,N-3*Nx-1,N-3*Nx-2, N-3*Nx-3,...
   N-2*Nx-3,N-Nx-3,  N-3,N-3+Nx ];
  return
end
if (x==Nx && y==Ny-1)
    propers=[ N-3*Nx,N-3*Nx-1,N-3*Nx-2, N-3*Nx-3,...
   N-2*Nx-3,N-Nx-3,  N-3,N-3+Nx ];
  return
end
if (x>3 && x<(Nx-2)) && (y==Ny-2)
  propers=[N+3+2*Nx,N+3+Nx,N+3,N+3-Nx,N+3-2*Nx,N+3-3*Nx,N+2-3*Nx,  N+1-3*Nx,N-3*Nx,N-3*Nx-1,N-3*Nx-2, N-3*Nx-3,...
   N-2*Nx-3,N-Nx-3,  N-3,N-3+Nx,N-3+2*Nx ];
  return
end
if (x==3) && (y==Ny-2)
 propers=[N+3+2*Nx,N+3+Nx,N+3,N+3-Nx,N+3-2*Nx,N+3-3*Nx,N+2-3*Nx,  N+1-3*Nx,N-3*Nx,N-3*Nx-1,N-3*Nx-2];
  return
end    
if (x==2) && (y==Ny-2)
 propers=[N+3+2*Nx,N+3+Nx,N+3,N+3-Nx,N+3-2*Nx,N+3-3*Nx,N+2-3*Nx,  N+1-3*Nx,N-3*Nx,N-3*Nx-1];
  return
end    

if (x==1) && (y==Ny-2)
 propers=[N+3+2*Nx,N+3+Nx,N+3,N+3-Nx,N+3-2*Nx,N+3-3*Nx,N+2-3*Nx,  N+1-3*Nx,N-3*Nx];
  return
end    
 if (x==Nx-2) && (y==Ny-2)
 propers=[N+2-3*Nx,  N+1-3*Nx,N-3*Nx,N-3*Nx-1,N-3*Nx-2, N-3*Nx-3,...
   N-2*Nx-3,N-Nx-3,  N-3,N-3+Nx,N-3+2*Nx ];
  return
 end     
 if (x==Nx-1) && (y==Ny-2)
 propers=[  N+1-3*Nx,N-3*Nx,N-3*Nx-1,N-3*Nx-2, N-3*Nx-3,...
   N-2*Nx-3,N-Nx-3,  N-3,N-3+Nx,N-3+2*Nx ];
  return
 end     
 if (x==Nx) && (y==Ny-2)
 propers=[N-3*Nx,N-3*Nx-1,N-3*Nx-2, N-3*Nx-3,...
   N-2*Nx-3,N-Nx-3,  N-3,N-3+Nx,N-3+2*Nx ];
  return
 end     
 


 
if (x==1 && y==1)
    propers=[N+3*Nx,N+3*Nx+1,N+3*Nx+2,N+3*Nx+3,N+2*Nx+3,N+Nx+3,N+3 ];
    return
end
if (x==2 && y==1)
    propers=[N+3*Nx-1,N+3*Nx,N+3*Nx+1,N+3*Nx+2,N+3*Nx+3,N+2*Nx+3,N+Nx+3,N+3 ];
    return
end

if (x==3 && y==1)
    propers=[N+3*Nx-2,N+3*Nx-1,N+3*Nx,N+3*Nx+1,N+3*Nx+2,N+3*Nx+3,N+2*Nx+3,N+Nx+3,N+3 ];
    return
end
if (x>3 && x<Nx-2) && (y==1)
    propers=[N-3,N+Nx-3,N+2*Nx-3,N+3*Nx-3,N+3*Nx-2,N+3*Nx-1,N+3*Nx,N+3*Nx+1,N+3*Nx+2,N+3*Nx+3,N+2*Nx+3,N+Nx+3,N+3 ];
    return
end
if (x==Nx-2 && y==1)
    propers=[N-3,N+Nx-3,N+2*Nx-3,N+3*Nx-3,N+3*Nx-2,N+3*Nx-1,N+3*Nx,N+3*Nx+1,N+3*Nx+2];
    return
end
if (x==Nx-1 && y==1)
    propers=[N-3,N+Nx-3,N+2*Nx-3,N+3*Nx-3,N+3*Nx-2,N+3*Nx-1,N+3*Nx,N+3*Nx+1];
    return
end
if (x==Nx && y==1)
    propers=[N-3,N+Nx-3,N+2*Nx-3,N+3*Nx-3,N+3*Nx-2,N+3*Nx-1,N+3*Nx];
    return
end

if (x==1 && y==2)
    propers=[N+3*Nx,N+3*Nx+1,N+3*Nx+2,N+3*Nx+3,N+2*Nx+3,N+Nx+3,N+3,N+3-Nx ];
    return
end
if (x==2 && y==2)
    propers=[N+3*Nx-1,N+3*Nx,N+3*Nx+1,N+3*Nx+2,N+3*Nx+3,N+2*Nx+3,N+Nx+3,N+3,N+3-Nx ];
    return
end
if (x==3 && y==2)
    propers=[N+3*Nx-2,N+3*Nx-1,N+3*Nx,N+3*Nx+1,N+3*Nx+2,N+3*Nx+3,N+2*Nx+3,N+Nx+3,N+3,N+3-Nx ];
    return
end

if (x>3 && x<Nx-2) && (y==2)
    propers=[N-3-Nx,N-3,N+Nx-3,N+2*Nx-3,N+3*Nx-3,N+3*Nx-2,N+3*Nx-1,N+3*Nx,...
        N+3*Nx+1,N+3*Nx+2,N+3*Nx+3,N+2*Nx+3,N+Nx+3,N+3,N+3-Nx ];
    return
end
if (x==Nx-2 && y==2)
    propers=[N-3-Nx,N-3,N+Nx-3,N+2*Nx-3,N+3*Nx-3,N+3*Nx-2,N+3*Nx-1,N+3*Nx,N+3*Nx+1,N+3*Nx+2];
    return
end
if (x==Nx-1 && y==2)
    propers=[N-3-Nx,N-3,N+Nx-3,N+2*Nx-3,N+3*Nx-3,N+3*Nx-2,N+3*Nx-1,N+3*Nx,N+3*Nx+1];
    return
end
if (x==Nx && y==2)
    propers=[N-3-Nx,N-3,N+Nx-3,N+2*Nx-3,N+3*Nx-3,N+3*Nx-2,N+3*Nx-1,N+3*Nx];
    return
end
%%%%%%%%%%
if (x==1 && y==3)
    propers=[N+3*Nx,N+3*Nx+1,N+3*Nx+2,N+3*Nx+3,N+2*Nx+3,N+Nx+3,N+3,N+3-Nx,N+3-2*Nx ];
    return
end
if (x==2 && y==3)
    propers=[N+3*Nx-1,N+3*Nx,N+3*Nx+1,N+3*Nx+2,N+3*Nx+3,N+2*Nx+3,N+Nx+3,N+3,N+3-Nx,N+3-2*Nx ];
    return
end
if (x==3 && y==3)
    propers=[N+3*Nx-2,N+3*Nx-1,N+3*Nx,N+3*Nx+1,N+3*Nx+2,N+3*Nx+3,N+2*Nx+3,N+Nx+3,N+3,N+3-Nx,N+3-2*Nx ];
    return
end

if (x>3 && x<Nx-2) && (y==3)
    propers=[N-3-2*Nx,N-3-Nx,N-3,N+Nx-3,N+2*Nx-3,N+3*Nx-3,N+3*Nx-2,N+3*Nx-1,N+3*Nx,...
        N+3*Nx+1,N+3*Nx+2,N+3*Nx+3,N+2*Nx+3,N+Nx+3,N+3,N+3-Nx,N+3-2*Nx ];
    return
end
if (x==Nx-2 && y==3)
    propers=[N-3-2*Nx,N-3-Nx,N-3,N+Nx-3,N+2*Nx-3,N+3*Nx-3,N+3*Nx-2,N+3*Nx-1,N+3*Nx,N+3*Nx+1,N+3*Nx+2];
    return
end
if (x==Nx-1 && y==3)
    propers=[N-3-2*Nx,N-3-Nx,N-3,N+Nx-3,N+2*Nx-3,N+3*Nx-3,N+3*Nx-2,N+3*Nx-1,N+3*Nx,N+3*Nx+1];
    return
end
if (x==Nx && y==3)
    propers=[N-3-2*Nx,N-3-Nx,N-3,N+Nx-3,N+2*Nx-3,N+3*Nx-3,N+3*Nx-2,N+3*Nx-1,N+3*Nx];
    return
end
if x==1
    propers=[N+3*Nx,N+3*Nx+1,N+3*Nx+2,N+3*Nx+3,N+2*Nx+3,N+Nx+3,N+3,N+3-Nx,N+3-2*Nx,N+3-3*Nx,N+2-3*Nx,N+1-3*Nx,N-3*Nx];
    return
end
if x==2
    propers=[N+3*Nx-1,N+3*Nx,N+3*Nx+1,N+3*Nx+2,N+3*Nx+3,N+2*Nx+3,N+Nx+3,N+3,N+3-Nx,...
        N+3-2*Nx,N+3-3*Nx,N+2-3*Nx,N+1-3*Nx,N-3*Nx,N-3*Nx-1];
    return
end
if x==3
    propers=[N+3*Nx-2,N+3*Nx-1,N+3*Nx,N+3*Nx+1,N+3*Nx+2,N+3*Nx+3,N+2*Nx+3,N+Nx+3,N+3,N+3-Nx,...
        N+3-2*Nx,N+3-3*Nx,N+2-3*Nx,N+1-3*Nx,N-3*Nx,N-3*Nx-1,N-3*Nx-2];
    return
end
if x==Nx
    propers=[N+3*Nx,N+3*Nx-1,N+3*Nx-2,N+3*Nx-3,N+2*Nx-3,N+Nx-3,N-3,N-3-Nx,...
        N-3-2*Nx,N-3-3*Nx,N-2-3*Nx,N-1-3*Nx,N-3*Nx];        
    return
end
if x==Nx-1
    propers=[N+3*Nx+1,N+3*Nx,N+3*Nx-1,N+3*Nx-2,N+3*Nx-3,N+2*Nx-3,N+Nx-3,N-3,N-3-Nx,...
        N-3-2*Nx,N-3-3*Nx,N-2-3*Nx,N-1-3*Nx,N-3*Nx,N-3*Nx+1];        
    return
end
if x==Nx-2
    propers=[N+3*Nx+2,N+3*Nx+1,N+3*Nx,N+3*Nx-1,N+3*Nx-2,N+3*Nx-3,N+2*Nx-3,N+Nx-3,N-3,N-3-Nx,...
        N-3-2*Nx,N-3-3*Nx,N-2-3*Nx,N-1-3*Nx,N-3*Nx,N-3*Nx+1,N-3*Nx+2];        
    return
end
propers= 99999;
return


       
    
