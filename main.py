from  params import *
#from  func_namoa import *
from  mod_veins import *

#from load_waves import *
import matplotlib.pyplot as plt
import numpy as np
n=1380

L=veins(n)

plt.figure(1)
plt.plot(nodes[n,0],nodes[n,1],'*k')

for i in L:
    plt.plot(nodes[i,0],nodes[i,1],'o')
plt.show()