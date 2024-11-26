import streamlit as st
import pandas as pd
import plotly.express as px

# Carregar os dados
data = pd.read_csv('https://raw.githubusercontent.com/netobrandao/ImmigrationCanada/refs/heads/main/canadian_immegration_data.csv')

#tabelas para consulta
#Paises
datacountry = data.drop(columns=(['Continent','Region','DevName','Total']))
datacountry = datacountry.T
datacountry.columns = datacountry.iloc[0]
datacountry = datacountry[1:].reset_index()
datacountry = datacountry.rename(columns={'index': 'Ano'})
datacountry = datacountry.astype(int)

#Continentes
datacontinent = data.drop(columns=(['Country','Region','DevName','Total']))
datacontinent = datacontinent.groupby('Continent').sum().T.reset_index()
datacontinent.rename(columns={'index': 'Ano'},inplace=True)
datacontinent = datacontinent.astype(int)

#Regiões
dataregion = data.drop(columns=(['Country','Continent','DevName','Total']))
dataregion = dataregion.groupby('Region').sum().T
dataregion.reset_index(inplace=True)
dataregion = dataregion.rename(columns={'index': 'Ano'})
dataregion = dataregion.astype(int)

#DevName
datadevname = data.drop(columns=(['Country','Continent','Region','Total']))
datadevname = datadevname.groupby('DevName').sum().T
datadevname.reset_index(inplace=True)
datadevname = datadevname.rename(columns={'index': 'Ano'})
datadevname = datadevname.astype(int)


st.title("Séries Temporais da Imigração Canadense :flag-ca: ")
st.subheader('Visualize os dados da imigração canadense entre os anos de 1980 a 2013')

aba1,aba2,aba3,aba4 = st.tabs(["Paises", "Continentes","Regiões","Categoria"])

with aba1:
    st.header("Série Temporal por País")
    #Filtro: Seleção de países
    paises = st.multiselect(
        "Selecione os Países:",
        options=datacountry.columns[1:],  #Ignora a coluna 'Ano'
        default=datacountry.columns[25]    #Seleciona o 'Brazil' como padrão
    )

    #Filtro: Intervalo de anos
    anos = st.slider(
        "Selecione o intervalo de anos:",
        min_value=int(datacountry['Ano'].min()),
        max_value=int(datacountry['Ano'].max()),
        value=(int(datacountry['Ano'].min()), int(datacountry['Ano'].max())),key='slider_pais'
    )

    datacountry_filtrada = datacountry[(datacountry['Ano'] >= anos[0]) & (datacountry['Ano'] <= anos[1])]

    #Construção do grafico
    if paises:
        data_long = datacountry_filtrada.melt(id_vars=['Ano'], value_vars=paises, 
                                            var_name='País', value_name='Valor')
        fig_country = px.line(
            data_long,
            x="Ano",
            y="Valor",
            color="País",
            title="Série Temporal por País",
            labels={"Valor": "Valor", "Ano": "Ano", "País": "País"}
        )
        #Parametros do Grafico
        fig_country.update_layout(
        xaxis=dict(
        title="Ano",
        titlefont=dict(size=20),  
        tickfont=dict(size=16),showgrid=False
    ),yaxis=dict(showgrid=False,title="",tickfont=dict(size=16)))
        st.plotly_chart(fig_country, use_container_width=True)
    
    else:
        st.warning("Selecione pelo menos um país para visualizar o gráfico.")

with aba2:
    st.header("Série Temporal por Continente")
     #Filtro: Seleção de continentes
    continentes = st.multiselect(
        "Selecione os Continentes:",
        options=datacontinent.columns[1:],  #Ignora colunas 'Índice' e 'Ano'
        default=datacontinent.columns[2]
    )
    
    #Filtro: Intervalo de anos
    anos_continente = st.slider(
        "Selecione o intervalo de anos:",
        min_value=int(datacontinent['Ano'].min()),
        max_value=int(datacontinent['Ano'].max()),
        value=(int(datacontinent['Ano'].min()), int(datacontinent['Ano'].max())),key='slider_continent'
    )
    datacontinent_filtrada = datacontinent[
        (datacontinent['Ano'] >= anos_continente[0]) & 
        (datacontinent['Ano'] <= anos_continente[1])
    ]
    if continentes:
        #Tratamento dos dados
        data_long_continent = datacontinent_filtrada.melt(
            id_vars=['Ano'], value_vars=continentes, 
            var_name='Continente', value_name='Valor'
        )
        #Construção do grafico
        fig_continent = px.line(
            data_long_continent,
            x="Ano",
            y="Valor",
            color="Continente",
            title="Série Temporal por Continente",
            labels={"Valor": "Valor", "Ano": "Ano", "Continente": "Continente"}
        )
        #Parametros do Grafico
        fig_continent.update_layout(
        xaxis=dict(
        title="Ano",
        titlefont=dict(size=20),  
        tickfont=dict(size=16),showgrid=False
    ),yaxis=dict(showgrid=False,title="",tickfont=dict(size=16)))
        st.plotly_chart(fig_continent,use_container_width=True)
    else:
        st.warning("Selecione pelo menos um continente para visualizar o gráfico.")

with aba3:
    st.header("Série Temporal por Região")
    #Filtro: Seleção das regiões
    regioes = st.multiselect(
        "Selecione as Regiões:",
        options=dataregion.columns[1:],  # Ignora colunas 'Índice' e 'Ano'
        default=dataregion.columns[5]
    )
    #Filtro: Intervalo de anos
    anos_regiao = st.slider(
        "Selecione o intervalo de anos:",
        min_value=int(dataregion['Ano'].min()),
        max_value=int(dataregion['Ano'].max()),
        value=(int(dataregion['Ano'].min()), int(dataregion['Ano'].max())),key='slider_region'
    )
    dataregion_filtrada = dataregion[
        (dataregion['Ano'] >= anos_regiao[0]) & 
        (dataregion['Ano'] <= anos_regiao[1])
    ]
    if regioes:
        #Tratamento dos dados
        data_long_region = dataregion_filtrada.melt(
            id_vars=['Ano'], value_vars=regioes, 
            var_name='Regiao', value_name='Quantidade'
        )
        #Construção do grafico
        fig_region = px.line(
            data_long_region,
            x="Ano",
            y="Quantidade",
            color="Regiao",
            title="Série Temporal por Região",
            labels={"Quantidade": "Quantidade", "Ano": "Ano", "Regiao": "Regiao"}
        )
        #Parametros do Grafico
        fig_region.update_layout(
        xaxis=dict(
        title="Ano",
        titlefont=dict(size=20),  
        tickfont=dict(size=16),showgrid=False
    ),yaxis=dict(showgrid=False,title="",tickfont=dict(size=16)))
        st.plotly_chart(fig_region)
    else:
        st.warning("Selecione pelo menos uma região para visualizar o gráfico.")

with aba4:
    st.header("Série Temporal por DevName")
    #Filtro: Seleção das categorias
    devname = st.multiselect(
        "Selecione as Categorias:",
        options=datadevname.columns[1:],
        default=datadevname.columns[2]
    )
    #Filtro: Intervalo de anos
    anos_devname = st.slider(
        "Selecione o intervalo de anos:",
        min_value=int(datadevname['Ano'].min()),
        max_value=int(datadevname['Ano'].max()),
        value=(int(datadevname['Ano'].min()), int(datadevname['Ano'].max())),key='slider_devname'
    )
    datadevname_filtrada = datadevname[
        (datadevname['Ano'] >= anos_devname[0]) & 
        (datadevname['Ano'] <= anos_devname[1])
    ]
    if devname:
        #Tratamento dos dados
        data_long_devname = datadevname_filtrada.melt(
            id_vars=['Ano'], value_vars=devname, 
            var_name='Regiao', value_name='Quantidade'
        )
        #construção do grafico
        fig_devname = px.line(
            data_long_devname,
            x="Ano",
            y="Quantidade",
            color="Regiao",
            title="Série Temporal por DevName",
            labels={"Quantidade": "Quantidade", "Ano": "Ano", "Regiao": "Regiao"})
        #parametros do grafico
        fig_devname.update_layout(
        xaxis=dict(
        title="Ano",
        titlefont=dict(size=20),  
        tickfont=dict(size=16),showgrid=False
    ),yaxis=dict(showgrid=False,title="",tickfont=dict(size=16)))
        st.plotly_chart(fig_devname)
    else:
        st.warning("Selecione pelo menos uma categoria para visualizar o gráfico.")
#fonte dos dados
st.markdown("[Fonte dos Dados](https://www.kaggle.com/datasets/ammaraahmad/immigration-to-canada)")
        
