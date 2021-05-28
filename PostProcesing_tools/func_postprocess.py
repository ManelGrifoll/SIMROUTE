#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 14 00:01:26 2021

@author: xarx
"""
import numpy as np
def ang_encounter(ang_ship,ang_wave):
    if(ang_wave>ang_ship):
        theta=ang_wave-ang_ship
        return theta
    else:
        theta=360-(ang_ship-ang_wave)
        return theta
def dist_arc(loni,lati,lone,late):   #resultat en radiants    
    cosp=(np.cos(np.deg2rad(90-lati))*np.cos(np.deg2rad(90-late)) +
        np.sin(np.deg2rad(90-lati))*np.sin(np.deg2rad(90-late)) * 
        np.cos(np.deg2rad(lone-loni)))    
    return np.arccos(cosp)   #np.arccos(cosp)

def dist_mn(loni,lati,lone,late):                   
    d_rads=dist_arc(loni,lati,lone,late)
    d=d_rads*180/np.pi*60
    return d
            
def rumIni(loni,lati,lone,late):
    if lati==late:
        if loni >lone:
            return 270
        else:
            return 90     
    loni=loni+0.00001    
    k=dist_arc(loni,lati,lone,late)
    cosI=(np.cos(np.deg2rad(90-late))- np.cos(k)*
          np.cos(np.deg2rad(90-lati))) /((np.sin(k)) *
          np.sin(np.deg2rad(90-lati)) ) 
    I=np.arccos(cosI)
    I=I*180/np.pi
    if loni>lone:
        return  360-I
    else:
        return I

def rumEnd(loni,lati,lone,late):
    if lati==late:
        if loni >lone:
            return 270
        else:
            return 90
    loni=loni+0.00001        
    k=dist_arc(loni,lati,lone,late)
    cosE=(np.cos(np.deg2rad(90-lati))- np.cos(k)*
          np.cos(np.deg2rad(90-late))) /((np.sin(k)) *
          np.sin(np.deg2rad(90-late)) ) 
    E=np.arccos(cosE)
    E=E*180/np.pi
    if loni>lone:
        return  180+E
    else:
        return 180 -E
def distL(Lst,m):    
    ''' Last llista,  m valor donat la funcio torna
    el index de l'element de la llista mes prox a m
    '''
    ele=-1
    if m==0:
        return 0
    if Lst[-1]<m:
        return len(Lst)-1
    for i in range(len(Lst)):
        if (Lst[i]-m) < 0: # pssa el valor buscat
            ele=i
    d1=m-Lst[ele]
    d2=Lst[ele+1] -m
    if d1<d2 :
        return ele
    else:
        if ele>=len(Lst):
            return ele
        return ele+1            
            