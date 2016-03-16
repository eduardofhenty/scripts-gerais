import netCDF4 
import time
import numpy
from numpy.random import uniform
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt


rootgrp = netCDF4.Dataset('test.nc', 'w', format='NETCDF4')
print (rootgrp.data_model)

#Inicialmente definindo a dimensão das variaveis
level = rootgrp.createDimension('level', None)
time = rootgrp.createDimension('time', None)
lat = rootgrp.createDimension('lat', 73)#73 e 288
lon = rootgrp.createDimension('lon', 144)

#Imprime um dicionario
print (rootgrp.dimensions)

#Imprimindo se é ou não limitado, nome, tamanho 
for dimobj in rootgrp.dimensions.values():
    print (dimobj)
    
#Criando as variaveis    
times = rootgrp.createVariable('time','f8',('time',))
levels = rootgrp.createVariable('level','i4',('level',))
latitudes = rootgrp.createVariable('latitude','f4',('lat',))
longitudes = rootgrp.createVariable('longitude','f4',('lon',))

# two dimensions unlimited.
temp = rootgrp.createVariable('temp','f4',('time','level','lat','lon',))    
print(type(times))

#Atributo em em um  arquivo netCDF
#Há dois tipos de atributos em um arquivo netCDF: global e variavel
#Atributo global fornece informação sobre  um grupo ou sobre o conjunto de dados
#Atriibutos de variaveis definem atributos assumidos por variaveis. Esses
print("Aqui")
#atributos podem ser strings, numeros ou sequencias
print(rootgrp.ncattrs)

rootgrp.description = 'bogus example script'
rootgrp.source = 'netCDF4 python module tutorial'
latitudes.units = 'degrees north'
longitudes.units = 'degrees east'
levels.units = 'hPa'
temp.units = 'K'
times.units = 'hours since 0001-01-01 00:00:00.0'
times.calendar = 'gregorian'


#Escrendo dados e recuperando dados de uma variavel netCDF

lats =  numpy.arange(-90,91,2.5)
lons =  numpy.arange(-180,180,2.5)
latitudes[:] = lats
longitudes[:] = lons
print ("latitudes =\n",latitudes[:])

#Diferentemente de objetos arrays do Numpy, as variaveis netCDF com dimensão não limitada irão crescer ao longo dessas dimensões se for selecionado dados fora desse indice.
# append along two unlimited dimensions by assigning to slice.
nlats = len(rootgrp.dimensions['lat'])
nlons = len(rootgrp.dimensions['lon'])
print ("formato de temp antes de adicionar dados =",temp.shape)


temp[0:5,0:10,:,:] = uniform(size=(5,10,nlats,nlons))
print ('formato de temp depois de adicionar dados=',temp.shape)


# levels have grown, but no values yet assigned.
print ('formato de niveis depois de adicionar dados de pressão=',levels.shape)

levels[:] =  [1000.,850.,700.,500.,300.,250.,200.,150.,100.,50.]

#Como extrair dados 
tempdat = temp[::2, [1,3,6], lats>0, lons>0]
#Será extraido o tempo nos indices 0,2 e 4, a pressão nos níveis 850, 500 e 200 hPa e
#todas as latitudes no HN e longitudes no hemisfério Ocidental
print ('shape of fancy temp slice = ',tempdat.shape)


####Plotando 
import numpy as np
lat  = rootgrp.variables['latitude'][:]
lon  = rootgrp.variables['longitude'][:]
data=rootgrp.variables['temp'][0,0,:,:]

m=Basemap(projection='mill',lat_ts=10,llcrnrlon=lon.min(), \
  urcrnrlon=lon.max(),llcrnrlat=lat.min(),urcrnrlat=lat.max(), \
  resolution='c')

# convert the lat/lon values to x/y projections.

x, y = m(*np.meshgrid(lon,lat))

# plot the field using the fast pcolormesh routine 
# set the colormap to jet.

m.pcolormesh(x,y,data,shading='flat',cmap=plt.cm.jet)
m.colorbar(location='right')

# Add a coastline and axis values.

m.drawcoastlines()
m.fillcontinents()
m.drawmapboundary()
m.drawparallels(np.arange(-90.,120.,30.),labels=[1,0,0,0])
m.drawmeridians(np.arange(-180.,180.,60.),labels=[0,0,0,1])

# Add a colorbar and title, and then show the plot.

plt.title('Example 1: NWW3 Significant Wave Height from NOMADS')
plt.show()

