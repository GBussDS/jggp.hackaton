from google.cloud import bigquery

# Crie uma instância do cliente BigQuery
client = bigquery.Client(project='hackaton-fgv-guris')

# Faça a consulta SQL
query = """
SELECT *
FROM datario.clima_pluviometro.estacoes_alertario
"""
query_job = client.query(query)

df_alertario = query_job.to_dataframe()

# Faça a consulta SQL
query = """
SELECT * 
FROM datario.clima_pluviometro.taxa_precipitacao_alertario where data_particao >= "2024-03-01"
"""
query_job = client.query(query)

df_precipitacao_alertario = query_job.to_dataframe()

# Faça a consulta SQL
query = """
SELECT *
FROM datario.clima_pluviometro.estacoes_cemaden
"""
query_job = client.query(query)

df_cemaden = query_job.to_dataframe()

# Faça a consulta SQL
query = """
SELECT *
FROM datario.clima_pluviometro.taxa_precipitacao_cemaden
"""
query_job = client.query(query)

df_precipitacao_cemaden = query_job.to_dataframe()


# Faça a consulta SQL
query = """
SELECT *
FROM datario.clima_pluviometro.estacoes_inea
"""
query_job = client.query(query)

df_inea = query_job.to_dataframe()

# Faça a consulta SQL
query = """
SELECT *
FROM datario.clima_pluviometro.taxa_precipitacao_inea
"""
query_job = client.query(query)

df_precipitacao_inea = query_job.to_dataframe()


# Faça a consulta SQL
query = """
SELECT *
FROM `datario.adm_cor_comando.ocorrencias`
"""
query_job = client.query(query)

df_ocorrencias = query_job.to_dataframe()