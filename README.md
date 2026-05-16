# Por que todo mundo odeia o M34?
**Uma análise estrutural do estrangulamento viário da BR-101 usando Teoria dos Grafos e OSMnx.**

---

## 📖 Prólogo: A anatomia de um engarrafamento diário
Se você estuda na UFRN e mora na região sul da Grande Natal (Parnamirim, Emaús, Nova Parnamirim), você conhece a dor do **M34**. O bloco de aulas que vai das 08h50 às 10h30 exige um deslocamento que coincide com o pior momento da mobilidade urbana potiguar. 

Todos os dias, a viagem de ônibus entre Parnamirim e o Campus Universitário colapsa em um trecho muito específico: a BR-101, entre a Leroy Merlin e o complexo viário de Ponta Negra. O trânsito para, o tempo passa e a primeira aula é perdida. 

Mas por que esse engarrafamento é tão crônico? É apenas excesso de carros, ou existe uma falha fundamental na forma como as ruas da nossa cidade estão conectadas? 

Este projeto nasceu dessa frustração diária. Usando dados reais do OpenStreetMap e métricas de grafos, decidimos modelar a malha viária como uma rede matemática para responder a uma pergunta simples: **o quão dependente e vulnerável é a estrutura da nossa cidade?**

---

## 👥 Equipe
* Gabriel Sebastião do Nascimento Neto
* Ícaro [Sobrenome]
* Sara Gabrielly [Sobrenome]

**Disciplina:** Estrutura de Dados II (DCA3702)

---

## 📍 Identificação da Região Analisada
* **Região:** Corredor de mobilidade Sul-Norte (Centro de Parnamirim ao Campus da UFRN / Lagoa Nova).
* **Foco Estrutural:** Rodovia BR-101 e Viaduto de Ponta Negra.
* **Justificativa:** [Descrever brevemente por que o recorte dessa *bounding box* é ideal para analisar o gargalo de mobilidade entre a região metropolitana e os polos universitários/comerciais de Natal].

---

## 🎥 Apresentação do Projeto
[![Assista no Loom](https://img.shields.io/badge/Loom-Assistir_Apresentação-625df5?style=for-the-badge&logo=loom)](INSERIR_LINK_DO_LOOM_AQUI)
*(Duração: ~15 minutos. Apresentação da extração, métricas, visualizações no Gephi e conclusões).*

---

## 🎯 Objetivo do Trabalho
[Descrever que o objetivo é analisar a centralidade de intermediação (betweenness) e a topologia da rede para provar matematicamente a falta de rotas alternativas e o estrangulamento do fluxo rodoviário].

---

## 🛠️ Metodologia
* **Extração de Dados:** [Explicar o uso do `OSMnx` com `network_type="drive"` e a definição da *bounding box*].
* **Processamento:** [Uso da biblioteca `NetworkX` para transformação em grafo não-direcionado e cálculo topológico].
* **Visualização:** [Exportação em `.graphml` e renderização via `Gephi`].
* **Configuração do Ambiente:** Veja como rodar o projeto usando o `uv` em [CONTRIBUTING.md](./CONTRIBUTING.md).

---

## 📊 Métricas Calculadas
[Listar e explicar rapidamente o que cada número representa no contexto do nosso trânsito]
1. **Grau dos Nós (Degree):** 2. **Centralidade de Intermediação (Betweenness Centrality):** 3. **Centralidade de Proximidade (Closeness Centrality):** 4. **Core Number (K-Core):** ---

## 🗺️ Principais Visualizações (Gephi)
### 1. Visualização Geográfica (Mapa Real)
*(Inserir Imagem Aqui)*
> **Descrição:** [Explicar como as cores e tamanhos refletem as métricas na geografia real da cidade, destacando o corredor da BR-101].

### 2. Visualização Estrutural (ForceAtlas2)
*(Inserir Imagem Aqui)*
> **Descrição:** [Explicar o que acontece quando a geografia é ignorada e a gravidade do grafo entra em ação. Falar sobre o formato de funil/ampulheta gerado pela falta de vias alternativas].

### 3. Filtro: Top 10% Hubs e K-Core
*(Inserir Imagem Aqui)*
> **Descrição:** [Explicar o que restou na tela após os filtros (ex: os miolos residenciais vs as grandes rotatórias)].

---

## ❓ Respostas às Questões Obrigatórias

**1. Os nós com maior grau coincidem com os nós de maior betweenness?**
> [Sua resposta aqui]

**2. O núcleo identificado pelo k-core coincide com os principais hubs?**
> [Sua resposta aqui]

**3. O que a métrica de betweenness revela que o grau não revela?**
> [Sua resposta aqui - *Focar na questão de que grau é apenas esquina cruzada, while betweenness mostra a dependência de fluxo de vias longas*].

**4. O que muda quando a rede é analisada em sua posição geográfica real e quando é analisada por um layout estrutural?**
> [Sua resposta aqui - *Falar sobre a revelação do "gargalo"*].

**5. Existem regiões críticas para mobilidade urbana na área analisada?**
> [Sua resposta aqui - *Apontar o viaduto e a rodovia*].

**6. A rede parece homogênea ou apresenta concentração estrutural?**
> [Sua resposta aqui]

**7. Os resultados obtidos fazem sentido considerando o conhecimento urbano da região escolhida?**
> [Sua resposta aqui - *Amarrar com a história do ônibus e do M34*].

---

## 🏁 Principais Conclusões
[Resumo final do grupo. Exemplo: "O grafo comprova que a lentidão diária não é apenas uma questão de volume de veículos, mas uma falha topológica: a dependência extrema de uma única aresta de alta intermediação para conectar núcleos habitacionais densos..."]
