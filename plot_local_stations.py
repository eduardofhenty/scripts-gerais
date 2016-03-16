#Script para plotagem dos locais das estações do ICA,CEMADEN e DAEE
import pygrib
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap
import os

def plot_local_stations (dado,tipo):   
    
    #Plotagem do campo usando o Basemap. Inicia a projeção do mapa usando os limites min e max dos proprios dados
    lat=dado[:,0]
    lon=dado[:,1]
    
    llcrnrlon=np.rint(lon.min())-1
    urcrnrlon=np.rint(lon.max())+1
    llcrnrlat=np.rint(lat.min())-1
    urcrnrlat=np.rint(lat.max())+1
    
    m=Basemap(projection='mill',lat_ts=10,llcrnrlon=llcrnrlon, \
    urcrnrlon=urcrnrlon,llcrnrlat=llcrnrlat,urcrnrlat=urcrnrlat, \
    resolution='i',area_thresh=10000)

    x,y = m(lon, lat)
    #m.plot(x, y, 'bo', markersize=5,label='tes')
    m.plot(x, y, 'bo', markersize=5,)
      
        
    plt.xlabel('xlabel', fontsize=18)
    #plt.axis()
   
        #Adicionado a linha de costa e limites dos eixos

    m.drawcoastlines()
    m.fillcontinents()
    m.drawstates(linewidth=1.0, linestyle='solid', color='k', antialiased=1)
    
    #m.drawmapboundary()
    m.drawparallels(np.arange(llcrnrlat, urcrnrlat,2.),labels=[1,0,0,0])
    m.drawmeridians(np.arange( llcrnrlon, urcrnrlon,2.),labels=[0,0,0,1])
    
    
    
    titulo='Localização das estações do '+tipo
    plt.title(titulo)
   
    
    fig_out='/home/eduardo/dado/fig1/'+'local das estações' +tipo + '.png'
    
    #plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    
    plt.savefig(fig_out)   
    plt.show()
    plt.close()
    
path_fig='/home/eduardo/dado/fig1/'
arq1='/mnt2/dado/local das estações/cemaden estacoes.csv'
arq2='/mnt2/dado/local das estações/stations_IAC.csv'
arq3='/mnt2/dado/local das estações/estations_daee.csv'



#Verifica e cria o diretório
os.makedirs(path_fig, exist_ok=True)



dado_cem =np.loadtxt(arq1,delimiter=";")
dado_iac =np.loadtxt(arq2,delimiter=";")
dado_daee=np.loadtxt(arq3,delimiter=";")


plot_local_stations (dado_cem,'CEMADEN')
plot_local_stations (dado_iac,'IAC')
plot_local_stations (dado_daee,'DAEE')








