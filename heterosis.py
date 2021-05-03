#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 23 12:59:32 2021

@author: stefan
"""

import pandas as pd
import numpy as np
from scipy.stats import ttest_ind
data=pd.read_csv("heterosis.csv")
Pf_v=data['P_f value']
F1_v=data['F_1 value']
Pm_v=data['P_m value']

Pf_mean=data['P_f value'].mean()
F1_mean=data['F_1 value'].mean()
Pm_mean=data['P_m value'].mean()

Pf_n=data['P_f name'][1]
F1_n=data['F_1 name'][1]
Pm_n=data['P_m name'][1]


#index=['$P_f$', '$F_1$', '$P_m$']

index=[Pf_n,F1_n,Pm_n]

mean_data=pd.DataFrame({'Percentage':[Pf_mean, F1_mean, Pm_mean]},index)
mpv=(Pf_mean+Pm_mean)/2

Pf_sem=data['P_f value'].sem()
F1_sem=data['F_1 value'].sem()
Pm_sem=data['P_m value'].sem()

sem_data=pd.DataFrame({'Percentage':[Pf_sem, F1_sem, Pm_sem]},index)

#independent t-tests
#ptt_Pf_Pm=ttest_ind(Pf,Pm)
ptt_Pf_F1=ttest_ind(Pf_v,F1_v)
ptt_Pm_F1=ttest_ind(Pm_v,F1_v)


ax = mean_data.plot.bar(yerr=sem_data,rot=0,
                          title='Rate of Seed Setting ($\%$)', 
                          color='forestgreen',
                          edgecolor='green', width=0.8)
                          
    
ax.set(ylim=(0,100))      
ax.legend(loc='upper right')
ax.set(xlabel='Variety', ylabel='Rate of Seed Setting ($\%$)')

mpv=(Pf_mean+Pm_mean)/2
ax.axhline(mpv, color="gray")
ax.text(-0.08, mpv, 'MPV', va='center', ha="left",
        bbox=dict(facecolor="w",alpha=0.5),
        transform=ax.get_yaxis_transform())
ax.text(1.02, mpv, mpv.round(2), va='center', ha="left",
        bbox=dict(facecolor="w",alpha=0.5),
        transform=ax.get_yaxis_transform())
ax.text(0.02, 92, 'a=MPV-'+ str(Pf_n) + '='
        + str((mpv-Pf_mean).round(2)) , va='center', ha="left",
        bbox=dict(facecolor="w",alpha=0.5),
        transform=ax.get_yaxis_transform())
ax.text(0.42, 92, 'd='+ str(F1_n) + '-MPV=' 
        + str((F1_mean-mpv).round(2)) , va='center', ha="left",
        bbox=dict(facecolor="w",alpha=0.5),
        transform=ax.get_yaxis_transform())
ax.text(0.02, 82, '|d/a|=|'+ str((F1_mean-mpv).round(2))  + '/'
        + str((mpv-Pf_mean).round(2)) + '|=' 
        + str(abs((F1_mean-mpv) /(mpv-Pf_mean)).round(2))
        , va='center', ha="left",
        bbox=dict(facecolor="w",alpha=0.5),
        transform=ax.get_yaxis_transform())
if abs((F1_mean-mpv)/(mpv-Pf_mean))<0.2:
    ax.text(0.42, 82, 'additive (|d/a|<0.2)'
        , va='center', ha="left",
        bbox=dict(facecolor="w",alpha=0.5),
        transform=ax.get_yaxis_transform())
if abs((F1_mean-mpv)/(mpv-Pf_mean))>=0.2 and abs(
        (F1_mean-mpv)/(mpv-Pf_mean))<0.8:
    ax.text(0.42, 82, 'partially dominant (0.2 ≤ |d/a| < 0.8)'
        , va='center', ha="left",
        bbox=dict(facecolor="w",alpha=0.5),
        transform=ax.get_yaxis_transform())
if abs((F1_mean-mpv)/(mpv-Pf_mean))>=0.8 and abs(
        (F1_mean-mpv)/(mpv-Pf_mean))<1.2:
    ax.text(0.42, 82, 'completely dominant (0.8 ≤ |d/a| < 1.2)'
        , va='center', ha="left",
        bbox=dict(facecolor="w",alpha=0.5),
        transform=ax.get_yaxis_transform())
if abs((F1_mean-mpv)/(mpv-Pf_mean))>=1.2:
    ax.text(0.42, 82, 'overdominant (|d/a| >= 1.2)'
        , va='center', ha="left",
        bbox=dict(facecolor="w",alpha=0.5),
        transform=ax.get_yaxis_transform())
ax.text(0.02, 72, 'MPH=('+ str(F1_n)+'-MPV)/MPV*100%'  + '='
        + str(((F1_mean-mpv)/mpv*100).round(2)) + '$\%$'
        , va='center', ha="left",
        bbox=dict(facecolor="w",alpha=0.5),
        transform=ax.get_yaxis_transform())
ax.figure.savefig('heterosis.pdf')              
ax.clear()