import customtkinter as ctk
import sys, os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../../")))

from config import *
import src.ui.fonts as F
from src.controllers.clinica_controller import controller
from exceptions import AtendimentoInvalido


class LoginView(ctk.CTkToplevel):
    """
    Tela de login exibida antes da janela principal.
    Bloqueia o acesso ao sistema até autenticação válida.
    """
    def __init__(self):
        super().__init__()
        self.title("Pantokrátor — Login")
        self.geometry("860x560")
        self.resizable(False, False)
        self.configure(fg_color=FUNDO_APP)
        self._usuario_logado = None
        self._modo           = "login"  # "login" ou "cadastro"

        # Centraliza na tela
        self.update_idletasks()
        w = self.winfo_screenwidth()
        h = self.winfo_screenheight()
        x = (w - 860) // 2
        y = (h - 560) // 2
        self.geometry(f"860x560+{x}+{y}")

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._build_painel_esq()
        self._build_painel_dir()

        # Impede fechar sem autenticar
        self.protocol("WM_DELETE_WINDOW", self._ao_fechar)

    # ── Painel esquerdo (fixo) ───────────────────────────────
    def _build_painel_esq(self):
        esq = ctk.CTkFrame(
            self, fg_color=AZUL_ESCURO,
            corner_radius=0, width=340)
        esq.grid(row=0, column=0, sticky="nsew")
        esq.grid_propagate(False)

        # Linha dourada no topo
        ctk.CTkFrame(
            esq, fg_color=DOURADO_FORTE,
            height=3, corner_radius=0
        ).pack(fill="x")

        # Conteúdo centralizado
        centro = ctk.CTkFrame(esq, fg_color="transparent")
        centro.pack(expand=True)

        # Logo
        logo = ctk.CTkFrame(
            centro, fg_color=AZUL_PROFUNDO,
            corner_radius=18, width=72, height=72,
            border_width=1, border_color=DOURADO_BORDA)
        logo.pack(pady=(0, 18))
        logo.pack_propagate(False)
        ctk.CTkLabel(
            logo, text=LOGO,
            font=F.font(34),
            text_color=DOURADO_FORTE
        ).place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(
            centro, text="Pantokrátor",
            font=F.font(26, "bold"),
            text_color=DOURADO_CLARO
        ).pack()

        ctk.CTkLabel(
            centro, text="Παντοκράτωρ",
            font=F.font(12),
            text_color=DOURADO_FORTE
        ).pack(pady=(2, 16))

        # Linha decorativa
        linha = ctk.CTkFrame(centro, fg_color="transparent")
        linha.pack(fill="x", padx=30, pady=(0, 16))
        ctk.CTkFrame(
            linha, fg_color=DOURADO_FORTE,
            height=1, corner_radius=0
        ).pack(fill="x")

        self._label_desc = ctk.CTkLabel(
            centro,
            text="Sistema de Gestão de\nAtendimentos de Clínica Médica.\n\n"
                 "Acesse com suas credenciais\npara continuar.",
            font=F.pequena(),
            text_color=AZUL_CLARO,
            justify="center"
        )
        self._label_desc.pack()

    # ── Painel direito (dinâmico) ────────────────────────────
    def _build_painel_dir(self):
        self._painel_dir = ctk.CTkFrame(
            self, fg_color=FUNDO_APP, corner_radius=0)
        self._painel_dir.grid(row=0, column=1, sticky="nsew")
        self._painel_dir.grid_columnconfigure(0, weight=1)
        self._painel_dir.grid_rowconfigure(0, weight=1)
        self._mostrar_login()

    # ══════════════════════════════════════════════════════════
    # TELA DE LOGIN
    # ══════════════════════════════════════════════════════════
    def _mostrar_login(self):
        self._modo = "login"
        for w in self._painel_dir.winfo_children():
            w.destroy()

        frame = ctk.CTkFrame(
            self._painel_dir, fg_color="transparent")
        frame.grid(row=0, column=0, padx=48, pady=0)
        frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            frame, text="Bem-vindo de volta",
            font=F.titulo(), text_color=TEXTO_TITULO
        ).grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(
            frame, text="Faça login para acessar o sistema",
            font=F.corpo(), text_color=AZUL_MEDIO
        ).grid(row=1, column=0, sticky="w", pady=(4, 24))

        # Mensagem de erro
        self._label_erro_login = ctk.CTkLabel(
            frame, text="",
            font=F.pequena(), text_color=ERRO_TEXT,
            fg_color=ERRO_BG, corner_radius=RAIO_BTN
        )
        self._label_erro_login.grid(
            row=2, column=0, sticky="ew", pady=(0, 14), ipadx=12, ipady=8)
        self._label_erro_login.grid_remove()

        # Campo usuário
        ctk.CTkLabel(
            frame, text="USUÁRIO",
            font=F.label(), text_color=AZUL_ESCURO
        ).grid(row=3, column=0, sticky="w", pady=(0, 4))

        self._entry_usuario = ctk.CTkEntry(
            frame, placeholder_text="Digite seu usuário",
            height=ALTURA_INPUT, corner_radius=RAIO_INPUT,
            border_color=AZUL_CLARO, border_width=1,
            fg_color=FUNDO_INPUT, text_color=TEXTO_TITULO,
            placeholder_text_color=TEXTO_MUTED,
            font=F.corpo()
        )
        self._entry_usuario.grid(
            row=4, column=0, sticky="ew", pady=(0, 16))

        # Campo senha
        ctk.CTkLabel(
            frame, text="SENHA",
            font=F.label(), text_color=AZUL_ESCURO
        ).grid(row=5, column=0, sticky="w", pady=(0, 4))

        self._entry_senha_login = ctk.CTkEntry(
            frame, placeholder_text="Digite sua senha",
            show="•",
            height=ALTURA_INPUT, corner_radius=RAIO_INPUT,
            border_color=AZUL_CLARO, border_width=1,
            fg_color=FUNDO_INPUT, text_color=TEXTO_TITULO,
            placeholder_text_color=TEXTO_MUTED,
            font=F.corpo()
        )
        self._entry_senha_login.grid(
            row=6, column=0, sticky="ew", pady=(0, 20))

        # Bind Enter
        self._entry_usuario.bind("<Return>",
            lambda e: self._entry_senha_login.focus())
        self._entry_senha_login.bind("<Return>",
            lambda e: self._fazer_login())

        # Botão entrar
        ctk.CTkButton(
            frame, text="Entrar no Sistema",
            height=ALTURA_BTN + 4,
            fg_color=AZUL_ESCURO, text_color=DOURADO_CLARO,
            hover_color=AZUL_PROFUNDO,
            corner_radius=RAIO_BTN,
            font=F.btn_bold(),
            command=self._fazer_login
        ).grid(row=7, column=0, sticky="ew", pady=(0, 20))

        # Link cadastro
        link_frame = ctk.CTkFrame(frame, fg_color="transparent")
        link_frame.grid(row=8, column=0)

        ctk.CTkLabel(
            link_frame, text="Não tem uma conta?  ",
            font=F.pequena(), text_color=TEXTO_MUTED
        ).pack(side="left")

        ctk.CTkButton(
            link_frame, text="Cadastre-se",
            fg_color="transparent",
            text_color=AZUL_ESCURO,
            hover_color=AZUL_PALE,
            font=F.pequena_bold(),
            height=24, width=90,
            command=self._mostrar_cadastro
        ).pack(side="left")

        self._entry_usuario.focus()

    # ══════════════════════════════════════════════════════════
    # TELA DE CADASTRO
    # ══════════════════════════════════════════════════════════
    def _mostrar_cadastro(self):
        self._modo = "cadastro"
        for w in self._painel_dir.winfo_children():
            w.destroy()

        frame = ctk.CTkFrame(
            self._painel_dir, fg_color="transparent")
        frame.grid(row=0, column=0, padx=40, pady=0)
        frame.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkLabel(
            frame, text="Cadastro de Usuário",
            font=F.titulo(), text_color=TEXTO_TITULO
        ).grid(row=0, column=0, columnspan=2, sticky="w")

        ctk.CTkLabel(
            frame,
            text="Preencha os dados para criar seu acesso",
            font=F.corpo(), text_color=AZUL_MEDIO
        ).grid(row=1, column=0, columnspan=2,
               sticky="w", pady=(4, 20))

        # Erro
        self._label_erro_cad = ctk.CTkLabel(
            frame, text="",
            font=F.pequena(), text_color=ERRO_TEXT,
            fg_color=ERRO_BG, corner_radius=RAIO_BTN
        )
        self._label_erro_cad.grid(
            row=2, column=0, columnspan=2,
            sticky="ew", pady=(0, 12), ipadx=12, ipady=8)
        self._label_erro_cad.grid_remove()

        # ── Campos ──
        campos_esq = [
            ("NOME COMPLETO", "nome", "Ex: Davi Saldanha", False),
            ("SENHA",         "senha", "Mínimo 6 caracteres", True),
        ]
        campos_dir = [
            ("USUÁRIO",          "usuario", "Ex: davi.saldanha", False),
            ("CONFIRMAR SENHA",  "confirmar_senha", "Repita a senha", True),
        ]

        self._campos_cad = {}

        for row_off, (label, chave, ph, senha) in enumerate(campos_esq):
            ctk.CTkLabel(
                frame, text=label,
                font=F.label(), text_color=AZUL_ESCURO
            ).grid(row=row_off * 2 + 3, column=0,
                   sticky="w", padx=(0, 10), pady=(0, 4))

            e = ctk.CTkEntry(
                frame, placeholder_text=ph,
                show="•" if senha else "",
                height=ALTURA_INPUT, corner_radius=RAIO_INPUT,
                border_color=AZUL_CLARO, border_width=1,
                fg_color=FUNDO_INPUT, text_color=TEXTO_TITULO,
                placeholder_text_color=TEXTO_MUTED,
                font=F.corpo()
            )
            e.grid(row=row_off * 2 + 4, column=0,
                   sticky="ew", padx=(0, 10), pady=(0, 12))
            self._campos_cad[chave] = e

        for row_off, (label, chave, ph, senha) in enumerate(campos_dir):
            ctk.CTkLabel(
                frame, text=label,
                font=F.label(), text_color=AZUL_ESCURO
            ).grid(row=row_off * 2 + 3, column=1,
                   sticky="w", padx=(10, 0), pady=(0, 4))

            e = ctk.CTkEntry(
                frame, placeholder_text=ph,
                show="•" if senha else "",
                height=ALTURA_INPUT, corner_radius=RAIO_INPUT,
                border_color=AZUL_CLARO, border_width=1,
                fg_color=FUNDO_INPUT, text_color=TEXTO_TITULO,
                placeholder_text_color=TEXTO_MUTED,
                font=F.corpo()
            )
            e.grid(row=row_off * 2 + 4, column=1,
                   sticky="ew", padx=(10, 0), pady=(0, 12))
            self._campos_cad[chave] = e

        # Nível de acesso
        ctk.CTkLabel(
            frame, text="NÍVEL DE ACESSO",
            font=F.label(), text_color=AZUL_ESCURO
        ).grid(row=7, column=0, columnspan=2,
               sticky="w", pady=(0, 4))

        self._opt_nivel = ctk.CTkOptionMenu(
            frame, values=NIVEIS_ACESSO,
            height=ALTURA_INPUT, corner_radius=RAIO_INPUT,
            fg_color=FUNDO_INPUT,
            button_color=AZUL_CLARO,
            button_hover_color=AZUL_PALE,
            text_color=TEXTO_TITULO,
            font=F.corpo()
        )
        self._opt_nivel.grid(row=8, column=0, columnspan=2,
                             sticky="ew", pady=(0, 16))

        # Botão cadastrar
        ctk.CTkButton(
            frame, text="✓   Criar Conta",
            height=ALTURA_BTN + 4,
            fg_color=AZUL_ESCURO, text_color=DOURADO_CLARO,
            hover_color=AZUL_PROFUNDO,
            corner_radius=RAIO_BTN,
            font=F.btn_bold(),
            command=self._fazer_cadastro
        ).grid(row=9, column=0, columnspan=2,
               sticky="ew", pady=(0, 14))

        # Link login
        link_frame = ctk.CTkFrame(frame, fg_color="transparent")
        link_frame.grid(row=10, column=0, columnspan=2)

        ctk.CTkLabel(
            link_frame, text="Já tem uma conta?  ",
            font=F.pequena(), text_color=TEXTO_MUTED
        ).pack(side="left")

        ctk.CTkButton(
            link_frame, text="Fazer login",
            fg_color="transparent",
            text_color=AZUL_ESCURO,
            hover_color=AZUL_PALE,
            font=F.pequena_bold(),
            height=24, width=90,
            command=self._mostrar_login
        ).pack(side="left")

        self._campos_cad["nome"].focus()

    # ══════════════════════════════════════════════════════════
    # LÓGICA
    # ══════════════════════════════════════════════════════════
    def _fazer_login(self):
        usuario = self._entry_usuario.get()
        senha   = self._entry_senha_login.get()

        try:
            u = controller.autenticar(usuario, senha)
            self._usuario_logado = u
            self.destroy()
        except AtendimentoInvalido as e:
            self._label_erro_login.configure(
                text=f"  ⚠  {e}  ")
            self._label_erro_login.grid()
            self._entry_senha_login.delete(0, "end")
            self._entry_senha_login.focus()

    def _fazer_cadastro(self):
        nome    = self._campos_cad["nome"].get()
        usuario = self._campos_cad["usuario"].get()
        senha   = self._campos_cad["senha"].get()
        conf    = self._campos_cad["confirmar_senha"].get()
        nivel   = self._opt_nivel.get()

        # Valida confirmação de senha
        if senha != conf:
            self._label_erro_cad.configure(
                text="  ⚠  As senhas não coincidem.  ")
            self._label_erro_cad.grid()
            return

        try:
            controller.cadastrar_usuario(nome, usuario, senha, nivel)
            # Volta para login com mensagem de sucesso
            self._mostrar_login()
            self._label_erro_login.configure(
                text="  ✓  Conta criada! Faça login para continuar.  ",
                text_color=VERDE_TEXT,
                fg_color=VERDE_BG
            )
            self._label_erro_login.grid()
            self._entry_usuario.insert(0, usuario)
        except AtendimentoInvalido as e:
            self._label_erro_cad.configure(
                text=f"  ⚠  {e}  ")
            self._label_erro_cad.grid()

    def _ao_fechar(self):
        """Encerra o app se fechar o login sem autenticar."""
        self.master.destroy()

    @property
    def usuario_logado(self):
        return self._usuario_logado