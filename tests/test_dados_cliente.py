"""
Testes Unitários: Value Object DadosCliente
Testa validações de CPF e Email (não é crítico para o microserviço de classificação).
"""

import pytest
from src.domain.value_objects import DadosCliente


class TestDadosCliente:
    """Suite de testes para o Value Object DadosCliente."""
    
    @pytest.fixture
    def cpf_valido(self):
        """CPF válido para testes."""
        return "11144477735"
    
    def test_criar_dados_cliente_validos(self, cpf_valido):
        """
        Testa: Criação com dados válidos.
        Evidência: Factory method funciona.
        """
        cliente = DadosCliente.criar(
            nome_cliente="João Silva",
            cpf=cpf_valido,
            email="joao@email.com",
            telefone="11999999999",
            numero_conta="123456789"
        )
        
        assert cliente.nome_cliente == "João Silva"
        assert cpf_valido in cliente.cpf  # CPF contém os dígitos
        assert cliente.email == "joao@email.com"
    
    def test_criar_dados_cliente_cpf_invalido(self):
        """
        Testa: CPF inválido lança erro.
        Evidência: Validação no factory method.
        """
        with pytest.raises(ValueError, match="CPF inválido"):
            DadosCliente.criar(
                nome_cliente="João Silva",
                cpf="00000000000",  # CPF inválido
                email="joao@email.com"
            )
    
    def test_criar_dados_cliente_email_invalido(self, cpf_valido):
        """
        Testa: Email inválido lança erro.
        """
        with pytest.raises(ValueError, match="Email inválido"):
            DadosCliente.criar(
                nome_cliente="João Silva",
                cpf=cpf_valido,
                email="email_invalido"  # Email sem @
            )
    
    def test_criar_dados_cliente_nome_vazio(self, cpf_valido):
        """
        Testa: Nome vazio lança erro.
        """
        with pytest.raises(ValueError, match="não pode estar vazio"):
            DadosCliente.criar(
                nome_cliente="",
                cpf=cpf_valido,
                email="joao@email.com"
            )
    
    def test_dados_cliente_imutavel(self, cpf_valido):
        """
        Testa: Propriedades são read-only (immutable).
        Evidência: dataclass frozen=True
        """
        cliente = DadosCliente.criar(
            nome_cliente="João",
            cpf=cpf_valido,
            email="joao@email.com"
        )
        
        # Tenta modificar
        with pytest.raises(Exception):  # FrozenInstanceError
            cliente.nome_cliente = "Maria"
    
    def test_igualdade_mesmo_cpf_e_email(self, cpf_valido):
        """
        Testa: Igualdade por valor (mesmo CPF e Email).
        Evidência: Value Object implementa __eq__
        """
        cliente1 = DadosCliente.criar(
            nome_cliente="João Silva",
            cpf=cpf_valido,
            email="joao@email.com"
        )
        
        cliente2 = DadosCliente.criar(
            nome_cliente="João Silva",
            cpf=cpf_valido,
            email="joao@email.com"
        )
        
        # Mesmo valor = iguais
        assert cliente1 == cliente2
    
    def test_mascarar_cpf(self, cpf_valido):
        """
        Testa: Mascaramento de CPF para exibição segura.
        """
        cliente = DadosCliente.criar(
            nome_cliente="João",
            cpf=cpf_valido,
            email="joao@email.com"
        )
        
        cpf_mascarado = cliente.mascarar_cpf()
        
        # Verifica que é mascarado (contém *)
        assert "*" in cpf_mascarado
        assert len(cpf_mascarado) > 0
    
    def test_mascarar_email(self, cpf_valido):
        """
        Testa: Mascaramento de email para exibição segura.
        """
        cliente = DadosCliente.criar(
            nome_cliente="João",
            cpf=cpf_valido,
            email="joao@email.com"
        )
        
        email_mascarado = cliente.mascarar_email()
        
        # Verifica que é mascarado
        assert "*" in email_mascarado
        assert "@" in email_mascarado
    
    def test_cpf_com_pontuacao_aceito(self):
        """
        Testa: CPF com pontuação é aceito.
        """
        cliente = DadosCliente.criar(
            nome_cliente="João",
            cpf="111.444.777-35",  # Com pontuação
            email="joao@email.com"
        )
        
        assert cliente is not None
    
    def test_dados_opcionais_nao_obrigatorios(self, cpf_valido):
        """
        Testa: Campos opcionais (telefone, conta) não são obrigatórios.
        """
        cliente = DadosCliente.criar(
            nome_cliente="João",
            cpf=cpf_valido,
            email="joao@email.com"
            # Sem telefone e numero_conta
        )
        
        assert cliente.telefone is None
        assert cliente.numero_conta is None
