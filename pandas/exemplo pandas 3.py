# -*- coding: utf-8 -*-
"""
Created on Thu Sep 21 09:36:15 2023

@author: Eduardo Fernandes Henriques
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates
import numpy as np
from matplotlib.ticker import StrMethodFormatter


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
#df['date']= df['date'].dt.strftime("%Y-%m-%d")
df.index =df['date']

#Primeira opção de subplots com uma linha
df[['ta','taed']].plot(subplots=True,color=['k']    )
 
#A testar o formato da data em %Y-%m e frequencia 
ax=plt.figure(figsize=(7,4), dpi=300)
fig, ax = plt.subplots(figsize=(12, 12))
fig.suptitle('sitio')
sns.lineplot(data=df,x=df.date.values,y='ta')
date_form = DateFormatter("%m-%Y")
ax.xaxis.set_major_formatter(date_form)
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=6))


#
sns.set_theme()
#Modifica o estilo padrão do plot
sns.set(font_scale=1.5, style="whitegrid")
fig,axes = plt.subplots(2,1,figsize=(10, 10))
fig.suptitle('sitio')
date_form = DateFormatter("%m-%Y")
sns.lineplot(data=df,x='date',y='ta',ax=axes[0])
axes[0].xaxis.set_major_formatter(date_form)
axes[0].xaxis.set_major_locator(mdates.MonthLocator(interval=6))
#Ajusta com os valores y aparecem
ytick = np.linspace(min( df['ta']),max( df['ta']),5)
axes[0].set_yticks(ytick,np.round(ytick,0)  )
axes[0].yaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))
#sns.lineplot(data=df,x='date',y='taed',ax=axes[1])
sns.lineplot(data=df,x='date',y=df.iloc[:,1],ax=axes[1])
axes[1].xaxis.set_major_formatter(date_form)
axes[1].xaxis.set_major_locator(mdates.MonthLocator(interval=6))
ytick = np.linspace(min( df['taed']),max( df['taed']),5)
axes[1].set_yticks(ytick,np.round(ytick,0)  )
axes[1].yaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))

num_vars = len(df.columns)-1
#Resto da divisão 
rd = num_vars%5
ntotal= int((num_vars -rd)/5)
path_fig = "C:/script python/fig/"

#Plots das variáves figuras com 5 subplots
for i in range(0,ntotal-1):
    print(i)
    fig,axes = plt.subplots(5,1,figsize=(10, 15))
    fig.subplots_adjust(left=0.1, bottom=None, right=0.95, top=.95,
                       wspace=None, hspace=0.7)
    #fig.tight_layout()
    fig.suptitle('sitio')
    date_form = DateFormatter("%m-%Y")
    #Primeiro plot
    df_var = df.iloc[:,0 + 5*i]
    sns.lineplot(data=df,x='date',y=df_var,ax=axes[0])
    axes[0].xaxis.set_major_formatter(date_form)
    axes[0].xaxis.set_major_locator(mdates.MonthLocator(interval=6))
    #De acordo com min e max da variável é definido as marcas em y
    ytick = np.linspace(df_var.min(),df_var.max(),5)
    axes[0].set_yticks(ytick,np.round(ytick,0)  )
    axes[0].yaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))
    #Segundo plot
    df_var = df.iloc[:,1 + 5*i]
    sns.lineplot(data=df,x='date',y=df_var,ax=axes[1])
    axes[1].xaxis.set_major_formatter(date_form)
    axes[1].xaxis.set_major_locator(mdates.MonthLocator(interval=6))
    ytick = np.linspace(df_var.min(),df_var.max(),5)    
    axes[1].set_yticks(ytick,np.round(ytick,0)  )
    axes[1].yaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))    
    #Terceiro plot
    df_var = df.iloc[:,2 + 5*i]
    sns.lineplot(data=df,x='date',y=df_var,ax=axes[2])
    axes[2].xaxis.set_major_formatter(date_form)
    axes[2].xaxis.set_major_locator(mdates.MonthLocator(interval=6))
    ytick = np.linspace(df_var.min(),df_var.max(),5)    
    axes[2].set_yticks(ytick,np.round(ytick,0)  )
    axes[2].yaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))
    #Quarto plot
    df_var = df.iloc[:,3 + 5*i]
    sns.lineplot(data=df,x='date',y=df_var,ax=axes[3])
    axes[3].xaxis.set_major_formatter(date_form)
    axes[3].xaxis.set_major_locator(mdates.MonthLocator(interval=6))
    ytick = np.linspace(df_var.min(),df_var.max(),5)    
    axes[3].set_yticks(ytick,np.round(ytick,0)  )
    axes[3].yaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))
    #Quinto plot
    df_var = df.iloc[:,4 + 5*i]
    sns.lineplot(data=df,x='date',y=df_var,ax=axes[4])
    axes[4].xaxis.set_major_formatter(date_form)
    axes[4].xaxis.set_major_locator(mdates.MonthLocator(interval=6))
    ytick = np.linspace(df_var.min(),df_var.max(),5)    
    axes[4].set_yticks(ytick,np.round(ytick,0)  )
    axes[4].yaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))
    #Salvo os plots
    fname = path_fig + 'plot_serie_diaria_parte_'+str(i+1)+'.png'    
    plt.savefig(fname,dpi=100)
    

#Plot da variaveis restantes
fig, axes = plt.subplots(nrows=rd, ncols=1,figsize=(10, 10))    
fig.suptitle('sitio')
for i in range(1,rd ):    
    cor='k'    
    lw= 0.9
    print(i+ 5*ntotal )
    df.iloc[:,i+ 5*ntotal ].plot(ax=axes[1-i] ,lw=lw,color=cor)    
    axes[1-i].set(xlabel='Data', ylabel=df.columns[i+ 5*ntotal])
    axes[1-i].xaxis.set_major_formatter(date_form)
    axes[1-i].xaxis.set_major_locator(mdates.MonthLocator(interval=6)) 



fname = path_fig + 'plot_serie_diaria_parte_'+'teste'+'.png'    
fig.savefig(fname,dpi=100)



