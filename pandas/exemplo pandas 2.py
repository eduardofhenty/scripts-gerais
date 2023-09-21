# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 14:31:58 2023

@author: Eduardo Fernandes Henriques
"""

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates


#Leitura do ficheiro de dados
name_f ="C:/data3/SITES FLUXTOWER/sitio_new.csv"
df_bruto = pd.read_csv( name_f ,  sep=";")
#Imprime as primeiras linhas do ficheiro
print(df_bruto.head( ))
#Imprime as últimas linhas do ficheiro
print( df_bruto.tail())

df_brutod = df_bruto
df_brutod['date'] = pd.to_datetime(df_brutod['date'])
df = df_brutod.set_index('date').groupby(pd.Grouper(freq='d')).mean()
df['date'] = df.index
df['date'] = pd.to_datetime(df['date'])
df['date']= df['date'].dt.strftime("%Y-%m-%d")

ax=plt.figure(figsize=(7,4), dpi=300)
df[['ta','taed']].plot(subplots=True,color=['k']    )

plt.show()    



num_vars = len(df.columns)-1
rd = num_vars%5
ntotal= int((num_vars -rd)/5)

path_fig = "C:/data3/SITES FLUXTOWER/figura/"
mydpi = 1
plt.figure(figsize=(20/mydpi, 10/mydpi))


for i in range(0,ntotal-1):     
    fig, axes = plt.subplots(nrows=5, ncols=1,gridspec_kw={'height_ratios': [1, 1,1,1, 3]})
    plt.tight_layout()
    
    plt.subplots_adjust(left=0.1, bottom=None, right=None, top=.9,
                        wspace=None, hspace=0.5)
    #Escreve o titulo principal
    fig.suptitle("Sitio") 
    cor='k'    
    lw= 0.9
    df.iloc[:,0 + 5*i ].plot(ax=axes[0] ,lw=lw,color=cor )    
    df.iloc[:,1 + 5*i ].plot(ax=axes[1],lw=lw,color=cor)
    df.iloc[:,2 + 5*i ] .plot(ax=axes[2],lw=lw,color=cor)
    df.iloc[:,3 + 5*i ].plot(ax=axes[3],lw=lw,color=cor)
    df.iloc[:,4 + 5*i ].plot(ax=axes[4],lw=lw,color=cor)
    
    j=0 + 5*i 
    for ax in axes.flat:
        ax.set(xlabel='Data', ylabel=df.columns[j] )   
        ax.title.set_text(df.columns[j] )      
        # Define the date format
        date_form = DateFormatter("%Y-%m")
        ax.xaxis.set_major_formatter(date_form)
        j = j+1
    fname = path_fig + 'plot_serie_diaria_parte_'+str(i+1)+'.png'    

    plt.savefig(fname,dpi=mydpi*1000)

    
fig, axes = plt.subplots(nrows=rd, ncols=1)    
for i in range(1,rd ):    
    cor='k'    
    lw= 0.9
    print(i+ 5*ntotal )
    df.iloc[:,i+ 5*ntotal ].plot(ax=axes[1-i] ,lw=lw,color=cor)    
    ax.set(xlabel='Data', ylabel=df.columns[i+ 5*ntotal])

    
fname = path_fig + 'plot_serie_diaria_parte_'+str(i+1).png
plt.savefig()
        
    
    
