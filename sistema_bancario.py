from abc import ABC, abstractmethod 
from datetime import datetime
import textwrap

class Cliente:
  def __init__(self, endereco):
    self.endereco = endereco
    self.contas = []

  def realizar_transacao(self, conta, transacao):
      transacao.registrar(conta)

  def adicionar_conta(self, conta):
      self.contas.append(conta)

class PessoaFisica(Cliente): # Estende da classe cliente
  def __init__(self, nome, data_nascimento, cpf, endereco):
    super().__init__(endereco)  # construtor da classe pai
    self.nome = nome
    self.data_nascimento = data_nascimento
    self.cpf = cpf

class Conta:
  def __init__(self, numero, cliente):
    self._saldo = 0
    self._numero = numero
    self._agencia = "0001"
    self._cliente = cliente
    self._historico = Historico()

  @classmethod
  def nova_conta(cls, cliente, numero):
    return cls(numero, cliente)         # class method recebe cliente e numero e retorna uma instancia de conta
  
  @property                 # propriedades para acesso
  def saldo(self):
    return self._saldo
  
  @property                 
  def numero(self):
    return self._numero
  
  @property                 
  def agencia(self):
    return self._agencia

  @property                 
  def cliente(self):
    return self._cliente

  @property                 
  def historico(self):
    return self._historico
  
  def sacar(self, valor):
    saldo = self.saldo
    excedeu_saldo = valor > saldo

    if excedeu_saldo:
      print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")

    elif valor > 0:
      print("\n=== Saque realizado com sucesso!===")
      return True
    
    else: 
      print("\n@@@ Operração falhou! O valor informado é inválido. @@@")

    return False
  
  def depositar(self, valor):
    if valor > 0:
      self._saldo += valor
      print("\n=== Depósito realizado com sucesso! =====")
    else:
      print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
      return False
    
    return True
  
class ContaCorrente(Conta): # estende de conta
  def __init__(self, numero, cliente, limite=500,limite_saques=3):
    super().__init__(numero, cliente)
    self.limite = limite
    self.limite_saques = limite_saques

  def sacar(self, valor):
    numero_saques = len(
      [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
    )

    excedeu_limite = valor > self.limite
    excedeu_saques = numero_saques >= self.limite_saques

    if excedeu_limite:
      print("\n@@@ Operação falhou! O valor do saque excedeu o limite. @@@")

    elif excedeu_saques:
      print("\n@@@ Operação Falhou! Número máximo de saques excedido. @@@")

    else:
      return super().sacar(valor)
    
    return False
  
  def __str__(self):
    return f"""\
          Agência:\t{self.agencia}
          C/C: \t\t{self.numero}
          Titular:\t{self.cliente.nome}
    """
  
class Historico:
  def __init__(self):
    self._transacoes = []

  @property
  def transacoes(self):
    return self._transacoes
  
  def adicionar_transacao(self, transacao):
    self._transacoes.append(
      {
          "tipo": transacao.__class__.__name__,
          "valor": transacao.valor,
          "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
      }
    )

class Transacao(ABC):

  @property
  def valor(self):
    pass

  @abstractmethod
  def registrar(self, conta):
    pass

class Saque(Transacao):
  def __init__(self, valor):
    self._valor = valor

  @property
  def valor(self):
    return self._valor
  
  def registrar(self, conta):
    sucesso_transacao = conta.sacar(self.valor)

    if sucesso_transacao:
      conta.historico.adicionar_transacao(self)

class Deposito(Transacao):

  def __init__(self, valor):
    self._valor = valor

  @property
  def valor(self):
    return self._valor
  
  def registrar(self, conta):
    sucesso_transacao = conta.depositar(self.valor)

    if sucesso_transacao:
      conta.historico.adicionar_transacao(self)

def menu():

  menu = """\n
==================== MENU ====================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [n]\tNovo Cliente
    [c]\tNova Conta
    [l]\tListar Contas
    [q]\tSair
    => """
  return input(textwrap.dedent(menu))

def recuperar_conta_cliente(cliente):
  if not cliente.contas:
    print("@@@ Cliente não possui conta! @@@")
    return
  
# FIXME: não permite clientes escolher a conta
  return cliente.contas[0]

def depositar(clientes):
  cpf = input("Informe o CPF do cliente: ")
  cliente = filtrar_cliente(cpf, clientes)

  if not cliente:
    print("\n@@@ cliente não encontrado! @@@")
    return

  valor = float(input("Informe o valor do depósito: "))
  transacao = Deposito(valor)

  conta = recuperar_conta_cliente(cliente)
  if not conta:
    return
  
  cliente.realizar_transacao(conta, transacao)

def sacar(clientes):
  cpf = input("Informe o CPF do cliente: ")
  cliente = filtrar_cliente(cpf, clientes)

  if not cliente:
    print("\n@@@ Cliente não encontrado! @@@")
    return

  valor = float(input("Informe o valor do saque: "))
  transacao = Saque(valor)

  conta = recuperar_conta_cliente(cliente)
  if not conta:
    return
  
  cliente.realizar_transacao(conta, transacao)

def filtrar_cliente(cpf, clientes):
  clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
  return clientes_filtrados[0] if clientes_filtrados else None

def exibir_extrato(clientes):
  cpf = input("Informe o CPF do cliente: ")
  cliente = filtrar_cliente(cpf, clientes)

  if not cliente:
    print("\n@@@ Cliente não encontrado! @@@")
    return
  
  conta = recuperar_conta_cliente(cliente)
  if not conta:
    return
  
  print("\n ===== EXTRATO =====")
  transacoes = conta.historico.transacoes

  extrato = ""
  if not transacoes:
    extrato = "Não foram realizadas movimentações."

  else: 
    for transacao in transacoes:
      extrato += f"\n{transacao['tipo']}\n\tR${transacao['valor']:.2f}"

  print(extrato)
  print(f"\nSaldo: \n\tR$ {conta.saldo:.2f}")
  print("==================")

def listar_contas(contas):
  for conta in contas:
    print("=" * 100)
    print(textwrap.dedent(str(conta)))

def criar_cliente(clientes):
  cpf = input("Informe o CPF do cliente: ")
  cliente = filtrar_cliente(cpf, clientes)

  if cliente:
    print("\n@@@ Já existe cliente com esse CPF! @@@")
    return
  
  nome = input("Informe o nome completo: ")
  data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
  endereco = input("Informe o endereco (logradouro, nr - bairro - cidade/sigla Estado): ")

  cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento,cpf=cpf,endereco=endereco)

  clientes.append(cliente)

  print("\n=== Cliente criado com sucesso! ===")

def criar_conta(numero_conta, clientes, contas):
  cpf = input("informe o cpf do cliente: ")
  cliente = filtrar_cliente(cpf, clientes)

  if not cliente: 
    print("\n@@@ Cliente não encontrado, fluxo de criação de conta encerrado! @@@")
    return
  
  conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
  contas.append(conta)
  cliente.contas.append(conta)

  print("\n=== Conta Criada com sucesso! ===")

def main():
  clientes = []
  contas = []

  while True:
    opcao = menu()

    if opcao == "d":
      depositar(clientes)

    elif opcao == "s":
      sacar(clientes)

    elif opcao == "e":
      exibir_extrato(clientes)

    elif opcao == "n":
      criar_cliente(clientes)

    elif opcao == "c":
      numero_conta = len(contas) + 1
      criar_conta(numero_conta, clientes, contas)

    elif opcao == "l":
      listar_contas(contas)

    elif opcao == "q":
      break

    else:
      print("\n@@@ Operação inválida, por favor selecione a operação desejada. @@@")


# Executar o programa quando o arquivo for chamado
if __name__ == "__main__":
    main()
