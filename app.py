import pandas as pd
import streamlit as st
import time
from datetime import datetime
import openpyxl as op

import validation
import filters
import images

# msg de saudação
saudacao = "Meu camarada da cidade de Londres Flavio Andrade"
print(saudacao)

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
            .st-emotion-cache-1wbqy5l {display: none;}
            .stToolbarActionButton {display: none;}

            ._profilePreview_gzau3_63 {display: none;}
            ._profileContainer_gzau3_53 {display: none;}

            .css-18e3th9 {
                visibility: hidden;
                display: none;
            }
            .css-1f1i60u {
                visibility: hidden;
            }
            .css-1gg49ve {
                display: none;
            }
            .css-1y0t01g {
                display: none;
            }
        </style>
    """,
    unsafe_allow_html=True
)

validation.validateUser()

caminho_rede = "https://github.com/flavio-foa-dev/excel/raw/main/data_printer.xlsm"
data = pd.read_excel(caminho_rede, sheet_name='Controle_Inventario_Impressoras')
historico = pd.read_excel(caminho_rede, sheet_name='HISTORICO')

TODOS = data[['MODELO', 'TIPO','NUMERO DE SERIE', 'LOCALIZAÇÃO', 'SETOR', 'EMPRESA', 'ATUALIZADO', 'PRINTWAY']]
TODOSS = data[['MODELO','TIPO', 'NUMERO DE SERIE', 'LOCALIZAÇÃO', 'SETOR', 'EMPRESA', 'ATUALIZADO', 'PRINTWAY', 'OBSERVAÇÃO']]

# selected
indiceSelect = TODOS['LOCALIZAÇÃO'].drop_duplicates().sort_values()
print('Pritando indice')
print(indiceSelect)

with st.sidebar:
    with st.spinner("Loading..."):
        time.sleep(2)
    st.success("So Lagos Impressora 🖨️")

filteredToLocation = add_selectbox = st.sidebar.selectbox(
    "BUSCA POR LOCAL 🔎🔽 ",
    (indiceSelect)
)
print('Minha Escolha foi: ',filteredToLocation )

location = TODOS.loc[TODOS['LOCALIZAÇÃO'] == filteredToLocation]
location['ATUALIZADO'] = location['ATUALIZADO'].dt.strftime('%d/%m/%Y')
print(location)

st.header("Impressora por :blue[Localização 🖨️]")
#locationN = location.drop(['TIPO', 'EMPRESA'], axis=1)
df = st.dataframe(location, hide_index=True)

#Tabela  de  impressoras filtradas sideBar
total = len(location['NUMERO DE SERIE'])
st.sidebar.title(total)

coutPrint = location['MODELO'].value_counts().reset_index(name='QUANT.')
coutEmpresa = location['EMPRESA'].value_counts().reset_index(name='QUANT.')
coutType= location['TIPO'].value_counts().reset_index(name='QUANT.')


df_concat = pd.concat([coutEmpresa, coutType]).fillna('')

with st.sidebar:
    st.dataframe(coutPrint, hide_index=True)
    st.dataframe(coutEmpresa, hide_index=True)
    st.dataframe(coutType, hide_index=True)

    #st.dataframe(df_concat, hide_index=True)


# Obtendo o ano atual
current_year = datetime.now().year

# Adicionando a mensagem de copyright com o ano atual
st.sidebar.markdown(
    f"""
    ---
    &copy; {current_year} Desenvolvido 🚀 Flavio Andrade.
    """
)

filters.filterByModel(TODOS)

filters.filterByAll(TODOSS)

filters.listAllprint(TODOS, TODOSS)

images.show_imagens()

images.show_video()

# Remover o nome de deploy
st.markdown(
    """
        <style>
            .st-emotion-cache-1wbqy5l {display: none;}
        </style>
    """,
    unsafe_allow_html=True
)
