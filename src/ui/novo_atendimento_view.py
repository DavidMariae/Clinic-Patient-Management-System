import customtkinter as ctk
from datetime import datetime
from tkinter import messagebox
import config


class NovoAtendimentoView(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master, fg_color="transparent")
        self.controller = controller
        self._setup_ui()

    def _setup_ui(self):
        # Título da Tela
        ctk.CTkLabel(
            self,
            text="Registrar Novo Atendimento",
            font=config.FONTE_H1,
            text_color=config.COR_TEXTO_DARK,
        ).pack(pady=(0, 20), anchor="w")

        # ScrollableFrame para garantir que o formulário caiba em telas menores
        self.form_container = ctk.CTkScrollableFrame(
            self, fg_color=config.COR_CARD, corner_radius=15
        )
        self.form_container.pack(fill="both", expand=True, padx=10)

        # --- 1. SELEÇÃO DE PACIENTE ---
        self._criar_label("Paciente:")
        self.combo_paciente = ctk.CTkComboBox(
            self.form_container,
            values=self.controller.obter_nomes_pacientes(),
            width=500,
            height=40,
        )
        self.combo_paciente.pack(pady=(5, 15), padx=30, anchor="w")

        # --- 2. DATA DO ATENDIMENTO ---
        self._criar_label("Data (DD/MM/AAAA):")
        self.entry_data = ctk.CTkEntry(self.form_container, width=500, height=40)
        # Preenche automaticamente com a data de hoje
        self.entry_data.insert(0, datetime.now().strftime("%d/%m/%Y"))
        self.entry_data.pack(pady=(5, 15), padx=30, anchor="w")

        # --- 3. TIPO DE ATENDIMENTO ---
        self._criar_label("Tipo de Atendimento:")
        self.entry_tipo = ctk.CTkEntry(
            self.form_container,
            width=500,
            height=40,
            placeholder_text="Ex: Avaliação, Retorno...",
        )
        self.entry_tipo.pack(pady=(5, 15), padx=30, anchor="w")

        # --- 4. STATUS ---
        self._criar_label("Status:")
        self.combo_status = ctk.CTkComboBox(
            self.form_container,
            values=["Realizado", "Em acompanhamento"],
            width=500,
            height=40,
        )
        self.combo_status.pack(pady=(5, 15), padx=30, anchor="w")

        # --- 5. OBSERVAÇÕES ---
        self._criar_label("Observações / Prontuário:")
        self.txt_obs = ctk.CTkTextbox(
            self.form_container, width=500, height=150, font=config.FONTE_CORPO
        )
        self.txt_obs.pack(pady=(5, 20), padx=30, anchor="w")

        # --- BOTÃO SALVAR ---
        self.btn_salvar = ctk.CTkButton(
            self.form_container,
            text="Confirmar e Salvar Atendimento",
            font=config.FONTE_H2,
            fg_color=config.COR_PRINCIPAL,
            height=50,
            command=self._salvar,
        )
        self.btn_salvar.pack(pady=(10, 30), padx=30, fill="x")

    def _criar_label(self, texto):
        """Auxiliar para manter o padrão de labels"""
        ctk.CTkLabel(
            self.form_container,
            text=texto,
            font=(config.FONTE_FAMILIA, 13, "bold"),
            text_color="gray",
        ).pack(padx=30, anchor="w")

    def _salvar(self):
        # Captura e validação básica
        paciente_selecionado = self.combo_paciente.get()
        if not paciente_selecionado:
            messagebox.showwarning("Erro", "Por favor, selecione um paciente.")
            return

        # Extrair apenas o ID do paciente da string 'Nome (ID: 001)'
        try:
            paciente_id = paciente_selecionado.split("ID: ")[1].replace(")", "")
        except IndexError:
            messagebox.showerror("Erro", "Formato de paciente inválido.")
            return

        dados = {
            "paciente_id": paciente_id,
            "paciente_nome": paciente_selecionado.split(" (")[0],
            "data": self.entry_data.get(),
            "tipo": self.entry_tipo.get(),
            "status": self.combo_status.get(),
            "observacoes": self.txt_obs.get("1.0", "end").strip(),
        }

        if self.controller.salvar_atendimento(dados):
            messagebox.showinfo("Sucesso", "Atendimento registrado com sucesso!")
            self.master.master.mostrar_dashboard()
