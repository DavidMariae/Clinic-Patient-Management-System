import customtkinter as ctk

# Configuração visual global (Opcional: "blue", "green", "dark-blue")
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sistema de Gestão de Clínica")
        self.geometry("1000x600")

        # 1. Configurar o Layout de Grid (2 colunas: Menu e Conteúdo)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # 2. Criar o Menu Lateral
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")

        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame,
            text="Menu Clínica",
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Botões do Menu (Conforme o PDF do professor)
        self.btn_dashboard = ctk.CTkButton(
            self.sidebar_frame, text="Dashboard", command=self.mostrar_dashboard
        )
        self.btn_dashboard.grid(row=1, column=0, padx=20, pady=10)

        self.btn_pacientes = ctk.CTkButton(
            self.sidebar_frame, text="Pacientes", command=self.mostrar_pacientes
        )
        self.btn_pacientes.grid(row=2, column=0, padx=20, pady=10)

        self.btn_atendimentos = ctk.CTkButton(
            self.sidebar_frame, text="Atendimentos", command=self.mostrar_atendimentos
        )
        self.btn_atendimentos.grid(row=3, column=0, padx=20, pady=10)

        # 3. Área de Conteúdo (Onde as telas vão aparecer)
        self.home_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        self.label_info = ctk.CTkLabel(
            self.home_frame, text="Bem-vindo ao Sistema!", font=ctk.CTkFont(size=24)
        )
        self.label_info.pack()

    # Funções para trocar de tela (vamos preencher depois)
    def mostrar_dashboard(self):
        print("Abrindo Dashboard...")

    def mostrar_pacientes(self):
        print("Abrindo Pacientes...")

    def mostrar_atendimentos(self):
        print("Abrindo Atendimentos...")


if __name__ == "__main__":
    app = App()
    app.mainloop()
