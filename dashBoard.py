import streamlit as st

locationSelect = ['SAUDE', 'PACO', 'SEDUC', 'CARTORIO', 'PARTICULAR', 'SEPOL', 'ITABORAI', 'ARRAIAL']

def dashBoardSelect():
    setored = add_selectbox = st.selectbox(
        "ANALISE DE COPIAS 🔎",
        (locationSelect)
    )