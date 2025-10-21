import pandas as pd

def calcular_escores(df: pd.DataFrame) -> pd.DataFrame:
    """
    - Usa linha 1 como cabeçalho (rótulos Q)
    - Ignora linha 2 (textos do questionário)
    - Usa dados a partir da linha 3 como observações
    - Recodifica textos para valores numéricos
    - Aplica inversão em Q3, Q4 e Q26
    """

    # Etapa 1: Reindexa usando linha 1 como cabeçalho
    df_resetado = df.reset_index(drop=True)
    novo_header = df_resetado.iloc[0]
    df_dados = df_resetado.iloc[2:].copy()
    df_dados.columns = novo_header

    # Etapa 2: Seleciona colunas Q1 a Q26
    colunas_q = [f"Q{i}" for i in range(1, 27)]
    df_q = df_dados[colunas_q].copy()

    # Etapa 3: Recodificação textual
    mapa_texto = {
        "Muito boa": 5,
        "Muito satisfeito(a)": 5,
        "Extremamente": 5,
        "Muito bom": 5,
        "Nada": 5,
        "Boa": 4,
        "Satisfeito(a)": 4,
        "Bastante": 4,
        "Bom": 4,
        "Nem boa nem ruim": 3,
        "Nem satisfeito(a) nem insatisfeito(a)": 3,
        "Mais ou menos": 3,
        "Nem ruim nem bom": 3,
        "Ruim": 2,
        "Insatisfeito(a)": 2,
        "Pouco": 2,
        "Muito ruim": 1,
        "Muito insatisfeito(a)": 1,
        "Muito pouco": 1,
        " ": "."
    }

    for col in df_q.columns:
        df_q[col] = df_q[col].replace(mapa_texto)

    # Etapa 4: Recodificação invertida
    mapa_inverso = {1: 5, 2: 4, 3: 3, 4: 2, 5: 1}
    colunas_invertidas = ["Q3", "Q4", "Q26"]

    for col in colunas_invertidas:
        if col in df_q.columns:
            df_q[col] = pd.to_numeric(df_q[col], errors='coerce').map(mapa_inverso)

    return df_q