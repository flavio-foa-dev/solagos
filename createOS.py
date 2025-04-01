import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
import tempfile
from datetime import datetime

def gerar_os_pdf(dados, filename):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    # Data automática
    data_atual = datetime.now().strftime("%d/%m/%Y")

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

# Interface Streamlit
st.title("Gerador de Ordem de Serviço")

cliente = st.text_input("Nome do Cliente")
endereco = st.text_input("Endereço")
contato = st.text_input("Contato")

st.subheader("Serviços Prestados")
servicos = []
num_servicos = st.number_input("Número de Serviços", min_value=1, step=1, value=1)

for i in range(num_servicos):
    st.write(f"Serviço {i+1}")
    descricao = st.text_input(f"Descrição {i+1}", key=f"desc{i}")
    quantidade = st.number_input(f"Quantidade {i+1}", min_value=1, step=1, key=f"qtd{i}")
    servicos.append({"descricao": descricao, "quantidade": quantidade})

if st.button("Gerar PDF"):
    dados = {
        "cliente": cliente,
        "endereco": endereco,
        "contato": contato,
        "servicos": servicos
    }
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
        gerar_os_pdf(dados, tmpfile.name)
        st.success("PDF gerado com sucesso!")
        with open(tmpfile.name, "rb") as file:
            st.download_button("Baixar PDF", file, "ordem_de_servico.pdf", "application/pdf")
