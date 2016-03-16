#Script para plotagem dos locais das estações do ICA,CEMADEN e DAEE com zoom no sistema Cantareira

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap
import os
from scipy import interpolate
from scipy.interpolate import Rbf 

def plot_local_stations (dado_cem,dado_iac,dado_daee,dado_all):   
    
    #Plotagem do campo usando o Basemap. Inicia a projeção do mapa usando os limites min e max dos proprios dados
    lat=dado_cem[:,0]
    lon=dado_cem[:,1]
    
    llcrnrlon=-46.8
    urcrnrlon=-45.75
    llcrnrlat=-23.5
    urcrnrlat=-22.5
    
   
    
    m=Basemap(projection='mill',lat_ts=10,llcrnrlon=llcrnrlon, \
    urcrnrlon=urcrnrlon,llcrnrlat=llcrnrlat,urcrnrlat=urcrnrlat, \
    resolution='i',area_thresh=10000)
    m.readshapefile('/mnt2/dado/local das estações/shapefile/cantareiraWGS','cantareiraWGS',linewidth=1,color='b')
    mypatches=m.readshapefile('/mnt2/dado/local das estações/shapefile/cantareiraWGS','cantareiraWGS',linewidth=1,color='b')  
    
    
    
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
    
    
    ###
    lon=dado_all[:,1]
    lat=dado_all[:,0]
    print('lat')
    
    x,y = m(lon, lat)
    xx, yy = np.meshgrid(x, y)
    
    z=dado_all[:,2]
    print(lat,lon,z)
    rbfi = Rbf(x,y,z,function="cubic",episilon=0.5)
    zz=rbfi(xx,yy)
    
    
    
    #f = interpolate.interp2d(x, y, z, kind='cubic')
    
    
    
    ###
    #xnew = np.arange(llcrnrlon,urcrnrlon, 0.5)
    #ynew = np.arange(llcrnrlat, urcrnrlat, 0.5)
    #znew = f(xnew, ynew)
    cs=m.contourf (xx,yy ,zz,origin='lower')
    cbar = plt.colorbar(cs,pad=0.04)
        
    plt.xlabel('xlabel', fontsize=18)
    
    

    m.drawstates(linewidth=1., linestyle='dotted', color='k', antialiased=1)
    
    #m.drawmapboundary()
    m.drawparallels(np.arange(llcrnrlat, urcrnrlat,.25),labels=[1,0,0,0])
    m.drawmeridians(np.arange( llcrnrlon, urcrnrlon,.25),labels=[0,0,0,1])
        
    titulo='Localização das estações '
    plt.title(titulo)
   
    
    fig_out='/home/eduardo/dado/fig1/'+'local das estações zoom em Cantareira' + '.png'
    
    #Coloca a legenda abaixo do gráfico com sombreado e 'tamanho' igual a 1 para 
    #os simbolos
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
          fancybox=True, shadow=True,numpoints=1)
    
    #Opção bbox_inches evita que a legenda seja cortada na hora de salvar a figura
    plt.savefig(fig_out,bbox_inches='tight' )   
    #plt.show()
    plt.close()
    
path_fig='/home/eduardo/dado/fig1/'
arq1='/mnt2/dado/local das estações/cemaden estacoes.csv'
arq2='/mnt2/dado/local das estações/stations_IAC.csv'
arq3='/mnt2/dado/local das estações/estations_daee.csv'

arq4="/mnt2/dado/local das estações/all_por_mes/nprec_all_2014-01-01.txt"



#Verifica e cria o diretório
os.makedirs(path_fig, exist_ok=True)



dado_cem =np.loadtxt(arq1,delimiter=";")
dado_iac =np.loadtxt(arq2,delimiter=";")
dado_daee=np.loadtxt(arq3,delimiter=";")
dado_all=np.loadtxt(arq4,delimiter=";")

plot_local_stations (dado_cem,dado_iac,dado_daee,dado_all)

print( dado_all.shape)
print(dado_all)


    

    









