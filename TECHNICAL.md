# TECHNICAL.md — Money Ball: Cartola FC Scouting System

Documentação técnica completa do projeto. Para a visão de negócio e insights, veja o [README.md](README.md).

---

## 🏗️ Arquitetura — Medallion (Bronze → Silver → Gold)

```
API Cartola FC
      ↓
[BRONZE]  Raw Data             → Parquet (dados brutos da API)
      ↓
[SILVER]  Clean Data           → Validação, limpeza, normalização
      ↓
[GOLD]    Features + Rankings  → Value Score, quadrantes, ML features
      ↓
Rankings CSV + Power BI Dashboard
```

---

## 📁 Estrutura de Pastas

```
moneyball-cartola-analytics/
│
├── README.md                          ← Case study (negócio + insights)
├── TECHNICAL.md                       ← Este arquivo
├── requirements.txt
│
├── notebooks/
│   ├── 01_extraction_cartola.ipynb    ← Extração via API → Bronze (713 atletas)
│   ├── 02_extraction_statsbomb.ipynb  ← Dados complementares
│   ├── 03_data_quality.ipynb          ← Limpeza e validação → Silver
│   ├── 04_eda_feature_engineering.ipynb ← EDA + Features → Gold
│   ├── 05_scouting_system.ipynb       ← Rankings por Value Score
│   └── 06_machine_learning.ipynb      ← Modelo LightGBM
│
├── src/
│   ├── utils/
│   │   ├── config.py                  ← Configurações globais
│   │   └── logger.py                  ← Logging estruturado
│   ├── atualizar_cartola_v3.py        ← ⭐ Script principal V3 (histórico)
│   └── iniciar_historico_simples.py   ← Bootstrap do histórico inicial
│
├── data/
│   ├── bronze/                        ← Dados brutos da API
│   ├── silver/                        ← Dados limpos
│   └── gold/
│       ├── features/
│       └── scouting/
│           ├── ranking_historico.parquet  ← ⭐ Histórico completo (todas as rodadas)
│           ├── ranking_completo.parquet   ← Rodada atual
│           ├── dim_rodadas.csv            ← Dimensão temporal
│           ├── dim_clubes.csv             ← Dimensão de clubes
│           ├── top_100_value.csv
│           ├── pechinchas.csv             ← Quadrante OURO
│           └── ranking_[posição].csv      ← Rankings por posição
│
├── dashboards/
│   └── cartola_scouting.pbix          ← Dashboard Power BI
│
├── models/
│   ├── lightgbm_pontos.txt            ← Modelo treinado (serializado)
│   ├── metrics.json                   ← Métricas de avaliação
│   └── feature_importance.csv
│
├── docs/
│   ├── POWERBI_DASHBOARD.md           ← Documentação técnica do dashboard
│   └── MEDIDAS_DAX_TEMPORAIS.md       ← 15 medidas para análises temporais
│
└── logs/                              ← Logs de execução com timestamp
```

---

## 🗄️ Modelagem de Dados (Star Schema)

```
Tabela Fato
  └── fato_ranking_historico
        ├── atleta_id (FK → dim_clubes)
        ├── rodada_id (FK → dim_rodadas)
        ├── pontos_num
        ├── preco_num
        └── value_score

Tabelas Dimensão
  ├── dim_clubes      (20 clubes, Many-to-One)
  └── dim_rodadas     (dimensão temporal, Rodada 4/2026+)

Tabelas de Ranking (Gold Layer)
  ├── top_100_value       (top geral)
  ├── pechinchas          (Quadrante OURO)
  └── ranking_[posição]   (GOL, ZAG, LAT, MEI, ATA)
```

**8 relacionamentos** validados (Many-to-One, cross-filtering unidirecional).

---

## ⚙️ Feature Engineering — 8 Features Criadas

| Feature | Descrição |
|---------|-----------|
| `pontos_por_jogo` | Média de pontos por rodada jogada |
| `custo_beneficio` | Value Score = Pontos / Preço × 100 |
| `categoria_pontos` | Classificação em quartis (baixo/médio/alto/elite) |
| `destaque` | Flag top 10% da rodada (binário) |
| `pontos_rolling_avg` | Média móvel dos últimos 3 jogos |
| `tendencia` | Δ pontos entre rodadas (em alta / em baixa) |
| `consistencia` | Desvio padrão histórico (confiabilidade) |
| `freq_destaque` | Frequência de aparição entre top 10% |

---

## 🤖 Modelo de Machine Learning

**Algoritmo:** LightGBM (Gradient Boosting)

```python
# Parâmetros principais
params = {
    'objective': 'regression',
    'metric': 'mae',
    'boosting_type': 'gbdt',
    'num_leaves': 31,
    'learning_rate': 0.05,
    'feature_fraction': 0.9
}
```

**Performance no conjunto de teste:**

| Métrica | Valor |
|---------|-------|
| MAE | ~3.0–4.0 pontos |
| RMSE | ~4.5–5.5 pontos |
| R² | ~0.50–0.60 |

**Features por importância:**
1. `preco_num` — preço (proxy de qualidade)
2. `posicao_encoded` — posição (atacantes pontuam mais)
3. `media_num` — média histórica
4. `value_score` — custo-benefício calculado

**Interpretação prática:** previsão de 10 pontos → valor real entre 7–13 com 95% de confiança. Suficiente para ranquear e priorizar, não para prever pontuação exata.

---

## 📊 Power BI — Medidas DAX

**21 medidas base + 15 medidas temporais** (36 total).

### Medidas Principais

| Medida | Fórmula / Descrição |
|--------|---------------------|
| `ValueScore_Universal` | Funciona em qualquer contexto de tabela |
| `ValueScore_Correto` | `Pontos / Preço * 100` — cálculo preciso |
| `Quadrante_Categoria` | Classifica em OURO / PREMIUM / ECONOMIA / CARO |
| `Melhor_CustoBeneficio` | Card de destaque — melhor Value Score geral |
| `Pechincha_Rodada` | Card — melhor do Quadrante OURO |
| `Maior_Pontuador` | Card — maior pontuação absoluta |
| `Mais_Caro` | Card — maior preço do mercado |
| `Preco_Mediana` | Linha de corte dinâmica para quadrantes |
| `Pontos_Mediana` | Linha de corte dinâmica para quadrantes |

### Medidas Temporais (V3.0)

Documentação completa em [`docs/MEDIDAS_DAX_TEMPORAIS.md`](docs/MEDIDAS_DAX_TEMPORAIS.md).

---

## 🚀 Como Executar

### Pré-requisitos

```bash
python --version  # Python 3.11+
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows
pip install -r requirements.txt
```

### Pipeline completo (primeira vez)

```bash
# 1. Extrair dados da API Cartola FC
jupyter notebook notebooks/01_extraction_cartola.ipynb

# 2. Limpeza e qualidade
jupyter notebook notebooks/03_data_quality.ipynb

# 3. Feature Engineering
jupyter notebook notebooks/04_eda_feature_engineering.ipynb

# 4. Sistema de Scouting + Rankings
jupyter notebook notebooks/05_scouting_system.ipynb

# 5. Treinar modelo ML
jupyter notebook notebooks/06_machine_learning.ipynb
```

⏱️ Tempo total estimado: **3–5 minutos**

### Atualização semanal (após cada rodada)

```bash
cd caminho/do/projeto
python src/atualizar_cartola_v3.py
```

O script V3.0 automaticamente:
- Baixa dados da nova rodada via API
- Adiciona ao histórico sem sobrescrever rodadas anteriores
- Atualiza `ranking_historico.parquet` e `ranking_completo.parquet`
- Atualiza `dim_rodadas.csv`
- Cria backup com timestamp em `data/gold/powerbi/`

### Atualizar o Dashboard

```
1. Abrir cartola_scouting.pbix no Power BI Desktop
2. Home → Refresh
3. Navegar pelas 3 páginas
```

---

## ⚠️ Limitações Conhecidas

**API do Cartola FC:**
- Mantém apenas as últimas 2–3 rodadas disponíveis via endpoint público
- Não é possível baixar retroativamente rodadas muito antigas
- Solução: executar `atualizar_cartola_v3.py` semanalmente para acumular histórico progressivamente

**Qualidade dos dados:**
- Pontuação pode ser atualizada/corrigida após a rodada
- Mercado fechado exibe `pontos_num = 0` — script usa `media_num` como fallback
- Status de jogadores (contundidos, suspensos) pode mudar entre extração e jogo

**Modelo de ML:**
- R² ~0.50–0.60: futebol tem alta variância por natureza
- Fatores externos não capturados: lesões de última hora, mudanças táticas, clima
- Uso recomendado: triagem inicial combinada com análise contextual manual

---

## 📈 Roadmap

- [x] Pipeline ETL completo (Bronze → Silver → Gold)
- [x] Sistema de scouting com Value Score
- [x] Dashboard Power BI (3 páginas)
- [x] Modelo LightGBM
- [x] Histórico de rodadas V3.0
- [x] 15 medidas DAX temporais
- [x] Publicar dashboard no Power BI Service (público)
- [ ] Página 4 — Análise Temporal completa
- [ ] Sistema de recomendação de time completo (12 jogadores otimizados)


---

*Documentação técnica por [Thales Manetti](https://www.linkedin.com/in/thalesmanetti/)*
