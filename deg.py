#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 18:09:32 2021

@author: stefan
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 23 12:59:32 2021

@author: stefan
"""
import matplotlib.pyplot as plt
from matplotlib_venn import venn3
import pandas as pd
import numpy as np
from scipy.stats import ttest_ind
data=pd.read_csv("deg.csv")

Pf_n=data['P_f name'][1]
F1_n=data['F_1 name'][1]
Pm_n=data['P_m name'][1]


PfF1deg=0
PmF1deg=0
PfPmdeg=0
tdeg=0

Pfgenemeansem=pd.DataFrame(columns=["Gene", "mean","sem"])
F1genemeansem=pd.DataFrame(columns=["Gene", "mean","sem"])
Pmgenemeansem=pd.DataFrame(columns=["Gene", "mean","sem"])
for gene in data['Gene'].unique():
    #calculates means and sems for each gene
    Pfgenemeansem=Pfgenemeansem.append({'Gene': gene,
                       'mean': data['P_f value'][data['Gene']==gene].mean(),
    'sem': data['P_f value'][data['Gene']==gene].sem()},
    ignore_index=True)
    F1genemeansem=F1genemeansem.append({'Gene': gene,
                       'mean': data['F_1 value'][data['Gene']==gene].mean(),
    'sem': data['F_1 value'][data['Gene']==gene].sem()},
    ignore_index=True)
    Pmgenemeansem=Pmgenemeansem.append({'Gene': gene,
                       'mean': data['P_m value'][data['Gene']==gene].mean(),
    'sem': data['P_m value'][data['Gene']==gene].sem()},
    ignore_index=True)
    #independent t-tests test whether the F1 has differently expressed genes
    if ttest_ind(data['P_f value'][data['Gene']==gene],
           data['P_m value'][data['Gene']==gene])[1]<0.05 and ttest_ind(
                   data['P_f value'][data['Gene']==gene],
           data['F_1 value'][data['Gene']==gene])[1]<0.05 and ttest_ind(
                   data['F_1 value'][data['Gene']==gene],
           data['P_m value'][data['Gene']==gene])[1]<0.05:
        tdeg+=1
    if ttest_ind(data['P_f value'][data['Gene']==gene],
           data['F_1 value'][data['Gene']==gene])[1]<0.05:
        PfF1deg+=1
    if ttest_ind(data['F_1 value'][data['Gene']==gene],
           data['P_m value'][data['Gene']==gene])[1]<0.05:
        PmF1deg+=1
    if ttest_ind(data['P_f value'][data['Gene']==gene],
           data['P_m value'][data['Gene']==gene])[1]<0.05:
        PfPmdeg+=1
#for number of genes
nog=data['Gene'].unique().size
venn3(subsets = (nog, nog, PfPmdeg,nog,PfF1deg,PmF1deg,tdeg),
      set_labels = (Pf_n, Pm_n,F1_n))
plt.savefig('deg.pdf',bbox_inches='tight')  