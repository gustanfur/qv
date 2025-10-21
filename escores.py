import pandas as pd

def calcular_escores(df: pd.DataFrame) -> pd.DataFrame:
    """
    - Usa linha 1 como cabeçalho (rótulos Q)
    - Ignora linha 2 (textos do questionário)
    - Usa dados a partir da linha 3 como observações
    - Aplica recodificação invertida em Q3, Q4 e Q26
    """

    # Etapa 1: Reindexa usando linha 1 como cabeçalho
    df_resetado = df.reset_index(drop=True)

    # Linha 0: rótulos Q
    # Linha 1: textos do questionário
    # Linha 2 em diante: dados válidos
    novo_header = df_resetado.iloc[0]
    df_dados = df_resetado.iloc[2:].copy()
    df_dados.columns = novo_header

    # Etapa 2: Seleciona colunas Q1 a Q26
    colunas_q = [f"Q{i}" for i in range(1, 27)]
    df_q = df_dados[colunas_q].copy()

    # Etapa 3: Recodificação invertida
    mapa_inverso = {1: 5, 2: 4, 3: 3, 4: 2, 5: 1}
    colunas_invertidas = ["Q3", "Q4", "Q26"]

    for col in colunas_invertidas:
        if col in df_q.columns:
            df_q[col] = pd.to_numeric(df_q[col], errors='coerce').map(mapa_inverso)

    return df_q