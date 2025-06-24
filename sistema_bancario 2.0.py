# constantes 
LIMITE_VALOR_SAQUE = 500
LIMITE_SAQUES = 3
AGENCIA = "0001"

# Funções
def depositar(saldo, valor, extrato, /):
  if valor > 0:
      saldo += valor
      extrato += f"Depósito: R$ {valor:.2f}\n"
      print(f"Depósito de R$ {valor:.2f} realizado com sucesso!")
  else:
      print("Operação falhou! O valor do depósito deve ser positivo.")
  return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
  if valor > saldo:
      print("Operação falhou! Você não tem saldo suficiente.")

  elif valor > limite:
      print("Operação falhou! O valor do saque excede o limite de R$500,00.")

  elif numero_saques >= limite_saques:
      print("Operação falhou! Número máximo de saques diários atingido.")

  elif valor > 0:
      saldo -= valor
      extrato += f"Saque: R$ {valor:.2f}\n"
      numero_saques +=1
      print(f"Saque de R$ {valor:.2f} realizado com sucesso!")

  else:
      print("Operação falhou! O valor do saque deve ser positivo.")

  return saldo, extrato, numero_saques

def exibir_extrato(saldo, /, *, extrato):
   print("\n=== EXTRATO ===")
   print(extrato if extrato else "Não foram realizadas movimentações.")
   print(f"Saldo atual: R$ {saldo:.2f}")

def cadastrar_usuario(usuarios):
   cpf = input("Informe o CPF (somente números): ").strip()

   # Aqui verifica se o CPF já existe
   usuario  = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
   if usuario:
      print("Já existe um usuário com esse CPF")
      return 
   
   nome = input("Informe o nome completo: ").strip()
   data_nascimento = input("Informe a data de nascimento (dd/mm/aaa): ").strip()
   endereco = input("Informe o endereço (lograduro, número, bairro, cidade/sigla estado): ").strip()

   usuarios.append({
      "nome": nome,
      "data_nascimento": data_nascimento,
      "cpf": cpf,
      "endereco": endereco
   })

   print("Usuário cadastrado com sucesso")

def cadastrar_conta(agencia, numero_conta, usuarios):
   cpf = input("Informe o CPF do usuário: ").strip()

  # Aqui verifica se o usuario já possui cadastro
   usuario = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
   if not usuario:
    print("Usuário não encontrado! Cadastro de conta cancelado")
    return None

   print("Conta criada com sucesso!")
   return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario[0]}

# Programa principal
menu = """

Escolha uma opção:
[d] Depositar
[s] Sacar
[e] Extrato
[u] Novo Usuário
[c] Nova Conta
[q] Sair

=>"""

saldo = 0 
extrato = ""
numero_saques = 0
usuarios = []
contas = []
numero_conta = 1

while True:

  opcao = input(menu).lower()

  if opcao == "d":
    print("Depósito")
    try:
      valor = float(input("Informe o valor do depósito: "))
    except ValueError:
      print("Valor inválido! Informe um número válido.")
      continue # Verificação para não quebrar o código
    
    saldo, extrato = depositar(saldo, valor, extrato)

  elif opcao == "s":
    print("Saque")
    try:
      valor = float(input("Informe o valor do saque: "))
    except ValueError:
      print("Valor inválido! Informe um número válido.")
      continue 

    saldo, extrato, numero_saques = sacar(
       saldo=saldo,
       valor=valor,
       extrato=extrato,
       limite=LIMITE_VALOR_SAQUE,
       numero_saques=numero_saques,
       limite_saques=LIMITE_SAQUES 
     )

  elif opcao == "e":
    exibir_extrato(saldo, extrato=extrato)

  elif opcao == "u":
     cadastrar_usuario(usuarios)

  elif opcao == "c":
     conta = cadastrar_conta(AGENCIA, numero_conta, usuarios)
     if conta:
        contas.append(conta)
        numero_conta += 1

  elif opcao == "q":
    print("Saindo do sistema. Até mais!")
    break

  else:
    print("Operação inválida, por favor selecione novamente a operação desejada.")

    # separar as funcoes existentes saque, deposito e extrato em funcoes def
      # saque: keyword only (saldo, valor, extrato, limite, numero_saques, limite_saques) return saldo e extrato
      # deposito: position only ( saldo, valor, extrato) retorno saldo e extrato
      # extrato: keyword e position ( posicional = saldo, argumentos nomeados = extrato)
    # criar duas novas funcoes: cadastrar usuario e cadastrar conta bancaria
      # criar usuario numa lista (nome, data nascimento, cpd e endereco)
        # endereço: logradouro, nro, bairro, cidade/sigla estado
        # armazena somente os numerros do cpf e não pode repetir
      # conta: agencia, numero e usuario. Numero da conta é sequencial iniciando em 1 e agencia fixo "0001"
        # o usuario pode ter mais contas, mas uma conta pertence a somente um usuario
  # dica: Para vincularr um usuario a uma conta, filtre a lista de usuaios buscando o numero do cpf informado-
    # para cada usuario da lista