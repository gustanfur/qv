import pandas as pd

def calcular_escores(df: pd.DataFrame) -> pd.DataFrame:
    """
    - Assume que df já está tratado e com colunas corretas (Índice, Q1 a Q26)
    - Recodifica textos para valores numéricos
    - Aplica inversão em Q3, Q4 e Q26
    - Calcula escores dos 4 domínios e remove colunas intermediárias
    - Mantém a ordem e estrutura original do DataFrame
    """

    df_resultado = df.copy()

    colunas_q = [f"Q{i}" for i in range(1, 27)]
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

    # Recodifica os textos
    for col in colunas_q:
        if col in df_resultado.columns:
            df_resultado[col] = df_resultado[col].astype(str).str.strip().map(mapa_texto)

    # Inversão nas colunas específicas
    mapa_inverso = {1: 5, 2: 4, 3: 3, 4: 2, 5: 1}
    colunas_invertidas = ["Q3", "Q4", "Q26"]
    for col in colunas_invertidas:
        if col in df_resultado.columns:
            df_resultado[col] = df_resultado[col].map(mapa_inverso)

    # Cálculo dos escores
    df_resultado["fisico"] = df_resultado[["Q3", "Q4", "Q10", "Q15", "Q16", "Q17", "Q18"]].mean(axis=1) * 4
    df_resultado["Domínio Físico"] = (df_resultado["fisico"] - 4) * (100 / 16)

    df_resultado["psico"] = df_resultado[["Q5", "Q6", "Q7", "Q11", "Q19", "Q26"]].mean(axis=1) * 4
    df_resultado["Domínio Psicológico"] = (df_resultado["psico"] - 4) * (100 / 16)

    df_resultado["social"] = df_resultado[["Q20", "Q21", "Q22"]].mean(axis=1) * 4
    df_resultado["Domínio Social"] = (df_resultado["social"] - 4) * (100 / 16)

    df_resultado["ambiente"] = df_resultado[["Q8", "Q9", "Q12", "Q13", "Q14", "Q23", "Q24", "Q25"]].mean(axis=1) * 4
    df_resultado["Domínio Ambiente"] = (df_resultado["ambiente"] - 4) * (100 / 16)

    # Remove colunas intermediárias
    df_resultado.drop(columns=["fisico", "psico", "social", "ambiente"], inplace=True)

    return df_resultado