# Historico das impressoras:
st.header(":orange[Historico das impressora]  🕡")
with st.expander("Clique para expandir historico"):
    todasImpressoras = len(historico['NUMERO DE SERIE'])
    st.write('ToTal: ', todasImpressoras)
    hisgroup = historico.groupby(by=['NUMERO DE SERIE'])['OBSERVAÇÃO'].apply(list)
    st.dataframe(hisgroup, hide_index=True)

# validação de caminho de data
dados = 123  # ou pode ser None, [], etc.
if not dados:  # Verifica se a variável está vazia
    print("Erro: os dados estão vazios!")
else:
    print(f"Dados encontrados: {dados}")
