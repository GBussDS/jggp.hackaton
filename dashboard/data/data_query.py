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

# Faça a consulta SQL
query = """
WITH ranked_data AS (
  SELECT
    *,
    ROW_NUMBER() OVER (PARTITION BY id_estacao, EXTRACT(YEAR FROM data_particao), EXTRACT(MONTH FROM data_particao) ORDER BY id_estacao, data_particao) AS row_num
  FROM
    `datario.clima_pluviometro.taxa_precipitacao_alertario`
),
summed_data AS (
  SELECT
    EXTRACT(YEAR FROM data_particao) AS ano,
    EXTRACT(MONTH FROM data_particao) AS mes,
    CONCAT(EXTRACT(YEAR FROM data_particao), '-', LPAD(CAST(EXTRACT(MONTH FROM data_particao) AS STRING), 2, '0')) AS mes_ano,
    SUM(acumulado_chuva_24_h) AS soma_acumulado_chuva_24_h
  FROM
    ranked_data
  WHERE
    row_num = 1
  GROUP BY
    ano, mes, mes_ano
)
SELECT * FROM summed_data;
"""
query_job = client.query(query)

df_precipitacao_alertario_mensal = query_job.to_dataframe()