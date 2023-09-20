# -*- coding: utf-8 -*-
"""
Created on Mon Aug 28 11:37:06 2023

@author: eduardo.henriques
"""

import pandas as pd

def get_min_max_diario (sitio,name_var):
    """  
    Obtem os valores valores mínimos e máximos de corte de uma variável
    """
    name_f  = "filtro_estat_diario.csv"
    df_tab = pd.read_csv(name_f  ,  sep=",")
    var_min = name_var+'_min'     
    var_max = name_var+'_max'      
    val_min = df_tab [ (df_tab.nome_alternativo==sitio) | (df_tab.sitio==sitio)][var_min]
    val_min=val_min.iloc[0]
    val_max = df_tab [ (df_tab.nome_alternativo==sitio) | (df_tab.sitio==sitio)][var_max]
    val_max =val_max.iloc[0]
    msg = "Sitio: "+ sitio + " Variável: "+ name_var+" L_min: "+str(val_min)+ " L_max: "+ str(val_max)
    print(msg)
    return( [val_min,val_max ] )

def aplicar_fdiariov2(df_bruto,sitio,name_var,name_col):
    """  
    Aplica um filtro diário nos dados. Calcula a média diaria e elimina
    os dados abaixo e acima desses limiares na coluna da variável
    """    
    val_lims = get_min_max_diario(sitio, name_var)
    val_min =val_lims[0]
    val_max =val_lims[1]
    df_brutod = df_bruto[["date",name_col]  ]
    df_brutod['date'] = pd.to_datetime(df_brutod['date'])
    df = df_brutod.set_index('date').groupby(pd.Grouper(freq='d')).mean()
    
    seq_date = df.loc[ (df[name_col] < val_min) | (df[name_col] > val_max) ]
    #verifica a quantidade de dados a serem eliminadas
    if(len (seq_date) >0):                 
        seq_date = seq_date.index.strftime("%Y-%m-%d")              
        mydate = pd.to_datetime(df_bruto['date']).dt
        df_bruto['daten']= mydate.strftime("%Y-%m-%d")
        seq_bol= df_bruto['daten'] .isin(seq_date)
        df_bruto.loc[seq_bol,name_col] = None
    else:
        df_bruto[name_col]
    
    print("Total a serem removidos: "+ str(len(seq_date)))
    return (df_bruto[name_col])



sitio = "sitio"
df_bruto = pd.read_csv( "flx_raw.csv" ,  sep=";")
#Imprime as primeiras linhas do ficheiro
print(df_bruto.head( ))
#Imprime as últimas linhas do ficheiro
print( df_bruto.tail())

df_bruto.sort_values("date"    ,ascending=True)
df_bruto.ta.mean() #média de ta
#Verifica e elimina dados duplicados
if(df_bruto.duplicated("date").sum() >0):
    print("Existe dado duplicado")
    df_bruto.drop_duplicates("date"    )  
 
#tipo de dados
df_bruto.dtypes  
df =df_bruto[ ['date','par','Rn'] ]

# Adiantando a hora em num novo df
td = pd.Timedelta(hours=1)
ts =pd.to_datetime( df['date'])
new_ts_series = ts.apply(lambda x: x + td)
df['daten'] =  new_ts_series

#Leitura de planilha excel
name_f = "descritor_variaveis_dados_brutos.xlsx"
df_desc = pd.read_excel(name_f,"sitio_raw")
#Novos nomes
df_desc.columns= ["variavel","descricao","status"]
#Acha os indices iguais desprez
idx = df_desc[ df_desc['status']=="desprez" ].index
#remove as linhas 
df_desc.drop( idx,inplace=True )
variaveis=df_desc.variavel
#Atualiza o df só as variiáveis válidas
df_bruto = df_bruto.loc[:,variaveis ]
    
#Filtragem dos dados de humidade e temperatura
df_bruto.loc[ df_bruto['rh'] >=99, 'rh'   ]= None
df_bruto.loc[ df_bruto.ta  >=35, 'ta'   ]= None
df_bruto.loc[ df_bruto.ta  <=19, 'ta'   ]= None

#Define o fluxo de calor do solo 
df_bruto.G_cor = 0.02*df_bruto.Rn -5
df_bruto['H'] = aplicar_fdiariov2(df_bruto,"sitio",'H','H' )
df_bruto['LE'] = aplicar_fdiariov2(df_bruto,"sitio",'LE','LE' )
#Escreve o resultado em novo ficheiro 
nmficheiro ="C:/data3/SITES FLUXTOWER/sitio_new.csv"
df_bruto.to_csv( nmficheiro,  header=True,index=False,  sep=';',decimal='.',  na_rep="NA"  ) 
