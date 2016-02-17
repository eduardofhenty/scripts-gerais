#Script para plotagem de dados de reanálise
#Dados de reanalise 2 http://rda.ucar.edu/datasets/ds091.0/#!description
#Formato dos arquivos grib1
#Script por Eduardo Fernandes Henriques em 17 /02/2016
#

import pygrib
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap
import os

#Função para plotagem necessita de um obejto grib, o nome do arquivo grib
def gerafig (gr,file):
    #Escolhido o campo de temperatura em 1000 hPa
    #Posição determinada a partir do inventário do grib
    msg=gr[69]
    data=msg.values-273 #Convertendo de k para Celsius
    lat,lon = msg.latlons()
    ano=file[8:12]
    mes=file[12:14]
    dia=file[14:16]
    hora=file[16:18]
    lista=[ano,'-',mes,'-',dia,' ',hora,':','00']
    data_hora=''.join(lista)

    print(data_hora)


    #Plotagem do campo usando o Basemap. Inicia a projeção do mapa usando os limites min e max dos proprios dados

    m=Basemap(projection='mill',lat_ts=10,llcrnrlon=lon.min(), \
    urcrnrlon=lon.max(),llcrnrlat=lat.min(),urcrnrlat=lat.max(), \
    resolution='c')

    #Convertendo os valores de lat/lon para as projeções de x/y
    x, y = m(lon,lat)

    cs = m.pcolormesh(x,y,data,shading='flat',cmap=plt.cm.jet,vmin=-24,vmax=40)

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
    
    fig_out='/home/eduardo/dado/fig/'+'temperatura'+data_hora + '.png'
    plt.savefig(fig_out)    
    plt.close()
    
    
    #Função para ler o arquivo grib, necessita do caminho completo
def le_grib (name_file):
    gr = pygrib.open(name_file)  
    return (gr)
    


#Defindo os diretórios com a pasta com arquivos grib e da pasta de saída das figs
path ='/home/eduardo/dado/grib/'
path_fig='/home/eduardo/dado/fig/'
#Verifica e cria o diretório
os.makedirs(path_fig, exist_ok=True)

list_files=os.listdir(path)

for file in list_files:    
    name_file=path+file
    print(name_file)
    gr=le_grib(name_file)
    gerafig(gr,file)
    
    
    
    













   
