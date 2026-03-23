"""
============================================================
FOOTBALL ANALYTICS PROJECT - SISTEMA DE LOGGING
============================================================
Autor: Thales Gazola Manetti
Data: 03/02/2026
Descrição: Sistema de logging estruturado para o projeto
============================================================
"""

import logging
import sys
from pathlib import Path
from typing import Optional
from datetime import datetime


def setup_logger(
    name: str,
    log_file: Optional[str] = None,
    level: int = logging.INFO,
    console: bool = True,
    file_mode: str = 'a'
) -> logging.Logger:
    """
    Configura um logger para o projeto
    
    Args:
        name: Nome do logger (ex: 'extraction', 'modeling')
        log_file: Caminho para arquivo de log (opcional)
        level: Nível de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        console: Se True, também loga no console
        file_mode: Modo de abertura do arquivo ('a' = append, 'w' = write)
    
    Returns:
        logging.Logger configurado
    
    Example:
        >>> logger = setup_logger('extraction', 'logs/extraction.log')
        >>> logger.info("Iniciando extração de dados")
    """
    
    # Criar logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Evitar duplicação de handlers
    if logger.handlers:
        return logger
    
    # Formato detalhado
    formatter = logging.Formatter(
        fmt='%(asctime)s | %(name)s | %(levelname)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    if console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        console_handler.setLevel(level)
        logger.addHandler(console_handler)
    
    # File handler
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file, mode=file_mode)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(level)
        logger.addHandler(file_handler)
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Retorna um logger existente ou cria um novo
    
    Args:
        name: Nome do logger
    
    Returns:
        logging.Logger
    """
    return logging.getLogger(name)


class LoggerContext:
    """
    Context manager para logging temporário
    
    Example:
        >>> with LoggerContext('temp_task', 'logs/temp.log') as logger:
        ...     logger.info("Executando tarefa temporária")
    """
    
    def __init__(self, name: str, log_file: Optional[str] = None):
        self.name = name
        self.log_file = log_file
        self.logger = None
    
    def __enter__(self):
        self.logger = setup_logger(self.name, self.log_file)
        return self.logger
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        # Limpar handlers
        if self.logger:
            for handler in self.logger.handlers[:]:
                handler.close()
                self.logger.removeHandler(handler)


def log_execution_time(func):
    """
    Decorator para logar tempo de execução de funções
    
    Example:
        >>> @log_execution_time
        ... def processar_dados():
        ...     # código aqui
        ...     pass
    """
    import functools
    import time
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger = get_logger(func.__module__)
        
        logger.info(f"Iniciando: {func.__name__}")
        start_time = time.time()
        
        try:
            result = func(*args, **kwargs)
            elapsed = time.time() - start_time
            logger.info(f"Concluído: {func.__name__} em {elapsed:.2f}s")
            return result
        
        except Exception as e:
            elapsed = time.time() - start_time
            logger.error(f"Erro em {func.__name__} após {elapsed:.2f}s: {e}")
            raise
    
    return wrapper


def log_dataframe_info(df, name: str = "DataFrame", logger: Optional[logging.Logger] = None):
    """
    Loga informações básicas de um DataFrame pandas
    
    Args:
        df: pandas DataFrame
        name: Nome descritivo do DataFrame
        logger: Logger a usar (ou cria um novo)
    """
    if logger is None:
        logger = get_logger(__name__)
    
    logger.info(f"📊 {name}:")
    logger.info(f"  - Shape: {df.shape[0]:,} linhas × {df.shape[1]} colunas")
    logger.info(f"  - Memory: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    logger.info(f"  - Columns: {list(df.columns[:10])}{'...' if len(df.columns) > 10 else ''}")


def create_session_log(base_dir: str = 'logs') -> Path:
    """
    Cria um arquivo de log único para a sessão atual
    
    Args:
        base_dir: Diretório base para logs
    
    Returns:
        Path para o arquivo de log da sessão
    """
    session_time = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_dir = Path(base_dir) / 'sessions'
    log_dir.mkdir(parents=True, exist_ok=True)
    
    log_file = log_dir / f'session_{session_time}.log'
    return log_file


# ============================================
# LOGGERS PRÉ-CONFIGURADOS DO PROJETO
# ============================================

# Logger principal do projeto
project_logger = setup_logger(
    'football_analytics',
    'logs/project.log',
    level=logging.INFO
)

# Logger para extração de dados
extraction_logger = setup_logger(
    'extraction',
    'logs/extraction.log',
    level=logging.INFO
)

# Logger para transformação/limpeza
transformation_logger = setup_logger(
    'transformation',
    'logs/transformation.log',
    level=logging.INFO
)

# Logger para modelagem ML
modeling_logger = setup_logger(
    'modeling',
    'logs/modeling.log',
    level=logging.INFO
)

# Logger para análises
analytics_logger = setup_logger(
    'analytics',
    'logs/analytics.log',
    level=logging.INFO
)


# ============================================
# FUNÇÕES UTILITÁRIAS
# ============================================

def log_separator(logger: logging.Logger, char: str = '=', length: int = 60):
    """Loga uma linha separadora"""
    logger.info(char * length)


def log_section(logger: logging.Logger, title: str, level: int = logging.INFO):
    """
    Loga uma seção formatada
    
    Example:
        >>> log_section(logger, "ETAPA 1: EXTRAÇÃO DE DADOS")
    """
    log_separator(logger)
    logger.log(level, f"  {title}")
    log_separator(logger)


def log_progress(logger: logging.Logger, current: int, total: int, prefix: str = "Progresso"):
    """
    Loga progresso de uma operação
    
    Example:
        >>> log_progress(logger, 50, 100, "Processando")
        >>> INFO | Processando: 50/100 (50.0%)
    """
    percentage = (current / total * 100) if total > 0 else 0
    logger.info(f"{prefix}: {current}/{total} ({percentage:.1f}%)")


def log_dict(logger: logging.Logger, data: dict, title: str = "Dados"):
    """
    Loga um dicionário formatado
    
    Example:
        >>> stats = {'partidas': 100, 'jogadores': 500}
        >>> log_dict(logger, stats, "Estatísticas")
    """
    logger.info(f"{title}:")
    for key, value in data.items():
        logger.info(f"  {key}: {value}")


def log_error_with_context(logger: logging.Logger, error: Exception, context: str = ""):
    """
    Loga um erro com contexto adicional
    
    Args:
        logger: Logger a usar
        error: Exception capturada
        context: Informação contextual adicional
    """
    logger.error(f"❌ Erro{f' em {context}' if context else ''}: {type(error).__name__}")
    logger.error(f"   Mensagem: {str(error)}")
    
    # Incluir traceback em DEBUG
    import traceback
    logger.debug(f"   Traceback:\n{traceback.format_exc()}")


# ============================================
# TESTES E VALIDAÇÃO
# ============================================

if __name__ == "__main__":
    # Demonstração do sistema de logging
    
    print("="*60)
    print(" "*15 + "DEMONSTRAÇÃO DO SISTEMA DE LOGGING")
    print("="*60)
    
    # Criar logger de teste
    test_logger = setup_logger('test', 'logs/test.log', level=logging.DEBUG)
    
    # Testar diferentes níveis
    test_logger.debug("🔍 Mensagem de DEBUG (detalhes técnicos)")
    test_logger.info("ℹ️  Mensagem de INFO (operações normais)")
    test_logger.warning("⚠️  Mensagem de WARNING (atenção)")
    test_logger.error("❌ Mensagem de ERROR (erro recuperável)")
    test_logger.critical("🚨 Mensagem de CRITICAL (erro grave)")
    
    # Testar funções utilitárias
    log_section(test_logger, "TESTANDO FUNÇÕES UTILITÁRIAS")
    
    log_progress(test_logger, 50, 100, "Processamento")
    
    test_dict = {
        'total_jogadores': 500,
        'total_partidas': 100,
        'media_gols': 2.5
    }
    log_dict(test_logger, test_dict, "Estatísticas")
    
    # Testar decorator
    @log_execution_time
    def funcao_teste():
        import time
        time.sleep(0.5)
        return "Concluído"
    
    resultado = funcao_teste()
    
    # Testar context manager
    with LoggerContext('temp', 'logs/temp.log') as logger:
        logger.info("Operação temporária")
    
    print("\n✅ Demonstração concluída!")
    print(f"📁 Logs salvos em: logs/")
    print("="*60)