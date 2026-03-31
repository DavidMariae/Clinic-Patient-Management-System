import customtkinter as ctk
import config


class NovoPacienteView(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master, fg_color="transparent")
        self.controller = controller
        self._criar_layout()

    def _criar_layout(self):
        # Título
        ctk.CTkLabel(
            self,
            text="Cadastrar Novo Paciente",
            font=config.FONTE_H1,
            text_color=config.COR_TEXTO_DARK,
        ).pack(pady=(0, 20), anchor="w")

        # Container do Formulário
        self.form_frame = ctk.CTkFrame(self, fg_color=config.COR_CARD, corner_radius=15)
        self.form_frame.pack(fill="both", expand=True, padx=2, pady=2)

        # Configurando as colunas do formulário
        self.form_frame.grid_columnconfigure((0, 1), weight=1, pad=20)

        # --- LINHA 0: NOME (OCUPA AS DUAS COLUNAS) ---
        self.entry_nome = self._add_input("Nome Completo:", 0, 0, colspan=2)

        # --- LINHA 1: DATA NASC. E TELEFONE ---
        self.entry_nasc = self._add_input(
            "Data de Nascimento:", 1, 0, placeholder="dd/mm/aaaa"
        )
        self.entry_tel = self._add_input(
            "Telefone:", 1, 1, placeholder="(00) 00000-0000"
        )

        # --- LINHA 2: E-MAIL E DOCUMENTO ---
        self.entry_email = self._add_input("E-mail:", 2, 0)

        # Frame para Documento (Label + Seletor + Entry)
        doc_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        doc_frame.grid(row=2, column=1, padx=20, pady=10, sticky="ew")

        ctk.CTkLabel(
            doc_frame, text="Documento:", font=config.FONTE_CORPO, text_color="gray"
        ).pack(anchor="w")

        self.tipo_doc = ctk.CTkSegmentedButton(
            doc_frame, values=["CPF", "RG"], height=35
        )
        self.tipo_doc.set("CPF")
        self.tipo_doc.pack(fill="x", pady=(5, 5))

        self.entry_doc = ctk.CTkEntry(
            doc_frame, height=40, placeholder_text="Digite o número..."
        )
        self.entry_doc.pack(fill="x")

        # --- BOTÕES NO RODAPÉ ---
        btn_container = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        btn_container.grid(row=3, column=0, columnspan=2, pady=40, padx=20, sticky="ew")

        self.btn_salvar = ctk.CTkButton(
            btn_container,
            text="Finalizar Cadastro",
            fg_color=config.COR_SUCESSO,
            hover_color="#27ae60",
            font=config.FONTE_PILL,
            height=45,
            command=self._on_salvar,
        )
        self.btn_salvar.pack(side="right", padx=10)

    def _add_input(self, label, row, col, colspan=1, placeholder=""):
        frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        frame.grid(
            row=row, column=col, columnspan=colspan, padx=20, pady=10, sticky="ew"
        )

        ctk.CTkLabel(
            frame, text=label, font=config.FONTE_CORPO, text_color="gray"
        ).pack(anchor="w")
        entry = ctk.CTkEntry(frame, height=40, placeholder_text=placeholder)
        entry.pack(fill="x", pady=(5, 0))
        return entry

    def _on_salvar(self):
        # Aqui você pegaria os dados e enviaria para o controller
        print(
            f"Salvando: {self.entry_nome.get()} - {self.tipo_doc.get()}: {self.entry_doc.get()}"
        )
