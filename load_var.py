import numpy  as np

dat = np.load('in/nodes.npz')
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

dat = np.load('in/waves_xxxx.npz')
hs=dat['arr_0']
fp=dat['arr_1']
dir=dat['arr_2']

dat=np.load('in/ldcTrim.npz')
ldc=dat['arr_0']