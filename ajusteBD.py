import pandas as pd

def tratar_dados(df_original: pd.DataFrame) -> pd.DataFrame:
    """
    - Adiciona rótulos Q1 a Q38 nas colunas L até AK
    - Move a coluna AL para o início
    - Remove colunas AM, AN, A e B
    - Reinicia a contagem Q nas colunas restantes até L
    """
    df = df_original.copy()

    # Etapa 1: Adiciona rótulos Q1 a Q38 nas colunas L até AK
    colunas_q1 = df.columns[11:38]  # L (índice 11) até AK (índice 38)
    q_labels = [f"Q{i+1}" for i in range(len(colunas_q1))]
    q_map = dict(zip(colunas_q1, q_labels))
    df.rename(columns=q_map, inplace=True)

    # Etapa 2: Move a coluna AL (índice 39) para o início
    col_al = df.columns[38] if len(df.columns) > 38 else None
    if col_al:
        colunas = [col_al] + [col for col in df.columns if col != col_al]
        df = df[colunas]

    # Etapa 3: Remove colunas AM, AN, A e B
    colunas_para_remover = []
    for nome in df.columns:
        if nome.strip().upper() in ["AM", "AN", "A", "B"]:
            colunas_para_remover.append(nome)
    df.drop(columns=colunas_para_remover, inplace=True, errors='ignore')

    # Etapa 4: Reinicia contagem Q nas colunas restantes até a nova posição de "L"
    if "L" in df.columns:
        idx_l = df.columns.get_loc("L")
        novas_q = [f"Q{i+1}" for i in range(idx_l + 1)]
        nova_linha = novas_q + [""] * (len(df.columns) - len(novas_q))
    else:
        nova_linha = [""] * len(df.columns)

    # Insere a nova linha no topo
    df.loc[-1] = nova_linha
    df.index = df.index + 1
    df = df.sort_index()

    return df