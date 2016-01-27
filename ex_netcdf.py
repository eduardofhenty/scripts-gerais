import netCDF4 
import time
import numpy
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
>>> # append along two unlimited dimensions by assigning to slice.
>>> nlats = len(rootgrp.dimensions['lat'])
>>> nlons = len(rootgrp.dimensions['lon'])
>>> print 'temp shape before adding data = ',temp.shape
temp shape before adding data =  (0, 0, 73, 144)

>>> from numpy.random import uniform
>>> temp[0:5,0:10,:,:] = uniform(size=(5,10,nlats,nlons))
>>> print 'temp shape after adding data = ',temp.shape
temp shape after adding data =  (6, 10, 73, 144)
>>>
>>> # levels have grown, but no values yet assigned.
>>> print 'levels shape after adding pressure data = ',levels.shape
levels shape after adding pressure data =  (10,)



