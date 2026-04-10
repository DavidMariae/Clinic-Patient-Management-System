import customtkinter as ctk
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

from config import *
import src.ui.fonts as F
from src.controllers.clinica_controller import controller

POR_PAGINA = ITENS_POR_PAGINA


class PacientesView(ctk.CTkFrame):
    def __init__(self, parent, janela):
        super().__init__(parent, fg_color=FUNDO_APP, corner_radius=0)
        self.janela     = janela
        self._pagina    = 0
        self._pacientes = []
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self._build_topbar()
        self._build_busca()
        self._build_tabela()
        self._carregar()

    # ── Topbar ──────────────────────────────────────────────
    def _build_topbar(self):
        topbar = ctk.CTkFrame(self, fg_color="transparent")
        topbar.grid(row=0, column=0, sticky="ew",
                    padx=PAD_LATERAL, pady=(PAD_TOPO, 0))
        topbar.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            topbar, text="Pacientes",
            font=F.titulo(),
            text_color=TEXTO_TITULO
        ).grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(
            topbar, text="Gerencie os pacientes cadastrados",
            font=F.corpo(),
            text_color=AZUL_MEDIO
        ).grid(row=1, column=0, sticky="w")

        ctk.CTkButton(
            topbar, text="＋  Novo Paciente",
            height=ALTURA_TOPBAR_BTN,
            fg_color=AZUL_ESCURO, text_color=BRANCO,
            hover_color=AZUL_PROFUNDO,
            corner_radius=RAIO_BTN,
            font=F.btn_bold(),
            command=lambda: self.janela.mostrar_frame("novo_paciente")
        ).grid(row=0, column=1, rowspan=2, sticky="e")

    # ── Busca ───────────────────────────────────────────────
    def _build_busca(self):
        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.grid(row=1, column=0, sticky="ew",
                   padx=PAD_LATERAL, pady=(14, 0))
        frame.grid_columnconfigure(0, weight=1)

        # Entry busca
        self._entry_busca = ctk.CTkEntry(
            frame,
            placeholder_text="🔍   Buscar por nome ou telefone...",
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
        self._entry_busca.bind("<KeyRelease>", lambda e: self._pesquisar())

        # Filtro
        self._opt_filtro = ctk.CTkOptionMenu(
            frame,
            values=["Todos os pacientes",
                    "Com atendimento hoje",
                    "Em acompanhamento"],
            width=200, height=ALTURA_INPUT,
            corner_radius=RAIO_INPUT,
            fg_color=BRANCO,
            button_color=AZUL_CLARO,
            button_hover_color=AZUL_PALE,
            text_color=AZUL_ESCURO,
            font=F.corpo(),
            command=lambda _: self._pesquisar()
        )
        self._opt_filtro.grid(row=0, column=1, padx=(0, 12))

        # Badge contador
        self._badge = ctk.CTkLabel(
            frame, text="  0 pacientes  ",
            font=F.badge(),
            text_color=AZUL_ESCURO,
            fg_color=AZUL_PALE,
            corner_radius=RAIO_PILL
        )
        self._badge.grid(row=0, column=2, ipady=6)

    # ── Tabela ───────────────────────────────────────────────
    def _build_tabela(self):
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.grid(row=2, column=0, sticky="nsew",
                       padx=PAD_LATERAL, pady=(14, 0))
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)

        # Scroll
        self._scroll = ctk.CTkScrollableFrame(
            container, fg_color=BRANCO,
            corner_radius=RAIO_CARD,
            border_width=1, border_color=BORDA,
            scrollbar_button_color=AZUL_PALE,
            scrollbar_button_hover_color=AZUL_CLARO
        )
        self._scroll.grid(row=0, column=0, sticky="nsew")
        self._scroll.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

        # Cabeçalho
        colunas = ["Paciente", "Telefone", "E-mail", "Nascimento", "Ações"]
        for col, titulo in enumerate(colunas):
            ctk.CTkLabel(
                self._scroll, text=titulo,
                font=F.tabela_head(),
                text_color=DOURADO_FORTE,
                fg_color=BRANCO,
                anchor="w", corner_radius=0
            ).grid(row=0, column=col, sticky="ew",
                   padx=(16 if col == 0 else 8, 8), pady=10)

        # Frame paginação
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
        fatia  = self._pacientes[inicio: inicio + POR_PAGINA]

        if not fatia:
            ctk.CTkLabel(
                self._scroll,
                text="Nenhum paciente encontrado.",
                font=F.corpo(),
                text_color=TEXTO_MUTED
            ).grid(row=1, column=0, columnspan=5, pady=50)
            self._atualizar_paginacao()
            return

        termo = self._entry_busca.get().strip().lower()

        for i, p in enumerate(fatia):
            bg      = BRANCO if i % 2 == 0 else FUNDO_ALT
            row_num = i + 1
            nome    = p.get("nome", "")

            # ── Paciente (nome + documento) ──
            nome_frame = ctk.CTkFrame(
                self._scroll, fg_color=bg, corner_radius=0)
            nome_frame.grid(row=row_num, column=0, sticky="ew",
                            padx=(16, 8), pady=7)

            # Destaca termo buscado no nome
            nome_display = self._destacar(nome, termo)
            ctk.CTkLabel(
                nome_frame, text=nome_display,
                font=F.tabela_bold(),
                text_color=TEXTO_TITULO, anchor="w"
            ).pack(anchor="w")

            ctk.CTkLabel(
                nome_frame, text=p.get("documento", "—"),
                font=F.tabela_sub(),
                text_color=TEXTO_MUTED, anchor="w"
            ).pack(anchor="w")

            # ── Telefone ──
            tel = p.get("telefone", "—")
            tel_display = self._destacar(tel, termo)
            ctk.CTkLabel(
                self._scroll, text=tel_display,
                font=F.tabela_body(),
                text_color=TEXTO_BODY,
                fg_color=bg, anchor="w"
            ).grid(row=row_num, column=1, sticky="ew", padx=8, pady=7)

            # ── E-mail ──
            ctk.CTkLabel(
                self._scroll,
                text=p.get("email", "—") or "—",
                font=F.tabela_sub(),
                text_color=TEXTO_MUTED,
                fg_color=bg, anchor="w"
            ).grid(row=row_num, column=2, sticky="ew", padx=8, pady=7)

            # ── Nascimento ──
            nasc_raw = p.get("data_nascimento", "—")
            try:
                a, m, d  = nasc_raw.split("-")
                nasc_fmt = f"{d}/{m}/{a}"
            except Exception:
                nasc_fmt = nasc_raw

            ctk.CTkLabel(
                self._scroll, text=nasc_fmt,
                font=F.tabela_body(),
                text_color=TEXTO_BODY,
                fg_color=bg, anchor="w"
            ).grid(row=row_num, column=3, sticky="ew", padx=8, pady=7)

            # ── Ações ──
            acoes = ctk.CTkFrame(
                self._scroll, fg_color=bg, corner_radius=0)
            acoes.grid(row=row_num, column=4, sticky="ew",
                       padx=(8, 16), pady=6)

            ctk.CTkButton(
                acoes, text="Ver",
                width=50, height=ALTURA_BTN_SMALL,
                fg_color=AZUL_PALE, text_color=AZUL_ESCURO,
                hover_color=AZUL_CLARO,
                corner_radius=RAIO_BTN,
                font=F.btn_pequeno(),
                command=lambda pid=p["id"]: self.janela.mostrar_frame(
                    "historico", paciente_id=pid)
            ).pack(side="left", padx=(0, 6))

            ctk.CTkButton(
                acoes, text="✎ Editar",
                width=66, height=ALTURA_BTN_SMALL,
                fg_color=DOURADO_PALE, text_color=AMBER_TEXT,
                hover_color=AMBER_BG,
                corner_radius=RAIO_BTN,
                font=F.btn_pequeno(),
                command=lambda pid=p["id"]: self.janela.mostrar_frame(
                    "editar_paciente", paciente_id=pid)
            ).pack(side="left", padx=(0, 6))

            ctk.CTkButton(
                acoes, text="＋ Atend.",
                width=80, height=ALTURA_BTN_SMALL,
                fg_color=AZUL_ESCURO, text_color=BRANCO,
                hover_color=AZUL_PROFUNDO,
                corner_radius=RAIO_BTN,
                font=F.btn_pequeno(),
                command=lambda pid=p["id"]: self.janela.mostrar_frame(
                    "novo_atendimento", paciente_id=pid)
            ).pack(side="left")

        self._atualizar_paginacao()

    def _destacar(self, texto: str, termo: str) -> str:
        """
        Destaca o termo buscado no texto
        colocando entre colchetes para indicar o match.
        """
        if not termo or termo not in texto.lower():
            return texto
        idx   = texto.lower().index(termo)
        antes = texto[:idx]
        match = texto[idx: idx + len(termo)]
        depois = texto[idx + len(termo):]
        return f"{antes}[{match}]{depois}"

    # ── Paginação ────────────────────────────────────────────
    def _atualizar_paginacao(self):
        for w in self._pag_frame.winfo_children():
            w.destroy()

        total = max(1, -(-len(self._pacientes) // POR_PAGINA))

        def ir(p):
            self._pagina = p
            self._renderizar_pagina()

        # Botão anterior
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

        # Botão próximo
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
        self._pacientes = controller.obter_pacientes()
        self._atualizar_badge()
        self._pagina = 0
        self._renderizar_pagina()

    def _pesquisar(self):
        termo  = self._entry_busca.get().strip()
        filtro = self._opt_filtro.get()
        hoje   = __import__("datetime").date.today().strftime("%Y-%m-%d")

        # Busca por termo
        if termo:
            resultado = controller.buscar_pacientes(termo)
        else:
            resultado = controller.obter_pacientes()

        # Filtro adicional
        if filtro == "Com atendimento hoje":
            ids_hoje = {
                a.get("paciente_id")
                for a in controller.obter_atendimentos_hoje()
            }
            resultado = [p for p in resultado if p["id"] in ids_hoje]

        elif filtro == "Em acompanhamento":
            ids_acomp = {
                a.get("paciente_id")
                for a in controller.obter_todos_atendimentos()
                if "acompanhamento" in a.get("status", "").lower()
            }
            resultado = [p for p in resultado if p["id"] in ids_acomp]

        self._pacientes = resultado
        self._pagina    = 0
        self._atualizar_badge()
        self._renderizar_pagina()

    def _atualizar_badge(self):
        n = len(self._pacientes)
        texto = f"  {n} paciente{'s' if n != 1 else ''}  "
        self._badge.configure(text=texto)
        