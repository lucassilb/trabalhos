import json
import os


PASTA_PROJETO = os.path.dirname(__file__)
ARQUIVO_PADRAO = os.path.join(PASTA_PROJETO, "tarefas.json")


def carregar_tarefas(caminho=ARQUIVO_PADRAO):
    try:
        arquivo = open(caminho, "r", encoding="utf-8")
    except FileNotFoundError:
        return []

    with arquivo:
        dados = json.load(arquivo)

    if not isinstance(dados, list):
        raise ValueError("Arquivo de tarefas invalido: esperado uma lista.")
    return dados


def salvar_tarefas(tarefas, caminho=ARQUIVO_PADRAO):
    with open(caminho, "w", encoding="utf-8") as arquivo:
        json.dump(tarefas, arquivo, ensure_ascii=False, indent=2)
        arquivo.write("\n")
