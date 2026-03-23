"""
ATUALIZAÇÃO AUTOMÁTICA - CARTOLA FC
====================================

Este script:
1. Busca a rodada atual na API do Cartola
2. Baixa dados atualizados do mercado
3. Atualiza ranking_completo.parquet
4. Recalcula métricas e value scores
5. Atualiza dim_clubes
6. Gera novos arquivos para Power BI

Colunas padronizadas com os notebooks do projeto:
  apelido, posicao_nome, clube_id, pontos_num, preco_num, media_num,
  value_score, value_score_normalized, value_categoria

Autor: Thales Gazola Manetti
Data: 2026-02-12
Versão: 3.0
"""

import sys
import os

# Garantir UTF-8 no console Windows (suporte a emojis)
if sys.platform == 'win32':
    os.system('chcp 65001 >nul 2>&1')
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

import pandas as pd
import requests
from pathlib import Path
import warnings
import re
from datetime import datetime
warnings.filterwarnings('ignore')

# ========================================
# CONFIGURAÇÕES
# ========================================
BASE_DIR = Path(r'D:\football analytics project\data')
GOLD_DIR = BASE_DIR / 'gold' / 'scouting'
GOLD_DIR.mkdir(parents=True, exist_ok=True)

# Posições Cartola FC (mesmo mapeamento do config.py)
CARTOLA_POSITIONS = {
    1: 'GOL',
    2: 'LAT',
    3: 'ZAG',
    4: 'MEI',
    5: 'ATA',
    6: 'TEC'
}

# API Cartola
API_BASE = "https://api.cartolafc.globo.com"

print("=" * 80)
print(" " * 20 + "🔄 ATUALIZAÇÃO AUTOMÁTICA - CARTOLA FC")
print("=" * 80)
print(f"📅 Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 80)

# ========================================
# 1. VERIFICAR RODADA ATUAL
# ========================================
print("\n[1/7] 🔍 Verificando rodada atual...")

try:
    response = requests.get(f"{API_BASE}/mercado/status", timeout=10)
    mercado_status = response.json()

    rodada_atual = mercado_status.get('rodada_atual', 1)
    mercado_aberto = mercado_status.get('status_mercado', 1) == 1

    print(f"   ✅ Rodada atual: {rodada_atual}")
    print(f"   {'✅' if mercado_aberto else '🔒'} Mercado: {'ABERTO' if mercado_aberto else 'FECHADO'}")

except Exception as e:
    print(f"   ⚠️  Erro ao verificar rodada: {e}")
    print(f"   ℹ️  Continuando com atualização mesmo assim...")
    rodada_atual = None

# ========================================
# 2. BUSCAR DADOS DO MERCADO
# ========================================
print("\n[2/7] 📥 Baixando dados do mercado...")

try:
    response = requests.get(f"{API_BASE}/atletas/mercado", timeout=15)
    data = response.json()

    # Extrair atletas
    atletas_api = pd.DataFrame(data['atletas'])
    print(f"   ✅ {len(atletas_api)} atletas baixados")

    # Extrair clubes (para dim_clubes)
    clubes_api = pd.DataFrame.from_dict(data['clubes'], orient='index')
    clubes_api = clubes_api.reset_index(drop=True)
    clubes_api['id'] = clubes_api['id'].astype(int)
    print(f"   ✅ {len(clubes_api)} clubes baixados")

    api_success = True

except Exception as e:
    print(f"   ❌ Erro ao baixar dados: {e}")
    print(f"   ⚠️  Usando dados locais existentes...")
    api_success = False

# ========================================
# 3. PROCESSAR DADOS
# ========================================
print("\n[3/7] ⚙️  Processando dados...")

if api_success:
    df = atletas_api.copy()

    # Adicionar posicao_nome (mesmo padrão do notebook 01)
    df['posicao_nome'] = df['posicao_id'].map(CARTOLA_POSITIONS)

    # Usar media_num como pontos_num quando pontos_num estiver zerado
    # (pontos_num = pontos da ultima rodada, zerado quando mercado fechado;
    #  media_num = media por rodada na temporada, sempre disponivel)
    if df['pontos_num'].sum() == 0 and df['media_num'].sum() != 0:
        df['pontos_num'] = df['media_num']
        print(f"   ℹ️  pontos_num zerado (mercado fechado), usando media_num")

    # Manter apenas colunas relevantes (padrão dos notebooks)
    colunas_manter = [
        'atleta_id', 'apelido', 'apelido_abreviado', 'nome', 'foto', 'slug',
        'clube_id', 'posicao_id', 'posicao_nome', 'rodada_id', 'status_id',
        'pontos_num', 'media_num', 'preco_num', 'variacao_num',
        'jogos_num', 'entrou_em_campo'
    ]
    colunas_disponiveis = [c for c in colunas_manter if c in df.columns]
    df = df[colunas_disponiveis]

    print(f"   ✅ Dados processados: {len(df)} atletas, {len(df.columns)} colunas")

else:
    # Carregar ranking local
    try:
        df = pd.read_parquet(GOLD_DIR / 'ranking_completo.parquet')
        print(f"   ✅ Dados locais carregados: {len(df)} atletas")
    except Exception as e:
        print(f"   ❌ Erro ao carregar dados locais: {e}")
        raise

# ========================================
# 4. CALCULAR VALUE SCORES
# ========================================
print("\n[4/7] 📊 Calculando métricas...")

# Filtrar apenas jogadores com preço
df = df[df['preco_num'] > 0].copy()

# value_score (mesmo nome do notebook 05)
df['value_score'] = df.apply(
    lambda row: (row['pontos_num'] / row['preco_num']) if row['preco_num'] > 0 else 0,
    axis=1
)

# value_score_normalized 0-100 (mesmo nome do notebook 05)
from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler(feature_range=(0, 100))
df['value_score_normalized'] = scaler.fit_transform(df[['value_score']])

# value_categoria (mesmo nome e mesmas faixas do notebook 05)
df['value_categoria'] = pd.cut(
    df['value_score_normalized'],
    bins=[0, 25, 50, 75, 100],
    labels=['Baixo', 'Médio', 'Alto', 'Excelente'],
    include_lowest=True
)

# Quadrante (feature extra para Power BI, usando medianas)
jogadores_que_pontuaram = df[df['pontos_num'] > 0]

if len(jogadores_que_pontuaram) > 0:
    mediana_preco = jogadores_que_pontuaram['preco_num'].median()
    mediana_pontos = jogadores_que_pontuaram['pontos_num'].median()

    def categorizar_quadrante(row):
        if row['pontos_num'] <= 0:
            return 'Nao jogou/Negativo'

        preco_alto = row['preco_num'] >= mediana_preco
        pontos_alto = row['pontos_num'] >= mediana_pontos

        if pontos_alto and not preco_alto:
            return 'OURO'
        elif pontos_alto and preco_alto:
            return 'PREMIUM'
        elif not pontos_alto and not preco_alto:
            return 'ECONOMIA'
        else:
            return 'CARO'

    df['Quadrante_Categoria'] = df.apply(categorizar_quadrante, axis=1)

    print(f"   ✅ Mediana Preço: C$ {mediana_preco:.2f}")
    print(f"   ✅ Mediana Pontos: {mediana_pontos:.2f}")
else:
    df['Quadrante_Categoria'] = 'Sem dados'
    print(f"   ⚠️  Nenhum jogador pontuou ainda")

print(f"   ✅ Value Scores calculados")
print(f"   ℹ️  Melhor value_score: {df['value_score'].max():.2f}")
print(f"   ℹ️  value_score médio: {df['value_score'].mean():.2f}")

# ========================================
# 5. CRIAR DIM_CLUBES
# ========================================
print("\n[5/7] 🏟️  Criando dimensão de clubes...")

def extrair_codigo_clube(url_foto):
    """Extrai código do clube da URL da foto"""
    if pd.isna(url_foto):
        return None
    match = re.search(r'/silhuetas/([A-Z]+)/', str(url_foto))
    if match:
        return match.group(1)
    return None

CODIGO_PARA_NOME = {
    'FLA': 'Flamengo', 'BOT': 'Botafogo', 'FLU': 'Fluminense', 'VAS': 'Vasco',
    'SAO': 'São Paulo', 'PAL': 'Palmeiras', 'COR': 'Corinthians', 'SAN': 'Santos',
    'CAM': 'Atlético-MG', 'CRU': 'Cruzeiro', 'GRE': 'Grêmio', 'INT': 'Internacional',
    'CAP': 'Athletico-PR', 'BAH': 'Bahia', 'FOR': 'Fortaleza', 'CFC': 'Coritiba',
    'VIT': 'Vitória', 'GOI': 'Goiás', 'CEA': 'Ceará', 'SPO': 'Sport',
    'RBB': 'Red Bull Bragantino', 'CUI': 'Cuiabá', 'JUV': 'Juventude', 'ACG': 'Atlético-GO',
    'AME': 'América-MG', 'PON': 'Ponte Preta', 'AVA': 'Avaí', 'CHA': 'Chapecoense',
}

if 'foto' in df.columns:
    codigos = df[['clube_id', 'foto']].drop_duplicates(subset='clube_id')
    codigos['codigo_clube'] = codigos['foto'].apply(extrair_codigo_clube)
    codigos = codigos[codigos['codigo_clube'].notna()]
    codigos['Clube'] = codigos['codigo_clube'].map(CODIGO_PARA_NOME)
    codigos['Clube'] = codigos['Clube'].fillna(codigos['codigo_clube'])

    # dim_clubes com ID_Clube (mesmo padrão do notebook 05)
    dim_clubes = codigos[['clube_id', 'Clube']].rename(
        columns={'clube_id': 'ID_Clube'}
    ).sort_values('ID_Clube').reset_index(drop=True)

    print(f"   ✅ dim_clubes criada: {len(dim_clubes)} clubes")

    clubes_no_ranking = df['clube_id'].nunique()
    if clubes_no_ranking == len(dim_clubes):
        print(f"   ✅ Integridade OK: Todos os {clubes_no_ranking} clubes mapeados")
    else:
        print(f"   ⚠️  Atenção: {clubes_no_ranking} clubes no ranking, {len(dim_clubes)} na dimensão")
else:
    print(f"   ⚠️  Coluna 'foto' não encontrada, usando dim_clubes existente")
    try:
        dim_clubes = pd.read_csv(GOLD_DIR / 'dim_clubes.csv')
        print(f"   ✅ dim_clubes carregada: {len(dim_clubes)} clubes")
    except Exception:
        print(f"   ❌ Erro ao carregar dim_clubes")
        dim_clubes = None

# ========================================
# 6. SALVAR ARQUIVOS
# ========================================
print("\n[6/7] 💾 Salvando arquivos...")

timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

# 1. Ranking completo (ordenado por value_score)
df_sorted = df.sort_values('value_score', ascending=False)
output_ranking = GOLD_DIR / 'ranking_completo.parquet'
df_sorted.to_parquet(output_ranking, compression='snappy', index=False)
print(f"   ✅ ranking_completo.parquet ({len(df_sorted)} atletas)")

# Backup com timestamp
backup_ranking = GOLD_DIR / f'ranking_completo_{timestamp}.parquet'
df_sorted.to_parquet(backup_ranking, compression='snappy', index=False)
print(f"   📦 Backup: ranking_completo_{timestamp}.parquet")

# 2. Top 100
output_top100 = GOLD_DIR / 'top_100_value.csv'
df_sorted.head(100).to_csv(output_top100, index=False, encoding='utf-8-sig')
print(f"   ✅ top_100_value.csv")

# 3. Pechinchas (value_score_normalized > 75 e preco < mediana)
preco_mediano = df['preco_num'].median()
pechinchas = df[
    (df['value_score_normalized'] > 75) &
    (df['preco_num'] < preco_mediano)
].sort_values('value_score_normalized', ascending=False)

if len(pechinchas) > 0:
    output_pechinchas = GOLD_DIR / 'pechinchas.csv'
    pechinchas.to_csv(output_pechinchas, index=False, encoding='utf-8-sig')
    print(f"   ✅ pechinchas.csv ({len(pechinchas)} jogadores)")

# 4. dim_clubes
if dim_clubes is not None:
    output_clubes = GOLD_DIR / 'dim_clubes.csv'
    dim_clubes.to_csv(output_clubes, index=False, encoding='utf-8-sig')
    print(f"   ✅ dim_clubes.csv ({len(dim_clubes)} clubes)")

# 5. Rankings por posição
if 'posicao_nome' in df.columns:
    for posicao in df['posicao_nome'].unique():
        if posicao == 'TEC':
            continue

        df_pos = df[df['posicao_nome'] == posicao].sort_values('value_score', ascending=False)
        output_pos = GOLD_DIR / f'ranking_{posicao.lower()}.csv'
        df_pos.to_csv(output_pos, index=False, encoding='utf-8-sig')
        print(f"   ✅ ranking_{posicao.lower()}.csv ({len(df_pos)} atletas)")

print(f"\n   📁 Arquivos salvos em: {GOLD_DIR}")

# ========================================
# 7. RESUMO FINAL
# ========================================
print("\n[7/7] 📊 Resumo da atualização")
print("=" * 80)

if rodada_atual:
    print(f"🏆 Rodada processada: {rodada_atual}")

print(f"👥 Total de atletas: {len(df)}")
print(f"🏟️  Total de clubes: {len(dim_clubes) if dim_clubes is not None else 'N/A'}")
print(f"⚽ Atletas que pontuaram: {len(df[df['pontos_num'] > 0])}")
print(f"💎 Melhor value_score: {df['value_score'].max():.2f}")
print(f"💰 Preço médio: C$ {df['preco_num'].mean():.2f}")
print(f"📊 Pontos médios: {df['pontos_num'].mean():.2f}")

print(f"\n📋 Colunas no ranking_completo.parquet:")
for c in df_sorted.columns:
    print(f"   - {c}")

print("\n" + "=" * 80)
print("✅ ATUALIZAÇÃO CONCLUÍDA COM SUCESSO!")
print("=" * 80)

print("\n🔄 PRÓXIMOS PASSOS:")
print("   1. Abra o Power BI")
print("   2. Vá em Home → Refresh")
print("   3. Todos os visuais serão atualizados automaticamente!")

print("\n💡 DICA:")
print("   Execute este script semanalmente após cada rodada do Brasileirão")
print("   para manter seu dashboard sempre atualizado!")
