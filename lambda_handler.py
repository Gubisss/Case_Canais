"""
Lambda Handler: Classificação Automática de Reclamações
Entry point para AWS Lambda ou outras plataformas serverless.
Responsável por: entrada -> classificar -> saída
"""

import json
from domain.services import ClassificadorReclamacoes
from application.use_cases import ClassificacaoHandler
from application.dtos import ClassificacaoRequest


def lambda_handler(event, context):
    """
    Handler para AWS Lambda.
    
    Args:
        event: Evento Lambda contendo:
            {
                "texto": "Texto da reclamação a classificar"
            }
        context: Contexto Lambda
        
    Returns:
        {
            "statusCode": 200 ou 400,
            "body": JSON com resultado da classificação
        }
    """
    try:
        # Extrai texto do evento
        body = event.get("body")
        if isinstance(body, str):
            body = json.loads(body)
        
        texto = body.get("texto", "")
        
        if not texto or not texto.strip():
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "erro": "Campo 'texto' é obrigatório e não pode estar vazio"
                })
            }
        
        # Cria request
        request = ClassificacaoRequest(texto=texto.strip())
        
        # Inicializa classificador e handler
        classificador = ClassificadorReclamacoes()
        handler = ClassificacaoHandler(classificador)
        
        # Classifica
        resposta = handler.classificar(request)
        
        # Prepara resposta
        if resposta.tem_erros:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "erro": resposta.mensagem_erro,
                    "texto": resposta.texto_original
                })
            }
        
        # Sucesso
        categorias = [
            {
                "nome": cat.nome,
                "confianca": cat.confianca
            }
            for cat in resposta.categorias
        ]
        
        return {
            "statusCode": 200,
            "body": json.dumps({
                "texto": resposta.texto_original,
                "categorias": categorias,
                "sucesso": True
            })
        }
    
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "erro": f"Erro ao processar: {str(e)}"
            })
        }


def classificar_texto(texto: str) -> dict:
    """
    Função utilitária para classificar texto sem context Lambda.
    Útil para testes locais e integração.
    
    Args:
        texto: Texto a classificar
        
    Returns:
        dict: Resultado da classificação
    """
    try:
        request = ClassificacaoRequest(texto=texto.strip())
        
        # Valida
        valido, erro = request.validar()
        if not valido:
            return {
                "sucesso": False,
                "erro": erro,
                "texto": texto
            }
        
        # Classifica
        classificador = ClassificadorReclamacoes()
        handler = ClassificacaoHandler(classificador)
        resposta = handler.classificar(request)
        
        if resposta.tem_erros:
            return {
                "sucesso": False,
                "erro": resposta.mensagem_erro,
                "texto": resposta.texto_original
            }
        
        categorias = [
            {
                "nome": cat.nome,
                "confianca": cat.confianca
            }
            for cat in resposta.categorias
        ]
        
        return {
            "sucesso": True,
            "texto": resposta.texto_original,
            "categorias": categorias
        }
    
    except Exception as e:
        return {
            "sucesso": False,
            "erro": str(e),
            "texto": texto
        }
