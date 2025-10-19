import streamlit as st
import requests
from io import BytesIO

# Função para exibir as imagens do GitHub
def show_imagens():
    st.title("Galeria de Imagens")
    col1, col2, col3 = st.columns(3)  # 3 colunas para distribuir as imagens

    # Lista de links das imagens hospedadas no GitHub
    imagem_urls = [
        "https://raw.githubusercontent.com/flavio-foa-dev/excel/main/image/image1.jpeg",
        "https://raw.githubusercontent.com/flavio-foa-dev/excel/main/image/image2.jpeg",
        "https://raw.githubusercontent.com/flavio-foa-dev/excel/main/image/image3.jpeg",
        "https://raw.githubusercontent.com/flavio-foa-dev/excel/main/image/image4.jpeg",
        "https://raw.githubusercontent.com/flavio-foa-dev/excel/main/image/image5.jpeg",
        "https://raw.githubusercontent.com/flavio-foa-dev/excel/main/image/image6.jpeg",
        "https://raw.githubusercontent.com/flavio-foa-dev/excel/main/image/image7.jpeg",
        "https://raw.githubusercontent.com/flavio-foa-dev/excel/main/image/image8.jpeg",
        "https://raw.githubusercontent.com/flavio-foa-dev/excel/main/image/image9.jpeg",
        "https://raw.githubusercontent.com/flavio-foa-dev/excel/main/image/image10.jpeg",
        "https://raw.githubusercontent.com/flavio-foa-dev/excel/main/image/image11.jpeg",
        "https://raw.githubusercontent.com/flavio-foa-dev/excel/main/image/image12.jpeg",
        "https://raw.githubusercontent.com/flavio-foa-dev/excel/main/image/image13.jpeg",
        "https://raw.githubusercontent.com/flavio-foa-dev/excel/main/image/image14.jpeg",
        "https://raw.githubusercontent.com/flavio-foa-dev/excel/main/image/image15.jpeg",
        "https://raw.githubusercontent.com/flavio-foa-dev/excel/main/image/image16.jpeg",
        "https://raw.githubusercontent.com/flavio-foa-dev/excel/main/image/image17.jpeg",
        "https://raw.githubusercontent.com/flavio-foa-dev/excel/main/image/image18.jpeg"

    ]

    captions = [
        "Brothes - 502",
        "HPs - 5200",
        "3710",
        "Ricoh 550",
        "Ricoh 5200",
        "HPs - 5200",
        "HPs",
        "Ricoh 601",
        "Ricoh 501",
        "Ricoh c300 color - brothes",
        "Ricoh",
        "Ricoh",
        "Carrinhos - Gavetas",
        "Impressoras - Gabinetes",
        "Toners Brothes",
        "Brother 5512 Nova",
        "Ricoh 201",
        "Ventilador Coluna"
    ]

    for idx, (url, caption) in enumerate(zip(imagem_urls, captions)):
        if idx % 3 == 0:
            col1.image(url, caption=caption, use_container_width=True)
        elif idx % 3 == 1:
            col2.image(url, caption=caption, use_container_width=True)
        else:
            col3.image(url, caption=caption, use_container_width=True)


def show_video():
    videos_urls = ["https://github.com/flavio-foa-dev/excel/raw/main/video/video1.mp4" ]

    st.title("Galeria de Vídeos")
    st.video(videos_urls[0])


# st.image(imagem_urls[0], caption="Brothes - 502 ")




