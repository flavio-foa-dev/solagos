import streamlit as st
import images

# Funções para cada página
def home():
    st.title("Bem-vindo à Página Inicial")
    st.write("Esta é a página inicial do site. Aqui você pode colocar informações gerais sobre seu projeto ou empresa.")
s
def sobre():
    st.title("Sobre a Empresa")
    st.write("Somos uma empresa dedicada a oferecer os melhores serviços aos nossos clientes. Nossa missão é garantir qualidade e satisfação em tudo o que fazemos.")
    images.show_imagens()

def servicos():
    st.title("Serviços que Oferecemos")
    st.write("Aqui estão os serviços que oferecemos:")
    st.write("- Consultoria Empresarial")
    st.write("- Desenvolvimento Web")
    st.write("- Marketing Digital")



    os.gerar_ordem_servico()

# Função para a navegação com botões
def main():
    # Estilização para garantir que a altura ocupe 100% da tela
    st.markdown(
        """
        <style>
            html, body {
                height: 100%;
                margin: 0;
                padding: 0;
                display: flex;
                flex-direction: column;
            }
            .header {
                text-align: center;
                font-size: 2.5em;
                margin-bottom: 20px;
                padding: 20px;
                background-color: #2c3e50;
                color: white;
            }
            .stButton > button {
                background-color: #f39c12;
                border: none;
                border-radius: 5px;
                color: white;
                padding: 15px;
                font-size: 1.2em;
                margin: 5px;
                width: 100%;
                cursor: pointer;
            }
            .stButton > button:hover {
                background-color: #e67e22;
            }
            .content {
                flex-grow: 1;
                padding: 20px;
                overflow-y: auto;
            }
        </style>
        """, unsafe_allow_html=True
    )

    # Cabeçalho do site
    st.markdown('<div class="header">Bem-vindo ao Meu Site!</div>', unsafe_allow_html=True)

    # Criação de botões para navegação
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Home"):
            st.session_state.page = "Home"

    with col2:
        if st.button("Sobre"):
            st.session_state.page = "Sobre"

    with col3:
        if st.button("Serviços"):
            st.session_state.page = "Serviços"

    # Exibe a página de acordo com a seleção
    if "page" not in st.session_state:
        st.session_state.page = "Home"

    # Divisão de conteúdo conforme a seleção
    with st.container():
        st.markdown('<div class="content">', unsafe_allow_html=True)
        if st.session_state.page == "Home":
            home()
        elif st.session_state.page == "Sobre":
            sobre()
        elif st.session_state.page == "Serviços":
            servicos()
        st.markdown('</div>', unsafe_allow_html=True)

# Chama a função principal para a navegação
if __name__ == "__main__":
    main()
