{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "00b52433-2d77-45bd-b548-22f0715190d3",
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "from google.oauth2 import service_account\n",
    "from googleapiclient.discovery import build\n",
    "import streamlit as st  # necessário para acessar st.secrets\n",
    "\n",
    "def carregar_e_tratar_planilha() -> pd.DataFrame:\n",
    "    \"\"\"\n",
    "    Acessa a planilha do Google Sheets via st.secrets,\n",
    "    carrega os dados, aplica tratamento e retorna o DataFrame.\n",
    "    \"\"\"\n",
    "    # Autenticação via secrets\n",
    "    creds = service_account.Credentials.from_service_account_info(st.secrets[\"google\"])\n",
    "    service = build('sheets', 'v4', credentials=creds)\n",
    "    sheet = service.spreadsheets()\n",
    "\n",
    "    # Parâmetros da planilha\n",
    "    SHEET_ID = st.secrets[\"planilha\"][\"sheet_id\"]\n",
    "    RANGE = st.secrets[\"planilha\"][\"range\"]\n",
    "\n",
    "    # Carrega os dados\n",
    "    result = sheet.values().get(spreadsheetId=SHEET_ID, range=RANGE).execute()\n",
    "    values = result.get('values', [])\n",
    "\n",
    "    if not values:\n",
    "        raise ValueError(\"Não foi possível carregar os dados da planilha.\")\n",
    "\n",
    "    # Cria DataFrame com cabeçalho original\n",
    "    df = pd.DataFrame(values[1:], columns=values[0])\n",
    "\n",
    "    # Adiciona linha com rótulos genéricos\n",
    "    linha_generica = [f\"Coluna{i+1}\" for i in range(len(df.columns))]\n",
    "    df.loc[-1] = linha_generica\n",
    "    df.index = df.index + 1\n",
    "    df = df.sort_index()\n",
    "\n",
    "    return df"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python [conda env:base] *",
   "language": "python",
   "name": "conda-base-py"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
