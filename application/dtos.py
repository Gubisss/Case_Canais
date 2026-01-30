"""
Application Layer: DTOs (Data Transfer Objects)
DTOs simples para entrada e saída do microserviço de classificação.
"""

from dataclasses import dataclass
from typing import List


@dataclass
class CategoriaResultado:
    """Resultado de uma categoria identificada."""
    nome: str
    confianca: float


@dataclass
class ClassificacaoRequest:
    """Requisição de classificação de texto."""
    texto: str
    
    def validar(self) -> tuple[bool, str]:
        """
        Valida a requisição.
        
        Returns:
            tuple: (é_válida, mensagem_erro)
        """
        if not self.texto or not self.texto.strip():
            return False, "Texto não pode estar vazio"
        
        return True, ""


@dataclass
class ClassificacaoResponse:
    """Resposta da classificação."""
    texto_original: str
    categorias: List[CategoriaResultado]
    tem_erros: bool = False
    mensagem_erro: str = ""
