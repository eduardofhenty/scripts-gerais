#Exemplo retirado de 
#http://docs.scipy.org/doc/scipy/reference/tutorial/interpolate.html
import numpy as np
from scipy.interpolate import griddata
import matplotlib.pyplot as plt

#Definindo uma função 2d
def func(x, y):
   return x*(1-x)*np.cos(4*np.pi*x) * np.sin(4*np.pi*y**2)**2


#Construindo um grid (0,1) x (0,1). O intervalo de 0 a 1  é divido em 100 partes
grid_x, grid_y = np.mgrid[0:1:100j, 0:1:200j]

#Gerando  mil pontos aleatorios em mil linhas por duas colunas
points = np.random.rand(1000, 2)
values = func(points[:,0], points[:,1])


grid_z0 = griddata(points, values, (grid_x, grid_y), method='nearest')
grid_z1 = griddata(points, values, (grid_x, grid_y), method='linear')
grid_z2 = griddata(points, values, (grid_x, grid_y), method='cubic')



plt.subplot(221)
plt.imshow(func(grid_x, grid_y).T, extent=(0,1,0,1), origin='lower')
plt.plot(points[:,0], points[:,1], 'k.', ms=1)
plt.title('Original')
plt.subplot(222)
plt.imshow(grid_z0.T, extent=(0,1,0,1), origin='lower')
plt.title('Nearest')
plt.subplot(223)
plt.imshow(grid_z1.T, extent=(0,1,0,1), origin='lower')
plt.title('Linear')
plt.subplot(224)
plt.imshow(grid_z2.T, extent=(0,1,0,1), origin='lower')
plt.title('Cubic')
plt.gcf().set_size_inches(6, 6)
plt.show()







