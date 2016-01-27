 #Exemplo simples para ler e plotar dados em formato grib2 com python 
 #Testado no Ubunto 15 com python 3.4.3
 #Original em:
 #http://polar.ncep.noaa.gov/waves/examples/usingpython.shtml
 #Download do grib2
 #ftp://polar.ncep.noaa.gov/arc/nfcens_eval/nomads.ncep.noaa.gov/pub/data/nccf/com/wave/para/wave.20111022/multi_1.at_10m.t00z.f000.grib2
 

#Defindo os modulos necessários

import pygrib
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap

plt.figure()

grib='multi_1.at_10m.t00z.f000.grib2';
grbs=pygrib.open(grib)

#Neste exemplo será usado o campo de altura siginificativo de onda. Em python do indice começa no zero

grb = grbs.select(name='Significant height of wind waves')[0]
data=grb.values
lat,lon = grb.latlons()


#Plotagem do campo usando o Basemap. Inicia a projeção do mapa usando os limites min e max dos proprios dados

m=Basemap(projection='mill',lat_ts=10,llcrnrlon=lon.min(), \
urcrnrlon=lon.max(),llcrnrlat=lat.min(),urcrnrlat=lat.max(), \
resolution='c')

#Convertendo os valores de lat/lon para as projeções de x/y

x, y = m(lon,lat)

#Next, plot the field using the fast pcolormesh routine and set the colormap to jet.

cs = m.pcolormesh(x,y,data,shading='flat',cmap=plt.cm.jet)

#Adicionado a linha de costa e limites dos eixos

m.drawcoastlines()
m.fillcontinents()
m.drawmapboundary()
m.drawparallels(np.arange(-90.,120.,30.),labels=[1,0,0,0])
m.drawmeridians(np.arange(-180.,180.,60.),labels=[0,0,0,1])

#Adicionando a barra de cor e titulo e finalmente mostrando o plot
#Add a colorbar and title, and then show the plot.

plt.colorbar(cs,orientation='vertical')
plt.title('Example 2: NWW3 Significant Wave Height from GRiB')
plt.show()

