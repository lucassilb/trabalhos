import re
from pathlib import Path


def buscar_palavra(caminho: str, palavra: str) -> list[int]:
    palavra_normalizada = palavra.lower()
    linhas_encontradas = []

    with Path(caminho).open("r", encoding="utf-8") as arquivo:
        for numero_linha, linha in enumerate(arquivo, start=1):
            palavras_linha = re.findall(r"\w+", linha.lower(), flags=re.UNICODE)
            if palavra_normalizada in palavras_linha:
                linhas_encontradas.append(numero_linha)

    return linhas_encontradas


if __name__ == "__main__":
    arquivo = input("Nome do arquivo de texto: ").strip()
    palavra = input("Palavra para buscar: ").strip()
    linhas = buscar_palavra(arquivo, palavra)

    if linhas:
        print(f"Palavra encontrada nas linhas: {linhas}")
    else:
        print("Palavra nao encontrada.")
