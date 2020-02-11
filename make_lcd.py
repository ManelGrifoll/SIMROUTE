# donada un columna de lon i lats es treu una matriu lon lats
import numpy  as np
import re
from  params import *
# #####################
arx_lcd='in/lcd_eu_h.dat'
ldc_out='in/ldcA1'
# ##################3
#nodes=dat['arr_0']
#inc=dat['arr_1']
#Nx=dat['arr_2']
#Ny=dat['arr_3']
#LonMin=dat['arr_4']
#LonMax=dat['arr_5']
#LatMin=dat['arr_6']
#LatMax=dat['arr_7']
p = re.compile(r'[-+]?\d+\.\d+')  # Compile a pattern to capture float values
file = open(arx_lcd, 'r')
nl=len(file.readlines()) 
print (nl) # 
file.close()
ldc=np.ones(shape=(nl, 2))
#ldc=np.ones(shape=(7, 2))
with open(arx_lcd,'r') as f:
      for cnt, line in enumerate(f):
       #     print("Line {}: {}".format(cnt, line))

            if line.find("NaN") !=-1:
                  ldc[cnt,0]=np.nan
                  ldc[cnt,1]=np.nan                        
            else:
                  floats = [float(i) for i in p.findall(line)]
                  a=floats[0]
                  b=floats[1]
                  if(a<LonMin or a>LonMax or b<LatMin or b>LatMax):
                        ldc[cnt,0]=np.nan
                        ldc[cnt,1]=np.nan                                                 
                  else:

                        ldc[cnt,0]=a
                        ldc[cnt,1]=b   

np.savez_compressed(ldc_out, ldc)

print("Acabat aqui")