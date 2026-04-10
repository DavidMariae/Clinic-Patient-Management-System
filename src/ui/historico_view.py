import customtkinter as ctk
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

from config import *
import src.ui.fonts as F
from src.controllers.clinica_controller import controller


class HistoricoView(ctk.CTkFrame):
    def __init__(self, parent, janela, paciente_id=None):
        super().__init__(parent, fg_color=FUNDO_APP, corner_radius=0)
        self.janela              = janela
        self._paciente           = None
        self._atendimentos_todos = []
        self._filtro_tipo        = "Todos os tipos"
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self._build_topbar()
        self._build_conteudo()
        if paciente_id:
            self._carregar(paciente_id)

    # ── Topbar ──────────────────────────────────────────────
    def _build_topbar(self):
        topbar = ctk.CTkFrame(self, fg_color="transparent")
        topbar.grid(row=0, column=0, sticky="ew",
                    padx=PAD_LATERAL, pady=(PAD_TOPO, 0))
        topbar.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            topbar, text="Histórico do Paciente",
            font=F.titulo(),
            text_color=TEXTO_TITULO
        ).grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(
            topbar, text="Todos os atendimentos registrados",
            font=F.corpo(),
            text_color=AZUL_MEDIO
        ).grid(row=1, column=0, sticky="w")

        ctk.CTkButton(
            topbar, text="← Voltar",
            width=100, height=ALTURA_TOPBAR_BTN,
            fg_color=AZUL_PALE, text_color=AZUL_ESCURO,
            hover_color=AZUL_CLARO, corner_radius=RAIO_BTN,
            font=F.btn(),
            command=lambda: self.janela.mostrar_frame("pacientes")
        ).grid(row=0, column=1, rowspan=2, sticky="e")

    # ── Conteúdo ────────────────────────────────────────────
    def _build_conteudo(self):
        self._scroll = ctk.CTkScrollableFrame(
            self, fg_color="transparent",
            scrollbar_button_color=AZUL_PALE,
            scrollbar_button_hover_color=AZUL_CLARO
        )
        self._scroll.grid(row=1, column=0, sticky="nsew",
                          padx=PAD_LATERAL, pady=20)
        self._scroll.grid_columnconfigure(0, weight=1)

    # ── Carregar ────────────────────────────────────────────
    def _carregar(self, paciente_id):
        try:
            self._paciente = controller.obter_paciente_por_id(paciente_id)
        except Exception:
            return

        self._atendimentos_todos = controller.obter_atendimentos_do_paciente(
            paciente_id)
        self._renderizar()

    def _renderizar(self):
        for w in self._scroll.winfo_children():
            w.destroy()
        self._build_card_perfil()
        self._build_timeline_header()
        self._build_timeline()

    # ── Card perfil ─────────────────────────────────────────
    def _build_card_perfil(self):
        p        = self._paciente
        nome     = p.get("nome", "")
        iniciais = "".join([x[0].upper() for x in nome.split()[:2]])
        total    = len(self._atendimentos_todos)
        em_acomp = sum(
            1 for a in self._atendimentos_todos
            if "acompanhamento" in a.get("status", "").lower()
        )

        card = ctk.CTkFrame(
            self._scroll, fg_color=BRANCO,
            corner_radius=RAIO_CARD,
            border_width=1, border_color=BORDA
        )
        card.grid(row=0, column=0, sticky="ew", pady=(0, 14))
        card.grid_columnconfigure(1, weight=1)

        # Avatar
        av = ctk.CTkFrame(
            card, fg_color=AZUL_PALE,
            corner_radius=28, width=56, height=56
        )
        av.grid(row=0, column=0, rowspan=2, padx=(20, 16), pady=18)
        av.grid_propagate(False)
        ctk.CTkLabel(
            av, text=iniciais,
            font=F.font(20, "bold"),
            text_color=AZUL_ESCURO
        ).place(relx=0.5, rely=0.5, anchor="center")

        # Nome
        ctk.CTkLabel(
            card, text=nome,
            font=F.font(16, "bold"),
            text_color=TEXTO_TITULO
        ).grid(row=0, column=1, sticky="sw", pady=(18, 2))

        # Detalhes
        nasc_raw = p.get("data_nascimento", "")
        try:
            a, m, d  = nasc_raw.split("-")
            nasc_fmt = f"{d}/{m}/{a}"
        except Exception:
            nasc_fmt = nasc_raw

        detalhes = (
            f"🪪  {p.get('documento','—')}     "
            f"📅  Nasc. {nasc_fmt}     "
            f"📞  {p.get('telefone','—')}     "
            f"✉   {p.get('email','—') or '—'}"
        )
        ctk.CTkLabel(
            card, text=detalhes,
            font=F.mini(),
            text_color=TEXTO_MUTED
        ).grid(row=1, column=1, sticky="nw", pady=(0, 18))

        # Stats
        stats = ctk.CTkFrame(card, fg_color="transparent")
        stats.grid(row=0, column=2, rowspan=2, padx=(0, 14), pady=18)

        for val, label in [
            (str(total),    "Atendimentos"),
            (str(em_acomp), "Em acomp.")
        ]:
            s = ctk.CTkFrame(
                stats, fg_color=FUNDO_APP,
                corner_radius=RAIO_BTN)
            s.pack(side="left", padx=6)
            ctk.CTkLabel(
                s, text=val,
                font=F.font(20, "bold"),
                text_color=AZUL_ESCURO
            ).pack(padx=16, pady=(10, 0))
            ctk.CTkLabel(
                s, text=label,
                font=F.mini(),
                text_color=TEXTO_MUTED
            ).pack(padx=16, pady=(0, 10))

        # Botão novo atendimento
        ctk.CTkButton(
            card, text="＋  Novo Atendimento",
            height=ALTURA_BTN, corner_radius=RAIO_BTN,
            fg_color=AZUL_ESCURO, text_color=BRANCO,
            hover_color=AZUL_PROFUNDO,
            font=F.btn_bold(),
            command=lambda: self.janela.mostrar_frame(
                "novo_atendimento",
                paciente_id=self._paciente["id"])
        ).grid(row=0, column=3, rowspan=2, padx=(0, 20), pady=18)

    # ── Header timeline ─────────────────────────────────────
    def _build_timeline_header(self):
        row = ctk.CTkFrame(self._scroll, fg_color="transparent")
        row.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        row.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            row, text="Histórico de Atendimentos",
            font=F.subtitulo(),
            text_color=AZUL_PROFUNDO
        ).grid(row=0, column=0, sticky="w")

        self._opt_filtro = ctk.CTkOptionMenu(
            row,
            values=["Todos os tipos", "Consulta", "Retorno",
                    "Exame", "Procedimento", "Urgência"],
            width=180, height=32, corner_radius=RAIO_BTN,
            fg_color=BRANCO,
            button_color=AZUL_CLARO,
            button_hover_color=AZUL_PALE,
            text_color=AZUL_ESCURO,
            font=F.pequena(),
            command=self._aplicar_filtro
        )
        self._opt_filtro.grid(row=0, column=1, sticky="e")

    # ── Timeline ────────────────────────────────────────────
    def _build_timeline(self):
        # Limpa itens anteriores (row >= 2)
        for w in self._scroll.winfo_children():
            info = w.grid_info()
            if info and int(info.get("row", 0)) >= 2:
                w.destroy()

        atendimentos = self._atendimentos_todos
        if self._filtro_tipo != "Todos os tipos":
            atendimentos = [
                a for a in atendimentos
                if a.get("tipo") == self._filtro_tipo
            ]

        if not atendimentos:
            ctk.CTkLabel(
                self._scroll,
                text="Nenhum atendimento encontrado.",
                font=F.corpo(),
                text_color=TEXTO_MUTED
            ).grid(row=2, column=0, pady=40)
            return

        for i, atend in enumerate(atendimentos):
            self._item_timeline(
                atend, row=i + 2,
                is_last=(i == len(atendimentos) - 1)
            )

    def _item_timeline(self, atend, row, is_last):
        status     = atend.get("status", "")
        is_real    = "acompanhamento" not in status.lower()
        dot_color  = VERDE_TEXT  if is_real else AMBER_TEXT
        pill_bg    = VERDE_BG    if is_real else AMBER_BG
        pill_fg    = VERDE_TEXT  if is_real else AMBER_TEXT
        pill_texto = "Realizado" if is_real else "Em acompanhamento"

        # Container do item
        item = ctk.CTkFrame(self._scroll, fg_color="transparent")
        item.grid(row=row, column=0, sticky="ew", pady=(0, 2))
        item.grid_columnconfigure(1, weight=1)

        # Coluna da linha do tempo
        tl = ctk.CTkFrame(item, fg_color="transparent", width=24)
        tl.grid(row=0, column=0, sticky="ns", padx=(2, 10))
        tl.grid_propagate(False)

        # Ponto colorido
        dot = ctk.CTkFrame(
            tl, fg_color=dot_color,
            corner_radius=7, width=14, height=14
        )
        dot.place(relx=0.5, y=10, anchor="n")

        # Linha conectora
        if not is_last:
            linha = ctk.CTkFrame(tl, fg_color=BORDA, width=2, height=50)
            linha.place(relx=0.5, y=26, anchor="n",
                        )

        # Card do atendimento
        card = ctk.CTkFrame(
            item, fg_color=BRANCO,
            corner_radius=RAIO_BTN,
            border_width=1, border_color=BORDA
        )
        card.grid(row=0, column=1, sticky="ew", pady=(0, 12))
        card.grid_columnconfigure(0, weight=1)

        # Topo do card
        topo = ctk.CTkFrame(card, fg_color="transparent")
        topo.grid(row=0, column=0, sticky="ew",
                  padx=16, pady=(12, 6))
        topo.grid_columnconfigure(0, weight=1)

        # Tipo + pill
        esq = ctk.CTkFrame(topo, fg_color="transparent")
        esq.grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(
            esq, text=atend.get("tipo", "—"),
            font=F.tabela_bold(),
            text_color=TEXTO_TITULO
        ).pack(side="left", padx=(0, 10))

        ctk.CTkLabel(
            esq,
            text=f"  {pill_texto}  ",
            font=F.pill(),
            text_color=pill_fg,
            fg_color=pill_bg,
            corner_radius=RAIO_PILL
        ).pack(side="left")

        # Data formatada
        data_raw = atend.get("data", "")
        try:
            a, m, d  = data_raw.split("-")
            data_fmt = f"{d}/{m}/{a}"
        except Exception:
            data_fmt = data_raw

        ctk.CTkLabel(
            topo, text=data_fmt,
            font=F.pequena(),
            text_color=TEXTO_MUTED
        ).grid(row=0, column=1, sticky="e")

        # Observações
        obs = atend.get("observacoes", "").strip()
        ctk.CTkLabel(
            card,
            text=obs if obs else "Nenhuma observação registrada.",
            font=F.corpo(),
            text_color=TEXTO_BODY if obs else TEXTO_MUTED,
            wraplength=540,
            justify="left",
            anchor="w"
        ).grid(row=1, column=0, sticky="ew",
               padx=16, pady=(0, 12))

    def _aplicar_filtro(self, valor):
        self._filtro_tipo = valor
        self._build_timeline()