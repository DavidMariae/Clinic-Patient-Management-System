import customtkinter as ctk
import config

# Como acrescentar a foto de álguem no cadastro de um novo cliente?

class NovoPacienteView(ctk.CTkFrame):
    def __init__(self, master, controller):
        # O 'master' será o main_frame da Janela Principal
        super().__init__(master, fg_color='transparent')
        self.controller = controller

        self._criar_layout()

    def _criar_layout(self):
        # Título da Tela
        self.lbl_titulo = ctk.CTkLabel(self, text='Cadastrar Novo Paciente', 
                                        font=config.FONTE_H1, text_color=config.COR_TEXTO_DARK)
        self.lbl_titulo.pack(pady=(0, 20), anchor='w')

        # Container do Formulário (Com fundo branco igual aos cards)
        self.form_container = ctk.CTkFrame(self, fg_color=config.COR_CARD, corner_radius=15)
        self.form_container.pack(fill='both', expand=True, padx=2, pady=2)

        # Exemplo de Campo: Nome
        self._criar_campo('Nome Completo:', 'Digite o nome do paciente')
        self._criar_campo('CPF:', '000.000.000-00')
        
        # Botão Salvar
        self.btn_salvar = ctk.CTkButton(self.form_container, text='Salvar Cadastro', 
                                         fg_color=config.COR_SUCESSO, hover_color='#27ae60',
                                         font=config.FONTE_PILL, height=40)
        self.btn_salvar.pack(pady=30, padx=20, side='bottom', fill='x')

    def _criar_campo(self, label_text, placeholder):
        """Helper para criar Label + Entry rapidamente"""
        lbl = ctk.CTkLabel(self.form_container, text=label_text, font=config.FONTE_CORPO, text_color='gray')
        lbl.pack(pady=(15, 0), padx=20, anchor='w')
        
        entry = ctk.CTkEntry(self.form_container, placeholder_text=placeholder, 
                             height=40, font=config.FONTE_CORPO)
        entry.pack(pady=(5, 10), padx=20, fill='x')
        return entry