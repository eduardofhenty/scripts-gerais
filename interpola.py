# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 16:43:47 2016

@author: eduardo
"""

import numpy as np
from scipy.interpolate import Rbf
import matplotlib.pyplot as plt
from matplotlib import cm
namef="/home/eduardo/Downloads/nprec_all_2014-01-01.txt"
dado = np.loadtxt(namef,delimiter  =","      )
x=dado[:,0]
y=dado[:,1]
z=dado[:,2]


xmin=dado[:,0].min()
xmax=dado[:,0].max()
ymin=dado[:,1].min()
ymax=dado[:,1].max()

np.mgrid[xmin:xmax:10,  ymin:ymax:10 ]

tx= np.linspace(xmin,xmax,10 )
ty= np.linspace(ymin,ymax,10 )

XI,YI=np.meshgrid(tx,ty)
rbf=Rbf(x,y,z,epsilon=0.5)

ZI=rbf(XI,YI)
plt.pcolor(XI,YI,ZI,cmap=cm.jet)
plt.scatter(x,y,100,z,cmap=cm.jet)
plt.colorbar()
plt.show()