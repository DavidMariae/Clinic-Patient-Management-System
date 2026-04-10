import customtkinter as ctk
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

from config import *
import src.ui.fonts as F
from src.controllers.clinica_controller import controller
from src.utils.validadores import validador
from exceptions import AtendimentoInvalido


class EditarPacienteView(ctk.CTkFrame):
    def __init__(self, parent, janela, paciente_id=None):
        super().__init__(parent, fg_color=FUNDO_APP, corner_radius=0)
        self.janela       = janela
        self._paciente_id = paciente_id
        self._paciente    = None
        self._campos      = {}
        self._erros       = {}
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self._build_topbar()
        self._build_formulario()
        if paciente_id:
            self._carregar(paciente_id)

    # ── Topbar ──────────────────────────────────────────────
    def _build_topbar(self):
        topbar = ctk.CTkFrame(self, fg_color="transparent")
        topbar.grid(row=0, column=0, sticky="ew",
                    padx=PAD_LATERAL, pady=(PAD_TOPO, 0))
        topbar.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            topbar, text="Editar Paciente",
            font=F.titulo(), text_color=TEXTO_TITULO
        ).grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(
            topbar, text="Atualize os dados do paciente",
            font=F.corpo(), text_color=AZUL_MEDIO
        ).grid(row=1, column=0, sticky="w")

        ctk.CTkButton(
            topbar, text="← Voltar",
            width=100, height=ALTURA_TOPBAR_BTN,
            fg_color=AZUL_PALE, text_color=AZUL_ESCURO,
            hover_color=AZUL_CLARO, corner_radius=RAIO_BTN,
            font=F.btn(),
            command=lambda: self.janela.mostrar_frame("pacientes")
        ).grid(row=0, column=1, rowspan=2, sticky="e")

    # ── Formulário ──────────────────────────────────────────
    def _build_formulario(self):
        scroll = ctk.CTkScrollableFrame(
            self, fg_color="transparent",
            scrollbar_button_color=AZUL_PALE,
            scrollbar_button_hover_color=AZUL_CLARO)
        scroll.grid(row=1, column=0, sticky="nsew",
                    padx=PAD_LATERAL, pady=20)
        scroll.grid_columnconfigure(0, weight=1)

        self._card = ctk.CTkFrame(
            scroll, fg_color=BRANCO,
            corner_radius=RAIO_CARD,
            border_width=1, border_color=BORDA)
        self._card.grid(row=0, column=0, sticky="ew")
        self._card.grid_columnconfigure((0, 1), weight=1)

        # Título + botão excluir
        titulo_frame = ctk.CTkFrame(self._card, fg_color="transparent")
        titulo_frame.grid(row=0, column=0, columnspan=2,
                          sticky="ew", padx=PAD_CARD, pady=(PAD_CARD, 0))
        titulo_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            titulo_frame, text="Dados do Paciente",
            font=F.subtitulo(), text_color=AZUL_PROFUNDO
        ).grid(row=0, column=0, sticky="w")

        ctk.CTkButton(
            titulo_frame, text="🗑   Excluir Paciente",
            height=32, width=150,
            fg_color=ERRO_BG, text_color=ERRO_TEXT,
            hover_color="#FCA5A5",
            border_width=1, border_color=ERRO_TEXT,
            corner_radius=RAIO_BTN,
            font=F.btn_pequeno(),
            command=self._confirmar_exclusao
        ).grid(row=0, column=1, sticky="e")

        self._separador(self._card, row=1)

        # ── Seção: Informações pessoais ──
        self._secao(self._card, "Informações Pessoais", row=2)

        self._campo(self._card, "NOME COMPLETO", "nome",
                    "Ex: Maria da Silva Souza", row=3, col=0, span=2)
        self._campo(self._card, "DATA DE NASCIMENTO", "data_nascimento",
                    "DD/MM/AAAA", row=4, col=0)
        self._campo(self._card, "DOCUMENTO (CPF ou RG)", "documento",
                    "Ex: 123.456.789-00", row=4, col=1)

        self._separador(self._card, row=5)

        # ── Seção: Contato ──
        self._secao(self._card, "Contato", row=6)

        self._campo(self._card, "TELEFONE", "telefone",
                    "Ex: (88) 99999-9999", row=7, col=0)
        self._campo(self._card, "E-MAIL  (opcional)", "email",
                    "Ex: maria@email.com", row=7, col=1)

        self._separador(self._card, row=8)
        self._build_botoes(self._card, row=9)

        self._label_feedback = ctk.CTkLabel(
            self._card, text="",
            font=F.feedback(), text_color=VERDE_TEXT)
        self._label_feedback.grid(
            row=10, column=0, columnspan=2, pady=(0, 12))

    # ── Helpers layout ───────────────────────────────────────
    def _separador(self, parent, row):
        ctk.CTkFrame(
            parent, fg_color=BORDA, height=1, corner_radius=0
        ).grid(row=row, column=0, columnspan=2,
               sticky="ew", padx=0, pady=4)

    def _secao(self, parent, texto, row):
        ctk.CTkLabel(
            parent, text=texto.upper(),
            font=F.secao(), text_color=AZUL_MEDIO
        ).grid(row=row, column=0, columnspan=2,
               sticky="w", padx=PAD_CARD, pady=(8, 2))

    def _campo(self, parent, label, chave, placeholder,
               row, col, span=1):
        padx_esq = PAD_CARD if col == 0 else 10
        padx_dir = PAD_CARD if (col == 1 or span == 2) else 10

        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.grid(row=row, column=col, columnspan=span,
                   sticky="ew", padx=(padx_esq, padx_dir), pady=(0, 4))
        frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            frame, text=label,
            font=F.label(), text_color=AZUL_ESCURO
        ).pack(anchor="w", pady=(0, 4))

        entry = ctk.CTkEntry(
            frame, placeholder_text=placeholder,
            height=ALTURA_INPUT, corner_radius=RAIO_INPUT,
            border_color=AZUL_CLARO, border_width=1,
            fg_color=FUNDO_INPUT, text_color=TEXTO_TITULO,
            placeholder_text_color=TEXTO_MUTED,
            font=F.corpo()
        )
        entry.pack(fill="x")
        entry.bind("<KeyRelease>",
                   lambda e, c=chave: self._limpar_erro(c))

        erro = ctk.CTkLabel(
            frame, text="",
            font=F.mini(), text_color=ERRO_TEXT, anchor="w")
        erro.pack(anchor="w")

        self._campos[chave] = entry
        self._erros[chave]  = erro

    def _build_botoes(self, parent, row):
        btns = ctk.CTkFrame(parent, fg_color="transparent")
        btns.grid(row=row, column=0, columnspan=2,
                  sticky="e", padx=PAD_CARD, pady=(10, 16))

        ctk.CTkButton(
            btns, text="Cancelar",
            width=110, height=ALTURA_BTN,
            fg_color="transparent", text_color=AZUL_ESCURO,
            border_width=1, border_color=AZUL_CLARO,
            hover_color=AZUL_PALE, corner_radius=RAIO_BTN,
            font=F.btn(),
            command=lambda: self.janela.mostrar_frame("pacientes")
        ).pack(side="left", padx=(0, 10))

        ctk.CTkButton(
            btns, text="✓   Salvar Alterações",
            width=180, height=ALTURA_BTN,
            fg_color=AZUL_ESCURO, text_color=BRANCO,
            hover_color=AZUL_PROFUNDO,
            corner_radius=RAIO_BTN,
            font=F.btn_bold(),
            command=self._salvar
        ).pack(side="left")

    # ── Carregar dados ───────────────────────────────────────
    def _carregar(self, paciente_id):
        try:
            self._paciente = controller.obter_paciente_por_id(paciente_id)
        except Exception:
            self._label_feedback.configure(
                text="⚠  Paciente não encontrado.",
                text_color=ERRO_TEXT)
            return

        p = self._paciente

        # Preenche os campos
        self._campos["nome"].insert(0, p.get("nome", ""))
        self._campos["documento"].insert(0, p.get("documento", ""))
        self._campos["telefone"].insert(0, p.get("telefone", ""))
        self._campos["email"].insert(0, p.get("email", "") or "")

        # Converte data ISO → BR para exibição
        nasc_raw = p.get("data_nascimento", "")
        try:
            a, m, d  = nasc_raw.split("-")
            nasc_fmt = f"{d}/{m}/{a}"
        except Exception:
            nasc_fmt = nasc_raw
        self._campos["data_nascimento"].insert(0, nasc_fmt)

    # ── Lógica ──────────────────────────────────────────────
    def _limpar_erro(self, chave):
        if chave in self._erros:
            self._erros[chave].configure(text="")
        self._label_feedback.configure(text="")

    def _mostrar_erro_campo(self, chave, mensagem):
        if chave in self._erros:
            self._erros[chave].configure(text=f"⚠  {mensagem}")
        if chave in self._campos:
            self._campos[chave].configure(border_color=ERRO_TEXT)

    def _resetar_bordas(self):
        for entry in self._campos.values():
            entry.configure(border_color=AZUL_CLARO)
        for erro in self._erros.values():
            erro.configure(text="")

    def _salvar(self):
        self._resetar_bordas()
        self._label_feedback.configure(text="")

        nome      = self._campos["nome"].get()
        data_nasc = self._campos["data_nascimento"].get()
        documento = self._campos["documento"].get()
        telefone  = self._campos["telefone"].get()
        email     = self._campos["email"].get()

        erro_encontrado = False
        validacoes = [
            ("nome",            lambda: validador.nome(nome)),
            ("data_nascimento", lambda: validador.data_nascimento(data_nasc)),
            ("documento",       lambda: validador.documento(documento)),
            ("telefone",        lambda: validador.telefone(telefone)),
            ("email",           lambda: validador.email(email)),
        ]

        for chave, fn in validacoes:
            try:
                fn()
            except AtendimentoInvalido as e:
                self._mostrar_erro_campo(chave, str(e))
                if not erro_encontrado:
                    self._campos[chave].focus()
                    erro_encontrado = True

        if erro_encontrado:
            self._label_feedback.configure(
                text="⚠  Corrija os campos destacados.",
                text_color=ERRO_TEXT)
            return

        try:
            controller.atualizar_paciente(
                self._paciente_id,
                nome=nome,
                data_nascimento=data_nasc,
                documento=documento,
                telefone=telefone,
                email=email
            )
            self._label_feedback.configure(
                text=f"✓  Dados de '{nome}' atualizados com sucesso!",
                text_color=VERDE_TEXT)
        except Exception as e:
            self._label_feedback.configure(
                text=f"⚠  Erro: {e}", text_color=ERRO_TEXT)

    # ── Modal de exclusão ────────────────────────────────────
    def _confirmar_exclusao(self):
        if not self._paciente:
            return

        nome = self._paciente.get("nome", "este paciente")

        # Overlay escuro
        overlay = ctk.CTkFrame(
            self, fg_color=("gray10", "gray10"),
            corner_radius=0)
        overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        overlay.configure(fg_color="transparent")

        # Modal central
        modal = ctk.CTkFrame(
            overlay, fg_color=BRANCO,
            corner_radius=RAIO_CARD,
            border_width=1, border_color=BORDA,
            width=400)
        modal.place(relx=0.5, rely=0.5, anchor="center")

        # Ícone
        icone_frame = ctk.CTkFrame(
            modal, fg_color=ERRO_BG,
            corner_radius=28, width=56, height=56)
        icone_frame.pack(pady=(28, 0))
        icone_frame.pack_propagate(False)
        ctk.CTkLabel(
            icone_frame, text="🗑",
            font=F.font(24)
        ).place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(
            modal, text="Excluir Paciente?",
            font=F.subtitulo(), text_color=TEXTO_TITULO
        ).pack(pady=(14, 4))

        ctk.CTkLabel(
            modal,
            text=f"Tem certeza que deseja excluir\n{nome}?\n\n"
                 f"Todos os atendimentos vinculados\ntambém serão removidos.",
            font=F.corpo(), text_color=TEXTO_MUTED,
            justify="center"
        ).pack(pady=(0, 6))

        ctk.CTkLabel(
            modal,
            text="Esta ação não pode ser desfeita.",
            font=F.mini_bold(), text_color=ERRO_TEXT
        ).pack(pady=(0, 20))

        # Botões
        btns = ctk.CTkFrame(modal, fg_color="transparent")
        btns.pack(pady=(0, 24))

        ctk.CTkButton(
            btns, text="Cancelar",
            width=120, height=ALTURA_BTN,
            fg_color="transparent", text_color=AZUL_ESCURO,
            border_width=1, border_color=AZUL_CLARO,
            hover_color=AZUL_PALE, corner_radius=RAIO_BTN,
            font=F.btn(),
            command=overlay.destroy
        ).pack(side="left", padx=(0, 12))

        ctk.CTkButton(
            btns, text="Sim, excluir",
            width=140, height=ALTURA_BTN,
            fg_color=ERRO_TEXT, text_color=BRANCO,
            hover_color="#991B1B",
            corner_radius=RAIO_BTN,
            font=F.btn_bold(),
            command=lambda: self._executar_exclusao(overlay)
        ).pack(side="left")

    def _executar_exclusao(self, overlay):
        try:
            controller.deletar_paciente(self._paciente_id)
            overlay.destroy()
            self.janela.mostrar_frame("pacientes")
        except Exception as e:
            overlay.destroy()
            self._label_feedback.configure(
                text=f"⚠  Erro ao excluir: {e}",
                text_color=ERRO_TEXT)