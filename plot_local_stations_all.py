#Script para plotagem dos locais das estações do ICA,CEMADEN e DAEE
import pygrib
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap
import os

def plot_local_stations (dado_cem,dado_iac,dado_daee):   
    
    #Plotagem do campo usando o Basemap. Inicia a projeção do mapa usando os limites min e max dos proprios dados
    lat=dado_cem[:,0]
    lon=dado_cem[:,1]
    
    llcrnrlon=np.rint(lon.min())-1
    urcrnrlon=np.rint(lon.max())+1
    llcrnrlat=np.rint(lat.min())-1
    urcrnrlat=np.rint(lat.max())+1
    
    m=Basemap(projection='mill',lat_ts=10,llcrnrlon=llcrnrlon, \
    urcrnrlon=urcrnrlon,llcrnrlat=llcrnrlat,urcrnrlat=urcrnrlat, \
    resolution='i',area_thresh=10000)

    x,y = m(lon, lat)
       
    m.plot(x, y, 'bo', markersize=5,label='CEMADEN')
    
    #Dados IAC
    lat=dado_iac[:,0]
    lon=dado_iac[:,1]
    x,y = m(lon, lat)
    m.plot(x,y , 'ro', markersize=5,label='IAC')
    #Dados do DAEE
    lat=dado_daee[:,0]
    lon=dado_daee[:,1]
    x,y = m(lon, lat)
    m.plot(x,y , 'go', markersize=5,label='DAEE')
    
      
        
    plt.xlabel('xlabel', fontsize=18)
    #plt.axis()
   
        #Adicionado a linha de costa e limites dos eixos

    m.drawcoastlines()
    m.fillcontinents()
    m.drawstates(linewidth=1.0, linestyle='solid', color='k', antialiased=1)
    
    #m.drawmapboundary()
    m.drawparallels(np.arange(llcrnrlat, urcrnrlat,2.),labels=[1,0,0,0])
    m.drawmeridians(np.arange( llcrnrlon, urcrnrlon,2.),labels=[0,0,0,1])
    
    
    
    titulo='Localização das estações '
    plt.title(titulo)
   
    
    fig_out='/home/eduardo/dado/fig1/'+'local das estações' + '.png'
    
    #Coloca a legenda abaixo do gráfico com sombreado e 'tamanho' igual a 1 para 
    #os simbolos
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
          fancybox=True, shadow=True,numpoints=1)
    
    #Opção bbox_inches evita que a legenda seja cortada na hora de salvar a figura
    plt.savefig(fig_out,bbox_inches='tight' )   
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

plot_local_stations (dado_cem,dado_iac,dado_daee)









