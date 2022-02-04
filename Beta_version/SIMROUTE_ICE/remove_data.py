# -*- coding: utf-8 -*-
"""
Created on Sun Oct  3 18:47:21 2021

@author: polbl
"""

import os
import glob
print('All data interpolated and routes optimized, proceeding to delete files in /storeWaves')
storeddatapath = 'C:/Users/polbl/OneDrive/Documents/SIMROUTE/storeWaves/'
files = glob.glob(storeddatapath+'*.nc')
for f in files:
    os.remove(f)
print('Files deleted')

npz1storedpath = 'C:/Users/polbl/OneDrive/Documents/SIMROUTE/in/'
files = glob.glob(npz1storedpath+'*.npz')
for f in files:
    os.remove(f)
print('Files deleted')

npz2storedpath = 'C:/Users/polbl/OneDrive/Documents/SIMROUTE/out/'
files = glob.glob(npz2storedpath+'*.npz')
for f in files:
    os.remove(f)
print('Files deleted')