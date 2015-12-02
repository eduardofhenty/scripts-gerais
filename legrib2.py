#Exemplo baseado em 
#http://www.himpactwxlab.com/home/how-to-wiki/write-grib2-data-with-pygrib
#http://pt.slideshare.net/arulalan/pygrib-documentation


import pygrib
import pickle
import numpy as np


file= "diabf01.gdas.200912.00Z.grb2"
gr = pygrib.open(file) 
gr.tell()

arquivo =open("saida1.txt","w")
arquivo2 =open("saida2.txt","w")

#Para obter as 10 primeiras mensagens do grib2
print("Obtendo as 10 primeiras mensagens do grib2\n")
grbmsg = gr.read(10)
print(grbmsg)
#Ler a mensagem especificando palavras chaves
print("Lendo a mensagem especificando palavras chaves\n")
msg = gr[28]
print(msg)
print("Imprimindo as palavras chaves \n")
print(msg.keys())

print("Imprimindo as diferentes latitudes \n")
print(msg['distinctLatitudes'])

print("\nImprimindo as diferentes latitudes \n")
print(msg['distinctLongitudes'])

#Obtendo os dados e outras propriedades usando indices
file_name = "diabf01.gdas.200912.00Z.grb2"
fileidx=pygrib.index(file_name,'shortName','level')
g=fileidx.select(shortName="toz",level=1000)
print("Imprimindo os valores associados ao nivel 1000\n")
print(g[0]['values'])

lats,lons = msg.latlons()
print("latitudes \n")
print(lats)
print("longitudes \n")
print(lons)

#Lendo uma msg associada a uma variavel
print("Lendo uma msg associada a uma variavel\n" )
pozmsg = gr.select(shortName='poz')
#Obtendo os valores
msg_vals = msg.values
print("Valores\n")
print(msg_vals)
print ("Dimensoes da matriz\n")
print(msg_vals.shape)
#Valores máximos e mínimos
print("Imprimindo os valores máximos e mínimos\n")
print ( np.amax(msg_vals),np.amin(msg_vals))

lista =[]
for g in gr:
    lista.append(g.shortName)    
#Imprimindo uma lista com as variaveis
print("Imprimindo uma lista das variaveis \n")
print(list(set (sorted(lista))))
print("Numero de variaveis \n")
print(len (list(set (sorted(lista))))) 


gr = pygrib.open(file) 
lista =[]
for g in gr:
    lista.append(g.level)    
#Imprimindo uma lista com os niveis
print("Imprimindo uma lista de niveis \n")
print(list(set (sorted(lista))))
print("Numero de niveis \n")
print(len (set(lista))  )
    
    

#Para mover o ponteiro para primeira posição. Evita ter que abrir o arquivo
gr.seek(0)
#Escrevendo no arquivo saida.txt algumas informações como descrição, variavel e nível
for g in gr:
        arquivo2.write(g.name+";"+ g.shortName+";"+str (g.level)+ "\n")
arquivo2.close()


gr.seek(0)
#Imprime um inventário do grib2
#Escrevendo apenas a variavel 
for g1 in gr:
    arquivo.write("%s  \n" %g1.shortName)

arquivo.close()        
