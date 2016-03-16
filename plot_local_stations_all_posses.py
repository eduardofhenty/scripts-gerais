#Script para plotagem dos locais das estações do ICA,CEMADEN e DAEE com zoom no sistema Cantareira

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap
import os

def plot_local_stations (dado):   
    
    #Plotagem do campo usando o Basemap. Inicia a projeção do mapa usando os limites min e max dos proprios dados
    
    llcrnrlon=-46.27
    urcrnrlon=-46.22
    llcrnrlat=-22.90
    urcrnrlat=-22.83
    
    #x.range <- as.numeric(c(-46.5, -46))  # min/max longitude of the interpolation area
  #y.range <- as.numeric(c(-23., -22.75))  # min/max latitude of the interpolation area
  
    
   
    
    m=Basemap(projection='mill',lat_ts=10,llcrnrlon=llcrnrlon, \
    urcrnrlon=urcrnrlon,llcrnrlat=llcrnrlat,urcrnrlat=urcrnrlat, \
    resolution='i',area_thresh=10000)
    local_shapefile='/mnt2/dado/local das estações/shapefile_posses/basin'
    nome_shapefile='basin'
    m.readshapefile(local_shapefile,nome_shapefile,linewidth=1,color='b')
    
    
    #Dados ANA
    lat=dado[0:5,1]
    lon=dado[0:5,0]    
    print(lat)    
    x,y = m(lon, lat)       
    m.plot(x, y, 'bo', markersize=5,label='ANA')
    
    
    #Dados LCB_IAG
    lat=dado[6:17,1]
    lon=dado[6:17,0]
    x,y = m(lon, lat)
    names=["C04","C05","C06","C07","C08","C09","C10","C11","C12","C13","C14","C15"]
    print(len(names))
    for i in range(len(names)-1):
      print(i)
      plt.text(x[i], y[i], names[i], va="top", family="monospace", weight="bold")
    
    
    x,y = m(lon, lat)
    m.plot(x,y , 'ro', markersize=5,label='WXT-LCB')
    #Dados do DAEE
    lat=dado[18:22,1]
    lon=dado[18:22,0]
    x,y = m(lon, lat)
    m.plot(x,y , 'go', markersize=5,label='Umidade do solo-LCB')    
    
    lat=dado[:,1]
    lon=dado[:,0]    
    print(len(lat))
    
        
    plt.xlabel('xlabel', fontsize=18)
    
    

    m.drawstates(linewidth=1., linestyle='dotted', color='k', antialiased=1)
    
    #m.drawmapboundary()
    m.drawparallels(np.arange(llcrnrlat, urcrnrlat,.02),labels=[1,0,0,0])
    m.drawmeridians(np.arange( llcrnrlon, urcrnrlon,.03),labels=[0,0,0,1])
        
    titulo='Localização das estações '
    plt.title(titulo)
   
    
    fig_out='/home/eduardo/dado/fig1/'+'local das estações zoom em Posses' + '.png'
    
    #Coloca a legenda abaixo do gráfico com sombreado e 'tamanho' igual a 1 para 
    #os simbolos
    plt.legend(loc='center left', bbox_to_anchor=(1., 0.5),
          fancybox=True, shadow=True,numpoints=1)
    
    #Opção bbox_inches evita que a legenda seja cortada na hora de salvar a figura
    plt.savefig(fig_out,bbox_inches='tight' )   
    plt.show()
    plt.close()

    
path_fig='/mnt2/dado/fig1'
arq1='/mnt2/dado/local das estações/Informacao_Estacoes_Extrema.csv'


#Verifica e cria o diretório
os.makedirs(path_fig, exist_ok=True)



dado =np.loadtxt(arq1,delimiter=";")

plot_local_stations (dado)

print( dado.shape)
print(dado)


    

    









