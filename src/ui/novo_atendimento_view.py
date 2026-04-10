import customtkinter as ctk
from datetime import date
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

from config import *
import src.ui.fonts as F
from src.controllers.clinica_controller import controller
from src.utils.validadores import validador
from exceptions import AtendimentoInvalido


class NovoAtendimentoView(ctk.CTkFrame):
    def __init__(self, parent, janela, paciente_id=None):
        super().__init__(parent, fg_color=FUNDO_APP, corner_radius=0)
        self.janela          = janela
        self._paciente_atual = None
        self._status         = "Realizado"
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self._build_topbar()
        self._build_conteudo()
        if paciente_id:
            self._pre_selecionar(paciente_id)

    # ── Topbar ──────────────────────────────────────────────
    def _build_topbar(self):
        topbar = ctk.CTkFrame(self, fg_color="transparent")
        topbar.grid(row=0, column=0, sticky="ew",
                    padx=PAD_LATERAL, pady=(PAD_TOPO, 0))
        topbar.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            topbar, text="Novo Atendimento",
            font=F.titulo(),
            text_color=TEXTO_TITULO
        ).grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(
            topbar, text="Registre um atendimento para um paciente",
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

        self._build_card_paciente()
        self._build_formulario()

    # ── Card paciente selecionado ────────────────────────────
    def _build_card_paciente(self):
        card = ctk.CTkFrame(
            self._scroll, fg_color=BRANCO,
            corner_radius=RAIO_CARD,
            border_width=1, border_color=BORDA
        )
        card.grid(row=0, column=0, sticky="ew", pady=(0, 14))
        card.grid_columnconfigure(1, weight=1)

        # Avatar
        self._avatar_frame = ctk.CTkFrame(
            card, fg_color=AZUL_PALE,
            corner_radius=RAIO_AVATAR, width=48, height=48
        )
        self._avatar_frame.grid(row=0, column=0, rowspan=2,
                                padx=(18, 14), pady=16)
        self._avatar_frame.grid_propagate(False)
        self._avatar_label = ctk.CTkLabel(
            self._avatar_frame, text="?",
            font=F.font(18, "bold"),
            text_color=AZUL_ESCURO
        )
        self._avatar_label.place(relx=0.5, rely=0.5, anchor="center")

        # Nome
        self._label_nome = ctk.CTkLabel(
            card,
            text="Nenhum paciente selecionado",
            font=F.corpo_bold(),
            text_color=TEXTO_MUTED
        )
        self._label_nome.grid(row=0, column=1, sticky="sw", pady=(16, 0))

        # Documento e nascimento
        self._label_doc = ctk.CTkLabel(
            card, text="",
            font=F.mini(),
            text_color=TEXTO_MUTED
        )
        self._label_doc.grid(row=1, column=1, sticky="nw", pady=(0, 16))

        # Badge status
        self._badge_pac = ctk.CTkLabel(
            card,
            text="  Selecione um paciente  ",
            font=F.mini_bold(),
            text_color=TEXTO_MUTED,
            fg_color=BORDA,
            corner_radius=RAIO_PILL
        )
        self._badge_pac.grid(row=0, column=2, rowspan=2,
                             padx=(0, 18), pady=16)

    # ── Formulário ──────────────────────────────────────────
    def _build_formulario(self):
        card = ctk.CTkFrame(
            self._scroll, fg_color=BRANCO,
            corner_radius=RAIO_CARD,
            border_width=1, border_color=BORDA
        )
        card.grid(row=1, column=0, sticky="ew")
        card.grid_columnconfigure((0, 1), weight=1)

        # Título
        ctk.CTkLabel(
            card, text="Dados do Atendimento",
            font=F.subtitulo(),
            text_color=AZUL_PROFUNDO
        ).grid(row=0, column=0, columnspan=2,
               sticky="w", padx=PAD_CARD, pady=(PAD_CARD, 0))

        self._sep(card, row=1)

        # ── Seção: Busca de paciente ──
        self._secao(card, "Selecionar Paciente", row=2)
        self._build_busca_paciente(card, row=3)

        self._sep(card, row=4)

        # ── Seção: Dados do atendimento ──
        self._secao(card, "Informações do Atendimento", row=5)

        # Data
        data_frame = ctk.CTkFrame(card, fg_color="transparent")
        data_frame.grid(row=6, column=0, sticky="ew",
                        padx=(PAD_CARD, 10), pady=(0, 14))
        data_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            data_frame, text="DATA DO ATENDIMENTO",
            font=F.label(), text_color=AZUL_ESCURO
        ).pack(anchor="w", pady=(0, 4))

        self._entry_data = ctk.CTkEntry(
            data_frame,
            height=ALTURA_INPUT, corner_radius=RAIO_INPUT,
            border_color=AZUL_CLARO, border_width=1,
            fg_color=FUNDO_INPUT, text_color=TEXTO_TITULO,
            font=F.corpo()
        )
        self._entry_data.insert(0, date.today().strftime("%d/%m/%Y"))
        self._entry_data.pack(fill="x")

        self._erro_data = ctk.CTkLabel(
            data_frame, text="", font=F.mini(), text_color=ERRO_TEXT)
        self._erro_data.pack(anchor="w")

        # Tipo
        tipo_frame = ctk.CTkFrame(card, fg_color="transparent")
        tipo_frame.grid(row=6, column=1, sticky="ew",
                        padx=(10, PAD_CARD), pady=(0, 14))
        tipo_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            tipo_frame, text="TIPO DE ATENDIMENTO",
            font=F.label(), text_color=AZUL_ESCURO
        ).pack(anchor="w", pady=(0, 4))

        self._opt_tipo = ctk.CTkOptionMenu(
            tipo_frame,
            values=["Consulta", "Retorno", "Exame",
                    "Procedimento", "Urgência"],
            height=ALTURA_INPUT, corner_radius=RAIO_INPUT,
            fg_color=FUNDO_INPUT,
            button_color=AZUL_CLARO,
            button_hover_color=AZUL_PALE,
            text_color=TEXTO_TITULO,
            font=F.corpo()
        )
        self._opt_tipo.pack(fill="x")

        # Observações
        obs_frame = ctk.CTkFrame(card, fg_color="transparent")
        obs_frame.grid(row=7, column=0, columnspan=2,
                       sticky="ew", padx=PAD_CARD, pady=(0, 14))
        obs_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            obs_frame, text="OBSERVAÇÕES DO PROFISSIONAL",
            font=F.label(), text_color=AZUL_ESCURO
        ).pack(anchor="w", pady=(0, 4))

        self._obs = ctk.CTkTextbox(
            obs_frame, height=84,
            corner_radius=RAIO_INPUT,
            border_color=AZUL_CLARO, border_width=1,
            fg_color=FUNDO_INPUT, text_color=TEXTO_TITULO,
            font=F.corpo()
        )
        self._obs.pack(fill="x")

        # ── Status ──
        self._sep(card, row=8)
        self._secao(card, "Status do Atendimento", row=9)

        status_frame = ctk.CTkFrame(card, fg_color="transparent")
        status_frame.grid(row=10, column=0, columnspan=2,
                          sticky="ew", padx=PAD_CARD, pady=(0, 14))
        status_frame.grid_columnconfigure((0, 1), weight=1)

        self._btn_realizado = ctk.CTkButton(
            status_frame,
            text="✓   Realizado",
            height=42, corner_radius=RAIO_BTN,
            border_width=1,
            fg_color=VERDE_BG, text_color=VERDE_TEXT,
            border_color=VERDE_TEXT,
            hover_color="#D4EDDA",
            font=F.btn_bold(),
            command=lambda: self._set_status("Realizado")
        )
        self._btn_realizado.grid(row=0, column=0, sticky="ew", padx=(0, 8))

        self._btn_acomp = ctk.CTkButton(
            status_frame,
            text="⟳   Em Acompanhamento",
            height=42, corner_radius=RAIO_BTN,
            border_width=1,
            fg_color=FUNDO_INPUT, text_color=TEXTO_MUTED,
            border_color=AZUL_CLARO,
            hover_color=AMBER_BG,
            font=F.btn(),
            command=lambda: self._set_status("Em acompanhamento")
        )
        self._btn_acomp.grid(row=0, column=1, sticky="ew", padx=(8, 0))

        # ── Botões ──
        self._sep(card, row=11)

        btns = ctk.CTkFrame(card, fg_color="transparent")
        btns.grid(row=12, column=0, columnspan=2,
                  sticky="e", padx=PAD_CARD, pady=(12, PAD_CARD))

        ctk.CTkButton(
            btns, text="Limpar",
            width=110, height=ALTURA_BTN,
            fg_color="transparent", text_color=AZUL_ESCURO,
            border_width=1, border_color=AZUL_CLARO,
            hover_color=AZUL_PALE, corner_radius=RAIO_BTN,
            font=F.btn(),
            command=self._limpar
        ).pack(side="left", padx=(0, 10))

        ctk.CTkButton(
            btns, text="✓   Salvar Atendimento",
            width=200, height=ALTURA_BTN,
            fg_color=AZUL_ESCURO, text_color=BRANCO,
            hover_color=AZUL_PROFUNDO,
            corner_radius=RAIO_BTN,
            font=F.btn_bold(),
            command=self._salvar
        ).pack(side="left")

        # Feedback
        self._label_feedback = ctk.CTkLabel(
            card, text="",
            font=F.feedback(),
            text_color=VERDE_TEXT
        )
        self._label_feedback.grid(
            row=13, column=0, columnspan=2, pady=(0, 10))

    # ── Busca de paciente inline ─────────────────────────────
    def _build_busca_paciente(self, parent, row):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.grid(row=row, column=0, columnspan=2,
                   sticky="ew", padx=PAD_CARD, pady=(0, 4))
        frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            frame, text="BUSCAR PACIENTE",
            font=F.label(), text_color=AZUL_ESCURO
        ).pack(anchor="w", pady=(0, 4))

        self._entry_busca = ctk.CTkEntry(
            frame,
            placeholder_text="🔍   Digite o nome ou telefone...",
            height=ALTURA_INPUT, corner_radius=RAIO_INPUT,
            border_color=AZUL_CLARO, border_width=1,
            fg_color=FUNDO_INPUT, text_color=TEXTO_TITULO,
            placeholder_text_color=TEXTO_MUTED,
            font=F.corpo()
        )
        self._entry_busca.pack(fill="x", pady=(0, 4))
        self._entry_busca.bind("<KeyRelease>", lambda e: self._pesquisar())

        # Lista de sugestões
        self._lista = ctk.CTkFrame(
            frame, fg_color=BRANCO,
            corner_radius=RAIO_BTN,
            border_width=1, border_color=AZUL_CLARO
        )

        self._erro_paciente = ctk.CTkLabel(
            frame, text="", font=F.mini(), text_color=ERRO_TEXT)
        self._erro_paciente.pack(anchor="w")

    # ── Helpers ─────────────────────────────────────────────
    def _sep(self, parent, row):
        ctk.CTkFrame(
            parent, fg_color=BORDA, height=1, corner_radius=0
        ).grid(row=row, column=0, columnspan=2,
               sticky="ew", padx=0, pady=4)

    def _secao(self, parent, texto, row):
        ctk.CTkLabel(
            parent, text=texto.upper(),
            font=F.secao(), text_color=AZUL_MEDIO
        ).grid(row=row, column=0, columnspan=2,
               sticky="w", padx=PAD_CARD, pady=(6, 2))

    def _set_status(self, status):
        self._status = status
        if status == "Realizado":
            self._btn_realizado.configure(
                fg_color=VERDE_BG, text_color=VERDE_TEXT,
                border_color=VERDE_TEXT, font=F.btn_bold())
            self._btn_acomp.configure(
                fg_color=FUNDO_INPUT, text_color=TEXTO_MUTED,
                border_color=AZUL_CLARO, font=F.btn())
        else:
            self._btn_acomp.configure(
                fg_color=AMBER_BG, text_color=AMBER_TEXT,
                border_color=AMBER_TEXT, font=F.btn_bold())
            self._btn_realizado.configure(
                fg_color=FUNDO_INPUT, text_color=TEXTO_MUTED,
                border_color=AZUL_CLARO, font=F.btn())

    def _pesquisar(self):
        termo = self._entry_busca.get().strip()
        for w in self._lista.winfo_children():
            w.destroy()

        if not termo:
            self._lista.pack_forget()
            return

        resultados = controller.buscar_pacientes(termo)[:6]
        if not resultados:
            self._lista.pack_forget()
            return

        self._lista.pack(fill="x", pady=(0, 4))
        for p in resultados:
            nome = p.get("nome", "")
            doc  = p.get("documento", "")
            ctk.CTkButton(
                self._lista,
                text=f"  {nome}  —  {doc}",
                anchor="w", height=36,
                fg_color="transparent",
                text_color=TEXTO_TITULO,
                hover_color=AZUL_PALE,
                corner_radius=0,
                font=F.corpo(),
                command=lambda pac=p: self._selecionar(pac)
            ).pack(fill="x")

    def _selecionar(self, paciente):
        self._paciente_atual = paciente
        nome     = paciente.get("nome", "")
        doc      = paciente.get("documento", "")
        nasc_raw = paciente.get("data_nascimento", "")
        iniciais = "".join([p[0].upper() for p in nome.split()[:2]])

        # Formata nascimento
        try:
            a, m, d  = nasc_raw.split("-")
            nasc_fmt = f"{d}/{m}/{a}"
        except Exception:
            nasc_fmt = nasc_raw

        # Atualiza card
        self._avatar_label.configure(text=iniciais)
        self._label_nome.configure(
            text=nome, text_color=TEXTO_TITULO)
        self._label_doc.configure(
            text=f"{doc}   ·   Nasc. {nasc_fmt}",
            text_color=TEXTO_MUTED)
        self._badge_pac.configure(
            text="  ✓ Paciente selecionado  ",
            text_color=VERDE_TEXT, fg_color=VERDE_BG)

        # Limpa busca e esconde lista
        self._entry_busca.delete(0, "end")
        self._entry_busca.insert(0, nome)
        self._lista.pack_forget()
        self._erro_paciente.configure(text="")

    def _pre_selecionar(self, paciente_id):
        """Pré-seleciona paciente quando vindo da tela de listagem."""
        try:
            p = controller.obter_paciente_por_id(paciente_id)
            self._selecionar(p)
        except Exception:
            pass

    def _limpar(self):
        self._paciente_atual = None
        self._entry_busca.delete(0, "end")
        self._entry_data.delete(0, "end")
        self._entry_data.insert(0, date.today().strftime("%d/%m/%Y"))
        self._obs.delete("1.0", "end")
        self._opt_tipo.set("Consulta")
        self._set_status("Realizado")
        self._avatar_label.configure(text="?")
        self._label_nome.configure(
            text="Nenhum paciente selecionado",
            text_color=TEXTO_MUTED)
        self._label_doc.configure(text="")
        self._badge_pac.configure(
            text="  Selecione um paciente  ",
            text_color=TEXTO_MUTED, fg_color=BORDA)
        self._label_feedback.configure(text="")
        self._erro_paciente.configure(text="")
        self._erro_data.configure(text="")
        self._lista.pack_forget()

    # ── Salvar ───────────────────────────────────────────────
    def _salvar(self):
        self._label_feedback.configure(text="")
        self._erro_paciente.configure(text="")
        self._erro_data.configure(text="")
        erro = False

        # Valida paciente
        if not self._paciente_atual:
            self._erro_paciente.configure(
                text="⚠  Selecione um paciente.")
            self._entry_busca.configure(border_color=ERRO_TEXT)
            erro = True

        # Valida data
        data = self._entry_data.get().strip()
        try:
            validador.data_atendimento(data)
        except AtendimentoInvalido as e:
            self._erro_data.configure(text=f"⚠  {e}")
            self._entry_data.configure(border_color=ERRO_TEXT)
            erro = True

        if erro:
            self._label_feedback.configure(
                text="⚠  Corrija os campos antes de salvar.",
                text_color=ERRO_TEXT)
            return

        # Salva
        try:
            tipo = self._opt_tipo.get()
            obs  = self._obs.get("1.0", "end").strip()

            a = controller.registrar_atendimento(
                paciente_id=self._paciente_atual["id"],
                data=data,
                tipo=tipo,
                observacoes=obs,
                status=self._status
            )
            nome = self._paciente_atual.get("nome", "")
            self._label_feedback.configure(
                text=f"✓  Atendimento de '{nome}' registrado com sucesso!",
                text_color=VERDE_TEXT)
            self._limpar()

        except AtendimentoInvalido as e:
            self._label_feedback.configure(
                text=f"⚠  {e}", text_color=ERRO_TEXT)
        except Exception as e:
            self._label_feedback.configure(
                text=f"⚠  Erro inesperado: {e}", text_color=ERRO_TEXT)