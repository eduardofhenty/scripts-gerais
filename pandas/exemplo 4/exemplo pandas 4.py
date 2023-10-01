# -*- coding: utf-8 -*-
"""
Created on Fri Sep 22 15:26:06 2023

@author: eduardo.henriques
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from numpy import mean

#Leitura dos dados de temperatura diária mínima e máxima. Fonte IPMA
#name_f = "C:/script python/dado/tmintmaxdaily_1855-2018_Lisbon-Geofisico.xlsx"
path_fig = "C:/data3/SITES FLUXTOWER/figura/"
name_f = "C:/data3/SITES FLUXTOWER/tmintmaxdaily_1855-2018_Lisbon-Geofisico.xlsx"
df = pd.read_excel( name_f, "tmintmaxdaily_1855-2018_Lisbon-",skiprows=2)
#Seleciona as colunas de interesse
df = df.iloc[:,0:5]
#Remove as primeiras linhas
df= df.drop(df.index[range(0,31)])
#Define a data a partir da combinação das colunas de ano, mes e dia
df["date"] = df['year'].astype(str) +"-"+ df["month"].astype(str)+"-"+df["day"].astype(str)
#Calcula resumo estatístico 
df[['tmin','tmax']].describe()
#Plot de dispersão
sns.scatterplot(data=df, x="tmin",y="tmax",  color="black"  ,sizes=1)
plt.xlabel("Temperatura mínima (ºC)")
plt.ylabel("Temperatura máxima (ºC)")
fname = path_fig + 'plot_dispersao Tmax e Tmin'+'.png'    
plt.savefig(fname,dpi=100)    

#Histograma
#Opção 1
fig,axes= plt.subplots(1,2,figsize=(15, 10))
fig.suptitle('Histograma')
#Primeiro subplot
sns.histplot(ax=axes[0],data=df, x="tmin", color="blue"  ,bins=30)
axes[0].set_xlabel("Temperatura mínima (ºC)")
axes[0].set_ylabel("Contagem")
#Segundo subplot
sns.histplot(ax=axes[1],data=df, x="tmax", color="red"  ,bins=30)
axes[1].set_xlabel("Temperatura máxima (ºC)")
axes[1].set_ylabel("Contagem")
#Salva o plot
fname = path_fig + 'plot_histograma Tmax e Tmin_v1'+'.png'    
plt.savefig(fname,dpi=300)

#subplot com uso de for e plot d densidade
fig,axes= plt.subplots(1,2,figsize=(15, 10))
axes = axes.ravel()  # flattening the array makes indexing easier
cols=['tmin','tmax']
cores=['blue','red']

for col, ax,cor in zip(cols, axes,cores):
    #sns.displot(data=df[col], ax=ax,color=cor)#Displot está obsoleto
    sns.histplot(data=df[col], kde=True, stat='density',color=cor, ax=ax)
#Salva o plot
fname = path_fig + 'plot_histograma Tmax e Tmin_v2'+'.png'    
plt.savefig(fname,dpi=100)
plt.close()
plt.figure().clear()
plt.cla()
plt.clf()

#plot de linha
#Converte a coluna date para um objeto datetime e calcula a média por ano
df['date']= pd.to_datetime(df['date'])
df_y =  df.set_index('date').groupby(pd.Grouper(freq='y')).mean()
df_y['date']= df_y.index
#Aplica o melt que nem no R
df_melt = pd.melt(df_y[['date','tmin','tmax']],id_vars='date',  value_vars=['tmin','tmax'])

#Opção 1. So o necessários

fig= sns.lineplot(data=df_melt,x='date',y='value',hue='variable')
fig.set(xlabel ="Ano", ylabel = "Temperatura (ºC)", title ='Série temporal em Lisboa')

#Salva o plot
fname = path_fig + 'plot_serie_temporal_Tmax e Tminv1'+'.png'    
plt.savefig(fname,dpi=300)

#Opção 2. Com vários itens a mais
labels=['1860','1880','1900','1920','1940','1960','1980','2000','2020']
graf,ax= plt.subplots(1,figsize=(15, 10))
t_min_media= np.round( df_y['tmin'].mean(),1)
t_max_media= np.round( df_y['tmax'].mean(),1)
sns.set_style("ticks", {'axes.grid' : True})
fig=sns.lineplot(data=df_melt ,x='date',y='value',hue='variable',palette=['blue','red'])
ax.set_title('Série temporal em Lisboa', fontdict={'size': 25, 'weight': 'bold'})
ax.set_xlabel('Ano',fontsize=25)
ax.set_ylabel('Temperatura (ºC)', fontsize=25)

ax.set_xticklabels(labels, size=15)
ax.set_yticklabels(ax.get_yticks(), size=15)
ax.axhline(t_min_media ,  color='blue',linestyle ='--')
ax.axhline(t_max_media,  color='red',linestyle ='--')
ax.text(df_melt[['date']].iloc[1], t_min_media , str(t_min_media), ha='center',fontsize=15)
ax.text(df_melt[['date']].iloc[1], t_max_media , str(t_max_media), ha='center',fontsize=15)
fig.legend(title='Variável',
    labels=['Temperatura mínima média','Temperatura máxima média'],
    loc='lower center', #'upper rigth','lower left','center', 'best'
            bbox_to_anchor=(0.8, -0.1),#Plota fora do gráfico
            frameon=False)#Remove a borda
#Define as cores da legenda
leg = fig.get_legend()
leg.legendHandles[0].set_color('blue')
leg.legendHandles[1].set_color('red')
#Salva o plot
fname = path_fig + 'plot_serie_temporal_Tmax e Tminv2'+'.png'    
plt.savefig(fname,dpi=400)

#PLots com FacetGrid
#Cálculo das médias mensais
df_m =  df[['date','tmin','tmax']].set_index('date').groupby(pd.Grouper(freq='m')).mean()
df_m['date']= df_m.index
databk = df_m.index
#Retorna uma string de um objeto datetime
df_m['date']=df_m['date'].dt.strftime("%Y-%m")
df_m['mes']= df_m.index.strftime("%m").astype(int)
df_m['ano']=df_m.index.strftime("%Y").astype(int)

#Concatena os dataframe para plotar duas variáveis 
df_m1 = df_m[['ano','mes','tmin']]
df_m2 = df_m[['ano','mes','tmax']]
df_m2 ['tmin'] =df_m2['tmax'] 
df_m2 = df_m2[['ano','mes','tmin']]
df_mes = pd.concat([df_m1.assign(temp='tmin'),
                  df_m2.assign(temp='tmax')])

#Muda o nome dos meses
lmes=['JAN','FEV','MAR','ABR','MAI','JUN','JUL','AGO','SET','OUT','NOV','DEZ']
#Estilo escolhido 
sns.set_style("ticks", {'axes.grid' : True})
#incia os subplots
grid = sns.FacetGrid(df_mes, col="mes",hue='temp' ,palette=['blue','red'],
                     col_wrap=4, height=3.5,aspect=1)

# Plot temperatura em função do ano
grid.map(sns.lineplot, "ano", "tmin")
grid.set(xlim=(1856, 2018))
grid.fig.suptitle("Lisboa",fontsize=30)
grid.fig.subplots_adjust(top=0.9) 
#Ajusta o eixo e os títulos
axes = grid.axes.flatten()
for ax,mes in zip(axes,lmes):
    ax.set_title(mes )
    ax.set_ylabel('Temperatura (ºC)', fontsize=15)
    ax.set_xlabel('Ano',fontsize=15)

plt.legend(title='Variável',
    labels=['Temperatura mínima média','Temperatura máxima média'],
    loc='lower center', #'upper rigth','lower left','center', 'best'
            bbox_to_anchor=(0.8, -0.5),#Plota fora do gráfico
            frameon=False)    
# Ajusta o arranjo dos plots
grid.fig.tight_layout(w_pad=1)
fname = path_fig + 'plot_serie_temporal_ Tmin por mes'+'.png'    
plt.savefig(fname,dpi=400)
plt.close()
plt.figure().clear()
plt.cla()
plt.clf()

#plots do tipo boxplot
bp =sns.boxplot(data=df ,x= 'month',y='tmin'  ,  color='blue') 
bp.set_xlabel('Mês', fontsize=15)
bp.set_ylabel('Temperatura (ºC)', fontsize=15)
bp.set_title('Temperatura mínima diária',fontsize=20)
bp.set_yticks( [5,10,15,20] )
#Salva os plots
fname = path_fig + 'plot_boxplot Tmin por mes v1'+'.png'    
plt.savefig(fname,dpi=400)


#plots de boxplot
#Temperatura mínima média por mês
df_box = df_m[['ano','mes','tmin']]
bp =sns.boxplot(data=df_box ,x= 'mes',y='tmin'  ,  color='blue') 
bp.set_xlabel('Mês', fontsize=15)
bp.set_ylabel('Temperatura (ºC)', fontsize=15)
bp.set_title('Temperatura mínima média mensal',fontsize=20)
bp.set_yticks( [5,10,15,20] )
#Salva o plot
fname = path_fig + 'plot_boxplot Tmin por mes v2'+'.png'    
plt.savefig(fname,dpi=400)
#Temperatura máxima por mês
df_box = df_m[['ano','mes','tmax']]
bp =sns.boxplot(data=df_box ,x= 'mes',y='tmax'  ,  color='red') 
bp.set_xlabel('Mês', fontsize=15)
bp.set_ylabel('Temperatura (ºC)', fontsize=15)
bp.set_title('Temperatura máxima média mensal',fontsize=20)
bp.set_yticks( [10,15,20,25,30,35] )
fname = path_fig + 'plot_boxplot Tmax por mes'+'.png'    
plt.savefig(fname,dpi=400)

#boxplot de temperatura mínima e máxima por mes
fig, ax = plt.subplots()
df_box = df_mes
my_cor = {'tmin':'blue','tmax':'red' }
bp =sns.boxplot(data=df_box ,x= 'mes',y='tmin' ,hue='temp' ,palette=my_cor) 
bp.set_xlabel('Mês', fontsize=15)
bp.set_ylabel('Temperatura (ºC)', fontsize=15)
bp.set_title('Temperatura mínima e máxima média',fontsize=20)
hands, labs = ax.get_legend_handles_labels()
plt.legend(handles=my_cor, labels=['Temperatura mínima média','Temperatura máxima média'])
plt.legend(title='Variável',
    labels=['Temperatura mínima média','Temperatura máxima média'],
    loc='lower center', #'upper rigth','lower left','center', 'best'
            bbox_to_anchor=(0.8, -0.5),#Plota fora do gráfico
            frameon=False)    
plt.setp(bp.get_legend().get_texts(), fontsize='10') 
#Salva o plot
fname = path_fig + 'plot_boxplot_ Tmax e Tmin por mes'+'.png'    
plt.savefig(fname,dpi=400)

#Calcular as medias mensais
dfM_bym =  df_m[['mes','tmin','tmax']].groupby( by= ['mes'],as_index=False).mean()
print(dfM_bym)
fig,axes= plt.subplots(1,2,figsize=(15, 10))
fig.suptitle("Lisboa",fontsize=30)
pl_b1= sns.barplot(data=dfM_bym, x='mes', y='tmin', color="blue",ax=axes[0])
pl_b2=sns.barplot(data=dfM_bym, x='mes', y='tmax',ax=axes[1], color="red")
axes[0].set_xlabel('Mês', fontsize=20)
axes[0].set_ylabel('Temperatura (ºC)', fontsize=20)
axes[1].set_xlabel('Mês', fontsize=20)
axes[1].set_ylabel('Temperatura (ºC)', fontsize=20)
axes[0].set_yticks( [0,10,15,20,25,30] )
axes[1].set_yticks( [0,10,15,20,25,30] )
axes[0].set_title('Temperatura mínima',fontsize=20)
axes[1].set_title('Temperatura máxima',fontsize=20)
axes[0].tick_params(axis='both', which='major', labelsize=14)   
axes[1].tick_params(axis='both', which='major', labelsize=14)   
#Adiciona os valores da media em cima da barra
ymin= np.round( dfM_bym['tmin']    ,1 )
for i, v in enumerate(ymin):
   pl_b1.text(i, v + 0.2, str(v), ha='center',fontsize=18)
ymax= np.round( dfM_bym['tmax']    ,1 )
for i, v in enumerate(ymax):
   pl_b2.text(i, v + 0.2, str(v), ha='center',fontsize=18)
   
#Salva o plot
fname = path_fig + 'plot de barra Tmin e Tmax por mes em subplots'+'.png'    
plt.savefig(fname,dpi=400)
plt.close()
plt.figure().clear()
plt.cla()
plt.clf()

fig,ax= plt.subplots(1,figsize=(15, 10))
df_melt_Mbym = pd.melt(dfM_bym[['mes','tmin','tmax']],id_vars='mes',  value_vars=['tmin','tmax'])
ax=sns.barplot(data=df_melt_Mbym , x='mes', y='value',hue='variable' ,palette=['blue','red'])
ax.set_xlabel('Mês', fontsize=20)
ax.set_ylabel('Temperatura (ºC)', fontsize=20)
ax.set_yticks( [0,5,10,15,20,25,30] )
ax.tick_params(axis='both', which='major', labelsize=14)   
ax.set_title('Lisboa',fontsize=30)
plt.legend(title='Variável',    
    labels=['Temperatura mínima média','Temperatura máxima média'],
    loc='lower center', #'upper rigth','lower left','center', 'best'
            bbox_to_anchor=(0.8, -0.3),#Plota fora do gráfico
            frameon=False)    

for i, v in enumerate(ymin):
   ax.text(i-0.1, v + 0.2, str(v), ha='center',fontsize=10)

for i, v in enumerate(ymax):
   ax.text(i+0.1, v + 0.2, str(v), ha='center',fontsize=10)

ax = plt.gca()
leg = ax.get_legend()
leg.legendHandles[0].set_color('blue')
leg.legendHandles[1].set_color('red')

#Salva o plot
fname = path_fig + 'plot de barra Tmin e Tmax por mes'+'.png'    
plt.savefig(fname,dpi=400)
plt.close()
plt.figure().clear()
plt.cla()
plt.clf()

#Plot com estimador e desvio padrão
df_temp =df_m[['mes','tmin','tmax']]
ax=sns.barplot(data=df_temp, x='mes', y='tmin',estimator=mean,ci='sd',color='blue',
              errcolor = 'gray', errwidth = 4, capsize = 0.15 ,saturation = 8   )
ax.set_xlabel('Mês', fontsize=20)
ax.set_ylabel('Temperatura (ºC)', fontsize=20)
ax.tick_params(axis='both', which='major', labelsize=14)   
ax.set_title('Lisboa: Temperatura mínima média',fontsize=25)

#Salva o plot
fname = path_fig + 'plot de barra Tmin por mes com barra de erro'+'.png'    
plt.savefig(fname,dpi=400)
