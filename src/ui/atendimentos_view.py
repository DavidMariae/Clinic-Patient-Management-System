import customtkinter as ctk
from datetime import date
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

from config import *
import src.ui.fonts as F
from src.controllers.clinica_controller import controller

POR_PAGINA = ITENS_POR_PAGINA


class AtendimentosView(ctk.CTkFrame):
    def __init__(self, parent, janela):
        super().__init__(parent, fg_color=FUNDO_APP, corner_radius=0)
        self.janela         = janela
        self._pagina        = 0
        self._atendimentos  = []
        self._tab_ativa     = "Todos"
        self._pacientes_map = {}
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self._build_topbar()
        self._build_filtros()
        self._build_tabs()
        self._build_tabela()
        self._carregar()

    # ── Topbar ──────────────────────────────────────────────
    def _build_topbar(self):
        topbar = ctk.CTkFrame(self, fg_color="transparent")
        topbar.grid(row=0, column=0, sticky="ew",
                    padx=PAD_LATERAL, pady=(PAD_TOPO, 0))
        topbar.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            topbar, text="Atendimentos",
            font=F.titulo(),
            text_color=TEXTO_TITULO
        ).grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(
            topbar, text="Todos os atendimentos registrados na clínica",
            font=F.corpo(),
            text_color=AZUL_MEDIO
        ).grid(row=1, column=0, sticky="w")

        ctk.CTkButton(
            topbar, text="＋  Novo Atendimento",
            height=ALTURA_TOPBAR_BTN,
            fg_color=AZUL_ESCURO, text_color=BRANCO,
            hover_color=AZUL_PROFUNDO,
            corner_radius=RAIO_BTN,
            font=F.btn_bold(),
            command=lambda: self.janela.mostrar_frame("novo_atendimento")
        ).grid(row=0, column=1, rowspan=2, sticky="e")

    # ── Filtros ─────────────────────────────────────────────
    def _build_filtros(self):
        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.grid(row=1, column=0, sticky="ew",
                   padx=PAD_LATERAL, pady=(14, 0))
        frame.grid_columnconfigure(0, weight=1)

        # Busca
        self._entry_busca = ctk.CTkEntry(
            frame,
            placeholder_text="🔍   Buscar por paciente ou tipo...",
            height=ALTURA_INPUT,
            corner_radius=RAIO_INPUT,
            border_color=AZUL_CLARO,
            border_width=1,
            fg_color=BRANCO,
            text_color=TEXTO_TITULO,
            placeholder_text_color=TEXTO_MUTED,
            font=F.corpo()
        )
        self._entry_busca.grid(row=0, column=0, sticky="ew", padx=(0, 12))
        self._entry_busca.bind("<KeyRelease>", lambda e: self._aplicar_filtros())

        # Filtro tipo
        self._opt_tipo = ctk.CTkOptionMenu(
            frame,
            values=["Todos os tipos", "Consulta", "Retorno",
                    "Exame", "Procedimento", "Urgência"],
            width=170, height=ALTURA_INPUT,
            corner_radius=RAIO_INPUT,
            fg_color=BRANCO,
            button_color=AZUL_CLARO,
            button_hover_color=AZUL_PALE,
            text_color=AZUL_ESCURO,
            font=F.corpo(),
            command=lambda _: self._aplicar_filtros()
        )
        self._opt_tipo.grid(row=0, column=1, padx=(0, 12))

        # Badge
        self._badge = ctk.CTkLabel(
            frame, text="  0 atendimentos  ",
            font=F.badge(),
            text_color=AZUL_ESCURO,
            fg_color=AZUL_PALE,
            corner_radius=RAIO_PILL
        )
        self._badge.grid(row=0, column=2, ipady=6)

    # ── Tabs ────────────────────────────────────────────────
    def _build_tabs(self):
        self._tabs_frame = ctk.CTkFrame(self, fg_color="transparent")
        self._tabs_frame.grid(row=2, column=0, sticky="ew",
                              padx=PAD_LATERAL, pady=(10, 0))
        self._tab_btns = {}

        tabs = [
            ("Todos",             BRANCO,   TEXTO_MUTED, AZUL_CLARO),
            ("Realizados",        VERDE_BG, VERDE_TEXT,  VERDE_TEXT),
            ("Em acompanhamento", AMBER_BG, AMBER_TEXT,  AMBER_TEXT),
            ("Hoje",              BRANCO,   TEXTO_MUTED, AZUL_CLARO),
        ]

        for chave, bg, fg, borda in tabs:
            btn = ctk.CTkButton(
                self._tabs_frame,
                text=chave,
                height=30,
                fg_color=bg,
                text_color=fg,
                border_width=1,
                border_color=borda,
                hover_color=AZUL_PALE,
                corner_radius=RAIO_PILL,
                font=F.pequena(),
                command=lambda c=chave: self._set_tab(c)
            )
            btn.pack(side="left", padx=(0, 8))
            self._tab_btns[chave] = btn

        self._set_tab("Todos", renderizar=False)

    def _set_tab(self, chave, renderizar=True):
        self._tab_ativa = chave
        for k, btn in self._tab_btns.items():
            if k == chave:
                btn.configure(
                    fg_color=AZUL_ESCURO,
                    text_color=BRANCO,
                    border_color=AZUL_ESCURO
                )
            else:
                if k == "Realizados":
                    btn.configure(fg_color=VERDE_BG,
                                  text_color=VERDE_TEXT,
                                  border_color=VERDE_TEXT)
                elif k == "Em acompanhamento":
                    btn.configure(fg_color=AMBER_BG,
                                  text_color=AMBER_TEXT,
                                  border_color=AMBER_TEXT)
                else:
                    btn.configure(fg_color=BRANCO,
                                  text_color=TEXTO_MUTED,
                                  border_color=AZUL_CLARO)
        if renderizar:
            self._aplicar_filtros()

    # ── Tabela ───────────────────────────────────────────────
    def _build_tabela(self):
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.grid(row=3, column=0, sticky="nsew",
                       padx=PAD_LATERAL, pady=(12, 0))
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)

        self._scroll = ctk.CTkScrollableFrame(
            container, fg_color=BRANCO,
            corner_radius=RAIO_CARD,
            border_width=1, border_color=BORDA,
            scrollbar_button_color=AZUL_PALE,
            scrollbar_button_hover_color=AZUL_CLARO
        )
        self._scroll.grid(row=0, column=0, sticky="nsew")
        self._scroll.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)

        # Cabeçalho
        colunas = ["Tipo", "Paciente", "Data",
                   "Observações", "Status", "Ação"]
        for col, titulo in enumerate(colunas):
            ctk.CTkLabel(
                self._scroll, text=titulo,
                font=F.tabela_head(),
                text_color=DOURADO_FORTE,
                fg_color=BRANCO,
                anchor="w", corner_radius=0
            ).grid(row=0, column=col, sticky="ew",
                   padx=(16 if col == 0 else 8, 8), pady=10)

        # Paginação
        self._pag_frame = ctk.CTkFrame(container, fg_color="transparent")
        self._pag_frame.grid(row=1, column=0, sticky="e", pady=(10, 20))

    # ── Renderização ────────────────────────────────────────
    def _limpar_linhas(self):
        for w in self._scroll.winfo_children():
            info = w.grid_info()
            if info and int(info.get("row", 0)) > 0:
                w.destroy()

    def _renderizar_pagina(self):
        self._limpar_linhas()

        inicio = self._pagina * POR_PAGINA
        fatia  = self._atendimentos[inicio: inicio + POR_PAGINA]

        if not fatia:
            ctk.CTkLabel(
                self._scroll,
                text="Nenhum atendimento encontrado.",
                font=F.corpo(),
                text_color=TEXTO_MUTED
            ).grid(row=1, column=0, columnspan=6, pady=50)
            self._atualizar_paginacao()
            return

        for i, atend in enumerate(fatia):
            bg      = BRANCO if i % 2 == 0 else FUNDO_ALT
            row_num = i + 1

            paciente = self._pacientes_map.get(atend.get("paciente_id"), {})
            nome_pac = paciente.get("nome", "—")
            doc_pac  = paciente.get("documento", "")
            status   = atend.get("status", "")
            is_real  = "acompanhamento" not in status.lower()
            pill_bg  = VERDE_BG   if is_real else AMBER_BG
            pill_fg  = VERDE_TEXT if is_real else AMBER_TEXT

            # Tipo
            ctk.CTkLabel(
                self._scroll,
                text=atend.get("tipo", "—"),
                font=F.tabela_bold(),
                text_color=TEXTO_TITULO,
                fg_color=bg, anchor="w"
            ).grid(row=row_num, column=0, sticky="ew",
                   padx=(16, 8), pady=8)

            # Paciente
            pac_frame = ctk.CTkFrame(
                self._scroll, fg_color=bg, corner_radius=0)
            pac_frame.grid(row=row_num, column=1,
                           sticky="ew", padx=8, pady=6)
            ctk.CTkLabel(
                pac_frame, text=nome_pac,
                font=F.tabela_body(),
                text_color=TEXTO_BODY, anchor="w"
            ).pack(anchor="w")
            ctk.CTkLabel(
                pac_frame, text=doc_pac,
                font=F.tabela_sub(),
                text_color=TEXTO_MUTED, anchor="w"
            ).pack(anchor="w")

            # Data
            data_raw = atend.get("data", "")
            try:
                a, m, d  = data_raw.split("-")
                data_fmt = f"{d}/{m}/{a}"
            except Exception:
                data_fmt = data_raw

            ctk.CTkLabel(
                self._scroll, text=data_fmt,
                font=F.tabela_body(),
                text_color=TEXTO_BODY,
                fg_color=bg, anchor="w"
            ).grid(row=row_num, column=2, sticky="ew", padx=8, pady=8)

            # Observações truncadas
            obs       = atend.get("observacoes", "").strip()
            obs_curta = (obs[:30] + "...") if len(obs) > 30 else (obs or "—")
            ctk.CTkLabel(
                self._scroll, text=obs_curta,
                font=F.tabela_sub(),
                text_color=TEXTO_MUTED,
                fg_color=bg, anchor="w"
            ).grid(row=row_num, column=3, sticky="ew", padx=8, pady=8)

            # Status pill
            pill_frame = ctk.CTkFrame(
                self._scroll, fg_color=bg, corner_radius=0)
            pill_frame.grid(row=row_num, column=4,
                            sticky="ew", padx=8, pady=6)
            ctk.CTkLabel(
                pill_frame,
                text=f"  {status}  ",
                font=F.pill(),
                text_color=pill_fg,
                fg_color=pill_bg,
                corner_radius=RAIO_PILL
            ).pack(anchor="w")

            # Botão histórico
            ctk.CTkButton(
                self._scroll, text="Histórico",
                width=80, height=ALTURA_BTN_SMALL,
                fg_color=AZUL_PALE, text_color=AZUL_ESCURO,
                hover_color=AZUL_CLARO,
                corner_radius=RAIO_BTN,
                font=F.btn_pequeno(),
                command=lambda pid=paciente.get("id"): self._ver_historico(pid)
            ).grid(row=row_num, column=5, sticky="w",
                   padx=(8, 16), pady=6)

        self._atualizar_paginacao()

    # ── Paginação ────────────────────────────────────────────
    def _atualizar_paginacao(self):
        for w in self._pag_frame.winfo_children():
            w.destroy()

        total = max(1, -(-len(self._atendimentos) // POR_PAGINA))

        def ir(p):
            self._pagina = p
            self._renderizar_pagina()

        ctk.CTkButton(
            self._pag_frame, text="‹",
            width=32, height=32,
            fg_color=BRANCO, text_color=AZUL_ESCURO,
            border_width=1, border_color=AZUL_CLARO,
            hover_color=AZUL_PALE, corner_radius=RAIO_BTN,
            font=F.corpo_bold(),
            command=lambda: ir(max(0, self._pagina - 1))
        ).pack(side="left", padx=3)

        for p in range(total):
            ativo = p == self._pagina
            ctk.CTkButton(
                self._pag_frame, text=str(p + 1),
                width=32, height=32,
                fg_color=AZUL_ESCURO if ativo else BRANCO,
                text_color=BRANCO if ativo else AZUL_ESCURO,
                border_width=1, border_color=AZUL_CLARO,
                hover_color=AZUL_PALE, corner_radius=RAIO_BTN,
                font=F.corpo_bold(),
                command=lambda pg=p: ir(pg)
            ).pack(side="left", padx=3)

        ctk.CTkButton(
            self._pag_frame, text="›",
            width=32, height=32,
            fg_color=BRANCO, text_color=AZUL_ESCURO,
            border_width=1, border_color=AZUL_CLARO,
            hover_color=AZUL_PALE, corner_radius=RAIO_BTN,
            font=F.corpo_bold(),
            command=lambda: ir(min(total - 1, self._pagina + 1))
        ).pack(side="left", padx=3)

    # ── Lógica ──────────────────────────────────────────────
    def _carregar(self):
        self._pacientes_map = {
            p["id"]: p for p in controller.obter_pacientes()
        }
        self._aplicar_filtros()

    def _aplicar_filtros(self):
        todos  = controller.obter_todos_atendimentos()
        termo  = self._entry_busca.get().strip().lower()
        tipo   = self._opt_tipo.get()
        tab    = self._tab_ativa
        hoje   = date.today().strftime("%Y-%m-%d")

        resultado = []
        for a in todos:
            paciente = self._pacientes_map.get(a.get("paciente_id"), {})
            nome_pac = paciente.get("nome", "").lower()
            tipo_a   = a.get("tipo", "")
            status   = a.get("status", "")
            data_a   = a.get("data", "")

            # Filtro busca
            if termo and termo not in nome_pac \
                    and termo not in tipo_a.lower():
                continue

            # Filtro tipo
            if tipo != "Todos os tipos" and tipo_a != tipo:
                continue

            # Filtro tab
            if tab == "Realizados" \
                    and "acompanhamento" in status.lower():
                continue
            if tab == "Em acompanhamento" \
                    and "acompanhamento" not in status.lower():
                continue
            if tab == "Hoje" and data_a != hoje:
                continue

            resultado.append(a)

        self._atendimentos = resultado
        self._pagina       = 0
        n                  = len(resultado)
        self._badge.configure(
            text=f"  {n} atendimento{'s' if n != 1 else ''}  "
        )
        self._renderizar_pagina()

    def _ver_historico(self, paciente_id):
        if paciente_id:
            self.janela.mostrar_frame(
                "historico", paciente_id=paciente_id)