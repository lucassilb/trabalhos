from pathlib import Path


def concatenar_arquivos(
    primeiro_arquivo: str,
    segundo_arquivo: str,
    arquivo_saida: str,
) -> None:
    primeiro_texto = Path(primeiro_arquivo).read_text(encoding="utf-8")
    segundo_texto = Path(segundo_arquivo).read_text(encoding="utf-8")
    Path(arquivo_saida).write_text(
        primeiro_texto + "\n" + segundo_texto,
        encoding="utf-8",
    )


if __name__ == "__main__":
    primeiro = input("Primeiro arquivo: ").strip()
    segundo = input("Segundo arquivo: ").strip()
    saida = input("Arquivo de saida: ").strip()
    concatenar_arquivos(primeiro, segundo, saida)
    print(f"Arquivo criado: {saida}")
