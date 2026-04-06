import customtkinter as ctk
import config


class AtendimentosView(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master, fg_color="transparent")
        self.controller = controller
        self._setup_ui()

    def _setup_ui(self):
        # Cabeçalho e Busca
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(
            header_frame, text="Histórico de Atendimentos", font=config.FONTE_H1
        ).pack(side="left")

        # Barra de Busca (Filtro por nome do paciente)
        self.entry_busca = ctk.CTkEntry(
            header_frame, placeholder_text="Buscar paciente...", width=250
        )
        self.entry_busca.pack(side="right", padx=10)
        self.entry_busca.bind("<KeyRelease>", lambda e: self.atualizar_lista())

        # Container da Tabela
        self.main_container = ctk.CTkFrame(
            self, fg_color=config.COR_CARD, corner_radius=15
        )
        self.main_container.pack(fill="both", expand=True)

        # Cabeçalho da Tabela
        self.labels_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.labels_frame.pack(fill="x", padx=20, pady=10)
        self.labels_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        headers = ["Paciente", "Data", "Tipo", "Status"]
        for i, text in enumerate(headers):
            ctk.CTkLabel(
                self.labels_frame,
                text=text,
                font=(config.FONTE_FAMILIA, 12, "bold"),
                text_color="gray",
            ).grid(row=0, column=i, sticky="w")

        # Área de Rolagem para os Dados
        self.scroll_frame = ctk.CTkScrollableFrame(
            self.main_container, fg_color="transparent"
        )
        self.scroll_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.scroll_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.atualizar_lista()

    def atualizar_lista(self):
        # Limpa a lista atual
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        termo = self.entry_busca.get().lower()
        # Busca todos os atendimentos via controller
        atendimentos = self.controller.obter_todos_atendimentos()

        row = 0
        for at in atendimentos:
            # Lógica de filtro simples
            if termo in at.get("paciente_nome", "").lower():
                self._renderizar_linha(at, row)
                row += 1

    def _renderizar_linha(self, at, row_idx):
        # Nome do Paciente
        ctk.CTkLabel(
            self.scroll_frame, text=at.get("paciente_nome"), font=config.FONTE_CORPO
        ).grid(row=row_idx, column=0, sticky="w", pady=10, padx=10)

        # Data
        ctk.CTkLabel(
            self.scroll_frame, text=at.get("data"), font=config.FONTE_CORPO
        ).grid(row=row_idx, column=1, sticky="w", pady=10)

        # Tipo
        ctk.CTkLabel(
            self.scroll_frame, text=at.get("tipo"), font=config.FONTE_CORPO
        ).grid(row=row_idx, column=2, sticky="w", pady=10)

        # Status (Pill/Badge)
        status = at.get("status", "Realizado")
        cor_bg = (
            config.COR_STATUS_REALIZADO
            if status == "Realizado"
            else config.COR_STATUS_ACOMPANHAMENTO
        )
        cor_txt = (
            config.COR_STATUS_REALIZADO_TEXT
            if status == "Realizado"
            else config.COR_STATUS_ACOMPANHAMENTO_TEXT
        )

        pill = ctk.CTkFrame(
            self.scroll_frame, fg_color=cor_bg, corner_radius=20, height=28
        )
        pill.grid(row=row_idx, column=3, sticky="w", pady=10)
        ctk.CTkLabel(
            pill, text=status, font=config.FONTE_PILL, text_color=cor_txt
        ).pack(padx=15)
