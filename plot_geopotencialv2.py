#Script para gerar plotagem do tipo contorno sombreado com dados de geopotencial em 1000 hPa
import pygrib
import matplotlib.pyplot as plt
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

      
        
    cs=m.contourf (x,y ,data,origin='lower')
    #Plota uma barra com escala de cores
    #Opção pad controla a distância da barra em relação ao gráfico
    cbar = plt.colorbar(cs,pad=0.04)
    

    #plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
     #      ncol=2, mode="expand", borderaxespad=0.)
    #plt.axis()
   
        #Adicionado a linha de costa e limites dos eixos

    m.drawcoastlines()
    #m.fillcontinents()
    #m.drawmapboundary()
    m.drawparallels(np.arange(-90.,120.,30.),labels=[1,0,0,0])
    m.drawmeridians(np.arange(-180.,180.,60.),labels=[0,0,0,1])
    cbar.ax.set_ylabel('Altura do geopotencial (mgp)',rotation=270)
    plt.xlabel('xlabel', fontsize=18)
   
    plt.title('Altura do '+tipo+ ' em 500 hPa  em 1 jan 2016')
   
    
    fig_out='/home/eduardo/dado/fig1/'+'Altura do geopotencialv2 '+tipo+' _janeiro_2016' + '.png'
    
    plt.savefig(fig_out)   
    plt.show()
    plt.close()


path ='/home/eduardo/dado/grib/'
path_fig='/home/eduardo/dado/fig1/'
#Verifica e cria o diretório
os.makedirs(path_fig, exist_ok=True)
name_file=path+'pgb.anl.2016010100.grib'

gr = pygrib.open(name_file)  

msg=gr[6]


gera_contour(msg,"geopotencial")