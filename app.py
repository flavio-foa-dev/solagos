import pandas as pd
import streamlit as st
import time
from datetime import datetime
import openpyxl as op

import validation
import filters
import images
import dashBoard

# msg de saudação
saudacao = "Meu camarada da cidade de Londres Flavio Andrade"
print(saudacao)
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

caminho_rede = "https://github.com/flavio-foa-dev/excel/raw/main/data_printer.xlsx"
#caminho_rede = "/home/flavio/Documentos/2024/sologas/solagos/data_printer.xlsx"

data = pd.read_excel(caminho_rede, sheet_name='PRINTERS_INVENTORY')
stock = pd.read_excel(caminho_rede, sheet_name='estoque')

TODOS = data[['MODELO', 'TIPO','NUMERO DE SERIE', 'LOCALIZAÇÃO', 'SETOR', 'EMPRESA', 'ATUALIZADO', 'PRINTWAY']]
TODOSS = data[['MODELO','TIPO', 'NUMERO DE SERIE', 'LOCALIZAÇÃO', 'SETOR', 'EMPRESA', 'ATUALIZADO', 'PRINTWAY', 'OBSERVAÇÃO']]

# selected
indiceSelect = TODOS['LOCALIZAÇÃO'].drop_duplicates().sort_values()

with st.sidebar:
    with st.spinner("Loading..."):
        time.sleep(2)
    st.success("So Lagos Impressora 🖨️")

filteredToLocation = add_selectbox = st.sidebar.selectbox(
    "BUSCA POR LOCAL 🔎🔽 ",
    (indiceSelect)
)

location = TODOS.loc[TODOS['LOCALIZAÇÃO'] == filteredToLocation]
location['ATUALIZADO'] = location['ATUALIZADO'].dt.strftime('%d/%m/%Y')

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

st.dataframe(stock.fillna(""), hide_index=True)

df = pd.DataFrame(indiceSelect)
# Título da aplicação
st.title('CARD BY LOCATION')

# Dividir a tela em 3 colunas
col1, col2, col3 = st.columns(3)

# Criar cards para cada linha e distribuir em 3 colunas
for i in range(0, len(df), 3):  # Itera em blocos de 3 linhas

    with col1:
        if i < len(df):
            row = df.iloc[i]

            loca = TODOS.loc[TODOS['LOCALIZAÇÃO'] == row['LOCALIZAÇÃO']]
            total = len(loca['NUMERO DE SERIE'])

            st.markdown(f"""
                <div style="
                    border: 2px solid #f2a73d;
                    border-radius: 15px;
                    padding: 20px;
                    margin-bottom: 20px;
                    background-color: #2c3e50;
                    box-sizing: border-box;
                    word-wrap: break-word;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
                    transition: transform 0.3s ease;">
                    <h3 style="color: #ecf0f1; text-align: center; margin: 0 0 10px 0; font-size: 1.5em;">{row['LOCALIZAÇÃO']}</h3>
                    <p style="color: #ecf0f1; text-align: center; font-size: 1.2em;"><strong>Total:</strong> {total}</p>
                </div>
            """, unsafe_allow_html=True)

    with col2:
        if i + 1 < len(df):
            row = df.iloc[i + 1]

            loca = TODOS.loc[TODOS['LOCALIZAÇÃO'] == row['LOCALIZAÇÃO']]
            total = len(loca['NUMERO DE SERIE'])

            st.markdown(f"""
                <div style="
                    border: 2px solid #f2a73d;
                    border-radius: 15px;
                    padding: 20px;
                    margin-bottom: 20px;
                    background-color: #2c3e50;
                    box-sizing: border-box;
                    word-wrap: break-word;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
                    transition: transform 0.3s ease;">
                    <h3 style="color: #ecf0f1; text-align: center; margin: 0 0 10px 0; font-size: 1.5em;">{row['LOCALIZAÇÃO']}</h3>
                    <p style="color: #ecf0f1; text-align: center; font-size: 1.2em;"><strong>Total:</strong> {total}</p>
                </div>
            """, unsafe_allow_html=True)

    with col3:
        if i + 2 < len(df):
            row = df.iloc[i + 2]

            loca = TODOS.loc[TODOS['LOCALIZAÇÃO'] == row['LOCALIZAÇÃO']]
            total = len(loca['NUMERO DE SERIE'])

            st.markdown(f"""
                <div style="
                    border: 2px solid #f2a73d;
                    border-radius: 15px;
                    padding: 20px;
                    margin-bottom: 20px;
                    background-color: #2c3e50;
                    box-sizing: border-box;
                    word-wrap: break-word;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
                    transition: transform 0.3s ease;">
                    <h3 style="color: #ecf0f1; text-align: center; margin: 0 0 10px 0; font-size: 1.5em;">{row['LOCALIZAÇÃO']}</h3>
                    <p style="color: #ecf0f1; text-align: center; font-size: 1.2em;"><strong>Total:</strong> {total}</p>
                </div>
            """, unsafe_allow_html=True)


dashBoard.dashBoardSelect()

# Remover o nome de deploy
st.markdown(
    """
        <style>
            .st-emotion-cache-1wbqy5l {display: none;}
        </style>
    """,
    unsafe_allow_html=True
)
