from pathlib import Path


def ordenar_linhas(arquivo_entrada: str, arquivo_saida: str) -> None:
    linhas = Path(arquivo_entrada).read_text(encoding="utf-8").splitlines()
    linhas_ordenadas = sorted(linhas, key=str.lower)
    Path(arquivo_saida).write_text(
        "\n".join(linhas_ordenadas) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    entrada = input("Arquivo de entrada: ").strip()
    saida = input("Arquivo de saida: ").strip()
    ordenar_linhas(entrada, saida)
    print(f"Arquivo ordenado criado: {saida}")
