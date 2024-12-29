# Historico das impressoras:
st.header(":orange[Historico das impressora]  🕡")
with st.expander("Clique para expandir historico"):
    todasImpressoras = len(historico['NUMERO DE SERIE'])
    st.write('ToTal: ', todasImpressoras)
    hisgroup = historico.groupby(by=['NUMERO DE SERIE'])['OBSERVAÇÃO'].apply(list)
    st.dataframe(hisgroup, hide_index=True)