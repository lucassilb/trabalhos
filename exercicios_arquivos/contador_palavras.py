from pathlib import Path


def contar_palavras(caminho: str) -> int:
    texto = Path(caminho).read_text(encoding="utf-8")
    return len(texto.split())


if __name__ == "__main__":
    arquivo = input("Nome do arquivo de texto: ").strip()
    print(f"Quantidade de palavras: {contar_palavras(arquivo)}")
