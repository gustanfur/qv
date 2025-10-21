import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from google.oauth2 import service_account
from googleapiclient.discovery import build
import statsmodels.api as sm

# Configuração do Streamlit
st.set_page_config(page_title="Análise de Qualidade de Vida", layout="wide")
st.title("📊 Análise de Qualidade de Vida")

# Autenticação Google Sheets
CREDENTIALS_PATH = r"C:\Users\Gustavo\Documents\GitHub\qv\teseqv.json"
creds = service_account.Credentials.from_service_account_file(CREDENTIALS_PATH)
service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()

SHEET_ID = "1PgkoCQqyfqrwSIinYCnZ4sq5WjjeJJmVDFmQLNHFPak"
RANGE = "Respostas ao formulário 1!A1:Z1000"

result = sheet.values().get(spreadsheetId=SHEET_ID, range=RANGE).execute()
values = result.get('values', [])

if values:
    df = pd.DataFrame(values[1:], columns=values[0])
else:
    st.error("Não foi possível carregar os dados da planilha.")
    st.stop()

# Conversão de colunas numéricas
if 'Idade' in df.columns:
    df['Idade'] = pd.to_numeric(df['Idade'], errors='coerce')
if 'QV_Escore' in df.columns:
    df['QV_Escore'] = pd.to_numeric(df['QV_Escore'], errors='coerce')

# Menu lateral
aba = st.sidebar.radio("📂 Selecione uma aba:", [
    "Dados brutos",
    "Estatísticas descritivas",
    "Gráficos",
    "Filtros combinados",
    "Exportar dados",
    "Análises estatísticas"
])

# Aba 1: Dados brutos
if aba == "Dados brutos":
    st.subheader("📋 Dados brutos")
    st.dataframe(df)

# Aba 2: Estatísticas descritivas
elif aba == "Estatísticas descritivas":
    st.subheader("📊 Estatísticas descritivas")
    st.write("**Resumo geral:**")
    st.dataframe(df.describe(include='all'))
    if 'Idade' in df.columns:
        st.write("**Resumo da idade:**")
        st.dataframe(df['Idade'].describe())

# Aba 3: Gráficos
elif aba == "Gráficos":
    st.subheader("📈 Gráficos")
    if 'Idade' in df.columns:
        fig, ax = plt.subplots()
        df['Idade'].dropna().astype(int).hist(bins=10, ax=ax)
        ax.set_title("Histograma de Idade")
        st.pyplot(fig)
    if 'Idade' in df.columns and 'QV_Escore' in df.columns:
        fig, ax = plt.subplots()
        ax.scatter(df['Idade'], df['QV_Escore'], alpha=0.5)
        ax.set_xlabel("Idade")
        ax.set_ylabel("Escore de Qualidade de Vida")
        ax.set_title("Idade vs QV")
        st.pyplot(fig)

# Aba 4: Filtros combinados
elif aba == "Filtros combinados":
    st.subheader("🔍 Filtros combinados")
    col1, col2, col3 = st.columns(3)
    sexo = col1.selectbox("Sexo", options=df['Sexo'].unique()) if 'Sexo' in df.columns else None
    regiao = col2.selectbox("Região", options=df['Região'].unique()) if 'Região' in df.columns else None
    faixa = col3.slider("Idade mínima", min_value=0, max_value=100, value=18) if 'Idade' in df.columns else None

    df_filtrado = df.copy()
    if sexo:
        df_filtrado = df_filtrado[df_filtrado['Sexo'] == sexo]
    if regiao:
        df_filtrado = df_filtrado[df_filtrado['Região'] == regiao]
    if faixa is not None:
        df_filtrado = df_filtrado[df_filtrado['Idade'] >= faixa]

    st.dataframe(df_filtrado)

# Aba 5: Exportar dados
elif aba == "Exportar dados":
    st.subheader("📥 Exportar dados")
    st.download_button(
        label="Baixar dados completos",
        data=df.to_csv(index=False).encode('utf-8'),
        file_name='dados_qualidade_vida.csv',
        mime='text/csv'
    )

# Aba 6: Análises estatísticas
elif aba == "Análises estatísticas":
    st.subheader("📐 Análises estatísticas")
    if 'Idade' in df.columns and 'QV_Escore' in df.columns:
        correlacao = df[['Idade', 'QV_Escore']].corr().iloc[0, 1]
        st.metric(label="Correlação entre Idade e QV", value=f"{correlacao:.2f}")

        df_reg = df[['Idade', 'QV_Escore']].dropna()
        X = sm.add_constant(df_reg['Idade'])
        y = df_reg['QV_Escore']
        modelo = sm.OLS(y, X).fit()
        st.write("**Resumo da regressão linear:**")
        st.text(modelo.summary())