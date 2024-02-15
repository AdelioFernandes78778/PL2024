import os
import sys

def processar_dados(filename):
    with open(filename, 'r') as file:
        linhas = file.readlines()

    linhas = linhas[1:]

    modalidades = set()
    aptos = 0
    inaptos = 0
    distribuicao_idades = {'[20-24]': 0, '[25-29]': 0, '[30-34]': 0, '[35-39]': 0, '[40-44]': 0, '[45-49]': 0}


    for linha in linhas:
        colunas = linha.split('\t')

        modalidade = colunas[8]
        idade = int(colunas[5])

        modalidades.add(modalidade)

        federado = colunas[11]
        resultado = colunas[12]
        if federado == 'true' and resultado == 'true':
            aptos += 1
        else:
            inaptos += 1

        for faixa in distribuicao_idades:
            faixa_inicio, faixa_fim = map(int, faixa.strip('[]').split('-'))
            if faixa_inicio <= idade <= faixa_fim:
                distribuicao_idades[faixa] += 1
                break

    modalidades_ordenadas = sorted(list(modalidades))

    total_atletas = aptos + inaptos
    percentagem_aptos = (aptos / total_atletas) * 100
    percentagem_inaptos = (inaptos / total_atletas) * 100

    return modalidades_ordenadas, percentagem_aptos, percentagem_inaptos, distribuicao_idades


modalidades, percentagem_aptos, percentagem_inaptos, distribuicao_idades = processar_dados("./emd.csv")

print("Modalidades:", modalidades)
print("Atletas aptos:", percentagem_aptos)
print("Atletas inaptos:", percentagem_inaptos)
print("Atletas por escalão etário:")
for faixa_etaria, num_atletas in distribuicao_idades.items():
    print(faixa_etaria, ":", num_atletas)
