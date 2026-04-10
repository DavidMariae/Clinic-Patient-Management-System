import customtkinter as ctk
from datetime import date
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

from config import *
import src.ui.fonts as F
from src.controllers.clinica_controller import controller


class DashboardView(ctk.CTkFrame):
    def __init__(self, parent, janela):
        super().__init__(parent, fg_color=FUNDO_APP, corner_radius=0)
        self.janela = janela
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self._build_topbar()
        self._build_conteudo()

    # ── Topbar ──────────────────────────────────────────────
    def _build_topbar(self):
        topbar = ctk.CTkFrame(self, fg_color="transparent")
        topbar.grid(row=0, column=0, sticky="ew",
                    padx=PAD_LATERAL, pady=(PAD_TOPO, 0))
        topbar.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            topbar, text="Dashboard",
            font=F.titulo(),
            text_color=TEXTO_TITULO
        ).grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(
            topbar, text="Visão geral da clínica",
            font=F.corpo(),
            text_color=AZUL_MEDIO
        ).grid(row=1, column=0, sticky="w")

        # Badge data
        hoje = date.today().strftime("%d de %B de %Y")
        badge = ctk.CTkFrame(
            topbar, fg_color=DOURADO_PALE,
            corner_radius=RAIO_PILL,
            border_width=1, border_color=DOURADO_BORDA)
        badge.grid(row=0, column=1, rowspan=2, sticky="e")
        ctk.CTkLabel(
            badge, text=f"  📅  {hoje}  ",
            font=F.pequena_bold(),
            text_color=AMBER_TEXT
        ).pack(padx=4, pady=7)

    # ── Conteúdo ────────────────────────────────────────────
    def _build_conteudo(self):
        scroll = ctk.CTkScrollableFrame(
            self, fg_color="transparent",
            scrollbar_button_color=AZUL_PALE,
            scrollbar_button_hover_color=AZUL_CLARO)
        scroll.grid(row=1, column=0, sticky="nsew",
                    padx=PAD_LATERAL, pady=20)
        scroll.grid_columnconfigure(0, weight=1)

        self._build_cards(scroll)
        self._build_tabela(scroll)

    # ── Cards ───────────────────────────────────────────────
    def _build_cards(self, parent):
        resumo = controller.obter_resumo_dashboard()

        cards_frame = ctk.CTkFrame(parent, fg_color="transparent")
        cards_frame.grid(row=0, column=0, sticky="ew", pady=(0, 22))
        cards_frame.grid_columnconfigure((0, 1, 2), weight=1)

        dados = [
            (
                "Total de Pacientes",
                str(resumo["total_pacientes"]),
                "👥",
                AZUL_PALE,
                AZUL_ESCURO,
                f"+{resumo['total_pacientes']} cadastrados",
                0
            ),
            (
                "Total de Atendimentos",
                str(resumo["total_atendimentos"]),
                "📄",
                TEAL_BG,
                TEAL_TEXT,
                f"{resumo['total_atendimentos']} no histórico",
                1
            ),
            (
                "Atendimentos Hoje",
                str(resumo["atendimentos_hoje"]),
                "📅",
                DOURADO_PALE,
                AMBER_TEXT,
                "Atualizado agora",
                2
            ),
        ]

        for titulo, valor, icone, bg_icone, cor_icone, sub, col in dados:
            self._card(cards_frame, titulo, valor,
                       icone, bg_icone, cor_icone, sub, col)

    def _card(self, parent, titulo, valor, icone,
              bg_icone, cor_icone, sub, col):
        card = ctk.CTkFrame(
            parent, fg_color=BRANCO,
            corner_radius=RAIO_CARD,
            border_width=1, border_color=BORDA)
        card.grid(row=0, column=col, sticky="ew",
                  padx=(0, 14) if col < 2 else 0)
        card.grid_columnconfigure(0, weight=1)

        # Ícone
        icone_frame = ctk.CTkFrame(
            card, fg_color=bg_icone,
            corner_radius=RAIO_ICONE, width=40, height=40)
        icone_frame.grid(row=0, column=0, sticky="w",
                         padx=PAD_CARD, pady=(PAD_CARD, 10))
        icone_frame.grid_propagate(False)
        ctk.CTkLabel(
            icone_frame, text=icone,
            font=F.font(18),
            text_color=cor_icone
        ).place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(
            card, text=titulo,
            font=F.card_label(),
            text_color=TEXTO_MUTED
        ).grid(row=1, column=0, sticky="w", padx=PAD_CARD)

        ctk.CTkLabel(
            card, text=valor,
            font=F.card_valor(),
            text_color=TEXTO_TITULO
        ).grid(row=2, column=0, sticky="w", padx=PAD_CARD)

        ctk.CTkLabel(
            card, text=sub,
            font=F.card_label(),
            text_color=VERDE_TEXT
        ).grid(row=3, column=0, sticky="w",
               padx=PAD_CARD, pady=(2, PAD_CARD))

    # ── Tabela recentes ─────────────────────────────────────
    def _build_tabela(self, parent):
        # Cabeçalho da seção
        topo = ctk.CTkFrame(parent, fg_color="transparent")
        topo.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        topo.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            topo, text="Atendimentos recentes",
            font=F.subtitulo(),
            text_color=AZUL_PROFUNDO
        ).grid(row=0, column=0, sticky="w")

        ctk.CTkButton(
            topo, text="Ver todos →",
            font=F.pequena(),
            fg_color="transparent",
            text_color=AZUL_MEDIO,
            hover_color=AZUL_PALE,
            corner_radius=RAIO_BTN,
            height=28, width=90,
            command=lambda: self.janela.mostrar_frame("atendimentos")
        ).grid(row=0, column=1, sticky="e")

        # Card tabela
        tabela = ctk.CTkFrame(
            parent, fg_color=BRANCO,
            corner_radius=RAIO_CARD,
            border_width=1, border_color=BORDA)
        tabela.grid(row=2, column=0, sticky="ew")
        tabela.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # Cabeçalho azul + dourado
        colunas = ["Paciente", "Tipo", "Data", "Status"]
        for col, titulo in enumerate(colunas):
            ctk.CTkLabel(
                tabela, text=titulo,
                font=F.tabela_head(),
                text_color=DOURADO_FORTE,
                fg_color=BRANCO,
                anchor="w",
                corner_radius=0
            ).grid(row=0, column=col, sticky="ew",
                   padx=(16 if col == 0 else 8, 8), pady=10)

        # Dados
        pacientes    = {p["id"]: p for p in controller.obter_pacientes()}
        atendimentos = controller.obter_todos_atendimentos()[:8]

        if not atendimentos:
            ctk.CTkLabel(
                tabela,
                text="Nenhum atendimento registrado ainda.",
                font=F.corpo(),
                text_color=TEXTO_MUTED
            ).grid(row=1, column=0, columnspan=4, pady=36)
            return

        for i, atend in enumerate(atendimentos):
            bg = BRANCO if i % 2 == 0 else FUNDO_ALT
            paciente = pacientes.get(atend.get("paciente_id"), {})
            nome     = paciente.get("nome", "—")
            status   = atend.get("status", "")
            is_real  = "acompanhamento" not in status.lower()
            pill_bg  = VERDE_BG   if is_real else AMBER_BG
            pill_fg  = VERDE_TEXT if is_real else AMBER_TEXT

            # Nome
            nome_frame = ctk.CTkFrame(tabela, fg_color=bg, corner_radius=0)
            nome_frame.grid(row=i + 1, column=0, sticky="ew",
                            padx=(16, 8), pady=7)
            ctk.CTkLabel(
                nome_frame, text=nome,
                font=F.tabela_bold(),
                text_color=TEXTO_TITULO, anchor="w"
            ).pack(anchor="w")
            doc = paciente.get("documento", "")
            if doc:
                ctk.CTkLabel(
                    nome_frame, text=doc,
                    font=F.tabela_sub(),
                    text_color=TEXTO_MUTED, anchor="w"
                ).pack(anchor="w")

            # Tipo
            ctk.CTkLabel(
                tabela, text=atend.get("tipo", "—"),
                font=F.tabela_body(),
                text_color=TEXTO_BODY,
                fg_color=bg, anchor="w"
            ).grid(row=i + 1, column=1, sticky="ew", padx=8, pady=7)

            # Data
            data_raw = atend.get("data", "")
            try:
                a, m, d = data_raw.split("-")
                data_fmt = f"{d}/{m}/{a}"
            except Exception:
                data_fmt = data_raw

            ctk.CTkLabel(
                tabela, text=data_fmt,
                font=F.tabela_body(),
                text_color=TEXTO_BODY,
                fg_color=bg, anchor="w"
            ).grid(row=i + 1, column=2, sticky="ew", padx=8, pady=7)

            # Pill status
            pill_frame = ctk.CTkFrame(tabela, fg_color=bg, corner_radius=0)
            pill_frame.grid(row=i + 1, column=3, sticky="ew",
                            padx=(8, 16), pady=6)
            ctk.CTkLabel(
                pill_frame,
                text=f"  {status}  ",
                font=F.pill(),
                text_color=pill_fg,
                fg_color=pill_bg,
                corner_radius=RAIO_PILL
            ).pack(anchor="w")