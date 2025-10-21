import pandas as pd

def tratar_dados(df_original: pd.DataFrame) -> pd.DataFrame:
    """
    - Adiciona coluna 'Índice' para rastrear cada linha
    - Separa colunas L até AK em df_q
    - Separa o restante em df_restante
    - Une as tabelas via 'Índice'
    - Adiciona nova linha no topo com rótulos Q1...Qn (exceto na coluna 'Índice')
    """

    df = df_original.copy()

    # Etapa 1: Adiciona coluna de índice
    df.insert(0, "Índice", range(len(df)))

    # Etapa 2: Identifica colunas L até AK (índices 11 a 37 após inserção do índice)
    colunas_q = df.columns[12:39]  # L até AK
    colunas_restantes = [col for col in df.columns if col not in colunas_q]

    # Etapa 3: Cria duas tabelas
    df_q = df[["Índice"] + list(colunas_q)].copy()
    df_restante = df[colunas_restantes].copy()

    # Etapa 4: Une as tabelas via 'Índice'
    df_final = pd.merge(df_q, df_restante, on="Índice", how="inner")

    # Etapa 5: Adiciona nova linha com rótulos Q1...Qn (exceto na coluna 'Índice')
    nova_linha = [""] + [f"Q{i+1}" for i in range(len(df_final.columns) - 1)]
    df_final.loc[-1] = nova_linha
    df_final.index = df_final.index + 1
    df_final = df_final.sort_index()

    return df_final