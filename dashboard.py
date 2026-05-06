import html
import webbrowser
from datetime import date
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlencode, urlparse

from persistencia import carregar_tarefas, salvar_tarefas
from tarefas import (
    atualizar_tarefa,
    cadastrar_tarefa,
    listar_tarefas,
    remover_tarefa,
)


PORTA = 8080


def texto(valor):
    return html.escape(str(valor), quote=True)


def contar_status(tarefas, status):
    total = 0
    for tarefa in tarefas:
        if tarefa["status"] == status:
            total += 1
    return total


def classe_status(status):
    if status == "concluida":
        return "concluida"
    if status == "em andamento":
        return "andamento"
    return "pendente"


def montar_cards(tarefas):
    if not tarefas:
        return """
        <div class="empty-state">
            <span class="empty-dot"></span>
            <strong>Nenhuma tarefa encontrada</strong>
            <p>Cadastre uma tarefa no painel lateral para testar a persistencia em arquivo.</p>
        </div>
        """

    cards = ""
    for tarefa in tarefas:
        tarefa_id = texto(tarefa["id"])
        descricao = texto(tarefa["descricao"])
        data_vencimento = texto(tarefa["data_vencimento"])
        status = tarefa["status"]
        status_txt = texto(status)
        form_id = f"editar-{tarefa_id}"

        cards += f"""
        <article class="task-card" draggable="true" data-id="{tarefa_id}">
            <div class="task-head">
                <div>
                    <span class="task-id">TAREFA #{tarefa_id}</span>
                    <h3>{descricao}</h3>
                </div>
                <span class="status-pill {classe_status(status)}">{status_txt}</span>
            </div>

            <form id="{form_id}" method="post" action="/atualizar" class="task-edit">
                <input type="hidden" name="id" value="{tarefa_id}">
                <label>
                    Descricao
                    <input name="descricao" value="{descricao}">
                </label>
                <label>
                    Vencimento
                    <input name="data_vencimento" type="date" value="{data_vencimento}">
                </label>
                <label>
                    Status
                    <select name="status">
                        <option value="pendente" {"selected" if status == "pendente" else ""}>pendente</option>
                        <option value="em andamento" {"selected" if status == "em andamento" else ""}>em andamento</option>
                        <option value="concluida" {"selected" if status == "concluida" else ""}>concluida</option>
                    </select>
                </label>
            </form>

            <div class="task-actions">
                <button form="{form_id}" type="submit">Salvar</button>
                <form method="post" action="/remover">
                    <input type="hidden" name="id" value="{tarefa_id}">
                    <button type="submit" class="danger">Remover</button>
                </form>
            </div>
        </article>
        """

    return cards


def montar_sessoes(tarefas):
    sessoes = ""
    ultimas = tarefas[-8:]
    ultimas.reverse()

    if not ultimas:
        return '<div class="session muted">sem tarefas ainda</div>'

    for tarefa in ultimas:
        sessoes += f"""
        <div class="session">
            <span class="session-dot {classe_status(tarefa["status"])}"></span>
            <span>{texto(tarefa["descricao"])}</span>
            <small>#{texto(tarefa["id"])}</small>
        </div>
        """
    return sessoes


def pagina_html(mensagem="", erro="", filtro_status="", filtro_data=""):
    tarefas = carregar_tarefas()
    status_filtro = filtro_status or None
    data_filtro = filtro_data or None
    data_padrao = date.today().isoformat()

    try:
        if status_filtro or data_filtro:
            tarefas_filtradas = listar_tarefas(tarefas, status_filtro, data_filtro)
        else:
            tarefas_filtradas = tarefas
    except ValueError:
        tarefas_filtradas = tarefas
        erro = "Filtro invalido."

    total = len(tarefas)
    pendentes = contar_status(tarefas, "pendente")
    andamento = contar_status(tarefas, "em andamento")
    concluidas = contar_status(tarefas, "concluida")

    return f"""<!doctype html>
<html lang="pt-br">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Painel de Tarefas</title>
    <style>
        * {{
            box-sizing: border-box;
        }}
        body {{
            margin: 0;
            min-height: 100vh;
            overflow: hidden;
            background: #090d16;
            color: #eef3ff;
            font-family: Inter, "Segoe UI", Arial, sans-serif;
        }}
        body::before {{
            content: "";
            position: fixed;
            inset: 0;
            background:
                radial-gradient(circle at 42% 22%, rgba(123, 160, 224, .10), transparent 22%),
                radial-gradient(circle at 68% 54%, rgba(90, 125, 210, .08), transparent 26%),
                linear-gradient(135deg, #070a11, #0c1220 50%, #111827);
            pointer-events: none;
        }}
        body::after {{
            content: "";
            position: fixed;
            inset: 0;
            background-image:
                radial-gradient(circle at 1px 1px, rgba(126, 141, 178, .32) 1px, transparent 0),
                radial-gradient(circle at 1px 1px, rgba(123, 160, 224, .30) 1.2px, transparent 0);
            background-size: 16px 16px, 210px 210px;
            opacity: .40;
            pointer-events: none;
        }}
        .app-shell {{
            position: relative;
            z-index: 1;
            display: grid;
            grid-template-columns: 188px minmax(0, 1fr) 320px;
            grid-template-rows: 64px minmax(0, 1fr);
            height: 100vh;
        }}
        .sidebar {{
            grid-row: 1 / 3;
            border-right: 1px solid rgba(148, 163, 184, .16);
            background: rgba(13, 19, 33, .86);
            padding: 18px 10px;
        }}
        .brand {{
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 0 10px 20px;
        }}
        .brand-mark {{
            display: grid;
            grid-template-columns: repeat(3, 6px);
            gap: 3px;
        }}
        .brand-mark span {{
            width: 6px;
            height: 6px;
            background: #eef3ff;
        }}
        .brand strong {{
            display: block;
            font-size: 20px;
            letter-spacing: -.04em;
        }}
        .brand small {{
            display: block;
            color: #64708a;
            font-size: 9px;
            font-weight: 800;
            letter-spacing: .14em;
            text-transform: uppercase;
        }}
        .nav-title {{
            color: #64708a;
            font-family: Consolas, monospace;
            font-size: 11px;
            font-weight: 800;
            letter-spacing: .12em;
            text-transform: uppercase;
            padding: 10px;
        }}
        .project-row, .session {{
            height: 34px;
            display: flex;
            align-items: center;
            gap: 8px;
            border-radius: 6px;
            padding: 0 10px;
            color: #c9d4ec;
            font-size: 13px;
        }}
        .project-row.active, .session:hover {{
            background: rgba(123, 160, 224, .12);
            color: #ffffff;
        }}
        .project-dot, .session-dot {{
            width: 7px;
            height: 7px;
            border-radius: 999px;
            background: #7ba0e0;
        }}
        .session-dot.andamento {{
            background: #7ba0e0;
        }}
        .session-dot.pendente {{
            background: #c87a4f;
        }}
        .session-dot.concluida {{
            background: #9db089;
        }}
        .session small {{
            margin-left: auto;
            color: #64708a;
            font-family: Consolas, monospace;
            font-size: 11px;
        }}
        .muted {{
            color: #64708a;
        }}
        .topbar {{
            grid-column: 2 / 4;
            border-bottom: 1px solid rgba(148, 163, 184, .16);
            background: rgba(8, 12, 21, .78);
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 16px;
            padding: 0 18px 0 22px;
            backdrop-filter: blur(16px);
        }}
        .topbar-left {{
            display: flex;
            align-items: center;
            gap: 12px;
        }}
        .workspace-title {{
            font-size: 12px;
            font-family: Consolas, monospace;
            color: #64708a;
            text-transform: uppercase;
            letter-spacing: .14em;
        }}
        .chip-row {{
            display: flex;
            align-items: center;
            gap: 8px;
            flex-wrap: wrap;
            justify-content: flex-end;
        }}
        .chip {{
            height: 32px;
            border: 1px solid rgba(148, 163, 184, .16);
            background: rgba(26, 34, 56, .92);
            color: #d8e2fb;
            border-radius: 999px;
            padding: 0 13px;
            display: inline-flex;
            align-items: center;
            font-family: Consolas, monospace;
            font-size: 11px;
            font-weight: 800;
        }}
        .canvas {{
            position: relative;
            min-width: 0;
            overflow: auto;
            border-right: 1px solid rgba(148, 163, 184, .16);
        }}
        .canvas-inner {{
            min-height: 100%;
            padding: 42px;
        }}
        .hero-card {{
            width: min(760px, 100%);
            margin: 70px auto 24px;
            border: 1px solid rgba(123, 160, 224, .30);
            border-radius: 14px;
            background: rgba(7, 11, 20, .76);
            box-shadow: 0 28px 90px rgba(0, 0, 0, .38);
            padding: 24px;
        }}
        .agent-label {{
            color: #7ba0e0;
            font-family: Consolas, monospace;
            font-size: 11px;
            font-weight: 900;
            letter-spacing: .16em;
            text-transform: uppercase;
        }}
        .hero-card h1 {{
            margin: 8px 0 10px;
            font-family: Consolas, monospace;
            font-size: 30px;
            line-height: 1.1;
            letter-spacing: -.02em;
            text-transform: uppercase;
        }}
        .hero-card p {{
            color: #b7bccb;
            margin: 0 0 18px;
            max-width: 560px;
        }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 10px;
        }}
        .stat {{
            border: 1px solid rgba(148, 163, 184, .14);
            border-radius: 10px;
            background: rgba(18, 24, 40, .76);
            padding: 12px;
        }}
        .stat strong {{
            display: block;
            font-size: 24px;
        }}
        .stat span {{
            display: block;
            color: #7a8194;
            font-family: Consolas, monospace;
            font-size: 10px;
            text-transform: uppercase;
            letter-spacing: .12em;
        }}
        .task-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(310px, 1fr));
            gap: 14px;
            max-width: 980px;
            margin: 0 auto;
        }}
        .task-card, .panel {{
            border: 1px solid rgba(148, 163, 184, .16);
            border-radius: 12px;
            background: rgba(10, 15, 27, .80);
            box-shadow: 0 18px 60px rgba(0, 0, 0, .30);
            backdrop-filter: blur(14px);
        }}
        .task-card {{
            padding: 16px;
            cursor: grab;
            transition: border-color 160ms ease, opacity 160ms ease, transform 160ms ease;
        }}
        .task-card:active {{
            cursor: grabbing;
        }}
        .task-card.arrastando {{
            opacity: .45;
            transform: scale(.99);
        }}
        .task-card.destino {{
            border-color: rgba(123, 160, 224, .72);
        }}
        .task-head {{
            display: flex;
            justify-content: space-between;
            gap: 12px;
            margin-bottom: 14px;
        }}
        .task-id {{
            color: #7ba0e0;
            font-family: Consolas, monospace;
            font-size: 10px;
            font-weight: 900;
            letter-spacing: .14em;
        }}
        h3 {{
            margin: 5px 0 0;
            font-size: 17px;
            line-height: 1.25;
        }}
        .status-pill {{
            align-self: flex-start;
            border-radius: 999px;
            padding: 6px 8px;
            font-family: Consolas, monospace;
            font-size: 10px;
            font-weight: 900;
            text-transform: uppercase;
            white-space: nowrap;
        }}
        .status-pill.andamento {{
            color: #a8c5f4;
            background: rgba(123, 160, 224, .12);
            border: 1px solid rgba(123, 160, 224, .26);
        }}
        .status-pill.pendente {{
            color: #f4b28b;
            background: rgba(200, 122, 79, .12);
            border: 1px solid rgba(200, 122, 79, .24);
        }}
        .status-pill.concluida {{
            color: #bde6a6;
            background: rgba(157, 176, 137, .12);
            border: 1px solid rgba(157, 176, 137, .24);
        }}
        label {{
            display: block;
            color: #7a8194;
            font-family: Consolas, monospace;
            font-size: 10px;
            font-weight: 900;
            letter-spacing: .10em;
            text-transform: uppercase;
            margin-bottom: 10px;
        }}
        input, select {{
            width: 100%;
            height: 40px;
            margin-top: 6px;
            border: 1px solid rgba(148, 163, 184, .18);
            border-radius: 8px;
            background: rgba(5, 8, 15, .82);
            color: #eef3ff;
            padding: 0 11px;
            outline: none;
        }}
        input:focus, select:focus {{
            border-color: rgba(123, 160, 224, .70);
            box-shadow: 0 0 0 3px rgba(123, 160, 224, .12);
        }}
        input::placeholder {{
            color: #58627a;
        }}
        .task-edit {{
            display: grid;
            gap: 4px;
        }}
        .task-actions {{
            display: flex;
            gap: 8px;
            justify-content: flex-end;
            margin-top: 12px;
        }}
        button, .button-link {{
            height: 38px;
            border: 0;
            border-radius: 8px;
            padding: 0 14px;
            background: #7ba0e0;
            color: #07101f;
            font-size: 11px;
            font-weight: 900;
            letter-spacing: .08em;
            text-transform: uppercase;
            cursor: pointer;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            justify-content: center;
        }}
        .primary {{
            background: #7ba0e0;
            color: #07101f;
        }}
        .danger {{
            background: rgba(214, 17, 43, .86);
            color: white;
        }}
        .ghost {{
            background: rgba(123, 160, 224, .12);
            color: #d8e2fb;
        }}
        .right-panel {{
            display: flex;
            flex-direction: column;
            min-width: 0;
            background: rgba(8, 12, 21, .72);
        }}
        .panel {{
            margin: 14px;
            padding: 16px;
        }}
        .panel h2 {{
            margin: 0 0 14px;
            color: #eef3ff;
            font-family: Consolas, monospace;
            font-size: 13px;
            text-transform: uppercase;
            letter-spacing: .12em;
        }}
        .side-form {{
            display: grid;
            gap: 8px;
        }}
        .filters {{
            display: grid;
            grid-template-columns: 1fr;
            gap: 8px;
        }}
        .filter-actions {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 8px;
            margin-top: 4px;
        }}
        .message {{
            margin: 14px;
            border-radius: 12px;
            border: 1px solid rgba(123, 160, 224, .26);
            background: rgba(123, 160, 224, .10);
            color: #d8e2fb;
            padding: 12px;
            font-size: 13px;
        }}
        .error {{
            margin: 14px;
            border-radius: 12px;
            border: 1px solid rgba(214, 17, 43, .34);
            background: rgba(214, 17, 43, .12);
            color: #ffc8cf;
            padding: 12px;
            font-size: 13px;
        }}
        .empty-state {{
            grid-column: 1 / -1;
            width: min(430px, 100%);
            margin: 20px auto;
            text-align: center;
            border: 1px dashed rgba(148, 163, 184, .22);
            border-radius: 14px;
            background: rgba(10, 15, 27, .62);
            padding: 28px;
            color: #b7bccb;
        }}
        .empty-state strong {{
            display: block;
            color: #eef3ff;
            margin-bottom: 8px;
        }}
        .empty-dot {{
            display: block;
            width: 9px;
            height: 9px;
            border-radius: 999px;
            background: #7ba0e0;
            margin: 0 auto 14px;
            box-shadow: 0 0 18px rgba(123, 160, 224, .38);
        }}
        @media (max-width: 1100px) {{
            .app-shell {{
                grid-template-columns: 160px minmax(0, 1fr);
            }}
            .right-panel {{
                display: none;
            }}
            .topbar {{
                grid-column: 2;
            }}
        }}
        @media (max-width: 760px) {{
            body {{
                overflow: auto;
            }}
            .app-shell {{
                display: block;
                height: auto;
            }}
            .sidebar, .topbar {{
                display: none;
            }}
            .canvas {{
                min-height: 100vh;
            }}
            .canvas-inner {{
                padding: 20px;
            }}
            .hero-card {{
                margin: 20px auto;
            }}
            .stats {{
                grid-template-columns: repeat(2, 1fr);
            }}
        }}
    </style>
</head>
<body>
    <div class="app-shell">
        <aside class="sidebar">
            <div class="brand">
                <span class="brand-mark">
                    <span></span><span></span><span></span>
                    <span></span><span></span><span></span>
                    <span></span><span></span><span></span>
                </span>
                <div>
                    <strong>simple</strong>
                    <small>painel de tarefas</small>
                </div>
            </div>
            <div class="nav-title">Projeto</div>
            <div class="project-row active"><span class="project-dot"></span> CP ToDo List</div>
            <div class="nav-title">Recentes</div>
            {montar_sessoes(tarefas)}
        </aside>

        <header class="topbar">
            <div class="topbar-left">
                <span class="workspace-title">painel de tarefas</span>
            </div>
            <div class="chip-row">
                <span class="chip">arquivo json</span>
                <span class="chip">python stdlib</span>
                <span class="chip">modo escuro</span>
            </div>
        </header>

        <main class="canvas">
            <div class="canvas-inner">
                <section class="hero-card">
                    <span class="agent-label">PAINEL 01</span>
                    <h1>Controle de tarefas</h1>
                    <p>Cadastre, filtre, atualize, remova e arraste os cards para organizar a ordem das tarefas.</p>
                    <div class="stats">
                        <div class="stat"><strong>{total}</strong><span>Total</span></div>
                        <div class="stat"><strong>{pendentes}</strong><span>Pendentes</span></div>
                        <div class="stat"><strong>{andamento}</strong><span>Em andamento</span></div>
                        <div class="stat"><strong>{concluidas}</strong><span>Concluidas</span></div>
                    </div>
                </section>

                <section class="task-grid">
                    {montar_cards(tarefas_filtradas)}
                </section>
            </div>
        </main>

        <aside class="right-panel">
            {"<div class='message'>" + texto(mensagem) + "</div>" if mensagem else ""}
            {"<div class='error'>" + texto(erro) + "</div>" if erro else ""}

            <section class="panel">
                <h2>Cadastrar</h2>
                <form method="post" action="/cadastrar" class="side-form">
                    <label>Descricao
                        <input name="descricao" placeholder="descreva a tarefa..." required>
                    </label>
                    <label>Vencimento
                        <input name="data_vencimento" type="date" value="{data_padrao}" required>
                    </label>
                    <label>Status
                        <select name="status">
                            <option value="pendente">pendente</option>
                            <option value="em andamento">em andamento</option>
                            <option value="concluida">concluida</option>
                        </select>
                    </label>
                    <button class="primary" type="submit">Criar tarefa</button>
                </form>
            </section>

            <section class="panel">
                <h2>Filtros</h2>
                <form method="get" action="/" class="filters">
                    <label>Status
                        <select name="status">
                            <option value="">todos</option>
                            <option value="pendente" {"selected" if filtro_status == "pendente" else ""}>pendente</option>
                            <option value="em andamento" {"selected" if filtro_status == "em andamento" else ""}>em andamento</option>
                            <option value="concluida" {"selected" if filtro_status == "concluida" else ""}>concluida</option>
                        </select>
                    </label>
                    <label>Data
                        <input name="data" type="date" value="{texto(filtro_data)}">
                    </label>
                    <div class="filter-actions">
                        <button type="submit">Filtrar</button>
                        <a class="button-link ghost" href="/">Limpar</a>
                    </div>
                </form>
            </section>
        </aside>
    </div>
    <script>
        const grade = document.querySelector(".task-grid");
        let cardArrastado = null;

        function cardsOrdenados() {{
            return [...document.querySelectorAll(".task-card")]
                .map((card) => card.dataset.id)
                .filter(Boolean);
        }}

        function salvarOrdem() {{
            const ids = cardsOrdenados();
            if (!ids.length) return;

            fetch("/reordenar", {{
                method: "POST",
                headers: {{
                    "Content-Type": "application/x-www-form-urlencoded"
                }},
                body: "ids=" + encodeURIComponent(ids.join(","))
            }}).catch(() => {{}});
        }}

        if (grade) {{
            grade.addEventListener("dragstart", (event) => {{
                const card = event.target.closest(".task-card");
                if (!card) return;
                cardArrastado = card;
                card.classList.add("arrastando");
                event.dataTransfer.effectAllowed = "move";
            }});

            grade.addEventListener("dragend", () => {{
                document.querySelectorAll(".task-card").forEach((card) => {{
                    card.classList.remove("arrastando", "destino");
                }});
                cardArrastado = null;
                salvarOrdem();
            }});

            grade.addEventListener("dragover", (event) => {{
                event.preventDefault();
                const destino = event.target.closest(".task-card");
                if (!destino || destino === cardArrastado) return;

                document.querySelectorAll(".task-card").forEach((card) => {{
                    card.classList.remove("destino");
                }});
                destino.classList.add("destino");

                const box = destino.getBoundingClientRect();
                const depois = event.clientY > box.top + box.height / 2;
                if (depois) {{
                    destino.after(cardArrastado);
                }} else {{
                    destino.before(cardArrastado);
                }}
            }});
        }}
    </script>
</body>
</html>"""


class DashboardHandler(BaseHTTPRequestHandler):
    def enviar_html(self, conteudo):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(conteudo.encode("utf-8"))

    def redirecionar(self, mensagem=""):
        destino = "/"
        if mensagem:
            destino = "/?" + urlencode({"mensagem": mensagem})
        self.send_response(303)
        self.send_header("Location", destino)
        self.end_headers()

    def ler_post(self):
        tamanho = int(self.headers.get("Content-Length", 0))
        dados = self.rfile.read(tamanho).decode("utf-8")
        return parse_qs(dados)

    def do_GET(self):
        consulta = parse_qs(urlparse(self.path).query)
        status = consulta.get("status", [""])[0]
        data = consulta.get("data", [""])[0]
        mensagem = consulta.get("mensagem", [""])[0]
        self.enviar_html(
            pagina_html(mensagem=mensagem, filtro_status=status, filtro_data=data)
        )

    def do_POST(self):
        dados = self.ler_post()
        tarefas = carregar_tarefas()

        try:
            if self.path == "/cadastrar":
                cadastrar_tarefa(
                    tarefas,
                    dados.get("descricao", [""])[0],
                    dados.get("data_vencimento", [""])[0],
                    dados.get("status", ["pendente"])[0],
                )
                salvar_tarefas(tarefas)
                self.redirecionar("Tarefa cadastrada.")

            elif self.path == "/atualizar":
                atualizar_tarefa(
                    tarefas,
                    int(dados.get("id", ["0"])[0]),
                    dados.get("descricao", [""])[0],
                    dados.get("data_vencimento", [""])[0],
                    dados.get("status", [""])[0],
                )
                salvar_tarefas(tarefas)
                self.redirecionar("Tarefa atualizada.")

            elif self.path == "/remover":
                remover_tarefa(tarefas, int(dados.get("id", ["0"])[0]))
                salvar_tarefas(tarefas)
                self.redirecionar("Tarefa removida.")

            elif self.path == "/reordenar":
                ids_texto = dados.get("ids", [""])[0]
                ids = []
                for item in ids_texto.split(","):
                    if item.strip().isdigit():
                        ids.append(int(item.strip()))

                ordenadas = []
                for tarefa_id in ids:
                    for tarefa in tarefas:
                        if int(tarefa["id"]) == tarefa_id and tarefa not in ordenadas:
                            ordenadas.append(tarefa)

                for tarefa in tarefas:
                    if tarefa not in ordenadas:
                        ordenadas.append(tarefa)

                salvar_tarefas(ordenadas)
                self.enviar_html("ok")

            else:
                self.redirecionar()

        except ValueError as erro:
            self.enviar_html(pagina_html(erro=str(erro)))


def iniciar_dashboard():
    endereco = ("localhost", PORTA)
    servidor = ThreadingHTTPServer(endereco, DashboardHandler)
    url = f"http://localhost:{PORTA}"
    print(f"Dashboard aberto em {url}")
    webbrowser.open(url)
    servidor.serve_forever()


if __name__ == "__main__":
    iniciar_dashboard()
