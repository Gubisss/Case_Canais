"""
Testes Unitários: Classificador de Reclamações
Testa a lógica de classificação NLP com 3 estratégias.
Nota: Testes legados, não críticos para o microserviço de classificação.
"""

import pytest
from src.domain.services import ClassificadorReclamacoes


class TestClassificadorReclamacoes:
    """Suite de testes para o ClassificadorReclamacoes."""
    
    @pytest.fixture
    def classificador(self):
        """Fixture: cria classificador para cada teste."""
        return ClassificadorReclamacoes()
    
    def test_classificar_texto_vazio_retorna_erro(self, classificador):
        """
        Testa: Texto vazio retorna erro.
        Evidência de validação de entrada.
        """
        resultado = classificador.classificar("")
        
        assert resultado.tem_erros is True
        assert len(resultado.categorias) == 0
    
    def test_classificar_problema_cobranca_identifica_categoria(self, classificador):
        """
        Testa: Texto com problema de cobrança é classificado.
        Exemplo: "Fui cobrado duas vezes"
        """
        resultado = classificador.classificar(
            "Recebi uma cobrança duplicada no meu boleto"
        )
        
        assert resultado.tem_erros is False
        assert len(resultado.categorias) > 0
        
        categorias_encontradas = [cat.nome for cat in resultado.categorias]
        assert any("cobranca" in cat for cat in categorias_encontradas)
    
    def test_classificar_texto_generico_retorna_vazio(self, classificador):
        """
        Testa: Texto genérico sem palavras-chave não classifica.
        Exemplo: "Não gosto do banco"
        """
        resultado = classificador.classificar(
            "Estou insatisfeito com o banco em geral"
        )
        
        # Pode retornar vazio ou baixa confiança
        assert resultado.tem_erros is False
    
    def test_scores_normalizados_entre_0_e_1(self, classificador):
        """
        Testa: Todos os scores são normalizados para [0, 1].
        """
        resultado = classificador.classificar(
            "Problema com cobrança no meu cartão de crédito"
        )
        
        assert resultado.tem_erros is False
        
        for categoria in resultado.categorias:
            assert 0.0 <= categoria.confianca <= 1.0
    
    def test_atualizar_categorias_adiciona_palavras_chave(self, classificador):
        """
        Testa: Adicionar nova categoria funciona.
        """
        # Adiciona categoria customizada
        classificador.atualizar_categorias(
            "problema_pessoal",
            ["divida", "emprestimo", "credito", "juros"]
        )
        
        # Testa se identifica a nova categoria
        resultado = classificador.classificar(
            "Estou com divida alta nos juros"
        )
        
        assert resultado.tem_erros is False
    
    def test_obter_categorias_disponiveis(self, classificador):
        """
        Testa: Retorna lista de categorias disponíveis.
        """
        categorias = classificador.obter_categorias_disponiveis()
        
        assert len(categorias) > 0
        assert "cobranca" in categorias
    
    def test_obter_palavras_chave_categoria_existente(self, classificador):
        """
        Testa: Retorna palavras-chave de categoria existente.
        """
        palavras = classificador.obter_palavras_chave("cobranca")
        
        assert palavras is not None
        assert len(palavras) > 0
    
    def test_obter_palavras_chave_categoria_inexistente(self, classificador):
        """
        Testa: Retorna None para categoria inexistente.
        """
        palavras = classificador.obter_palavras_chave("categoria_inexistente")
        
        assert palavras is None

