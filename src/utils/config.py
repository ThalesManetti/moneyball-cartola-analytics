"""
============================================================
FOOTBALL ANALYTICS PROJECT - CONFIGURAÇÕES GLOBAIS
============================================================
Autor: Thales Gazola Manetti
Data: 03/02/2026
Descrição: Configurações centralizadas - Cartola FC + StatsBomb
Projeto Híbrido: Brasil + Internacional
============================================================
"""

from pathlib import Path

# ============================================
# FONTES DE DADOS
# ============================================

# Cartola FC (Brasil)
CARTOLA_BASE_URL = 'https://api.cartola.globo.com'
CARTOLA_SEASONS = list(range(2020, 2025))  # 2020-2024
CARTOLA_MAX_RODADA = 38  # Rodadas por temporada

# StatsBomb (Internacional) - Usar IDs corretos
# Ver documentação: https://github.com/statsbomb/StatsBombR
STATSBOMB_COMPS = ['La Liga', 'FIFA World Cup', 'UEFA Euro']

# ============================================
# PATHS
# ============================================

# Base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Data Lake (Medallion Architecture)
DATA_DIR = BASE_DIR / 'data'
BRONZE_PATH = DATA_DIR / 'bronze'
SILVER_PATH = DATA_DIR / 'silver'
GOLD_PATH = DATA_DIR / 'gold'

# Bronze - Subdivisões
BRONZE_CARTOLA = BRONZE_PATH / 'cartola'
BRONZE_STATSBOMB = BRONZE_PATH / 'statsbomb'

# Silver - Subdivisões
SILVER_CARTOLA = SILVER_PATH / 'cartola'
SILVER_STATSBOMB = SILVER_PATH / 'statsbomb'

# Gold - Subdivisões
GOLD_FEATURES = GOLD_PATH / 'features'
GOLD_SCOUTING = GOLD_PATH / 'scouting'

# Database
DATABASE_DIR = BASE_DIR / 'database'
DB_CARTOLA = DATABASE_DIR / 'dw_cartola.db'
DB_STATSBOMB = DATABASE_DIR / 'dw_statsbomb.db'

# Reports
REPORTS_DIR = BASE_DIR / 'reports'
PDF_PATH = REPORTS_DIR / 'pdf'
VIZ_PATH = REPORTS_DIR / 'visualizations'

# Logs
LOGS_DIR = BASE_DIR / 'logs'

# Models
MODELS_DIR = BASE_DIR / 'models'

# ============================================
# API & SCRAPING
# ============================================

# Cartola FC API
CARTOLA_RATE_LIMIT = 1  # Segundos entre requests
CARTOLA_TIMEOUT = 10     # Timeout em segundos
CARTOLA_MAX_RETRIES = 3  # Tentativas em caso de erro

# StatsBomb (sem rate limit - API oficial)
STATSBOMB_TIMEOUT = 30

# Cache geral
CACHE_ENABLED = True
CACHE_EXPIRE_DAYS = 7
CACHE_DIR = BASE_DIR / '.cache'

# User Agent
USER_AGENT = 'Football-Analytics-Project/2.0 (Educational Purpose)'

# ============================================
# DATA QUALITY
# ============================================

# Thresholds para qualidade de dados
MAX_MISSING_PCT = 0.3      # Máximo 30% missing por feature
MIN_GAMES_PLAYER = 5       # Mínimo de jogos para incluir jogador
MIN_MINUTES_PLAYER = 450   # Mínimo de minutos (5 jogos de 90min)

# Outliers (IQR method)
OUTLIER_MULTIPLIER = 3.0   # Multiplicador IQR para detecção

# ============================================
# FEATURE ENGINEERING
# ============================================

# Posições Cartola FC (IDs da API)
CARTOLA_POSITIONS = {
    1: 'GOL',   # Goleiro
    2: 'LAT',   # Lateral
    3: 'ZAG',   # Zagueiro
    4: 'MEI',   # Meia
    5: 'ATA',   # Atacante
    6: 'TEC'    # Técnico
}

# Posições StatsBomb (agrupadas)
STATSBOMB_POSITIONS = {
    'FW': ['FW', 'CF', 'ST', 'LW', 'RW'],           # Atacantes
    'MF': ['MF', 'CM', 'AM', 'DM', 'LM', 'RM'],     # Meio-campistas
    'DF': ['DF', 'CB', 'LB', 'RB', 'WB', 'FB'],     # Defensores
    'GK': ['GK']                                     # Goleiros
}

# Mapeamento Cartola → StatsBomb
POSITION_MAPPING = {
    'GOL': 'GK',
    'LAT': 'DF',
    'ZAG': 'DF',
    'MEI': 'MF',
    'ATA': 'FW'
}

# Pesos para Performance Score - CARTOLA FC
CARTOLA_WEIGHTS = {
    'GOL': {'defesas': 0.40, 'gols_sofridos': -0.30, 'saldo': 0.30},
    'LAT': {'assistencias': 0.25, 'desarmes': 0.25, 'finalizacoes': 0.25, 'saldo': 0.25},
    'ZAG': {'desarmes': 0.30, 'interceptacoes': 0.25, 'jogos_sem_sofrer': 0.25, 'gols_sofridos': -0.20},
    'MEI': {'assistencias': 0.30, 'passes_certos': 0.25, 'finalizacoes': 0.25, 'gols': 0.20},
    'ATA': {'gols': 0.40, 'assistencias': 0.30, 'finalizacoes': 0.20, 'passes_certos': 0.10}
}

# Janela para rolling metrics
ROLLING_WINDOW = 5  # Últimos 5 jogos

# ============================================
# MACHINE LEARNING
# ============================================

# Train/Test split
TEST_SIZE = 0.2
RANDOM_STATE = 42

# LightGBM - Previsão Pontos Cartola
LGBM_CARTOLA_PARAMS = {
    'objective': 'regression',
    'metric': 'rmse',
    'boosting_type': 'gbdt',
    'num_leaves': 31,
    'learning_rate': 0.05,
    'feature_fraction': 0.9,
    'random_state': RANDOM_STATE,
    'verbosity': -1
}

# LightGBM - Previsão Resultados StatsBomb
LGBM_MATCH_PARAMS = {
    'objective': 'multiclass',
    'num_class': 3,
    'metric': 'multi_logloss',
    'boosting_type': 'gbdt',
    'num_leaves': 31,
    'learning_rate': 0.05,
    'random_state': RANDOM_STATE,
    'verbosity': -1
}

# ============================================
# VISUALIZATION
# ============================================

SOURCE_COLORS = {
    'cartola': '#00A859',
    'statsbomb': '#EE3124',
    'brasil': '#009C3B',
    'europa': '#003DA5'
}

FIGSIZE_DEFAULT = (12, 6)
DPI_EXPORT = 300

# ============================================
# SCOUTING
# ============================================

VALUE_THRESHOLDS = {'excellent': 1.5, 'good': 1.2, 'average': 1.0}
TOP_N_SCOUTING = 50

# ============================================
# UTILITIES
# ============================================

def create_directories():
    """Cria todos os diretórios necessários"""
    dirs = [
        BRONZE_CARTOLA, BRONZE_STATSBOMB,
        SILVER_CARTOLA, SILVER_STATSBOMB,
        GOLD_FEATURES, GOLD_SCOUTING,
        DATABASE_DIR, PDF_PATH, VIZ_PATH,
        LOGS_DIR, MODELS_DIR, CACHE_DIR
    ]
    
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)
    
    print("Diretorios criados com sucesso!")


if __name__ == "__main__":
    print("="*60)
    print(" "*15 + "CONFIGURAÇÕES CARREGADAS")
    print("="*60)
    print(f"\n🇧🇷 Cartola: {CARTOLA_SEASONS}")
    print(f"🌍 StatsBomb: {STATSBOMB_COMPS}")
    print(f"📁 Base: {BASE_DIR}")
    print("="*60)