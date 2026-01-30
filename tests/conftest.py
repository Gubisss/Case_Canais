"""
Arquivo de configuração pytest
Define fixtures compartilhadas e configurações de testes.
"""

import pytest
import logging
import sys

# Configura logging para testes
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


@pytest.fixture(scope="session", autouse=True)
def configurar_ambiente():
    """Configura ambiente para testes."""
    # Pode adicionar configurações de banco de dados, etc.
    yield
    # Limpeza após testes


@pytest.fixture
def captura_logs(caplog):
    """Fixture para capturar logs durante testes."""
    with caplog.at_level(logging.INFO):
        yield caplog
