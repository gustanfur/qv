import pandas as pd

def calcular_escores(df: pd.DataFrame) -> pd.DataFrame:
    """
    - Usa linha 1 como cabeçalho (rótulos Q)
    - Ignora linha 2 (textos do questionário)
    - Usa dados a partir da linha 3 como observações
    - Recodifica textos para valores numéricos
    - Aplica inversão em Q3, Q4 e Q26
    - Calcula escores dos 4 domínios e remove colunas intermediárias
    """

    # Etapa 1: Reindexa usando linha 1 como cabeçalho
    df_resetado = df.reset_index(drop=True)
    novo_header = df_resetado.iloc[0]
    df_dados = df_resetado.iloc[2:].copy().reset_index(drop=True)
    df_dados.columns = novo_header

    # Etapa 2: Seleciona colunas Q1 a Q26
    colunas_q = [f"Q{i}" for i in range(1, 27)]
    df_q = df_dados[colunas_q].copy()

    # Etapa 3: Recodificação textual com limpeza
    mapa_texto = {
        "Muito boa": 5,
        "Muito satisfeito(a)": 5,
        "Extremamente": 5,
        "Muito bom": 5,
        "Nada": 5,
        "Nunca": 5,
        "Boa": 4,
        "Satisfeito(a)": 4,
        "Bastante": 4,
        "Bom": 4,
        "Algumas vezes": 4,
        "Nem boa nem ruim": 3,
        "Nem satisfeito(a) nem insatisfeito(a)": 3,
        "Mais ou menos": 3,
        "Nem ruim nem bom": 3,
        "Frequentemente": 3,
        "Ruim": 2,
        "Insatisfeito(a)": 2,
        "Pouco": 2,
        "Muito frequentemente": 2,
        "Muito ruim": 1,
        "Muito insatisfeito(a)": 1,
        "Muito pouco": 1,
        "Sempre": 1
    }

    for col in df_q.columns:
        df_q[col] = df_q[col].astype(str).str.strip().map(mapa_texto)

    # Etapa 4: Recodificação invertida
    mapa_inverso = {1: 5, 2: 4, 3: 3, 4: 2, 5: 1}
    colunas_invertidas = ["Q3", "Q4", "Q26"]

    for col in colunas_invertidas:
        if col in df_q.columns:
            df_q[col] = df_q[col].map(mapa_inverso)

    # Etapa 5: Cálculo dos escores
    df_q["fisico"] = df_q[["Q3", "Q4", "Q10", "Q15", "Q16", "Q17", "Q18"]].mean(axis=1, skipna=True) * 4
    df_q["Domínio Físico"] = (df_q["fisico"] - 4) * (100 / 16)

    df_q["psico"] = df_q[["Q5", "Q6", "Q7", "Q11", "Q19", "Q26"]].mean(axis=1, skipna=True) * 4
    df_q["Domínio Psicológico"] = (df_q["psico"] - 4) * (100 / 16)

    df_q["social"] = df_q[["Q20", "Q21", "Q22"]].mean(axis=1, skipna=True) * 4
    df_q["Domínio Social"] = (df_q["social"] - 4) * (100 / 16)

    df_q["ambiente"] = df_q[["Q8", "Q9", "Q12", "Q13", "Q14", "Q23", "Q24", "Q25"]].mean(axis=1, skipna=True) * 4
    df_q["Domínio Ambiente"] = (df_q["ambiente"] - 4) * (100 / 16)

    # Etapa 6: Remove colunas intermediárias
    df_q.drop(columns=["fisico", "psico", "social", "ambiente"], inplace=True)

    return df_q