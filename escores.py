import pandas as pd

def calcular_escores(df: pd.DataFrame) -> pd.DataFrame:
    """
    - Seleciona colunas Q1 a Q26
    - Aplica recodificação invertida em Q3, Q4 e Q26
    - Retorna DataFrame com escores tratados
    """

    # Etapa 1: Seleciona colunas Q1 a Q26
    colunas_q = [f"Q{i}" for i in range(1, 27)]
    df_q = df[colunas_q].copy()

    # Etapa 2: Recodificação invertida
    mapa_inverso = {1: 5, 2: 4, 3: 3, 4: 2, 5: 1}
    colunas_invertidas = ["Q3", "Q4", "Q26"]

    for col in colunas_invertidas:
        if col in df_q.columns:
            df_q[col] = pd.to_numeric(df_q[col], errors='coerce').map(mapa_inverso)

    return df_q