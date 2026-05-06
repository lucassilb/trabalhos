from datetime import datetime

from persistencia import carregar_tarefas, salvar_tarefas
from tarefas import (
    FORMATO_DATA,
    STATUS_VALIDOS,
    atualizar_tarefa,
    cadastrar_tarefa,
    listar_tarefas,
    remover_tarefa,
)


def ler_data(mensagem, obrigatoria=True):
    while True:
        valor = input(mensagem).strip()
        if not valor and not obrigatoria:
            return None
        try:
            datetime.strptime(valor, FORMATO_DATA)
            return valor
        except ValueError:
            print("Data invalida. Use o formato AAAA-MM-DD.")


def ler_status(mensagem, obrigatorio=True):
    while True:
        valor = input(mensagem).strip().lower()
        if not valor and not obrigatorio:
            return None
        if valor in STATUS_VALIDOS:
            return valor
        print("Status invalido. Opcoes: pendente, em andamento, concluida.")


def ler_id():
    while True:
        try:
            return int(input("ID da tarefa: ").strip())
        except ValueError:
            print("Digite um numero inteiro para o ID.")


def imprimir_tarefas(tarefas_filtradas):
    if not tarefas_filtradas:
        print("Nenhuma tarefa encontrada.")
        return

    print("\nID | Vencimento | Status        | Descricao")
    print("-" * 70)
    for tarefa in tarefas_filtradas:
        print(
            f"{tarefa['id']:>2} | {tarefa['data_vencimento']} | "
            f"{tarefa['status']:<13} | {tarefa['descricao']}"
        )


def menu():
    tarefas = carregar_tarefas()

    while True:
        print("\nSistema de Gerenciamento de Tarefas")
        print("1. Cadastrar tarefa")
        print("2. Listar tarefas")
        print("3. Atualizar tarefa")
        print("4. Remover tarefa")
        print("5. Sair")

        opcao = input("Escolha uma opcao: ").strip()

        try:
            if opcao == "1":
                descricao = input("Descricao: ")
                data_vencimento = ler_data("Data de vencimento (AAAA-MM-DD): ")
                status = ler_status(
                    "Status (pendente/em andamento/concluida): "
                )
                tarefa = cadastrar_tarefa(
                    tarefas,
                    descricao,
                    data_vencimento or "",
                    status or "pendente",
                )
                salvar_tarefas(tarefas)
                print(f"Tarefa cadastrada com ID {tarefa['id']}.")

            elif opcao == "2":
                print("Filtros opcionais. Pressione Enter para ignorar.")
                status = ler_status(
                    "Filtrar por status (pendente/em andamento/concluida): ",
                    obrigatorio=False,
                )
                data_vencimento = ler_data(
                    "Filtrar por data de vencimento (AAAA-MM-DD): ",
                    obrigatoria=False,
                )
                imprimir_tarefas(listar_tarefas(tarefas, status, data_vencimento))

            elif opcao == "3":
                tarefa_id = ler_id()
                print("Novos dados. Pressione Enter para manter o valor atual.")
                descricao = input("Nova descricao: ").strip() or None
                data_vencimento = ler_data(
                    "Nova data de vencimento (AAAA-MM-DD): ",
                    obrigatoria=False,
                )
                status = ler_status(
                    "Novo status (pendente/em andamento/concluida): ",
                    obrigatorio=False,
                )
                tarefa = atualizar_tarefa(
                    tarefas,
                    tarefa_id,
                    descricao=descricao,
                    data_vencimento=data_vencimento,
                    status=status,
                )
                salvar_tarefas(tarefas)
                print(f"Tarefa {tarefa['id']} atualizada.")

            elif opcao == "4":
                tarefa_id = ler_id()
                tarefa = remover_tarefa(tarefas, tarefa_id)
                salvar_tarefas(tarefas)
                print(f"Tarefa {tarefa['id']} removida.")

            elif opcao == "5":
                salvar_tarefas(tarefas)
                print("Dados salvos. Encerrando.")
                break

            else:
                print("Opcao invalida.")

        except ValueError as erro:
            print(f"Erro: {erro}")


if __name__ == "__main__":
    menu()
