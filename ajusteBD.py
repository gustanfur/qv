import pandas as pd

def tratar_dados(df_original: pd.DataFrame) -> pd.DataFrame:
    """
    - Adiciona coluna 'Índice' para rastrear cada linha
    - Separa colunas L até AK em df_q
    - Separa o restante em df_restante
    - Une as tabelas via 'Índice'
    - Adiciona nova linha no topo com rótulos Q1...Qn (somente nas colunas L até AK)
    """

    df = df_original.copy()

    # Etapa 1: Adiciona coluna de índice
    df.insert(0, "Índice", range(len(df)))

    # Etapa 2: Identifica colunas L até AK (índices 12 a 38 após inserção do índice)
    colunas_q = df.columns[12:39]  # L até AK
    colunas_restantes = [col for col in df.columns if col not in colunas_q]

    # Etapa 3: Cria duas tabelas
    df_q = df[["Índice"] + list(colunas_q)].copy()
    df_restante = df[colunas_restantes].copy()

    # Etapa 4: Renomeia colunas de df_q para Q1...Qn (exceto 'Índice')
    novas_colunas_q = ["Índice"] + [f"Q{i+1}" for i in range(len(colunas_q))]
    df_q.columns = novas_colunas_q

    # Etapa 5: Une as tabelas via 'Índice'
    df_final = pd.merge(df_q, df_restante, on="Índice", how="inner")

    return df_final