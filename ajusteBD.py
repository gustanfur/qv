import pandas as pd

def tratar_dados(df_original: pd.DataFrame) -> pd.DataFrame:
    """
    - Mantém os nomes originais das colunas
    - Cria uma nova linha com rótulos Q1, Q2, ..., Qn
      aplicados às colunas específicas
    """

    df = df_original.copy()
    total_colunas = len(df.columns)

    # Define quais colunas receberão rótulos Q (exemplo: da coluna L até AK)
    # Isso corresponde aos índices de coluna 11 a 37 (inclusive)
    colunas_q = list(range(11, 38))  # Ajuste conforme necessário

    # Cria a nova linha com rótulos Q ou vazio
    nova_linha = []
    for i in range(total_colunas):
        if i in colunas_q:
            nova_linha.append(f"Q{i - colunas_q[0] + 1}")
        else:
            nova_linha.append("")

    # Insere a nova linha no topo
    df.loc[-1] = nova_linha
    df.index = df.index + 1
    df = df.sort_index()

    return df