#Exemplo simples para ler e plotar dados em formato netCDF4 com python 
#Testado no Ubunto 15 com python 3.4.3 
#Exemplo 1
#http://polar.ncep.noaa.gov/waves/examples/usingpython.shtml

#Defindo os modulos necessários
from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
import netCDF4


plt.figure()

# Configurando a URL para acessor o servidor de dados.

mydate='20151123'
url='http://nomads.ncep.noaa.gov:9090/dods/wave/nww3/nww3'+ \
    mydate+'/nww3'+mydate+'_00z'

#Extraindo a altura significativa de onda e swell

file = netCDF4.Dataset(url)
lat  = file.variables['lat'][:]
lon  = file.variables['lon'][:]
data = file.variables['htsgwsfc'][1,:,:]
file.close()


# Plotagem do campo uando Basemap.  Define os limites com base nos 
#valores fornecidos

m=Basemap(projection='mill',lat_ts=10,llcrnrlon=lon.min(), \
  urcrnrlon=lon.max(),llcrnrlat=lat.min(),urcrnrlat=lat.max(), \
  resolution='c')

#Convertendo os valores de lat/lon para as projeções de x/y

x, y = m(*np.meshgrid(lon,lat))

#Plotagem do compo usando a rotina pcolormesh
# set the colormap to jet.

m.pcolormesh(x,y,data,shading='flat',cmap=plt.cm.jet)
m.colorbar(location='right')

#Adicionado a linha de costa e limites dos eixos

m.drawcoastlines()
m.fillcontinents()
m.drawmapboundary()
m.drawparallels(np.arange(-90.,120.,30.),labels=[1,0,0,0])
m.drawmeridians(np.arange(-180.,180.,60.),labels=[0,0,0,1])

#Adicionando a barra de cor e titulo e finalmente mostrando o plot
#Add a colorbar and title, and then show the plot.

plt.title('Example 1: NWW3 Significant Wave Height from NOMADS')
plt.show()
