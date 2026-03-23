"""
ATUALIZAÇÃO CARTOLA FC - VERSÃO 3.0 COM HISTÓRICO
===================================================

Combina:
- Correções e melhorias do seu script atual (UTF-8, API correta, sklearn)
- Sistema de histórico incremental (mantém todas as rodadas)

Funcionalidades:
1. Busca rodada atual na API
2. Baixa dados do mercado
3. Mantém histórico completo de todas as rodadas
4. Atualiza ranking_completo.parquet (compatibilidade)
5. Cria dim_rodadas para análises temporais
6. Gera arquivos complementares (top_100, pechinchas, etc.)

Autor: Thales Gazola Manetti
Data: 2026-02-20
Versão: 3.0 (Com Histórico)
"""

import sys
import os

# Garantir UTF-8 no console Windows (suporte a emojis)
if sys.platform == 'win32':
    os.system('chcp 65001 >nul 2>&1')
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

import pandas as pd
import numpy as np
import requests
from pathlib import Path
import warnings
import re
from datetime import datetime
from sklearn.preprocessing import MinMaxScaler

warnings.filterwarnings('ignore')

# ========================================
# CONFIGURAÇÕES
# ========================================
BASE_DIR = Path(r'D:\football analytics project\data')
GOLD_DIR = BASE_DIR / 'gold' / 'scouting'
GOLD_DIR.mkdir(parents=True, exist_ok=True)

# Arquivos
HISTORICO_FILE = GOLD_DIR / 'ranking_historico.parquet'  # NOVO: Histórico completo
RANKING_ATUAL = GOLD_DIR / 'ranking_completo.parquet'   # Compatibilidade

# Posições Cartola FC
CARTOLA_POSITIONS = {
    1: 'GOL',
    2: 'LAT',
    3: 'ZAG',
    4: 'MEI',
    5: 'ATA',
    6: 'TEC'
}

# API Cartola (URL CORRIGIDA)
API_BASE = "https://api.cartolafc.globo.com"

print("=" * 80)
print(" " * 15 + "🔄 ATUALIZAÇÃO CARTOLA FC V3.0 - COM HISTÓRICO")
print("=" * 80)
print(f"📅 Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 80)

# ========================================
# FUNÇÕES AUXILIARES
# ========================================

def carregar_historico():
    """Carrega histórico existente ou retorna DataFrame vazio"""
    if HISTORICO_FILE.exists():
        df = pd.read_parquet(HISTORICO_FILE)
        rodadas = sorted(df['rodada_id'].unique())
        print(f"\n📂 Histórico existente carregado:")
        print(f"   Total: {len(df):,} registros")
        print(f"   Rodadas: {rodadas}")
        return df
    else:
        print(f"\n📂 Nenhum histórico encontrado. Criando novo...")
        return pd.DataFrame()


def salvar_historico(df):
    """Salva histórico completo com backup"""
    # Principal
    df.to_parquet(HISTORICO_FILE, index=False, compression='snappy')
    
    # Backup timestamped
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup = GOLD_DIR / f'ranking_historico_{timestamp}.parquet'
    df.to_parquet(backup, index=False, compression='snappy')
    
    print(f"\n💾 Histórico salvo:")
    print(f"   Principal: {HISTORICO_FILE.name}")
    print(f"   Backup: {backup.name}")


def criar_dim_rodadas(df):
    """Cria dimensão de rodadas"""
    dim = df.groupby('rodada_id').agg({
        'data_atualizacao': 'first',
        'atleta_id': 'count'
    }).reset_index()
    
    dim.columns = ['rodada_id', 'data_atualizacao', 'qtd_jogadores']
    dim = dim.sort_values('rodada_id')
    
    path = GOLD_DIR / 'dim_rodadas.csv'
    dim.to_csv(path, index=False, encoding='utf-8-sig')
    
    print(f"\n📊 dim_rodadas criada: {len(dim)} rodadas")
    return dim


def criar_ranking_atual(df):
    """Extrai rodada mais recente para compatibilidade"""
    rodada_max = df['rodada_id'].max()
    df_atual = df[df['rodada_id'] == rodada_max].copy()
    
    # Salvar como ranking_completo (compatibilidade com dashboard atual)
    df_atual.to_parquet(RANKING_ATUAL, index=False, compression='snappy')
    
    print(f"\n💾 Ranking atual (rodada {rodada_max}):")
    print(f"   {len(df_atual)} jogadores")
    print(f"   Arquivo: {RANKING_ATUAL.name}")
    
    return df_atual


def extrair_codigo_clube(url_foto):
    """Extrai código do clube da URL da foto"""
    if pd.isna(url_foto):
        return None
    match = re.search(r'/silhuetas/([A-Z]+)/', str(url_foto))
    return match.group(1) if match else None


# Mapeamento de códigos para nomes
CODIGO_PARA_NOME = {
    'FLA': 'Flamengo', 'BOT': 'Botafogo', 'FLU': 'Fluminense', 'VAS': 'Vasco',
    'SAO': 'São Paulo', 'PAL': 'Palmeiras', 'COR': 'Corinthians', 'SAN': 'Santos',
    'CAM': 'Atlético-MG', 'CRU': 'Cruzeiro', 'GRE': 'Grêmio', 'INT': 'Internacional',
    'CAP': 'Athletico-PR', 'BAH': 'Bahia', 'FOR': 'Fortaleza', 'CFC': 'Coritiba',
    'VIT': 'Vitória', 'GOI': 'Goiás', 'CEA': 'Ceará', 'SPO': 'Sport',
    'RBB': 'Red Bull Bragantino', 'CUI': 'Cuiabá', 'JUV': 'Juventude', 
    'ACG': 'Atlético-GO', 'AME': 'América-MG', 'PON': 'Ponte Preta', 
    'AVA': 'Avaí', 'CHA': 'Chapecoense', 'MIR': 'Mirassol', 'REM': 'REM'
}

# ========================================
# 1. VERIFICAR RODADA ATUAL
# ========================================
print("\n[1/8] 🔍 Verificando rodada atual...")

try:
    response = requests.get(f"{API_BASE}/mercado/status", timeout=10)
    mercado_status = response.json()

    rodada_atual = mercado_status.get('rodada_atual', 1)
    mercado_aberto = mercado_status.get('status_mercado', 1) == 1

    print(f"   ✅ Rodada atual: {rodada_atual}")
    print(f"   {'✅' if mercado_aberto else '🔒'} Mercado: {'ABERTO' if mercado_aberto else 'FECHADO'}")

except Exception as e:
    print(f"   ⚠️  Erro ao verificar rodada: {e}")
    print(f"   ℹ️  Continuando com atualização...")
    rodada_atual = None
    mercado_aberto = False

if rodada_atual is None:
    print("\n❌ Não foi possível obter rodada da API. Abortando...")
    exit(1)

# ========================================
# 2. CARREGAR HISTÓRICO
# ========================================
print("\n[2/8] 📂 Verificando histórico...")

df_historico = carregar_historico()

# Verificar se rodada já existe
if not df_historico.empty and rodada_atual in df_historico['rodada_id'].values:
    print(f"\n⚠️  Rodada {rodada_atual} já existe no histórico!")
    resposta = input("   Deseja atualizar mesmo assim? (s/n): ").lower()
    
    if resposta != 's':
        print("\n❌ Operação cancelada.")
        print("\n💡 DICA: Use este script apenas quando houver nova rodada")
        exit(0)
    
    # Remover rodada antiga para atualizar
    df_historico = df_historico[df_historico['rodada_id'] != rodada_atual]
    print(f"   ✅ Rodada {rodada_atual} será atualizada")

# ========================================
# 3. BUSCAR DADOS DO MERCADO
# ========================================
print(f"\n[3/8] 📥 Baixando dados da rodada {rodada_atual}...")

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
    exit(1)

# ========================================
# 4. PROCESSAR DADOS
# ========================================
print("\n[4/8] ⚙️  Processando dados...")

df = atletas_api.copy()

# Adicionar posicao_nome
df['posicao_nome'] = df['posicao_id'].map(CARTOLA_POSITIONS)

# Usar media_num como fallback quando pontos_num estiver zerado
# (pontos_num zerado = mercado fechado, media_num sempre disponível)
if df['pontos_num'].sum() == 0 and df['media_num'].sum() != 0:
    df['pontos_num'] = df['media_num']
    print(f"   ℹ️  pontos_num zerado (mercado fechado), usando media_num")

# Colunas essenciais
colunas_manter = [
    'atleta_id', 'apelido', 'apelido_abreviado', 'nome', 'foto', 'slug',
    'clube_id', 'posicao_id', 'posicao_nome', 'rodada_id', 'status_id',
    'pontos_num', 'media_num', 'preco_num', 'variacao_num',
    'jogos_num', 'entrou_em_campo'
]
colunas_disponiveis = [c for c in colunas_manter if c in df.columns]
df = df[colunas_disponiveis]

# Adicionar metadados
df['rodada_id'] = rodada_atual
df['data_atualizacao'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

print(f"   ✅ {len(df)} atletas, {len(df.columns)} colunas")

# ========================================
# 5. CALCULAR MÉTRICAS
# ========================================
print("\n[5/8] 📊 Calculando métricas...")

# Filtrar apenas jogadores com preço
df = df[df['preco_num'] > 0].copy()
print(f"   ✅ Filtrados: {len(df)} jogadores com preço")

# Value Score
df['value_score'] = np.where(
    df['preco_num'] > 0,
    df['pontos_num'] / df['preco_num'],
    0
)

# Value Score Normalizado 0-100 (usando sklearn como seu script)
scaler = MinMaxScaler(feature_range=(0, 100))
df['value_score_normalized'] = scaler.fit_transform(df[['value_score']])

# Categoria
df['value_categoria'] = pd.cut(
    df['value_score_normalized'],
    bins=[0, 25, 50, 75, 100],
    labels=['Baixo', 'Médio', 'Alto', 'Excelente'],
    include_lowest=True
).astype(str)

# Quadrantes (usando medianas)
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

print(f"   ✅ Métricas calculadas")
print(f"   ℹ️  Melhor value_score: {df['value_score'].max():.2f}")
print(f"   ℹ️  Value_score médio: {df['value_score'].mean():.2f}")

# ========================================
# 6. ATUALIZAR HISTÓRICO
# ========================================
print(f"\n[6/8] 📚 Atualizando histórico...")

if df_historico.empty:
    df_historico = df
    print(f"   ✅ Histórico inicial criado")
else:
    df_historico = pd.concat([df_historico, df], ignore_index=True)
    print(f"   ✅ Nova rodada adicionada")

print(f"   Total: {len(df_historico):,} registros")
print(f"   Rodadas: {sorted(df_historico['rodada_id'].unique())}")

# Salvar histórico
salvar_historico(df_historico)

# Criar dimensões
criar_dim_rodadas(df_historico)
df_atual = criar_ranking_atual(df_historico)

# ========================================
# 7. CRIAR ARQUIVOS COMPLEMENTARES
# ========================================
print(f"\n[7/8] 📄 Criando arquivos complementares...")

timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

# 1. dim_clubes
if 'foto' in df_atual.columns:
    codigos = df_atual[['clube_id', 'foto']].drop_duplicates(subset='clube_id')
    codigos['codigo_clube'] = codigos['foto'].apply(extrair_codigo_clube)
    codigos = codigos[codigos['codigo_clube'].notna()]
    codigos['Clube'] = codigos['codigo_clube'].map(CODIGO_PARA_NOME)
    codigos['Clube'] = codigos['Clube'].fillna(codigos['codigo_clube'])
    
    dim_clubes = codigos[['clube_id', 'Clube']].rename(
        columns={'clube_id': 'ID_Clube'}
    ).sort_values('ID_Clube').reset_index(drop=True)
    
    dim_clubes.to_csv(GOLD_DIR / 'dim_clubes.csv', index=False, encoding='utf-8-sig')
    print(f"   ✅ dim_clubes.csv - {len(dim_clubes)} clubes")

# 2. Top 100
df_sorted = df_atual.sort_values('value_score', ascending=False)
df_sorted.head(100).to_csv(GOLD_DIR / 'top_100_value.csv', index=False, encoding='utf-8-sig')
print(f"   ✅ top_100_value.csv")

# 3. Pechinchas
preco_mediano = df_atual['preco_num'].median()
pechinchas = df_atual[
    (df_atual['value_score_normalized'] > 75) &
    (df_atual['preco_num'] < preco_mediano)
].sort_values('value_score_normalized', ascending=False)

if len(pechinchas) > 0:
    pechinchas.to_csv(GOLD_DIR / 'pechinchas.csv', index=False, encoding='utf-8-sig')
    print(f"   ✅ pechinchas.csv - {len(pechinchas)} jogadores")

# 4. Rankings por posição
for posicao in df_atual['posicao_nome'].unique():
    if posicao == 'TEC':
        continue
    
    df_pos = df_atual[df_atual['posicao_nome'] == posicao].sort_values(
        'value_score', ascending=False
    )
    df_pos.to_csv(GOLD_DIR / f'ranking_{posicao.lower()}.csv', index=False, encoding='utf-8-sig')
    print(f"   ✅ ranking_{posicao.lower()}.csv - {len(df_pos)} jogadores")

print(f"\n   📁 Todos os arquivos em: {GOLD_DIR}")

# ========================================
# 8. RESUMO FINAL
# ========================================
print("\n[8/8] 📊 Resumo da atualização")
print("=" * 80)

print(f"🏆 Rodada processada: {rodada_atual}")
print(f"📚 Total no histórico: {len(df_historico):,} registros")
print(f"📊 Rodadas armazenadas: {sorted(df_historico['rodada_id'].unique())}")
print(f"👥 Atletas na rodada {rodada_atual}: {len(df_atual)}")
print(f"⚽ Jogaram: {len(df_atual[df_atual['pontos_num'] > 0])}")
print(f"💎 Melhor value_score: {df_atual['value_score'].max():.2f}")
print(f"💰 Preço médio: C$ {df_atual['preco_num'].mean():.2f}")
print(f"📊 Pontos médios: {df_atual['pontos_num'].mean():.2f}")

# Quadrantes
print(f"\n🎯 Distribuição por Quadrante (Rodada {rodada_atual}):")
for quad, count in df_atual['Quadrante_Categoria'].value_counts().items():
    pct = count / len(df_atual) * 100
    print(f"   {quad}: {count} ({pct:.1f}%)")

# Top 5
print(f"\n🏆 TOP 5 VALUE SCORE:")
top5 = df_atual.nlargest(5, 'value_score')[
    ['apelido', 'posicao_nome', 'pontos_num', 'preco_num', 'value_score']
]
for _, row in top5.iterrows():
    vs = row['value_score'] * 100
    print(f"   {row['apelido']} ({row['posicao_nome']}) - {vs:.1f} pts/C$100")

print("\n" + "=" * 80)
print("✅ ATUALIZAÇÃO CONCLUÍDA COM SUCESSO!")
print("=" * 80)

print("\n🔄 PRÓXIMOS PASSOS:")
print("   1. Abra o Power BI Desktop")
print("   2. Home → Refresh")
print("   3. Analise as novas tendências! 📊")

print("\n💡 NOVIDADES V3.0:")
print("   ✅ Histórico completo de todas as rodadas")
print("   ✅ Análises temporais disponíveis")
print("   ✅ dim_rodadas para comparações")
print("   ✅ Tendências de valorização/desvalorização")

print(f"\n📁 ARQUIVOS GERADOS:")
print(f"   ✅ ranking_historico.parquet (histórico completo)")
print(f"   ✅ ranking_completo.parquet (rodada atual)")
print(f"   ✅ dim_rodadas.csv (dimensão temporal)")
print(f"   ✅ dim_clubes.csv")
print(f"   ✅ top_100_value.csv")
print(f"   ✅ pechinchas.csv")
print(f"   ✅ ranking_*.csv (por posição)")
