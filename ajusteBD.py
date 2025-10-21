import pandas as pd

def tratar_dados(df_original: pd.DataFrame) -> pd.DataFrame:
    """
    - Adiciona coluna 'Índice' para rastrear cada linha
    - Separa colunas L até AK em uma tabela (df_q)
    - Separa o restante das colunas em outra tabela (df_restante)
    - Reúne as duas tabelas usando o índice como chave
    - Adiciona uma linha de rótulos Q1 a Qn nas colunas L até AK
    """

    df = df_original.copy()

    # Etapa 1: Adiciona coluna de índice
    df.insert(0, "Índice", range(len(df)))

    # Etapa 2: Identifica colunas L até AK (índices 11 a 37, considerando que 'Índice' foi inserido na posição 0)
    colunas_q = df.columns[12:39]  # L até AK
    colunas_restantes = [col for col in df.columns if col not in colunas_q]

    # Etapa 3: Cria duas tabelas
    df_q = df[["Índice"] + list(colunas_q)].copy()
    df_restante = df[colunas_restantes].copy()

    # Etapa 4: Adiciona rótulos Q1 a Qn na tabela df_q
    linha_q = [""] + [f"Q{i+1}" for i in range(len(colunas_q))]
    df_q.loc[-1] = linha_q
    df_q.index = df_q.index + 1
    df_q = df_q.sort_index()

    # Etapa 5: Junta as tabelas usando o índice
    df_final = pd.merge(df_q, df_restante, on="Índice", how="inner")

    return df_final