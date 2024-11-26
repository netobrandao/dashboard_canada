import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout= 'wide')
#carregando os dados
data = pd.read_csv('https://raw.githubusercontent.com/netobrandao/ImmigrationCanada/refs/heads/main/canadian_immegration_data.csv')

st.title('Dashboard da Imigração canadense :flag-ca: ')
st.subheader('Visualize os dados da imigração canadense entre os anos de 1980 a 2013')


#tabelas para consulta

#tabela para consulta paises
country = data.sort_values(by='Total',ascending=False)
country.drop(columns=['Continent','Region','DevName'],inplace=True)
country = country[['Country','Total']]

#tabela para consulta regioes
region = pd.DataFrame(data.groupby(by='Region').sum().sort_values(by='Total',ascending=False)).reset_index()

#tabela para consulta de continentes
continent = pd.DataFrame(data.groupby(by='Continent').sum().sort_values(by='Total',ascending=False)['Total']).reset_index()

#tabela para consulta de devname
devname = pd.DataFrame(data.groupby(by='DevName').sum().sort_values(by='Total',ascending=False)).reset_index()

aba1,aba2,aba3,aba4,aba5 = st.tabs(["Dados","Paises", "Continentes","Regiões","Categoria"])

#grafico1

with aba1:
    st.header("Imigração Canadense")
    st.write("Visualize dados referentes a imigração canadense.")
    st.dataframe(data,width=2000,height=600,selection_mode='single-row')


with aba2:
    st.header("Gráfico de Barras por Países")

    # Seleção de países para filtrar
    countries = st.multiselect("Selecione os Países:", options=country['Country'].unique(), default=country['Country'][23:28])
    # Filtrar os dados
    filtered_country = country[country['Country'].isin(countries)]
    # Criar gráfico de barras
    if countries:
        fig_country = px.bar(filtered_country, x='Country', y='Total',width=600, height=600)
        
        fig_country.update_traces(text=filtered_country['Total'],textposition='outside',textfont=dict(size=16))
        
        fig_country.update_layout(
    xaxis=dict(
        title="Países",
        titlefont=dict(size=20),  # Tamanho do título do eixo X
        tickfont=dict(size=18),showgrid=False   # Tamanho dos ticks do eixo X
    ),yaxis=dict(showgrid=False,title="",tickfont=dict(size=16)))
        
        st.plotly_chart(fig_country, use_container_width= True)
    else:
        st.warning("Selecione pelo menos um país para visualizar o gráfico.")

#grafico2
with aba3:
    st.header("Gráfico de Barras por Região")
    # Seleção de países para filtrar
    regions = st.multiselect("Selecione as Regiões:", options=region['Region'].unique(), 
                             default=region['Region'][5:8])
    # Filtrar os dados
    filtered_data = region[region['Region'].isin(regions)]
    #Criar grafico de barras
    if regions:
        fig_region = px.bar(
                filtered_data,x='Region',y='Total',
                width=600, height=600)
        fig_region.update_traces(
                text=filtered_data['Total'],
                textposition='outside',textfont=dict(size=16))
        fig_region.update_layout(
        xaxis=dict(
        title="Regiões",
        titlefont=dict(size=20),  # Tamanho do título do eixo X
        tickfont=dict(size=18),showgrid=False   # Tamanho dos ticks do eixo X
    ),yaxis=dict(showgrid=False,title="",tickfont=dict(size=16)))
        
        

        st.plotly_chart(fig_region, use_container_width= True)
    else:
        st.warning("Selecione pelo menos uma região para visualizar o gráfico.")

#grafico3
with aba4:
    st.header("Gráfico de Barras por Continente")
    # Seleção de países para filtrar
    continents = st.multiselect("Selecione os Continentes:", options=continent['Continent'].unique(), 
                                default=continent['Continent'].unique())
    # Filtrar os dados
    filtered_data = continent[continent['Continent'].isin(continents)]
    #Criar grafico de barras
    if continents:
        fig_continent = px.bar(filtered_data,x='Continent',y='Total',
                            width=600, height=600)
        fig_continent.update_traces(text=continent['Total'],
                                    textposition='outside',textfont=dict(size=16))
        fig_continent.update_layout(
        xaxis=dict(
        title="Continente",
        titlefont=dict(size=20),  # Tamanho do título do eixo X
        tickfont=dict(size=18),showgrid=False   # Tamanho dos ticks do eixo X
    ),yaxis=dict(showgrid=False,title="",tickfont=dict(size=16)))

        st.plotly_chart(fig_continent,use_container_width= True)
    else:
        st.warning("Selecione pelo menos um continente para visualizar o gráfico.")

#grafico4
with aba5:
    st.header("Gráfico de Barras por Categoria")
     # Seleção de países para filtrar
    devnames = st.multiselect("Selecione as Categorias:", options=devname['DevName'].unique(), 
                                default=devname['DevName'].unique())
    # Filtrar os dados
    filtered_data = devname[devname['DevName'].isin(devnames)]

    if devnames:
        fig_devname = px.bar(filtered_data,x='DevName',y='Total',width=600, height=600)
        fig_devname.update_traces(
        text=continent['Total'],
        textposition='outside',textfont=dict(size=16))

        fig_devname.update_layout(
        xaxis=dict(
        title="Categoria",
        titlefont=dict(size=20),  # Tamanho do título do eixo X
        tickfont=dict(size=18),showgrid=False   # Tamanho dos ticks do eixo X
    ),yaxis=dict(showgrid=False,title="",tickfont=dict(size=16)))
        st.plotly_chart(fig_devname,use_container_width=True)
    else:
        st.warning("Selecione pelo menos uma categoria para visualizar o gráfico.")
        
st.markdown("[Fonte dos Dados](https://www.kaggle.com/datasets/ammaraahmad/immigration-to-canada)")
     
   


