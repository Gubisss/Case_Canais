"""
Domain Service: ClassificadorReclamacoes
Implementa lógica complexa de classificação NLP com 3 estratégias de matching.
"""

import re
import unicodedata
from typing import List, Dict, Optional
from dataclasses import dataclass

from src.domain.entities import CategoriaReclamacao


@dataclass
class ClassificacaoResultado:
    """Resultado da classificação de uma reclamação."""
    categorias: List[CategoriaReclamacao]
    tem_erros: bool = False
    mensagem_erro: str = ""


class ClassificadorReclamacoes:
    """
    Domain Service que classifica reclamações automaticamente.
    
    Implementa 3 estratégias de keyword matching:
    1. Match Exato (peso 100): Palavra exata com limites
    2. Palavra Completa (peso 80): Começa com a palavra-chave
    3. Contains (peso 50): Contém em qualquer lugar
    
    Características:
    - Normalização de texto (acentos, pontuação)
    - Scoring com ponderação
    - Normalização para [0, 1]
    - Limiar mínimo de confiança (30%)
    - Suporte a categorias dinâmicas
    """
    
    def __init__(self):
        """Inicializa o classificador com categorias padrão."""
        self._categorias: Dict[str, List[str]] = {
            "imobiliario": [
                "imovel", "propriedade", "aluguel", "locacao", "casa", 
                "apartamento", "terreno", "hipoteca", "empreendimento"
            ],
            "seguros": [
                "seguro", "apólice", "cobertura", "indenizacao", "sinistro",
                "seguradora", "ressarcimento", "beneficiario"
            ],
            "cobranca": [
                "cobranca", "debito", "duplicata", "nota", "boleto",
                "conta", "fatura", "pagamento", "cheque", "repasse"
            ],
            "acesso": [
                "acesso", "bloqueio", "senha", "login", "autenticacao",
                "usuario", "conta bloqueada", "plataforma indisponivel"
            ],
            "aplicativo": [
                "app", "aplicativo", "sistema", "erro", "bug", "crash",
                "lentidao", "indisponivel", "falha", "travado"
            ],
            "fraude": [
                "fraude", "roubo", "defraudacao", "transacao nao reconhecida",
                "clonagem", "cartao clonado", "golpe", "transacao indevida"
            ]
        }
    
    def classificar(self, texto_reclamacao: str) -> ClassificacaoResultado:
        """
        Classifica uma reclamação usando múltiplas estratégias.
        
        Args:
            texto_reclamacao: Texto da reclamação a classificar
            
        Returns:
            ClassificacaoResultado: Categorias identificadas com confiança
        """
        try:
            # Valida entrada
            if not texto_reclamacao or not texto_reclamacao.strip():
                return ClassificacaoResultado(
                    categorias=[],
                    tem_erros=True,
                    mensagem_erro="Texto da reclamação não pode estar vazio"
                )
            
            # Preprocessa texto
            texto_processado = self._preprocessar_texto(texto_reclamacao)
            
            if not texto_processado:
                return ClassificacaoResultado(
                    categorias=[],
                    tem_erros=True,
                    mensagem_erro="Texto processado está vazio"
                )
            
            # Calcula scores para cada categoria
            scores = self._calcular_scores(texto_processado)
            
            # Normaliza scores para [0, 1]
            self._normalizar_scores(scores)
            
            # Filtra por limiar mínimo (30%)
            categorias_resultado = []
            for categoria, score in scores.items():
                if score >= 0.30:
                    categorias_resultado.append(
                        CategoriaReclamacao(
                            nome=categoria,
                            confianca=round(score, 2)
                        )
                    )
            
            # Ordena por confiança decrescente
            categorias_resultado.sort(key=lambda x: x.confianca, reverse=True)
            
            return ClassificacaoResultado(categorias=categorias_resultado)
        
        except Exception as e:
            return ClassificacaoResultado(
                categorias=[],
                tem_erros=True,
                mensagem_erro=f"Erro ao classificar: {str(e)}"
            )
    
    def _preprocessar_texto(self, texto: str) -> str:
        """
        Preprocessa o texto: remove acentos, pontuação, normaliza espaços.
        
        Args:
            texto: Texto bruto
            
        Returns:
            str: Texto processado
        """
        # Converte para minúsculas
        texto = texto.lower()
        
        # Remove acentos usando NFKD
        texto_sem_acento = unicodedata.normalize('NFKD', texto)
        texto_sem_acento = ''.join(
            c for c in texto_sem_acento 
            if unicodedata.category(c) != 'Mn'
        )
        
        # Remove pontuação mantendo espaços
        texto_limpo = re.sub(r'[^\w\s]', ' ', texto_sem_acento)
        
        # Normaliza espaços múltiplos
        texto_limpo = ' '.join(texto_limpo.split())
        
        return texto_limpo
    
    def _calcular_scores(self, texto_processado: str) -> Dict[str, float]:
        """
        Calcula scores para cada categoria usando 3 estratégias.
        
        Args:
            texto_processado: Texto já processado
            
        Returns:
            Dict[str, float]: Scores brutos (não normalizados)
        """
        scores: Dict[str, float] = {}
        palavras_texto = set(texto_processado.split())
        
        for categoria, palavras_chave in self._categorias.items():
            score = 0.0
            
            for palavra_chave in palavras_chave:
                # Estratégia 1: Match Exato (peso 100)
                if palavra_chave in palavras_texto:
                    score += 100
                # Estratégia 2: Palavra Completa - começa com (peso 80)
                elif any(p.startswith(palavra_chave) for p in palavras_texto):
                    score += 80
                # Estratégia 3: Contains - contém em texto contínuo (peso 50)
                elif palavra_chave in texto_processado:
                    score += 50
            
            if score > 0:
                scores[categoria] = score
        
        return scores
    
    def _normalizar_scores(self, scores: Dict[str, float]) -> None:
        """
        Normaliza scores para intervalo [0, 1] modificando dicionário in-place.
        
        Args:
            scores: Dicionário de scores a normalizar
        """
        if not scores:
            return
        
        max_score = max(scores.values())
        
        if max_score > 0:
            for categoria in scores:
                scores[categoria] = scores[categoria] / max_score
    
    def atualizar_categorias(
        self,
        categoria: str,
        palavras_chave: List[str]
    ) -> None:
        """
        Adiciona ou atualiza palavras-chave de uma categoria.
        
        Args:
            categoria: Nome da categoria
            palavras_chave: Lista de palavras-chave
            
        Raises:
            ValueError: Se entrada for inválida
        """
        if not categoria or not categoria.strip():
            raise ValueError("Categoria não pode estar vazia")
        
        if not isinstance(palavras_chave, list) or not palavras_chave:
            raise ValueError("Palavras-chave deve ser uma lista não-vazia")
        
        # Processa palavras-chave
        palavras_limpas = [
            self._preprocessar_texto(p) 
            for p in palavras_chave 
            if p and p.strip()
        ]
        
        if not palavras_limpas:
            raise ValueError("Nenhuma palavra-chave válida fornecida")
        
        # Atualiza ou cria categoria
        categoria_limpa = self._preprocessar_texto(categoria)
        self._categorias[categoria_limpa] = palavras_limpas
    
    def obter_categorias_disponiveis(self) -> List[str]:
        """
        Retorna lista de categorias disponíveis.
        
        Returns:
            List[str]: Nomes das categorias
        """
        return list(self._categorias.keys())
    
    def obter_palavras_chave(self, categoria: str) -> Optional[List[str]]:
        """
        Retorna palavras-chave de uma categoria.
        
        Args:
            categoria: Nome da categoria
            
        Returns:
            Optional[List[str]]: Palavras-chave ou None se não existe
        """
        return self._categorias.get(self._preprocessar_texto(categoria))
