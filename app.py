import pandas as pd
import streamlit as st
import time
import os
import locale
from datetime import datetime
import openpyxl as op

# msg de saudação
saudacao = "Meu camarada da cidade de Londres Flavio Andrade"
print(saudacao)

locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
print('meu caminho separado',os.sep)

st.set_page_config(
    page_title="So Lagos Impressoras",
    page_icon="icone.png",
    layout="wide",
    initial_sidebar_state="expanded"  # Pode ser "auto", "expanded" ou "collapsed"
)

# Remover o nome de deploy
st.markdown(
    """
    <style>
    .st-emotion-cache-1wbqy5l {display: none;}  /* Seleciona e oculta o nome do deploy */

    </style>
    """,
    unsafe_allow_html=True,
)

# validação de caminho de data
dados = 123  # ou pode ser None, [], etc.
if not dados:  # Verifica se a variável está vazia
    print("Erro: os dados estão vazios!")
else:
    print(f"Dados encontrados: {dados}")


caminho_rede = "https://github.com/flavio-foa-dev/excel/raw/main/data_printer.xlsm"

data = pd.read_excel(caminho_rede, sheet_name='Controle_Inventario_Impressoras')
historico = pd.read_excel(caminho_rede, sheet_name='HISTORICO')
print(data)

TODOS = data[['MODELO', 'NUMERO DE SERIE', 'LOCALIZAÇÃO', 'SETOR', 'EMPRESA', 'ATUALIZADO']]
# TODOS = data[[ 'MODELO', 'NUMERO DE SERIE', 'LOCALIZAÇÃO', 'SETOR', 'EMPRESA']]

# selected
indiceSelect = TODOS['LOCALIZAÇÃO'].drop_duplicates().sort_values()
print('Pritando indice')
print(indiceSelect)

with st.sidebar:
    with st.spinner("Loading..."):
        time.sleep(2)
    st.success("So Lagos Impressora 🖨️")

filteredToLocation = add_selectbox = st.sidebar.selectbox(
    "BUSCA PO LOCAL🔎🔽 ",
    (indiceSelect)
)

print('Minha Escolha foi: ',filteredToLocation )

location = TODOS.loc[TODOS['LOCALIZAÇÃO'] == filteredToLocation]
location['ATUALIZADO'] = location['ATUALIZADO'].dt.strftime('%d/%m/%Y')
print(location)

st.header("Impressora por :blue[Localização 🖨️]")
df = st.dataframe(location, hide_index=True)

#Tabela  de  impressoras filtradas sideBar
total = len(location['NUMERO DE SERIE'])
st.sidebar.title(total)

coutEmpresa = location['EMPRESA'].value_counts().reset_index(name='QUANT.')
coutPrint = location['MODELO'].value_counts().reset_index(name='QUANT.')

with st.sidebar:
    st.dataframe(coutPrint, hide_index=True)
    st.dataframe(coutEmpresa, hide_index=True)

# Obtendo o ano atual
current_year = datetime.now().year

# Adicionando a mensagem de copyright com o ano atual
st.sidebar.markdown(
    f"""
    ---
    &copy; {current_year} Desenvolvido 🚀 Flavio Andrade.
    """
)

# container com 3 colunas com todas impressoras
coutGeral = data['EMPRESA'].value_counts().reset_index(name='QUANT.')
todosTipos = data['TIPO'].value_counts().reset_index(name='QUANT.')

todosModelos = TODOS['MODELO'].value_counts().reset_index(name='QUANT.')
#todosModelos.name = 'TOTAL'

todosLocalizacao = TODOS['LOCALIZAÇÃO'].value_counts().reset_index(name='QUANT.')
#todosModelos.name = 'TOTAL'

#container = st.container(border=4)
#col1, col2, col3, col4 = container.columns([1, 1, 1, 1])
#with col1:
#    st.header("MODELOS")
#   st.write(todosModelos)

#with col2:
#    st.header("EMPRESA")
#    st.write(coutGeral)

#with col3:
#    st.header("TIPO")
#   st.write(todosTipos)

#with col4:
#    st.header("LOCAL")
#    st.write(todosLocalizacao)

# CAMPO DE PESQUISA COM TODAS AS IMPRESSORAS

pesquisa = st.text_input("Digite o modelo da impressora: 🧐🕵️", placeholder="Digite sua pesquisa aqui...   🔎").upper()
botao = st.button('Pesquisar🔎')
if botao and pesquisa:
    st.write(f"voce pesquisou por: {pesquisa}")

    location = TODOS.loc[TODOS['MODELO'].str.contains(pesquisa)]
    listafiltrada = len(location['NUMERO DE SERIE'])
    st.write(f"total de impressoras: :orange[{listafiltrada}]")
    st.write(location)

# Historico das impressoras:
st.header(":orange[Historico das impressora]  🕡")
with st.expander("Clique para expandir historico"):
    todasImpressoras = len(historico['NUMERO DE SERIE'])
    st.write('ToTal: ', todasImpressoras)
    hisgroup = historico.groupby(by=['NUMERO DE SERIE'])['OBSERVAÇÃO'].apply(list)
    st.dataframe(hisgroup)


st.header("Relatorio com todas as :blue[impressora]  ⬇️")
with st.expander("Clique para expandir tabela com todas impressoras"):
    todasImpressoras = len(TODOS['NUMERO DE SERIE'])
    st.write('ToTal: ', todasImpressoras)
    TODOS
# abas
#container
with st.expander("Clique para expandir relatório com todas impressora"):

    container2 = st.container(border=4)
    tab1, tab2, tab3, tab4 = container2.tabs(["Modelos", "Empresa", "Tipo", "Local"])

    with tab1:
        st.header("Modelos")
        st.write(todosModelos)
    with tab2:
        st.header("Empresa")
        st.write(coutGeral)
    with tab3:
        st.header("Tipo")
        st.write(todosTipos)
    with tab4:
        st.header("Local")
        st.write(todosLocalizacao)
