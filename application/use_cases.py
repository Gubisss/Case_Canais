"""
Application Layer: Handlers
Handler simples para classificação de texto.
"""

from domain.services import ClassificadorReclamacoes
from application.dtos import ClassificacaoRequest, ClassificacaoResponse, CategoriaResultado


class ClassificacaoHandler:
    """
    Handler de classificação automática de reclamações.
    
    Responsabilidade única: receber texto e retornar categorias classificadas.
    """
    
    def __init__(self, classificador: ClassificadorReclamacoes):
        """
        Inicializa handler.
        
        Args:
            classificador: Serviço de classificação
        """
        self.classificador = classificador
    
    def classificar(self, request: ClassificacaoRequest) -> ClassificacaoResponse:
        """
        Classifica texto de reclamação.
        
        Args:
            request: Requisição com texto a classificar
            
        Returns:
            ClassificacaoResponse: Resposta com categorias identificadas
        """
        try:
            # Valida requisição
            valido, erro = request.validar()
            if not valido:
                return ClassificacaoResponse(
                    texto_original=request.texto,
                    categorias=[],
                    tem_erros=True,
                    mensagem_erro=erro
                )
            
            # Classifica
            resultado = self.classificador.classificar(request.texto)
            
            # Monta resposta
            categorias = []
            if resultado and not resultado.tem_erros:
                for cat in resultado.categorias:
                    categorias.append(
                        CategoriaResultado(
                            nome=cat.nome,
                            confianca=cat.confianca
                        )
                    )
            
            return ClassificacaoResponse(
                texto_original=request.texto,
                categorias=categorias,
                tem_erros=False,
                mensagem_erro=""
            )
        
        except Exception as e:
            return ClassificacaoResponse(
                texto_original=request.texto,
                categorias=[],
                tem_erros=True,
                mensagem_erro=f"Erro na classificação: {str(e)}"
            )


