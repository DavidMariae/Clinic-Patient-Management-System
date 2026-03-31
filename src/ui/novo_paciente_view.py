import customtkinter as ctk
from tkinter import messagebox, filedialog
from PIL import Image
from src.utils.validadores import validar_email, validar_data_nascimento, validar_cpf
import config


class NovoPacienteView(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master, fg_color="transparent")
        self.controller = controller
        self.foto_path = None
        self._criar_layout()

    def _criar_layout(self):
        self.lbl_titulo = ctk.CTkLabel(
            self, text="Novo Cadastro de Paciente", font=config.FONTE_H1
        )
        self.lbl_titulo.pack(pady=(0, 20), anchor="w")

        # Container Principal
        self.form_frame = ctk.CTkFrame(self, fg_color=config.COR_CARD, corner_radius=15)
        self.form_frame.pack(fill="both", expand=True, padx=2, pady=2)
        self.form_frame.grid_columnconfigure((0, 1), weight=1)

        # --- ÁREA DA FOTO ---
        self.frame_foto = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        self.frame_foto.grid(row=0, column=0, columnspan=2, pady=20)

        self.btn_foto = ctk.CTkButton(
            self.frame_foto,
            text="＋\nFoto",
            width=100,
            height=100,
            corner_radius=50,
            fg_color="#f0f0f0",
            text_color="gray",
            hover_color="#e0e0e0",
            command=self._selecionar_foto,
        )
        self.btn_foto.pack()

        # --- CAMPOS (Usando as chaves do Controller) ---
        self.entry_nome = self._add_input(
            "Nome Completo:", 1, 0, colspan=2, placeholder="Digite o nome completo..."
        )
        self.entry_nasc = self._add_input(
            "Data de Nascimento:", 2, 0, placeholder="DD/MM/AAAA"
        )
        self.entry_tel = self._add_input(
            "Telefone:", 2, 1, placeholder="(00) 00000-0000"
        )
        self.entry_email = self._add_input(
            "E-mail:", 3, 0, placeholder="exemplo@clinica.com"
        )

        # --- DOCUMENTO ---
        doc_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        doc_frame.grid(row=3, column=1, padx=20, pady=10, sticky="ew")

        ctk.CTkLabel(
            doc_frame, text="Documento:", font=config.FONTE_CORPO, text_color="gray"
        ).pack(anchor="w")

        inner_doc_row = ctk.CTkFrame(doc_frame, fg_color="transparent")
        inner_doc_row.pack(fill="x", pady=(5, 0))

        self.tipo_doc = ctk.CTkSegmentedButton(
            inner_doc_row,
            values=["CPF", "RG"],
            command=self._ajustar_documento,
            height=28,
            width=100,
        )
        self.tipo_doc.set("CPF")
        self.tipo_doc.pack(side="left", padx=(0, 10))

        self.entry_doc = ctk.CTkEntry(
            inner_doc_row, placeholder_text="000.000.000-00", height=40
        )
        self.entry_doc.pack(side="left", fill="x", expand=True)

        # --- BOTÃO FINALIZAR ---
        self.btn_salvar = ctk.CTkButton(
            self.form_frame,
            text="Finalizar e Salvar",
            fg_color=config.COR_SUCESSO,
            width=250,
            height=45,
            font=config.FONTE_PILL,
            command=self._processar_salvamento,
        )
        self.btn_salvar.grid(row=4, column=0, columnspan=2, pady=(40, 20))

    def _ajustar_documento(self, tipo):
        placeholder = "000.000.000-00" if tipo == "CPF" else "000000000000-0"
        self.entry_doc.configure(placeholder_text=placeholder)

    def _selecionar_foto(self):
        caminho = filedialog.askopenfilename(
            filetypes=[("Imagens", "*.jpg *.png *.jpeg")]
        )
        if caminho:
            self.foto_path = caminho
            self.btn_foto.configure(text="Foto OK", fg_color="#d1e7dd")

    def _processar_salvamento(self):
        # 1. Coleta dos dados
        dados = {
            "nome": self.entry_nome.get().strip(),
            "nasc": self.entry_nasc.get().strip(),
            "tel": self.entry_tel.get().strip(),
            "email": self.entry_email.get().strip(),
            "doc": self.entry_doc.get().strip(),
            "tipo_doc": self.tipo_doc.get(),
            "foto": self.foto_path,
        }

        # 2. Validações de Preenchimento
        if not dados["nome"] or len(dados["nome"].split()) < 2:
            return messagebox.showwarning(
                "Atenção", "Digite o nome completo do paciente."
            )

        if not dados["tel"]:
            return messagebox.showwarning("Atenção", "O telefone é obrigatório.")

        if not dados["nasc"]:
            return messagebox.showwarning(
                "Atenção", "A data de nascimento é obrigatória."
            )

        if not dados["doc"]:
            return messagebox.showwarning("Atenção", "O documento é obrigatório.")

        # 3. Validações Lógicas (Utils)
        if not validar_data_nascimento(dados["nasc"]):
            return messagebox.showerror(
                "Erro", "Data de nascimento inválida (use DD/MM/AAAA)."
            )

        if dados["email"] and not validar_email(dados["email"]):
            return messagebox.showerror("Erro", "Formato de e-mail inválido.")

        if dados["tipo_doc"] == "CPF" and not validar_cpf(dados["doc"]):
            return messagebox.showerror("Erro", "CPF informado é inválido.")

        # 4. Envio para o Controller
        try:
            self.controller.cadastrar_paciente(dados)
            messagebox.showinfo(
                "Sucesso", f'Paciente {dados["nome"]} cadastrado com sucesso!'
            )
            self._limpar_campos()
        except Exception as e:
            messagebox.showerror("Erro de Sistema", f"Erro ao salvar no JSON: {e}")

    def _limpar_campos(self):
        self.entry_nome.delete(0, "end")
        self.entry_nasc.delete(0, "end")
        self.entry_tel.delete(0, "end")
        self.entry_email.delete(0, "end")
        self.entry_doc.delete(0, "end")
        self.foto_path = None
        self.btn_foto.configure(text="＋\nFoto", fg_color="#f0f0f0")

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
