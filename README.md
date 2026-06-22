# Dashboard de Análise Exploratória de Dados (EDA)

Este dashboard foi projetado para facilitar a etapa inicial e fundamental de qualquer projeto de Ciência de Dados: a **Análise Exploratória de Dados (EDA)**. 
Nele, o usuário encontra ferramentas interativas para cumprir as principais tarefas de pré-processamento e análise estrutural, desde a visualização gráfica dos dados até testes estatísticos de aderência a distribuições.

## 🎯 Funcionalidades e Abas Principais

### 🏠 Início
* **Importação de Dados:** Suporte para upload de arquivos CSV/Excel locais.
* **Integração Externa:** Download de dados de ativos financeiros através da API do Yahoo Finance (`yahooquery`).
* **Visão Geral:** Exibição das primeiras e últimas linhas do *dataset* (Head/Tail) e resumo estatístico preliminar das variáveis.

### 📊 Gráficos
* **Análise Univariada e Bivariada:** Seleção interativa da variável a ser observada.
* **Gráficos Inteligentes:** Renderização automática de gráficos de acordo com o tipo da variável (ex: histogramas para dados contínuos, gráficos de barra para categóricos).
* **Matriz de Correlação:** Visualização interativa da correlação entre as variáveis numéricas (Pearson, Spearman) com o PHO para verificar relação linear ou não.

### 📈 Distribuições
* **Testes de Aderência:** Verificação automática de qual distribuição de probabilidade (Normal, Lognormal, Exponencial, etc.) melhor se encaixa com os dados de cada coluna.
* **Gráficos Estatísticos:** Plotagem de Q-Q plots e curvas de densidade sobrepostas para facilitar a validação visual.

### 🚨 Outliers (Valores Atípicos) *[Nova Sugestão]*
* Identificação visual de outliers através de Boxplots interativos.
* Opções para filtrar, remover ou aplicar métodos de limite (como *Winsorization* ou limites de Z-Score/IQR).

### 🛠️ Dados Faltantes (Missing Values)
* **Mapeamento:** Verificação visual e percentual do total de dados faltantes por coluna.
* **Simulação de Tratamento:** Interface para verificar como os dados se comportariam após possíveis estratégias de imputação/substituição por tipo de categoria. Exemplo:
  * *Dados Categóricos:* Preenchimento por moda ou substituição de valores anômalos (ex: substituir `-0.001` por `0`).
  * *Dados Contínuos:* Imputação de dados faltantes utilizando média, mediana ou algoritmos de interpolação.

### 💾 Dados
* **Visualização em Tabela:** Visualização consolidada do *dataset* após o tratamento.
* **Exportação:** Página dedicada para aplicar filtros adicionais e realizar o download (exportar) dos dados limpos, facilitando o uso do arquivo em modelos de Machine Learning futuros.

---

## 💻 Tecnologias Utilizadas
O projeto foi construído utilizando as seguintes bibliotecas Python:
* **Streamlit:** Criação da interface interativa.
* **Pandas & NumPy:** Manipulação e tratamento dos dados.
* **Plotly & Seaborn:** Geração de gráficos estáticos e dinâmicos de alto nível.
* **YahooQuery:** Extração de dados do mercado financeiro.

## 🚀 Como Executar
```bash
# Instale as dependências
pip install -r requirements.txt

# Execute o dashboard localmente
streamlit run dashboard.py
```
