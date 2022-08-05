# -*- coding: utf-8 -*-
"""
Created on Thu Aug  4 13:49:41 2022
Exemplo de como interpolar um conjunto de dados dentro dos
límites de shapefile
author: Eduardo Fernandes Henriques
Referencia
https://basemaptutorial.readthedocs.io/en/latest/clip.html#the-code
"""



import numpy as np
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
from numpy.random import uniform, seed
from mpl_toolkits.basemap import Basemap
from matplotlib.path import Path
from matplotlib.patches import PathPatch
import numpy
import shapefile

fig = plt.figure()
ax = fig.add_subplot(111)
#Lê um shp com as bacias do sistema cantareira
sf = shapefile.Reader("C:/shape_file/shape_Sub-bacias_cantareira/bacias.shp"   )

for shape_rec in sf.shapeRecords():
    x=shape_rec.record[1]
    print(x) #Imprime quais bacias fazem parte do shapefile
    if (shape_rec.record[1] == 'Bacia do Jaguari'):        
        vertices = []
        codes = []
        pts = shape_rec.shape.points
        prt = list(shape_rec.shape.parts) + [len(pts)]
        for i in range(len(prt) - 1):
            for j in range(prt[i], prt[i+1]):
                vertices.append((pts[j][0], pts[j][1]))
            codes += [Path.MOVETO]
            codes += [Path.LINETO] * (prt[i+1] - prt[i] -2)
            codes += [Path.CLOSEPOLY]
        clip = Path(vertices, codes)
        clip = PathPatch(clip, transform=ax.transData)



m = Basemap(llcrnrlon=-46.4,
    llcrnrlat=-22.92,
    urcrnrlon=-46.1,
    urcrnrlat=-22.7,
    resolution = None, 
    projection = 'cyl')


# Define os dados aleatoriamente
seed(1)
npts = 400
x = uniform(-46.4,-46.1,npts)
y = uniform(-22.92,-22.7,npts)
#Calcula a função
z=  (-(np.sin(x*0.01  )+y) -23)*100


# Constroi o Grid.
xi = np.linspace(-46.4,-46.1,100)
yi = np.linspace(-22.92,-22.7,100)

zi = griddata((x, y), z, (xi[None,:], yi[:,None]), method='cubic')
# contour the gridded data, plotting dots at the randomly spaced data points.
cs = plt.contourf(xi,yi,zi,15,cmap=plt.cm.jet)

valores_bar= np.round ( np.linspace(13.5, 37,9),  decimals=0)
cb=plt.colorbar(   ) #  draw colorbar
cb.ax.set_ylabel('Temperatura ºC', rotation=270,labelpad=12   )
cb.set_ticks(ticks=valores_bar, ticklabels=valores_bar  )

# plot data points.
plt.scatter(x,y,marker='o',c='b',s=5)
plt.xlim(-46.4,-46.2)
plt.ylim(-22.92,-22.775)
#Define uma escala específica em x
xticks= np.linspace(-46.4,-46.2 ,8)
ticklabels = np.round(xticks,       decimals=2 )
plt.xticks(xticks,  ticklabels )

plt.title('Resultado da interpolação com (%d pontos)' % npts)
#Realiza o preenchimento apenas no limite do shapefile
for contour in cs.collections:
        contour.set_clip_path(clip)
#Plota o contorno do shapefile
for shape in sf.shapeRecords():
    if (shape.record[1] == 'Bacia do Jaguari'):
        for i in range(len(shape.shape.parts)):
            i_start = shape.shape.parts[i]
            if i==len(shape.shape.parts)-1:
                i_end = len(shape.shape.points)
            else:
                i_end = shape.shape.parts[i+1]
            x = [i[0] for i in shape.shape.points[i_start:i_end]]
            y = [i[1] for i in shape.shape.points[i_start:i_end]]
            plt.plot(x,y,c="black")                  
            

plt.show()




