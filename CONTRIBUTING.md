# Instruções para Rodar e Contribuir

Este projeto utiliza o [uv](https://github.com/astral-sh/uv) como gerenciador de dependências e ambiente Python. O `uv` é extremamente rápido e garante que todos os colaboradores utilizem as mesmas versões de bibliotecas.

## 🚀 Como Executar

### 1. Pré-requisitos
Certifique-se de ter o `uv` instalado em sua máquina. Se não tiver, instale com:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Sincronizar o Ambiente
Ao clonar o repositório, execute o comando abaixo para criar o ambiente virtual e instalar todas as dependências listadas no `uv.lock`:
```bash
uv sync
```

### 3. Rodar o Jupyter Notebook
Para abrir o ambiente de análise (onde estão os notebooks), utilize:
```bash
uv run jupyter notebook
```
Isso garantirá que o Jupyter utilize o kernel correto com as bibliotecas `osmnx`, `networkx`, `folium`, etc.

---

## 🛠️ Como Contribuir

### Adicionando Novas Dependências
Se você precisar de uma nova biblioteca (ex: `pandas`), não use o `pip install`. Use o comando do `uv`:
```bash
uv add pandas
```
Isso atualizará automaticamente os arquivos `pyproject.toml` e `uv.lock`.

### Atualizando o Código
1. Crie uma nova branch para sua funcionalidade.
2. Realize as alterações nos notebooks ou scripts Python.
3. Antes de commitar, certifique-se de que o ambiente está sincronizado (`uv sync`).
4. Faça o push da sua branch e abra um Pull Request.

---

## 📂 Estrutura de Pastas
- `analise_mobilidade_br101.ipynb`: Notebook principal com a extração e cálculos.
- `pyproject.toml`: Definição de dependências do projeto.
- `uv.lock`: Trava de versões para garantir reprodutibilidade.
- `ROTEIRO_A_SEGUIR.md`: Guia de etapas do projeto.
