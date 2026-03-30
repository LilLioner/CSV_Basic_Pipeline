import pandas as pd
from pathlib import Path

raw = Path("data/raw")
psd = Path("data/processed")
psd.mkdir(exist_ok=True)
csv_raw = raw.glob("*.csv")
    
limpos = []
errors = []
mapa_colunas =  {
  'id' : ["id", "id_compra", "compra_id", "id_pedido", "pedido_id"],
  'cliente' : ["nome", "nome_cliente", "cliente_nome"],
  'valor_produto' : ["preço", "preco", "valor_compra", "valor", "preco_unitario"],
  'quantidade' : ["qtd", "unidades", "quantia"],
  'cidade' : ["loja", "região", "regiao", "local"]
}
obg_column = [
  'id', 'valor_produto', 'quantidade'
]
schema_columns = ['id', 'cliente', 'valor_produto', 'quantidade', 'cidade']

def padronizar_colunas(df, mapa):
    #padronização de texto
    df.columns = (
     df.columns
     .str.strip()
     .str.lower()
     .str.replace(' ', '_')
    )

    #mudança de nomes variaveis em colunas para o padrão do script
    colunas_novas = {}
    for col_padrao, variacoes in mapa.items():
      for col in df.columns:
        if col in variacoes:
          colunas_novas[col] = col_padrao
    df = df.rename(columns=colunas_novas)
    return df


def validar_colunas(df):
    #se uma das colunas obrigatorias nao estiver no arquivo, retornar ValueError
    mssg_clm = [col for col in obg_column if col not in df.columns]
    if mssg_clm:
      raise ValueError(f"Colunas Faltando: {mssg_clm}")


def limpeza(df):
   df = df.dropna(subset=obg_column)  
   df = df.drop_duplicates(subset='id', keep='first')
   colunas = ['cliente', 'cidade']
   df[colunas] = df[colunas].fillna("desconhecido")
   df['produto'] = df['produto'].fillna("nao_informado")
   colunas = ['cliente', 'cidade', 'produto']
   df[colunas] = df[colunas].apply(lambda x: x.str.strip().str.lower())
   return df






for i in csv_raw:
  try:
    df = pd.read_csv(i)
    df = padronizar_colunas(df, mapa_colunas)
    validar_colunas(df)
    df = limpeza(df)
    df['valor_total'] = df['valor_produto'] * df['quantidade']
    limpos.append(i)

    print(f"Arquivo {i} OK!")
    print(df)
  except ValueError as e:
    print(f"Arquivo {i} foi Rejeitado: {e}")
    errors.append({
       "arquivo" : i,
       "erro": str(e)
    })

    continue

