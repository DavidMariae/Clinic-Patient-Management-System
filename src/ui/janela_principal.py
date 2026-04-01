import customtkinter as ctk
import config
from src.ui.novo_paciente_view import NovoPacienteView
from src.ui.pacientes_view import PacientesView


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

        # - Cria a Sidebar (Menu)
        self._criar_sidebar()

        # - Cria o Frame de Conteúdo (O 'ambiente' que nunca muda)
        self.main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=30, pady=30)

        # - Inicia na tela de Dashboard
        self.mostrar_dashboard()

    # --- NAVEGAÇÃO ---
    def _limpar_conteudo_principal(self):
        """Limpa o ambiente para a próxima tela"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def mostrar_dashboard(self):
        self._limpar_conteudo_principal()
        self._desenhar_dashboard()

    def mostrar_tela_novo_paciente(self):
        self._limpar_conteudo_principal()
        # Criando a tela dentro do main_frame
        self.tela_cadastro = NovoPacienteView(self.main_frame, self.controller)
        self.tela_cadastro.pack(fill="both", expand=True)

    def mostrar_tela_pacientes(self):
        self._limpar_conteudo_principal()
        self.tela_listagem = PacientesView(self.main_frame, self.controller)
        self.tela_listagem.pack(fill="both", expand=True)
        # Força a atualização da lista ao abrir
        self.tela_listagem.atualizar_lista()

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
        self.btn_dash = self._gerar_botao_menu("Dashboard", icone="home")
        self.btn_dash.configure(command=self.mostrar_dashboard)

        # Grupo de Pacientes
        self._criar_separador("PACIENTES")

        self.btn_novo_paciente = self._gerar_botao_menu("Novo Paciente", icone="plus")
        self.btn_novo_paciente.configure(command=self.mostrar_tela_novo_paciente)

        self.btn_pacientes = self._gerar_botao_menu("Pacientes", icone="users")
        self.btn_pacientes.configure(command=self.mostrar_tela_pacientes)

        # Grupo de Atendimentos
        self._criar_separador("ATENDIMENTOS")

        self.btn_novo_atendimento = self._gerar_botao_menu(
            "Novo Atendimento", icone="plus-circle"
        )

        self.btn_agenda = self._gerar_botao_menu("Atendimentos", icone="calendar")

        # Rodapé
        self.lbl_versao = ctk.CTkLabel(
            self.sidebar_frame,
            text="v 1.1.5",
            font=(config.FONTE_FAMILIA, 10),
            text_color="gray",
        )
        self.lbl_versao.pack(side="bottom", pady=20)

    def _gerar_botao_menu(self, texto, icone=None):
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

        # O placeholder do ícone (será adicionado posteriormetne)
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
    def _desenhar_dashboard(self):
        # Título
        self.lbl_titulo = ctk.CTkLabel(
            self.main_frame,
            text="Resumo Geral",
            font=config.FONTE_H1,
            text_color=config.COR_TEXTO_DARK,
        )
        self.lbl_titulo.pack(pady=(0, 30), anchor="w")

        # Container dos Cards
        self.cards_container = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.cards_container.pack(fill="x")

        stats = self.controller.buscar_estatisticas()

        self._cria_card(
            "Total de Pacientes", str(stats["total_pacientes"]), config.COR_PRINCIPAL
        )
        self._cria_card(
            "Atendimentos Hoje", str(stats["atendimentos_hoje"]), config.COR_SUCESSO
        )
        self._cria_card(
            "Total Atendimentos", str(stats["total_atendimentos"]), config.COR_AVISO
        )

        # Tabela
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
        card.pack_propagate(False)  # Impede ajuste automaticamente o tamanho

        borda = ctk.CTkFrame(card, width=5, fg_color=cor_destaque, corner_radius=0)
        borda.pack(side="left", fill="y")

        ctk.CTkLabel(
            card,
            text=titulo.upper(),
            font=(config.FONTE_FAMILIA, 12, "bold"),
            text_color="gray",
        ).pack(pady=(20, 0), padx=20, anchor="w")
        ctk.CTkLabel(
            card,
            text=valor,
            font=config.FONTE_CARD_VALOR,
            text_color=config.COR_TEXTO_DARK,
        ).pack(pady=(5, 0), padx=20, anchor="w")

    def _criar_tabela_atendimentos(self, total_atendimentos):
        self.tabela_frame = ctk.CTkFrame(
            self.main_frame, fg_color=config.COR_CARD, corner_radius=15
        )
        self.tabela_frame.pack(fill="x", pady=(40, 0))

        ctk.CTkLabel(
            self.tabela_frame,
            text="Últimos Atendimentos",
            font=config.FONTE_H2,
            text_color=config.COR_TEXTO_DARK,
        ).pack(pady=20, padx=20, anchor="w")

        self.grid_frame = ctk.CTkFrame(self.tabela_frame, fg_color="transparent")
        self.grid_frame.pack(fill="x", padx=20, pady=(0, 20))
        self.grid_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        headers = ["Paciente", "Data", "Tipo", "Status"]
        for i, header in enumerate(headers):
            ctk.CTkLabel(
                self.grid_frame,
                text=header,
                font=(config.FONTE_FAMILIA, 13, "bold"),
                text_color="gray",
                anchor="w",
            ).grid(row=0, column=i, sticky="ew", padx=10, pady=10)

        # Dados de Teste
        test_data = [
            ["João Silva", "23/04/2024", "Consulta", "Realizado"],
            ["Ana Costa", "23/04/2024", "Exame", "Realizado"],
            ["Carlos Lima", "22/04/2024", "Retorno", "Em Acompanhamento"],
        ]
        for row_idx, data in enumerate(test_data):
            self._criar_atendimento_row(data, row_idx + 1)

    def _criar_atendimento_row(self, data, row_idx):
        for col_idx, value in enumerate(data):
            if col_idx == 3:
                self._criar_status_pill(value, row_idx)
            else:
                ctk.CTkLabel(
                    self.grid_frame,
                    text=value,
                    font=config.FONTE_CORPO,
                    text_color=config.COR_TEXTO_DARK,
                    anchor="w",
                ).grid(row=row_idx, column=col_idx, sticky="ew", padx=10, pady=5)

    def _criar_status_pill(self, status, row_idx):
        bg_cor = (
            config.COR_STATUS_REALIZADO
            if status == "Realizado"
            else config.COR_STATUS_ACOMPANHAMENTO
        )
        txt_cor = (
            config.COR_STATUS_REALIZADO_TEXT
            if status == "Realizado"
            else config.COR_STATUS_ACOMPANHAMENTO_TEXT
        )

        pill = ctk.CTkFrame(
            self.grid_frame, fg_color=bg_cor, corner_radius=20, height=30
        )
        pill.grid(row=row_idx, column=3, sticky="w", padx=10, pady=5)
        pill.grid_propagate(False)
        pill.pack_propagate(False)

        ctk.CTkLabel(
            pill, text=status, font=config.FONTE_PILL, text_color=txt_cor
        ).pack(pady=0, padx=20, fill="both")

    def mostrar_detalhes_paciente(self, paciente):
        self._limpar_conteudo_principal()

        # Criaremos uma view simples de detalhes
        container = ctk.CTkFrame(self.main_frame)
        container.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(
            container,
            text=f"Ficha do Paciente: {paciente.nome}",
            font=("Segoe UI", 20, "bold"),
        ).pack(pady=10)

        # Grid de informações
        info_text = (
            f"ID: {paciente.id}\n"
            f"Data de Nascimento: {paciente.data_nasc}\n"
            f"Documento: {paciente.documento}\n"
            f"Telefone: {paciente.telefone}\n"
            f"E-mail: {paciente.email}"
        )

        ctk.CTkLabel(
            container, text=info_text, justify="left", font=("Segoe UI", 14)
        ).pack(pady=20)

        ctk.CTkButton(
            container, text="Voltar para Lista", command=self.mostrar_tela_pacientes
        ).pack(pady=10)
