import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
import tempfile
from datetime import datetime
import pytz
import os
import create_uuid

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

    # Título fixo na interface (não muda)
    st.subheader("Crie ordens de serviço, recibos e outros documentos personalizados.")

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
