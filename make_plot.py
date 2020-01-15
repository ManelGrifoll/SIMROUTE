import numpy  as np
from modsim import * 
from netCDF4 import Dataset 
import scipy.interpolate
import matplotlib.pyplot as plt
nodes='nodes.npz'
waves='in/waves_xxxx.npz'
dat = np.load(nodes)
nodes=dat['arr_0']
inc=dat['arr_1']
Nx=dat['arr_2']
Ny=dat['arr_3']
LonMin=dat['arr_4']
LonMax=dat['arr_5']
LatMin=dat['arr_6']
LatMax=dat['arr_7']
tira_lon=dat['arr_8']
tira_lat=dat['arr_9']

dat = np.load(waves)
hs=dat['arr_0']
fp=dat['arr_1']
dir=dat['arr_2']