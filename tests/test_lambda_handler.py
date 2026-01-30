"""
Testes para Lambda Handler
Testa o entry point serverless.
"""

import json
import pytest
from lambda_handler import lambda_handler, classificar_texto


class TestLambdaHandler:
    """Suite de testes para lambda_handler."""
    
    def test_lambda_handler_classificacao_sucesso(self):
        """
        Testa: Lambda handler com requisição válida.
        Evidência: Retorna status 200 e resposta JSON.
        """
        evento = {
            "body": json.dumps({
                "texto": "Tenho problemas com acesso à minha conta"
            })
        }
        
        resposta = lambda_handler(evento, None)
        
        assert resposta["statusCode"] == 200
        body = json.loads(resposta["body"])
        assert body["sucesso"] is True
        assert "categorias" in body
        assert "texto" in body
    
    def test_lambda_handler_texto_vazio(self):
        """
        Testa: Lambda handler com texto vazio.
        Evidência: Retorna status 400 com erro.
        """
        evento = {
            "body": json.dumps({
                "texto": ""
            })
        }
        
        resposta = lambda_handler(evento, None)
        
        assert resposta["statusCode"] == 400
        body = json.loads(resposta["body"])
        assert "erro" in body
    
    def test_lambda_handler_sem_texto(self):
        """
        Testa: Lambda handler sem campo texto.
        Evidência: Retorna status 400.
        """
        evento = {
            "body": json.dumps({})
        }
        
        resposta = lambda_handler(evento, None)
        
        assert resposta["statusCode"] == 400
    
    def test_lambda_handler_body_string(self):
        """
        Testa: Lambda handler com body como string JSON.
        Evidência: Parse correto de JSON.
        """
        evento = {
            "body": '{"texto": "Erro ao transferir dinheiro"}'
        }
        
        resposta = lambda_handler(evento, None)
        
        assert resposta["statusCode"] == 200
        body = json.loads(resposta["body"])
        assert body["sucesso"] is True
    
    def test_lambda_handler_exception(self):
        """
        Testa: Lambda handler com erro não esperado.
        Evidência: Retorna status 500 com mensagem de erro.
        """
        evento = {
            "body": None
        }
        
        resposta = lambda_handler(evento, None)
        
        assert resposta["statusCode"] == 500
        body = json.loads(resposta["body"])
        assert "erro" in body
    
    def test_classificar_texto_sucesso(self):
        """
        Testa: Função classificar_texto com texto válido.
        Evidência: Retorna dicionário com sucesso.
        """
        resultado = classificar_texto("Problema com débito automático")
        
        assert resultado["sucesso"] is True
        assert "categorias" in resultado
        assert "texto" in resultado
        assert isinstance(resultado["categorias"], list)
    
    def test_classificar_texto_vazio(self):
        """
        Testa: Função classificar_texto com texto vazio.
        Evidência: Retorna sucesso=False.
        """
        resultado = classificar_texto("")
        
        assert resultado["sucesso"] is False
        assert "erro" in resultado
    
    def test_classificar_texto_apenas_espacos(self):
        """
        Testa: Função classificar_texto com espaços.
        Evidência: Tratamento de whitespace.
        """
        resultado = classificar_texto("   ")
        
        assert resultado["sucesso"] is False
