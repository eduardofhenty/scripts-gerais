from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
from scipy.interpolate import griddata
from scipy.interpolate import interp2d 

id,x,y,z=np.loadtxt(fname='/home/eduardo/Script/scripts-gerais/dados_mes/all_por_mes/prec_all_2014-01-01.txt',unpack=True)
y= y-360


#lat, lon = np.meshgrid(x, y)
print(x.min())
print(x.max())
print(y.min())
print(y.max())

print(np.floor(x.min()))
print(np.ceil (x.max()))
print(np.floor(y.min()))
print(np.ceil (y.max()))

xmin = np.floor(x.min())
xmax = np.floor(x.max())
ymin = np.floor(y.min())
ymax = np.floor(y.max())

nx = int(np.absolute(xmax -xmin)/0.5)*1j
ny = int( np.absolute(ymax -ymin)/0.5)*1j

#z = interpolate.interp2d(grid_x, grid_y, z, kind='cubic')


print("valor de nx e ny ")
print(nx);print(ny)



#grid_x, grid_y = np.mgrid[x.min():x.max():20j, y.min():y.max():20j]
grid_x, grid_y = np.mgrid[xmin:xmax:nx, ymin:ymax:ny]

#nx, ny = (0.5, 0.5)
#x = np.arange(x.min(), x.max(), nx)
#y = np.arange(y.min(), y.max(), ny)
#grid_x, grid_y = np.meshgrid(x, y)

print(grid_x)
print(type(grid_x))
print(grid_x.shape)

print("Numero de pontos")
#print(grid_x)


points = (x,y)
values =z
grid_z0 = griddata(points, values, (grid_x, grid_y), method='nearest')
grid_z1 = griddata(points, values, (grid_x, grid_y), method='linear')


grid_z2 = interpolate.interp2d(grid_x, grid_y, z, kind='cubic')
#grid_z2 = griddata(points, values, (grid_x, grid_y), method='cubic',rescale="True")

plt.subplot(221)

plt.plot(x, y, 'k.', ms=2)
plt.title('Original')
plt.subplot(222)
#plt.imshow(grid_z0.T, extent=(grid_x.min(),grid_x.max(),grid_y.min(),grid_y.max()), origin='lower')
plt.imshow(grid_z0.T, extent=(-26,-19,-54,-42),
           origin='lower',aspect="auto")
plt.colorbar()
plt.title('Nearest')
plt.subplot(223)
plt.imshow(grid_z1.T, extent=(-26,-19,-54,-42), origin='lower',aspect="auto")
#plt.contour(grid_x,grid_y,grid_z0,15,linewidths=0.5,colors='k')
plt.colorbar()
plt.title('Linear')
plt.subplot(224)
plt.imshow(grid_z2.T, extent=(-26,-19,-54,-42), origin='lower',aspect="auto")
plt.title('Cubic')
plt.colorbar()
plt.gcf().set_size_inches(6, 6)
plt.show()





