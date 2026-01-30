"""
Enumerações para o domínio de reclamações bancárias.
Define os estados e canais possíveis no sistema.
"""

from enum import Enum


class Canal(Enum):
    """Canais através dos quais a reclamação pode chegar ao sistema."""
    
    WEBSITE = "website"
    PRESENCIAL = "presencial"
    TELEFONE = "telefone"
    EMAIL = "email"


class StatusReclamacao(Enum):
    """Estados possíveis de uma reclamação no ciclo de vida."""
    
    RECEBIDA = "recebida"
    CLASSIFICADA = "classificada"
    EM_ANALISE = "em_analise"
    RESOLVIDA = "resolvida"
    VENCIDA = "vencida"
    CANCELADA = "cancelada"
