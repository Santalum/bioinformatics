#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 23 12:59:32 2021

@author: stefan
"""

import pandas as pd
import numpy as np
from scipy.stats import ttest_ind
data=pd.read_csv("traits.csv")
Pf_v=data['P_f value']
F1_v=data['F_1 value']
Pm_v=data['P_m value']



Pf_n=data['P_f name'][1]
F1_n=data['F_1 name'][1]
Pm_n=data['P_m name'][1]

index=[Pf_n,F1_n,Pm_n]

Pftraitmeansem=pd.DataFrame(columns=["Trait", "mean","sem"])
F1traitmeansem=pd.DataFrame(columns=["Trait", "mean","sem"])
Pmtraitmeansem=pd.DataFrame(columns=["Trait", "mean","sem"])
for trait in data['Trait'].unique():
    #calculates means and sems for each trait
    Pftraitmeansem=Pftraitmeansem.append({'Trait': trait,
                       'mean': data['P_f value'][data['Trait']==trait].mean(),
    'sem': data['P_f value'][data['Trait']==trait].sem()},
    ignore_index=True)
    F1traitmeansem=F1traitmeansem.append({'Trait': trait,
                       'mean': data['F_1 value'][data['Trait']==trait].mean(),
    'sem': data['F_1 value'][data['Trait']==trait].sem()},
    ignore_index=True)
    Pmtraitmeansem=Pmtraitmeansem.append({'Trait': trait,
                       'mean': data['P_m value'][data['Trait']==trait].mean(),
    'sem': data['P_m value'][data['Trait']==trait].sem()},
    ignore_index=True)
    
    
    #index=['$P_f$', '$F_1$', '$P_m$']
    
    
    mean_data=pd.DataFrame({trait:[
            Pftraitmeansem['mean'][Pftraitmeansem['Trait']==trait].iloc[0], 
                F1traitmeansem['mean'][F1traitmeansem['Trait']==trait].iloc[0],
            Pmtraitmeansem['mean'][Pmtraitmeansem['Trait']==trait].iloc[0]]},index)
    
    mpv=(Pftraitmeansem['mean'][Pftraitmeansem['Trait']==trait]+
        Pmtraitmeansem['mean'][Pmtraitmeansem['Trait']==trait])/2
    mpv=mpv.iloc[0]
    
    sem_data=pd.DataFrame({trait:[
        Pftraitmeansem['sem'][Pftraitmeansem['Trait']==trait].iloc[0], 
        F1traitmeansem['sem'][F1traitmeansem['Trait']==trait].iloc[0],
        Pmtraitmeansem['sem'][Pmtraitmeansem['Trait']==trait].iloc[0]]},index)    
    
    ax = mean_data.plot.bar(yerr=sem_data,rot=0,
                              title=trait, 
                              color='forestgreen',
                              edgecolor='green', width=0.8)
   
    Pf_mean=Pftraitmeansem['mean'][Pftraitmeansem['Trait']==trait].iloc[0]
    F1_mean=F1traitmeansem['mean'][F1traitmeansem['Trait']==trait].iloc[0]
    Pm_mean=Pmtraitmeansem['mean'][Pmtraitmeansem['Trait']==trait].iloc[0]

    Pf_sem=Pftraitmeansem['sem'][Pftraitmeansem['Trait']==trait].iloc[0]
    F1_sem=F1traitmeansem['sem'][F1traitmeansem['Trait']==trait].iloc[0]
    Pm_sem=Pmtraitmeansem['sem'][Pmtraitmeansem['Trait']==trait].iloc[0]
    
    axymax=max([Pf_mean,F1_mean,Pm_mean])+max([Pf_sem,F1_sem,Pm_sem])
    axymin=min([Pf_mean,F1_mean,Pm_mean])-max([Pf_sem,F1_sem,Pm_sem])
    ax.set(ylim=(axymin,axymax))      
    #ax.legend(loc='upper right')
    ax.set(xlabel='Variety', ylabel=trait)
    ax.get_legend().remove()
    ax.axhline(mpv, color="gray")
    ax.text(1.02, mpv+0.1*(axymax-axymin), 'MPV', va='center', ha="left",
            bbox=dict(facecolor="w",alpha=0.5),
            transform=ax.get_yaxis_transform())
    ax.text(1.02, mpv, mpv.round(2), va='center', ha="left",
            bbox=dict(facecolor="w",alpha=0.5),
            transform=ax.get_yaxis_transform())
    ax.text(-0.08, 1.08, 'a=MPV-'+ str(Pf_n) + '='
            + str((mpv-Pf_mean).round(2)) , va='center', ha="left",
            bbox=dict(facecolor="w",alpha=0.5),
            transform=ax.transAxes)
    ax.text(0.78, 1.08, 'd='+ str(F1_n) + '-MPV=' 
            + str((F1_mean-mpv).round(2)) , va='center', ha="left",
            bbox=dict(facecolor="w",alpha=0.5),
            transform=ax.transAxes)
    ax.text(-0.08, -0.12, '|d/a|=|'+ str((F1_mean-mpv).round(2))  + '/'
            + str((mpv-Pf_mean).round(2)) + '|=' 
            + str(abs((F1_mean-mpv) /(mpv-Pf_mean)).round(2))
            , va='center', ha="left",
            bbox=dict(facecolor="w",alpha=0.5),
            transform=ax.transAxes)
    if abs((F1_mean-mpv)/(mpv-Pf_mean))<0.2:
        ax.text(0.58, -0.12, 'additive(|d/a|<0.2)'
            , va='center', ha="left",
            bbox=dict(facecolor="w",alpha=0.5),
            transform=ax.transAxes)
    if abs((F1_mean-mpv)/(mpv-Pf_mean))>=0.2 and abs(
            (F1_mean-mpv)/(mpv-Pf_mean))<0.8:
        ax.text(0.58, -0.12, 'partial dominance(0.2 ≤|d/a|<0.8)'
            , va='center', ha="left",
            bbox=dict(facecolor="w",alpha=0.5),
            transform=ax.transAxes)
    if abs((F1_mean-mpv)/(mpv-Pf_mean))>=0.8 and abs(
            (F1_mean-mpv)/(mpv-Pf_mean))<1.2:
        ax.text(0.57, -0.12, 'complete dominance(0.8≤|d/a|<1.2)'
            , va='center', ha="left",
            bbox=dict(facecolor="w",alpha=0.5),
            transform=ax.transAxes)
    if abs((F1_mean-mpv)/(mpv-Pf_mean))>=1.2:
        ax.text(0.58, -0.12, 'overdominance(|d/a|>=1.2)'
            , va='center', ha="left",
            bbox=dict(facecolor="w",alpha=0.5),
            transform=ax.transAxes)
    ax.text(0.02, 0.96, 'MPH=('+ str(F1_n)+'-MPV)/MPV*100%'  + '='
            + str(((F1_mean-mpv)/mpv*100).round(2)) + '$\%$'
            , va='center', ha="left",
            bbox=dict(facecolor="w",alpha=0.5),
            transform=ax.transAxes)
    ax.figure.savefig(trait+'.pdf')              
    ax.clear()