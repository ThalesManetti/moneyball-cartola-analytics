<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0A0F1E,50:00E5FF,100:FF6B2B&height=180&section=header&text=Money%20Ball%20%E2%80%94%20Cartola%20FC%20Scouting&fontSize=38&fontColor=ffffff&fontAlignY=38&desc=Python%20%7C%20Machine%20Learning%20%7C%20Power%20BI%20%7C%20Sistema%20de%20Scouting&descAlignY=58&descSize=16&animation=fadeIn" width="100%"/>

</div>

<br/>

<div align="center">

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Power BI](https://img.shields.io/badge/Power%20BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)
![LightGBM](https://img.shields.io/badge/LightGBM-2EA44F?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Status](https://img.shields.io/badge/Status-Conclu%C3%ADdo-2EA44F?style=for-the-badge)
![Nível](https://img.shields.io/badge/N%C3%ADvel-Pleno%20%2F%20S%C3%AAnior-FF6B2B?style=for-the-badge)

</div>

<div align="center">

🔗 **[Acessar Dashboard no Power BI Service](https://app.powerbi.com/reportEmbed?reportId=37ccd3ae-7036-4a0b-a987-557d324d8d7b&autoAuth=true&ctid=57d2ea99-01a6-4ab8-86bb-75c0642ef771)**

</div>

---

## 🎬 A História do Projeto

A ideia original era ambiciosa: replicar a lógica do *Moneyball* no futebol brasileiro real — coletar dados da Série A, identificar jogadores subvalorizados fora do radar dos grandes clubes e construir um sistema de scouting baseado em dados públicos.

O obstáculo foi real: **dados históricos detalhados da Série A não estão disponíveis gratuitamente em APIs públicas**. Pagar por feeds profissionais de dados (Opta, StatsBomb) estava fora do escopo do projeto.

A decisão foi pivotear com inteligência. O **Cartola FC** — o maior fantasy football do Brasil com milhões de jogadores — tem uma API pública gratuita com dados reais de todos os atletas do Brasileirão. Mesma lógica analítica, mesmo desafio de otimização, dados acessíveis.

> *O problema mudou de escala, mas a essência permaneceu: encontrar valor onde os outros não estão olhando.*

---

## 🎯 O Problema

No Cartola FC, cada usuário tem **C$ 100 de orçamento** para escalar **12 atletas por rodada**. Com 713 jogadores disponíveis no mercado, a maioria das pessoas escala por intuição — nomes conhecidos, jogadores caros, times grandes.

**A questão analítica:** existe um padrão nos dados que identifica jogadores com alto desempenho e preço baixo *antes* que o mercado perceba e valorize?

**Decisões que o sistema responde:**
- Quais jogadores têm o melhor custo-benefício nesta rodada?
- Quais pechinchas estão no Quadrante OURO antes da valorização?
- Quais times têm elencos com alto Value Score e preço acessível?
- Como está a tendência de um jogador nas últimas rodadas?

---

## 📊 Dados

| Dimensão | Detalhe |
|----------|---------|
| **Fonte** | API pública do Cartola FC (dados reais) |
| **Atletas** | 713 por rodada |
| **Atualização** | Semanal — após cada rodada |
| **Histórico** | Acumulado desde Rodada 4/2026 (V3.0) |
| **Modelo** | Star Schema — `fato_ranking_historico` + dimensões |

---

## 🧮 Value Score — A Métrica Central

```
Value Score = Pontos ÷ Preço × 100
```

Quanto maior o Value Score, melhor o retorno por cruzeiro investido. A métrica divide o mercado em **4 quadrantes estratégicos**, usando medianas como linhas de corte dinâmicas:

| Quadrante | Perfil | Estratégia |
|-----------|--------|------------|
| 🥇 **OURO** | Barato + Alta pontuação | **Comprar** — pechinchas reais |
| 💎 **PREMIUM** | Caro + Alta pontuação | Investimento justificado |
| 💰 **ECONOMIA** | Barato + Baixa pontuação | Banco — custo baixo |
| ⚠️ **CARO** | Caro + Baixa pontuação | **Evitar** — pior ROI |

> Medianas de referência: **C$ 641** (preço) · **65 pontos**

---

## 💡 Principais Insights

### 1. Laterais = Melhor Posição para Value Score
Laterais têm Value Score médio de **80–100**, enquanto outras posições ficam entre 50–70. Priorizar LAT na montagem do time maximiza o ROI do orçamento disponível.

### 2. Pechincha Extrema — Walter Clar (LAT)
```
Preço:       C$ 56    (muito abaixo da mediana de C$ 641)
Pontos:      475
Value Score: 848.2    → 15x acima da média do mercado
```
Jogadores no Quadrante OURO com preço abaixo de C$ 100 são oportunidades raras que o sistema identifica antes da valorização.

### 3. Times de Série B = Valor Escondido
A **Chapecoense** tem Value Score médio de **132.1** (2º melhor entre todos os clubes), com preço médio de elenco acessível. Elencos de times menores oferecem pechinchas ignoradas pela maioria dos jogadores.

---

## 📐 Estratégia Recomendada pelo Sistema

**Regra 80/20 aplicada ao Cartola:**
- **80% do orçamento** → 8–9 jogadores do Quadrante OURO (Value Score alto, preço baixo)
- **20% do orçamento** → 2–3 jogadores PREMIUM de alta pontuação garantida

**Sinais de timing para compra/venda (V3.0):**
- Δ Pontos positivo + Preço estável → **comprar antes da valorização**
- Jogador valorizado + Δ Pontos negativo → **vender antes da queda**

---

## 🤖 Machine Learning

Modelo **LightGBM** para previsão de pontuação por rodada:

| Métrica | Resultado |
|---------|-----------|
| Algoritmo | LightGBM (Gradient Boosting) |
| MAE | ~3–4 pontos |
| RMSE | ~4.5–5.5 pontos |
| R² | ~0.50–0.60 |

> Se o modelo prever 10 pontos, o valor real estará entre 7–13 com 95% de confiança — suficiente para ranquear e priorizar.

**Features mais importantes:** preço (proxy de qualidade), posição, média histórica, Value Score calculado.

---

## 🖥️ Dashboard Power BI — 3 Páginas

| Página | O que mostra |
|--------|-------------|
| 🎯 **Quadrantes** | Scatter plot com 713 jogadores posicionados nos 4 quadrantes |
| 🏆 **Top Performers** | Top 10/20 ranking + 4 cards de destaque + Top 5 por posição |
| 🏟️ **Análise por Clubes** | Rankings de times por Value Score médio e perfil de elenco |

---

## 📸 Screenshots

> *Em breve — prints do dashboard serão adicionados após a próxima rodada.*

---

## 🛠️ Stack

```
Linguagem         →  Python 3.11
Análise de Dados  →  Pandas · NumPy
Machine Learning  →  LightGBM · Scikit-learn
Visualização      →  Matplotlib · Seaborn · Power BI
Armazenamento     →  Parquet (colunar)
BI / DAX          →  21 medidas base + 15 medidas temporais
```

📄 Para detalhes técnicos completos (pipeline ETL, arquitetura, notebooks, como executar), veja o [TECHNICAL.md](TECHNICAL.md).

---

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:FF6B2B,50:00E5FF,100:0A0F1E&height=100&section=footer" width="100%"/>

**Thales Manetti** · [LinkedIn](https://www.linkedin.com/in/thalesmanetti/) · [Portfólio](https://thalesmanetti.github.io)

</div>

