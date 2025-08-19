menu = """
========== BANCO ==========
Bem vindo ao nosso sistema bancário!
Escolha uma das opções abaixo:
===========================
[1] Depositar
[2] Sacar
[3] Extrato
[4] Cadastrar Usuário
[5] Criar Conta
[6] Listar Contas
[7] Sair
===========================
Digite a opção desejada: """

# ==============================
# Variáveis globais
# ==============================
saldo = 0
saque_maximo = 500
numero_saques = 0
limite_saques = 3
extrato = ""

usuarios = []  # lista de dicionários
contas = []    # lista de dicionários
conta_logada = None  # guarda a conta que está em uso


# ==============================
# Funções do sistema bancário
# ==============================
def depositar(valor, saldo, extrato):
    if valor < 100:
        print("\nValor mínimo para depósito é R$ 100,00.")
    else:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
        print(f"\nDepósito realizado! Saldo atual: R$ {saldo:.2f}")
    return saldo, extrato


def sacar(valor, saldo, extrato, numero_saques, limite_saques, saque_maximo):
    if numero_saques >= limite_saques:
        print("\nNúmero máximo de saques diários atingido.")
    elif valor > saque_maximo:
        print(f"\nValor máximo para saque é R$ {saque_maximo:.2f}")
    elif valor > saldo:
        print("\nSaldo insuficiente.")
    else:
        numero_saques += 1
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        print(f"\nSaque realizado! Saldo atual: R$ {saldo:.2f} | Saques restantes: {limite_saques - numero_saques}")
    return saldo, extrato, numero_saques


def mostrar_extrato(saldo, extrato):
    print("\n========== EXTRATO ==========")
    if extrato:
        print(extrato)
    else:
        print("Nenhuma movimentação realizada.")
    print(f"Saldo atual: R$ {saldo:.2f}")
    print("=============================")
# ==============================
# Funções de usuário e conta
# ==============================
def cadastrar_usuario(usuarios):
    cpf = input("Digite o CPF (somente números): ")

    usuario = next((u for u in usuarios if u["cpf"] == cpf), None)
    if usuario:
        print("\nUsuário já cadastrado!")
        return usuarios

    nome = input("Digite o nome completo: ")
    data_nascimento = input("Digite a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Digite o endereço (logradouro, número, bairro, cidade/UF, CEP): ")

    usuarios.append({
        "nome": nome,
        "data_nascimento": data_nascimento,
        "cpf": cpf,
        "endereco": endereco
    })

    print("\nUsuário cadastrado com sucesso!")
    return usuarios


def criar_conta(usuarios, contas):
    cpf = input("Informe o CPF do usuário: ")
    usuario = next((u for u in usuarios if u["cpf"] == cpf), None)

    if not usuario:
        print("\nUsuário não encontrado. Cadastre primeiro.")
        return contas, None

    numero_conta = f"{len(contas)+1:04d}"  # gera id sequencial
    conta = {
        "id": numero_conta,
        "usuario": cpf
    }
    contas.append(conta)

    print(f"\nConta criada com sucesso! Número da conta: {numero_conta}")
    return contas, conta


def listar_contas(contas, usuarios):
    print("\n========== CONTAS ==========")
    if not contas:
        print("Nenhuma conta cadastrada.")
    else:
        for conta in contas:
            usuario = next(u for u in usuarios if u["cpf"] == conta["usuario"])
            print(f"Conta: {conta['id']} | Usuário: {usuario['nome']} | CPF: {usuario['cpf']}")
    print("=============================")

# Loop principal

while True:
    opcao = input(menu)

    if opcao in ["1", "2", "3"] and not conta_logada:
        print("\nVocê precisa cadastrar um usuário e criar uma conta antes de usar essa opção.\nVoltando ao menu principal...")
        continue

    if opcao == "1":
        valor = float(input("Valor para depósito: "))
        saldo, extrato = depositar(valor, saldo, extrato)

    elif opcao == "2":
        valor = float(input("Valor para saque: "))
        saldo, extrato, numero_saques = sacar(valor, saldo, extrato, numero_saques, limite_saques, saque_maximo)

    elif opcao == "3":
        mostrar_extrato(saldo, extrato)

    elif opcao == "4":
        cadastrar_usuario(usuarios)

    elif opcao == "5":
        contas, conta = criar_conta(usuarios, contas)
        if conta:
            conta_logada = conta  # define a conta atual
            print(f"Agora você está usando a conta {conta['id']}.")

    elif opcao == "6":
        listar_contas(contas, usuarios)

    elif opcao == "7":
        print("\nObrigado por usar nosso banco. Até mais!")
        break

    else:
        print("\nOpção inválida. Tente novamente.")
