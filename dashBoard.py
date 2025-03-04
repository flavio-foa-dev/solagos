import streamlit as st
import pandas as pd

pathDashboard = "https://github.com/flavio-foa-dev/excel/raw/main/dashboard.xlsx"
SAUDE = pd.read_excel(pathDashboard, sheet_name='Saude')
PACO = pd.read_excel(pathDashboard, sheet_name='Paco')

locationSelect = ['SAUDE', 'PACO', 'SEDUC', 'CARTORIO', 'PARTICULAR', 'SEPOL', 'ITABORAI', 'ARRAIAL']

def dashBoardSelect():
    # Selectbox to choose location
    filteredToLocation = st.selectbox(
        "ANALISE DE COPIAS 🔎",
        locationSelect
    )

    # Print the selected location (for debugging purposes)
    print(filteredToLocation)

    # Filter data based on the selected location and display the relevant dataframe
    if filteredToLocation == 'SAUDE':
        st.dataframe(SAUDE, hide_index=True)
    elif filteredToLocation == 'PACO':
        st.dataframe(PACO, hide_index=True)
    else:
        st.write(f"Nada encontrado para {filteredToLocation}")


