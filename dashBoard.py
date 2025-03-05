import streamlit as st
import pandas as pd

# Path to the Excel file on GitHub
pathDashboard = "https://github.com/flavio-foa-dev/excel/raw/main/dashboard.xlsx"

# Function to read the Excel file
@st.cache_data
def load_data():
    try:
        # Load the Excel data
        SAUDE = pd.read_excel(pathDashboard, sheet_name='Saude')
        PACO = pd.read_excel(pathDashboard, sheet_name='Paco')
        return SAUDE, PACO
    except Exception as e:
        st.error(f"Erro ao carregar os dados: {e}")
        return None, None

# Load data
SAUDE, PACO = load_data()

# List of available locations
locationSelect = ['SAUDE', 'PACO', 'SEDUC', 'CARTORIO', 'PARTICULAR', 'SEPOL', 'ITABORAI', 'ARRAIAL']

def dashBoardSelect():
    # Selectbox for location selection

    filteredToLocation = st.selectbox("ANALISE DE CÓPIAS 🔎", locationSelect)

    # Filter and display the relevant data based on location
    if filteredToLocation == 'SAUDE':
        if SAUDE is not None:
            st.dataframe(SAUDE, hide_index=True)
        else:
            st.write("Dados não encontrados para SAUDE.")
    elif filteredToLocation == 'PACO':
        if PACO is not None:
            st.dataframe(PACO, hide_index=True)
        else:
            st.write("Dados não encontrados para PACO.")
    else:
        st.write(f"Nada encontrado para {filteredToLocation}")

# Run the function to display the dashboard
# dashBoardSelect()
