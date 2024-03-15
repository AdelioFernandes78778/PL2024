import re

def somador(texto):
    somar = False
    soma = 0
    for palavra in texto.split():
        if somar:
            numeros = re.findall(r'\d+', palavra)
            for numero in numeros:
                soma += int(numero)
        if "on" in palavra.lower():
            somar = True
        elif "off" in palavra.lower():
            somar = False
        elif "=" in palavra:
            print(soma)
            soma = 0


# Exemplos de uso:
# Exemplo 1:
texto1 = "O somador está moN agora, 123 e 456 devem ser somados = 579 Off"
somador(texto1)  # Saída esperada: 579

# Exemplo 2:
texto2 = "oN O primeiro número é 100, depois vem Off = 100 On então mais 200 e 300 = 500"
somador(texto2)  # Saída esperada: 100, 500

# Exemplo 3:
texto3 = "Temos oFf 10 e On 20 = 20"
somador(texto3)  # Saída esperada: 20

# Exemplo 4: 
texto4 = """
on 27 12 ON 1 off 0 monad 1 = on 27 12 ON 1 off 0 moNaD 1 = on 27 12 ON 1 off 0 on 1 =

monad 5 on 3 off 4 on 1 = on 5 on 3 off 4 on 1 =

off 7 on 1 on 3 on 1 = oFfshore 7 on 1 on 3 on 1 =

on 1 inOffsrx 3 on 1 on 5 = on 1 off 3 on 1 on 5 =
"""
somador(texto4) # Saída esperada: 41, 41, 41, 9, 9, 5, 5, 7, 7

