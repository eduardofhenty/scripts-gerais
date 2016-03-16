#Script para plotar  média, máximo e mínimo do mês de 
#janeiro de 2016 da temperatura de arquivos de reanálise 2 
import pygrib
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap
import os

#Função para gerar gráficos. Necessita do caminho completo
#do arquivo,a matriz com os dados e tipo de dado em formato de string
def gera_graf (file,res,tipo):
#Escolhido o campo de temperatura em 1000 hPa
    #Posição determinada a partir do inventário do grib
    gr = pygrib.open(file)  
    msg=gr[69]

    lat,lon = msg.latlons()
    data=res  


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
    plt.title('Temperatura '+tipo+ ' em 1000 hPa  em jan 2016')
    #plt.show()
    
    fig_out='/home/eduardo/dado/fig1/'+'temperatura '+tipo+' _janeiro_2016' + '.png'
    plt.savefig(fig_out)    
    plt.close()


    
#Classe com opção de média, máximo ou mínimo para plotagem
class plot (object):
   
    def media(file,dado):
        res=np.mean(dado,axis=0) 
        tipo="média"
        gera_graf(file,res,tipo)
        return 
    def max(file,dado):
        res=np.max(dado,axis=0)
        tipo="máxima"
        gera_graf(file,res,tipo)
        return 
    def min(file,dado):
        res=np.min(dado,axis=0)        
        tipo="mínima"
        gera_graf(file,res,tipo)
        return 
    
    

#Defindo os diretórios com a pasta com arquivos grib e da pasta de saída das figs
path ='/home/eduardo/dado/grib/'
path_fig='/home/eduardo/dado/fig1/'
#Verifica e cria o diretório
os.makedirs(path_fig, exist_ok=True)

list_files=os.listdir(path)


dado=[]
for file in list_files:    
   name_file=path+file
   print(name_file)
   gr = pygrib.open(name_file)  
   msg=gr[69]
   temperatura=msg.values-273 #Convertendo de k para Celsius
   dado.append(temperatura)
    
 



file=path+list_files[1]
print(file)

plot.media(file,dado)
plot.max(file,dado)
plot.min(file,dado)
