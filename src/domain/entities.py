"""
Entidades do Domínio de Reclamações Bancárias.
Simplificadas para microserviço de classificação.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List
from uuid import UUID, uuid4


@dataclass
class CategoriaReclamacao:
    """
    Representa uma categoria identificada na reclamação.
    Resultado da classificação automática com confiança.
    """
    nome: str
    confianca: float = 0.0
    
    def validar(self) -> bool:
        """Valida a categoria."""
        return (
            bool(self.nome.strip()) and
            0.0 <= self.confianca <= 1.0
        )
