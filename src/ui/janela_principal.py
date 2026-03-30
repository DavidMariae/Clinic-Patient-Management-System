import customtkinter as ctk
import config


class JanelaPrincipal(ctk.CTk):
    def __init__(self, controller):
        super().__init__()

        self.controller = controller  # Recebe o cérebro do sistema

        # Configurações da Janela vindas do config.py
        self.title("Clínica Pantocrator - Cuidando de você por inteiro")
        self.geometry(f"{config.LARGURA_JANELA}x{config.ALTURA_JANELA}")
        ctk.set_appearance_mode(config.TEMA_APARENCIA)
        ctk.set_default_color_theme(config.TEMA_COR)
        self.configure(fg_color=config.COR_FUNDO)

        # Layout de Grid (Coluna 0: Menu, Coluna 1: Conteúdo)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._criar_sidebar()
        self._criar_dashboard()

    # --- MENU LATERAL (SIDEBAR) ---
    def _criar_sidebar(self):
        self.sidebar_frame = ctk.CTkFrame(
            self,
            width=config.LARGURA_MENU,
            corner_radius=0,
            fg_color=config.COR_SIDEBAR,
        )
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")

        # Logo/Nome
        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame,
            text="Clínica Pantocrator",
            font=config.FONTE_H2,
            text_color=config.COR_TEXTO_LIGHT,
        )
        self.logo_label.pack(pady=(30, 40), padx=20)

        # Botões do Menu
        # Grupo de Pacientes
        self._criar_separador("PACIENTES")
        self.btn_novo_paciente = self._gerar_botao_menu(
            "Novo Paciente", 2, icone="plus"
        )
        self.btn_pacientes = self._gerar_botao_menu("Pacientes", 3, icone="users")

        # Grupo de Atendimentos
        self._criar_separador("ATENDIMENTOS")
        self.btn_novo_atendimento = self._gerar_botao_menu(
            "Novo Atendimento", 4, icone="plus-circle"
        )
        self.btn_agenda = self._gerar_botao_menu("Agenda", 5, icone="calendar")

        # Rodapé
        self.lbl_versao = ctk.CTkLabel(
            self.sidebar_frame,
            text="v 1.0.0",
            font=(config.FONTE_FAMILIA, 10),
            text_color="gray",
        )
        self.lbl_versao.pack(side="bottom", pady=20)

    def _gerar_botao_menu(self, texto, ordem, icone=None):
        """para criar botões do menu padronizados e modularizados"""
        btn = ctk.CTkButton(
            self.sidebar_frame,
            text=texto,
            height=45,
            corner_radius=8,
            fg_color="transparent",
            text_color=config.COR_TEXTO_LIGHT,
            hover_color=config.COR_BOTAO_HOVER_SIDEBAR,
            anchor="w",
            font=config.FONTE_CORPO,
        )
        btn.pack(fill="x", padx=20, pady=5)

        # O placeholder do ícone (será adicionado possteriormetne)
        if icone:
            pass  # Lógica de ícone ficará em src/utils/ui_utils.py talvez

        return btn

    def _criar_separador(self, texto):
        lbl = ctk.CTkLabel(
            self.sidebar_frame,
            text=texto,
            font=(config.FONTE_FAMILIA, 11, "bold"),
            text_color="gray",
        )
        lbl.pack(fill="x", padx=20, pady=(15, 0), anchor="w")

    # --- ÁREA DE CONTEÚDO (DASHBOARD) ---
    def _criar_dashboard(self):
        # Frame principal do conteúdo
        self.main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=30, pady=30)

        # Título
        self.lbl_titulo = ctk.CTkLabel(
            self.main_frame,
            text="Resumo Geral",
            font=config.FONTE_H1,
            text_color=config.COR_TEXTO_DARK,
        )
        self.lbl_titulo.pack(pady=(0, 30), anchor="w")

        # Container dos Cards (Lado a Lado)
        self.cards_container = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.cards_container.pack(fill="x")

        # Buscar dados reais do Controller para o Dashboard
        stats = self.controller.buscar_estatisticas()

        # Criar os 3 Cards Principais
        self._cria_card(
            "Total de Pacientes", str(stats["total_pacientes"]), config.COR_PRINCIPAL
        )
        self._cria_card(
            "Atendimentos Hoje", str(stats["atendimentos_hoje"]), config.COR_SUCESSO
        )
        self._cria_card(
            "Total Atendimentos", str(stats["total_atendimentos"]), config.COR_AVISO
        )

        # --- A NOVA TABELA DE ATENDIMENTOS ---
        self._criar_tabela_atendimentos(stats["total_atendimentos"])

    def _cria_card(self, titulo, valor, cor_destaque):
        card = ctk.CTkFrame(
            self.cards_container,
            fg_color=config.COR_CARD,
            width=250,
            height=150,
            corner_radius=15,
        )
        card.pack(side="left", padx=(0, 20))
        card.pack_propagate(False)

        # Detalhe colorido na borda esquerda
        borda = ctk.CTkFrame(card, width=5, fg_color=cor_destaque, corner_radius=0)
        borda.pack(side="left", fill="y")

        lbl_tit = ctk.CTkLabel(
            card,
            text=titulo.upper(),
            font=(config.FONTE_FAMILIA, 12, "bold"),
            text_color="gray",
        )
        lbl_tit.pack(pady=(20, 0), padx=20, anchor="w")

        lbl_val = ctk.CTkLabel(
            card,
            text=valor,
            font=config.FONTE_CARD_VALOR,
            text_color=config.COR_TEXTO_DARK,
        )
        lbl_val.pack(pady=(5, 0), padx=20, anchor="w")

    # --- TABELA DE ÚLTIMOS ATENDIMENTOS ---
    def _criar_tabela_atendimentos(self, total_atendimentos):
        # Frame Container da Tabela
        self.tabela_frame = ctk.CTkFrame(
            self.main_frame, fg_color=config.COR_CARD, corner_radius=15
        )
        self.tabela_frame.pack(fill="x", pady=(40, 0))

        # Título da Tabela
        self.lbl_tabela_tit = ctk.CTkLabel(
            self.tabela_frame,
            text="Últimos Atendimentos",
            font=config.FONTE_H2,
            text_color=config.COR_TEXTO_DARK,
        )
        self.lbl_tabela_tit.pack(pady=20, padx=20, anchor="w")

        # Frame da Grade de Dados
        self.grid_frame = ctk.CTkFrame(self.tabela_frame, fg_color="transparent")
        self.grid_frame.pack(fill="x", padx=20, pady=(0, 20))

        # Cabeçalhos da Tabela (Grid 1x4)
        self.grid_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        headers = ["Paciente", "Data", "Tipo", "Status"]
        for i, header in enumerate(headers):
            lbl = ctk.CTkLabel(
                self.grid_frame,
                text=header,
                font=(config.FONTE_FAMILIA, 13, "bold"),
                text_color="gray",
                anchor="w",
            )
            lbl.grid(row=0, column=i, sticky="ew", padx=10, pady=10)

        # Lógica para preencher com dados reais (para teste)
        if total_atendimentos > 0:
            # Aqui chamar self.controller.buscar_ultimos_atendimentos(5)
            pass  # Lógica real virá posteriormente
        else:
            # Dados de Teste
            test_data = [
                ["João Silva", "23/04/2024", "Consulta", "Realizado"],
                ["Ana Costa", "23/04/2024", "Exame", "Realizado"],
                ["Carlos Lima", "22/04/2024", "Retorno", "Em Acompanhamento"],
            ]
            for row_idx, data in enumerate(test_data):
                self._criar_atendimento_row(data, row_idx + 1)

    def _criar_atendimento_row(self, data, row_idx):
        # Cria uma linha de dados
        for col_idx, value in enumerate(data):
            # Se for a última coluna, é o status, vamos criar o "pill"
            if col_idx == 3:
                self._criar_status_pill(value, row_idx)
            else:
                lbl = ctk.CTkLabel(
                    self.grid_frame,
                    text=value,
                    font=config.FONTE_CORPO,
                    text_color=config.COR_TEXTO_DARK,
                    anchor="w",
                )
                lbl.grid(row=row_idx, column=col_idx, sticky="ew", padx=10, pady=5)

    def _criar_status_pill(self, status, row_idx):
        # Lógica de cor baseada no status
        if status == "Realizado":
            bg_cor = config.COR_STATUS_REALIZADO
            text_cor = config.COR_STATUS_REALIZADO_TEXT
        elif status == "Em Acompanhamento":
            bg_cor = config.COR_STATUS_ACOMPANHAMENTO
            text_cor = config.COR_STATUS_ACOMPANHAMENTO_TEXT
        else:
            bg_cor = "gray"
            text_cor = "white"

        # O Pill (Um frame com label dentro)
        pill = ctk.CTkFrame(
            self.grid_frame, fg_color=bg_cor, corner_radius=20, height=30
        )
        pill.grid(row=row_idx, column=3, sticky="w", padx=10, pady=5)
        pill.grid_propagate(False)  # Mantém o tamanho fixo do pill
        pill.pack_propagate(
            False
        )  # Mantém o tamanho fixo do pill (para o label dentro)

        lbl = ctk.CTkLabel(
            pill, text=status, font=config.FONTE_PILL, text_color=text_cor
        )
        lbl.pack(pady=0, padx=20, fill="both")  # Preenche o pill
