import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.legend_handler import HandlerLine2D
st.set_option('deprecation.showPyplotGlobalUse', False)

# Imagem
img = Image.open('logo_daumau.png')
st.image(img)

# Título
st.markdown('## Validação de estimativas para DAU/MAU/Stickiness - MVF')
st.write("")
st.write('''Esta aplicação tem como objetivo validar as visualizações das estimativas de DAU, MAU e Stickiness que 
	comparam os dados reais e as estimativas com um determindado intervalo de confiança.''')

# Carregando base de dados
df = pd.read_csv('dau_mau_streamlit.csv', parse_dates=['DATE'])

app_cliente = st.selectbox('Cliente',df['APP'].unique())
app_competitor = st.selectbox('Concorrente',df['APP'].unique())

food_dau = 0.10
food_mau = 0.08
food_stick = 0.08
health_dau = 0.15
health_mau = 0.07
health_stick = 0.15
shopping_dau = 0.16
shopping_mau = 0.13
shopping_stick = 0.16
finance_dau = 0.19
finance_mau = 0.21
finance_stick = 0.12
travel_dau = 0.23
travel_mau = 0.19
travel_stick = 0.25
others_dau = 0.12
others_mau = 0.05
others_stick = 0.11

# Definindo Categoria
app_cat_df = df[df['APP'] == app_competitor]
app_cat = app_cat_df['CATEGORY'].unique()[0]

limit_dau = []
limit_mau = []
limit_stick = []

if app_cat == 'FOOD_AND_DRINK':
	limit_dau.append(food_dau)
	limit_mau.append(food_mau)
	limit_stick.append(food_stick)
elif app_cat == 'HEALTH_AND_FITNESS':
	limit_dau.append(health_dau)
	limit_mau.append(health_mau)
	limit_stick.append(health_stick)
elif app_cat == 'SHOPPING':
	limit_dau.append(shopping_dau)
	limit_mau.append(shopping_mau)
	limit_stick.append(shopping_stick)
elif app_cat == 'FINANCE':
	limit_dau.append(finance_dau)
	limit_mau.append(finance_mau)
	limit_stick.append(finance_stick)
elif app_cat == 'TRAVEL':
	limit_dau.append(travel_dau)
	limit_mau.append(travel_mau)
	limit_stick.append(travel_stick)
else:
	limit_dau.append(others_dau)
	limit_mau.append(others_mau)
	limit_stick.append(others_stick)

good = ['FOOD_AND_DRINK','OTHERS']
medium = ['HEALTH_AND_FITNESS','SHOPPING']
bad = ['FINANCE','TRAVEL']

if app_cat in good:
	st.success('''ACCURATE: O nível de acurácia para estas visualizações são altas. 
		As estimativas deste nível podem ser utilizadas para análises mais profundas pois ficam perto da realidade.''')
elif app_cat in medium:
	st.warning('''FAIR: O nível de acurácia para estas visualizações é médio. 
	É indicado usar essas estimativas para análises de comportamento.''')
elif app_cat in bad:
	st.error('''MODERATE: O nível de acurácia para estas visualizações é moderado.
	 Não há muitos dados para uma estimativa precisa.''')

############ Gráfico DAU ############
df_cliente = df[['DATE', 'APP', 'DAU Real']]
df_cliente = df_cliente[df_cliente['APP'] == app_cliente]
df_cliente = df_cliente.set_index('DATE')

df_competitor = df[['DATE', 'APP', 'preds_dau']]
df_competitor = df_competitor[df_competitor['APP'] == app_competitor]
df_competitor = df_competitor.set_index('DATE')

df_plot = pd.merge(df_cliente,df_competitor,left_index=True, right_index=True)
df_plot['limit sup'] = df_plot['preds_dau'] * (1+limit_dau[0])
df_plot['limit inf'] = df_plot['preds_dau'] * (1-limit_dau[0])

fig, ax = plt.subplots(figsize=(14,5))
lineDau1, = ax.plot(df_plot['preds_dau'], label="DAU Competitor")
plt.fill_between(df_plot.index,df_plot['limit inf'],df_plot['limit sup'], color='b', alpha=.1)
lineDau2, = ax.plot(df_plot['DAU Real'], label="DAU Cliente")
ax.legend(handler_map={lineDau1: HandlerLine2D(numpoints=8)})
plt.title('DAU REAL X DAU CONCORRENTE (Estimativa)')

st.pyplot()

############ Gráfico MAU ############
df_cliente_mau = df[['DATE', 'APP', 'MAU Real']]
df_cliente_mau = df_cliente_mau[df_cliente_mau['APP'] == app_cliente]
df_cliente_mau = df_cliente_mau.set_index('DATE')

df_competitor_mau = df[['DATE', 'APP', 'preds_mau']]
df_competitor_mau = df_competitor_mau[df_competitor_mau['APP'] == app_competitor]
df_competitor_mau = df_competitor_mau.set_index('DATE')

df_plot_mau = pd.merge(df_cliente_mau,df_competitor_mau,left_index=True, right_index=True)
df_plot_mau['limit sup'] = df_plot_mau['preds_mau'] * (1+limit_mau[0])
df_plot_mau['limit inf'] = df_plot_mau['preds_mau'] * (1-limit_mau[0])

fig, ax = plt.subplots(figsize=(14,5))
lineMau1, = ax.plot(df_plot_mau['preds_mau'], label="MAU Competitor")
plt.fill_between(df_plot_mau.index,df_plot_mau['limit inf'],df_plot_mau['limit sup'], color='b', alpha=.1)
lineMau2, = ax.plot(df_plot_mau['MAU Real'], label="MAU Cliente")
ax.legend(handler_map={lineMau1: HandlerLine2D(numpoints=8)})
plt.title('MAU REAL X MAU CONCORRENTE (Estimativa)')

st.pyplot()

############ Gráfico Stickiness ############
df_cliente_stick = df[['DATE', 'APP', 'Stickiness Real']]
df_cliente_stick = df_cliente_stick[df_cliente_stick['APP'] == app_cliente]
df_cliente_stick = df_cliente_stick.set_index('DATE')

df_competitor_stick = df[['DATE', 'APP', 'Stickiness Preds']]
df_competitor_stick = df_competitor_stick[df_competitor_stick['APP'] == app_competitor]
df_competitor_stick = df_competitor_stick.set_index('DATE')

df_plot_stick = pd.merge(df_cliente_stick,df_competitor_stick,left_index=True, right_index=True)
df_plot_stick['limit sup'] = df_plot_stick['Stickiness Preds'] * (1+limit_stick[0])
df_plot_stick['limit inf'] = df_plot_stick['Stickiness Preds'] * (1-limit_stick[0])

fig, ax = plt.subplots(figsize=(14,5))
lineStick1, = ax.plot(df_plot_stick['Stickiness Preds'], label="Stickiness Competitor")
plt.fill_between(df_plot_stick.index,df_plot_stick['limit inf'],df_plot_stick['limit sup'], color='b', alpha=.1)
lineStick2, = ax.plot(df_plot_stick['Stickiness Real'], label="Stickiness Cliente")
ax.legend(handler_map={lineStick1: HandlerLine2D(numpoints=8)})
plt.title('Stickiness REAL X Stickiness CONCORRENTE (Estimativa)')

st.pyplot()