import pandas as pd
import streamlit as st
import time
from datetime import datetime
import openpyxl as op
import pytz

import validation
import filters
import images
import dashBoard
from data_request import load_data


from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
import tempfile
import os
import create_uuid



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

# Busca os dados
inventory_data = load_data()

# Busca as sheet_name
all_printers = inventory_data['PRINTERS_INVENTORY']
stock = inventory_data['estoque']
all_computers = inventory_data['COMPUTER']
# end

BASIC_COLUMNS = [
    'MODELO',
    'TIPO',
    'NUMERO DE SERIE',
    'LOCALIZAÇÃO',
    'SETOR',
    'EMPRESA',
    'ATUALIZADO',
    'PRINTWAY'
]

FULL_COLUMNS = BASIC_COLUMNS + ['OBSERVAÇÃO']

TODOS = all_printers[BASIC_COLUMNS].copy()
TODOSS = all_printers[FULL_COLUMNS].copy()


# selected
indiceSelect = TODOS['LOCALIZAÇÃO'].drop_duplicates().sort_values()

with st.sidebar:
    with st.spinner("Loading..."):
        time.sleep(1)
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


# Adicionando a mensagem busca de computadores
#selected de TI

indiceSelect_ti = all_computers ['LOCALIDADE'].drop_duplicates().sort_values()

with st.sidebar:
    with st.spinner("Loading..."):
        time.sleep(1)
    st.success("So Lagos TI 💻")

filteredToLocation_ti = add_selectbox = st.sidebar.selectbox(
    "BUSCA POR LOCAL 🔎🔽 ",
    (indiceSelect_ti)
)

location_ti = all_computers.loc[all_computers['LOCALIDADE'] == filteredToLocation_ti]
location_ti['ATUALIZADO'] = all_computers['DATA'].dt.strftime('%d/%m/%Y')

coutPrint_ti = location_ti['MODELO'].value_counts().reset_index(name='QUANT.')
coutEmpresa_ti = location_ti['EMPRESA'].value_counts().reset_index(name='QUANT.')
coutType_ti = location_ti['TIPO'].value_counts().reset_index(name='QUANT.')

with st.sidebar:
    st.dataframe(coutPrint_ti, hide_index=True)
    st.dataframe(coutEmpresa_ti, hide_index=True)
    st.dataframe(coutType_ti, hide_index=True)


# Funcoes de Buscas
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


# Função para gerar o PDF
uuid_8_caracteres = create_uuid.gerar_uuid_limitado(8)

def limitar_texto(texto, limite=50):
    return texto[:limite] + "..." if len(texto) > limite else texto

def gerar_os_pdf(dados, filename, titulo_pdf):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    # Data automática
    fuso_horario = pytz.timezone("America/Sao_Paulo")
    data_atual = datetime.now(fuso_horario).strftime("%d/%m/%Y")

    # Título do PDF baseado na seleção
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 50, f"id: {uuid_8_caracteres}")
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2, height - 50, titulo_pdf)  # Título baseado na seleção
    c.setFont("Helvetica", 12)
    c.drawString(450, height - 50, f"Data: {data_atual}")

    # Informações do Cliente
    y_cliente = height - 90
    c.drawString(50, y_cliente, f"Cliente: {limitar_texto(dados['cliente'])}")
    c.drawString(50, y_cliente - 20, f"Endereço: {limitar_texto(dados['endereco'])}")
    c.drawString(50, y_cliente - 40, f"Contato: {limitar_texto(dados['contato'])}")

    # Tabela de Serviços
    y_tabela = y_cliente - 90
    dados_tabela = [["Quantidade", "Descrição do Serviço"]] + [[s["quantidade"], limitar_texto(s["descricao"])] for s in dados["servicos"]]

    tabela = Table(dados_tabela, colWidths=[70, 450])
    tabela.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, -1), "Helvetica"),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))

    tabela.wrapOn(c, width, height)
    tabela.drawOn(c, 50, y_tabela - (len(dados["servicos"]) * 20))

    # Seção de "Serviço Prestado" no final da página
    y_servicos = 60
    box_height = max(120, len(dados["servicos"]) * 15 + 120)

    # Caixa de serviço prestado
    c.setStrokeColor(colors.black)
    c.rect(50, y_servicos, 240, box_height, stroke=1, fill=0)
    c.rect(310, y_servicos, 240, box_height, stroke=1, fill=0)

    c.setFont("Helvetica", 9)
    c.drawString(60, y_servicos + box_height - 30, "Serviço Prestado:")
    c.drawString(320, y_servicos + box_height - 30, "Serviço Prestado:")

    y_lista = y_servicos + box_height - 60
    for idx, servico in enumerate(dados["servicos"]):
        texto_limitado = f"{servico['quantidade']}x {limitar_texto(servico['descricao'])}"
        c.drawString(60, y_lista, texto_limitado)
        c.drawString(320, y_lista, texto_limitado)
        y_lista -= 30 if idx == len(dados["servicos"]) - 1 else 15

    # Linhas de assinatura
    assinatura_y = y_servicos + 30
    c.line(60, assinatura_y, 250, assinatura_y)
    c.line(320, assinatura_y, 510, assinatura_y)

    c.setFont("Helvetica", 11)
    c.drawString(60, assinatura_y - 10, "Assinatura do Cliente:")
    c.drawString(320, assinatura_y - 10, "Assinatura do Técnico:")

    c.save()

def gerar_ordem_servico():
    st.title("Gerador de Ordem de Serviço")

    # Selecione o tipo de documento (manter na sessão)
    if 'tipo_servico' not in st.session_state:
        st.session_state.tipo_servico = "ORDEM DE SERVIÇO"  # Valor inicial

    # Selecione o tipo de documento
    tipo_servico = st.selectbox("SELECIONE O TIPO DE DOCUMENTO",
                                ["RECIBO DE ENTREGA", "ORDEM DE SERVIÇO", "PEDIDO DE MERCADORIA"],
                                index=["RECIBO DE ENTREGA", "ORDEM DE SERVIÇO", "PEDIDO DE MERCADORIA"].index(st.session_state.tipo_servico))

    # Salvar a seleção do tipo de serviço no session_state
    st.session_state.tipo_servico = tipo_servico

    # Formulário para dados da ordem de serviço
    with st.form(key="ordem_servico_form"):
        cliente = st.text_input("Nome do Cliente", value=st.session_state.get("cliente", ""))
        endereco = st.text_input("Endereço", value=st.session_state.get("endereco", ""))
        contato = st.text_input("Contato", value=st.session_state.get("contato", ""))

        st.subheader("Serviços Prestados")
        servicos = st.session_state.get("servicos", [])
        num_servicos = st.number_input("Número de Serviços", min_value=1, step=1, value=max(len(servicos), 1))

        servicos.clear()
        for i in range(num_servicos):
            descricao = st.text_input(f"Descrição {i+1}", key=f"desc{i}", max_chars=50)
            quantidade = st.number_input(f"Quantidade {i+1}", min_value=1, step=1, key=f"qtd{i}")
            servicos.append({"descricao": descricao, "quantidade": quantidade})

        if st.form_submit_button("Salvar Dados"):
            st.session_state.update({"cliente": cliente, "endereco": endereco, "contato": contato, "servicos": servicos})
            st.success("Dados salvos com sucesso!")

    if st.button("Gerar PDF"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
            gerar_os_pdf(st.session_state, tmpfile.name, st.session_state.tipo_servico)  # Passando o título para a função
            st.success("PDF gerado com sucesso!")
            with open(tmpfile.name, "rb") as file:
                st.download_button("Baixar PDF", file, "ordem_de_servico.pdf", "application/pdf")

if __name__ == "__main__":
    gerar_ordem_servico()

st.write("Relatorio :blue[TI]  💻")
df = st.dataframe(location_ti, hide_index=True)

# Remover o nome de deploy
st.markdown(
    """
        <style>
            .st-emotion-cache-1wbqy5l {display: none;}
        </style>
    """,
    unsafe_allow_html=True
)
