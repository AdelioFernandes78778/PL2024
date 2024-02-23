import os
import sys

def processar_dados(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        linhas = file.readlines()

    linhas = linhas[1:]

    modalidades = set()
    aptos = 0
    inaptos = 0
    distribuicao_idades = {'[20-24]': {'num_atletas': 0, 'percentagem': 0},
                           '[25-29]': {'num_atletas': 0, 'percentagem': 0},
                           '[30-34]': {'num_atletas': 0, 'percentagem': 0},
                           '[35-39]': {'num_atletas': 0, 'percentagem': 0},
                           '[40-44]': {'num_atletas': 0, 'percentagem': 0},
                           '[45-49]': {'num_atletas': 0, 'percentagem': 0}}

    for linha in linhas:
        colunas = linha.split(',')

        if len(colunas) < 13:  # Verifica se há dados suficientes na linha
            continue  # Ignora a linha se não houver dados suficientes

        modalidade = colunas[8]
        idade = int(colunas[5])

        modalidades.add(modalidade)

        resultado = colunas[12].strip().lower()
        if resultado == 'true':
            aptos += 1
        else:
            inaptos += 1

        for faixa, info in distribuicao_idades.items():
            faixa_inicio, faixa_fim = map(int, faixa.strip('[]').split('-'))
            if faixa_inicio <= idade <= faixa_fim:
                info['num_atletas'] += 1
                break

    modalidades_ordenadas = sorted(list(modalidades))

    total_atletas = aptos + inaptos
    for faixa, info in distribuicao_idades.items():
        info['percentagem'] = round((info['num_atletas'] / total_atletas) * 100, 2)

    percentagem_aptos = (aptos / total_atletas) * 100 if total_atletas != 0 else 0
    percentagem_inaptos = (inaptos / total_atletas) * 100 if total_atletas != 0 else 0

    return modalidades_ordenadas, percentagem_aptos, percentagem_inaptos, distribuicao_idades


# Obtém o diretório do script atual
dir_path = os.path.dirname(os.path.realpath(__file__))

# Concatena o diretório do script com o nome do arquivo
file_path = os.path.join(dir_path, "emd.csv")

# Chama a função processar_dados usando o caminho absoluto do arquivo
modalidades, percentagem_aptos, percentagem_inaptos, distribuicao_idades = processar_dados(file_path)

print("Modalidades:", modalidades)
print("Atletas aptos:", percentagem_aptos)
print("Atletas inaptos:", percentagem_inaptos)
print("Atletas por escalão etário:")
for faixa_etaria, info in distribuicao_idades.items():
    print(f"{faixa_etaria} : {info['num_atletas']} ({info['percentagem']}%)")

