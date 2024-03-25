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
Este trecho de código Python corresponde à inicialização e configuração de um aplicativo web utilizando Dash, uma biblioteca em Python para criação de aplicações web interativas.

1. **Inicialização do Aplicativo Dash:**
   - Para rodar o projeto, dê um git clone ou download dos arquivos e rode o `app.py`.

2. **Páginas e seu Funcionamento:**
   - Todas as páginas estão definidas dentro da pasta Pages, onde temos todas as abas do projeto. Cada arquivo cria uma nova página e dentro do arquivo são puxados os dados das queries e feito os gráficos;
   - As queries estão disponíveis no arquivo `data_query.py` dentro da pasta data, lá é possível ver todos as requisições em SQL que utilizamos no projeto;
   - Por fim, são utilizados algumas funções da pasta Components, como criação de Divs HTML, containers e aplicar layouts em gráficos.

3. **Conexão com o Google Cloud:**
   - Para rodar o código, baixe o Google CLI, o que permite fazermos as queries. Todas as tabelas e dados foram puxadas através de BigQuery no Google Cloud.

O código tem como objetivo principal criar um ambiente web interativo, onde os usuários podem visualizar e interagir com os dados fornecidos, facilitando a análise e compreensão das informações apresentadas.

---

Este projeto representa um excelente exemplo de colaboração, inovação e aplicação prática de conhecimentos acadêmicos para resolver desafios do mundo real. Estamos gratos pela oportunidade de participar deste Hackaton e contribuir para soluções que impactam positivamente a cidade do Rio de Janeiro.
