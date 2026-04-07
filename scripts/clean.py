import pandas as pd
from pathlib import Path

raw = Path("data/raw")
psd = Path("data/processed")
psd.mkdir(exist_ok=True)
csv_raw = raw.glob('*.csv')
    
limpos = []
errors = []

#A Dict abaixo é uma lista de nomes parecidos com os nomes requeridos pelo script
mapa_colunas =  {
  'id' : ["id", "id_compra", "compra_id", "id_pedido", "pedido_id"],
  'cliente' : ["nome", "nome_cliente", "cliente_nome", "customer"],
  'valor_produto' : ["preço", "preco", "valor_compra", "valor", "preco_unitario", "price"],
  'quantidade' : ["qtd", "unidades", "quantia", "quantity"],
  'cidade' : ["loja", "região", "regiao", "local", "city"],
  'produto' : ["Item", "product"]
}
obg_column = [
  'id', 'valor_produto', 'quantidade'
]
schema_columns = ['id', 'cliente', 'valor_produto', 'quantidade', 'cidade', 'produto']

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
    df = df[schema_columns] 
    return df


def validar_colunas(df):
    #se uma das colunas obrigatorias nao estiver no arquivo, retornar ValueError
    mssg_clm = [col for col in obg_column if col not in df.columns]
    if mssg_clm:
      raise ValueError(f"Colunas Faltando: {mssg_clm}")


def limpeza(df):
   #Conversão de Valores
   df_numerics = ['id', 'quantidade', 'valor_produto']
   df_str = ['cliente', 'cidade', 'produto']

   df[df_str] = df[df_str].astype(str)   
   df[df_numerics] = df[df_numerics].apply(pd.to_numeric, errors = 'coerce')

   #filtro de linhas para garantir que valores invalidos ou erros de digitção sejam excluidos
   df = df.query('not (quantidade <= 0 or valor_produto <= 0 or valor_produto > 10000)') 

   #Exclusão de valores obrigatorios nulos e linhas de id duplicados
   df = df.dropna(subset=obg_column)  
   df = df.drop_duplicates(subset='id', keep='first')
  
   #Reconversão de valores numericos
   df_int = ['id', 'quantidade']
   df[df_int] = df[df_int].astype(int)
   df['valor_produto'] = df['valor_produto'].astype(float)

   #Preenchimento de linhas com valores nao obrigatorios
   colunas = ['cliente', 'cidade']
   df[colunas] = df[colunas].fillna("desconhecido")
   df['produto'] = df['produto'].fillna("nao_informado")

   #Padronização de texto para colunas de texto
   colunas = ['cliente', 'cidade', 'produto']
   df[colunas] = df[colunas].apply(lambda x: x.str.strip().str.lower())
   df['valor_total'] = df['valor_produto'] * df['quantidade']
   df = df.sort_values(by='valor_total', ascending=False)
   return df

for i in csv_raw:
  try:
    df = pd.read_csv(i, encoding='UTF-8', low_memory=False)
    df = padronizar_colunas(df, mapa_colunas)
    validar_colunas(df)
    df = limpeza(df)
    limpos.append(i)
    clean_csv = f"{i.stem}_limpo{i.suffix}"
    df.to_csv(psd / clean_csv, index=False)

  except Exception as e:
    print(f"Arquivo {i.name} foi Rejeitado: {e}")
    errors.append({
       "arquivo" : i,
       "erro": str(e)
    })

    continue

print("-" * 30)

print(f"Arquivos Limpos com Êxito: {len(limpos)}")

for i in limpos:
   print(f" - {i.name} processado e salvo em /processed")

print(f"\nArquivos Recusados: {len(errors)}")
for erro_dict in errors:
   file_error = erro_dict['arquivo'].name
   error_name = erro_dict['erro']

   print(f"Arquivo: {file_error} | Motivo : {error_name}")