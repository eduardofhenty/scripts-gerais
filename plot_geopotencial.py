#Script para gerar plotagem do tipo contour com dados de geopotencial em 1000 hPa
import pygrib
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from mpl_toolkits.basemap import Basemap
import os

#Função para gerar gráficos do tipo contorno. 
def gera_contour (msg,tipo):   

    lat,lon = msg.latlons()
    data=msg.values  


    #Plotagem do campo usando o Basemap. Inicia a projeção do mapa usando os limites min e max dos proprios dados

    m=Basemap(projection='mill',lat_ts=10,llcrnrlon=lon.min(), \
    urcrnrlon=lon.max(),llcrnrlat=lat.min(),urcrnrlat=lat.max(), \
    resolution='c')

    #Convertendo os valores de lat/lon para as projeções de x/y
    x, y = m(lon,lat)

        
    #Opção colors define a cor da linha. Nesse caso preto.
    #
    cs=m.contour (x,y ,data,linewidth=5,colors='k' )
    #inline estabele que os rotulos são desenhados através das linhas
    #fmt controla o formato do número
    plt.clabel(cs, fontsize=10, inline=1,fmt='%.1f') 

    #Adicionado a linha de costa e limites dos eixos

    m.drawcoastlines()
    #m.fillcontinents()
    #m.drawmapboundary()
    m.drawparallels(np.arange(-90.,120.,30.),labels=[1,0,0,0])
    m.drawmeridians(np.arange(-180.,180.,60.),labels=[0,0,0,1])
      
   
    plt.title('Altura do '+tipo+ ' em 500 hPa  em 1 jan 2016')
   
    
    fig_out='/home/eduardo/dado/fig1/'+'Altura do geopotencial '+tipo+' _janeiro_2016 v1' + '.png'
    
    plt.savefig(fig_out)   
    plt.show()
    plt.close()


path ='/home/eduardo/dado/grib/'
path_fig='/home/eduardo/dado/fig1/'
#Verifica e cria o diretório
os.makedirs(path_fig, exist_ok=True)
name_file=path+'pgb.anl.2016010100.grib'

gr = pygrib.open(name_file)  

msg=gr[6]#seleciona a variavel geopotencial em 500 hPa


gera_contour(msg,"geopotencial")


   

