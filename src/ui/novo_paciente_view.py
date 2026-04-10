import customtkinter as ctk
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

from config import *
import src.ui.fonts as F
from src.controllers.clinica_controller import controller
from src.utils.validadores import validador
from exceptions import AtendimentoInvalido


class NovoPacienteView(ctk.CTkFrame):
    def __init__(self, parent, janela):
        super().__init__(parent, fg_color=FUNDO_APP, corner_radius=0)
        self.janela = janela
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self._campos  = {}
        self._erros   = {}
        self._build_topbar()
        self._build_formulario()

    # ── Topbar ──────────────────────────────────────────────
    def _build_topbar(self):
        topbar = ctk.CTkFrame(self, fg_color="transparent")
        topbar.grid(row=0, column=0, sticky="ew",
                    padx=PAD_LATERAL, pady=(PAD_TOPO, 0))
        topbar.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            topbar, text="Novo Paciente",
            font=F.titulo(),
            text_color=TEXTO_TITULO
        ).grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(
            topbar, text="Preencha os dados para cadastrar um novo paciente",
            font=F.corpo(),
            text_color=AZUL_MEDIO
        ).grid(row=1, column=0, sticky="w")

        ctk.CTkButton(
            topbar, text="← Voltar",
            width=100, height=ALTURA_TOPBAR_BTN,
            fg_color=AZUL_PALE, text_color=AZUL_ESCURO,
            hover_color=AZUL_CLARO, corner_radius=RAIO_BTN,
            font=F.btn(),
            command=lambda: self.janela.mostrar_frame("dashboard")
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

        card = ctk.CTkFrame(
            scroll, fg_color=BRANCO,
            corner_radius=RAIO_CARD,
            border_width=1, border_color=BORDA)
        card.grid(row=0, column=0, sticky="ew")
        card.grid_columnconfigure((0, 1), weight=1)

        # Título do card
        ctk.CTkLabel(
            card, text="Dados do Paciente",
            font=F.subtitulo(),
            text_color=AZUL_PROFUNDO
        ).grid(row=0, column=0, columnspan=2,
               sticky="w", padx=PAD_CARD, pady=(PAD_CARD, 0))

        self._separador(card, row=1)

        # ── Seção: Informações pessoais ──
        self._secao(card, "Informações Pessoais", row=2)

        self._campo(
            card, "NOME COMPLETO", "nome",
            "Ex: Maria da Silva Souza",
            row=3, col=0, span=2
        )
        self._campo(
            card, "DATA DE NASCIMENTO", "data_nascimento",
            "DD/MM/AAAA",
            row=4, col=0
        )
        self._campo(
            card, "DOCUMENTO (CPF ou RG)", "documento",
            "Ex: 123.456.789-00",
            row=4, col=1
        )

        # ── Separador ──
        self._separador(card, row=5)

        # ── Seção: Contato ──
        self._secao(card, "Contato", row=6)

        self._campo(
            card, "TELEFONE", "telefone",
            "Ex: (88) 99999-9999",
            row=7, col=0
        )
        self._campo(
            card, "E-MAIL  (opcional)", "email",
            "Ex: maria@email.com",
            row=7, col=1
        )

        # ── Separador + botões ──
        self._separador(card, row=8)
        self._build_botoes(card, row=9)

        # Label feedback geral
        self._label_feedback = ctk.CTkLabel(
            card, text="",
            font=F.feedback(),
            text_color=VERDE_TEXT
        )
        self._label_feedback.grid(
            row=10, column=0, columnspan=2, pady=(0, 12))

    # ── Helpers de layout ───────────────────────────────────
    def _separador(self, parent, row):
        ctk.CTkFrame(
            parent, fg_color=BORDA, height=1, corner_radius=0
        ).grid(row=row, column=0, columnspan=2,
               sticky="ew", padx=0, pady=4)

    def _secao(self, parent, texto, row):
        ctk.CTkLabel(
            parent, text=texto.upper(),
            font=F.secao(),
            text_color=AZUL_MEDIO
        ).grid(row=row, column=0, columnspan=2,
               sticky="w", padx=PAD_CARD, pady=(8, 2))

    def _campo(self, parent, label, chave, placeholder,
               row, col, span=1):
        padx_esq = PAD_CARD if col == 0 else 10
        padx_dir = PAD_CARD if (col == 1 or span == 2) else 10

        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.grid(row=row, column=col, columnspan=span,
                   sticky="ew",
                   padx=(padx_esq, padx_dir),
                   pady=(0, 4))
        frame.grid_columnconfigure(0, weight=1)

        # Label do campo
        ctk.CTkLabel(
            frame, text=label,
            font=F.label(),
            text_color=AZUL_ESCURO
        ).pack(anchor="w", pady=(0, 4))

        # Entry
        entry = ctk.CTkEntry(
            frame,
            placeholder_text=placeholder,
            height=ALTURA_INPUT,
            corner_radius=RAIO_INPUT,
            border_color=AZUL_CLARO,
            border_width=1,
            fg_color=FUNDO_INPUT,
            text_color=TEXTO_TITULO,
            placeholder_text_color=TEXTO_MUTED,
            font=F.corpo()
        )
        entry.pack(fill="x")

        # Bind para limpar erro ao digitar
        entry.bind("<KeyRelease>",
                   lambda e, c=chave: self._limpar_erro(c))

        # Label de erro individual
        erro_label = ctk.CTkLabel(
            frame, text="",
            font=F.mini(),
            text_color=ERRO_TEXT,
            anchor="w"
        )
        erro_label.pack(anchor="w")

        self._campos[chave] = entry
        self._erros[chave]  = erro_label

    def _build_botoes(self, parent, row):
        btns = ctk.CTkFrame(parent, fg_color="transparent")
        btns.grid(row=row, column=0, columnspan=2,
                  sticky="e", padx=PAD_CARD, pady=(10, 16))

        ctk.CTkButton(
            btns, text="Limpar",
            width=110, height=ALTURA_BTN,
            fg_color="transparent",
            text_color=AZUL_ESCURO,
            border_width=1, border_color=AZUL_CLARO,
            hover_color=AZUL_PALE,
            corner_radius=RAIO_BTN,
            font=F.btn(),
            command=self._limpar
        ).pack(side="left", padx=(0, 10))

        ctk.CTkButton(
            btns, text="✓   Salvar Paciente",
            width=180, height=ALTURA_BTN,
            fg_color=AZUL_ESCURO,
            text_color=BRANCO,
            hover_color=AZUL_PROFUNDO,
            corner_radius=RAIO_BTN,
            font=F.btn_bold(),
            command=self._salvar
        ).pack(side="left")

    # ── Lógica ──────────────────────────────────────────────
    def _limpar_erro(self, chave):
        """Limpa o erro de um campo específico ao digitar."""
        if chave in self._erros:
            self._erros[chave].configure(text="")
        self._label_feedback.configure(text="")

    def _mostrar_erro_campo(self, chave, mensagem):
        """Exibe mensagem de erro abaixo do campo específico."""
        if chave in self._erros:
            self._erros[chave].configure(text=f"⚠  {mensagem}")
        if chave in self._campos:
            self._campos[chave].configure(border_color=ERRO_TEXT)

    def _resetar_bordas(self):
        """Reseta todas as bordas para o padrão."""
        for entry in self._campos.values():
            entry.configure(border_color=AZUL_CLARO)
        for erro in self._erros.values():
            erro.configure(text="")

    def _limpar(self):
        """Limpa todos os campos do formulário."""
        for entry in self._campos.values():
            entry.delete(0, "end")
        self._resetar_bordas()
        self._label_feedback.configure(text="")

    def _salvar(self):
        """Valida e salva o novo paciente."""
        self._resetar_bordas()
        self._label_feedback.configure(text="")

        nome      = self._campos["nome"].get()
        data_nasc = self._campos["data_nascimento"].get()
        documento = self._campos["documento"].get()
        telefone  = self._campos["telefone"].get()
        email     = self._campos["email"].get()

        # Validação campo a campo para mostrar erro no lugar certo
        erro_encontrado = False

        validacoes = [
            ("nome",             lambda: validador.nome(nome)),
            ("data_nascimento",  lambda: validador.data_nascimento(data_nasc)),
            ("documento",        lambda: validador.documento(documento)),
            ("telefone",         lambda: validador.telefone(telefone)),
            ("email",            lambda: validador.email(email)),
        ]

        for chave, fn in validacoes:
            try:
                fn()
            except AtendimentoInvalido as e:
                self._mostrar_erro_campo(chave, str(e))
                if not erro_encontrado:
                    # Foca no primeiro campo com erro
                    self._campos[chave].focus()
                    erro_encontrado = True

        if erro_encontrado:
            self._label_feedback.configure(
                text="⚠  Corrija os campos destacados antes de salvar.",
                text_color=ERRO_TEXT
            )
            return

        # Tudo válido — salva
        try:
            p = controller.cadastrar_paciente(
                nome, data_nasc, telefone, email, documento)
            self._label_feedback.configure(
                text=f"✓  Paciente '{p.nome}' cadastrado com sucesso!",
                text_color=VERDE_TEXT
            )
            self._limpar()
        except AtendimentoInvalido as e:
            self._label_feedback.configure(
                text=f"⚠  {e}",
                text_color=ERRO_TEXT
            )
        except Exception as e:
            self._label_feedback.configure(
                text=f"⚠  Erro inesperado: {e}",
                text_color=ERRO_TEXT
            )