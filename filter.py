import streamlit as st
import pandas as pd
from datetime import datetime

def searchLocation(TODOS):
    with st.container(border=4):
        pass

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
            st.write(f"Total de impressoras = :orange[{listafiltrada}]")
            # Converte a coluna 'ATUALIZADO' para datetime, caso não esteja no formato correto
            location['ATUALIZADO'] = pd.to_datetime(location['ATUALIZADO'], errors='coerce', dayfirst=True)
            # Verifica se a conversão deu certo antes de usar .dt
            if location['ATUALIZADO'].isnull().any():
                st.warning("Alguns valores de 'ATUALIZADO' estão vazias.")
            # Formata a coluna 'ATUALIZADO' para o formato de data
            location['ATUALIZADO'] = location['ATUALIZADO'].dt.strftime('%d/%m/%Y')
            # Exibe o dataframe filtrado
            st.write(location)
            # Exibe a contagem por localidade
            st.dataframe(contagem_por_localidade, hide_index=True)
        # Se o botão foi pressionado mas não há pesquisa
        elif searchButton:
            st.write("Por favor, insira um termo de pesquisa.")

def filterByAll(TODOSS):
    with st.container(border=4):
        selectedBox = ['TIPO','NUMERO DE SERIE', 'SETOR', 'EMPRESA', 'ATUALIZADO', 'PRINTWAY', 'OBSERVAÇÃO']

        filtered = st.selectbox("Escolha a categoria e digite sua busca 🕵️",(selectedBox))

        getByPrint = st.text_input("Digite sua pesquisa 🧐", placeholder="Digite aqui...").upper()
        # Adiciona o botão de pesquisa
        searchButton = st.button('Pesquisar🔎')

        if searchButton and getByPrint:

            location = TODOSS.loc[TODOSS[filtered].str.contains(getByPrint, case=False, na=False)]

            # Conta o número de impressoras filtradas
            listafiltrada = len(location['NUMERO DE SERIE'])

            # Agrupa por localidade e conta a quantidade
            contagem_por_localidade = location.groupby('LOCALIZAÇÃO').size().reset_index(name='Quant')

            # Exibe os resultados
            st.write(f"Total de impressoras = :orange[{listafiltrada}]")

            # Converte a coluna 'ATUALIZADO' para datetime, caso não esteja no formato correto
            location['ATUALIZADO'] = pd.to_datetime(location['ATUALIZADO'], errors='coerce', dayfirst=True)

            # Verifica se a conversão deu certo antes de usar .dt
            if location['ATUALIZADO'].isnull().any():
                st.warning("Alguns valores de 'ATUALIZADO' estão vazias.")

            # Formata a coluna 'ATUALIZADO' para o formato de data
            location['ATUALIZADO'] = location['ATUALIZADO'].dt.strftime('%d/%m/%Y')

            # Exibe o dataframe filtrado
            st.write(location)

            # Exibe a contagem por localidade
            st.dataframe(contagem_por_localidade, hide_index=True)

        # Se o botão foi pressionado mas não há pesquisa
        elif searchButton:
            st.write("Por favor, insira um termo de pesquisa.")

def listAllprint(TODOS, TODOSS):
    with st.container(border=4):
        st.write("Relatorio com todas as :blue[impressora]  🖨️")
        with st.expander("Clique para expandir tabela com todas impressoras"):
            todasImpressoras = len(TODOS['NUMERO DE SERIE'])
            st.write('ToTal: ', todasImpressoras)
            TODOS['ATUALIZADO'] = TODOS['ATUALIZADO'].dt.strftime('%d/%m/%Y')
            st.dataframe(TODOS, hide_index=True)


        # container com 3 colunas com todas impressoras
        coutGeral = TODOSS['EMPRESA'].value_counts().reset_index(name='QUANT.')
        todosTipos = TODOSS['TIPO'].value_counts().reset_index(name='QUANT.')
        todosModelos = TODOS['MODELO'].value_counts().reset_index(name='QUANT.')
        todosLocalizacao = TODOS['LOCALIZAÇÃO'].value_counts().reset_index(name='QUANT.')

        #container
        with st.expander("Clique para expandir relatório com todas impressora"):

            container2 = st.container(border=4)
            tab1, tab2, tab3, tab4 = container2.tabs(["Modelos", "Empresa", "Tipo", "Local"])

            with tab1:
                st.header("Modelos")
                st.dataframe(todosModelos, hide_index=True)
            with tab2:
                st.header("Empresa")
                st.dataframe(coutGeral, hide_index=True)
            with tab3:
                st.header("Tipo")
                st.dataframe(todosTipos, hide_index=True)
            with tab4:
                st.header("Local")
                st.dataframe(todosLocalizacao, hide_index=True)