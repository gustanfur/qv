import pandas as pd
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

def carregar_e_tratar_planilha(secrets_path="secrets.json") -> pd.DataFrame:
    # Carrega credenciais do arquivo JSON
    with open(secrets_path, "r") as f:
        secrets = json.load(f)

    creds = service_account.Credentials.from_service_account_info(secrets["google"])
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()

    SHEET_ID = secrets["planilha"]["sheet_id"]
    RANGE = secrets["planilha"]["range"]

    result = sheet.values().get(spreadsheetId=SHEET_ID, range=RANGE).execute()
    values = result.get('values', [])

    if not values:
        raise ValueError("Planilha vazia ou não acessível.")

    colunas = values[0]
    num_colunas = len(colunas)

    linhas = []
    for linha in values[1:]:
        linha += [""] * (num_colunas - len(linha))
        linhas.append(linha)

    df_original = pd.DataFrame(linhas, columns=colunas)

    # Adiciona linha com rótulos Q1 a Q26
    total_colunas = len(df_original.columns)
    linha_q = []
    for i in range(total_colunas):
        if 11 <= i <= 25:
            linha_q.append(f"Q{i - 10}")
        elif i < 11:
            linha_q.append(f"Q{i + 16}")
        else:
            linha_q.append("")
    df_original.loc[-1] = linha_q
    df_original.index = df_original.index + 1
    df_original = df_original.sort_index()

    return df_original