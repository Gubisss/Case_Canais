"""
Domain Layer __init__.py
Exporta principais classes e interfaces do domínio.
"""

from src.domain.enums import Canal, StatusReclamacao
from src.domain.value_objects import DadosCliente
from src.domain.entities import CategoriaReclamacao
from src.domain.services import ClassificadorReclamacoes, ClassificacaoResultado

__all__ = [
    "Canal",
    "StatusReclamacao",
    "DadosCliente",
    "CategoriaReclamacao",
    "ClassificadorReclamacoes",
    "ClassificacaoResultado",
]
