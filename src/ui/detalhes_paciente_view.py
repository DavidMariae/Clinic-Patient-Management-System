import customtkinter as ctk
import config


class DetalhesPacienteView(ctk.CTkFrame):
    def __init__(self, master, controller, paciente):
        super().__init__(master, fg_color="transparent")
        self.controller = controller
        self.paciente = paciente
        self._setup_ui()

    def _setup_ui(self):
        # 1. Cabeçalho (Usando PACK no self)
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", pady=(0, 20))

        ctk.CTkButton(
            header,
            text="← Voltar",
            width=80,
            command=self.master.master.mostrar_tela_pacientes,
        ).pack(side="left")

        ctk.CTkLabel(
            header, text=f"Ficha: {self.paciente.nome}", font=config.FONTE_H1
        ).pack(side="left", padx=20)

        # 2. Container do Corpo (O "truque": este frame é o único outro filho do self via PACK)
        corpo_container = ctk.CTkFrame(self, fg_color="transparent")
        corpo_container.pack(fill="both", expand=True)

        # Agora configuramos o GRID apenas dentro do corpo_container
        corpo_container.grid_columnconfigure(0, weight=1)
        corpo_container.grid_columnconfigure(1, weight=2)
        corpo_container.grid_rowconfigure(0, weight=1)

        # --- LADO ESQUERDO: INFO DO PACIENTE (Usando GRID no corpo_container) ---
        info_card = ctk.CTkFrame(
            corpo_container, fg_color=config.COR_CARD, corner_radius=15
        )
        info_card.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        ctk.CTkLabel(
            info_card,
            text="DADOS PESSOAIS",
            font=(config.FONTE_FAMILIA, 12, "bold"),
            text_color="gray",
        ).pack(pady=15)

        campos = [
            ("Telefone", self.paciente.telefone),
            ("E-mail", self.paciente.email),
            ("Documento", self.paciente.documento),
            ("Nascimento", self.paciente.data_nasc),
        ]

        for label, valor in campos:
            ctk.CTkLabel(
                info_card, text=f"{label}:", font=(config.FONTE_FAMILIA, 11, "bold")
            ).pack(anchor="w", padx=20)
            ctk.CTkLabel(info_card, text=valor, font=config.FONTE_CORPO).pack(
                anchor="w", padx=20, pady=(0, 10)
            )

        # --- LADO DIREITO: HISTÓRICO (Usando GRID no corpo_container) ---
        hist_card = ctk.CTkFrame(
            corpo_container, fg_color=config.COR_CARD, corner_radius=15
        )
        hist_card.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

        ctk.CTkLabel(
            hist_card,
            text="HISTÓRICO MÉDICO",
            font=(config.FONTE_FAMILIA, 12, "bold"),
            text_color="gray",
        ).pack(pady=15)

        scroll = ctk.CTkScrollableFrame(hist_card, fg_color="transparent", height=400)
        scroll.pack(fill="both", expand=True, padx=10, pady=10)

        atendimentos = self.controller.filtrar_atendimentos_por_paciente(
            self.paciente.id
        )

        if not atendimentos:
            ctk.CTkLabel(
                scroll, text="Nenhum atendimento registrado.", text_color="gray"
            ).pack(pady=20)
        else:
            for at in atendimentos:
                self._criar_item_historico(scroll, at)

    def _criar_item_historico(self, master, at):
        item = ctk.CTkFrame(master, fg_color=config.COR_FUNDO, corner_radius=10)
        item.pack(fill="x", pady=5)

        # Linha 1: Data e Tipo
        ctk.CTkLabel(
            item,
            text=f"{at['data']} - {at['tipo']}",
            font=(config.FONTE_FAMILIA, 13, "bold"),
        ).pack(anchor="w", padx=15, pady=(10, 0))

        # Linha 2: Observações
        ctk.CTkLabel(
            item,
            text=at.get("observacoes", "Sem observações."),
            font=config.FONTE_CORPO,
            wraplength=400,
            justify="left",
        ).pack(anchor="w", padx=15, pady=(5, 10))
