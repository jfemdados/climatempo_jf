# -*- coding: utf-8 -*-
"""
Created on Sat Aug 14 18:32:09 2021

@author: User
"""


import pandas as pd
import numpy as np
import plotly.io as pio
pio.renderers.default = 'browser' #ou svg

path = r'D:\Usuarios\Dell\Documents\5. JF em Dados\clima\tempo_jf.csv'
df_completo = pd.read_csv(path,sep = ';', skiprows=10,decimal='.')


df_completo = df_completo.dropna(axis=1,how='all').dropna(axis=0,thresh=7)
df_completo.columns = ['data','precipitacao','temp_max','temp_med','temp_min','umidade','vento']

df1 = df_completo
df1['data'] = df1['data'].astype(str)
df1['ano']=df1['data'].str.slice(0,4)
df1['mes']=df1['data'].str.slice(5,7)


verao = df1['mes'].isin(['12','01','02'])
inverno = df1['mes'].isin(['06','07','08'])
primavera = df1['mes'].isin(['09','10','11'])
outono = df1['mes'].isin(['03','04','05']) 

df_verao = df1[verao]
df_inverno = df1[inverno]
df_primavera = df1[primavera]
df_outono =df1[outono]

medias = df1.groupby('mes',as_index=False)['temp_max','temp_min','temp_med'].agg(np.mean)
medias['diff'] = medias['temp_max']-medias['temp_min']

precip = df1.groupby('mes',as_index=False)['precipitacao'].mean()

teste = df1.groupby(['mes','ano'],as_index=False)["temp_med"].mean()
teste = teste.loc[teste['ano']!="2007"]
teste = teste.loc[teste['ano']!="2020"]

teste2 = teste.values.tolist()

import plotly.graph_objects as go
import plotly.express as px 
from plotly.subplots import make_subplots

## #################################### LIVRO DE GEOGRAFIA

fig = go.Figure()

fig = make_subplots(specs=[[{"secondary_y": True}]])

fig.add_trace(go.Scatter(
        x=medias['mes'],
        y=medias['temp_med'],
        name="temperatura media",
        yaxis="y1",
        text=medias['temp_med'],line = dict(color='maroon', width=4), opacity=0.85
        ),
    secondary_y=True)

fig.add_trace(
    go.Bar(
        x=precip['mes'],
        y=precip['precipitacao'],
        name='precipitação',
        yaxis="y2",
        opacity=0.95,marker_color='royalblue',
        text=round(precip['precipitacao'],2)
    ),secondary_y=False)

fig.add_trace(go.Scatter(x=medias['mes'], y=medias['temp_min'], name='min',
                          line=dict(color='navy', width=2, dash='dot'),opacity=0.5),secondary_y=True)
fig.add_trace(go.Scatter(x=medias['mes'], y=medias['temp_max'], name='max',
                          line = dict(color='firebrick', width=2, dash='dot'),opacity=0.5),secondary_y=True)

fig.update_layout(yaxis2 = dict(range=[0, 29]), title='Temperatura média e preciptação em Juiz de Fora de 2007 a 2017')
fig.update_layout(yaxis1 = dict(range=[0, 15]))                 
fig.update_yaxes(title_text="<b>Temperatura</b> média", secondary_y=True)
fig.update_yaxes(title_text="<b>Precipitação</b> média", secondary_y=False)
fig.update_xaxes(title_text="<b>Meses</b>")

fig.show()

## ################################## HEATMAP

fig2 = go.Figure(data=go.Heatmap(
          x = teste['ano'],
          y = teste['mes'],
          z = teste['temp_med'],
          type = 'heatmap',
          colorscale = 'RdBu_r',
          ))
fig2.update_layout(
    title='Temperaturas médias mensais em Juiz de Fora 2008-2019')

fig2.show()

