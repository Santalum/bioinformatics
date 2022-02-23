# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 20:49:24 2018

@author: stefan
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy.special import erf#,erfinv

#Sources: Ellis and Roberts, 1980; http://data.kew.org/sid/viability/
#A.S. Cromarty; Design of Seed Storage Facilities for Genetic Conservation 1982
#For rice the following species specific oil content can be used:
D_0 = 0.018
#For rice the following species specific constant can be used:
Ke=8.668
# The following moisture content constant corresponds with O. sativa:
Cw=5.03
# The universal temperature constants can be used:
Ch=0.0329
Cq=0.000478
# Initial viability of the seed:
Ki=3
#days of storage
dos=250
#Equilibrium Temperature
eT = 20
#Storage temperature
sT = 35.0


#Equilibrium Relative Humidity (eRH)
R1 = 0.4
#Seed moisture content
m1 = ((1-D_0)*np.sqrt(-440*np.log(1-R1))/(1.1+(eT/90)))
sigma=10**(Ke-Cw*np.log10(m1)-Ch*sT-Cq*sT**2)
#Time it takes when 50% of the seeds fail to germinate
p50=Ki*sigma
v1 = []
#Storage in days
for x in range (dos+1):
    #p is equal to the days of storage
    p = x
    probit=Ki-p/sigma
    probability=1/2*(1+erf(probit/np.sqrt(2)))
    v1.append(probability*100)

#Relative humidity
R2 = 0.45
#Seed moisture content
m2 = ((1-D_0)*np.sqrt(-440*np.log(1-R2))/(1.1+(eT/90)))
sigma=10**(Ke-Cw*np.log10(m2)-Ch*sT-Cq*sT**2)
#Time it takes when 50% of the seeds fail to germinate
p50=Ki*sigma
v2 = []
#Storage in days
for x in range (dos+1):
    #p is equal to the days of storage
    p = x
    probit=Ki-p/sigma
    probability=1/2*(1+erf(probit/np.sqrt(2)))
    v2.append(probability*100)

#Relative humidity
R3 = 0.50
#Seed moisture content
m3 = ((1-D_0)*np.sqrt(-440*np.log(1-R3))/(1.1+(eT/90)))
sigma=10**(Ke-Cw*np.log10(m3)-Ch*sT-Cq*sT**2)
#Time it takes when 50% of the seeds fail to germinate
p50=Ki*sigma
v3 = []
#Storage in days
for x in range (dos+1):
    #p is equal to the days of storage
    p = x
    probit=Ki-p/sigma
    probability=1/2*(1+erf(probit/np.sqrt(2)))
    v3.append(probability*100)


#Relative humidity
R4 = 0.55
#Seed moisture content
m4 = ((1-D_0)*np.sqrt(-440*np.log(1-R4))/(1.1+(eT/90)))
sigma=10**(Ke-Cw*np.log10(m4)-Ch*sT-Cq*sT**2)
#Time it takes when 50% of the seeds fail to germinate
p50=Ki*sigma
v4 = []
#Storage in days
for x in range (dos+1):
    #p is equal to the days of storage
    p = x
    probit=Ki-p/sigma
    probability=1/2*(1+erf(probit/np.sqrt(2)))
    v4.append(probability*100)

#Relative humidity
R5 = 0.60
#Seed moisture content
m5 = ((1-D_0)*np.sqrt(-440*np.log(1-R5))/(1.1+(eT/90)))
sigma=10**(Ke-Cw*np.log10(m5)-Ch*sT-Cq*sT**2)
#Time it takes when 50% of the seeds fail to germinate
p50=Ki*sigma
v5 = []
#Storage in days
for x in range (dos+1):
    #p is equal to the days of storage
    p = x
    probit=Ki-p/sigma
    probability=1/2*(1+erf(probit/np.sqrt(2)))
    v5.append(probability*100)


#The following article describes going from probits to probabilities and vice versa:
#https://dc.etsu.edu/cgi/viewcontent.cgi?article=2497&context=etd
#Where the probability can be calculated as:
probability=1/2*(1+erf(Ki/np.sqrt(2)))
#The probit function may be expressed in terms of the inverse error function as:
#probit=np.sqrt(2)*erfinv(2*probability-1)
    
plt.show()
[p1,p2,p3,p4,p5] = plt.plot(v1,'r-',
         v2,'g-',
         v3,'b-',
         v4,'c-',
         v5, 'm-')
plt.ylim(0,100)
plt.xlim(0,dos)
plt.rcParams['font.size']=10
plt.rcParams["figure.figsize"]=[6*1.5,4*1.5]
plt.xlabel('Days of storage')    
plt.ylabel('Germination rate (%)')
plt.title('Germination rate of rice with ' + str(round(probability*100, 1)) + 
          '% initial germination rate stored at ' + str(sT) + '°C' )
plt.axhline(50,color='gray')
plt.text(125,45,'p50',rotation=0)
plt.legend([p1,p2,p3,p4,p5],['eRH of '+ str(round(R1*100, 0)) + '%',
           'eRH of '+ str(round(R2*100, 0)) + '%',
           'eRH of '+ str(round(R3*100, 0)) + '%',
           'eRH of '+ str(round(R4*100, 0)) + '%', 
           'eRH of '+ str(round(R5*100, 0)) + '%'],
            loc='upper right'), #bbox_to_anchor=(0.5, 0., 0.5, 0.5))

plt.show()