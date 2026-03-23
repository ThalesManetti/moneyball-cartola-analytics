# ⚽ Football Analytics - Cartola FC Scouting System

> Sistema de análise de dados e Machine Learning para identificar jogadores com melhor custo-benefício no Cartola FC

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-2.0+-green.svg)](https://pandas.pydata.org/)
[![LightGBM](https://img.shields.io/badge/LightGBM-4.0+-orange.svg)](https://lightgbm.readthedocs.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📋 Índice

- [Sobre o Projeto](#-sobre-o-projeto)
- [Tecnologias](#️-tecnologias)
- [Arquitetura](#️-arquitetura)
- [Resultados](#-resultados)
- [Como Executar](#-como-executar)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Insights Principais](#-insights-principais)
- [Contato](#-contato)

---

## 🎯 Sobre o Projeto

Sistema end-to-end de análise de dados para **Cartola FC** (fantasy football brasileiro), com foco em:

1. **Extração de dados** via API pública do Cartola FC
2. **Limpeza e qualidade** de dados (Bronze → Silver → Gold)
3. **Feature Engineering** para criação de métricas avançadas
4. **Sistema de Scouting** baseado em Value Score (custo-benefício)
5. **Machine Learning** para previsão de pontuação de jogadores
6. **Rankings personalizados** por posição
7. **Dashboard Interativo Power BI** com 3 páginas de análise estratégica

### 💡 Problema Resolvido

No Cartola FC, jogadores têm um orçamento limitado (C$ 100) para escalar 12 atletas. O desafio é **maximizar pontos dentro do orçamento**. Este projeto identifica jogadores com **melhor custo-benefício** através de análise de dados e visualização interativa.

---

## 🛠️ Tecnologias

### **Core Stack:**
- **Python 3.11** - Linguagem principal
- **Pandas** - Manipulação de dados
- **NumPy** - Computação numérica
- **LightGBM** - Machine Learning (Gradient Boosting)
- **Scikit-learn** - Pré-processamento e métricas

### **Business Intelligence:**
- **Power BI Desktop** - Dashboard interativo
- **DAX** - 21 medidas customizadas
- **Power Query** - Transformação de dados (Python Script)

### **Visualização:**
- **Matplotlib** - Gráficos estáticos
- **Seaborn** - Visualizações estatísticas

### **Data Engineering:**
- **Parquet** - Armazenamento colunar eficiente
- **Logging** - Rastreabilidade de processos
- **Jupyter Notebooks** - Análise interativa

### **APIs:**
- **Cartola FC API** - Dados de mercado e rodadas
- **StatsBomb API** - Dados de futebol (complementar)

---

## 🏗️ Arquitetura

### **Medalion Architecture (Bronze → Silver → Gold)**

```
┌─────────────────────────────────────────────────────────────┐
│                    DATA PIPELINE                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  API Cartola FC                                             │
│       ↓                                                     │
│  [BRONZE] Raw Data (Parquet)                                │
│       ↓                                                     │
│  [SILVER] Clean Data (Data Quality)                         │
│       ↓                                                     │
│  [GOLD] Features + Models                                   │
│       ↓                                                     │
│  Rankings & Insights                                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### **Notebooks:**

| Notebook | Descrição | Output |
|----------|-----------|--------|
| **01_extraction_cartola** | Extração via API | Bronze Layer (713 atletas) |
| **02_extraction_statsbomb** | Dados complementares | Matches, Events |
| **03_data_quality** | Limpeza e validação | Silver Layer |
| **04_eda_feature_engineering** | Análise + Features | Gold Layer + Features |
| **05_scouting_system** | Rankings por Value Score | Rankings CSV + dim_clubes |
| **06_machine_learning** | Modelo preditivo | LightGBM Model |

### **Power BI Dashboard:**

| Página | Descrição | Visuals |
|--------|-----------|---------|
| **Página 1** | Análise de Quadrantes | Scatter Plot + KPIs |
| **Página 2** | Top Performers | Bar Chart + Table + 4 Cards + 5 Mini-Tables |
| **Página 3** | Análise por Clubes | Club Analytics |

**📊 Sistema de Histórico de Rodadas (V3.0):**
- ✅ Mantém histórico completo de todas as rodadas
- ✅ Análises temporais (tendências, valorizações, comparações)
- ✅ Dimensão `dim_rodadas` para análises evolutivas
- ⚠️ **Nota sobre rodadas antigas:** A API do Cartola FC geralmente mantém dados apenas das últimas 2-3 rodadas. Rodadas muito antigas podem não estar mais disponíveis para download retroativo. O sistema de histórico começa a acumular dados a partir da primeira execução do script de atualização.

---

## 📊 Resultados

### **0. Dashboard Power BI - 3 Páginas Interativas**

**📊 Página 1 - Análise de Quadrantes Estratégicos:**
- **Scatter Plot** com 4 quadrantes de análise:
  - 🥇 **OURO** (Barato + Alto desempenho) - Pechinchas!
  - 💎 **PREMIUM** (Caro + Alto desempenho) - Vale o investimento
  - 💰 **ECONOMIA** (Barato + Baixo desempenho) - Opções de banco
  - ⚠️ **CARO** (Caro + Baixo desempenho) - Evitar!
- Linhas de referência (medianas de Preço e Pontos)
- Cores por Posição, Tamanho por Value Score
- Tooltips completos com detalhes do jogador

**🏆 Página 2 - Top Performers:**
- **Top 10 Bar Chart** - Melhor custo-benefício (sem técnicos)
- **Top 20 Table** - Detalhes completos (Jogador, Posição, Pontos, Preço, Value Score, Categoria)
- **4 Highlight Cards:**
  - 🥇 Melhor Custo-Benefício Geral
  - 💎 Pechincha da Rodada (Quadrante OURO)
  - ⚡ Maior Pontuador
  - 💰 Mais Caro
- **5 Mini-Tables Top 5 por Posição:**
  - 🥅 Goleiros (GOL)
  - 🛡️ Zagueiros (ZAG)
  - ➡️ Laterais (LAT)
  - ⚽ Meio-campistas (MEI)
  - 🎯 Atacantes (ATA)

**🏟️ Página 3 - Análise por Clubes:**
- Estatísticas agregadas por time
- Rankings de clubes por Value Score médio
- Análise de elenco (quantidade e qualidade)

**🔧 Medidas DAX Criadas (21 total):**
- `ValueScore_Universal` - Funciona em todas as tabelas
- `ValueScore_Correto` - Cálculo preciso (Pontos/Preço * 100)
- `Quadrante_Categoria` - Classificação estratégica
- Medidas de clube (Qtd_Jogadores, Preco_Medio, ValueScore_Medio)
- Cards de destaque (Melhor_CustoBeneficio, Pechincha_Rodada, Maior_Pontuador, Mais_Caro)
- Medianas (Preco, Pontos) para linhas de referência

**📈 Modelo de Dados:**
- **10 tabelas** (fato_ranking, dim_clubes, 5 rankings por posição, top_100_value, pechinchas, Medidas)
- **8 relacionamentos** limpos e otimizados
- **713 jogadores** analisados
- **20 clubes** mapeados

### **1. Sistema de Scouting**

**Value Score = Pontos / Preço * 100**

Identificação de jogadores com melhor custo-benefício:

- ✅ **713 atletas** analisados
- ✅ **Rankings por posição** (GOL, ZAG, LAT, MEI, ATA)
- ✅ **Pechinchas identificadas** (Quadrante OURO)
- ✅ **Dashboard interativo** para análise estratégica

**Exemplo de Top 3 Custo-Benefício (Value Score pts/C$100):**
```
1. Walter Clar - LAT - 475 pts, C$ 56 → Value Score: 848.2
2. Danilo - MEI - 1.685 pts, C$ 1.661 → Value Score: 101.4
3. Juninho Capixaba - LAT - 1.255 pts, C$ 1.354 → Value Score: 92.7
```

### **2. Machine Learning**

**Algoritmo:** LightGBM (Gradient Boosting)

**Performance (Teste):**
- **MAE:** ~3.0-4.0 pontos (erro médio absoluto)
- **RMSE:** ~4.5-5.5 pontos
- **R²:** ~0.50-0.60 (50-60% da variância explicada)

**Interpretação Prática:**
> Se o modelo prever 10 pontos, o valor real estará entre 7-13 pontos com 95% de confiança.

**Features Mais Importantes:**
1. `preco_num` - Preço (proxy de qualidade)
2. `posicao_encoded` - Posição (atacantes pontuam mais)
3. `media_num` - Média histórica
4. `value_score` - Custo-benefício

### **3. Feature Engineering**

**Features Criadas (8 novas):**
- `pontos_por_jogo` - Média de pontos
- `custo_beneficio` - Value Score
- `categoria_pontos` - Classificação
- `destaque` - Top 10% da rodada
- `pontos_rolling_avg` - Média móvel (3 jogos)
- `tendencia` - Em alta/baixa
- `consistencia` - Desvio padrão
- `freq_destaque` - Frequência de destaques

---

## 🚀 Como Executar

### **Pré-requisitos:**

```bash
# Python 3.11+
python --version

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instalar dependências
pip install -r requirements.txt
```

### **Executar Pipeline Completo:**

```bash
# 1. Extração de dados
jupyter notebook notebooks/01_extraction_cartola.ipynb

# 2. Limpeza
jupyter notebook notebooks/03_data_quality.ipynb

# 3. Feature Engineering
jupyter notebook notebooks/04_eda_feature_engineering.ipynb

# 4. Sistema de Scouting
jupyter notebook notebooks/05_scouting_system.ipynb

# 5. Machine Learning
jupyter notebook notebooks/06_machine_learning.ipynb
```

**Tempo total de execução:** ~3-5 minutos

### **Usar o Dashboard Power BI:**

```bash
# 1. Atualizar dados semanalmente (após cada rodada) - V3.0 com Histórico
cd "D:\football analytics project"
python atualizar_cartola_v3.py

# O script V3.0 automaticamente:
# - Baixa dados da nova rodada via API
# - Adiciona ao histórico (sem perder rodadas anteriores)
# - Atualiza ranking_historico.parquet (todas as rodadas)
# - Atualiza ranking_completo.parquet (rodada atual)
# - Atualiza dim_rodadas.csv (dimensão temporal)
# - Cria backups timestamped

# 2. Abrir o dashboard
# - Abra o arquivo .pbix no Power BI Desktop
# - Home → Refresh (para carregar dados atualizados)

# 3. Navegar pelas 3 páginas:
# - Página 1: Análise de Quadrantes (visão geral estratégica)
# - Página 2: Top Performers (rankings e destaques)
# - Página 3: Análise por Clubes (estatísticas por time)
```

**Dashboard Features:**
- 🔄 **Atualização semanal** automática via Python script V3.0
- 📚 **Histórico completo** de rodadas (análises temporais)
- 📊 **dim_rodadas** para comparações entre rodadas
- 🎯 **Filtros interativos** por posição, clube, quadrante, rodada
- 📈 **Análises de tendências** (valorizações, desvalorizações, consistência)
- 📊 **21 medidas DAX base** + 15 medidas temporais calculadas dinamicamente
- 💾 **Backup automático** com timestamp (arquivos .parquet)

**⚠️ Importante sobre Histórico:**
> O sistema de histórico inicia da primeira vez que você executa `atualizar_cartola_v3.py`. A API do Cartola FC geralmente **não disponibiliza rodadas muito antigas** para download retroativo. Por isso, é recomendado executar o script semanalmente para **acumular o histórico progressivamente** a partir da rodada atual.

---

## 📁 Estrutura do Projeto

```
football-analytics/
│
├── data/
│   ├── bronze/              # Dados brutos da API
│   ├── silver/              # Dados limpos
│   ├── gold/                # Features + Rankings
│   │   ├── features/
│   │   └── scouting/
│   │       ├── ranking_historico.parquet     # ⭐ NOVO: Histórico completo
│   │       ├── ranking_completo.parquet      # Dataset da rodada atual
│   │       ├── dim_rodadas.csv               # ⭐ NOVO: Dimensão temporal
│   │       ├── dim_clubes.csv                # Dimensão de clubes
│   │       ├── top_100_value.csv             # Top 100 jogadores
│   │       ├── pechinchas.csv                # Quadrante OURO
│   │       └── ranking_*.csv                 # Rankings por posição
│   └── powerbi/             # Backups timestamped
│
├── notebooks/
│   ├── 01_extraction_cartola.ipynb
│   ├── 02_extraction_statsbomb.ipynb
│   ├── 03_data_quality.ipynb
│   ├── 04_eda_feature_engineering.ipynb
│   ├── 05_scouting_system.ipynb              # ⭐ Atualizado com dim_clubes
│   └── 06_machine_learning.ipynb
│
├── dashboards/
│   └── cartola_scouting.pbix                 # ⭐ Dashboard Power BI (3 páginas)
│
├── src/
│   ├── utils/
│   │   ├── config.py                         # Configurações
│   │   └── logger.py                         # Logging
│   ├── atualizar_cartola_v3.py               # ⭐ Script V3 com histórico
│   ├── iniciar_historico_simples.py          # Criar histórico inicial
│   └── scripts auxiliares/                   # Troubleshooting, conversores
│
├── models/
│   ├── lightgbm_pontos.txt  # Modelo treinado
│   ├── metrics.json
│   └── feature_importance.csv
│
├── logs/                    # Logs de execução
│
├── docs/
│   ├── POWERBI_DASHBOARD.md                  # Documentação técnica completa
│   └── MEDIDAS_DAX_TEMPORAIS.md              # 15 medidas para análises temporais
│
├── requirements.txt
└── README.md
```

---

## 💡 Insights Principais

### **0. Dashboard Power BI - Descobertas Visuais**

**🎯 Sistema de Quadrantes:**
> O Quadrante OURO identifica **pechinchas extremas** - jogadores com Value Score > 100 custando < C$ 100

**Exemplo Real:** Walter Clar (LAT)
- Preço: C$ 56 (muito barato)
- Pontos: 475 (alta pontuação)
- Value Score: 848.2 pts/C$100 (**15x acima da média!**)

**📊 Top 5 por Posição:**
- **Goleiros:** Value Score médio ~60-75
- **Zagueiros:** Mais estáveis, VS ~40-60
- **Laterais:** **Melhor custo-benefício**, VS ~80-100
- **Meio-campistas:** VS ~50-70, boa consistência
- **Atacantes:** VS ~50-80, maior variância

**🏆 Clubs Analytics:**
- Red Bull Bragantino: Melhor Value Score médio (212.9)
- Chapecoense: Elenco barato com bom desempenho (VS 132.1)
- Palmeiras: Time mais caro (C$ 521 médio)

### **1. Custo-Benefício**

> Jogadores baratos (< C$ 5) podem ter **Value Score 2-3x maior** que jogadores caros

**Estratégia:** Escalar 2-3 jogadores premium + 9-10 "pechinchas"

### **2. Posições**

- **Atacantes:** Maior média de pontos (variância alta)
- **Meio-campistas:** Melhor custo-benefício (consistência)
- **Zagueiros:** Pontuação estável (baixo risco)

### **3. Previsibilidade**

- **50-60% da variância** dos pontos pode ser explicada por features básicas
- **Preço é o melhor preditor** (correlação forte com qualidade)
- **Média histórica** é fundamental para consistência

### **4. Descobertas Técnicas**

- API Cartola retorna apenas **rodadas atuais** (sem histórico completo via endpoint público)
- **692 atletas** disponíveis no mercado atual (2025)
- Rodada 1 teve **336 atletas que jogaram** (~48% do mercado)

---

## ⚠️ Limitações e Considerações

### **1. Histórico de Rodadas:**
A API do Cartola FC **não mantém dados de rodadas muito antigas** (geralmente apenas as últimas 2-3 rodadas estão disponíveis). Por isso:
- ✅ O sistema de histórico inicia **a partir da primeira execução** do script V3.0
- ✅ Recomenda-se executar `atualizar_cartola_v3.py` **semanalmente** após cada rodada
- ✅ O histórico vai **acumulando progressivamente** rodada após rodada
- ❌ **Não é possível baixar retroativamente** rodadas muito antigas da API

**Solução Implementada:**
- Script V3.0 mantém `ranking_historico.parquet` com todas as rodadas acumuladas
- Backups timestamped automáticos a cada execução
- `dim_rodadas.csv` para análises temporais

**Dica:** Execute o script desde o início do campeonato e mantenha os backups dos arquivos `.parquet` gerados para garantir histórico completo.

### **2. Qualidade dos Dados:**
- Dados dependem da API pública do Cartola FC (disponibilidade e uptime)
- Pontuação pode ser atualizada/corrigida após a rodada
- Mercado fechado pode mostrar `pontos_num = 0` (script usa `media_num` como fallback)
- Status de jogadores (contundidos, suspensos) pode mudar entre a extração e o jogo

### **3. Machine Learning:**
- Modelo tem alta variância devido à natureza imprevisível do futebol
- Fatores externos não capturados: lesões de última hora, mudanças táticas, clima
- Melhor uso: **triagem inicial** combinada com análise contextual manual
- Performance: R² ~0.50-0.60 (50-60% da variância explicada)
- MAE ~3-4 pontos (erro médio absoluto aceitável para classificação)

---

## 📈 Próximos Passos

- [x] ✅ **Dashboard interativo Power BI** (3 páginas completas)
- [x] ✅ **Sistema de histórico de rodadas** (V3.0 implementado)
- [x] ✅ **Análises temporais** (dim_rodadas + 15 medidas DAX)
- [ ] Publicar dashboard no Power BI Service
- [ ] Implementar Página 4 do dashboard (Análise Temporal completa)
- [ ] Modelo de classificação (jogará ou não?)
- [ ] Análise de adversários (dificuldade de partida)
- [ ] Sistema de recomendação de time completo (12 jogadores otimizado)
- [ ] Deploy do modelo (API REST)
- [ ] Automação via Azure Functions / GitHub Actions

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

---

## 📄 Licença

Distribuído sob a licença MIT. Veja `LICENSE` para mais informações.

---

## 👤 Contato

**Thales Gazola Manetti**

- LinkedIn: [Thales Gazola Manetti](https://linkedin.com/in/thalesmanetti)
- GitHub: [@ThalesManetti](https://github.com/ThalesManetti)
- Email: thalesmanetti@gmail.com

**Link do Projeto:** [https://github.com/ThalesManetti/football-analytics](https://github.com/ThalesManetti/football-analytics)

---

## 🙏 Agradecimentos

- [Cartola FC](https://cartola.globo.com/) - API de dados
- [StatsBomb](https://statsbomb.com/) - Dados de futebol
- [LightGBM](https://lightgbm.readthedocs.io/) - Framework de ML
- Comunidade Python & Data Science

---

## 📊 Estatísticas do Projeto

```python
# Dados processados
Atletas analisados: 713
Clubes mapeados: 20
Features criadas: 8
Modelos treinados: 1 (LightGBM)
Medidas DAX: 21
Páginas Dashboard: 3
Relacionamentos: 8
Linhas de código: ~3.000+
Tempo de execução: ~3-5 minutos (pipeline completo)
Acurácia (R²): ~0.50-0.60
```

---

<p align="center">
  Feito com ❤️ e ⚽ para a comunidade de Data Science
</p>

<p align="center">
  <sub>⭐ Se este projeto te ajudou, deixe uma estrela no GitHub!</sub>
</p>
