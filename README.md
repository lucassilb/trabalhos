# CP ToDo List

Este projeto Ã© uma ToDo List feita em Python para praticar manipulaÃ§Ã£o de
arquivos externos. A ideia Ã© simples: cadastrar tarefas, salvar tudo em arquivo e
conseguir consultar, editar ou remover depois.

O projeto foi montado a partir da aula **Aula 05 - Arquivos - ToDo List**.

## Demo online

Enquanto o computador estiver ligado e o tÃºnel estiver rodando, dÃ¡ para testar
pelo link:

```text
https://prev-valium-female-welfare.trycloudflare.com
```

Esse link usa um tÃºnel rÃ¡pido do Cloudflare. Ele Ã© Ã³timo para demonstraÃ§Ã£o, mas
nÃ£o Ã© um deploy permanente. Se o terminal ou o processo do tÃºnel for fechado, o
link pode parar de funcionar.

## Como testar no computador

O jeito mais fÃ¡cil Ã© abrir o dashboard visual:

```text
abrir_dashboard.bat
```

TambÃ©m dÃ¡ para rodar direto pelo PowerShell:

```powershell
python dashboard.py
```

Depois Ã© sÃ³ acessar:

```text
http://localhost:8080
```

## VersÃ£o pelo terminal

AlÃ©m do dashboard, tambÃ©m existe uma versÃ£o de menu no terminal:

```powershell
python interface.py
```

## O que o sistema faz

- Cadastra tarefas com descriÃ§Ã£o, data de vencimento e status.
- Lista todas as tarefas cadastradas.
- Filtra tarefas por status.
- Filtra tarefas por data de vencimento.
- Atualiza descriÃ§Ã£o, data e status.
- Remove tarefas.
- Permite arrastar os cards no dashboard para reorganizar a ordem.
- Salva os dados em `tarefas.json`, para nÃ£o perder as tarefas ao fechar o programa.

## Status aceitos

Use um destes trÃªs status:

- `pendente`
- `em andamento`
- `concluida`

## Formato da data

No cÃ³digo, a data Ã© salva no formato:

```text
AAAA-MM-DD
```

Exemplo:

```text
2026-05-10
```

No dashboard, o prÃ³prio campo de data do navegador ajuda a preencher no formato correto.

## Arquivos principais

- `dashboard.py`: dashboard visual no navegador.
- `abrir_dashboard.bat`: atalho para abrir o dashboard no Windows.
- `interface.py`: versÃ£o em linha de comando.
- `tarefas.py`: funÃ§Ãµes para cadastrar, listar, atualizar e remover tarefas.
- `persistencia.py`: funÃ§Ãµes para carregar e salvar as tarefas em arquivo.
- `tarefas.json`: arquivo onde os dados ficam salvos.
- `RELATORIO_REQUISITOS.md`: resumo dos requisitos do PDF e onde eles foram atendidos.
- `exercicios_arquivos/`: exercÃ­cios extras de arquivos citados na aula.

## ObservaÃ§Ã£o

O dashboard tem um visual mais moderno para facilitar a demonstraÃ§Ã£o, mas o
funcionamento principal continua sendo o que a atividade pediu: usar Python,
arquivos externos e funÃ§Ãµes separadas para organizar o sistema.

