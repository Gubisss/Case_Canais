"""
Value Object: DadosCliente
Representa dados imutáveis do cliente com validações.
Implementa igualdade por valor e encapsulamento.
"""

import re
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class DadosCliente:
    """
    Value Object imutável que encapsula dados do cliente.
    Propriedades são todas somente leitura.
    Valida CPF e Email na criação.
    """
    
    nome_cliente: str
    cpf: str
    email: str
    telefone: Optional[str] = None
    numero_conta: Optional[str] = None
    
    def __post_init__(self):
        """Valida os dados na criação."""
        if not self.nome_cliente or not self.nome_cliente.strip():
            raise ValueError("Nome do cliente não pode estar vazio")
        
        if not self.cpf or not self._validar_cpf(self.cpf):
            raise ValueError("CPF inválido")
        
        if not self._validar_email(self.email):
            raise ValueError("Email inválido")
    
    @staticmethod
    def _validar_cpf(cpf: str) -> bool:
        """
        Valida um CPF usando o algoritmo de dígito verificador.
        
        Args:
            cpf: String no formato com ou sem pontuação
            
        Returns:
            bool: True se CPF é válido, False caso contrário
        """
        # Remove pontuação
        cpf_limpo = re.sub(r'\D', '', cpf)
        
        # Verifica tamanho
        if len(cpf_limpo) != 11:
            return False
        
        # Verifica se não é sequência repetida
        if cpf_limpo == cpf_limpo[0] * 11:
            return False
        
        # Calcula primeiro dígito verificador
        soma = sum(int(cpf_limpo[i]) * (10 - i) for i in range(9))
        primeiro_digito = 11 - (soma % 11)
        primeiro_digito = 0 if primeiro_digito > 9 else primeiro_digito
        
        if int(cpf_limpo[9]) != primeiro_digito:
            return False
        
        # Calcula segundo dígito verificador
        soma = sum(int(cpf_limpo[i]) * (11 - i) for i in range(10))
        segundo_digito = 11 - (soma % 11)
        segundo_digito = 0 if segundo_digito > 9 else segundo_digito
        
        return int(cpf_limpo[10]) == segundo_digito
    
    @staticmethod
    def _validar_email(email: str) -> bool:
        """
        Valida formato básico de email.
        
        Args:
            email: String com endereço de email
            
        Returns:
            bool: True se email é válido, False caso contrário
        """
        padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(padrao, email))
    
    @classmethod
    def criar(
        cls,
        nome_cliente: str,
        cpf: str,
        email: str,
        telefone: Optional[str] = None,
        numero_conta: Optional[str] = None
    ) -> 'DadosCliente':
        """
        Factory method para criar DadosCliente com validação.
        
        Args:
            nome_cliente: Nome completo do cliente
            cpf: CPF do cliente (com ou sem pontuação)
            email: Email válido do cliente
            telefone: Telefone opcional do cliente
            numero_conta: Número da conta opcional
            
        Returns:
            DadosCliente: Instância validada do value object
            
        Raises:
            ValueError: Se algum dado for inválido
        """
        return cls(
            nome_cliente=nome_cliente.strip() if nome_cliente else "",
            cpf=cpf,
            email=email.strip() if email else "",
            telefone=telefone,
            numero_conta=numero_conta
        )
    
    def mascarar_cpf(self) -> str:
        """
        Retorna CPF mascarado para exibição (exemplo: "123.***.*-00").
        
        Returns:
            str: CPF mascarado
        """
        cpf_limpo = re.sub(r'\D', '', self.cpf)
        if len(cpf_limpo) == 11:
            return f"{cpf_limpo[:3]}.***.*-{cpf_limpo[-2:]}"
        return "***.**.**-**"
    
    def mascarar_email(self) -> str:
        """
        Retorna email mascarado para exibição (exemplo: "jo***@email.com").
        
        Returns:
            str: Email mascarado
        """
        if "@" in self.email:
            local, dominio = self.email.split("@")
            if len(local) > 2:
                mascarado = local[0] + "*" * (len(local) - 2) + local[-1]
                return f"{mascarado}@{dominio}"
        return "***@***"
