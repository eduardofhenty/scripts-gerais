#Exemplo baseado em 
#http://www.himpactwxlab.com/home/how-to-wiki/write-grib2-data-with-pygrib
#http://pt.slideshare.net/arulalan/pygrib-documentation


import pygrib
import pickle
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap
import os





path ='/home/eduardo/dado/grib/'
path_fig='/home/eduardo/dado/fig/'
os.makedirs(path_fig, exist_ok=True)
file="/home/eduardo/dado/grib/pgb.anl.2016010100.grib"
name_file="pgb.anl.2016010100.grib"

list_files=os.listdir(path)
#print(list_files)

gr = pygrib.open(file) 



print('Imprimindo osdados')
print("Valores de temperatura em k ")
print(gr[69]['values'])
msg=gr[69]
#print("Max, Min, Mean ",dado.mean(),dado.max(),dado.min())





#print(msg)
print("Imprimindo as palavras chaves \n")
print(msg.keys())

print("Imprimindo as diferentes latitudes \n")
print(msg['distinctLatitudes'])

print("\nImprimindo as diferentes longitudes \n")
print(msg['distinctLongitudes'])



lats,lons = msg.latlons()
print("latitudes \n")
print(lats)
print("longitudes \n")
print(lons)


#Obtendo os valores
msg_vals = msg.values
print("Valores\n")
print(msg_vals)
print ("Dimensoes da matriz\n")
print(msg_vals.shape)
#Valores máximos e mínimos
print("Imprimindo os valores máximos e mínimos\n")
print ( np.amax(msg_vals),np.amin(msg_vals))

print("Imprimindo a data\n")




ano=name_file[8:12]
mes=name_file[12:14]
dia=name_file[14:16]
hora=name_file[16:18]
lista=[ano,'-',mes,'-',dia,' ',hora,':','00']
data_hora=''.join(lista)

print(data_hora)
data=msg.values-273
lat,lon = msg.latlons()


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
plt.title('Temperatura no nível de 1000 hPa '+data_hora)
#plt.show()
fig_out='/home/eduardo/dado/fig/fig.png'
plt.savefig(fig_out)

   
