from datetime import datetime


STATUS_VALIDOS = ["pendente", "em andamento", "concluida"]
FORMATO_DATA = "%Y-%m-%d"


def validar_data(data_vencimento):
    datetime.strptime(data_vencimento, FORMATO_DATA)
    return data_vencimento


def validar_status(status):
    status = status.strip().lower()
    if status not in STATUS_VALIDOS:
        raise ValueError(
            "Status invalido. Use: pendente, em andamento ou concluida."
        )
    return status


def proximo_id(tarefas):
    if not tarefas:
        return 1
    maior_id = 0
    for tarefa in tarefas:
        if int(tarefa["id"]) > maior_id:
            maior_id = int(tarefa["id"])
    return maior_id + 1


def cadastrar_tarefa(tarefas, descricao, data_vencimento, status="pendente"):
    descricao = descricao.strip()
    if not descricao:
        raise ValueError("A descricao da tarefa nao pode ficar vazia.")

    tarefa = {
        "id": proximo_id(tarefas),
        "descricao": descricao,
        "data_vencimento": validar_data(data_vencimento),
        "status": validar_status(status),
    }
    tarefas.append(tarefa)
    return tarefa


def listar_tarefas(tarefas, status=None, data_vencimento=None):
    resultado = tarefas

    if status:
        status = validar_status(status)
        filtradas = []
        for tarefa in resultado:
            if tarefa["status"] == status:
                filtradas.append(tarefa)
        resultado = filtradas

    if data_vencimento:
        data_vencimento = validar_data(data_vencimento)
        filtradas = []
        for tarefa in resultado:
            if tarefa["data_vencimento"] == data_vencimento:
                filtradas.append(tarefa)
        resultado = filtradas

    return sorted(resultado, key=lambda tarefa: tarefa["data_vencimento"])


def buscar_tarefa(tarefas, tarefa_id):
    for tarefa in tarefas:
        if int(tarefa["id"]) == tarefa_id:
            return tarefa
    raise ValueError(f"Tarefa com ID {tarefa_id} nao encontrada.")


def atualizar_tarefa(tarefas, tarefa_id, descricao=None, data_vencimento=None, status=None):
    tarefa = buscar_tarefa(tarefas, tarefa_id)

    if descricao is not None and descricao.strip():
        tarefa["descricao"] = descricao.strip()

    if data_vencimento is not None and data_vencimento.strip():
        tarefa["data_vencimento"] = validar_data(data_vencimento.strip())

    if status is not None and status.strip():
        tarefa["status"] = validar_status(status)

    return tarefa


def remover_tarefa(tarefas, tarefa_id):
    tarefa = buscar_tarefa(tarefas, tarefa_id)
    tarefas.remove(tarefa)
    return tarefa
