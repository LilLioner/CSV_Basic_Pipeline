import pandas as pd
from pathlib import Path

raw = Path("data/raw")
psd = Path("data/processed")
psd.mkdir(exist_ok=True)
csv_raw = list(raw.glob('*.csv'))
    
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

   #Validação de arquivo, caso uma das colunas obrigatórias não exista, o arquivo é recusado.
    mssg_clm = [col for col in obg_column if col not in df.columns]
    if mssg_clm:
      raise ValueError(f"Colunas Faltando: {mssg_clm}")
    
    
    for col in schema_columns:
      if col not in df.columns:
        df[col] = None 

    return df[schema_columns]

def limpeza(df):
   df = df.copy()

   #Conversão de Valores
   df['quantidade'] = pd.to_numeric(df['quantidade'], errors='coerce')
   df['valor_produto'] = pd.to_numeric(df['valor_produto'], errors='coerce')
   df['id'] = pd.to_numeric(df['id'], errors='coerce')

   #Exclusão de valores obrigatorios nulos
   df = df.dropna(subset=obg_column)  

   #Filtro de regras de negócio
   df = df.query('not (quantidade <= 0 or valor_produto <= 0 or valor_produto > 10000)') 
   
   #Excluir linhas com id duplicados
   df = df.drop_duplicates(subset='id', keep='first')

   #Preenchimento de colunas string vazias
   df['cliente'] = df['cliente'].fillna("desconhecido")
   df['cidade'] = df['cidade'].fillna("desconhecido")
   df['produto'] = df['produto'].fillna("nao_informado")

   #tipagem final
   df = df.astype({'id': 'int64', 'quantidade': int, 'valor_produto': float})

   #Padronização de strings
   for col in ['cliente', 'cidade', 'produto']:
    df[col] = df[col].astype(str).str.strip().str.lower()
    
   #Coluna derivada e ordenação
   df['valor_total'] = df['valor_produto'] * df['quantidade']

   return df.sort_values(by='valor_total', ascending=False)


for i in csv_raw:
  try:
    df = pd.read_csv(i, low_memory=False)
    df = padronizar_colunas(df, mapa_colunas)
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