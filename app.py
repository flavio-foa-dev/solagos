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


from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
import tempfile



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


# Função para gerar o PDF
def gerar_os_pdf(dados, filename):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    # Data automática
    fuso_horario = pytz.timezone("America/Sao_Paulo")  # Ajuste para o fuso horário que você precisa
    # Data e hora no fuso horário correto
    data_atual = datetime.now(fuso_horario).strftime("%d/%m/%Y")
    print(data_atual)

    # Título centralizado
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2, height - 50, "ORDEM DE SERVIÇO")

    # Data
    c.setFont("Helvetica", 12)
    c.drawString(450, height - 50, f"Data: {data_atual}")

    # Informações do Cliente
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 90, f"Cliente: {dados['cliente']}")
    c.drawString(50, height - 110, f"Endereço: {dados['endereco']}")
    c.drawString(50, height - 130, f"Contato: {dados['contato']}")

    # Tabela de Serviços
    dados_tabela = [["Quantidade", "Descrição do Serviço"]]
    for servico in dados["servicos"]:
        dados_tabela.append([servico["quantidade"], servico["descricao"]])

    tabela = Table(dados_tabela, colWidths=[80, 400])
    tabela.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, -1), "Helvetica"),
        ('FONTSIZE', (0, 0), (-1, -1), 12)
    ]))

    tabela.wrapOn(c, width, height)
    tabela.drawOn(c, 50, height - 250)

    # Rodapé com caixas de assinatura e serviços prestados
    c.setStrokeColor(colors.black)
    c.rect(50, 50, 240, 100, stroke=1, fill=0)
    c.rect(310, 50, 240, 100, stroke=1, fill=0)

    c.setFont("Helvetica-Bold", 12)
    c.drawString(60, 130, "Serviço Prestado:")
    c.drawString(320, 130, "Serviço Prestado:")

    c.setFont("Helvetica", 10)
    y_position = 110
    for servico in dados["servicos"]:
        if y_position >= 80:
            c.drawString(60, y_position, f"{servico['quantidade']}x {servico['descricao']}")
            c.drawString(320, y_position, f"{servico['quantidade']}x {servico['descricao']}")
            y_position -= 15

    # Linhas para assinatura
    c.line(60, 65, 250, 65)  # Linha para assinatura do cliente
    c.line(320, 65, 510, 65)  # Linha para assinatura do técnico

    c.setFont("Helvetica", 12)
    c.drawString(60, 55, "Assinatura do Cliente:")
    c.drawString(320, 55, "Assinatura do Técnico:")

    c.save()

# Função principal que gera a interface e processa o formulário
def gerar_ordem_servico():
    # Título da aplicação
    st.title("Gerador de Ordem de Serviço")

    # Usar o formulário para controlar quando o conteúdo é submetido
    with st.form(key="ordem_servico_form"):
        # Recuperando dados do session_state (caso existam)
        cliente = st.text_input("Nome do Cliente", value=st.session_state.get("cliente", ""))
        endereco = st.text_input("Endereço", value=st.session_state.get("endereco", ""))
        contato = st.text_input("Contato", value=st.session_state.get("contato", ""))

        st.subheader("Serviços Prestados")
        servicos = st.session_state.get("servicos", [])

        # Definir o número de serviços
        # Garante que o número de serviços será no mínimo 1
        num_servicos = st.number_input("Número de Serviços", min_value=1, step=1, value=max(len(servicos), 1))

        # Preencher ou ajustar a lista de serviços
        servicos.clear()  # Limpa a lista de serviços, caso a quantidade de serviços seja alterada
        for i in range(num_servicos):
            descricao = st.text_input(f"Descrição {i+1}", value=servicos[i]["descricao"] if i < len(servicos) else "", key=f"desc{i}")
            quantidade = st.number_input(f"Quantidade {i+1}", min_value=1, step=1, value=servicos[i]["quantidade"] if i < len(servicos) else 1, key=f"qtd{i}")

            # Atualizando a lista de serviços
            if i < len(servicos):
                servicos[i] = {"descricao": descricao, "quantidade": quantidade}
            else:
                servicos.append({"descricao": descricao, "quantidade": quantidade})

        # Submeter o formulário
        submit_button = st.form_submit_button(label="Salvar Dados")

        # Atualiza o session_state com os dados preenchidos
        if submit_button:
            st.session_state["cliente"] = cliente
            st.session_state["endereco"] = endereco
            st.session_state["contato"] = contato
            st.session_state["servicos"] = servicos
            st.success("Dados salvos com sucesso!")

    # Gerar PDF quando o botão for pressionado
    if st.button("Gerar PDF"):
        dados = {
            "cliente": st.session_state.get("cliente", ""),
            "endereco": st.session_state.get("endereco", ""),
            "contato": st.session_state.get("contato", ""),
            "servicos": st.session_state.get("servicos", [])
        }
        # Gerar o PDF em um arquivo temporário
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
            gerar_os_pdf(dados, tmpfile.name)
            st.success("PDF gerado com sucesso!")
            with open(tmpfile.name, "rb") as file:
                st.download_button("Baixar PDF", file, "ordem_de_servico.pdf", "application/pdf")

# Executar a função principal
if __name__ == "__main__":
    gerar_ordem_servico()





# Remover o nome de deploy
st.markdown(
    """
        <style>
            .st-emotion-cache-1wbqy5l {display: none;}
        </style>
    """,
    unsafe_allow_html=True
)
