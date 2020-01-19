# first run de previous and zoom the zone desired to make sea
# afterwards, run this program.
#The sequence is from bottom left to top right
#the result is the start with sifix _m
import numpy  as np
N1=4138
N2=4472
dat = np.load('nodes.npz')
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


