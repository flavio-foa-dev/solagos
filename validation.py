import streamlit as st
import time

passwords_correct = "1234"
password_key = f"foa_{time.time()}"

def repeat_password():
    st.error("Senha incorreta. Tente novamente.")

def validateUser():
    while True:
        password = st.text_input("Digite a Senha:", type="password", placeholder="Digite a Senha...", key=password_key)
        if password == passwords_correct:
            st.success("Senha correta. Acesso liberado!")
            time.sleep(2)
            break
        if password == "":
                st.error("A senha não pode ser vazia. Por favor, digite a senha.")
                continue
        else:
            repeat_password()

