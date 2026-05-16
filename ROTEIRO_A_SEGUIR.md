# Roteiro do Projeto: Estrutura de Dados II (DCA3702)
**Tema:** Análise Estrutural do Gargalo da BR-101 (Trajeto Parnamirim -> UFRN)

## Objetivo Principal
Provar matematicamente e visualmente por que o trecho da BR-101 (entre Parnamirim e o viaduto de Ponta Negra) sofre com engarrafamentos crônicos, utilizando teoria dos grafos para demonstrar a alta dependência (betweenness) e a falta de rotas alternativas eficientes para o fluxo em direção à UFRN e bairros centrais.

---

## Fase 1: Extração e Preparação do Grafo (OSMnx)
* **Ferramenta:** Python + `osmnx`
* **Passos:**
  1. Definir uma *bounding box* (coordenadas) que englobe o centro de Parnamirim (Sul) até o anel viário do campus da UFRN (Norte).
  2. Extrair a rede viária utilizando o parâmetro `network_type="drive"`.
  3. Converter o grafo original para um grafo não-direcionado (`to_undirected()`) para viabilizar o cálculo do k-core.
  4. Imprimir informações básicas: número de nós (cruzamentos) e arestas (vias).

---

## Fase 2: Diagnóstico Matemático (NetworkX)
* **Ferramenta:** Python + `networkx`
* **Métricas Obrigatórias a Calcular:**
  1. **Grau (Degree):** Calcular e elencar o Top 10 nós por grau (identificação empírica dos grandes trevos e do viaduto).
  2. **Betweenness Centrality:** Calcular para comprovar o estrangulamento. A expectativa é que as arestas/nós da BR-101 tenham os maiores valores da rede.
  3. **Closeness Centrality:** Calcular a proximidade média dos nós.
  4. **K-Core (Core Number):** Executar a decomposição para identificar os miolos residenciais (alta densidade) versus vias de ligação.
* **Exportação:** Atribuir os valores calculados (`degree`, `betweenness`, `core_number`) como propriedades dos nós e exportar o grafo no formato `rede_br101.graphml`.

---

## Fase 3: Visualização e Filtros (Gephi)
* **Ferramenta:** Gephi
* **Visualização 1: Geográfica (O Mapa Real)**
  * Aplicar o *Geo Layout* usando os atributos `x` (longitude) e `y` (latitude).
  * Tamanho do nó proporcional ao **grau**.
  * Cor do nó definida pelo **core number**.
  * Aplicar cor de destaque (ex: vermelho escuro) nos nós de maior **betweenness**.
* **Visualização 2: Estrutural (A Força do Fluxo)**
  * Aplicar o layout *ForceAtlas2*. O objetivo é ver o grafo se deformar em um formato de "ampulheta", evidenciando a concentração estrutural na rodovia.
* **Filtros Obrigatórios (Salvar imagens):**
  * Subgrafo contendo apenas o **Top 10% de nós por grau**.
  * Subgrafo filtrado por um **k-core alto** (k definido após análise dos dados, focando em isolar os bairros residenciais).

---

## Fase 4: Documentação Analítica (README.md)
* Responder de forma crítica às 7 questões do roteiro:
  1. Os nós de maior grau (trevos/viadutos) coincidem com o maior betweenness (a rodovia em si)?
  2. O k-core revela os hubs principais ou apenas o adensamento residencial de Parnamirim/Nova Parnamirim?
  3. Discorrer sobre como o *betweenness* explicita a falta de vias alternativas que o grau ignora.
  4. Contrastar o mapa geográfico com a distorção gerada pelo ForceAtlas2.
  5. Apontar o corredor da BR-101 e o viaduto como regiões críticas para a mobilidade.
  6. Confirmar a altíssima concentração estrutural da rede.
  7. Relacionar os números aos engarrafamentos empíricos diários no trajeto para a universidade.

---

## Fase 5: Estrutura do Vídeo de Apresentação (15 min)
* **Gravação:** Loom (Apresentação assíncrona).
* **Divisão de Tarefas:**
  * **[Meu Nome]:** Introdução. Apresentação da motivação do problema (o trajeto diário de ônibus, o gargalo real). Explicação breve do código de extração da *bounding box* no OSMnx.
  * **Sara Gabrielly:** Análise de Métricas (NetworkX). Explicação teórica dos resultados obtidos para Grau, Hubs e a densidade identificada pelo K-core nas áreas residenciais.
  * **Ícaro:** Visualização e Conclusão (Gephi). Demonstração do ForceAtlas2, explicação do altíssimo *Betweenness* na BR-101 respondendo às perguntas obrigatórias, e conclusão final sobre a vulnerabilidade da malha.