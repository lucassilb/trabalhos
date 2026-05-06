from tarefas import (
    cadastrar_tarefa,
    listar_tarefas,
    atualizar_tarefa,
    remover_tarefa
)
from persistencia import carregar_tarefas, salvar_tarefas


def mostrar_menu():
    print("\n===== SISTEMA DE GERENCIAMENTO DE TAREFAS =====")
    print("1 - Cadastrar tarefa")
    print("2 - Listar tarefas")
    print("3 - Atualizar tarefa")
    print("4 - Remover tarefa")
    print("5 - Salvar e sair")


def interface():
    tarefas = carregar_tarefas()

    while True:
        mostrar_menu()
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            descricao = input("Descrição da tarefa: ")
            data_vencimento = input("Data de vencimento: ")
            status = input("Status (pendente / em andamento / concluída): ")

            cadastrar_tarefa(tarefas, descricao, data_vencimento, status)
            print("Tarefa cadastrada com sucesso!")

        elif opcao == "2":
            if not tarefas:
                print("Nenhuma tarefa cadastrada.")
            else:
                listar_tarefas(tarefas)
        elif opcao == "3":
            listar_tarefas(tarefas)

            indice = int(input("Digite o número da tarefa que deseja atualizar: ")) - 1
            nova_descricao = input("Nova descrição: ")
            nova_data = input("Nova data de vencimento: ")
            novo_status = input("Novo status: ")

            atualizar_tarefa(tarefas, indice, nova_descricao, nova_data, novo_status)
            print("Tarefa atualizada com sucesso!")

        elif opcao == "4":
            listar_tarefas(tarefas)

            indice = int(input("Digite o número da tarefa que deseja remover: ")) - 1
            remover_tarefa(tarefas, indice)
            print("Tarefa removida com sucesso!")

        elif opcao == "5":
            salvar_tarefas(tarefas)
            print("Tarefas salvas. Saindo do sistema...")
            break

        else:
            print("Opção inválida. Tente novamente.")


if name == "main":
    interface()        