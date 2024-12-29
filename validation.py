import streamlit as st
import time

passwords_correct = "1234"

def repeat_password():
    st.error("digite sua senha")

def validateUser():
    while True:
        password = st.text_input("Digite a Senha:", type="password", placeholder="Digite a Senha...")
        if password == passwords_correct:
            st.success("Senha correta. Acesso liberado!")
            time.sleep(2)
            break
        else:
            repeat_password()

