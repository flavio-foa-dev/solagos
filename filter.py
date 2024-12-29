import streamlit as st
import pandas as pd
from datetime import datetime

def filterByModel(TODOS):
    with st.container(border=4):
        # Solicita a entrada do usuário
        getByPrint = st.text_input("Digite o modelo da impressora: 🧐🕵️", placeholder="Digite sua pesquisa aqui...").upper()
        # Adiciona o botão de pesquisa
        searchButton = st.button('Pesquisa🔎')
        if searchButton and getByPrint:  # Verifica se o botão foi pressionado e a pesquisa não está vazia
            # Exibe o termo da pesquisa
            st.write(f"Você pesquisou por: {getByPrint.lower()}")
            # Filtra o dataframe usando a pesquisa
            location = TODOS.loc[TODOS['MODELO'].str.contains(getByPrint, case=False, na=False)]
            # Conta o número de impressoras filtradas
            listafiltrada = len(location['NUMERO DE SERIE'])
            # Agrupa por localidade e conta a quantidade
            contagem_por_localidade = location.groupby('LOCALIZAÇÃO').size().reset_index(name='Quant')
            # Exibe os resultados
            st.write(f"Total de impressoras: :orange[{listafiltrada}]")
            # Converte a coluna 'ATUALIZADO' para datetime, caso não esteja no formato correto
            location['ATUALIZADO'] = pd.to_datetime(location['ATUALIZADO'], errors='coerce', dayfirst=True)
            # Verifica se a conversão deu certo antes de usar .dt
            if location['ATUALIZADO'].isnull().any():
                st.warning("Alguns valores de 'ATUALIZADO' estao  vazias.")
            # Formata a coluna 'ATUALIZADO' para o formato de data
            location['ATUALIZADO'] = location['ATUALIZADO'].dt.strftime('%d/%m/%Y')
            # Exibe o dataframe filtrado
            st.write(location)
            # Exibe a contagem por localidade
            st.dataframe(contagem_por_localidade, hide_index=True)
        # Se o botão foi pressionado mas não há pesquisa
        elif searchButton:
            st.write("Por favor, insira um termo de pesquisa.")
