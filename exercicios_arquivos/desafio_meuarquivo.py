from pathlib import Path


def escrever_e_ler_arquivo(nome: str = "Aluno") -> str:
    caminho = Path("meuarquivo.txt")
    linhas = [
        "Ola, mundo!",
        "Este e um arquivo de texto.",
        f"Criado por {nome}.",
    ]

    with caminho.open("w", encoding="utf-8") as arquivo:
        for linha in linhas:
            arquivo.write(linha + "\n")

    with caminho.open("r", encoding="utf-8") as arquivo:
        return arquivo.read()


if __name__ == "__main__":
    nome = input("Digite seu nome: ").strip() or "Aluno"
    print(escrever_e_ler_arquivo(nome))
