"""
Testes Unitários: Handler de Classificação
Testa o handler de classificação do microserviço.
"""

import pytest
from src.application.use_cases import ClassificacaoHandler
from src.application.dtos import ClassificacaoRequest, ClassificacaoResponse
from src.domain.services import ClassificadorReclamacoes


class TestClassificacaoHandler:
    """Suite de testes para ClassificacaoHandler."""
    
    @pytest.fixture
    def classificador(self):
        """Fixture: classificador inicializado."""
        return ClassificadorReclamacoes()
    
    @pytest.fixture
    def handler(self, classificador):
        """Fixture: handler inicializado."""
        return ClassificacaoHandler(classificador)
    
    def test_classificar_texto_valido(self, handler):
        """
        Testa: Classificação de texto válido.
        Evidência: Handler retorna resposta com categorias.
        """
        request = ClassificacaoRequest(
            texto="Tenho problemas com acesso à minha conta corrente"
        )
        
        resposta = handler.classificar(request)
        
        assert resposta is not None
        assert isinstance(resposta, ClassificacaoResponse)
        assert resposta.texto_original == request.texto
        assert not resposta.tem_erros
        assert len(resposta.categorias) > 0
    
    def test_classificar_texto_vazio_retorna_erro(self, handler):
        """
        Testa: Texto vazio retorna erro.
        Evidência: Validação detecta texto inválido.
        """
        request = ClassificacaoRequest(texto="")
        
        resposta = handler.classificar(request)
        
        assert resposta.tem_erros
        assert resposta.mensagem_erro != ""
        assert len(resposta.categorias) == 0
    
    def test_classificar_texto_apenas_espacos_retorna_erro(self, handler):
        """
        Testa: Texto com apenas espaços retorna erro.
        Evidência: Validação é rigorosa.
        """
        request = ClassificacaoRequest(texto="   ")
        
        resposta = handler.classificar(request)
        
        assert resposta.tem_erros
        assert len(resposta.categorias) == 0
    
    def test_categorias_tem_nome_e_confianca(self, handler):
        """
        Testa: Cada categoria tem nome e confiança.
        Evidência: Resposta contém dados estruturados.
        """
        request = ClassificacaoRequest(
            texto="Problema com débito automático em minha conta"
        )
        
        resposta = handler.classificar(request)
        
        assert not resposta.tem_erros
        for categoria in resposta.categorias:
            assert categoria.nome is not None
            assert categoria.nome.strip() != ""
            assert 0.0 <= categoria.confianca <= 1.0
    
    def test_confianca_entre_0_e_1(self, handler):
        """
        Testa: Confiança sempre está entre 0 e 1.
        Evidência: Validação de range de confiança.
        """
        textos = [
            "Erro ao transferir dinheiro",
            "Aplicativo não funciona",
            "Taxa muito alta",
            "Atendimento ruim"
        ]
        
        for texto in textos:
            request = ClassificacaoRequest(texto=texto)
            resposta = handler.classificar(request)
            
            if not resposta.tem_erros:
                for categoria in resposta.categorias:
                    assert 0.0 <= categoria.confianca <= 1.0
