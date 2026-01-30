"""
Domain Layer __init__.py
Exporta principais classes e interfaces do domínio.
"""

from domain.enums import Canal, StatusReclamacao
from domain.value_objects import DadosCliente
from domain.entities import CategoriaReclamacao
from domain.services import ClassificadorReclamacoes, ClassificacaoResultado

__all__ = [
    "Canal",
    "StatusReclamacao",
    "DadosCliente",
    "CategoriaReclamacao",
    "ClassificadorReclamacoes",
    "ClassificacaoResultado",
]

