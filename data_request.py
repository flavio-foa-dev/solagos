import pandas as pd

#caminho_rede = "https://github.com/flavio-foa-dev/excel/raw/main/data_printer.xlsx"
#caminho_rede = "/home/flavio/Documentos/2024/sologas/solagos/data_printer.xlsx"

BASE_URL = "https://github.com/flavio-foa-dev/excel/raw/main/data_printer.xlsx"

def load_data( ):

    sheets_to_load = ['PRINTERS_INVENTORY', 'estoque', 'COMPUTER']

    data_sheets = pd.read_excel(BASE_URL, sheet_name=sheets_to_load)

    return data_sheets



