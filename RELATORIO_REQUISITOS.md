# Relatorio de Requisitos

Origem analisada: `C:\Users\user\Downloads\Aula 05 - Arquivos - ToDo List.pdf`.

## Projeto identificado

Projeto de Sistema de Gerenciamento de Tarefas.

## Requisitos do PDF e entrega correspondente

### Projeto ToDo List

| Requisito | Evidencia na entrega |
| --- | --- |
| Cadastrar novas tarefas | Funcao `cadastrar_tarefa` em `tarefas.py` e opcao 1 em `interface.py`. |
| Informar descricao | Campo `descricao` exigido no cadastro. |
| Informar data de vencimento | Campo `data_vencimento` validado no formato `AAAA-MM-DD`. |
| Informar status da tarefa | Campo `status` validado com `pendente`, `em andamento` ou `concluida`. |
| Listar tarefas cadastradas | Funcao `listar_tarefas` e opcao 2 da interface. |
| Filtrar por status | Parametro `status` de `listar_tarefas` e filtro na opcao 2. |
| Filtrar por data de vencimento | Parametro `data_vencimento` de `listar_tarefas` e filtro na opcao 2. |
| Atualizar tarefas | Funcao `atualizar_tarefa` e opcao 3 da interface. |
| Atualizar status | Parametro `status` em `atualizar_tarefa`. |
| Editar descricao | Parametro `descricao` em `atualizar_tarefa`. |
| Editar data de vencimento | Parametro `data_vencimento` em `atualizar_tarefa`. |
| Remover tarefas | Funcao `remover_tarefa` e opcao 4 da interface. |
| Persistencia de dados em arquivos | Modulo `persistencia.py`, usando `tarefas.json`. |
| Interface simples de usuario | Menu de linha de comando em `interface.py` e dashboard em `dashboard.py`. |
| Estrutura em modulos separados | Arquivos `tarefas.py`, `persistencia.py` e `interface.py`. |

### Desafios e exercicios de arquivos

| Requisito | Evidencia na entrega |
| --- | --- |
| Criar `meuarquivo.txt` e escrever tres linhas | `exercicios_arquivos/desafio_meuarquivo.py`. |
| Ler e exibir o conteudo de `meuarquivo.txt` | `exercicios_arquivos/desafio_meuarquivo.py`. |
| Contar palavras de um arquivo de texto | `exercicios_arquivos/contador_palavras.py`. |
| Concatenar dois arquivos de texto em um terceiro | `exercicios_arquivos/concatenador_arquivos.py`. |
| Buscar palavra em arquivo e exibir linhas | `exercicios_arquivos/busca_em_arquivo.py`. |
| Ordenar linhas em ordem alfabetica e salvar resultado | `exercicios_arquivos/ordenador_linhas.py`. |

## Observacao

O PDF cita funcionalidades extras como recorrencia, prioridades e categorias como expansoes possiveis, nao como requisitos obrigatorios. A entrega foca nos requisitos basicos obrigatorios.
