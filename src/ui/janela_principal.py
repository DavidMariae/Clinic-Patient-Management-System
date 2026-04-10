import customtkinter as ctk
from config import *
import src.ui.fonts as F

ctk.set_appearance_mode(APPEARANCE_MODE)
ctk.set_default_color_theme(COLOR_THEME)


class JanelaPrincipal(ctk.CTk):
    def __init__(self, usuario=None):
        super().__init__()
        self._usuario = usuario or {"nome": "Usuário", "nivel": ""}
        self.title(APP_TITLE)
        self.geometry(APP_GEOMETRY)
        self.minsize(APP_MIN_WIDTH, APP_MIN_HEIGHT) # Largura e altura mínima
        self.configure(fg_color=FUNDO_APP)
        self._frame_atual = None
        self._botoes_nav  = {}
        self._build_layout()
        self.mostrar_frame("dashboard")

    # ── Layout geral ────────────────────────────────────────
    def _build_layout(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self._build_sidebar()
        self.area_conteudo = ctk.CTkFrame(
            self, fg_color=FUNDO_APP, corner_radius=0)
        self.area_conteudo.grid(row=0, column=1, sticky="nsew")
        self.area_conteudo.grid_columnconfigure(0, weight=1)
        self.area_conteudo.grid_rowconfigure(0, weight=1)

    # ── Sidebar ─────────────────────────────────────────────
    def _build_sidebar(self):
        sidebar = ctk.CTkFrame(
            self, fg_color=AZUL_ESCURO,
            corner_radius=0, width=SIDEBAR_WIDTH)
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_propagate(False)
        sidebar.grid_columnconfigure(0, weight=1)
        sidebar.grid_rowconfigure(2, weight=1)

        # Linha dourada no topo
        ctk.CTkFrame(
            sidebar, fg_color=DOURADO_FORTE, height=3, corner_radius=0
        ).grid(row=0, column=0, sticky="ew")

        # Header / Logo
        self._build_header(sidebar)

        # Separador
        ctk.CTkFrame(
            sidebar, fg_color="#1E4275", height=1, corner_radius=0
        ).grid(row=2, column=0, sticky="ew")

        # Navegação
        self._build_nav(sidebar)

        # Separador
        ctk.CTkFrame(
            sidebar, fg_color="#1E4275", height=1, corner_radius=0
        ).grid(row=4, column=0, sticky="ew")

        # Footer
        self._build_footer(sidebar)

    def _build_header(self, sidebar):
        header = ctk.CTkFrame(sidebar, fg_color="transparent")
        header.grid(row=1, column=0, sticky="ew", padx=16, pady=(18, 16))
        header.grid_columnconfigure(1, weight=1)

        # Ícone da cruz
        logo_bg = ctk.CTkFrame(
            header, fg_color=AZUL_PROFUNDO,
            corner_radius=RAIO_ICONE, width=40, height=40,
            border_width=1, border_color=DOURADO_BORDA)
        logo_bg.grid(row=0, column=0, rowspan=2)
        logo_bg.grid_propagate(False)
        ctk.CTkLabel(
            logo_bg, text=LOGO,
            font=F.font(18, "bold"),
            text_color=DOURADO_FORTE
        ).place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(
            header, text="Pantokrátor",
            font=F.logo(),
            text_color=DOURADO_CLARO
        ).grid(row=0, column=1, sticky="w", padx=(12, 0))

        ctk.CTkLabel(
            header, text="GESTÃO CLÍNICA",
            font=F.logo_sub(),
            text_color=AZUL_CLARO
        ).grid(row=1, column=1, sticky="w", padx=(12, 0))

    def _build_nav(self, sidebar):
        nav = ctk.CTkFrame(sidebar, fg_color="transparent")
        nav.grid(row=3, column=0, sticky="nsew", padx=12, pady=12)
        nav.grid_columnconfigure(0, weight=1)

        # ── Seção Menu ──
        ctk.CTkLabel(
            nav, text="MENU",
            font=F.micro_bold(),
            text_color=DOURADO_FORTE
        ).grid(row=0, column=0, sticky="w", padx=8, pady=(4, 2))

        itens_menu = [
            ("dashboard",    "⊞", "Dashboard"),
            ("pacientes",    "👥", "Pacientes"),
            ("atendimentos", "📄", "Atendimentos"),
        ]
        for i, (chave, icone, label) in enumerate(itens_menu):
            self._nav_btn(nav, chave, icone, label, row=i + 1)

        # ── Seção Ações ──
        ctk.CTkLabel(
            nav, text="AÇÕES",
            font=F.micro_bold(),
            text_color=DOURADO_FORTE
        ).grid(row=5, column=0, sticky="w", padx=8, pady=(16, 2))

        itens_acao = [
            ("novo_paciente",    "＋", "Novo Paciente"),
            ("novo_atendimento", "＋", "Novo Atendimento"),
        ]
        for i, (chave, icone, label) in enumerate(itens_acao):
            self._nav_btn(nav, chave, icone, label, row=i + 6)

    def _nav_btn(self, parent, chave, icone, label, row):
        btn = ctk.CTkButton(
            parent,
            text=f"  {icone}   {label}",
            anchor="w",
            font=F.nav(),
            fg_color="transparent",
            text_color="#A8C0DC",
            hover_color=AZUL_MEDIO,
            corner_radius=RAIO_BTN,
            height=ALTURA_BTN_NAV,
            border_width=0,
            command=lambda c=chave: self.mostrar_frame(c)
        )
        btn.grid(row=row, column=0, sticky="ew", pady=1)
        self._botoes_nav[chave] = btn

    def _build_footer(self, sidebar):
        footer = ctk.CTkFrame(sidebar, fg_color="transparent")
        footer.grid(row=5, column=0, sticky="ew", padx=12, pady=14)
        footer.grid_columnconfigure(1, weight=1)

        avatar = ctk.CTkFrame(
            footer, fg_color=AZUL_PROFUNDO,
            corner_radius=20, width=34, height=34,
            border_width=1, border_color=DOURADO_BORDA)
        avatar.grid(row=0, column=0, rowspan=2)
        avatar.grid_propagate(False)
        
        nome     = self._usuario.get("nome", "U")
        iniciais = "".join([p[0].upper() for p in nome.split()[:2]])

        ctk.CTkLabel(
            avatar, text=iniciais,
            font=F.avatar(),
            text_color=DOURADO_FORTE
        ).place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(
            footer, text=self._usuario.get("nome", "Usuário"),
            font=F.pequena_bold(),
            text_color=DOURADO_CLARO
        ).grid(row=0, column=1, sticky="w", padx=(10, 0))

        ctk.CTkLabel(
            footer, text=self._usuario.get("nivel", ""),
            font=F.logo_sub(),
            text_color=AZUL_CLARO
        ).grid(row=1, column=1, sticky="w", padx=(10, 0))

    # ── Destaque nav ────────────────────────────────────────
    def _destacar_nav(self, chave):
        for k, btn in self._botoes_nav.items():
            if k == chave:
                btn.configure(
                    fg_color=AZUL_PROFUNDO,
                    text_color=DOURADO_CLARO,
                    border_width=0
                )
            else:
                btn.configure(
                    fg_color="transparent",
                    text_color="#A8C0DC",
                    border_width=0
                )

    # ── Navegação entre telas ───────────────────────────────
    def mostrar_frame(self, chave, paciente_id=None):
        if self._frame_atual:
            self._frame_atual.destroy()

        self._destacar_nav(chave)

        from src.ui.dashboard_view         import DashboardView
        from src.ui.pacientes_view         import PacientesView
        from src.ui.novo_paciente_view     import NovoPacienteView
        from src.ui.novo_atendimento_view  import NovoAtendimentoView
        from src.ui.atendimentos_view      import AtendimentosView
        from src.ui.historico_view         import HistoricoView
        from src.ui.editar_paciente_view   import EditarPacienteView

        # Telas que recebem paciente_id
        if chave == "historico" and paciente_id:
            self._frame_atual = HistoricoView(
                self.area_conteudo, self, paciente_id=paciente_id)
        elif chave == "novo_atendimento" and paciente_id:
            self._frame_atual = NovoAtendimentoView(
                self.area_conteudo, self, paciente_id=paciente_id)
        elif chave == "editar_paciente" and paciente_id:
            self._frame_atual = EditarPacienteView(
                self.area_conteudo, self, paciente_id=paciente_id)
        else:
            frames = {
                "dashboard":        DashboardView,
                "pacientes":        PacientesView,
                "atendimentos":     AtendimentosView,
                "novo_paciente":    NovoPacienteView,
                "novo_atendimento": NovoAtendimentoView,
                "historico":        HistoricoView,
                "editar_paciente":  EditarPacienteView,
            }
            cls = frames.get(chave)
            if cls:
                self._frame_atual = cls(self.area_conteudo, self)

        if self._frame_atual:
            self._frame_atual.grid(row=0, column=0, sticky="nsew")