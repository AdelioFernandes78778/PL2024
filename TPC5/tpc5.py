import json
import ply.lex as lex
from datetime import datetime
import re


tokens = (
    'LISTAR',
    'MOEDA',
    'SELECIONAR',
    'ADICIONAR',
    'SAIR',
    'CODIGO',
    'NOME',
    'QUANTIDADE',
    'PRECO',
    'VALOR_MOEDA',
)

t_LISTAR = r'LISTAR'

t_SELECIONAR = r'SELECIONAR'
t_ADICIONAR = r'ADICIONAR'
t_SAIR = r'SAIR'
t_CODIGO = r'[A-Z][0-9]+'
t_NOME = r'\".*\"'
t_QUANTIDADE = r'[0-9]+'
t_PRECO = r'[0-9]+e[0-9]+c'
t_VALOR_MOEDA = r'(1|2|5|10|20|50)e|(1|2|5)c'

t_ignore = ' \n'


# Função para processar o token MOEDA
def t_MOEDA(t):
    r'MOEDA\s+((2|5|10|20|50)c|(1|2)e)(?:\s*,\s*((2|5|10|20|50)c|(1|2)e))*'

    # Inicializar saldo
    saldo = 0

    # Processar moedas e calcular saldo
    for moeda in re.finditer(r'(?:(?P<cent>2|5|10|20|50)c|(?P<euro>1|2)e)', t.value):
        if moeda.lastgroup == "cent":
            saldo += int(moeda.group("cent"))
        else:
            saldo += int(moeda.group("euro")) * 100

    # Exibir saldo
    printable_euro, printable_cent = divmod(saldo, 100)
    print(f"maq: Saldo = {printable_euro}e{printable_cent}c")
    
    # Retorna o saldo calculado
    t.value = saldo
    return t

def t_error(t):
    print(f"Caracter ilegal '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

# Função para processar o comando de selecionar produto
def selecionar_produto(codigo, saldo, stock):
    for produto in stock:
        if produto['cod'] == codigo:
            if produto['quant'] > 0 and produto['preco'] <= saldo:
                produto['quant'] -= 1
                saldo -= produto['preco']
                print(f"Pode retirar o produto dispensado \"{produto['nome']}\"")
                print(f"Saldo = {saldo // 100}e{saldo % 100}c")
            elif produto['quant'] == 0:
                print("Produto esgotado.")
            else:
                print(f"Saldo insuficiente para satisfazer o seu pedido")
                print(f"Saldo = {saldo // 100}e{saldo % 100}c; Pedido = {produto['preco'] // 100}e{produto['preco'] % 100}c")
            return saldo
    print("Produto inexistente.")
    return saldo

# Função para adicionar produto ao estoque
def adicionar_produto(codigo, nome, quantidade, preco, stock):
    for produto in stock:
        if produto['cod'] == codigo:
            produto['quant'] += quantidade
            print(f"Adicionadas {quantidade} unidades de \"{nome}\" ao stock.")
            return
    novo_produto = {"cod": codigo, "nome": nome, "quant": quantidade, "preco": preco}
    stock.append(novo_produto)
    print(f"Produto \"{nome}\" adicionado ao stock.")

# Função principal
def main():
    # Carregar dados do arquivo stock.json
    with open('TPC5/stock.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Obter o estoque do arquivo JSON
    stock = data["stock"]

    print("maq: 2024-03-08, Stock carregado, Estado atualizado.")
    print("maq: Bom dia. Estou disponível para atender o seu pedido.")

    saldo = 0  # Inicializa o saldo como zero

    while True:
        comando = input(">> ")
        lexer.input(comando)

        # Processa cada token do comando
        for tok in lexer:
            if tok.type == 'LISTAR':
                print("maq:")
                print("cod | nome | quantidade | preço")
                print("-" * 33)
                for produto in stock:
                    print(f"{produto['cod']} {produto['nome']} {produto['quant']} {produto['preco']}")
                print()
            elif tok.type == 'SELECIONAR':
                codigo = input("Código do produto: ")
                saldo = selecionar_produto(codigo, saldo, stock)
            elif tok.type == 'ADICIONAR':
                codigo = input("Código do produto: ")
                nome = input("Nome do produto: ")
                quantidade = int(input("Quantidade: "))
                preco = input("Preço (em centavos): ")
                adicionar_produto(codigo, nome, quantidade, preco, stock)
            elif tok.type == 'SAIR':
                print("Saindo...")
                return
            elif tok.type == 'MOEDA':
                moeda_completo = comando.split()[1]  # Obtém a parte após o comando MOEDA
                moedas = re.findall(r'\d+', moeda_completo)  # Extrai valores numéricos
                saldo += sum(int(m) for m in moedas)  # Adiciona ao saldo total
                print(f"maq: Saldo = {saldo // 100}e{saldo % 100}c")
                break  # Interrompe o loop após processar o token MOEDA
            else:
                print(f"Comando inválido: {tok.value}")

if __name__ == "__main__":
    main()
