"""
INICIAR HISTÓRICO - VERSÃO SIMPLIFICADA
Cria histórico inicial usando o arquivo ranking_completo.parquet que você já tem

Execute este script UMA VEZ para criar o histórico inicial
"""

import pandas as pd
from pathlib import Path
from datetime import datetime

# ====================================
# CONFIGURAÇÕES
# ====================================
BASE_DIR = Path(r'D:\football analytics project\data')
GOLD_DIR = BASE_DIR / 'gold' / 'scouting'

# Arquivos
RANKING_ATUAL = GOLD_DIR / 'ranking_completo.parquet'
HISTORICO_FILE = GOLD_DIR / 'ranking_historico.parquet'

print("=" * 70)
print("📚 INICIAR HISTÓRICO - VERSÃO SIMPLIFICADA")
print("=" * 70)

# ====================================
# VALIDAÇÕES
# ====================================

# Verificar se pasta existe
if not GOLD_DIR.exists():
    print(f"\n❌ ERRO: Pasta não existe!")
    print(f"   {GOLD_DIR}")
    print(f"\n💡 SOLUÇÃO:")
    print(f"   Verifique o caminho no script (linha BASE_DIR)")
    exit(1)

# Verificar se arquivo existe
if not RANKING_ATUAL.exists():
    print(f"\n❌ ERRO: Arquivo não encontrado!")
    print(f"   {RANKING_ATUAL}")
    print(f"\n💡 SOLUÇÃO:")
    print(f"   1. Execute o notebook: 05_scouting_system.ipynb")
    print(f"   2. OU execute: atualizar_cartola.py")
    print(f"   3. Para gerar o arquivo ranking_completo.parquet")
    exit(1)

# Verificar se já existe histórico
if HISTORICO_FILE.exists():
    print(f"\n⚠️  AVISO: Já existe um histórico!")
    print(f"   {HISTORICO_FILE}")
    
    # Mostrar info do histórico existente
    df_existente = pd.read_parquet(HISTORICO_FILE)
    rodadas_existentes = sorted(df_existente['rodada_id'].unique())
    
    print(f"\n📊 Histórico atual:")
    print(f"   Total de registros: {len(df_existente):,}")
    print(f"   Rodadas: {rodadas_existentes}")
    
    resposta = input(f"\n   Deseja SUBSTITUIR o histórico? (s/n): ").lower()
    
    if resposta != 's':
        print("\n❌ Operação cancelada.")
        print("\n💡 Use atualizar_cartola_v2.py para adicionar novas rodadas")
        exit(0)

# ====================================
# CARREGAR DADOS
# ====================================

print(f"\n📂 Carregando dados...")
print(f"   Arquivo: {RANKING_ATUAL.name}")

df = pd.read_parquet(RANKING_ATUAL)
print(f"   ✅ {len(df):,} jogadores carregados")

# ====================================
# DESCOBRIR RODADA
# ====================================

# Verificar se já tem rodada_id no arquivo
if 'rodada_id' in df.columns and df['rodada_id'].notna().any():
    rodada_atual = int(df['rodada_id'].mode()[0])  # Pegar a mais comum
    print(f"\n✅ Rodada detectada automaticamente: {rodada_atual}")
else:
    # Perguntar ao usuário
    print(f"\n⚠️  Campo 'rodada_id' não encontrado no arquivo")
    print(f"\n🔍 QUAL É A RODADA DESTES DADOS?")
    print(f"   (Consulte o site do Cartola FC ou a API)")
    
    while True:
        try:
            rodada_input = input(f"\n   Digite o número da rodada (ex: 2): ")
            rodada_atual = int(rodada_input)
            
            if rodada_atual < 1 or rodada_atual > 38:
                print(f"   ❌ Rodada inválida! Deve ser entre 1 e 38")
                continue
            
            break
        except ValueError:
            print(f"   ❌ Digite apenas números!")
    
    # Adicionar rodada ao DataFrame
    df['rodada_id'] = rodada_atual
    print(f"\n   ✅ Rodada {rodada_atual} definida")

# ====================================
# ADICIONAR DATA DE ATUALIZAÇÃO
# ====================================

if 'data_atualizacao' not in df.columns or df['data_atualizacao'].isna().all():
    data_atual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    df['data_atualizacao'] = data_atual
    print(f"   ✅ Data de atualização: {data_atual}")

# ====================================
# VALIDAR CAMPOS ESSENCIAIS
# ====================================

print(f"\n🔍 Validando campos essenciais...")

campos_essenciais = [
    'atleta_id', 'apelido', 'posicao_nome', 'clube_id',
    'pontos_num', 'preco_num', 'value_score', 'Quadrante_Categoria',
    'rodada_id', 'data_atualizacao'
]

campos_faltando = [campo for campo in campos_essenciais if campo not in df.columns]

if campos_faltando:
    print(f"\n⚠️  AVISO: Campos faltando: {campos_faltando}")
    
    # Tentar corrigir campos comuns
    if 'Quadrante_Categoria' not in df.columns and 'value_categoria' in df.columns:
        print(f"   ℹ️  Usando 'value_categoria' como 'Quadrante_Categoria'")
        df['Quadrante_Categoria'] = df['value_categoria']
else:
    print(f"   ✅ Todos os campos essenciais presentes")

# ====================================
# SALVAR HISTÓRICO
# ====================================

print(f"\n💾 Salvando histórico...")

# Salvar Parquet principal
df.to_parquet(HISTORICO_FILE, index=False, compression='snappy')
print(f"   ✅ Histórico principal: {HISTORICO_FILE.name}")

# Backup com timestamp
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
backup_file = GOLD_DIR / f'ranking_historico_{timestamp}.parquet'
df.to_parquet(backup_file, index=False, compression='snappy')
print(f"   ✅ Backup: {backup_file.name}")

# ====================================
# CRIAR dim_rodadas
# ====================================

print(f"\n📊 Criando dim_rodadas...")

dim_rodadas = pd.DataFrame({
    'rodada_id': [rodada_atual],
    'data_atualizacao': [df['data_atualizacao'].iloc[0]],
    'qtd_jogadores': [len(df)]
})

dim_path = GOLD_DIR / 'dim_rodadas.csv'
dim_rodadas.to_csv(dim_path, index=False, encoding='utf-8-sig')
print(f"   ✅ dim_rodadas.csv criada")

# ====================================
# RELATÓRIO FINAL
# ====================================

print("\n" + "=" * 70)
print("✅ HISTÓRICO INICIAL CRIADO COM SUCESSO!")
print("=" * 70)

print(f"\n📊 RESUMO:")
print(f"   Total de registros: {len(df):,}")
print(f"   Rodada inicial: {rodada_atual}")
print(f"   Data: {df['data_atualizacao'].iloc[0]}")
print(f"   Jogadores: {len(df)}")
print(f"   Jogaram: {(df['pontos_num'] > 0).sum()}")

print(f"\n📁 ARQUIVOS CRIADOS:")
print(f"   ✅ {HISTORICO_FILE.name}")
print(f"   ✅ {backup_file.name}")
print(f"   ✅ {dim_path.name}")

print(f"\n📊 ESTATÍSTICAS:")
quadrantes = df['Quadrante_Categoria'].value_counts() if 'Quadrante_Categoria' in df.columns else None

if quadrantes is not None:
    print(f"\n   Distribuição por Quadrante:")
    for quad, count in quadrantes.items():
        pct = count / len(df) * 100
        print(f"   - {quad}: {count} ({pct:.1f}%)")

print(f"\n🎯 PRÓXIMOS PASSOS:")
print(f"   1. ✅ Histórico inicial criado!")
print(f"   2. Configure o Power BI:")
print(f"      - Adicione tabela: fato_ranking_historico")
print(f"      - Adicione tabela: dim_rodadas")
print(f"      - Crie relacionamento entre elas")
print(f"   3. A partir de agora, use:")
print(f"      python atualizar_cartola_v2.py")
print(f"      (Após cada rodada do Brasileirão)")

print("\n" + "=" * 70)
