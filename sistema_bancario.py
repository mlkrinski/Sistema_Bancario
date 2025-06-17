menu = """

Escolha uma opção:
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=>"""

saldo = 0 
LIMITE_VALOR_SAQUE = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:

  opcao = input(menu).lower()

  if opcao == "d":
    print("Depósito")
    try:
      valor = float(input("Informe o valor do depósito: "))
    except ValueError:
      print("Valor inválido! Informe um número válido.")
      continue # Verificação para não quebrar o código
    
    if valor > 0:
      saldo += valor
      extrato += f"Depósito: R$ {valor:.2f}\n"
      print(f"Depósito de R$ {valor:.2f} realizado com sucesso!")
    else:
      print("Operação falhou! O valor do depósito deve ser positivo.")

  elif opcao == "s":
    print("Saque")
    try:
      valor = float(input("Informe o valor do saque: "))
    except ValueError:
      print("Valor inválido! Informe um número válido.")
      continue 

    if valor > saldo:
      print("Operação falhou! Você não tem saldo suficiente.")

    elif valor > LIMITE_VALOR_SAQUE:
      print("Operação falhou! O valor do saque excede o limite de R$500,00.")

    elif numero_saques >= LIMITE_SAQUES:
      print("Operação falhou! Número máximo de saques diários atingido.")

    elif valor > 0:
      saldo -= valor
      extrato += f"Saque: R$ {valor:.2f}\n"
      numero_saques +=1
      print(f"Saque de R$ {valor:.2f} realizado com sucesso!")

    else:
      print("Operação falhou! O valor do saque deve ser positivo.")



  elif opcao == "e":
    print("\n=== EXTRATO ===")
    print(extrato if extrato else "Não foram realizadas movimentações.")
    print(f"Saldo atual: R$ {saldo:.2f}")

  elif opcao == "q":
    print("Saindo do sistema. Até mais!")
    break

  else:
    print("Operação inválida, por favor selecione novamente a operação desejada.")