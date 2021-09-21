#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 11:13:17 2021
Code part of SIMROUTE (UPC-BarcelonaTech)
version 31/01/2021
@author: manel grifoll (UPC-BarcelonaTech)

ship_emissions.py: estimate the make emissions using the STEAM2 (Jalkanen et al., 2012) 
and speed penalization from Molland et al (2007)

output: figure and .txt files in SIMROUTE/out/
"""
name_Simu='Palma_Barna'

import numpy as np
from func_postprocess import *
import matplotlib.pyplot as plt
import math as math
import os
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.mpl.ticker as cticker 
#offset=0.2
toTn=1/10**6   # passar a Tn
EL=0.80 # Engine load (in unit percentage)% 
Pow_Ins=18000 # Engine Power(kW)
V_design=26 # Velocity design (knots)
SFOC=200 # Specific fuel compsuntion (gr/kWh). 
SC=0.005 # Sulphur content of fuel (mass%) for Fuel Oil - IMO 2020 outside ECA zones
CC=0.88 # Carbon content of fuel (mass %) MDO
Engine_RPM=500 # Engine rpm; 

M_S=32.0655 # Molar mass of sulphur (gr/mol)
M_SO2=64.06436 # molar mass of sulphur dioxide g/mol (number of mols of S=number of mols of SO2)
M_C=12.01 # Molar mass of carbon (gr/mol)
M_CO2=44.0886 # Molar mass of carbon dioxide (gr/mol) (number of mols of C=number of mols of CO2)


## PARTICULATE MATTER

EF_EC=0.08 # Emission factor elementary carbon (gr/kWh)
EF_OC=0.2 # Emission factor for organic carbon (gr/kWh)
EF_ASH=0.06 # Emission factor for ash (gr/kWh)
OC_EL=1.024 # Part of organic carbon dependent of EL (dimensionless)

# END OF USER INPUTS   #######################

arx = '../out/'+name_Simu+'.npz'
if os.path.exists(arx) == False:
    print('Simulation '+arx+' not exist')
    raise SystemExit
arx_out = '../out/Emissions_'+name_Simu+'.txt'

dat = np.load(arx)
LonMin=dat['arr_0'][0]
LonMax=dat['arr_0'][1]
LatMin=dat['arr_0'][2]
LatMax=dat['arr_0'][3]
v0=dat['arr_0'][4]
inc=dat['arr_0'][5] 
nodIni=int(dat['arr_0'][6])
nodEnd=int(dat['arr_0'][7])
t_ini=int(dat['arr_0'][8])
time_res=int(dat['arr_0'][9])
WEN_form=int(dat['arr_0'][10])
Lbp=dat['arr_0'][11]
DWT=dat['arr_0'][12]
hs=dat['arr_1']
fp=dat['arr_2']
dir=dat['arr_3']
L_Trip=dat['arr_4']
L_TripFix=dat['arr_5']
Cost_Opt=dat['arr_6']
L_ConsCostTrip=dat['arr_7']
Cost_Min=dat['arr_8']
ARX=dat['arr_9']  

inc=inc/60.0    
#Re-build Mesh:
Nx=int(np.floor((LonMax-LonMin)/inc)+2)
Ny=int(np.floor((LatMax-LatMin)/inc)+2)
tira_lon=[]
for i in range(Nx):
    tira_lon.append(LonMin+i*inc)
tira_lat=[]
for j in range(Ny):  
    tira_lat.append(LatMin+j*inc)
nodes=np.zeros((Nx*Ny,2))
#print( ' Nx = {:6d} ---   Ny = {:4d}\n'.format(Nx,Ny))
#print('longituds    {:8.3f}    -----   {:8.3f} \n'.format(tira_lon[0],tira_lon[-1]))
#print('latituds     {:8.3f}    -----   {:8.3f} \n'.format(tira_lat[0],tira_lat[-1]))
for j in range(Ny):   
    for i in range(Nx):
        nodes[Nx*j +i,0]=tira_lon[i]
        nodes[Nx*j +i,1]=tira_lat[j]
inc=inc*60


nTrack= len(L_Trip)-1
v_opt= np.zeros (shape =( nTrack))   
for i in range(nTrack):
    N2=L_Trip[i+1]
    N1=L_Trip[i]
    v_opt[i]=( dist_mn(nodes[N2,0],nodes[N2,1],nodes[N1,0],nodes[N1,1]))/(Cost_Opt[i+1]-Cost_Opt[i])

nTrack= len(L_TripFix)-1
v_min= np.zeros (shape =( nTrack))   
for i in range(nTrack):
    N2=L_TripFix[i+1]
    N1=L_TripFix[i]
    v_min[i]=( dist_mn(nodes[N2,0],nodes[N2,1],nodes[N1,0],nodes[N1,1]))/(Cost_Min[i+1]-Cost_Min[i])


cte_k=(EL*Pow_Ins)/((V_design)**3) #Constant K (kW/kn^3)
#
Pow_trans_h=cte_k*(np.power(v_opt,3)) # transient Power at each interval (kW) (interval = node to node)
Pow_trans_h_min=cte_k*(np.power(v_min,3))# ; % hourly transient Power (kW)
#
Pow_trans=Pow_trans_h.sum()/(len(Pow_trans_h))  #;% Average Transient Power Opt
Pow_trans_min=Pow_trans_h_min.sum()/(len(Pow_trans_h_min)) #;%Average Transitient Power Dmin
#
Delta_V=v0-v_opt  #; % speed loss due to waves

#%%%%%%%% RUTA OPTIMA %%%%%%%%%%%%%%
Pow_Ef=Pow_Ins*0.80 #; % Effective power

Delta_Pow=Pow_trans_h*(1/(np.power((1-Delta_V/v0),3))-1) #; % Power increase to maintain speed

Pow_New=Pow_Ef+Delta_Pow

fig1 , (ax1,ax2) = plt.subplots(1,2)    
ax1.plot(Cost_Opt[1:],Pow_New)
ax1.set_xlabel('Hours')
ax1.set_title('Power Opt')
ax1.grid(True)
#plot(SIM.costt(2:end),Pow_New);
#xlabel('Hours')
#ylabel('Total power needed to maintain speed')
#grid on
#
#%%Impact of enigne load EL on SFOC
#
EL_New=Pow_New/Pow_Ins


SFOC_REL_New=(0.445*(np.power(EL_New,2))-(0.71*EL_New)+1.28)
#%%% And the absolute fuel consumption is estimated from:

SFOC_End=SFOC_REL_New*SFOC

Interv_t=np.diff(Cost_Opt)

Fuel_comp_New=Pow_New*SFOC_End*Interv_t

Fuel_comp_End=np.sum(Fuel_comp_New)

print('FFFF',Fuel_comp_End)
emi=open(arx_out,'w')
st='Simulation name: '+name_Simu+'\n'
emi.write(st)
print(st)
st='Fuel Consumption opt route    {:10.3f} Tn \n'.format(Fuel_comp_End*toTn)

print(st)
emi.write(st)
#%%%%%%%% RUTA MÍNIMA %%%%%%%%%%%%%%

Delta_V_min=v0-v_min

Delta_Pow_min=Pow_trans_h_min*(1./(np.power((1-Delta_V_min/v0),3))-1) #; % Power increase to maintain speed

Pow_New_min=Pow_Ef+Delta_Pow_min

EL_New_min=Pow_New_min/Pow_Ins

SFOC_REL_New_min=(0.445*(np.power(EL_New_min,2))-(0.71*EL_New_min)+1.28)

SFOC_End_min=SFOC_REL_New_min*SFOC
Interv_t_min=np.diff(Cost_Min)

Fuel_comp_New_min=Pow_New_min*SFOC_End_min*Interv_t_min

Fuel_comp_End_min=sum(Fuel_comp_New_min)

st='Fuel Consumption minimum route: {:10.3f} Tn \n'.format(Fuel_comp_End_min*toTn)  ###
print(st)
emi.write(st)
Fuel_saving=(1-(Fuel_comp_End/Fuel_comp_End_min))*100;

st='Fuel consumption reduction following optimum route: {:4.2f}%  \n'.format(Fuel_saving)  ###
print(st)
emi.write(st)
ax2.plot(Cost_Min[1:],Pow_New_min,'r')
ax2.set_title('Power Min')
ax2.set_xlabel('hours')
ax2.grid(True)
#plot(SIM_min.cost_min(2:end),Pow_New_min);

#%%%%%%%% RUTA OPTIMA %%%%%%%%%%%%%%

#%%% SO2

n_SO2_Interv=(SFOC_End*SC)/M_S  #;% number of mols of sulphur dioxide (mol/kWh)

Emi_fac_SO2_Interv=M_SO2*n_SO2_Interv #; % SO2 Emission factor (gr/kWh)

SO2_Interv=Pow_New*EL_New*Emi_fac_SO2_Interv*Interv_t  #; % SO2 emited at each interval in (gr)

SO2_End=np.sum(SO2_Interv)
#%%% CO2

n_CO2_Interv=(SFOC_End*CC)/M_C #;% number of mols of carbon dioxide (mol/kWh)
#
Emi_fac_CO2_Interv=M_CO2*n_CO2_Interv

CO2_Interv=Pow_New*EL_New*Emi_fac_CO2_Interv*Interv_t

CO2_End=np.sum(CO2_Interv)
#%%% NOX


if Engine_RPM<130:
    Emi_fac_NOx=17
else:
    if (130<=Engine_RPM) and (Engine_RPM<=2000):
        Emi_fac_NOx=45*Engine_RPM**(-0.2)
    else:
        if Engine_RPM>2000:
            Emi_fac_NOx=9.8



NOx_Interv=Pow_New*EL_New*Emi_fac_NOx*Interv_t #; % NOx emited at each interval in (gr)

NOx_End=np.sum(NOx_Interv) #; %Accumulated NOx emited optimized route (gr)

#%%% PARTICULATE MATTER

EF_SO4=0.312*SC  #; % Emission factor for SO4 (gr/kWh)

EF_H2O=0.244*SC#; % Emission factor H2O (gr/kWh)

Emi_fac_PM_Interv=SFOC_REL_New*(EF_SO4+EF_H2O+EF_OC*OC_EL+EF_EC+EF_ASH)#; %Particulate matter emission factor (gr/kWh)

PM_Interv=Pow_New*EL_New*Emi_fac_PM_Interv*Interv_t#; %PM emited at each interval in (gr)

PM_End=np.sum(PM_Interv)  #; % Accumulated PM emited optimized route (gr)

#%%%%%%%% RUTA MÍNIMA %%%%%%%%%%%%%%

#%%% SO2

n_SO2_Interv_min=(SFOC_End_min*SC)/M_S #;% number of mols of sulphur dioxide (mol/kWh)

Emi_fac_SO2_Interv_min=M_SO2*n_SO2_Interv_min #; % SO2 Emission factor (gr/kWh)

SO2_Interv_min=Pow_New_min*EL_New_min*Emi_fac_SO2_Interv_min*Interv_t_min#; % SO2 emited at each interval in (gr)


SO2_End_min=np.sum(SO2_Interv_min)  #; % Accumulated SO2 for the whole minimum distance trip in (gr)

#%%% CO2

n_CO2_Interv_min=(SFOC_End_min*CC)/M_C #;% number of mols of carbon dioxide (mol/kwh)

Emi_fac_CO2_Interv_min=M_CO2*n_CO2_Interv_min  #; % CO2 Emission factor (gr/kWh)

CO2_Interv_min=Pow_New_min*EL_New_min*Emi_fac_CO2_Interv_min*Interv_t_min#; %CO2 emited at each interval in (gr)

CO2_End_min=np.sum(CO2_Interv_min)#; % Accumulated CO2 for the whole minimum distance trip in (gr)

#%%% NOX

if Engine_RPM<130:
    Emi_fac_NOx=17
else:
    if (130<=Engine_RPM)and(Engine_RPM<=2000):
        Emi_fac_NOx=45*Engine_RPM**(-0.2)
    else:
        if Engine_RPM>2000:
            Emi_fac_NOx=9.8
 
#NOx_Interv_min=Pow_New_min.*EL_New_min.*Emi_fac_NOx.*Interv_t_min; % NOx emited per interval in (gr)
NOx_Interv_min=Pow_New_min*EL_New_min*Emi_fac_NOx*Interv_t_min# % NOx emited per interval in (gr)
#NOx_End_min=sum(NOx_Interv_min(1:end)); % Accumulated NOx for the whole minimum distance route (gr)
NOx_End_min=np.sum(NOx_Interv_min)#; % Accumulated NOx for the whole minimum distance route (gr)

#%%% PARTICULATE MATTER


EF_SO4=0.312*SC#; % Emission factor for SO4 (gr/kWh)

EF_H2O=0.244*SC # % Emission factor H2O (gr/kWh)

Emi_fac_PM_Interv_min=SFOC_REL_New_min*(EF_SO4+EF_H2O+EF_OC*OC_EL+EF_EC+EF_ASH)#; %Particulate matter emission factor (gr/kWh)

PM_Interv_min=Pow_New_min*EL_New_min*Emi_fac_PM_Interv_min*Interv_t_min#; %PM emited per interval in (gr)

PM_End_min=np.sum(PM_Interv_min) #; % Accumulated PM per minimum distance route in (gr)

Emissions_mitigation_percentage=(1-(CO2_End/CO2_End_min))*100

st='Percentage of emissions mitigation following optimum route: {:.2f}% \n'.format(Emissions_mitigation_percentage)
print(st)
emi.write(st)
#disp(['CO2 optimized: ' num2str(CO2_End/.10^(-06)) ' Tn'])
st='CO2 optimized:       {:7.3f} Tn \n'.format(CO2_End*toTn)
print(st)
emi.write(st)
#disp(['CO2 minimum: ' num2str(CO2_End_min/.10^(-06)) ' Tn'])
st='CO2 minimum dist.:   {:7.3f} Tn \n'.format(CO2_End_min*toTn)
print(st)
emi.write(st)
#disp(['SO2 optimized: ' num2str(SO2_End/.10^(-06)) ' Tn'])
st='SO2 optimized:       {:7.3f} Tn \n'.format(SO2_End*toTn)
print(st)
emi.write(st)
#disp(['SO2 minimum: ' num2str(SO2_End_min/.10^(-06)) ' Tn'])
st='SO2 minimum dist.:   {:7.3f} Tn \n'.format(SO2_End_min*toTn)
print(st)
emi.write(st)
#disp(['NOx optimized: ' num2str(NOx_End/.10^(-06)) ' Tn'])
st='NOx optimized:       {:7.3f} Tn \n'.format(NOx_End*toTn)
print(st)
emi.write(st)
#disp(['NOx minimum: ' num2str(NOx_End_min/.10^(-06)) ' Tn'])
st='NOx minimum dist.:   {:7.3f} Tn \n'.format(NOx_End_min*toTn)
print(st)
emi.write(st)
#disp(['PM optimized: ' num2str(PM_End/.10^(-06)) ' Tn'])
st='PM optimized:        {:7.3f} Tn \n'.format(PM_End*toTn)
print(st)
emi.write(st)
#disp(['PM minimum: ' num2str(PM_End_min/.10^(-06)) ' Tn'])
st='PM minimum dist.:    {:7.3f} Tn \n'.format(PM_End_min*toTn)
print(st)
emi.write(st)

emi.close()

fig2, axs = plt.subplots(2, 2, figsize=(9,9))
axs[0,0].plot(Cost_Opt[1:],CO2_Interv*toTn,'*m',label='$CO_{2}$ opt')
axs[0,0].plot(Cost_Min[1:],CO2_Interv_min*toTn,'*',color='orange',label='$CO_{2}$ min')
axs[0,0].set_title('Node-to-node $CO_{2}$')
#axs[0,0].set_xlabel('Hours')
axs[0,0].set_ylabel('Emissions (Tn)')
axs[0,0].grid(True)
axs[0,0].legend(loc='upper left')

axs[0,1].plot(Cost_Opt[1:],NOx_Interv*toTn,'*m',label='N0x opt')
axs[0,1].plot(Cost_Min[1:],NOx_Interv_min*toTn,'*',color='orange',label='NOx min')
axs[0,1].set_title('NOx')
#axs[0,1].set_xlabel('Hours')
#axs[0,1].set_ylabel('Emissions (Tn)')
axs[0,1].grid(True)
axs[0,1].legend(loc='upper left')

axs[1,0].plot(Cost_Opt[1:],SO2_Interv*toTn,'*m',label='$SO_{2}$ opt')
axs[1,0].plot(Cost_Min[1:],SO2_Interv_min*toTn,'*',color='orange',label='$SO_{2}$ min')
axs[1,0].set_title('Node-to-node $SO_{2}$')
axs[1,0].set_xlabel('Hours since departure')
axs[1,0].set_ylabel('Emissions (Tn)')
axs[1,0].grid(True)
axs[1,0].legend(loc='upper left')

axs[1,1].plot(Cost_Opt[1:],PM_Interv*toTn,'*m',label='PM opt')
axs[1,1].plot(Cost_Min[1:],PM_Interv_min*toTn,'*',color='orange',label='PM min')
axs[1,1].set_title('Node-to-node PM')
axs[1,1].set_xlabel('Hours since departure')
#axs[1,1].set_ylabel('Emissions (Tn)')
axs[1,1].grid(True)
axs[1,1].legend(loc='upper left')

plt.savefig('../out/Emission_'+name_Simu+'.png',dpi=300)
plt.show()

fig2, axs = plt.subplots(2, 2, figsize=(9,9))
axs[0,0].plot(Cost_Opt[1:],np.cumsum(CO2_Interv*toTn),'m',label='$CO_{2}$ opt')
axs[0,0].plot(Cost_Min[1:],np.cumsum(CO2_Interv_min*toTn),'orange',label='$CO_{2}$ min')
axs[0,0].set_title('Accum. $CO_{2}$')
#axs[0,0].set_xlabel('Hours')
axs[0,0].set_ylabel('Emissions (Tn)')
axs[0,0].grid(True)
axs[0,0].legend(loc='upper left')

axs[0,1].plot(Cost_Opt[1:],np.cumsum(NOx_Interv*toTn),'m',label='N0x opt')
axs[0,1].plot(Cost_Min[1:],np.cumsum(NOx_Interv_min*toTn),'orange',label='NOx min')
axs[0,1].set_title('Accum. NOx')
#axs[0,1].set_xlabel('Hours')
#axs[0,1].set_ylabel('Emissions (Tn)')
axs[0,1].grid(True)
axs[0,1].legend(loc='upper left')

axs[1,0].plot(Cost_Opt[1:],np.cumsum(SO2_Interv*toTn),'m',label='$SO_{2}$ opt')
axs[1,0].plot(Cost_Min[1:],np.cumsum(SO2_Interv_min*toTn),'orange',label='$SO_{2}$ min')
axs[1,0].set_title('Accum. $CO_{2}$')
axs[1,0].set_xlabel('Hours since departure')
axs[1,0].set_ylabel('Emissions (Tn)')
axs[1,0].grid(True)
axs[1,0].legend(loc='upper left')

axs[1,1].plot(Cost_Opt[1:],np.cumsum(PM_Interv*toTn),'m',label='PM opt')
axs[1,1].plot(Cost_Min[1:],np.cumsum(PM_Interv_min*toTn),'orange',label='PM min')
axs[1,1].set_title('Accum. PM')
axs[1,1].set_xlabel('Hours since departure')
#axs[1,1].set_ylabel('Emissions (Tn)')
axs[1,1].grid(True)
axs[1,1].legend(loc='upper left')

plt.savefig('../out/Emission_accumulated'+name_Simu+'.png',dpi=300)
plt.show()


