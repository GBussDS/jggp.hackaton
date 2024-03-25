# Projeto Hackaton - Rio Águas

Projeto desenvolvido durante o Hackaton promovido pela FGValley em parceria com a FGV EMAp e a prefeitura do Rio de Janeiro. O objetivo era criar uma solução para auxiliar a equipe da Rio Águas em suas demandas relacionadas a visualizações, índices e formas de download de dados.

## Participantes
- João Gabriel
- Guilherme Buss
- Gustavo Bianchi
- Pedro Coterli

## Introdução
O projeto visa fornecer uma plataforma web para visualização e análise de dados relacionados a chuvas, alagamentos e enchentes na cidade do Rio de Janeiro. Utilizamos tecnologias como Python, Dash e Google Cloud para criar um dashboard interativo e informativo.

## Extração de Dados
Os dados foram extraídos de duas formas:
1. Baixando dados como CSV através de consultas no BigQuery.
2. Utilizando a biblioteca `google-cloud-bigquery` em Python para consultas diretas no BigQuery, permitindo atualizações em tempo real dos dados.

## Visualizações
### Mapa de Chuva
- Utilizamos polígonos de cada bairro e dados da websirene para calcular a média da chuva acumulada em cada região.
- Implementamos filtros para escolher intervalos de tempo específicos.

### Alagamentos
- Disponibilizamos gráficos que mostram os casos totais de alagamento por bairro e a incidência de enchentes ao longo do tempo.
- Implementamos um filtro de tempo para a ocorrência de inundações.

### Cemaden e Chuvas por Período
- Facilitamos a visualização das precipitações acumuladas em diferentes períodos (15 minutos, 1 hora, 24 horas e 96 horas) em uma única aba.

## Resultados
Desenvolvemos um dashboard altamente funcional e informativo, oferecendo soluções eficazes para os desafios enfrentados pela equipe do Rio Águas. Integrando diferentes tecnologias e aplicando conhecimentos adquiridos na FGV, criamos visualizações intuitivas e informativas, proporcionando uma experiência de usuário aprimorada.

## Código
O código foi desenvolvido em Python utilizando a biblioteca Dash para construção do dashboard. Foi utilizado o Google Cloud BigQuery para extração de dados em tempo real.

---

Este projeto representa um excelente exemplo de colaboração, inovação e aplicação prática de conhecimentos acadêmicos para resolver desafios do mundo real. Estamos gratos pela oportunidade de participar deste Hackaton e contribuir para soluções que impactam positivamente a cidade do Rio de Janeiro.
