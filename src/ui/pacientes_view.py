import customtkinter as ctk
from tkinter import messagebox


class PacientesView(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        # Configuração de layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # 1. Barra de Busca Superior
        self.search_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.search_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")

        self.entry_busca = ctk.CTkEntry(
            self.search_frame,
            placeholder_text="Buscar por nome ou telefone...",
            height=40,
        )
        self.entry_busca.pack(side="left", fill="x", expand=True, padx=(0, 10))

        # Faz a busca disparar a cada tecla digitada
        self.entry_busca.bind("<KeyRelease>", lambda event: self.filtrar_lista())

        self.btn_buscar = ctk.CTkButton(
            self.search_frame,
            text="🔍",
            width=50,
            height=40,
            command=self.filtrar_lista,
        )
        self.btn_buscar.pack(side="right")

        # 2. Área de Rolagem para os Cards
        self.scroll_pacientes = ctk.CTkScrollableFrame(
            self,
            label_text="Pacientes Cadastrados",
            label_font=("Segoe UI", 16, "bold"),
        )
        self.scroll_pacientes.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

        # Carregar lista inicial
        self.atualizar_lista()

    def atualizar_lista(self, pacientes=None):
        """Limpa a tela e desenha os cards dos pacientes"""
        # Limpar cards antigos
        for widget in self.scroll_pacientes.winfo_children():
            widget.destroy()

        # Se não passarmos uma lista filtrada, pegamos todos
        if pacientes is None:
            pacientes = self.controller.obter_todos_pacientes()

        for p in pacientes:
            self._criar_card(p)

    def _criar_card(self, paciente):
        """Desenha um card individual para o paciente"""
        card = ctk.CTkFrame(self.scroll_pacientes)
        card.pack(fill="x", pady=5, padx=5)

        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.pack(side="left", padx=15, pady=10)

        ctk.CTkLabel(
            info_frame, text=paciente.nome, font=("Segoe UI", 14, "bold")
        ).pack(anchor="w")
        # Exibindo o telefone no card para facilitar a conferência da busca
        ctk.CTkLabel(
            info_frame, text=f"📞 {paciente.telefone}", font=("Segoe UI", 12)
        ).pack(anchor="w")

        # Botão Excluir
        btn_excluir = ctk.CTkButton(
            card,
            text="X",
            width=30,
            fg_color="#ff4d4d",
            hover_color="#cc0000",
            command=lambda p=paciente: self.confirmar_exclusao(p),
        )
        btn_excluir.pack(side="right", padx=(0, 15))

        # Botão Detalhes
        btn_ver = ctk.CTkButton(
            card,
            text="Ver Detalhes",
            width=100,
            # Chama uma função na Janela Principal para trocar a tela
            command=lambda p=paciente: self.master.master.mostrar_detalhes_paciente(p),
        )
        btn_ver.pack(side="right", padx=15)

    def filtrar_lista(self):
        termo = self.entry_busca.get()
        pacientes_filtrados = self.controller.buscar_pacientes(termo)
        self.atualizar_lista(pacientes_filtrados)

    def confirmar_exclusao(self, paciente):
        """Exibe um popup antes de deletar"""
        resposta = messagebox.askyesno(
            "Confirmar Exclusão",
            f"Tem certeza que deseja excluir o paciente {paciente.nome}?\nEsta ação não pode ser desfeita.",
        )
        if resposta:
            if self.controller.excluir_paciente(paciente.id):
                self.atualizar_lista()
